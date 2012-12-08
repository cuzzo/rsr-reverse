#! /usr/bin/env python

import re

class InvalidParameterError(Exception):
  """ """

class RouteParameterizationIrreversibleError(Exception):
  """ """

class RSRReverser(object):
  option_enclosures = '[]'
  param_enclosures = '{}'
  param_separator = ':'
  
  def __init__(self, route, option_enclosures=None, param_enclosures=None, \
               param_separator=None):

    self._route = route
    self.option_enclosures = self.pick('option_enclosures', option_enclosures)
    self.param_enclosures = self.pick('param_enclosures', param_enclosures)
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
    type_pattern = '(%s[a-zA-Z0-9]*)?' % self.param_separator
    param_pattern = '%s%%s%s%s' % (self.param_enclosures[0], \
                                         type_pattern, \
                                         self.param_enclosures[1])
    return param_pattern


  def get_option_start(self):
    start = self.get_route().find(self.option_enclosures[0])
    end = self.get_route().find(self.option_enclosures[1])
    if end == -1:
      return -1
    if end < start:
      return -1
    return start

  def get_option_end(self):
    start = self.get_option_start()
    if start == -1:
      return -1

    pos = start
    opts = 1
    while opts > 0:
      pos += 1  
      if pos >= len(self.get_route()):
        return -1

      char = self.get_route()[pos]
      if char not in self.option_enclosures:
        continue

      if char == self.option_enclosures[0]:
        opts += 1

      if char == self.option_enclosures[1]:
        opts -=1

    return pos

  def get_option(self):
    op_start = self.get_option_start()
    op_end = self.get_option_end()
    if op_start == -1 or op_end == -1:
      return ''
    if op_end < op_start:
      return ''
    return self.get_route()[op_start:op_end + 1]

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

  def substitute_parameters(self, parameters):
    substituted_route = self.get_route()
    for param in parameters.keys():
      pattern = self._param_pattern % param
      pattern = re.compile(pattern)
      matches = pattern.finditer(substituted_route)
      for match in matches:
        substituted_route = substituted_route.replace(match.group(), \
                                                      parameters[param])
    return substituted_route

  def replace_options(self, parameters):
    while True:
      option = self.get_option()
      if option == '':
        return self.get_route()
      
      option_reverser = RSRReverser(option[1:-1])
      try:
        option_reverser.reverse(parameters)
        sub_route = option_reverser.get_route()
      except RouteParameterizationIrreversibleError:
        sub_route = ''
      route = self.get_route().replace(option, sub_route)
      self.set_route(route)

  def reverse(self, parameters):
    self.replace_options(parameters)
    substituted_route = self.substitute_parameters(parameters)

    if re.search('{.*?}', substituted_route):
      raise RouteParameterizationIrreversibleError
    self.set_route(substituted_route)
    return self.get_route()

