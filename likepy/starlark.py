
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