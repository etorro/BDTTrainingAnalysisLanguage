# Code to aid with accessing jet collections
import cpplib.cpp_ast as cpp_ast
import ast

def getMomentFloatAst(call_node):
    r'''
    Return a cpp ast for this guy.
    '''
    # Get the name of the moment out
    if len(call_node.args) != 1:
        raise BaseException("Calling getMomentFloat - only one argument is allowed")
    if type(call_node.args[0]) is not ast.Str:
        raise BaseException("Calling getMomentFloat - only acceptable argument is a string")
    moment_name = call_node.args[0].s

    r = cpp_ast.CPPCodeValue()
    # We don't need include files for this - just quick access
    r.replacements['moment_name'] = moment_name
    r.replacement_instance_obj = ('obj_j', call_node.func.value.id)
    r.running_code += ['float result = obj_j->getAttribute<float>(moment_name);']
    r.result = 'result'

    # Replace it as the function that is going to get called.
    call_node.func = r

    return call_node

# Config everything.
cpp_ast.method_names['getMomentFloat'] = getMomentFloatAst