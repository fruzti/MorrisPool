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

import numpy as np
import math

class VectorPolar:
    
    def __init__(self, x, y, centre):
        '''
        Vector init function.
        @param x,y int vector space-coordinates
        @param (x1,y1) int tuple w/ centre coordinates
        '''
        
        self.centre = centre
        self.rho = self.calculateRho(x, y, centre)
        self.theta = self.calculateTheta(x, y, centre) # radians
        
        self.ghostCoords = []
        
        self.createGhosts()
        
    def calculateRho(self, x,y, centre):
        '''
        Computes the rho parameter in polar coordinates with the 
        new center 'centre' and the space coordinates (x,y)
        @param x,y int vector space-coordinates
        @param centre int tuple w/ center coordinates
        @return float rho parameter for polar coordinates
        '''
        return ( np.sqrt( (x - centre[0])**2 + (y - centre[1])**2 ) )
        
    def calculateTheta(self, x,y, centre):
        '''
        Computes the theta parameter in polar coordinates with the 
        new center 'centre' and the space coordinates (x,y)
        @param x,y int vector space-coordinates
        @param centre int tuple w/ center coordinates
        @return float theta parameter for polar coordinates
        '''
        deltaX = x - centre[0]
        deltaY = y - centre[1]
        return math.atan2(deltaY, deltaX) # radians
        
    def createGhosts(self):
        '''
        Computes the ghosts' coordinates (x,y) for the new points for 
        each of the four quadrants. Store the result in 'ghostCoords'
        '''
        for i in range(1,4):
            self.ghostCoords.append(self.newGhost(i))
            
    def newGhost(self, k):
        '''
        Creates a new ghost adding a rotation of k*pi radians.
        @return (x,y) w/ the new ghost's coordinates.
        '''
        x = self.rho * math.cos(self.theta + k*math.pi/2) + self.centre[0]
        y = self.rho * math.sin(self.theta + k*math.pi/2) + self.centre[1]
        return (int(round(x)),int(round(y)))
        
    def getGhostCoords(self):
        return self.ghostCoords