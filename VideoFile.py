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

class VideoFile(object):
    '''
    Class which contains the video information for the current
    sesion.
    '''
    
    testFileName = "C:/Users/Fruzti/Documents/Ratas/R4S1Ensayo1.avi"
    
    def __init__(self, fileName):
        """
        Inits the object, creating a new VideoCapture from 'fileName'.
        After creating, a list w/ all the video's frame is allocated.
        The VideoCapture object is release to save memory after the
        video sequence is created.
            fileName -> string w/ the video's path
        """
        self.videoFile = cv2.VideoCapture(fileName)
        
        videoOk = not self.videoFile.isOpened()
        
        assert not videoOk, "Error: Wrong File's Path..."
        
        self.fps = int(self.videoFile.get(cv2.cv.CV_CAP_PROP_FPS))
        self.videoLenght = 0 
        self.videoSequence = self.convertVideoToSequence()
        self.videoFile.release()
        
    def convertVideoToSequence(self):
        """
        Strip all the frames from the VideoCapture object and puts
        them into videoSequence.
        return list w/ self.videoFile's frames.
        """
        videoSequence = []
        
        while(True):
            ret, frame = self.videoFile.read()
            
            if frame == None:
                print "End of File Reached..."
                self.videoLenght = len(videoSequence)/30
                break
                
            videoSequence.append(frame)
            
        return videoSequence
        
    def showVideo(self):
        """
        Debug method to see the videoSequence in an OpenCV
        environment.
        """
        for frame in self.videoSequence:
            cv2.imshow("ShowSequence", frame)
            if cv2.waitKey(30) == 27:
                print "Sequence interrupted..."
                break
        print "End of File..."
        cv2.destroyAllWindows()
        
    def getVideoSequence(self):
        return self.videoSequence
        
    def getVideoFPS(self):
        return self.fps
        
    def getVideoLenght(self):
        return self.videoLenght
    