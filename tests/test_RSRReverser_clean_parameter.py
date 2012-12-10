from nose.tools import raises

from reverser import RSRReverser, InvalidParameterError


def test_rsrreverser_clean_parameter_simple():
    reverser = RSRReverser('')
    assert reverser.clean_parameter('param') == 'param'


def test_rsrreverser_clean_parameter_simple_enclosed():
    reverser = RSRReverser('')
    assert reverser.clean_parameter('{param}') == '{param}'


def test_rsrreverser_clean_parameter_complex():
    reverser = RSRReverser('')
    assert reverser.clean_parameter('complex_param:type') == 'complex_param'


def test_rsrreverser_clean_parameter_simple_invalid():
    reverser = RSRReverser('')
    assert reverser.clean_parameter('#+*&') == '#+*&'


def test_rsrreverser_clean_parameter_complex_invalid():
    reverser = RSRReverser('')
    assert reverser.clean_parameter('#+*&:type') == '#+*&'


@raises(InvalidParameterError)
def test_rsrreverser_clean_parameter_complex_multi_separator():
    reverser = RSRReverser('')
    reverser.clean_parameter('param:type:bad') 


@raises(InvalidParameterError)
def test_rsrreverser_clean_parameter_empty():
    reverser = RSRReverser('')
    reverser.clean_parameter('')
