from VideoFile import *


count = 0

while(True):
    
    if count == 5:
        print "Intentos Alcanzados"
        break
        
    try:
        video = VideoFile(VideoFile.testFileName)
        print "YA"
    except:
        count += 1
        
        