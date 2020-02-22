
import math
import random
import string
import builtins

utility_builtins = {}
limited_builtins = {}
safe_builtins = {}

_safe_names = [
    'None',
    'False',
    'True',
    'abs',
    'bool',
    'callable',
    'chr',
    'complex',
    'divmod',
    'float',
    'hash',
    'hex',
    'id',
    'int',
    'isinstance',
    'issubclass',
    'len',
    'oct',
    'ord',
    'pow',
    'range',
    'repr',
    'round',
    'slice',
    'str',
    'tuple',
    'zip'
]

_safe_exceptions = [
    'ArithmeticError',
    'AssertionError',
    'AttributeError',
    'BaseException',
    'BufferError',
    'BytesWarning',
    'DeprecationWarning',
    'EOFError',
    'EnvironmentError',
    'Exception',
    'FloatingPointError',
    'FutureWarning',
    'GeneratorExit',
    'IOError',
    'ImportError',
    'ImportWarning',
    'IndentationError',
    'IndexError',
    'KeyError',
    'KeyboardInterrupt',
    'LookupError',
    'MemoryError',
    'NameError',
    'NotImplementedError',
    'OSError',
    'OverflowError',
    'PendingDeprecationWarning',
    'ReferenceError',
    'RuntimeError',
    'RuntimeWarning',
    'StopIteration',
    'SyntaxError',
    'SyntaxWarning',
    'SystemError',
    'SystemExit',
    'TabError',
    'TypeError',
    'UnboundLocalError',
    'UnicodeDecodeError',
    'UnicodeEncodeError',
    'UnicodeError',
    'UnicodeTranslateError',
    'UnicodeWarning',
    'UserWarning',
    'ValueError',
    'Warning',
    'ZeroDivisionError',
]

_safe_names.extend([
    '__build_class__',  # needed to define new classes
])

for name in _safe_names:
    safe_builtins[name] = getattr(builtins, name)

for name in _safe_exceptions:
    safe_builtins[name] = getattr(builtins, name)


# Wrappers provided by this module:
# delattr
# setattr

# Wrappers provided by ZopeGuards:
# __import__
# apply
# dict
# enumerate
# filter
# getattr
# hasattr
# iter
# list
# map
# max
# min
# sum
# all
# any

# Builtins that are intentionally disabled
# compile   - don't let them produce new code
# dir       - a general purpose introspector, probably hard to wrap
# execfile  - no direct I/O
# file      - no direct I/O
# globals   - uncontrolled namespace access
# input     - no direct I/O
# locals    - uncontrolled namespace access
# open      - no direct I/O
# raw_input - no direct I/O
# vars      - uncontrolled namespace access

# There are several strings that describe Python.  I think there's no
# point to including these, although they are obviously safe:
# copyright, credits, exit, help, license, quit

# Not provided anywhere.  Do something about these?  Several are
# related to new-style classes, which we are too scared of to support
# <0.3 wink>.  coerce, buffer, and reload are esoteric enough that no
# one should care.

# buffer
# bytes
# bytearray
# classmethod
# coerce
# eval
# intern
# memoryview
# object
# property
# reload
# staticmethod
# super
# type


def _write_wrapper():
    # Construct the write wrapper class
    def _handler(secattr, error_msg):
        # Make a class method.
        def handler(self, *args):
            try:
                f = getattr(self.ob, secattr)
            except AttributeError:
                raise TypeError(error_msg)
            f(*args)
        return handler

    class Wrapper(object):
        def __init__(self, ob):
            self.__dict__['ob'] = ob

        __setitem__ = _handler(
            '__guarded_setitem__',
            'object does not support item or slice assignment')

        __delitem__ = _handler(
            '__guarded_delitem__',
            'object does not support item or slice assignment')

        __setattr__ = _handler(
            '__guarded_setattr__',
            'attribute-less object (assign or del)')

        __delattr__ = _handler(
            '__guarded_delattr__',
            'attribute-less object (assign or del)')
    return Wrapper


def _full_write_guard():
    # Nested scope abuse!
    # safetypes and Wrapper variables are used by guard()
    safetypes = {dict, list}
    Wrapper = _write_wrapper()

    def guard(ob):
        # Don't bother wrapping simple types, or objects that claim to
        # handle their own write security.
        if type(ob) in safetypes or hasattr(ob, '_guarded_writes'):
            return ob
        # Hand the object to the Wrapper instance, then return the instance.
        return Wrapper(ob)
    return guard


full_write_guard = _full_write_guard()


def guarded_setattr(object, name, value):
    setattr(full_write_guard(object), name, value)


safe_builtins['setattr'] = guarded_setattr


def guarded_delattr(object, name):
    delattr(full_write_guard(object), name)


safe_builtins['delattr'] = guarded_delattr


def safer_getattr(object, name, default=None, getattr=getattr):
    """Getattr implementation which prevents using format on string objects.

    format() is considered harmful:
    http://lucumr.pocoo.org/2016/12/29/careful-with-str-format/

    """
    if isinstance(object, str) and name == 'format':
        raise NotImplementedError(
            'Using format() on a %s is not safe.' % object.__class__.__name__)
    if name.startswith('_'):
        raise AttributeError(
            '"{name}" is an invalid attribute name because it '
            'starts with "_"'.format(name=name)
        )
    return getattr(object, name, default)


safe_builtins['_getattr_'] = safer_getattr


def guarded_iter_unpack_sequence(it, spec, _getiter_):
    """Protect sequence unpacking of targets in a 'for loop'.

    The target of a for loop could be a sequence.
    For example "for a, b in it"
    => Each object from the iterator needs guarded sequence unpacking.
    """
    # The iteration itself needs to be protected as well.
    for ob in _getiter_(it):
        yield guarded_unpack_sequence(ob, spec, _getiter_)


def guarded_unpack_sequence(it, spec, _getiter_):
    """Protect nested sequence unpacking.

    Protect the unpacking of 'it' by wrapping it with '_getiter_'.
    Furthermore for each child element, defined by spec,
    guarded_unpack_sequence is called again.

    Have a look at transformer.py 'gen_unpack_spec' for a more detailed
    explanation.
    """
    # Do the guarded unpacking of the sequence.
    ret = list(_getiter_(it))

    # If the sequence is shorter then expected the interpreter will raise
    # 'ValueError: need more than X value to unpack' anyway
    # => No childs are unpacked => nothing to protect.
    if len(ret) < spec['min_len']:
        return ret

    # For all child elements do the guarded unpacking again.
    for (idx, child_spec) in spec['childs']:
        ret[idx] = guarded_unpack_sequence(ret[idx], child_spec, _getiter_)

    return ret


safe_globals = {'__builtins__': safe_builtins}


def limited_range(iFirst, *args):
    # limited range function from Martijn Pieters
    RANGELIMIT = 1000
    if not len(args):
        iStart, iEnd, iStep = 0, iFirst, 1
    elif len(args) == 1:
        iStart, iEnd, iStep = iFirst, args[0], 1
    elif len(args) == 2:
        iStart, iEnd, iStep = iFirst, args[0], args[1]
    else:
        raise AttributeError('range() requires 1-3 int arguments')
    if iStep == 0:
        raise ValueError('zero step for range()')
    iLen = int((iEnd - iStart) / iStep)
    if iLen < 0:
        iLen = 0
    if iLen >= RANGELIMIT:
        raise ValueError(
            'To be created range() object would be to large, '
            'in RestrictedPython we only allow {limit} '
            'elements in a range.'.format(limit=str(RANGELIMIT)),
        )
    return range(iStart, iEnd, iStep)


limited_builtins['range'] = limited_range


def limited_list(seq):
    if isinstance(seq, str):
        raise TypeError('cannot convert string to list')
    return list(seq)


limited_builtins['list'] = limited_list


def limited_tuple(seq):
    if isinstance(seq, str):
        raise TypeError('cannot convert string to tuple')
    return tuple(seq)


limited_builtins['tuple'] = limited_tuple




utility_builtins['string'] = string
utility_builtins['math'] = math
utility_builtins['random'] = random
utility_builtins['whrandom'] = random
utility_builtins['set'] = set
utility_builtins['frozenset'] = frozenset

try:
    import DateTime
    utility_builtins['DateTime'] = DateTime.DateTime  # pragma: no cover
except ImportError:
    pass


def same_type(arg1, *args):
    """Compares the class or type of two or more objects."""
    t = getattr(arg1, '__class__', type(arg1))
    for arg in args:
        if getattr(arg, '__class__', type(arg)) is not t:
            return False
    return True


utility_builtins['same_type'] = same_type


def test(*args):
    length = len(args)
    for i in range(1, length, 2):
        if args[i - 1]:
            return args[i]

    if length % 2:
        return args[-1]


utility_builtins['test'] = test


def reorder(s, with_=None, without=()):
    # s, with_, and without are sequences treated as sets.
    # The result is subtract(intersect(s, with_), without),
    # unless with_ is None, in which case it is subtract(s, without).
    if with_ is None:
        with_ = s
    orig = {}
    for item in s:
        if isinstance(item, tuple) and len(item) == 2:
            key, value = item
        else:
            key = value = item
        orig[key] = value

    result = []

    for item in without:
        if isinstance(item, tuple) and len(item) == 2:
            key, ignored = item
        else:
            key = item
        if key in orig:
            del orig[key]

    for item in with_:
        if isinstance(item, tuple) and len(item) == 2:
            key, ignored = item
        else:
            key = item
        if key in orig:
            result.append((key, orig[key]))
            del orig[key]

    return result


utility_builtins['reorder'] = reorder
