import ast
import itertools

try:
    zip_longest = itertools.zip_longest
except AttributeError:
    zip_longest = itertools.izip_longest


class NonExistent(object):
    """This is not the class you are looking for.
    """
    pass


def iter_node(node, name='', unknown=None,
              # Runtime optimization
              list=list, getattr=getattr, isinstance=isinstance,
              enumerate=enumerate, missing=NonExistent):
    """Iterates over an object:
       - If the object has a _fields attribute,
         it gets attributes in the order of this
         and returns name, value pairs.
       - Otherwise, if the object is a list instance,
         it returns name, value pairs for each item
         in the list, where the name is passed into
         this function (defaults to blank).
       - Can update an unknown set with information about
         attributes that do not exist in fields.
    """
    fields = getattr(node, '_fields', None)
    if fields is not None:
        for name in fields:
            value = getattr(node, name, missing)
            if value is not missing:
                yield value, name
        if unknown is not None:
            unknown.update(set(vars(node)) - set(fields))
    elif isinstance(node, list):
        for value in node:
            yield value, name

def dump_tree(node, name=None, initial_indent='', indentation='    ',
              maxline=120, maxmerged=80,
              # Runtime optimization
              iter_node=iter_node, special=ast.AST,
              list=list, isinstance=isinstance, type=type, len=len):
    """Dumps an AST or similar structure:
       - Pretty-prints with indentation
       - Doesn't print line/column/ctx info
    """
    def dump(node, name=None, indent=''):
        level = indent + indentation
        name = name and name + '=' or ''
        values = list(iter_node(node))
        if isinstance(node, list):
            prefix, suffix = '%s[' % name, ']'
        elif values:
            prefix, suffix = '%s%s(' % (name, type(node).__name__), ')'
        elif isinstance(node, special):
            prefix, suffix = name + type(node).__name__, ''
        else:
            return '%s%s' % (name, repr(node))
        node = [dump(a, b, level) for a, b in values if b != 'ctx']
        oneline = '%s%s%s' % (prefix, ', '.join(node), suffix)
        if len(oneline) + len(indent) < maxline:
            return '%s' % oneline
        if node and len(prefix) + len(node[0]) < maxmerged:
            prefix = '%s%s,' % (prefix, node.pop(0))
        node = (',\n%s' % level).join(node).lstrip()
        return '%s\n%s%s%s' % (prefix, level, node, suffix)
    return dump(node, name, initial_indent)


def dump_code(code):
    tree = ast.parse(code)
    print(dump_tree(tree))