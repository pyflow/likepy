
from likepy import restrictedpy
from likepy.exceptions import CompileError
import pytest


restricted_eval = restrictedpy.eval
# Arithmetic Operators

def test_Add():
    assert restricted_eval('1 + 1') == 2


def test_Sub():
    assert restricted_eval('5 - 3') == 2


def test_Mult():
    assert restricted_eval('2 * 2') == 4


def test_Div():
    assert restricted_eval('10 / 2') == 5


def test_Mod():
    assert restricted_eval('10 % 3') == 1


def test_Pow():
    assert restricted_eval('2 ** 8') == 256


def test_FloorDiv():
    assert restricted_eval('7 // 2') == 3


def test_MatMult():
    with pytest.raises(CompileError, match=r".*: MatMult statements are not allowed.*"):
        result = restricted_eval('(8, 3, 5) @ (2, 7, 1)')

def test_BitAnd():
    assert restricted_eval('5 & 3') == 1


def test_BitOr():
    assert restricted_eval('5 | 3') == 7


def test_BitXor():
    assert restricted_eval('5 ^ 3') == 6


def test_Invert():
    assert restricted_eval('~17') == -18


def test_LShift():
    assert restricted_eval('8 << 2') == 32


def test_RShift():
    assert restricted_eval('8 >> 1') == 4


def test_Or():
    assert restricted_eval('False or True') is True


def test_And():
    assert restricted_eval('True and True') is True


def test_Not():
    assert restricted_eval('not False') is True

def test_Eq():
    assert restricted_eval('1 == 1') is True


def test_NotEq():
    assert restricted_eval('1 != 2') is True


def test_Gt():
    assert restricted_eval('2 > 1') is True


def test_Lt():
    assert restricted_eval('1 < 2')


def test_GtE():
    assert restricted_eval('2 >= 2') is True


def test_LtE():
    assert restricted_eval('1 <= 2') is True

def test_Is():
    assert restricted_eval('True is True') is True


def test_NotIs():
    assert restricted_eval('1 is not True') is True

def test_In():
    assert restricted_eval('1 in [1, 2, 3]') is True


def test_NotIn():
    assert restricted_eval('4 not in [1, 2, 3]') is True


def test_UAdd():
    assert restricted_eval('+a', {'a': 42}) == 42


def test_USub():
    assert restricted_eval('-a', {'a': 2411}) == -2411
