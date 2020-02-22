
from .compile import compile_restricted_eval, compile_restricted_exec
from .restricted_builtins import safe_builtins


class RestrictedPython:
    def eval(self, source, restricted_globals=None):
        if restricted_globals is None:
            restricted_globals = {}
        if '__builtins__' not in restricted_globals:
            restricted_globals['__builtins__'] = safe_builtins.copy()
        result = compile_restricted_eval(source)
        assert result.errors == (), result.errors
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