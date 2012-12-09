import re

RSR_TYPE_PATTERN = '(%s[a-zA-Z0-9]*)?'


class InvalidParameterError(Exception):
    """Raised to signal an encounter with a syntactically invalid parameter.
    """


class RouteParameterizationIrreversibleError(Exception):
    """Raised to signal an error while attempting to reverse a route due
    an unsupplied required parameter."""


class RSRReverser(object):
    option_bounds = '[]'
    param_bounds = '{}'
    param_separator = ':'

    def __init__(self, route, option_bounds=None, param_bounds=None,
                 param_separator=None):

        self._route = route
        self.option_bounds = self.pick('option_bounds', option_bounds)
        self.param_bounds = self.pick('param_bounds', param_bounds)
        self.param_separator = self.pick('param_separator', param_separator)
        self._param_pattern = self.extrapolate_param_pattern()

    def pick(self, attr, val):
        val = val if val else getattr(RSRReverser, attr)
        return val

    def set_route(self, route):
        self._route = route

    def get_route(self):
        return self._route

    def extrapolate_param_pattern(self):
        type_pattern = RSR_TYPE_PATTERN % self.param_separator
        param_pattern = '%s%%s%s%s' % (self.param_bounds[0],
                                       type_pattern,
                                       self.param_bounds[1])
        return param_pattern

    def get_option_start(self, route=None):
        route = route if route else self.get_route()

        start = route.find(self.option_bounds[0])
        end = route.find(self.option_bounds[1])
        if end == -1:
            return -1
        if end < start:
            return -1
        return start

    def get_option_end(self, route=None):
        route = route if route else self.get_route()

        start = self.get_option_start(route)
        if start == -1:
            return -1

        pos = start
        opts = 1
        while opts > 0:
            pos += 1
            if pos >= len(route):
                return -1

            char = route[pos]
            if char not in self.option_bounds:
                continue

            if char == self.option_bounds[0]:
                opts += 1

            if char == self.option_bounds[1]:
                opts -= 1

        return pos

    def get_option(self, route=None):
        route = route if route else self.get_route()
        op_start = self.get_option_start(route)
        op_end = self.get_option_end(route)
        if op_start == -1 or op_end == -1:
            return ''
        if op_end < op_start:
            return ''
        return route[op_start:op_end + 1]

    def clean_parameter(self, parameter):
        parts = parameter.split(self.param_separator)
        if len(parts) == 1:
            pass
        elif len(parts) == 2:
            parameter = parts[0]
        else:
            raise InvalidParameterError
        if parameter == '':
            raise InvalidParameterError
        return parameter

    def substitute_parameters(self, parameters, route=None):
        substituted_route = route if route else self.get_route()
        for param in parameters.keys():
            pattern = self._param_pattern % re.escape(param)
            matches = re.finditer(pattern, substituted_route)
            for match in matches:
                substituted_route = substituted_route.replace(match.group(),
                                                            parameters[param])
        return substituted_route

    def prune_options(self, parameters):
        route = self.get_route()
        while True:
            option = self.get_option(route)
            if option == '':
                return route

            option_reverser = RSRReverser(option[1:-1],
                                    option_bounds=self.option_bounds,
                                    param_bounds=self.param_bounds,
                                    param_separator=self.param_separator)

            pruned_route = option_reverser.prune_options(parameters)

            substituted_route = option_reverser.substitute_parameters(
                                                            parameters,
                                                            pruned_route)
            if self.is_reversed(substituted_route):
                route = route.replace(option, option[1:-1])
            else:
                route = route.replace(option, '')

    def is_reversed(self, route=None):
        route = route if route else self.get_route()
        if route.find(self.option_bounds[0]) != -1:
            return False
        if route.find(self.option_bounds[1]) != -1:
            return False
        if route.find(self.param_bounds[0]) != -1:
            return False
        if route.find(self.param_bounds[1]) != -1:
            return False
        return True

    def reverse(self, parameters):
        pruned_route = self.prune_options(parameters)
        reversed_route = self.substitute_parameters(parameters, pruned_route)
        if not self.is_reversed(reversed_route):
            raise RouteParameterizationIrreversibleError
        return reversed_route
