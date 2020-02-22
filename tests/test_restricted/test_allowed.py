from likepy import  restrictedpy


restricted_exec = restrictedpy.exec
restricted_eval = restrictedpy.eval

def test_allowed__visit_Assert__1():
    """It allows assert statements."""
    restricted_exec('assert 1')

def test_Num():
    """It allows to use number literals."""
    assert restricted_eval('42') == 42


def test_Bytes():
    """It allows to use bytes literals."""
    assert restricted_eval('b"code"') == b"code"


def test_Set():
    """It allows to use set literals."""
    assert restricted_eval('{1, 2, 3}') == set([1, 2, 3])


