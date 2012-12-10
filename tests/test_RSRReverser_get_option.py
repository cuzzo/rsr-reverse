from reverser import RSRReverser


def test_rsrreverser_get_option_happy_full_option():
    reverser = RSRReverser('[/{option1}/{option2}]')
    assert reverser.get_option() == '[/{option1}/{option2}]'


def test_rsrreverser_get_option_happy_starting_option():
    reverser = RSRReverser('[/{start_op}]/test/{param}')
    assert reverser.get_option() == '[/{start_op}]'


def test_rsrreverser_get_option_happy_ending_option():
    reverser = RSRReverser('/test/{param}[/{end_op}]')
    assert reverser.get_option() == '[/{end_op}]'


def test_rsrreverser_get_option_happy_middle_option():
    reverser = RSRReverser('/test[/{mid_op}]/{param}')
    assert reverser.get_option() == '[/{mid_op}]'


def test_rsrreverser_get_option_happy_multiple_options():
    reverser = RSRReverser('/test[/{option1}]/sep[/{option2]')
    assert reverser.get_option() == '[/{option1}]'


def test_rsrreverser_get_option_happy_nested_option():
    reverser = RSRReverser('/test[/{option}[/sep/{nested_option}]]')
    assert reverser.get_option() == '[/{option}[/sep/{nested_option}]]'


def test_rsrreverser_get_option_no_start():
    reverser = RSRReverser('/test/{option}]/sep')
    assert reverser.get_option() == ''


def test_rsrreverser_get_option_no_end():
    reverser = RSRReverser('/test[/{option}/end')
    assert reverser.get_option() == ''


def test_rsrreverser_get_option_ilformat():
    reverser = RSRReverser('/test]/sep[/{good_option}]')
    assert reverser.get_option() == ''


def test_rsrreverser_get_option_custom():
    reverser = RSRReverser('test[/{fake_out}]</{option}>', option_bounds='<>')
    assert reverser.get_option() == '</{option}>'
