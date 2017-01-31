import sys
from math import *
sys.path.insert(0, '../')

from Forage import Forage
import numpy as np

T = 20000
f = 200
nreps = 120

tot        = int( sys.argv[1] )
n          = int( sys.argv[2] )
scrt       = int( sys.argv[3] )
rcrt       = int( sys.argv[4] )
npatches   = int( sys.argv[5] )
Nexploiter = tot - n

totalfood = int( (40**2)*0.6*3 )
psize = int( sqrt(totalfood/0.6/npatches) )
print psize

for j in range(nreps):
    #print 'Eval...', n, ' - Repetition: ', j
    sim = Forage(Nexplorer = n, Nexploiter = Nexploiter, T = T,
                 SctPersistence = scrt, RecPersistence = rcrt)
    sim.resourcesCircle(npatches, 200, size=psize, ps=.6)
    
    for jj in range(T):
        sim.update()
        
    #if Log == None:
    #    Log  = sim.Log
    #    Log2 = sim.Log**2
    #else:
    #    Log  += sim.Log
    #    Log2 += sim.Log**2
    
    fname = 'Log_'+str(n)+'-'+str(j)+'.log'
    print 'Printing: ' + fname
    np.savetxt(fname, sim.Log)
    
