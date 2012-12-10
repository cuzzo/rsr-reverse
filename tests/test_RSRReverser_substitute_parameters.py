from reverser import RSRReverser


def test_rsrreverser_substitute_parameters_all_params():
    reverser = RSRReverser('/test/{param1}/{param2}/{param3}')
    params = {
        'param1': 'veni',
        'param2': 'vidi',
        'param3': 'vici',
    }
    sub_route = '/test/veni/vidi/vici'
    assert reverser.substitute_parameters(params) == sub_route


def test_rsrreverser_substitute_parameters_all_params_with_options():
    reverser = RSRReverser('/test/{param1}[/{param2}[/{param3}]]')
    params = {
        'param1': 'tests',
        'param2': 'are',
        'param3': 'fun',
    }
    sub_route = '/test/tests[/are[/fun]]'
    assert reverser.substitute_parameters(params) == sub_route


def test_rsrreverser_substitute_parameters_complex():
    reverser = RSRReverser('/test/{param1:digits}/{param2:type}/{param3:01}')
    params = {
        'param1': 'complex',
        'param2': 'types',
        'param3': 'sub',
    }
    sub_route = '/test/complex/types/sub'
    assert reverser.substitute_parameters(params) == sub_route


def test_rsrreverser_substitute_parameters_some_params():
    reverser = RSRReverser('/test/{param1}/{param2}/{param3}')
    params = {
        'param2': 'lucky_number_2',
    }
    sub_route = '/test/{param1}/lucky_number_2/{param3}'
    assert reverser.substitute_parameters(params) == sub_route


def test_rsrreverser_substitute_parameters_simple_matching_invalid():
    reverser = RSRReverser('/test/{_p1}/{p2;}/{p^3}')
    params = {
        '_p1': 'these',
        'p2;': 'are',
        'p^3': 'invalid_but_match',
    }
    sub_route = '/test/these/are/invalid_but_match'
    assert reverser.substitute_parameters(params) == sub_route


def test_rsrreverser_substitute_parameters_url_unsafe():
    reverser = RSRReverser('/test/{param1}/{param2}/{param3}')
    params = {
        'param1': '#$%^',
        'param2': '{param1[invalid!]}',
        'param3': '?q=;',
    }
    sub_route = '/test/#$%^/{param1[invalid!]}/?q=;'
    assert reverser.substitute_parameters(params) == sub_route


def test_rsrreverser_substitute_parameters_subset_params():
    route = '/test/{param1}/{param2}/{param3}'
    reverser = RSRReverser(route)
    params = {
        'param': 'veni',
        'aram2': 'vidi',
        'ram': 'vici',
    }
    assert reverser.substitute_parameters(params) == route


def test_rsrreverser_substitute_parameters_superset_params():
    route = '/test/{param1}/{param2}/{param3}'
    reverser = RSRReverser(route)
    params = {
        'aparam1': 'veni',
        'param2s': 'vidi',
        '{param3}': 'vici',
    }
    assert reverser.substitute_parameters(params) == route


def test_rsrreverser_substitute_parameters_no_params():
    route = '/test/{param1}/{param2}/{param3}'
    reverser = RSRReverser(route)
    params = {}
    assert reverser.substitute_parameters(params) == route


def test_rsrreverser_substitute_parameters_complex_matching_invalid():
    route = '/test/{param1:_digits}/{param2:t&}/{param3:#$*}'
    reverser = RSRReverser(route)
    params = {
        'param1': 'complex',
        'param2': 'types',
        'param3': 'sub',
    }
    assert reverser.substitute_parameters(params) == route


def test_rsrreverser_substitute_parameters_url_matches():
    route = '/test/this/case'
    reverser = RSRReverser(route)
    params = {
        'test': '1',
        'this': '2',
        'case': '3',
    }
    assert reverser.substitute_parameters(params) == route


def test_rsrreverser_substitute_parameters_custom():
    reverser = RSRReverser('/test/{param}/<param>', param_bounds='<>')
    params = {
        'param': 'fake_out',
    }
    reversed_url = '/test/{param}/fake_out'
    assert reverser.substitute_parameters(params) == reversed_url
