import ROOT

#RDF example
from clientlib.DataSets import EventDataSet

f = EventDataSet("data16_iso_728.root")
events = f.AsRDFEvents()
#output = events.Select('lambda e: e.eventNumber').value() # works fine
#output = events.Select('lambda e: (e.event_NCleanJets, e.event_HT)').value() # works fine
#output = events.Select('lambda e: e.eventNumber/10.0').value() # works fine
#output = events.Select('lambda e: e.eventNumber/e.runNumber').value() # works fine
output = events.Select('lambda e: e.event_NCleanJets>3').value() # works fine
#output = events.Select('lambda e: (e.event_NCleanJets>3, e.event_NCleanJets)').value()

print(output)

