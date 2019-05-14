import ROOT

#RDF example
from clientlib.DataSets import EventDataSet
#from cpplib.math_utils import DeltaR
#from cpplib.math_utils import mindR
#import cpplib.cpp_types as ctyp

f = EventDataSet("/Users/emma/IRIS-HEP/BDTTraining_versions/allverbose_version/data16_00311402_example.root")
events = f.AsRDFEvents()
# Select per event variable
#output = events.Select('lambda e: e.eventNumber').value() # works fine
# Operation on per event variable
#output = events.Select('lambda e: e.eventNumber/10.0').value() # works fine
# Select two per event variables
#output = events.Select('lambda e: (e.eventNumber, e.event_HT)').value() # works fine
# Select two per event variables, operate in one of them
#output = events.Select('lambda e: (e.eventNumber/10.0, e.event_HT)').value() # works fine
# Operation between per event variables
#output = events.Select('lambda e: e.eventNumber/e.runNumber').value() # works fine
# Cut in per event variable
#output = events.Select('lambda e: e.event_NJets>3').value() # works fine
# Cut in per event variable, select per event variables
#output = events.Select('lambda e: (e.event_NJets>3, e.event_NJets, e.eventNumber)').value()# works fine
# Select per jet variable
#output = events.Select('lambda e: (e.CalibJet_pT)').value()# works fine
# Select per jet variables
#output = events.Select('lambda e: (e.eventNumber, e.CalibJet_pT, e.Track_pT)').value()# works fine
# Cut in per jet variables
#output = events.Select('lambda e: e.Track_pT.Where(lambda t: t > 2.0)').value()
# Select per event, cut in per jet variables
#output = events.Select('lambda e: (e.eventNumber, e.Track_pT.Where(lambda t: t > 2))').value()

# Select per event and per jet variables, cut in 1 per jet variables
#output = events.Select('lambda e: (e.eventNumber, e.CalibJet_pT, e.CalibJet_eta)') \
#    .Select('lambda e1: (e1[0], e1[1].Where(lambda t: t > 40.0), e1[2])') \
#    .value()

# Select per event and per jet variables, cut in per jet variables for all per jets
#output = events.Select('lambda e: (e.eventNumber, e.CalibJet_pT, e.CalibJet_eta)') \
#    .Select('lambda e1: (e1[0], (e1[1], e1[2]).Where(lambda t: (t[0] > 40.0)))') \
#    .value()

# Select per event, per jet, per track variables. Cut in per jet variables and per track
output = events.Select('lambda e: (e.eventNumber, e.CalibJet_pT, e.CalibJet_eta, e.CalibJet_phi, e.Track_pT, e.Track_eta, e.Track_phi)') \
    .Select('lambda e1: (e1[0], (e1[1], e1[2], e1[3]).Where(lambda t: t[0] > 40.0), (e1[4], e1[5],e1[6]).Where(lambda t: t[0] > 2.0))') \
    .value()

# Include cpp expression !! not working yet!
#output = events.Select('lambda e: (e.CalibJet_eta, e.CalibJet_phi, e.Track_eta, e.Track_phi)') \
#    .Where('lambda t1: DeltaR(t1[0], t1[1], t1[2], t1[3])') \
#    .value()




print(output)

