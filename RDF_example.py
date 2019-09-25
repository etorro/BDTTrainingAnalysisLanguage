import ROOT

#RDF example
from clientlib.DataSets import EventDataSet
from cpplib.math_utils import DeltaR
from cpplib.math_utils import mindR
#import cpplib.cpp_types as ctyp

f = EventDataSet("/Users/emma/IRIS-HEP/emmasFork/LLPRO_study_125_35.root")
events = f.AsRDFEvents()
#output = events.Select('lambda e: e.eventNumber').value() 
#output = events.Select('lambda e: e.eventNumber/10.0').value() 
#output = events.Select('lambda e: (e.eventNumber, e.event_HT)').value() 
#output = events.Select('lambda e: (e.eventNumber/10.0, e.event_HT)').value() 
#output = events.Select('lambda e: e.eventNumber/e.runNumber').value()
#output = events.Select('lambda e: e.event_L1_tauRoIsize>0').value() # works fine
#output = events.Select('lambda e: (e.event_L1_tauRoIsize>0, e.event_L1_emRoIsize, e.eventNumber)').value()
#output = events.Select('lambda e: (e.L1_tauRoI_E)').value()
#output = events.Select('lambda e: (e.eventNumber, e.L1_tauRoI_E, e.L1_emRoI_E/1000)').value()
#output = events.Select('lambda e: e.L1_tauRoI_E.Where(lambda t: t > 30.0)').value()
#output = events.Select('lambda e: (e.eventNumber, e.L1_tauRoI_E.Where(lambda t: t > 2))').value()

#output = events.Select('lambda e: (e.eventNumber, e.L1_tauRoI_E, e.L1_tauRoI_eta)') \
#    .Select('lambda e1: (e1[0], e1[1].Where(lambda t: t > 30.0), e1[2])') \
#    .value()

#output = events.Select('lambda e: (e.eventNumber, e.L1_tauRoI_E, e.L1_tauRoI_eta)') \
#    .Select('lambda e1: (e1[0], (e1[1], e1[2]).Where(lambda t: (t[0] > 30.0)))') \
#    .value()

#output = events.Select('lambda e: (e.eventNumber, e.event_L1_tauRoIsize>0, e.event_L1_emRoIsize>0, e.L1_tauRoI_E, e.L1_tauRoI_eta, e.L1_tauRoI_phi, e.L1_emRoI_E/1000, e.L1_emRoI_eta, e.L1_emRoI_phi)') \
#    .Select('lambda t: (t[0], (t[3], t[4], t[5]).Where(lambda t1: (t1[0] > 30.0)), t[6], t[7], t[8])') \
#    .value()

#output = events.Select('lambda e: newmindR(e.L1_tauRoI_eta, e.L1_tauRoI_phi, e.L1_emRoI_eta, e.L1_emRoI_phi)') \
#    .value()

output = events.Select('lambda e: (e.L1_tauRoI_E, e.L1_tauRoI_eta, e.L1_tauRoI_phi, e.L1_emRoI_eta, e.L1_emRoI_phi, e.event_L1_tauRoIsize>0, e.event_L1_emRoIsize>0, e.event_passL1_LLPNM)') \
    .Select('lambda r1: (r1[0], newmindR(r1[1], r1[2], r1[3], r1[4]), r1[5], r1[6], r1[7])') \
    .value()

#output = events.Select('lambda e: (e.L1_tauRoI_E, e.L1_tauRoI_eta, e.L1_tauRoI_phi, e.L1_emRoI_eta, e.L1_emRoI_phi, e.event_L1_tauRoIsize>0, e.event_L1_emRoIsize>0, e.event_passL1_LLPNM)') \
#    .Select('lambda r1: ((r1[0], newmindR(r1[1], r1[2], r1[3], r1[4])).Where(lambda t1: (t1[0] > 30.0), t1[1]>0), r1[5], r1[6], r1[7])') \
#    .value()



print(output)

