from likepy.restricted_expression import restrictedexpr, RestrictedExpression

import pytest


exp = """
    {'a':[m.pop()]}['a'] \
        + [m[0]]
"""


def test_init_with_syntax_error():
    with pytest.raises(SyntaxError):
        restrictedexpr.eval("if:")


def test_eval():
    ret = restrictedexpr.eval(exp, {'m': [1, 2]})
    assert ret == [2, 1]


def test_eval_error_1():
    with pytest.raises(SyntaxError):
        restrictedexpr.eval("_a")


def test_eval_used():
    """It stores used names."""
    rexpr = RestrictedExpression()
    code, used = rexpr.compile_expr("[x for x in (1, 2, 3)]")
    assert used == ('x',)
    assert code is not None


def test_eval_1():
    """It does not add names from the mapping to the
    global scope which are already there."""
    result = restrictedexpr.eval("a + b + c", dict(a=1, b=2, c=4))
    assert result == 7


def test__eval_2():
    """It allows to use list comprehensions."""
    result = restrictedexpr.eval("[item for item in (1, 2)]", {})
    assert result == [1, 2]
