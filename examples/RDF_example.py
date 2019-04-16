import ROOT

#RDF example
from clientlib.DataSets import EventDataSet

f = EventDataSet("/Users/emma/IRIS-HEP/BDTTraining_versions/allverbose_version/data16_00311402_example.root")
events = f.AsRDFEvents()
#output = events.Select('lambda e: e.eventNumber').value() # works fine
#output = events.Select('lambda e: (e.event_NJets, e.event_HT)').value() # works fine
#output = events.Select('lambda e: (e.event_NJets/10.0, e.event_HT)').value() # works fine
#output = events.Select('lambda e: e.eventNumber/10.0').value() # works fine
#output = events.Select('lambda e: e.eventNumber/e.runNumber').value() # works fine
#output = events.Select('lambda e: (e.event_NJets>3, e.event_NJets)').value()
#output = events.Select('lambda e: e.event_NJets>3').value() # works fine
#output = events.Select('lambda e: (e.event_NJets>3, e.event_NJets, e.eventNumber)').value() # works fine
#output = events.Select('lambda e: (e.CalibJet_pT)').value() # works fine
#output = events.Select('lambda e: (e.eventNumber, e.Track_pT)').value() # works fine
#output = events.Select('lambda e: e.Track_pT.Where(lambda t: t>2)').value() # works fine
output = events.Select('lambda e: (e.eventNumber, e.Track_pT.Where(lambda t: t > 2))').value() # works fine
print(output)

