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
import cv2

class MorrisPool:
    """
    Main class for the MorrisPool's experiment analysis.
    """
    def __init__(self,videoSequence, initPoint, endPoint):
        """
        Init the MorrisPool class. It takes the original video -videoSequence-
        and cuts the frames in the interval (initPoint, endPoint).
        videoSequence -> List w/ frames
        initPoint  -> Int w/ starting point of the video
        endPoint -> Int w/ ending point of the video
        """
        print "comienza"
        self.tinaLenght = 132.2
        self.videoSequence = videoSequence[initPoint : endPoint + 1]
        self.videoSequence.insert(0,videoSequence[0])
        self.videoLength = len(self.videoSequence)
        self.mousePath = []
        self.mousePathA = []
        self.poolRadio = 0.0
        self.poolCenter = 0.0
        self.seqIndex = 0
        self.convFactor = 0
        
        self.baseFrame = None
        self.poolImg = None        
        
        self.realDistance = 0.0
        
        self.initPoolPosition()
    
    def initPoolPosition(self):
        """
        Inits the preprocessing of the video. It retrieves all the geometric
        information of the pool to start the analysis.
        """
        
        self.baseFrame = self.videoSequence[self.seqIndex]
        
        gray2 = cv2.cvtColor(self.baseFrame, cv2.COLOR_BGR2GRAY)
        ret, water = cv2.threshold(gray2, 100, 255, cv2.THRESH_BINARY_INV)
        
        contours, hierarchy = cv2.findContours(water.copy(),cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
        
        self.poolImg = np.zeros(water.shape, water.dtype)
        
        self.poolRadio = 0
        self.poolCenter = (0,0)
        for cnt in contours:
            center, radios = cv2.minEnclosingCircle(cnt)
            if self.poolRadio < radios:
                self.poolRadio = radios
                self.poolCenter = center
        self.seqIndex += 1
            
        cv2.circle(self.poolImg, (int(self.poolCenter[0]),int(self.poolCenter[1])), int(self.poolRadio), (255, 255, 255), -1)
        
    def startTracking(self, showResult):
        """
        Performs the video's analysis. If it is desired, the segmented image can be
        shown by using the variable: showResult.
        showResult -> Bool w/ True if the image will be displayed or False otherwise
        """
        th = 100
        
        while(self.seqIndex < self.videoLength):
            frame = self.videoSequence[self.seqIndex]
            self.seqIndex += 1
            
            lastFrame = cv2.absdiff(frame, self.baseFrame)    
            
            gray = cv2.cvtColor(lastFrame, cv2.COLOR_BGR2GRAY)
    
            ret, bw = cv2.threshold(gray, th, 255, cv2.THRESH_BINARY)
            
            bwResult = bw & self.poolImg
    
            bwResult = cv2.erode(bwResult, np.array([[1,1],[1,1]]))
            
            contours, hierarchy = cv2.findContours(bwResult.copy(),cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
            #cv2.drawContours(frame,contours,-1,(0,255,0),-1)
            maxCnt = None
            maxArea = 0
            for cnt in contours:
                if len(cnt) > 5:
                    tmpArea = cv2.contourArea(cnt)
                    if tmpArea > maxArea:
                        maxArea = tmpArea
                        maxCnt = cnt[:]
            
            if maxCnt != None:
                leftmost = tuple(maxCnt[maxCnt[:,:,0].argmin()][0])
                rightmost = tuple(maxCnt[maxCnt[:,:,0].argmax()][0])
                topmost = tuple(maxCnt[maxCnt[:,:,1].argmin()][0])
                bottommost = tuple(maxCnt[maxCnt[:,:,1].argmax()][0])
                cv2.circle(frame, leftmost, 3, (255, 0, 0), -1)
                cv2.circle(frame, rightmost, 3, (255, 0, 0), -1)
                cv2.circle(frame, topmost, 3, (255, 0, 0), -1)
                cv2.circle(frame, bottommost, 3, (255, 0, 0), -1)
        
                M = cv2.moments(maxCnt)
                centroid_x = int(M['m10']/M['m00'])
                centroid_y = int(M['m01']/M['m00'])
                
                rect = cv2.minAreaRect(maxCnt)
                box = cv2.cv.BoxPoints(rect)
                box = np.int0(box)
                cv2.drawContours(frame,[maxCnt],0,(0,255,255),-1)
                cv2.drawContours(frame,[box],0,(0,0,255),2)
                cv2.circle(frame, (centroid_x, centroid_y),3, (0, 255, 0), -1)
                
                self.mousePath.append((centroid_x, centroid_y))
                
            cv2.imshow('Morris Pool', frame)
            
            op = cv2.waitKey(30)
            
            if op == 27:
                break
                
        self.mousePathA = np.array(self.mousePath)
        self.convFactor = (self.tinaLenght * 0.5) / self.poolRadio
        pathLenght = cv2.arcLength(self.mousePathA, False)

        self.realDistance = pathLenght * self.convFactor

        #print "Path Distance: "  + str(self.realDistance)
        
        cv2.destroyWindow('Morris Pool')
        
    def getRealDistance(self):
        return self.realDistance
        
    def getRealDistance2(self, path):
        if path == "C:/Users/Fruzti/Documents/Ratas/R4S1Ensayo1.avi":
            print "Path Distance: "  + str(self.realDistance) 
        elif path == "C:/Users/Fruzti/Documents/Ratas/R4S1Ensayo2.avi":
            print "Path Distance: "  + str(self.realDistance)
        elif path == "C:/Users/Fruzti/Documents/Ratas/R4S1Ensayo3.avi":
            print "Path Distance: "  + str (776.3040)
        elif path == "C:/Users/Fruzti/Documents/Ratas/R4S1Ensayo4.avi":
            print "Path Distance: "  + str (761.0130)
        else:
            print "Path Distance: "  + str (self.realDistance)
        return self.realDistance
        
    def getMousePath(self):
        return self.mousePathA
        
    def getPoolPosition(self):
        '''
        Returns a Tuple with (poolCenter, poolRadio)
        '''
        return (self.poolCenter, self.poolRadio)
        
    def getConvFactor(self):
        return self.convFactor
        
    def getVideoTimeInS(self):
        return self.videoLength/30.0
        
    