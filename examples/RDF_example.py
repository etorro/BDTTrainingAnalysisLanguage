import ROOT

#RDF example
from clientlib.DataSets import EventDataSet
from cpplib.math_utils import DeltaR
from cpplib.math_utils import mindR
#import cpplib.cpp_types as ctyp

f = EventDataSet("/Users/emma/IRIS-HEP/BDTTraining_versions/allverbose_version/data16_00311402_example.root")
events = f.AsRDFEvents()
#output = events.Select('lambda e: e.eventNumber').value() # works fine
#output = events.Select('lambda e: e.eventNumber/10.0').value() # works fine
#output = events.Select('lambda e: (e.eventNumber, e.event_HT)').value() # works fine
#output = events.Select('lambda e: (e.eventNumber/10.0, e.event_HT)').value() # works fine
#output = events.Select('lambda e: e.eventNumber/e.runNumber').value() # works fine
#output = events.Select('lambda e: e.event_NJets>3').value() # works fine
#output = events.Select('lambda e: (e.event_NJets>3, e.event_NJets)').value()# works fine
#output = events.Select('lambda e: (e.event_NJets>3, e.event_NJets, e.eventNumber)').value()# works fine
#output = events.Select('lambda e: (e.CalibJet_pT)').value()# works fine
#output = events.Select('lambda e: (e.eventNumber, e.CalibJet_pT, e.Track_pT)').value()# works fine
#output = events.Select('lambda e: e.Track_pT.Where(lambda t: t > 2.0)').value()
#output = events.Select('lambda e: (e.eventNumber, e.Track_pT.Where(lambda t: t > 2))').value()

#output = events.Select('lambda e: (e.eventNumber, e.CalibJet_pT, e.CalibJet_eta)') \
#    .Select('lambda e1: (e1[0], e1[1].Where(lambda t: t > 40.0), e1[2])') \
#    .value()

#output = events.Select('lambda e: (e.eventNumber, e.CalibJet_pT, e.CalibJet_eta)') \
#    .Select('lambda e1: (e1[0], (e1[1], e1[2]).Where(lambda t: (t[0] > 40.0)))') \
#    .value()

output = events.Select('lambda e: (e.CalibJet_eta, e.CalibJet_phi, e.Track_eta, e.Track_phi )') \
    .Select('lambda t1: compute_mindR(t1[0], t1[1], t1[2], t1[3])') \
    .value()




print(output)

