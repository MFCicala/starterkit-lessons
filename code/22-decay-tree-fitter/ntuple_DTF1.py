from GaudiConf import IOHelper
from Configurables import DaVinci, DecayTreeTuple
from DecayTreeTuple.Configuration import *

# Stream and stripping line we want to use
stream = 'AllStreams'
line = 'D2hhCompleteEventPromptDst2D2RSLine'

# Create an ntuple to capture D*+ decays from the StrippingLine line
dtt = DecayTreeTuple('TupleDstToD0pi_D0ToKpi')
dtt.Inputs = ['/Event/{0}/Phys/{1}/Particles'.format(stream, line)]
dtt.Decay = '[D*(2010)+ -> ^(D0 -> ^K- ^pi+) ^pi+]CC'

# add a kinematic fitter
from Configurables import TupleToolDecayTreeFitter,TupleToolDecay
dtt.addTool(TupleToolDecay, name = 'Dstar')
dtt.Branches["Dstar"] = "[D*(2010)+ -> (D0 -> K- pi+) pi+]CC" 
dtt.Dstar.ToolList =  ["TupleToolDecayTreeFitter/ConsD"]
dtt.Dstar.addTool(TupleToolDecayTreeFitter("ConsD"))
dtt.Dstar.ConsD.constrainToOriginVertex = True
dtt.Dstar.ConsD.Verbose = True
dtt.Dstar.ConsD.daughtersToConstrain = [ "D0" ]


# Configure DaVinci
DaVinci().UserAlgorithms += [dtt]
DaVinci().InputType = 'DST'
DaVinci().TupleFile = 'DVntuple.root'
DaVinci().PrintFreq = 1000
DaVinci().DataType = '2012'
DaVinci().Simulation = True
# Only ask for luminosity information when not using simulated data
DaVinci().Lumi = not DaVinci().Simulation
DaVinci().EvtMax = -1

# Use the local input data
IOHelper().inputFiles([
  './00035742_00000002_1.allstreams.dst'
], clear=True)
