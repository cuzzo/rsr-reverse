from rsr_reverse import RSRReverser


def test_rsrreverse_get_option_end_start():
    reverser = RSRReverser('[]/test')
    assert reverser.get_option_end() == 1


def test_rsrreverse_get_option_end_end():
    route = '/[{option}]'
    reverser = RSRReverser(route)
    pos = len(route) - 1
    assert reverser.get_option_end() == pos


def test_rsrreverse_get_option_end_middle():
    reverser = RSRReverser('/[test]/sep')
    assert reverser.get_option_end() == 6


def test_rsrreverse_get_option_end_multiple():
    reverser = RSRReverser('/sep/[test]/[end]')
    assert reverser.get_option_end() == 10


def test_rsrreverse_get_option_start_after_end():
    reverser = RSRReverser('/sep]/[test')
    assert reverser.get_option_end() == -1


def test_rsrreverse_get_option_end_none():
    reverser = RSRReverser('/no/start')
    assert reverser.get_option_end() == -1


def test_rsrreverser_get_option_end_no_end():
    reverser = RSRReverser('/[start/no/end')
    assert reverser.get_option_end() == -1


def test_rsrreverser_get_option_end_no_start():
    reverser = RSRReverser('/end]/no/start')
    assert reverser.get_option_end() == -1
