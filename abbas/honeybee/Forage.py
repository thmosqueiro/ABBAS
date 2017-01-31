import numpy as np
import pylab as pl
import random
from math import *
from Agent import HoneyBee


class Forage:
    
    
    def __init__(self, Nexplorer = 5, Nexploiter = 100, T = 1500,
                 SctPersistence = 1, RecPersistence = 5):

        self.NBeesTotal = Nexplorer + Nexploiter
        
        # Area size
        self.Lx = 500
        self.Ly = 500
        
        # Resources
        self.Area = np.zeros( (self.Lx, self.Ly), dtype=int )
        self.RescMax = 50

        
        self.Nexplorers = Nexplorer
        self.Explorers = []
        for j in range(self.Nexplorers):
            self.Explorers.append(
                HoneyBee(0, 0,
                         self.Lx/2, self.Ly/2,
                         v = 1.5, tsigma = 5.,
                         persistence = SctPersistence)
            )
            self.Explorers[-1].Hive = self

        
        self.Nexploiters = Nexploiter
        self.Exploiters = []
        for j in range(self.Nexploiters):
            self.Exploiters.append(
                HoneyBee(1, 1,
                         self.Lx/2, self.Ly/2+2,
                         v = 1.0, tsigma = 2.,
                         persistence = RecPersistence )
            )
            self.Exploiters[-1].Hive = self
        
        
        ## Updating location of the hive
        self.Explorers[0].updateHivePosition([self.Lx/2, self.Ly/2])
        self.Nrecruiteds = 0
        
        
        # Broadcasted positions
        # The idea is that scout bees will use this dictionary to broadcast
        # the position of newly found spots to other bees.
        self.broadcastedPositions = {} 
        
        
        #HoneyBee.Hive = self
        Nfeatures = 5
        self.Log = np.zeros( (T, Nfeatures) )
        self.t = 0
        
        return
    
    
    
    
    ### 
    ### Resources distributions
    ### 
    
    #def resourcesPoissonPP(self, fraction = 0.0005, ri = 40.):
    def resourcesPoissonPP(self, Nres, ri = 40.):
        """Spreads resources around the area for the ants to look for. It is
        implemented as a Poisson Point process.

        """
        
        rmax = min(self.Lx, self.Ly)/2
        
        N = self.Lx * self.Ly

        self.Resx = np.zeros((Nres))
        self.Resy = np.zeros((Nres))
        for j in range(Nres):
            r = (rmax - ri)*random.random() + ri
            theta = 2*3.1415*random.random()
            self.Resx[j] = r*sin(theta) + self.Lx/2
            self.Resy[j] = r*cos(theta) + self.Ly/2
            self.Area[self.Resx[j], self.Resy[j]] = int( 5*random.random() )
        
        return
    
    def resourcesPatchy(self, Nr, size = 6, ps = 0.1, ri = 40.):
        """Spreads resources around the area for the ants to look for. It is
        implemented as a Poisson Point process.

        """

        twopi = 2*pi
        rmax = min(self.Lx, self.Ly)/2 - size
        self.Resx = np.zeros((Nr))
        self.Resy = np.zeros((Nr))
        
        for j in range(Nr):
            r = (rmax - ri)*random.random() + ri
            theta = twopi*random.random()
            self.Resx[j] = x = r*sin(theta) + self.Lx/2
            self.Resy[j] = y = r*cos(theta) + self.Ly/2

            for j in range(int(x - size), int(x + size)):
                for k in range(int(y - size), int(y + size)):
                    if random.random() <= ps: self.Area[j,k] = int( self.RescMax*random.random() )
        
        return


    
    def resourcesCircleRandom(self, Nr, R, dR, size = 6, ps = 0.1, ri = 40.):
        """Spreads resources around the area for the ants to look for. It is
        implemented as a Poisson Point process.

        """
        
        twopi = 2*pi
        self.Resx = np.zeros((Nr))
        self.Resy = np.zeros((Nr))
        
        for j in range(Nr):
            r = dR*(random.random() - 0.5) + R
            theta = twopi*random.random()
            self.Resx[j] = x = r*sin(theta) + self.Lx/2
            self.Resy[j] = y = r*cos(theta) + self.Ly/2

            for j in range(int(x - size), int(x + size)):
                for k in range(int(y - size), int(y + size)):
                    if random.random() <= ps: self.Area[j,k] = int( self.RescMax*random.random() )
        
        return


    def resourcesCircle(self, Nr, R, size = 6, ps = 0.1, ri = 40.):
        """Spreads resources around the area for the ants to look for. It is
        implemented as a Poisson Point process.

        """
        
        rmax = min(self.Lx, self.Ly)/2
        self.Resx = np.zeros((Nr))
        self.Resy = np.zeros((Nr))
        
        dTheta = 2*pi/Nr
        theta = 0.
        
        for j in range(Nr):
            theta += dTheta
            self.Resx[j] = x = R*sin(theta) + self.Lx/2
            self.Resy[j] = y = R*cos(theta) + self.Ly/2
            
            for j in range(int(x - size), int(x + size)):
                for k in range(int(y - size), int(y + size)):
                    if random.random() <= ps: self.Area[j,k] = int( self.RescMax*random.random() )
        
        return


    
    
    ### 
    ### Dynamics routines
    ### 
    
    def update(self):
        
        
        ## Updating explorerers
        for bee in self.Explorers:
            bee.update()
            if ( bee.mode == 0 or bee.mode == -3 ) and self.Area[int(bee.x),int(bee.y)].sum() > 0 :
                bee.foundSpot()
                self.Log[self.t,0] += 1
                self.Area[int(bee.x),int(bee.y)] -= 1
                
            self.Log[self.t, 2] += bee.energy

        
        ## Updating scouts
        Nrecruiteds_tmp = 0
        for bee in self.Exploiters:
            bee.update()
            if ( bee.mode == 0 or bee.mode == -3 ) and self.Area[int(bee.x),int(bee.y)].sum() > 0 :
                bee.mode = -1
                self.Area[int(bee.x),int(bee.y)] -= 1
                
            self.Log[self.t, 3] += bee.energy
            if bee.mode <= 0 : Nrecruiteds_tmp += 1
        
        
        ## Keeping track of the number of recrutable bees
        self.Nrecruiteds = Nrecruiteds_tmp
        self.Log[self.t, 4] = float( self.Nrecruiteds ) / self.Nexploiters
        
        
        self.t += 1
        return
    
    
    def addFood(self):
        self.Log[self.t,1] += 1
        return
    
    
    def picture(self, hl0, hle0, hl1):
        
        x = []
        y = []
        for bee in self.Exploiters:
            x.append(bee.x)
            y.append(bee.y)
        hl0.set_xdata(x)
        hl0.set_ydata(y)
        
        x = []
        y = []
        for bee in self.Explorers:
            x.append(bee.x)
            y.append(bee.y)
        hle0.set_xdata(x)
        hle0.set_ydata(y)
        
        x = np.nonzero( self.Area )
        hl1.set_xdata( x[0] )
        hl1.set_ydata( x[1] )
        
        return






if __name__ == "__main__":

    print '\nNo stand-alone. Import this script. You can try makeVideo.py script'
    print 'as a starting point'
    print '\n\nSee you space cowboy...\n'
