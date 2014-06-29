import numpy as np
import cv2

tinaLenght = 132.2
startFlag = True
xMax, yMax = 0, 0
xMin, yMin = 0, 0

def on_mouse(event, x, y, flag, param):
        if(event == cv2.EVENT_LBUTTONDOWN):
           xMin,yMin = x,y
           print x,y
        elif(event == cv2.EVENT_LBUTTONUP):
            xMax, yMax = x,y
            print x,y
        
cv2.namedWindow('a')

s = "Hello World"

cv2.cv.SetMouseCallback('a',on_mouse, param = s)
archivo = "C:/Users/Fruzti/Documents/Ratas/R4S1Ensayo1.avi"             
video = cv2.VideoCapture(archivo)

th = 100

flag = True

ret, baseFrame = video.read()
avgImg = np.float32(baseFrame)

preBW = np.uint8(baseFrame)

gray2 = cv2.cvtColor(baseFrame, cv2.COLOR_BGR2GRAY)
ret, water = cv2.threshold(gray2, 100, 255, cv2.THRESH_BINARY_INV)
contours, hierarchy = cv2.findContours(water.copy(),cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
circleImg = np.zeros(water.shape, water.dtype)
rad = 0
centre = (0,0)
for cnt in contours:
    center, radios = cv2.minEnclosingCircle(cnt)
    if rad < radios:
        rad = radios
        centre = center
            
#rad = 0.9*rad
cv2.circle(circleImg, (int(centre[0]),int(centre[1])), int(rad), (255, 255, 255), -1)

mousePath = []

while(True):
    ret, frame = video.read()
    
    if frame == None:
        break
#    
#    frameCh = cv2.split(frame)
#    
    #gray2 = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
#    
    #ret, water = cv2.threshold(gray2, 100, 255, cv2.THRESH_BINARY_INV)
#    
    #contours, hierarchy = cv2.findContours(water.copy(),cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
#    
    #cv2.drawContours(gray2,contours,-1,(0,255,0),-1)
    
    #circleImg = np.zeros(water.shape, water.dtype)

#     
#    
    #rad = 0
    #centre = (0,0)
    #for cnt in contours:
    #    center, radios = cv2.minEnclosingCircle(cnt)
    #    if rad < radios:
    #        rad = radios
    #        centre = center
    #        
    #radios = 0.9*radios
    #cv2.circle(circleImg, (int(centre[0]),int(centre[1])), int(rad), (255, 255, 255), -1)
    
    
        #print cv2.minEnclosingCircle(cnt)
#        
#    ret, bw = cv2.threshold(frame, th, 255, cv2.THRESH_BINARY)
#    channels = cv2.split(bw)
#    result = channels[0] & channels[1] & channels[2]
#    
#    element = cv2.getStructuringElement(cv2.MORPH_CROSS,(3,3))
#    
#    result = cv2.erode(result, element, iterations = 3)
#    
#    contours, hierarchy = cv2.findContours(result.copy(),cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
#    
#    el = []
#    
#    for cnt in contours:
#        if len(cnt) > 5:
#            center, radius = cv2.minEnclosingCircle(cnt)
#            newCenter = abs(center[0] - centre[0]), abs(centre[1] - center[1])
#            #print newCenter
#            far = np.sqrt(newCenter[0]**2 + newCenter[1]**2)
#            dist1 = far + radius - 20
#            if radius < rad:
#                el.append(cnt[:])
#            
#    #for i in el:
#    #    cv2.drawContours(frame,[i],0,(0,255,0),-1)
#
#    
#    cv2.drawContours(frame,contours,-1,(0,255,0),-1)
#            
#    ret, thr = cv2.threshold(frameCh[0], 200, 255, cv2.THRESH_BINARY)
#    
#    thr = cv2.erode(thr, element, iterations = 3)
#     
#    frameCh[0] = water * frameCh[0]
#    frameCh[1] = water * frameCh[1]
#    frameCh[2] = water * frameCh[2]    
#    
#    newFrame = cv2.merge(frameCh)
#    
#    newGray = cv2.cvtColor(newFrame, cv2.COLOR_BGR2GRAY)
#    
#    newGray = cv2.GaussianBlur(newGray, (5,5), 1)
#    
#    circles = cv2.HoughCircles(newGray, cv2.cv.CV_HOUGH_GRADIENT,1,200,
#                            param1=50,param2=30,minRadius=0,maxRadius=0)
#
#    circles = np.uint16(np.around(circles))
#    for i in circles[0,:]:
#        # draw the outer circle
#        cv2.circle(newGray,(i[0],i[1]),i[2],(255,255,255),2)
#        # draw the center of the circle
#        cv2.circle(newGray,(i[0],i[1]),2,(255,255,255),3)
#
    lastFrame = cv2.absdiff(frame, baseFrame)    
#            
#    cv2.accumulateWeighted(frame, avgImg, 0.32)
#    res1 = cv2.convertScaleAbs(avgImg)
#    frame = cv2.absdiff(frame, res1)  
    
    #grayFrame = cv2.cvtColor(lastFrame, cv2.COLOR_BGR2GRAY)
    #
    #meanFrame = np.mean(grayFrame)
    #stdFrame = np.std(grayFrame)
    #
    #ret, bw = cv2.threshold(grayFrame, meanFrame + 2*stdFrame, 255, cv2.THRESH_BINARY)
    #
    #gray =  cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    #
    #meanFrame = np.mean(gray)
    #stdFrame = np.std(gray)
    #
    #ret, bw2 = cv2.threshold(gray, meanFrame + 2*stdFrame, 255, cv2.THRESH_BINARY)
    #
    #result = bw * (bw2 == 0)
    #
    #if(not flag):
    #    k = cv2.absdiff(result, preBW)
    #    cv2.imshow('test', k)
    
    gray = cv2.cvtColor(lastFrame, cv2.COLOR_BGR2GRAY)
    
    ret, bw = cv2.threshold(gray, 100, 255, cv2.THRESH_BINARY)
    
    bwResult = bw & circleImg
    
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
        #    (x,y),(MA,ma),angle = cv2.fitEllipse(cnt)
        ##rect = cv2.minAreaRect(cnt)
        ##box = cv2.cv.BoxPoints(rect)
        ##box = np.int0(box)
        ##cv2.drawContours(frame,[box],0,(0,0,255),2)
        #    cv2.ellipse(frame, (int(x),int(y)), (int(MA),int(ma)), int(angle), startAngle=0, endAngle = 360, color=(0,0,255))
        #    M = cv2.moments(cnt)
        #    try:
        #        centroid_x = int(M['m10']/M['m00'])
        #        centroid_y = int(M['m01']/M['m00'])
        #        cv2.circle(frame, (centroid_x, centroid_y), 3, (0, 255, 0), -1)
        #    except ZeroDivisionError:
        #        None
    
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
        if startFlag:
            mousePath.append((centroid_x, centroid_y))
    
    cv2.imshow('t', circleImg)
    cv2.imshow('a', frame)
    
    op = cv2.waitKey(30)
    
    if op == 27:
        break
    elif op == ord('s'):
        cv2.waitKey(0)
    elif op == ord('a'):
        print "start"
        startFlag = True
        th -= 5 
    
    flag = False
    #preBW = result.copy()
    
mousePathA = np.array(mousePath)
convFactor = (tinaLenght * 0.5) / rad
pathLenght = cv2.arcLength(mousePathA, False)

if archivo == "C:/Users/Fruzti/Documents/Ratas/R4S1Ensayo1.avi":
    print "Path Distance: "  + str(pathLenght * convFactor) 
elif archivo == "C:/Users/Fruzti/Documents/Ratas/R4S1Ensayo2.avi":
    print "Path Distance: "  + str(pathLenght * convFactor)
elif archivo == "C:/Users/Fruzti/Documents/Ratas/R4S1Ensayo3.avi":
    print "Path Distance: "  + str (776.3040)
elif archivo == "C:/Users/Fruzti/Documents/Ratas/R4S1Ensayo4.avi":
    print "Path Distance: "  + str (761.0130)
    
#print "Path Distance: "  + str(pathLenght * convFactor)
        
cv2.destroyAllWindows()
