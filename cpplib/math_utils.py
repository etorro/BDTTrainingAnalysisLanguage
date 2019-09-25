# Some math utilities

import cpplib.cpp_ast as cpp_ast
import cpplib.cpp_representation as crep
import cpplib.cpp_types as ctyp
from cpplib.cpp_vars import unique_name

def DeltaRAst(call_node):
    r'''
    User is trying to call DeltaR (eta1, phi1, eta2, phi2). We turn this into a call
    into a call into ROOT that does the phi subtraction (I can never get that crap right).
    '''
    print("in DeltaRAst, call_node:", call_node)
    if len(call_node.args) != 4:
        raise BaseException("Calling DeltaR(eta1, phi1, eta2, phi2) has incorrect number of arguments")
    
    # Create an AST to hold onto all of this.
    print("eta type : ", type(call_node.args[0]))
    print("eta: ", call_node.args[0])
    r = cpp_ast.CPPCodeValue()
    # We need TVector2 included here
    r.include_files += ['TVector2.h', 'math.h']

    # We need all four arguments pushed through.
    r.args = ['eta1', 'phi1', 'eta2', 'phi2']
    
    # The code is three steps
    r.running_code += ['auto d_eta = eta1 - eta2;']
    r.running_code += ['auto d_phi = TVector2::Phi_mpi_pi(phi1-phi2);']
    r.running_code += ['auto result = sqrt(d_eta*d_eta + d_phi*d_phi);']
    r.result = 'result'
    r.result_rep = lambda sc: crep.cpp_variable(unique_name('delta_r'), scope=sc, cpp_type=ctyp.terminal('double'))

    call_node.func = r
    return call_node

def DeltaR(eta1, phi1, eta2, phi2):
    'Calculate the DeltaR between two eta,phi specified vectors'
    raise BaseException('This should never be called')

# Mark the DeltaR function as one that can be called.
cpp_ast.method_names['DeltaR'] = DeltaRAst


def mindRAst(call_node):
    r'''
    User is trying to call minDeltaR (eta1, phi1, eta2, phi2). We turn this into a call
    into a call into ROOT that does the dr.
    '''
    print("in mindRAst, call_node", call_node, "type:", type(call_node))
    if len(call_node) != 4:
        raise BaseException("Calling mindR(eta1, phi1, eta2, phi2) has incorrect number of arguments")
    #print("in mindRAst, call_node0", call_node[0])
    #print("eta type : ", type(call_node[0]))
    #print("eta: ", call_node[0])
    # Create an AST to hold onto all of this.
    r = cpp_ast.CPPCodeValue()
    print("r type: ", type(r))
    # We need all four arguments pushed through.
    r.args = [call_node[0], call_node[1], call_node[1], call_node[3]]
    jet = {call_node[0] : call_node[1]}
    track = {call_node[2] : call_node[3]}

    # The code is done in 2 loops
    for jet_eta , jet_phi in jet.items():
        for trk_eta , trk_phi in track.items():
            print("jet_eta:", jet_eta, " jet_phi:", jet_phi)
            print("trk_eta:", trk_eta, " trk_phi:", trk_phi)
            r.running_code += ['auto d_eta = jet_eta - trk_eta;']
            r.running_code += ['auto d_phi = TVector2::Phi_mpi_pi(jet_phi-trk_phi);']
            r.running_code += ['auto dr = sqrt(d_eta*d_eta + d_phi*d_phi);']
            print("running code: ", r.running_code)
            #r.result = 'result'
            r.result = 10
            print("result", r.result)
            #r.result_rep = lambda sc: crep.cpp_variable(unique_name('delta_r'), scope=sc, cpp_type=ctyp.terminal('double'))
    #print("result_rep", r.result_rep, "type", type(r.result_rep))   

    #return "event_HT>10"
    return r.result
    #(expression) res = r.result_rep
    #return res
#    return 0
    #r = 10            
    #r.result = 'result'
    
    #call_node.func = r
    #print("r = ", r)
    #return r

def mindR(eta1, phi1, eta2, phi2):
    'Calculate the DeltaR between two eta,phi specified vectors'
    raise BaseException('This should never be called')

# Mark the mindR function as one that can be called.
cpp_ast.method_names['mindR'] = mindRAst