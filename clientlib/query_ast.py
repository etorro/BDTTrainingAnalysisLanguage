# Contains AST elements for the query part of an expression
# In general, AST's do not have any implementation level code (e.g. writting out C++).
# Instead, they just hold data, and are visited.

class base_ast:
    r"""
    Base class for ast to provide some useful common tools
    """
    
    def __init__(self, source_ast):
        self._source = source_ast

    def get_executor (self):
        r"""
        Return the executor. This should climb the chain until it hits an ast that
        knows how to run. Usually this is the data file (the ROOT file?)
        """
        if self._source:
            return self._source.get_executor()
        else:
            raise BaseException("internal bug: get_executor should not be called with a null source.")
    
    def visit_ast(self, visitor):
        'Visit the ast. This needs to be implemented in each sub-class'
        raise BaseException("visit_ast is virtual and must be implemented everywhere: " + type(self).__qualname__)

class select_many_ast(base_ast):
    r"""
    AST node for select many. Incoming type is a collection
    """

    def __init__(self, source_ast, selection_function):
        r"""
        source_ast - an AST that represents a collection
        """
        base_ast.__init__(self, source_ast)
        self._selection_function = selection_function

    def visit_ast(self, visitor):
        visitor.visit_select_many_ast (self)

class select_ast (base_ast):
    r"""
    AST node for select. Transforms the input to the output.
    """

    def __init__(self, source_ast, select_function):
        base_ast.__init__(self, source_ast)
        self._selection_function = select_function

    def visit_ast(self, visitor):
        visitor.visit_select_ast (self)

class query_ast_vistor_base:
    r"""
    The base of the visitor call-back set.
    """
    def visit_select_ast (self, ast):
        'Visit select ast'
        ast._source.visit_ast(self)

    def visit_select_many_ast (self, ast):
        'Visit select many source'
        ast._source.visit_ast(self)
