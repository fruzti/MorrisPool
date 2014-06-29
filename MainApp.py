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

from PIL import Image,ImageTk
import Tkinter
import numpy as np
import cv2
from VideoFile import *
import MorrisPool

class MainApp(object):
    """
    """
    def __init__(self):
        """
        """
        self.videoSequence = None
        self.startIndex = 0
        self.stopIndex = 0
        #-----------------------------------
        # Parent's Level
        self.root = Tkinter.Toplevel()
        #-----------------------------------
        # First Level
        self.label = Tkinter.Label(self.root)
        self.label.pack()
        #-----------------------------------
        # Second Level
        self.frameA = Tkinter.Frame(self.root)
        self.frameA.pack()
        
        self.pathLabel = Tkinter.Label(self.frameA, text = "PathFile: ")
        self.pathLabel.pack(side = Tkinter.LEFT)
        
        self.pathName = Tkinter.StringVar() # textEdit Variable
        self.pathText = Tkinter.Entry(self.frameA, width = 50, textvariable = self.pathName)
        self.pathText.pack(side = Tkinter.LEFT)
        
        self.loadButton = Tkinter.Button(self.frameA, text = "Load Video", command = self.loadVideoSequence)
        self.loadButton.pack(side = Tkinter.LEFT)
        #-----------------------------------
        # Third Level (Not created yet...)
        self.frameB = None
        self.slideStart = None
        self.slideStop = None
        #-----------------------------------
        # Fourth Level
        self.startButton = Tkinter.Button(self.root, text = "Start Analysis", command = self.startApp)
        self.startButton.pack()
        #-----------------------------------
        self.startRotutine()
        
    def loadVideoSequence(self):
        """
        """
        filePath = self.pathName.get()
        try:
            video = VideoFile(filePath)
            self.videoSequence = video.getVideoSequence()
            del video
            videoSize = len(self.videoSequence)
            self.createThirdLevel(0, 300, videoSize - 301, videoSize - 1)
        except:
            self.pathName.set("")
    

    def createThirdLevel(self, startInit, startEnd, stopInit, stopEnd):
        """
        """
        slideSpan = 300
        #-----------------------------------
        # Third Level
        self.frameB = Tkinter.Frame(self.root)
        self.frameB.pack()

        self.slideStart = Tkinter.Scale(self.frameB, from_ = startInit, to = startEnd, orient = Tkinter.HORIZONTAL, label = "Inicio de Video",
                length = slideSpan)
        self.slideStop = Tkinter.Scale(self.frameB, from_ = stopInit, to = stopEnd, orient = Tkinter.HORIZONTAL, label = "Fin de Video",
                length = slideSpan)

        self.slideStart.pack(side = Tkinter.LEFT)
        self.slideStop.pack(side = Tkinter.LEFT)    
        
    def startApp(self):
        """
        """
        #self.morrisPool = MorrisPool(self.videoSequence[:],self.startFrame, self.stopFrame)
        #self.morrisPool.startTracking(None)
        #print 'Path Distance: ' + str(self.morrisPool.getRealDistance())
        self.root.destroy()
    
    def getVideoSequence(self):
        return self.videoSequence
        
    def getSequenceBoundaries(self):
        return (self.startIndex, self.stopIndex)
    
    def getPathName(self):
        return self.pathName.get()
        
    def startRotutine(self):
        """
        """
        #img = None
        tkimg = [None]

        delay = 30
        
        def loopCapture():
            """
            """
            if self.videoSequence != None:
                self.startIndex = self.slideStart.get()
                self.startFrame = self.videoSequence[self.startIndex]
                self.stopIndex = self.slideStop.get()
                self.stopFrame = self.videoSequence[self.stopIndex]
                #shrinkFrame = cv2.resize(frame, (frame.shape[1]/2, frame.shape[0]/2))
                mergedFrame = np.concatenate((self.startFrame, self.stopFrame), axis = 1)
                img = Image.fromarray(mergedFrame)
                tkimg[0] = ImageTk.PhotoImage(img)
                self.label.config(image=tkimg[0])
            self.root.update_idletasks()
            self.root.after(delay, loopCapture)
                
        loopCapture()
        self.root.mainloop()