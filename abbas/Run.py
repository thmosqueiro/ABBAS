import subprocess
import sys
import numpy as np
import sys

scrt     = int( sys.argv[1] )
rcrt     = int( sys.argv[2] )
total    = int( sys.argv[3] )
npatches = int( sys.argv[4] )

nproc = 16
Nset = np.linspace(0,total,nproc+2, dtype=int)[1:-1]
np.savetxt('HiveSizes_tested.log', Nset)

print 'Nset: ', Nset
nNs = Nset.shape[0]
Nrols = nNs / nproc + 1

for j in range(Nrols):
    Pset = []
    for N in Nset[nproc*j:min(nproc*(j+1),nNs)]:
        print N
        cmd = 'python Test1.py '+str(total)+' '+str(N)+' '+str(scrt)+' '+str(rcrt)+' '+str(npatches)
        print cmd
        Pset.append( subprocess.Popen(cmd, shell=True,
                                      stderr=subprocess.STDOUT,
                                      stdout=subprocess.PIPE)
        )

    [p.wait() for p in Pset]

    
