from likepy.restricted_builtins import limited_list, limited_range, limited_tuple
import pytest


def test_limited_range_length_1():
    result = limited_range(1)
    assert result == range(0, 1)


def test_limited_range_length_10():
    result = limited_range(10)
    assert result == range(0, 10)


def test_limited_range_5_10():
    result = limited_range(5, 10)
    assert result == range(5, 10)


def test_limited_range_5_10_sm1():
    result = limited_range(5, 10, -1)
    assert result == range(5, 10, -1)


def test_limited_range_15_10_s2():
    result = limited_range(15, 10, 2)
    assert result == range(15, 10, 2)


def test_limited_range_no_input():
    with pytest.raises(TypeError):
        limited_range()


def test_limited_range_more_steps():
    with pytest.raises(AttributeError):
        limited_range(0, 0, 0, 0)


def test_limited_range_zero_step():
    with pytest.raises(ValueError):
        limited_range(0, 10, 0)


def test_limited_range_range_overflow():
    with pytest.raises(ValueError) as excinfo:
        limited_range(0, 5000, 1)
    assert (
        'To be created range() object would be to large, '
        'in RestrictedPython we only allow 1000 elements in a range.'
        in str(excinfo.value)
    )


def test_limited_list_valid_list_input():
    input = [1, 2, 3]
    result = limited_list(input)
    assert result == input


def test_limited_list_invalid_string_input():
    with pytest.raises(TypeError):
        limited_list('input')


def test_limited_tuple_valid_list_input():
    input = [1, 2, 3]
    result = limited_tuple(input)
    assert result == tuple(input)


def test_limited_tuple_invalid_string_input():
    with pytest.raises(TypeError):
        limited_tuple('input')



def test_string_in_utility_builtins():
    import string
    from likepy.restricted_builtins import utility_builtins
    assert utility_builtins['string'] is string


def test_math_in_utility_builtins():
    import math
    from likepy.restricted_builtins import utility_builtins
    assert utility_builtins['math'] is math


def test_whrandom_in_utility_builtins():
    import random
    from likepy.restricted_builtins import utility_builtins
    assert utility_builtins['whrandom'] is random


def test_random_in_utility_builtins():
    import random
    from likepy.restricted_builtins import utility_builtins
    assert utility_builtins['random'] is random


def test_set_in_utility_builtins():
    from likepy.restricted_builtins import utility_builtins
    assert utility_builtins['set'] is set


def test_frozenset_in_utility_builtins():
    from likepy.restricted_builtins import utility_builtins
    assert utility_builtins['frozenset'] is frozenset


def test_DateTime_in_utility_builtins_if_importable():
    try:
        import DateTime
    except ImportError:
        pass
    else:
        from likepy.restricted_builtins import utility_builtins
        assert DateTime.__name__ in utility_builtins


def test_same_type_in_utility_builtins():
    from likepy.restricted_builtins import same_type
    from likepy.restricted_builtins import utility_builtins
    assert utility_builtins['same_type'] is same_type


def test_test_in_utility_builtins():
    from likepy.restricted_builtins import test
    from likepy.restricted_builtins import utility_builtins
    assert utility_builtins['test'] is test


def test_reorder_in_utility_builtins():
    from likepy.restricted_builtins import reorder
    from likepy.restricted_builtins import utility_builtins
    assert utility_builtins['reorder'] is reorder


def test_sametype_only_one_arg():
    from likepy.restricted_builtins import same_type
    assert same_type(object())


def test_sametype_only_two_args_same():
    from likepy.restricted_builtins import same_type
    assert same_type(object(), object())


def test_sametype_only_two_args_different():
    from likepy.restricted_builtins import same_type

    class Foo(object):
        pass
    assert same_type(object(), Foo()) is False


def test_sametype_only_multiple_args_same():
    from likepy.restricted_builtins import same_type
    assert same_type(object(), object(), object(), object())


def test_sametype_only_multipe_args_one_different():
    from likepy.restricted_builtins import same_type

    class Foo(object):
        pass
    assert same_type(object(), object(), Foo()) is False


def test_test_single_value_true():
    from likepy.restricted_builtins import test
    assert test(True) is True


def test_test_single_value_False():
    from likepy.restricted_builtins import test
    assert test(False) is False


def test_test_even_values_first_true():
    from likepy.restricted_builtins import test
    assert test(True, 'first', True, 'second') == 'first'


def test_test_even_values_not_first_true():
    from likepy.restricted_builtins import test
    assert test(False, 'first', True, 'second') == 'second'


def test_test_odd_values_first_true():
    from likepy.restricted_builtins import test
    assert test(True, 'first', True, 'second', False) == 'first'


def test_test_odd_values_not_first_true():
    from likepy.restricted_builtins import test
    assert test(False, 'first', True, 'second', False) == 'second'


def test_test_odd_values_last_true():
    from likepy.restricted_builtins import test
    assert test(False, 'first', False, 'second', 'third') == 'third'


def test_test_odd_values_last_false():
    from likepy.restricted_builtins import test
    assert test(False, 'first', False, 'second', False) is False


def test_reorder_with__None():
    from likepy.restricted_builtins import reorder
    before = ['a', 'b', 'c', 'd', 'e']
    without = ['a', 'c', 'e']
    after = reorder(before, without=without)
    assert after == [('b', 'b'), ('d', 'd')]


def test_reorder_with__not_None():
    from likepy.restricted_builtins import reorder
    before = ['a', 'b', 'c', 'd', 'e']
    with_ = ['a', 'd']
    without = ['a', 'c', 'e']
    after = reorder(before, with_=with_, without=without)
    assert after == [('d', 'd')]
