
from .restricted_builtins import safe_builtins
from collections import namedtuple
from .transformer import RestrictingNodeTransformer
from .exceptions import CompileError

import ast
import warnings

CompileResult = namedtuple(
    'CompileResult', 'code, errors, warnings, used_names')
syntax_error_template = (
    'Line {lineno}: {type}: {msg} at statement: {statement!r}')

def _compile_restricted_mode(
        source,
        filename='<string>',
        mode="exec",
        flags=0,
        dont_inherit=False,
        policy=RestrictingNodeTransformer):

    byte_code = None
    collected_errors = []
    collected_warnings = []
    used_names = {}
    if policy is None:
        # Unrestricted Source Checks
        byte_code = compile(source, filename, mode=mode, flags=flags,
                            dont_inherit=dont_inherit)
    elif issubclass(policy, RestrictingNodeTransformer):
        c_ast = None
        allowed_source_types = [str, ast.Module]
        if not issubclass(type(source), tuple(allowed_source_types)):
            raise TypeError('Not allowed source type: '
                            '"{0.__class__.__name__}".'.format(source))
        c_ast = None
        # workaround for pypy issue https://bitbucket.org/pypy/pypy/issues/2552
        if isinstance(source, ast.Module):
            c_ast = source
        else:
            try:
                c_ast = ast.parse(source, filename, mode)
            except (TypeError, ValueError) as e:
                collected_errors.append(str(e))
            except SyntaxError as v:
                collected_errors.append(syntax_error_template.format(
                    lineno=v.lineno,
                    type=v.__class__.__name__,
                    msg=v.msg,
                    statement=v.text.strip() if v.text else None
                ))
        if c_ast:
            policy_instance = policy(
                collected_errors, collected_warnings, used_names)
            policy_instance.visit(c_ast)
            if not collected_errors:
                byte_code = compile(c_ast, filename, mode=mode  # ,
                                    # flags=flags,
                                    # dont_inherit=dont_inherit
                                    )
    else:
        raise TypeError('Unallowed policy provided for RestrictedPython')
    return CompileResult(
        byte_code,
        tuple(collected_errors),
        collected_warnings,
        used_names)


def compile_restricted_exec(
        source,
        filename='<string>',
        flags=0,
        dont_inherit=False,
        policy=RestrictingNodeTransformer):
    """Compile restricted for the mode `exec`."""
    return _compile_restricted_mode(
        source,
        filename=filename,
        mode='exec',
        flags=flags,
        dont_inherit=dont_inherit,
        policy=policy)


def compile_restricted_eval(
        source,
        filename='<string>',
        flags=0,
        dont_inherit=False,
        policy=RestrictingNodeTransformer):
    """Compile restricted for the mode `eval`."""
    return _compile_restricted_mode(
        source,
        filename=filename,
        mode='eval',
        flags=flags,
        dont_inherit=dont_inherit,
        policy=policy)



class RestrictedPython:
    def eval(self, source, restricted_globals=None):
        if restricted_globals is None:
            restricted_globals = {}
        if '__builtins__' not in restricted_globals:
            restricted_globals['__builtins__'] = safe_builtins.copy()
        result = compile_restricted_eval(source)
        if result.errors:
            raise CompileError(result.errors[0])
        assert result.code is not None
        return eval(result.code, restricted_globals)

    def exec(self, source, restricted_globals=None):
        if restricted_globals is None:
            restricted_globals = {}
        if '__builtins__' not in restricted_globals:
            restricted_globals['__builtins__'] = safe_builtins.copy()
        result = compile_restricted_exec(source)
        assert result.errors == (), result.errors
        assert result.code is not None
        return exec(result.code, restricted_globals)

restrictedpy = RestrictedPython()


class RestrictedExpression(object):
    """A base class for restricted code."""
    nltosp = str.maketrans('\r\n', '  ')
    expr_globals = {'__builtins__': None}

    # No restrictions.
    default_guarded_getattr = getattr

    @staticmethod
    def default_guarded_getitem(ob, index):
        # No restrictions.
        return ob[index]

    @staticmethod
    def default_guarded_getiter(ob):
        # No restrictions.
        return ob

    def init_expr(self, expr):
        """Create a restricted expression

        where:

          expr -- a string containing the expression to be evaluated.
        """
        expr = expr.strip()
        self.__name__ = expr
        expr = expr.translate(self.nltosp)
        return expr

    def compile_expr(self, expr):
        result = compile_restricted_eval(expr, '<string>')
        if result.errors:
            raise SyntaxError(result.errors[0])
        used = tuple(result.used_names)
        return result.code, used


    def eval(self, expr, mapping={}):
        # This default implementation is probably not very useful. :-(
        # This is meant to be overridden.
        expr = self.init_expr(expr)
        rcode, used = self.compile_expr(expr)

        global_scope = {
            '_getattr_': RestrictedExpression.default_guarded_getattr,
            '_getitem_': RestrictedExpression.default_guarded_getitem,
            '_getiter_': RestrictedExpression.default_guarded_getiter,
        }

        global_scope.update(self.expr_globals)

        for name in used:
            if (name not in global_scope) and (name in mapping):
                global_scope[name] = mapping[name]

        return eval(rcode, global_scope)

restrictedexpr = RestrictedExpression()