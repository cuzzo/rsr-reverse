import re

RSR_TYPE_PATTERN = '(%s[a-zA-Z0-9]*)?'


class InvalidParameterError(Exception):
    """Raised to signal an encounter with a syntactically invalid parameter.
    """


class RouteParameterizationIrreversibleError(Exception):
    """Raised to signal an error while attempting to reverse a route due
    an unsupplied required parameter."""


class RSRReverser(object):
    """A Rails-style route reverser.

    Attributes:
        option_bounds (str): The characters signaling the beginning and end
                             of a route option.
        param_bounds (str): The characters signaling the beginning and end
                            of a route parameter.
        param_separator (str): The character signaling the separator between
                               the parameter's name and type.

    NOTE:
        The option_bounds, param_bounds, and param_separator must all be
        regex-safe strings.
    """

    option_bounds = '[]'
    param_bounds = '{}'
    param_separator = ':'

    def __init__(self, route, option_bounds=None, param_bounds=None,
                 param_separator=None):
        """Constructs a new RSRReverser.

        Args:
            option_bounds (str): @see RSRReverser::option_bounds.
            param_bounds (str): @see RSRReverser::param_bounds.
            param_separator (str): @see RSRReverser::param_separator.
        """

        self._route = route
        self.option_bounds = self.pick('option_bounds', option_bounds)
        self.param_bounds = self.pick('param_bounds', param_bounds)
        self.param_separator = self.pick('param_separator', param_separator)
        self._param_pattern = self.extrapolate_param_pattern()

    def pick(self, attr, val):
        """Gets the matching class attribute from RSRReverser if val is None.

        Args:
            attr (str): The name of the attribute to select from RSRReverser.
            val (var): Any value.

        Returns (var):
            If val is None, returns the matching class attribute from
            RSRReverser.  Otherwise, returns val.
        """

        val = val if val else getattr(RSRReverser, attr)
        return val

    def set_route(self, route):
        """Sets THIS RSRReverser's route.

        Args:
            route (str): A Rails-style route.
        """

        self._route = route

    def get_route(self):
        """Gets THIS RSRReverser's route.

        Returns (str):
            THIS RSRReverser's route.
        """

        return self._route

    def extrapolate_param_pattern(self):
        """Extrapolates the regular expression to be used to match parameters
        based on THIS RSRReverser's :param_separator: and :param_bounds:.

        Returns (str):
            The regular expression to be used to match parameters.
        """

        type_pattern = RSR_TYPE_PATTERN % self.param_separator
        param_pattern = '%s%%s%s%s' % (self.param_bounds[0],
                                       type_pattern,
                                       self.param_bounds[1])
        return param_pattern

    def get_option_start(self, route=None):
        """Gets the starting position of the FIRST option in the :route:.

        Args:
            route (str|None): The route to search--or None to search THIS
                              RSRReverser's route.

        Returns (int):
            The starting position of the FIRST option or -1 if none exists.
        """

        route = route if route else self.get_route()

        start = route.find(self.option_bounds[0])
        end = route.find(self.option_bounds[1])
        if end == -1:
            return -1
        if end < start:
            return -1
        return start

    def get_option_end(self, route=None):
        """Gets the ending position of the FIRST option in the :route:.

        Args:
            route (str|None): The route to search--or None to search THIS
                              RSRReverser's route.

        Returns (int):
            The ending position of the FIRST option or -1 if none exists.
        """

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
        """Gets the FIRST option in the :route:.

        Args:
            route (str|None): The route to search--or None to search THIS
                              RSRReverser's route.

        Returns (str):
            The first option in the :route: or '' if none exists.

            example:
                :route: '/eg[/{option1}]/sep[/{option2}]' -> '[/{option1}]'
                :route: '/eg/no/options' -> ''
        """

        route = route if route else self.get_route()
        op_start = self.get_option_start(route)
        op_end = self.get_option_end(route)
        if op_start == -1 or op_end == -1:
            return ''
        if op_end < op_start:
            return ''
        return route[op_start:op_end + 1]

    def clean_parameter(self, parameter):
        """Ensures that the :parameter: is syntactically valid and returns its
        name.

        Args:
            parameter (str|None): A route parameter string.

        Returns (str):
            The :parameter:'s name or '' if the :parameter: is syntactically
            invalid.

        example:
            :parameter: '{param}' -> 'param'
            :parameter: '{param:digits}' -> 'param'
            :parameter: '{param:invalid:type}' -> ''
        """

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
        """Substitutes parameter values in place of parameter keys.

        Args:
            parameters (dict): A dictionary of parameter names / keys
                               and values.
            route (str|None): The route to substitute values in place of keys
                              or None to use THIS RSRReverser's route.

        Returns (str):
            The route--with the parameter keys substituted by the parameter 
            values.

            example:
                :parameters: {
                                'p1': 'examples',
                                'p2': 'are',
                                'p3': 'useful',
                             }
                :route: '/eg/{p1}/{p3}'
                
                    -> '/eg/examples/useful'
        """

        substituted_route = route if route else self.get_route()
        for param, value in parameters.iteritems():
            pattern = self._param_pattern % re.escape(param)
            matches = re.finditer(pattern, substituted_route)
            for match in matches:
                substituted_route = substituted_route.replace(match.group(),
                                                              value)
        return substituted_route

    def prune_options(self, parameters):
        """Prunes any options that cannot be replaced due to unsupplied
        parameters.

        Args:
            parameters (dict): A dictionary of parameter names / keys
                               and values.

        Returns:
            THIS RSRReverer's route--with any unsubstitutable options pruned.

            example:
                :self.route: '/eg[/{o1}[/{o2}]]/s1[/{o3}[/{o4}]]/s2[/{o5}]'
                :parameters: {
                                 'o1': 'nest_1',
                                 'o2': 'replaced',
                                 'o4': 'nest_2_not',
                                 'aside': 'neither_is_o5',
                             }
                
                    -> '/eg/{op1}/{op2}/s1/s2'
        """

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
        """Determines whether a :route: is reversed.

        Args:
            route (str|None): The route to substitute values in place of keys
                              or None to use THIS RSRReverser's route.

        Returns (bool):
            Whehter or not the route is reversed.
        """

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
        """Reverses a Rails-style route.

        Args:
            parameters (dict): A dictionary of parameter names / keys
                               and values.

        Returns (str):
            THIS RSRReverser's route--reversed given the :parameters:.

            example:
                :self.route: '/eg[/{o1}[/{o2}]]/s1[/{o3}[/{o4}]]/s2/{p1}'
                :parameters: {
                                 'o1': 'nest_1',
                                 'o2': 'replaced',
                                 'o4': 'nest_2_not',
                                 'p1': 'param_must_be_supplied',
                             }
                
                    -> '/eg/nest_1/replaced/s1/s2/param_must_be_supplied'

                :self.route: '/eg/{p1}'
                :parameters: {
                                 'aside': 'this_fials_param_must_be_supplied',
                             }
                
                    -> raises RouteParameterizationIrreversibleError  
        """

        pruned_route = self.prune_options(parameters)
        reversed_route = self.substitute_parameters(parameters, pruned_route)
        if not self.is_reversed(reversed_route):
            raise RouteParameterizationIrreversibleError
        return reversed_route
