
import parso
import os
from parso.tree import NodeOrLeaf, BaseNode, Leaf
from parso.python.tree import PythonLeaf, PythonBaseNode, Name, PythonNode
import contextlib
import sys
from .starlark import StarlarkGrammar
import ast

def prettyformat(node, _indent=0):
    indent_str='    '
    if node is None:  # pragma: nocovrage
        return repr(node)
    elif isinstance(node, str):
        return repr(node)
    elif isinstance(node, PythonLeaf):
        return '<{} {}> ({})'.format(type(node).__name__, node.type, repr(node.value))
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

        out = '<' + type(node).__name__  + " " + node.type + '> (\n'
        with indented():
            assert len(node.children) > 0
            for field in node.children:
                representation = _pformat(field, state.indent)
                out += '{}<{} {}>={},\n'.format(indentstr(), type(node).__name__,  repr(field.type), representation)
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
        visitor.visit(module)
        print(ast.dump(visitor.new_root_node))
        return module


class StarletteVisitor:
    def __init__(self):
        self.new_root_node = None

    def visit(self, node, is_leaf=False):
        """Visit a node."""
        print('visit:', node, node.type)
        type_name = type(node).__name__
        if type_name == 'PythonNode':
            type_name = node.type
        method = 'visit_' + type_name
        visitor = getattr(self, method, self.generic_visit if not is_leaf else None)
        if visitor:
            return visitor(node)

    def generic_visit(self, node):
        """Called if no explicit visitor function exists for a node."""
        new_nodes = []
        for child in node.children:
            if isinstance(child, parso.tree.BaseNode):
                new_node = self.visit(child)
            elif isinstance(child, parso.tree.NodeOrLeaf):
                new_node = self.visit(child, is_leaf=True)
            if isinstance(new_node, ast.AST):
                new_nodes.append(new_node)
        return new_nodes


    def visit_Module(self, node):
        new_node = ast.Module()
        if self.new_root_node is None:
            self.new_root_node = new_node
        child_nodes = self.generic_visit(node)
        new_node._fields = tuple(child_nodes)

    def visit_simple_stmt(self, node):
        print('visit_simple_stmt')
        new_nodes = self.generic_visit(node)
        if len(new_nodes) > 0:
            return new_nodes[0]

    def visit_atom_expr(self, node):
        new_node = ast.Expr()
        children = node.children
        if isinstance(children[0], Name):
            for child in children[1:]:
                if child.type == 'trailer':
                    pass
        #return new_node

    def visit_trailer(self, node):
        pass