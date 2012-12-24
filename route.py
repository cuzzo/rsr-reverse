import re

RS_TYPE_PATTERN = '(%s[a-zA-Z0-9]*)?'


class InvalidParameterError(Exception):
    """Raised to signal an encounter with a syntactically invalid parameter.
    """


class RSRoute(object):
    """A Rail-Style Route.

    Attributes:
        option_bounds (str): The characters signaling the beginning and end
                             of a route option.
        param_bounds (str): The characters signaling the beginning and end
                            of a route parameter.
        param_separator (str): The character signaling the separator between
                               the parameter's name and type.
        open_terminator (str): The terminal character of a route to signal
                               that the route is open ended.

    NOTE:
        The option_bounds, param_bounds, and param_separator must all be
        regex-safe strings.
    """

    option_bounds = '[]'
    param_bounds = '{}'
    param_separator = ':'
    open_terminator = '|'

    def __init__(self, route, param_bounds=None, option_bounds=None,
                 param_separator=None, open_terminator=None):
        """Constructs a new RSRoute.

        Args:
            route (str): A Rails-sytle route.
            param_bounds (str): @see RSRoute::param_bounds.
            option_bounds (str): @see RSRoute::option_bounds.
            param_separator (str): @see RSRoute::param_separator.
            open_terminator (str): @see RSRoute::open_terminator.
        """

        self._route = route
        self.option_bounds = self.pick('option_bounds', option_bounds)
        self.param_bounds = self.pick('param_bounds', param_bounds)
        self.param_separator = self.pick('param_separator', param_separator)
        self.open_terminator = self.pick('open_terminator', open_terminator)

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


    def pick(self, attr, val):
        """Gets the matching class attribute from RSRoute if val is None.

        Args:
            attr (str): The name of the attribute to select from RSRoute.
            val (var): Any value.

        Returns (var):
            If val is None, returns the matching class attribute from
            RSRoute.  Otherwise, returns val.
        """

        val = val if val else getattr(RSRoute, attr)
        return val

    def get_option_start(self):
        """Gets the starting position of the FIRST option in THIS
        RSReverser's :route:.

        Returns (int):
            The starting position of the FIRST option or -1 if none exists.
        """

        route = self.get_route()
        start = route.find(self.option_bounds[0])
        end = route.find(self.option_bounds[1])
        if end == -1:
            return -1
        if end < start:
            return -1
        return start

    def get_option_end(self):
        """Gets the ending position of the FIRST option in THIS 
        RSReverser's :route:.

        Returns (int):
            The ending position of the FIRST option or -1 if none exists.
        """

        route = self.get_route()
        start = self.get_option_start()
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

    def get_option(self):
        """Gets the FIRST option in THIS RSReverser's :route:.

        Returns (str):
            The first option in THIS RSReverser's route or '' if none exists.

            example:
                self.route: '/eg[/{option1}]/sep[/{option2}]' -> '[/{option1}]'
                self.route: '/eg/no/options' -> ''
        """

        op_start = self.get_option_start()
        op_end = self.get_option_end()
        if op_start == -1 or op_end == -1:
            return ''
        if op_end < op_start:
            return ''
        return self.get_route()[op_start:op_end + 1]

    def clean_parameter(self, parameter):
        """Ensures that the :parameter: is syntactically valid and returns its
        name.

        Args:
            parameter (str): A route parameter string.

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
            param_type = None
        elif len(parts) == 2:
            parameter = '%s%s' % (parts[0], self.param_bounds[1])
            param_type = parts[1][:-1]
        else:
            raise InvalidParameterError
        if parameter == '':
            raise InvalidParameterError
        return parameter, param_type
