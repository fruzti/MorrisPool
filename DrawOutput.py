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

import cv2
import numpy as np
from datetime import datetime

class DrawOutput:
    '''
    Drawer Class. It is used to create the output image with the path, quadrants and 
    target.
    '''
    
    def __init__(self, rad, cen, target, path):
        '''
        Initis the DrawOutput class and performs the the translation of the points to
        the center of the image.
        '''
        self.rad = int(round(rad))
        #self.cen = int(round(cen[0])), int(round(cen[1]))
        self.img = np.ones((self.rad*2,self.rad*2),np.uint8)*255
        self.cen = self.img.shape[0]/2, self.img.shape[1]/2
        dX = int(round(self.cen[0] - cen[0]))
        dY = int(round(self.cen[1] - cen[1]))
        self.delta = np.array([dX,dY])
        
        cv2.circle(self.img, self.cen, self.rad, 0,2)
        
        self.target = np.array(target) + self.delta
        self.drawImg = self.img.copy()
        self.path = path + self.delta
        
        self.showDraw()
        
    def showDraw(self):
        '''
        Main Drawing routine. It displays the image and it allows to perform
        modification to the desired output image.
        '''
        while(True):
            cv2.imshow('Path\'s Image',self.drawImg)
            op = cv2.waitKey(30)
            
            if op == 27:
                break
                
            elif op == ord('t'):
                cv2.drawContours(self.drawImg,[np.array(self.target)]
                                    ,0,0,-1)
            elif op == ord('p'):
                cv2.drawContours(self.drawImg,[np.array(self.path)]
                                    ,0,0,2)
                                    
            elif op == ord('c'):
               cv2.line(self.drawImg, (self.cen[0],self.cen[1] + self.rad), 
                            (self.cen[0], self.cen[1] - self.rad), 0, 1)
                            
               cv2.line(self.drawImg, (self.cen[0] + self.rad,self.cen[1]), 
                            (self.cen[0] - self.rad, self.cen[1]), 0, 1)
                            
            elif op == ord('r'):
                self.drawImg = self.img.copy()
                
            elif op == ord('s'):
                self.saveDraw()
                
        cv2.destroyAllWindows()
        
    def saveDraw(self):
        '''
        Save image to the default directory in PNG format.
        '''
        i = datetime.now()
        fileName = 'Transfer_Mouse' + '-' + i.strftime('%Y-%m-%d_%H;%M;%S')
        fileName += '.png'
        
        return cv2.imwrite(fileName, self.drawImg)
