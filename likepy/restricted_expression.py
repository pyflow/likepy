##############################################################################
#
# Copyright (c) 2002 Zope Foundation and Contributors.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE
#
##############################################################################
"""Restricted Python Expressions."""

from .compile import compile_restricted_eval

import ast

nltosp = str.maketrans('\r\n', '  ')

# No restrictions.
default_guarded_getattr = getattr


def default_guarded_getitem(ob, index):
    # No restrictions.
    return ob[index]


def default_guarded_getiter(ob):
    # No restrictions.
    return ob


class RestrictedExpression(object):
    """A base class for restricted code."""

    expr_globals = {'__builtins__': None}

    def init_expr(self, expr):
        """Create a restricted expression

        where:

          expr -- a string containing the expression to be evaluated.
        """
        expr = expr.strip()
        self.__name__ = expr
        expr = expr.translate(nltosp)
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
            '_getattr_': default_guarded_getattr,
            '_getitem_': default_guarded_getitem,
            '_getiter_': default_guarded_getiter,
        }

        global_scope.update(self.expr_globals)

        for name in used:
            if (name not in global_scope) and (name in mapping):
                global_scope[name] = mapping[name]

        return eval(rcode, global_scope)

restrictedexpr = RestrictedExpression()