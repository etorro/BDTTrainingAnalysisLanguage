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

#output = events.Select('lambda e: (e.event_HTMiss, e.event_NJets)') \
#    .Select('lambda t1: mindR(t1[0], t1[1], t1[2], t1[3])') \
#    .value()

#output = events.Select('lambda e: (e.runNumber, e.eventNumber, e.event_HTMiss, e.event_NJets)') \
#    .Select('lambda t1: mindR(t1[0], t1[1], t1[2], t1[3])') \
#    .value()

#output = events.Select('lambda e: (e.CalibJet_eta, e.CalibJet_phi, e.Track_eta, e.Track_phi)') \
#    .Where('lambda t1: DeltaR(t1[0], t1[1], t1[2], t1[3])') \
#    .value()

#output = events.Select('lambda e: (e.eventNumber, e.CalibJet_pT, e.CalibJet_eta, e.CalibJet_phi, e.Track_pT, e.Track_eta, e.Track_phi)') \
#    .Select('lambda e1: (e1[0], (e1[1], e1[2], e1[3]).Where(lambda t: t[0] > 40.0), (e1[4], e1[5],e1[6]).Where(lambda t: t[0] > 2.0))') \
#    .Where('lambda t1: mindR(t1[2], t1[3], t1[5], t1[6])') \
#    .value()


#    .Where('lambda t1: DeltaR(t1.eta(), t1.phi(), jInfo[1].eta(), jInfo[1].phi()) < 0.2)') \

##output = events.Select('lambda e: (e.eventNumber, e.CalibJet_pT, e.CalibJet_eta)') \
##   .Select('lambda e1: (e1[0], (e1[1], e1[2]).Where(lambda t: (t[0] > 40.0 and t[1]<2.5)))') \
##    .value()


#output = events.Select('lambda e: (e.eventNumber, e.Track_pT)').SelectMany('lambda e1: e1[1]').value()




print(output)

