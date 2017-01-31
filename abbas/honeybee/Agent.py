import numpy as np
from numpy import linalg as la
import random
from math import *

class HoneyBee:
    """
    mode:
    -2 = Dancing, dacing...
    -1 = Explorer returning to hive
     0 = Exploring
     1 = Exploiter waiting
     2 = Exploiter recruited
    """
    
    hiveX = 100
    hiveY = 100

    ## Importante variables
    timeWagDance = 50                 # Time each bee spends dancing
    #broadcastedPositions = {}        # Broadcasted spots
    Nbees = 0                         # Total number of bees
    #recrutableBees = 0               # Number of bees that can be recruited

    Krecruitment = 0.1                # average recruitment per dancing bee per dt
    ### IT WAS 0.05 BEFORE...
    # Average number of recruited bee per dance: timeWagDance x Krecruitment / recrutables
    
    
    # Energy consumption parameters: dE = a + b*x**3
    dE_a = 1e-5
    dE_b = 1e-6

    
    def __init__(self, bclass, mode, x0, y0, Lx = 200, Ly = 200, v = 1.5,
                 tsigma = 3., persistence = 5):
        
        self.BeeId = self.Nbees
        HoneyBee.Nbees += 1

        ## Main definitions
        self.x = x0
        self.y = y0
        self.bclass = bclass
        self.mode = mode
        self.spot = []
        
        ## Direct channel to the Hive
        self.Hive = None
        
        
        ## Keep track of the energy
        self.energy = 0.
        
        
        ## Dyanmical variables
        self.v = v
        self.v_explore = v
        self.v_exploit = 1.0
        self.tsigma = tsigma
        self.tsigma_explore = tsigma
        self.tsigma_exploit = 2.0
        
        self.recruitedSpot = []
        
        self.wagdance_t = 0
        
        self.persistence = persistence
        
        ## Creating an explorer
        if self.bclass == 0:
            self.update    = self.move
            self.updatePos = self.DriftRandomWalk
            self.Returned  = self.explorerReturned

            # Assigning a random exploration vector
            self.new_drift_vector()
            
            self.returnCount = 0

        ## Creating an exploiter
        elif self.bclass == 1:
            #HoneyBee.recrutableBees += 1
            self.update    = self.Recruitment
            self.updatePos = self.exploiterWalk
            self.Returned  = self.exploiterReturned

            self.returnCount = 0
            
        return
    


    ###
    ### Functions to update group parameters
    ###
    
    def updatePersistence(self, RT):
        """Persistence is an individual feature, which shows how persistent a
        given bee is when exploring a given resource spot.
        """
        self.persistence = RT
        return
    
    def updateHivePosition(self, Pos):
        HoneyBee.hiveX = Pos[0]
        HoneyBee.hiveY = Pos[1]
        return
    
    def updateWagDanceDuration(self, T):
        self.timeWagDance = T
        return
    
    def updateHAvgRecruitment(K):
        """This method updates the average number of recruited bees per time
        step for all bees.
        """
        HoneyBee.Krecruitment = K
        return 


    
    ###
    ### Dynamical functions
    ### 
    
    def foundSpot(self):
        """Generic function to update the bee's status when a resource spot is
        found.
        
        Specifically, it will set spot field to the position where the
        spot was found and its mode to -1 (return to the hive).

        """
        self.spot = [int(self.x), int(self.y)]
        self.mode = -1
        return

    
    
    def move(self, scale = 3):
        
        ## Exploring
        if self.mode == 0 or self.mode == -3:
            self.updatePos()

        ## Found spot, returning home
        elif self.mode == -1:
            
            if int( abs(self.x - self.hiveX) ) < 3 and int( abs(self.y - self.hiveY) ) < 3:
                self.Returned()
                
            else:
                cons = -.3/sqrt( (self.x - self.hiveX)**2 + (self.y - self.hiveY)**2 )
                self.x += cons*scale*(self.x - self.hiveX)
                self.y += cons*scale*(self.y - self.hiveY)

        ## Dancing, dancing, she's a dancing machine...
        elif self.mode == -2:
            
            self.wagdance_t += 1

            # Stops the dance after a while
            if self.wagdance_t >= self.timeWagDance:
                
                ## Danced enough
                self.wagdance_t = 0
                
                ## Leaving the hive again
                
                # When the scout is about to leave the Hive, it has
                # two options: it may either go back to exploit the
                # same spot or try to explore the evironment.
                
                if self.persistence == 0:
                    # Exploring the environment
                    self.leaveHive(mode = 0)
                    
                else:
                    # Going back to explore
                    self.leaveHive(mode = -3)

                
                ## Stops recruitment
                self.Hive.broadcastedPositions.pop(self.BeeId)
            

        ## Oops, going too far:
        ## Makes the bee back to the hive safe and sound.
        if abs(self.x - self.hiveX) > self.hiveX or abs(self.y - self.hiveY) > self.hiveX:
            self.x = self.hiveX
            self.y = self.hiveY
            if self.bclass == 0: self.mode = 0
            else: self.mode = 1

        return
    

    def new_drift_vector(self):
        self.v_drift = np.array([random.random() - 0.5, random.random() - 0.5])
        self.v_drift /= la.norm(self.v_drift)
        self.theta = acos(self.v_drift[0])*np.sign(self.v_drift[1])
        return
    

    
    ###
    ### Dynamics when returning to the hive
    ###
    
    def exploiterReturned___OLD(self):
        """*** NAME SHOULD BE REPLACED BY RECRUITRETURNED ***
        """

        self.returnCount += 1
        
        if self.returnCount == self.persistence:
            self.mode = 1                           ## back to state Waiting for recruitments
            self.update = self.Recruitment          ## Available back to recruitment
            self.returnCount = 0
            
        else:
            self.mode = 0
            
        ## Undoing any modication
        self.x = self.hiveX
        self.y = self.hiveY
        self.updatePos = self.exploiterWalk
        
        self.Hive.addFood()
        return



    def exploiterReturned(self):
        """*** NAME SHOULD BE REPLACED BY RECRUITRETURNED ***
        """
        
        if self.returnCount == self.persistence:
            self.mode = 1                           ## back to state Waiting for recruitments
            self.update = self.Recruitment          ## Available back to recruitment
            self.returnCount = 0
            
        elif self.returnCount == 0:
            if np.random.rand() < 0.1:
                self.mode = -2
                self.broadcastSpot()
                self.returnCount += 1
            else:
                self.returnCount += 1
                self.leaveHive( mode = -3 )
            
        else:
            self.returnCount += 1
            self.leaveHive( mode = -3 )
            
        
        
        ## Undoing any modication
        self.x = self.hiveX
        self.y = self.hiveY
        self.updatePos = self.exploiterWalk
        
        self.Hive.addFood()
        
        return

    
    def explorerReturned(self):
        """*** NAME SHOULD BE REPLACED BY SCOUTRETURNED ***
        """
        
        if self.returnCount == self.persistence:
            self.leaveHive( mode = 0 )
            
        elif self.returnCount == 0:
            ## Since this is the first time, it will dance
            self.mode = -2
            self.broadcastSpot()
            self.returnCount += 1
            
        else:
            #self.mode = -3
            self.returnCount += 1
            self.leaveHive( mode = -3 )

        
        self.x = self.hiveX
        self.y = self.hiveY
        
        self.Hive.addFood()   # Adding the new resource to the hive

        return


    def leaveHive(self, mode = 0):
        """This function sets a scout to start foraging, with a new drifting
        vector.
        
        Future: expand it for recruits as well.
        
        """
        
        self.mode = mode             ## back to state Waiting for recruitments
        self.update = self.move      ## It's going to get back to explore
        
        if self.mode == 0:
            
            # Clearing spot memory
            self.spot = []
            
            # Making sure this variable is reset to 0.
            self.returnCount = 0
            
            # Restoring the exploring accuity.
            self.v = self.v_explore
            self.tsigma = self.tsigma_explore
            self.updatePos = self.DriftRandomWalk
            
            self.v_drift = self.new_drift_vector()  ## Get new drift vector
            self.recruitedSpot = []
            
        elif mode == -3:
            # Setting the accuity
            self.v = self.v_exploit
            self.tsigma = self.tsigma_exploit
            self.updatePos = self.exploiterWalk
            
            # Setting the target
            U = self.spot
            self.recruitedSpot = np.array( U )
            u = np.array( U ) - np.array([self.hiveX,self.hiveY])
            self.v_drift = u/la.norm(u)
            self.theta = acos(self.v_drift[0])*np.sign(self.v_drift[1])
            
        return 
    
    

    
    ###
    ### Recruitment and broadcasting spots
    ###
    
    def broadcastSpot(self):
        self.Hive.broadcastedPositions[self.BeeId] = self.spot
        return
    

    
    def Recruitment(self):
        Pos = np.array( self.Hive.broadcastedPositions.values() )

        #if self.Hive.Nexploiters - self.Hive.Nrecruiteds < 0 : print 'ERROR 101 -- Misscounting recruits.'
        if Pos.shape[0] > 0 and random.random() < self.Krecruitment / float( self.Hive.Nexploiters - self.Hive.Nrecruiteds ) :
            #HoneyBee.recrutableBees -= 1
            U = Pos[ np.random.choice( np.arange(Pos.shape[0]), 1 )[0] ]
            self.mode = 0
            self.update = self.move
            
            self.recruitedSpot = np.array( U )
            self.spot = self.recruitedSpot
            u = np.array( U ) - np.array([self.hiveX,self.hiveY])
            self.v_drift = u/la.norm(u)
            self.theta = acos(self.v_drift[0])*np.sign(self.v_drift[1])
            
        return
    
    
    def energyUpdate(self, dx):
        self.energy += (self.dE_a + self.dE_b*dx**3)
        return
    
    
    
    
    ###
    ### Moving Routines
    ###
    
    def stayInHive(self):
        return
    
    def StraightLine(self):
        dx = 1.0 + int( 3*random.random() ) - 1
        dy = int( 3*random.random() ) - 1

        self.x += dx
        self.y += dy
        self.energyUpdate(sqrt(dx**2 + dy**2))
        return
    
    def DriftRandomWalk(self):
        theta = self.theta + self.tsigma*(random.random() - 0.5)
        dx = self.v*cos( theta )
        dy = self.v*sin( theta )
        
        self.x += dx
        self.y += dy
        self.energyUpdate(sqrt(dx**2 + dy**2))
        return
    
    def exploiterWalk(self):
        
        theta = self.theta + self.tsigma*(random.random() - 0.5)
        dx = self.v*cos( theta )
        dy = self.v*sin( theta )
        
        self.x += dx
        self.y += dy
        self.energyUpdate(sqrt(dx**2 + dy**2))
        
        
        d = la.norm( self.recruitedSpot - np.array([self.hiveX,self.hiveY]) ) - la.norm( np.array([int(self.x),int(self.y)]) - np.array([self.hiveX,self.hiveY]) ) 
        if d < 0: self.updatePos = self.RandomWalkUpdate

        return
    
    def RandomWalkUpdate(self):
        dx = 3*(random.random() - 0.5)
        dy = 3*(random.random() - 0.5)
        
        self.x += dx
        self.y += dy
        self.energyUpdate(sqrt(dx**2 + dy**2))
        return
