
import token
import tokenize
from .tokenizer import LikepyTokenizer, Mark, exact_token_types
import ast

from typing import Any, Callable, cast, Dict, Optional, Tuple, Type, TypeVar

T = TypeVar("T")
P = TypeVar("P", bound="StarLarkParser")
F = TypeVar("F", bound=Callable[..., Any])


class StarLarkParser:
    def __init__(self, sourcepath="", code=None, verbose: bool = False):
        self._tokenizer = LikepyTokenizer(sourcepath=sourcepath, code=code)
        self._verbose = verbose
        self._level = 0
        self._cache: Dict[Tuple[Mark, str, Tuple[Any, ...]], Tuple[Any, Mark]] = {}
        self.mark = self._tokenizer.mark
        self.reset = self._tokenizer.reset

    def parse(self):
        mark = self.mark()
        if ((a := self.statements(),)
            and
            (endmarker := self.expect('ENDMARKER'))
        ):
            return ast.Module(body=a)
        self.reset(mark)
        return None

    def statements(self):
        mark = self.mark()
        children = []
        while ((statement := self.statement())):
            children.append([statement])
            mark = self.mark()
        self.reset(mark)
        return children

    def statement(self):
        # statement: compound_stmt | simple_stmts
        mark = self.mark()
        if (
            (a := self.compound_stmt())
        ):
            return a
        self.reset(mark)
        if (
            (a := self.simple_stmts())
        ):
            return a
        self.reset(mark)
        return None

    def compound_stmt(self):
        # compound_stmt: &('def') function_def | &'if' if_stmt | &('with') with_stmt | &'for' for_stmt | &'try' try_stmt | &'while' while_stmt
        mark = self.mark()
        if (
            self.positive_lookahead(self.expect, 'def')
            and
            (function_def := self.function_def())
        ):
            return [function_def]
        self.reset(mark)
        if (
            self.positive_lookahead(self.expect, 'if')
            and
            (if_stmt := self.if_stmt())
        ):
            return [if_stmt]
        self.reset(mark)
        if (
            self.positive_lookahead(self.expect, 'with')
            and
            (with_stmt := self.with_stmt())
        ):
            return [with_stmt]
        self.reset(mark)
        if (
            self.positive_lookahead(self.expect, 'for')
            and
            (for_stmt := self.for_stmt())
        ):
            return [for_stmt]
        self.reset(mark)
        if (
            self.positive_lookahead(self.expect, 'try')
            and
            (try_stmt := self.try_stmt())
        ):
            return [try_stmt]
        self.reset(mark)
        if (
            self.positive_lookahead(self.expect, 'while')
            and
            (while_stmt := self.while_stmt())
        ):
            return [while_stmt]
        self.reset(mark)
        return None

    def function_def(self):
        # function_def: 'def' NAME '(' params? ')' ['->' expression] ':' func_type_comment? block | ASYNC 'def' NAME '(' params? ')' ['->' expression] ':' func_type_comment? block
        mark = self.mark()
        if (
            (literal := self.expect('def'))
            and
            (n := self.name())
            and
            (literal_1 := self.expect('('))
            and
            (params := self.params(),)
            and
            (literal_2 := self.expect(')'))
            and
            (literal_3 := self.expect(':'))
            and
            (b := self.block())
        ):
            return ast.FunctionDef(n, params, b)
        return None

    def params(self):
        # params: invalid_parameters | parameters
        mark = self.mark()
        self.reset(mark)
        return None

    def block(self):
        # block: NEWLINE INDENT statements DEDENT | simple_stmts | invalid_block
        mark = self.mark()
        self.reset(mark)
        return None


    def showpeek(self) -> str:
        tok = self._tokenizer.peek()
        return f"{tok.start[0]}.{tok.start[1]}: {token.tok_name[tok.type]}:{tok.string!r}"

    def name(self) -> Optional[tokenize.TokenInfo]:
        tok = self._tokenizer.peek()
        if tok.type == token.NAME:
            return self._tokenizer.getnext()
        return None

    def number(self) -> Optional[tokenize.TokenInfo]:
        tok = self._tokenizer.peek()
        if tok.type == token.NUMBER:
            return self._tokenizer.getnext()
        return None

    def string(self) -> Optional[tokenize.TokenInfo]:
        tok = self._tokenizer.peek()
        if tok.type == token.STRING:
            return self._tokenizer.getnext()
        return None

    def op(self) -> Optional[tokenize.TokenInfo]:
        tok = self._tokenizer.peek()
        if tok.type == token.OP:
            return self._tokenizer.getnext()
        return None

    def expect(self, type: str) -> Optional[tokenize.TokenInfo]:
        tok = self._tokenizer.peek()
        if tok.string == type:
            return self._tokenizer.getnext()
        if type in exact_token_types:
            if tok.type == exact_token_types[type]:
                return self._tokenizer.getnext()
        if type in token.__dict__:
            if tok.type == token.__dict__[type]:
                return self._tokenizer.getnext()
        if tok.type == token.OP and tok.string == type:
            return self._tokenizer.getnext()
        return None

    def positive_lookahead(self, func: Callable[..., T], *args: object) -> T:
        mark = self.mark()
        ok = func(*args)
        self.reset(mark)
        return ok

    def negative_lookahead(self, func: Callable[..., object], *args: object) -> bool:
        mark = self.mark()
        ok = func(*args)
        self.reset(mark)
        return not ok

    def make_syntax_error(self, filename: str = "<unknown>") -> SyntaxError:
        tok = self._tokenizer.diagnose()
        return SyntaxError(
            "pegen parse failure", (filename, tok.start[0], 1 + tok.start[1], tok.line)
        )


class StarLark:
    def eval(self, source, starlark_globals=None):
        pass

    def exec(self, source, starlark_globals=None):
        pass

starlark = StarLark()