# Executor and code for the ntup input files
from RDFlib.generated_code import generated_code
import RDFlib.RDFEventStream
from clientlib.query_ast import Where
from clientlib.ast_util import lambda_unwrap
import cpplib.cpp_ast as cpp_ast
from cpplib.cpp_vars import unique_name
import cpplib.cpp_types as ctyp
from cpplib.cpp_functions import find_known_functions, function_ast

from cpplib.math_utils import mindRAst

import pandas as pd
import uproot
import ast
import os, sys
from pprint import pprint
import ROOT




class query_ast_visitor(ast.NodeVisitor):
    r"""
    Drive the conversion to C++ from the top level query
    """
    def __init__(self):
        r'''
        Initialize the visitor.
        '''
        # Tracks the output of the code.
        self._gc = generated_code()
        self._var_dict = {}
        self._result = None

    def visit (self, node):
        '''Visit a note. If the node already has a rep, then it has been visited and we
        do not need to visit it again.

        node - if the node has a rep, just return

        '''
        if hasattr(node, 'rep'):
            return node.rep
        else:
            return ast.NodeVisitor.visit(self, node)

    def generic_visit(self, node):
        '''Visit a generic node. If the node already has a rep, then it has been
        visited once and we do not need to visit it again.

        node - If the node has a rep, do not visit it.
    '''
        if hasattr(node, 'rep'):
            return
        else:
            return ast.NodeVisitor.generic_visit(self, node)

    def get_rep(self, node):
        r'''Return the rep for the node. If it isn't set yet, then run our visit on it.
        node - The ast node to generate a representation for.
        '''
        if not hasattr(node, 'rep'):
            self.visit(node)
        return node.rep

    def resolve_id(self, id):
        'Look up the in our local dict'
        if id in self._var_dict:
            id = self._var_dict[id]
        if isinstance(id, ast.AST):
            id = self.get_rep(id)
        return id


    def visit_Call_Lambda(self, call_node):
        'Call to a lambda function. This is book keeping and we dive in'
        for c_arg, l_arg in zip(call_node.args, call_node.func.args.args):
            self._var_dict[l_arg.arg] = c_arg
        # Next, process the lambda's body.
        self.visit(call_node.func.body)

        # Done processing the lambda. Remove the arguments
        for l_arg in call_node.func.args.args:
            del self._var_dict[l_arg.arg]


    def visit_Attribute(self, call_node):
        'Method call on an object'
        # figure out what we are calling against, and the
        # method name we are going to be calling against.
        calling_against = self.get_rep(call_node.value) 
        attr_name = call_node.attr 
        call_node.rep =attr_name 
        self._result = attr_name

    def visit_BinOp(self, node):
        lhs = self.get_rep(node.left)
        rhs = self.get_rep(node.right)
        
        if type(node.op) is ast.Add:
            r = str(lhs) + "+" +  str(rhs) 
        elif type(node.op) is ast.Div:
            r = str(lhs) + "/" +  str(rhs)
        elif type(node.op) is ast.Gt:
            r = str(lhs) + ">" +  str(rhs)   
        elif type(node.op) is ast.Lt:
            r = str(lhs) + "<" +  str(rhs)   
        else:
            raise BaseException("Binary operator {0} is not implemented.".format(type(node.op)))

        # Cache the result to push it back further up.
        node.rep = r
        self._result = r
        return node.rep

    def visit_Num(self, node):
        node.rep = node.n
        self._result = node.rep

    def visit_Str(self, node):
        node.rep = node.s
        self._result = node.rep

    def visit_Name(self, node):
        'Visiting a name - which should represent something'
        node.rep = self.resolve_id(node.id)

        self._result = node.rep
        return node.rep
          
    def visit_Compare(self, node):
        ops = node.ops
        comps = node.comparators
        if len(comps) == 1:
            op = ops[0]
            binop = ast.BinOp(op=op, left=node.left, right=comps[0])
            node.rep = self.visit(binop)
            return self.visit(binop)
        else:
            raise BaseException("Compare operator {0} is not len 1.".format(type(node.op)))

    def visit_Call(self, call_node):
        r'''
        Very limited call forwarding.
        '''
        # What kind of a call is this?
        if type(call_node.func) is ast.Lambda:
            self.visit_Call_Lambda(call_node)
        elif type(call_node.func) is cpp_ast.CPPCodeValue:
            self._result = cpp_ast.process_ast_node(self, self._gc, call_node)
        elif type(call_node.func) is function_ast:
            self._result = self.visit_function_ast(call_node)    
        elif type(call_node.func) is ast.BinOp:
            self.visit_Call_Member(call_node)
        elif type(call_node.func) is ast.Attribute:
            self.visit_Call_Member(call_node)
            for arg in call_node.args:
                self.visit(arg)
            if call_node.func.attr == "Where":
                new_call = Where(source=call_node.func.value, filter_lambda=call_node.args[0])
                return new_call
            return call_node 
        elif type(call_node.func) is ast.Name:
            self.visit_Name(call_node.func)
            for arg in call_node.args:
                self.visit(arg)
            if call_node.func.id == "newmindR":
                s_rep = self.visit_minDR(call_node)
                self._result = s_rep
                return s_rep
        else:
            raise BaseException("Do not know how to call at " + type(call_node.func).__name__)
        call_node.rep = self._result

    def visit_minDR(self, node):
        'Apply a filtering to the current loop.'
        'list of attributes: eta1, phi1, eta2, phi2'
        if type(node.args[0]) is ast.Attribute:
            eta1 = node.args[0].attr
            phi1 = node.args[1].attr
            eta2 = node.args[2].attr
            phi2 = node.args[3].attr
        elif type(node.args[0]) is ast.Subscript:
            s_rep_all = self.visit_Name(node.args[0].value)  
            eta1 = s_rep_all[0] 
            phi1 = s_rep_all[1] 
            eta2 = s_rep_all[2]
            phi2 = s_rep_all[3]
            
        s_rep = "double mind=1000; vector<double> mdR;" 
        s_rep += " for(int i=0; i<" + eta1 + ".size();i++){"
        s_rep += "     mind=1000; "
        s_rep += "     for(int j=0; j<" + eta2 + ".size();j++) { "
        s_rep += "         double deta = " + eta1 + "[i]-" + eta2 + "[j]; "
        s_rep += "         double dphi = " + phi1 + "[i]-" + phi2 + "[j]; "
        s_rep += "         if(dphi>M_PI) dphi -= 2*M_PI; "
        s_rep += "         else if(dphi<-M_PI) dphi += 2*M_PI; "
        s_rep += "         double r2=deta*deta+dphi*dphi;  "
        s_rep += "         if(r2<mind){mind=r2; } } "
        s_rep += " mdR.push_back(sqrt(mind));} "
        s_rep += " return mdR;"

        node.rep = s_rep
        return node.rep

    
    def visit_Subscript(self, node):
        'Index into an array. Check types, as tuple indexing can be very bad for us'
        v = self.get_rep(node.value)
        if type(v) is not tuple:
            raise BaseException("Do not know how to take the index of type '{0}'".format(type(v_rep)))
        index = self.get_rep(node.slice)

        node.rep = v[index]
        self._result = node.rep

    def visit_Index(self, node):
        'We can only do single items, we cannot do slices yet'
        v = self.get_rep(node.value)
        node.rep = v
        self._result = node

    def visit_Tuple(self, tuple_node):
        r'''
        Process a tuple. We visit each component of it, and build up a representation from each result.
        See github bug #21 for the special case of dealing with (x1, x2, x3)[0].
        '''
        tuple_node.rep = tuple(self.get_rep(e) for e in tuple_node.elts)
        self._result = tuple_node.rep

    def visit_CreatePandasDF(self, node):
        'Generate the code to convert to a pandas DF'
        self.generic_visit(node)

    def visit_CreateTTreeFile(self, node):
        '''This AST means we are taking an iterable and converting it to a file.
        '''
        # For each incoming variable, we need to declare something we are going to write.
        var_names = [(name, unique_name(name, is_class_var=True)) for name in node.column_names]
        for cv in var_names:
            self._gc.declare_class_variable('float', cv[1])

        # Next, emit the booking code
        self._gc.add_book_statement(statement.book_ttree("analysis", var_names))

        # For each varable we need to save, put it in the C++ variable we've created above
        # and then trigger a fill statement once that is all done.

        self.generic_visit(node)
        v_rep = self.get_rep(node.source)
        if type(v_rep) is not tuple:
            v_rep = (v_rep,)
        if len(v_rep) != len(var_names):
            raise BaseException("Number of columns ({0}) is not the same as labels ({1}) in TTree creation".format(len(v_rep), len(var_names)))

        for e in zip(v_rep, var_names):
            self._gc.add_statement(statement.set_var(e[1][1], e[0].name()))

        self._gc.add_statement(statement.ttree_fill("analysis"))

        # And we are a terminal, so pop off the block.
        self._gc.pop_scope()

    
    def visit_Select(self, node):
        'Transform the iterable from one form to another'

        # Simulate this as a "call"    
        c = ast.Call(func=node.selection.body[0].value, args=[node.source])
        
        self.visit(c) # return ast.Call(_ast.Lambda, RDFlib.RDFEventStream.RDFFileStream)
        
        node.rep = self._result

    def visit_SelectMany(self, node):
        r'''
        Apply the selection function to the base to generate a collection, and then
        loop over that collection.
        '''

        # There isn't any difference between Select and SelectMany here
        self.visit_Select(node)
        node.rep += '.flatten()'


    

    def visit_Where(self, node):
        'Apply a filtering to the current loop.'

        self.source = node.source    
        self.filter = node.filter
        self._fields = ('source', 'filter')
        
        # Make sure we are in a loop
        s_rep = self.get_rep(node.source)

        # Simulate the filtering call - we want the resulting value to test.
        filter = lambda_unwrap(node.filter)
        c = ast.Call(func=filter, args=[node.source])
        rep = self.get_rep(c)

        if type(s_rep) is not tuple:
            r = str(s_rep) + "[" +  str(rep)  + "]"
        else:
            r = ROOT.std.vector("string")()
            for element in s_rep:
                r.push_back(str(element) + "[" +  str(rep)  + "]")

        node.rep = r
        self._result = r
        return node.rep

class ntup_executor:
    def __init__(self, dataset_source):
        self.dataset_source = dataset_source

    def apply_ast_transformations(self, ast):
        r'''
        Run through all the transformations that we have on tap to be run on the client side.
        Return a (possibly) modified ast.
        '''
        # Any C++ custom code needs to be threaded into the ast
        ast = cpp_ast.cpp_ast_finder().visit(ast)
        # And return the modified ast
        return ast


    def evaluate(self, ast_node):
        r"""
        Evaluate the ast over the file that we have been asked to run over
        """
        # Visit the AST to generate the code
        qv = query_ast_visitor()
        qv.visit(ast_node)
        data_pathname = self.dataset_source
        
        # open the input root file
        # need to change to read tree name from RDF_example.py
        RDF = ROOT.ROOT.RDataFrame
        file   = RDF("recoTree", data_pathname)

        # colNames contains the names of existing branches that will be passed to the output file
        # defNames contains the names of new branches to be Defined in RDF
        colNames = ROOT.std.vector("string")()
        defNames = ROOT.std.vector("string")()

        list = (ast_node.rep,)
        if type(ast_node.rep)==tuple:
            list=ast_node.rep
   
    # need to do a proper loop here!
        for var in list:    
            existingVar = 0
            for col in file.GetColumnNames():
                if col == var:
                    existingVar = 1
                    colNames.push_back(var)
            if existingVar==0:
                if(type(var) is not ROOT.std.vector("string")):
                    # var is a str, not a vector of str
                    defNames.push_back(var)
                else:
                    for var_tup in var: 
                        existingVar = 0
                        for col_tup in file.GetColumnNames():
                            if col_tup == var_tup:
                                existingVar = 1
                                colNames.push_back(var_tup)
                        if existingVar==0:  
                            defNames.push_back(var_tup) 

        output_file = "skimmed.root"   
        doFilter=False
        #all this naming needs fixing
        #also the flag doFilter is not well defined
        doflatten=False
        for defn in defNames:
            #newCol is the name of the new branch
            if(defn.find('double') >-1):
                 newCol = "minDR"
            else:
                 newCol = defn
            newCol = newCol.replace("/", "O")
            newCol = newCol.replace(">", "Gt")
            newCol = newCol.replace("<", "Lt")
            newCol = newCol.replace(".", "")
            newCol = newCol.replace("+", "Plus")
            newCol = newCol.replace("*", "times")
            newCol = newCol.replace(".flatten()", "flat")
            newCol = newCol.replace("[", "where")
            newCol = newCol.replace("]", "")

            if("Gt" in newCol): 
                doFilter=True

            # if creation of new variable: just Define
            # if selection: filter and defn. Filter does not work with x/10, it needs a bool or a comparison
            #file = file.Define(newCol,defn)
            if("flatten" in defn): 
                defn = defn.replace(".flatten()", "")   
                doflatten=True 
            if doFilter:
                file = file.Filter(defn).Define(newCol,defn)
            else:
                defn = defn.replace("compute_mindR", "")   
                file = file.Define(newCol,defn) 
            
                
            colNames.push_back(newCol)


        if len(colNames)>0:
            file.Snapshot("recoTree", output_file, colNames)
            data_file = uproot.open(output_file)
            ast_node.rep = data_file["recoTree"].pandas.df(flatten=doflatten)
            data_file._context.source.close()

        return ast_node.rep #pandas df containing the result
