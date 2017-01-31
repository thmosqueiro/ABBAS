import os

npatches_ = [3]
rts       = ['05-05']
sizes     = [300]



for npatches in npatches_:
    if not os.path.isdir( str(npatches) ): 
        os.system( "mkdir " + str(npatches) )
        print 'Created folder ' + str(npatches)
    for N in sizes:
        if not os.path.isdir( str(npatches) + "/" + str(N) ): 
            os.system( "mkdir " + str(npatches) + "/" + str(N) )
            print 'Created folder ' + str(N)
        for rt in rts:
            if not os.path.isdir( str(npatches) + "/" + str(N) + "/" + rt ):
                os.system( "mkdir " + str(npatches) + "/" + str(N) + "/rt" + rt )

                scrt = rt.split('-')[0]
                rcrt = rt.split('-')[1]
                
                os.system( "python Run.py " + str(int(scrt)) + " " + str(int(rcrt)) + " " + str(N) + " " + str(npatches) )
                os.system( "zip data_raw.zip *.log " )
                os.system( "rm *.log " )
                os.system( "mv data_raw.zip " + str(npatches) + "/" +  str(N) + "/rt" + rt + "/" )
