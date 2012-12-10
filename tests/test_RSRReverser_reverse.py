from nose.tools import raises

from rsr_reverse import RSRReverser, RouteParameterizationIrreversibleError


def test_rsrreverser_reverse_full_params():
    reverser = RSRReverser('/test/{param1}/{param2}/{param3}')
    params = {
        'param1': 'params',
        'param2': 'are',
        'param3': 'fun',
    }
    reversed_url = '/test/params/are/fun'
    assert reverser.reverse(params) == reversed_url


def test_rsrreverser_reverse_full_options():
    reverser = RSRReverser('/test[/{param1}][/{param2}][/{param3}]')
    params = {
        'param1': 'options',
        'param2': 'are',
        'param3': 'fun',
    }
    reversed_url = '/test/options/are/fun'
    assert reverser.reverse(params) == reversed_url


def test_rsrreverser_reverse_full_params_and_options():
    reverser = RSRReverser('/test[/{param1}]/{param2}[/{param3}]')
    params = {
        'param1': 'options',
        'param2': 'and',
        'param3': 'params_are_fun',
    }
    reversed_url = '/test/options/and/params_are_fun'
    assert reverser.reverse(params) == reversed_url


def test_rsrreverser_reverse_full_nested_options():
    reverser = RSRReverser('/test[/{param1}[/{param2}[/{param3}]]]')
    params = {
        'param1': 'nested',
        'param2': 'options',
        'param3': 'are_fun',
    }
    reversed_url = '/test/nested/options/are_fun'
    assert reverser.reverse(params) == reversed_url


@raises(RouteParameterizationIrreversibleError)
def test_rsrreverser_reverse_some_params():
    reverser = RSRReverser('/test/{param1}/{param2}/{param3}')
    params = {
        'param1': 'epic',
        'param2': 'fail',
    }
    reverser.reverse(params)


def test_rsrreverser_reverse_some_options():
    reverser = RSRReverser('/test[/{param1}][/{param2}][/{param3}]')
    params = {
        'param2': 'some',
        'param3': 'options',
    }
    reversed_url = '/test/some/options'
    assert reverser.reverse(params) == reversed_url


@raises(RouteParameterizationIrreversibleError)
def test_rsrreverser_reverse_some_params_and_options():
    reverser = RSRReverser('/test[/{param1}]/{param2}[/{param3}]/{param4}')
    params = {
        'param2': 'some',
        'param3': 'options',
    }
    reverser.reverse(params)


def test_rsrreverser_reverse_some_nested_options():
    route = '/test[/{param1}[/{param2}]]/sep[/{param3}[/{param4}]]'
    reverser = RSRReverser(route)
    params = {
        'param3': 'some',
        'param4': 'nested_options',
    }
    reversed_url = '/test/sep/some/nested_options'
    assert reverser.reverse(params) == reversed_url


def test_rsrreverser_reverse_nested_option_no_parent():
    route = '/test[/{param1}[/{param2}]]/sep[/{param3}[/{param4}]]'
    reverser = RSRReverser(route)
    params = {
        'param2': 'some',
        'param4': 'nested_options',
    }
    reversed_url = '/test/sep'
    assert reverser.reverse(params) == reversed_url


def test_rsrreverser_reverse_nested_incomplete():
    route = '/test[/{param1}[/{param2}]]/sep[/{param3}[/{param4}]]'
    reverser = RSRReverser(route)
    params = {
        'param1': 'some',
        'param3': 'nested_options',
    }
    reversed_url = '/test/some/sep/nested_options'
    assert reverser.reverse(params) == reversed_url


def test_rsrreverser_reverse_none():
    route = '/test[/{param1}[/{param2}]]/sep[/{param3}[/{param4}]]'
    reverser = RSRReverser(route)
    params = {
        'param1': 'some',
        'param3': 'nested_options',
    }
    reversed_url = '/test/some/sep/nested_options'
    assert reverser.reverse(params) == reversed_url


def test_rsrreverser_reverse_unsafe():
    reverser = RSRReverser('/test/{param1}/{param2}/{param3}')
    params = {
        'param1': '#$%^',
        'param2': 'unsafe_',
        'param3': ';unsafe'
    }
    reversed_url = '/test/#$%^/unsafe_/;unsafe'
    assert reverser.reverse(params) == reversed_url


def test_rsrreverser_reverse_invalid_param():
    reverser = RSRReverser('/test/{_p1}/{p2;}/{p^3}')
    params = {
        '_p1': 'invalid',
        'p2;': 'but',
        'p^3': 'subs'
    }
    reversed_url = '/test/invalid/but/subs'
    assert reverser.reverse(params) == reversed_url


def test_rsrreverser_reverse_invalid_option():
    reverser = RSRReverser('/test[/{_p1}][/{p2;}][/{p^3}]')
    params = {
        '_p1': 'invalid',
        'p2;': 'but',
        'p^3': 'subs'
    }
    reversed_url = '/test/invalid/but/subs'
    assert reverser.reverse(params) == reversed_url


def test_rsrreverer_reverse_plain():
    route = '/test/plain/route'
    reverser = RSRReverser(route)
    params = {
        'param1': 'test',
        'param2': 'no_sub',
    }
    assert reverser.reverse(params) == route
