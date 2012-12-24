#! /usr/bin/env python

import re
import copy

from route import RSRoute, InvalidParameterError


class RSRParser(object):
    
    patterns = {
        'word': r'\w+',
        'alpha': r'[a-zA-Z]+',
        'digits': r'\d+',
        'number': r'\d*.?\d+',
        'chunk': r'[^/^.]+',
        'segment': r'[^/]+',
        'any': r'.+',
    }
    default_pattern = 'chunk'

    def __init__(self, route, patterns=None, default_pattern=None):
        self.route = copy.copy(route)
        self.patterns = self.pick('patterns', patterns)
        self.param_pattern = self.extrapolate_param_pattern()
        self.default_pattern = self.pick('default_pattern', default_pattern)

    def pick(self, attr, val):
        """Gets the matching class attribute from RSRParser if val is None.

        Args:
            attr (str): The name of the attribute to select from RSRParser.
            val (var): Any value.

        Returns (var):
            If val is None, returns the matching class attribute from
            RSRParser.  Otherwise, returns val.
        """

        val = val if val else getattr(RSRParser, attr)
        return val

    def extrapolate_param_pattern(self):
        pattern = '%s[a-zA-Z_][a-zA-Z0-9_]*(%s%s)?%s' % (
                                          self.route.param_bounds[0],
                                          self.route.param_separator,
                                          '\w+',
                                          self.route.param_bounds[1])             
        return pattern

    def escape_route(self, route):
        route = route.replace('<', '#~#').replace('>', '#@#')
        route = route.replace('[', ':~:').replace(']', ':@:')
        route = route.replace('(', '=~=').replace(')', '=@=')
        return route

    def unescape_route(self, route):
        route = route.replace(':~:', '[').replace(':@:', ']')
        route = route.replace('=~=', '(').replace('=@=', ')')
        route = route.replace('#~#', '<').replace('#@#', '>')
        return route

    def substitute_capture_pattern(self, route, optional=False):
        matches = re.finditer(self.param_pattern, route)
        for match in matches:
            param, param_type = self.route.clean_parameter(match.group())
            if not param_type:
                type_pattern = self.patterns[self.default_pattern]
            elif param_type in self.patterns.keys():
                type_pattern = self.patterns[param_type]
            else:
                raise InvalidParameterError
            capture_pattern = '(?P<%s>%s)' % (param[1:-1], type_pattern)
            capture_pattern = self.escape_route(capture_pattern)
            route = route.replace(match.group(), capture_pattern)
            if optional:
                route = self.escape_route('(%s)?') % route
        return route

    def parser_factory(self, route):
        parser = copy.copy(self)
        parser.route.set_route(route)
        return parser
                              
    def parse(self, optional=False):
        route = self.route.get_route()
        while True:
            option = self.route.get_option()
            if option == '':
                break
            parser = self.parser_factory(option[1:-1])
            option_pattern = parser.parse(True)
            route = route.replace(option, option_pattern)
            self.route.set_route(route)
        route = self.substitute_capture_pattern(route, optional)
        if not optional:
            route = self.unescape_route(route)
        return route
