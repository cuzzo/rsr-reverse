from reverser import RSRReverser


def test_rsrreverser_is_reversed_happy():
    reverser = RSRReverser('/test/is/reversed')
    assert reverser.is_reversed() == True


def test_rsrreverser_is_reversed_url_unsafe():
    reverser = RSRReverser('/test/*is/unsafe;')
    assert reverser.is_reversed() == True


def test_rsrreverser_is_reversed_params():
    reverser = RSRReverser('/test/{is}/not/{reversed}')
    assert reverser.is_reversed() == False


def test_rsrreverser_is_reversed_options():
    reverser = RSRReverser('/test[/{is}][/{not}][/{reversed}]')
    assert reverser.is_reversed() == False


def test_rsrreverser_is_reversed_paramless_option():
    reverser = RSRReverser('/test[/is][/not][/reverser]')
    assert reverser.is_reversed() == False


def test_rsrreverser_is_reversed_nested_options():
    reverser = RSRReverser('/test[/is[/not[/reversed]]]')
    assert reverser.is_reversed() == False


def test_rsrreverser_is_reversed_params_and_options():
    reverser = RSRReverser('/test/{is}[/not][/{reversed]')
    assert reverser.is_reversed() == False


def test_rsrreverser_is_reversed_asymmteric_option():
    reverser = RSRReverser('/test/[is/not/reversed')
    assert reverser.is_reversed() == False


def test_rsrreverser_is_reversed_asymmetric_param():
    reverser = RSRReverser('test/{is/not/reversed')
    assert reverser.is_reversed() == False
