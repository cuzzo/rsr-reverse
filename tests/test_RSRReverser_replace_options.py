from reverse import RSRReverser

def test_rsrreverser_replace_options_full():
    reverser = RSRReverser('/test[/{option1}][/{option2}][/{option3}]')
    params = {
        'option1': 'options',
        'option2': 'are',
        'option3': 'fun',
    }
    replaced_route = '/test/{option1}/{option2}/{option3}'
    assert reverser.replace_options(params) == replaced_route

def test_rsrreverser_replace_options_some():
    reverser = RSRReverser('/test[/{option1}][/{option2}][/{option3}]')
    params = {
        'option2': 'some',
    }
    replaced_route = '/test/{option2}'
    assert reverser.replace_options(params) == replaced_route

def test_rsrreverser_replace_options_nested():
    reverser = RSRReverser('/test[/{option1}[/{option2}]][/{option3}]')
    params = {
        'option1': 'some',
        'option2': 'nest',
    }
    replaced_route = '/test/{option1}/{option2}'
    assert reverser.replace_options(params) == replaced_route

def test_rsrreverser_replace_options_nested_no_parent():
    reverser = RSRReverser('/test[/{option1}[/{option2}]][/{option3}]')
    params = {
        'option2': 'no_parent_nest',
        'option3': 'replace',
    }
    replaced_route = '/test/{option3}'
    assert reverser.replace_options(params) == replaced_route

def test_rsrreverser_replace_options_nested_incomplete():
    reverser = RSRReverser('/test[/{option1}[/{option2}]][/{option3}]')
    params = {
        'option1': 'incomplete_nest',
        'option3': 'replace',
    }
    replaced_route = '/test/{option1}/{option3}'
    assert reverser.replace_options(params) == replaced_route

def test_rsrreverser_replace_options_none():
    reverser = RSRReverser('/test[/{option1}][/{option2}][/{option3}]')
    params = {
        'param1': 'nothing',
        'param2': 'to',
        'param3': 'see',
        'param4': 'here',
    }
    replaced_route = '/test'
    assert reverser.replace_options(params) == replaced_route

def test_rsrreverser_replace_options_unsafe():
    reverser = RSRReverser('/test[/{option1}][/{option2}][/{option3}]')
    params = {
        'param1': 'nothing',
        'param2': 'to',
        'param3': 'see',
        'param4': 'here',
    }
    replaced_route = '/test'
    assert reverser.replace_options(params) == replaced_route
   
def test_rsrreverser_replace_options_invalid():
    reverser = RSRReverser('/test[/{_o1}][/{o2;}][/{o^3}]')
    params = {
        '_o1': 'invalid',
        'o2;': 'but',
        'o^3': 'subs',
    }
    replaced_route = '/test/{_o1}/{o2;}/{o^3}'
    assert reverser.replace_options(params) == replaced_route

