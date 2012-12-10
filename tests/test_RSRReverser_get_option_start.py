from rsr_reverse import RSRReverser


def test_rsrreverse_get_option_start_start():
    reverser = RSRReverser('[/{option}]/test')
    assert reverser.get_option_start() == 0


def test_rsrreverse_get_option_start_end():
    route = '/test[]'
    reverser = RSRReverser(route)
    pos = len(route) - 2
    assert reverser.get_option_start() == pos


def test_rsrreverse_get_option_start_middle():
    reverser = RSRReverser('/[test]/sep')
    assert reverser.get_option_start() == 1


def test_rsrreverse_get_option_start_multiple():
    reverser = RSRReverser('/sep/[test]/[end]')
    assert reverser.get_option_start() == 5


def test_rsrreverse_get_option_start_after_end():
    reverser = RSRReverser('/sep]/[test')
    assert reverser.get_option_start() == -1


def test_rsrreverse_get_option_start_none():
    reverser = RSRReverser('/no/start')
    assert reverser.get_option_start() == -1


def test_rsrreverser_get_option_start_no_end():
    reverser = RSRReverser('/[start/no/end')
    assert reverser.get_option_start() == -1


def test_rsrreverser_get_option_end_no_start():
    reverser = RSRReverser('/end]/no/start')
    assert reverser.get_option_start() == -1
