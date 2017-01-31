import numpy as np
import os
import pickle
from multiprocessing import Pool
import glob


## np.savetxt('HiveSizes_tested.log', n, fmt='%5d')



def filterRaw(path):
    
    print ' >> Unpacking files...'
    os.system( 'unzip ' + path + 'data_raw.zip -d ' + path + ' >> Filter_.log' )
    
    HiveSizes = np.loadtxt(path + 'HiveSizes_tested.log')
    HiveSizes = np.array(HiveSizes, dtype=int)

    files = glob.glob(path + "Log_" + str(HiveSizes[0]) + "-*.log")
    nexps = int( max( map((lambda x: float(x.split('/')[-1].split('.log')[0].split('-')[1])), files) ) + 1 )
    print 'Number of experiments detected: ', nexps
    
    Avgs = {}     ## To save the average values
    Stds = {}     ## To save the standard deviation ( Var(X) = <X**2> - <X>**2 )
    Sqds = {}     ## To save the second momentum

    args = []
    for Size in HiveSizes:
        args.append( [ Size, path, nexps ] )

    
    print ' >> Processing everything in parallel...'
    pool = Pool(processes = 4)

    print '---'
    results = pool.map(filterRaw_thread, args)
    print '---'


    j = 0
    for Size in HiveSizes:
        Avgs[Size] = results[j][0]
        Stds[Size] = results[j][1]
        j += 1

    ## Writing both averages and standard deviations into file
    print ' >> Writing results...'
    ResFile = open( path + 'data_avgs.bin', "wb" )
    pickle.dump(Avgs, ResFile)
    ResFile.close()
    ResFile = open( path + 'data_stds.bin', "wb" )
    pickle.dump(Stds, ResFile)
    ResFile.close()

    ## Removing unzipped log files 
    print ' >> Removing tmp files...'
    os.system( 'rm ' + path + '*.log' )
    
    
    print '\n >> Filtering done.'
    
    return 1


def filterRaw_thread(args):
    
    Size  = args[0]
    path  = args[1]
    nexps = args[2]
    
    print 'Size ' + str(Size) + ': Reading...'
        
    log = np.loadtxt( path + 'Log_'+str(Size)+'-0.log' )
    logShape = log.shape
    print 'Size ' + str(Size) + ': Read, shape ' + str(logShape) + '...'
    
    Avgs = np.zeros(logShape, dtype=float)
    Stds = np.zeros(logShape, dtype=float)
    Sqds = np.zeros(logShape, dtype=float)


    print 'Size ' + str(Size) + ': Evaluating...'
    
    for j in range(nexps):
        log = np.loadtxt( path + 'Log_'+str(Size)+'-'+str(j)+'.log' )
        
        # Resources per time
        Avgs[:,0] += log[:,1]
        Sqds[:,0] += log[:,1]**2
        
        # Resources up to certain time
        cs = np.cumsum(log[:,1])
        Avgs[:,1] += cs
        Sqds[:,1] += cs**2
        
        # Evaluated energy
        Avgs[:,2] += log[:,2]
        Avgs[:,3] += log[:,3]
        Sqds[:,2] += log[:,2]**2
        Sqds[:,3] += log[:,3]**2
        
        
        # Recrutable bees
        Avgs[:,4] += log[:,4]
        Sqds[:,4] += log[:,4]**2

    
    Avgs = Avgs/float(nexps)
    Stds = np.sqrt( Sqds/float(nexps) - Avgs**2 )
    

    print 'Size ' + str(Size) + ': Done.'
    return [Avgs, Stds]
