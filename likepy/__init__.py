
__version__ = '0.2.0'
import warnings
import platform

IS_CPYTHON = platform.python_implementation() == 'CPython'

NOT_CPYTHON_WARNING = (
    'likepy is only supported on CPython: use on other Python '
    'implementations may create security issues.'
)

if not IS_CPYTHON:
    warnings.warn_explicit(
        NOT_CPYTHON_WARNING, RuntimeWarning, 'likepy', 0)

from .restricted import (
    restrictedpy,
    restrictedexpr,
    RestrictedPython,
    RestrictedExpression
)