# Contains AST elements for the query part of an expression.
# This is an extension of the python AST, and is written in that same style.
#
# AST's are designed to have only data, no code. In that sense, they could
# be transmitted over the wire and received at the other end.
#
# Of course, this being python, it is possible to add new things to the class
# member variables.

# TODO: Rename atlaslib to xAODlib or similar, just to make it clear how these
#       libraries really work.
import ast

class SelectMany(ast.AST):
    r"""
    AST node for SelectMany. A selection function picks out
    a collection, and then one iterates over that collection.
    """
    def __init__(self, source, selection_function):
        r"""
        AST node that represents a SelectMany operation. It's resulting type is an iterator
        over the collection selected by ``selection_function``.

        source - An AST that represents the source iterator.
        selection_function - A lambda that selects a collection to iterate over when applied to source.
        """
        self.source = source
        self.selection = selection_function
        self._fields = ['source', 'selection']

class Select(ast.AST):
    r"""
    AST node for Select. Transforms the input to the output by applying
    some selection function.
    """

    def __init__(self, source, select_function):
        r"""
        Initialize an AST node that represents a Select operation. As input takes an iterator
        and transforms it to another iterator by applying ``select_function`` to each individual
        object.

        source - An AST that represents the source iterator.
        select_function - function that operates on each item of the source.
        """
        self.selection = select_function
        self.source = source
        self._fields = ('source', 'selection')
