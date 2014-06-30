#############################################################################
# Copyright 2014 by Mario Coutino                                           #
#                                                                           #
#                        All Rights Reserved                                #
#                                                                           #
# Permission to use, copy, modify, and distribute this software and         #
# its documentation for any purpose and without fee is hereby	            #
# granted, provided that the above copyright notice appear in all           #         
# copies and that both that copyright notice and this permission            #
# notice appear in supporting documentation, and that the name of Mario     #
# Coutino not be used in advertising or publicity pertaining to             #
# distribution of the software without specific, written prior              #
# permission.                                                               #
#                                                                           #
# MARIO COUTINO DISCLAIMS ALL WARRANTIES WITH REGARD TO THIS SOFTWARE,      #
# INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS, IN       #
# NO EVENT SHALL MARIO COUTINO BE LIABLE FOR ANY SPECIAL, INDIRECT OR       #
# CONSEQUENTIAL DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING FROM LOSS       #
# OF USE, DATA OR PROFITS, WHETHER IN AN ACTION OF CONTRACT,                #
# NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF OR IN                 #
# CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.                  #
#############################################################################

from datetime import datetime
import numpy as np
import cv2
from BasicClases import *
from PolarCoords import *

class Pool(object):
    '''
    Class designed for the Transfer's Analysis. Some of its methods are used to mark
    where the target's platform is located in the image.
    '''
    
    def __init__(self, poolCentre, mousePath, filePath):
        '''
        Init the Pool Object and starts the Target's localisation and Mouse's
        initial position for the analysis.
        poolCentre -> Int w/ the center of the pool
        mousePath -> List w/ the mouse's path
        filePath -> String w/ the path of the video
        '''
        
        self.filePath = filePath
    
        self.poolImg = cv2.imread(self.getBasePhotoPath())
        
        self.mouseState = False
        
        self.poolCentre = poolCentre
        self.mousePath = mousePath
        self.currPos = (0,0)
        
        self.xT, self.yT = (0, 0)
        self.rT  = 0
        
        self.numEntriesQuad = 0
        
        self.entriesPerQuad = {} # Format -> Dict[(i,j)] = int
        self.numTimesInQuad = {} # Format -> Dict[(i,j)] = int
        self.targetCrosses = {}
        
        for i in range(2):
            for j in range(2):
                self.numTimesInQuad[(i,j)] = 0
                self.entriesPerQuad[(i,j)] = 0
                self.targetCrosses[(i,j)] = 0
                
        self.currQuad = (0,0)
        self.prevQuad = (0,0)
        
        self.targetPosition = [] # Format -> [(x0,y0), (x1,y1), (x2,y2),(x3,y3)]
        self.targetQuad = (0,0)
        self.numTargetCrosses = 0
        self.inTarget = False
        self.prevInTarget = False
        self.targetGhostCoord = []
        
        self.initMousePosition()
        self.initTargetPosition()
        
    def getBasePhotoPath(self):
        '''
        Build the correct base photo's path for select the target position.
        Returns a string with the path.
        '''
        basePath = ''
        pathParts = self.filePath.split('/')
        for el in pathParts[:-1]:
            basePath += el + '/'
        basePath += 'basePhoto.png'
        
        return basePath
        
    def initMousePosition(self):
        '''
        Inits the mouse position with the first element of the path. Also, 
        updates the current quadrant and init the previous quadrant with the
        current quadrant.
        '''
        self.updateCurrPos(self.mousePath[0])
        self.updateCurrQuad()
        self.prevQuad = self.currQuad
        self.updateTimesInQuad()
    
    def initTargetPosition(self):
        '''
        Inits the targetPosition calling the grabTargetPosition() method
        to select the position from the image. Also, updates other target
        related variables.
        '''
        def targetCentroid():
            x, y = (0,0)
            numEl = float(len(self.targetPosition))
            for point in self.targetPosition:
                x += point[0]
                y += point[1]
            return (x/numEl,y/numEl)
            
        self.grabTargetPosition()
        self.targetQuad = self.checkCurrQuad(targetCentroid())
        self.inTarget = self.checkInTarget()
        self.prevInTarget = self.inTarget
        
        (self.xT, self.yT), self.rT = cv2.minEnclosingCircle(
                                        np.array(self.targetPosition))
                                        
        # Ghost Creation        
        v = VectorPolar(self.xT, self.yT, self.poolCentre)
        self.targetGhostCoord += [(self.xT,self.yT)]
        self.targetGhostCoord += v.getGhostCoords()
        
    def on_mouse(self,event, x, y, flag, param):
        '''
        Adds a new Vertex to the target's position at a Mouse's Click.
        OpenCV's Default Event
        param -> Vertexes' Index.
        '''
        if(event == cv2.EVENT_LBUTTONDOWN):
            self.targetPosition[param[0]] = (x,y)
            param[0] += 1 
            cv2.circle(self.poolImg, (x,y), 3, (0,255,0), -1)
            print 'Vertex #' + str(param[0]) + ' @ ' + str((x,y))

    def grabTargetPosition(self):
        '''
        Displays and image with the Target to select the position of its four
        vertices and store the tuples in the list targetPosition.
        '''
        self.targetPosition = [(),(),(),()]
        original = self.poolImg.copy()
        
        vertexNum = [0]
        winName = 'Select Target Position'
        cv2.namedWindow(winName)
        cv2.setMouseCallback(winName, self.on_mouse,vertexNum)
        
        imgTarget = self.poolImg.copy()
        showImg = self.poolImg
        
        while(True):
            cv2.imshow(winName, showImg)
            
            if vertexNum[0] > 0 and vertexNum[0] < 4:
                    showImg = self.poolImg
                    
            if vertexNum[0] == 4:
                cv2.drawContours(imgTarget,[np.array(self.targetPosition)]
                                    ,0,(0,0,255),-1)
                vertexNum[0] = 0
            
                self.poolImg = original.copy()
                showImg = imgTarget
                
            if cv2.waitKey(30) == 27:
                acc = 0
                for e in self.targetPosition:
                    acc += len(e)
                if(acc != 8):
                    print 'Target\'s Point Missing...'
                    vertexNum[0] = 0
                    self.poolImg = original.copy()
                    showImg = self.poolImg
                else:
                    break                
            
        cv2.destroyWindow(winName)        
        
        print 'Target Position @ '
        print self.targetPosition
            
    def checkCurrQuad(self, currPos):
        ''' 
        Finds in which Quadrant the currPos is found.
        Returns a Tuple with the Quadrant.
        '''
        mouseQuad = None
        
        if (currPos[0] < self.poolCentre[0] and 
                currPos[1] < self.poolCentre[1]):
                mouseQuad = (0,0)

        elif (currPos[0] >= self.poolCentre[0] and 
                currPos[1] < self.poolCentre[1]):
                mouseQuad = (0,1)
                
        elif (currPos[0] < self.poolCentre[0] and 
                currPos[1] >= self.poolCentre[1]):
                mouseQuad = (1,0)                
                
        elif (currPos[0] >= self.poolCentre[0] and 
                currPos[1] >= self.poolCentre[1]):
                mouseQuad = (1,1)
                
        return mouseQuad
        
    def updateCurrQuad(self):
        '''
        Updates the current Quadrant with the current mouse position.
        '''
        self.prevQuad = self.currQuad
        self.currQuad = self.checkCurrQuad(self.currPos)
    
    def updateTimesInQuad(self):        
        '''
        Increase the num of frames in which the mouse is found in
        the current quadrant.
        '''
        self.numTimesInQuad[self.currQuad] += 1
        
    def checkEntryToTargetQuadrad(self):
        '''
        Increase the number of entries to the Quadrant if the mouse
        crosses the boundary into the target's Quadrant.
        '''
        if self.currQuad != self.prevQuad: #and self.currQuad == self.targetQuad:
            self.entriesPerQuad[self.currQuad] += 1
            #self.numEntriesQuad += 1
            
    def point_in_poly(self, x,y,poly):
        '''
        Checks if a desired point (x,y) is inside the polygon (poly).
        Where poly is a list with (x,y) coordinates.
        Returns True if the point is inside of False otherwise.
        '''
        n = len(poly)
        inside = False

        p1x,p1y = poly[0]
        for i in range(n+1):
            p2x,p2y = poly[i % n]
            if y > min(p1y,p2y):
                if y <= max(p1y,p2y):
                    if x <= max(p1x,p2x):
                        if p1y != p2y:
                            xints = (y-p1y)*(p2x-p1x)/(p2y-p1y)+p1x
                        if p1x == p2x or x <= xints:
                            inside = not inside
            p1x,p1y = p2x,p2y

        return inside
                
    def pointInGhosts(self):
        '''
        Checks if currPos is inside in one of the Target' Ghosts or inside the
        Target. Return True if it is inside, False otherwise.
        '''
        for point in self.targetGhostCoord:
            if np.sqrt((point[0] - self.currPos[0])**2 + 
                            (point[1] - self.currPos[1])**2) < self.rT:
                return True
        return False
        
    def checkInTarget(self):
        '''
        Checks if the mouse's current position is inside the target's space.
        Returns True if it is inside or False otherwise.
        '''
        #return self.point_in_poly(self.currPos[0], self.currPos[1], 
                            #self.targetPosition)
        return self.pointInGhosts()
        
    def updateInTarget(self):
        '''
        Updates the inTarget calling the checkInTarget method and storages
        the previous state in prevInTarget.
        '''
        self.prevInTarget = self.inTarget
        self.inTarget = self.checkInTarget()
    
    def checkTargetIsCrossed(self):
        '''
        Checks if the target is crossed and increments it if it is true. 
        Compares the last state of inTarget to find if now the mouse is outside 
        the target and previously was inside.
        '''
        if not self.inTarget and self.prevInTarget:
            #self.numTargetCrosses += 1
            self.targetCrosses[self.currQuad] += 1
            
    def updateCurrPos(self,pos):
        '''
        Updates the current position of the mouse in the pool.
        '''
        self.currPos = pos
        
    def analyseMousePath(self):
        '''
        Performs the mouse path's analysis filling the related variables.
        '''
        for pos in self.mousePath[1:]:
            self.updateCurrPos(pos)
            self.updateCurrQuad()
            self.updateTimesInQuad()
            self.checkEntryToTargetQuadrad()
            self.updateInTarget()
            self.checkTargetIsCrossed()
            
    def showPath(self):
        '''
        Shows the mouse's path, the target and the pool's sectors.
        '''
        mapImg = np.zeros(self.poolImg.shape, self.poolImg.dtype)
        for pos in self.mousePath:
            cv2.circle(mapImg,pos,1,(255,255,255),-1)
        
        cv2.drawContours(mapImg,[np.array(self.targetPosition)]
                                    ,0,(255,0,0),-1)
                                    
        cv2.circle(mapImg, (int(self.xT), int(self.yT)), int(self.rT), (255, 0, 0), -1)
        
        # Ghost Creation        
        v = VectorPolar(self.xT, self.yT, self.poolCentre)
        ghostCoord = v.getGhostCoords()
        for point in ghostCoord:
            cv2.circle(mapImg, point, int(self.rT), (255,255,0), -1)
        
        cv2.circle(mapImg,self.mousePath[0],2,(0,255,0),-1)
        cv2.circle(mapImg,self.mousePath[-1],2,(0,0,255),-1)
        #------------------------------------------------------------
        
        cv2.line(mapImg, (int(self.poolCentre[0]),0), 
        (int(self.poolCentre[0]),self.poolImg.shape[0]),(0,255,255))

        cv2.line(mapImg, (0,int(self.poolCentre[1])), 
        (self.poolImg.shape[1],int(self.poolCentre[1])),(0,255,255))
                
        while(True):
            cv2.imshow('Mouse Path', mapImg)
            if cv2.waitKey(30) == 27:
                break
                
        cv2.destroyAllWindows()
        
    def getNumEntriesQuad(self):
        return self.numEntriesQuad
        
    def getNumTimesInQuad(self):
        return self.numTimesInQuad
        
    def getTimeInQuad(self):
        '''
        Returns the number of seconds in each of the quadrants.
        '''
        timeInQuad = {}
        for key in self.numTimesInQuad:
            timeInQuad[key] = self.numTimesInQuad[key] / 30.0
        return timeInQuad.copy()
        
    def getNumTargetCrosses(self):
        return self.numTargetCrosses
    
    def getTotalTime(self):
        timeInQuad = self.getTimeInQuad()
        return sum(timeInQuad.values())
        
    def generateReport(self):
        '''
        '''
        i = datetime.now()
        fileName = 'Transfer_Mouse' + '-' + i.strftime('%Y-%m-%d_%H;%M;%S') + '.txt'
        
        # Num of crosses of target's quadrant
        self.numEntriesQuad = self.entriesPerQuad[self.targetQuad]
        printReport([self.numEntriesQuad], 
            ['Number of Entries:'], 
            'Number of Entries to the Target\'s Quadrant', fileName, 'a')
            
        # Num of entries in  each quadrant
        keys = self.entriesPerQuad.keys()
        values = self.entriesPerQuad.values()
        printReport(values, 
            keys, 
            'Entries in each Quadrant', fileName, 'a')
        
        # Time in Target's quadrant
        printReport([self.numTimesInQuad[self.targetQuad]/30.0], 
            ['Time[s] in Target\'s Quadrant:'], 
            'Number of Seconds in Target\'s Quadrant', fileName, 'a')
            
        # Time in each quadrant
        timeInQuad = self.getTimeInQuad()
        keys = timeInQuad.keys()
        values = timeInQuad.values()
        printReport(values, 
            keys, 
            'Time[s] in each Quadrant', fileName, 'a')
            
        # Time target is crossed
        self.numTargetCrosses = self.targetCrosses[self.targetQuad]
        printReport([self.numTargetCrosses], 
            ['Number of Crosses:'], 
            'Number of Times the Target is Crossed', fileName, 'a')
            
        # Times each Ghost is crossed
        crosses = self.targetCrosses.values()
        keys = self.targetCrosses.keys()
        printReport(crosses, 
            keys, 
            'Times each Possible Target\'s zone is Crossed', fileName, 'a')
        
            
        
        
        
        
        