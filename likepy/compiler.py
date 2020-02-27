
import parso
import os
from parso.tree import NodeOrLeaf, BaseNode, Leaf
from parso.python.tree import PythonLeaf, PythonBaseNode
import contextlib
import sys
from .starlark import StarlarkGrammar

def prettyformat(node, _indent=0):
    indent_str='    '
    if node is None:  # pragma: nocovrage
        return repr(node)
    elif isinstance(node, str):
        return repr(node)
    elif isinstance(node, PythonLeaf):
        return '{}({})'.format(type(node).__name__, repr(node.value))
    else:
        class state:
            indent = _indent

        @contextlib.contextmanager
        def indented():
            state.indent += 1
            yield
            state.indent -= 1

        def indentstr():
            return state.indent * indent_str

        def _pformat(el, _indent=0):
            return prettyformat(el, _indent=_indent)

        out = type(node).__name__ + '(\n'
        with indented():
            assert len(node.children) > 0
            for field in node.children:
                representation = _pformat(field, state.indent)
                out += '{}{}={},\n'.format(indentstr(), repr(field.type), representation)
        out += indentstr() + ')'
        return out

def dump_ast(node):
    print(prettyformat(node))

class LikepyCompiler:
    def __init__(self):
        pass

    def compile_file(self, file_path):
        with open(file_path, "rb") as f:
            code = f.read()
            file_name = os.path.basename(file_path)
            ext = os.path.extname(file_path)
            dialect = 'starlette' if ext == '.star' else ext[1:]
            return self.compile(code, file_name=file_name, dialect=dialect)

    def compile(self, source, file_name="<string>", dialect="starlette"):
        if dialect == 'starlette':
            visitor = StarletteVisitor()
        else:
            raise Exception('only support starlette dialect now.')

        grammar = StarlarkGrammar()
        module = grammar.parse(source)
        #visitor.visit(module)
        return module


class StarletteVisitor:
    def visit(self, node):
        """Visit a node."""
        print('visit:', node)
        method = 'visit_' + node.__class__.__name__
        visitor = getattr(self, method, self.generic_visit)
        return visitor(node)

    def visit_leaf(self, node):
        """Visit a node."""
        method = 'visit_' + node.__class__.__name__
        visitor = getattr(self, method, None)
        if visitor:
            return visitor(node)

    def generic_visit(self, node):
        """Called if no explicit visitor function exists for a node."""
        for child in node.children:
            if isinstance(child, parso.tree.BaseNode):
                self.visit(child)
            elif isinstance(child, parso.tree.NodeOrLeaf):
                self.visit_leaf(child)
