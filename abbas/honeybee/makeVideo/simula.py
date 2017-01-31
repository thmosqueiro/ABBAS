## Libraries
import pickle as pk
import random
from math import *
import numpy as np

import pylab as pl
from matplotlib import gridspec
import subprocess

import Forage


## Main parameters

T            = 10000
Nexplorer    = 270
Nexploiter   = 300 - Nexplorer
Nr           = 3
R            = 200
showOTF      = False



## Starting the Forage object
sim = Forage.Forage(Nexplorer = Nexplorer, Nexploiter = Nexploiter,
                    T = T, SctPersistence = 20, RecPersistence = 20)

sim.resourcesCircle(Nr, R, size=40, ps=.6)


Positions = []
Resources = []
Recruited = []
AreaState = []

for j in range(T):

    if j % 100 == 0: print j
    
    sim.update()
    SctPos, RecPos, areaPos = sim.exportBeePositions()
    Positions.append( [SctPos, RecPos] )
    Resources.append( sim.Log[j,1] )
    Recruited.append( sim.Log[j,4]*100 )
    AreaState.append( areaPos )



pk.dump(Positions, open('Positions.data.pk', 'wb'))
pk.dump(Resources, open('Resources.data.pk', 'wb'))
pk.dump(Recruited, open('Recruited.data.pk', 'wb'))
pk.dump(AreaState, open('AreaState.data.pk', 'wb'))


print "Done."
