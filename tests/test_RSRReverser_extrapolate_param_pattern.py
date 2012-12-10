from rsr_reverse import RSRReverser, RSR_TYPE_PATTERN

def test_rsrreverser_extrapolate_param_pattern_plain():
    reverser = RSRReverser('')
    type_pattern = RSR_TYPE_PATTERN % ':'
    pattern = '{%%s%s}' % type_pattern
    assert reverser.extrapolate_param_pattern() == pattern

def test_rsrreverser_extrapolate_param_pattern_custom_bounds():
    reverser = RSRReverser('', param_bounds='[]')
    type_pattern = RSR_TYPE_PATTERN % ':'
    pattern = '[%%s%s]' % type_pattern
    assert reverser.extrapolate_param_pattern() == pattern

def test_rsrreverser_extrapolate_param_pattern_custom_separator():
    reverser = RSRReverser('', param_separator='|')
    type_pattern = RSR_TYPE_PATTERN % '|'
    pattern = '{%%s%s}' % type_pattern
    assert reverser.extrapolate_param_pattern() == pattern

def test_rsrreverser_extrapolate_param_pattern_custom_bounds_and_separator():
    reverser = RSRReverser('', param_bounds='[]', param_separator='|')
    type_pattern = RSR_TYPE_PATTERN % '|'
    pattern = '[%%s%s]' % type_pattern
    assert reverser.extrapolate_param_pattern() == pattern

