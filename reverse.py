import re
import copy

from route import RSRoute, RS_TYPE_PATTERN, InvalidParameterError


class RouteParameterizationIrreversibleError(Exception):
    """Raised to signal an error while attempting to reverse a route due
    an unsupplied required parameter."""


class RSRReverser(object):
    """A Rails-style route reverser."""

    def __init__(self, route):
        """Constructs a new RSRReverser.

        Args:
            route (RSRoute): the route to reverse.
        """

        self.route = copy.copy(route)
        self.param_pattern = self.extrapolate_param_pattern()

    def extrapolate_param_pattern(self):
        """Extrapolates the regular expression to be used to match parameters
        based on THIS RSRReverser's RSRoute's :param_bounds: and 
        :param_separator:.

        Returns (str):
            The regular expression to be used to match parameters.
        """

        type_pattern = RS_TYPE_PATTERN % self.route.param_separator
        param_pattern = '%s%%s%s%s' % (self.route.param_bounds[0],
                                       type_pattern,
                                       self.route.param_bounds[1])
        return param_pattern


    def reverser_factory(self, route):
        rs_route = copy.copy(self.route)
        rs_route.set_route(route)
        return RSRReverser(rs_route)

    def substitute_parameters(self, parameters):
        """Substitutes parameter values in place of parameter keys.

        Args:
            parameters (dict): A dictionary of parameter names / keys
                               and values.

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

        substituted_route = self.route.get_route() 
        for param, value in parameters.iteritems():
            pattern = self.param_pattern % re.escape(param)
            matches = re.finditer(pattern, substituted_route)
            for match in matches:
                substituted_route = substituted_route.replace(match.group(),
                                                              value)
        return substituted_route

    def prune_options(self, parameters):
        """Prunes any options that cannot be replaced due to unsupplied
        parameters.  Sets THIS RSReverser's route to the pruned route.

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

        while True:
            option = self.route.get_option()
            if option == '':
                return self.route.get_route()

            option_reverser = self.reverser_factory(option[1:-1])
            option_reverser.prune_options(parameters)
            substituted_route = option_reverser.substitute_parameters(
                                                            parameters)
            route = self.route.get_route()
            if self.is_reversed(substituted_route):
                route = route.replace(option, option[1:-1])
            else:
                route = route.replace(option, '')
            self.route.set_route(route)

    def is_reversed(self, route=None):
        """Determines whether a :route: is reversed.

        Args:
            route (str|None): The route to substitute values in place of keys
                              or None to use THIS RSRReverser's route.

        Returns (bool):
            Whehter or not the route is reversed.
        """

        route = route if route else self.route.get_route()
        if route.find(self.route.option_bounds[0]) != -1:
            return False
        if route.find(self.route.option_bounds[1]) != -1:
            return False
        if route.find(self.route.param_bounds[0]) != -1:
            return False
        if route.find(self.route.param_bounds[1]) != -1:
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

        self.prune_options(parameters)
        reversed_route = self.substitute_parameters(parameters)
        if not self.is_reversed(reversed_route):
            raise RouteParameterizationIrreversibleError
        return reversed_route
