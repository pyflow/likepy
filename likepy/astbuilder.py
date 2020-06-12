import parso
import os
from parso.tree import NodeOrLeaf, BaseNode, Leaf
from parso.python.tree import PythonLeaf, PythonBaseNode, Name, PythonNode
import contextlib
import sys
import ast

class Tokens:
    FILE_INPUT = 'file_input'
    EVAL_INPUT = 'eval_input'
    SINGLE_INPUT = 'single_input'
    STMT = 'stmt'
    SIMPLE_STMT = 'simple_stmt'
    COMPOUND_STMT = 'compound_stmt'
    SMALL_STMT = 'small_stmt'

    NEWLINE = 'newline'

tokens = Tokens()

class ASTBuilder:
    def __init__(self, node):
        self.root_node = node

    def build_ast(self):
        n = self.root_node
        if n.type == tokens.FILE_INPUT or n.type == tokens.SINGLE_INPUT:
            stmts = []
            for child in n.children:
                stmt = child
                if stmt.type == tokens.NEWLINE:
                    continue
                stmts.append(self.handle_stmt(stmt))
            return ast.Module(stmts)
        elif n.type == tokens.EVAL_INPUT:
            body = self.handle_testlist(n.children[0])
            return ast.Expression(body)
        else:
            raise AssertionError("unknown root node")

    def handle(self, node, parent_node=None):
        """Visit a node."""
        print('handle:', node, node.type)
        type_name = node.type
        method = 'handle_' + type_name
        handler = getattr(self, method, None)
        if handler:
            return handler(node, parent_node)

    def handle_stmt(self, stmt):
        stmt_type = stmt.type
        if stmt_type == tokens.STMT:
            stmt = stmt.children[0]
            stmt_type = stmt.type

        if stmt_type == tokens.SIMPLE_STMT:
            stmt = stmt.children[0]
            stmt_type = stmt.type
            return self.handle(stmt, None)

        if stmt_type == tokens.SMALL_STMT:
            stmt = stmt.children[0]
            stmt_type = stmt.type
            if stmt_type == tokens.expr_stmt:
                return self.handle_expr_stmt(stmt)
            elif stmt_type == tokens.del_stmt:
                return self.handle_del_stmt(stmt)
            elif stmt_type == tokens.pass_stmt:
                return ast.Pass(stmt.get_lineno(), stmt.get_column())
            elif stmt_type == tokens.flow_stmt:
                return self.handle_flow_stmt(stmt)
            elif stmt_type == tokens.import_stmt:
                return self.handle_import_stmt(stmt)
            elif stmt_type == tokens.global_stmt:
                return self.handle_global_stmt(stmt)
            elif stmt_type == tokens.nonlocal_stmt:
                return self.handle_nonlocal_stmt(stmt)
            elif stmt_type == tokens.assert_stmt:
                return self.handle_assert_stmt(stmt)
            else:
                raise AssertionError("unhandled small statement")
        else:
            return self.handle(stmt, None)
