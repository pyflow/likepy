# Likepy

Likepy is a library that helps to exec or eval the following python-like languages within a trusted environment:

* RestrictedPython
* starlark (progressing)


> :warning: **Likepy only supports CPython**. It does _not_ support PyPy and other Python implementations.


## starlark's differences with python

    Global variables are immutable.

    for statements are not allowed at the top-level. Use them within functions instead. In BUILD files, you may use list comprehensions.

    if statements are not allowed at the top-level. However, if expressions can be used: first = data[0] if len(data) > 0 else None.

    Deterministic order for iterating through Dictionaries.

    Recursion is not allowed.

    Int type is limited to 32-bit signed integers. Overflows will throw an error.

    Modifying a collection during iteration is an error.

    Except for equality tests, comparison operators <, <=, >=, >, etc. are not defined across value types. In short: 5 < 'foo' will throw an error and 5 == "5" will return false.

    In tuples, a trailing comma is valid only when the tuple is between parentheses, e.g. write (1,) instead of 1,.

    Dictionary literals cannot have duplicated keys. For example, this is an error: {"a": 4, "b": 7, "a": 1}.

    Strings are represented with double-quotes (e.g. when you call repr).

    Strings aren’t iterable.


The following Python features are not supported:

    implicit string concatenation (use explicit + operator).

    Chained comparisons (e.g. 1 < x < 5).

    class (see struct function).

    import (see load statement).

    while, yield.

    float and set types.

    generators and generator expressions.

    lambda and nested functions.

    is (use == instead).

    try, raise, except, finally (see fail for fatal errors).

    global, nonlocal.

    most builtin functions, most methods.
