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

# We assume the uppercorner as (0,0) and the downcorner as (m,n) in a 
# m x n cartesian space.
########################################################################
from datetime import datetime


########################################################################
import pylab
import numpy as np

def plotMousePath(mousePosition, numCols, numRows, name = 'Mouse'):
    '''
    Plots the tracking of the mouse's position over the simulation. 
        mousePosition -> List with the Position for each timeStep
    '''
    pointX = mousePosition[0:,0]
    pointY = mousePosition[0:,1]
    
    totalWidth = max(pointX) + 10
    totalHeight = max(pointY) + 10
    
    width = totalWidth / numRows
    height = totalHeight / numCols
        
    #totalWidth = numCols * width
    #totalHeight = numRows * height
    
    #pylab.figure(0)
    
    pylab.plot(pointX,pointY,'-b')
    pylab.title(name + '\'s Path')
    pylab.xlabel('X Axis')
    pylab.ylabel('Y Axis')
    pylab.ylim([totalHeight,0])
    pylab.xlim([0,totalWidth])
    pylab.plot(pointX[0],pointY[0],'or')
    pylab.plot(pointX[-1],pointY[-1],'og')
    
    ## field boundaries
    #pylab.plot([0,totalWidth],[0,0],'-k')
    #pylab.plot([0,totalWidth],[totalHeight,totalHeight],'-k')
    #pylab.plot([0,0],[0,totalHeight],'-k')
    #pylab.plot([totalWidth,totalWidth],[0,totalHeight],'-k')
    
    ## field tiles
    rows = ()
    cols = ()
    for i in range(numRows):
        pylab.plot([i*width, i*width],[0, totalHeight],'-r')
        rows += (str((i,0)),)
    for j in range(numCols):
        pylab.plot([0, totalWidth],[j*height, j*height],'-r')
        cols += (str((0,j)),)
        
    #pylab.show()
        
    #pylab.yticks(np.arange(0,totalWidth,totalWidth/numRows) + totalWidth/(2*numRows), rows)    
    #pylab.xticks(np.arange(0,totalHeight,totalHeight/numCols) + totalHeight/(2*numCols), cols)
########################################################################

def computeSpeed(mousePosition, convFactor = 1, fps = 30):
    """
    """
    
    pointX = mousePosition[0:,0]
    pointY = mousePosition[0:,1]
    
    speedX = np.diff(pointX)
    speedY = np.diff(pointY)
    
    speedX = speedX * fps * convFactor
    speedY = speedY * fps * convFactor
    
    newSpeedX, newSpeedY, newTimeX, newTimeY, tb = ([],[],[], [], [])
    
    t = np.arange(0,len(speedX)/30.0,(len(speedX)/30.0)/len(speedX))
    
    for i in range(len(speedX)):
        if speedX[i] != 0:
            newSpeedX.append(speedX[i])
            newTimeX.append(t[i])
        if speedY[i] != 0:
            newSpeedY.append(speedY[i])
            newTimeY.append(t[i])
        #if speedX[i] != 0 & speedY[i] != 0:
        #    tb.append(t[i])
        #    newSpeedX.append(speedX[i])
        #    newSpeedY.append(speedY[i])
    
    #return (speedX, speedY, t, newSpeedX, newSpeedY, newTimeX, newTimeY)
    return(newSpeedX, newSpeedY, np.array(newTimeX), np.array(newTimeY), t)
    #return(newSpeedX, newSpeedY, np.array(tb), t)

########################################################################
def printReport(data, dataLabels, dataName, fileName, mode):
    '''
    Helper function to write into the .txt report file.
    '''
    f = open(fileName, mode)
    f.write(dataName + '\n')
    bar = (len(dataName) + 2) * '-'
    f.write(bar + '\n')
    for i in range(len(data)):
        f.write(str(dataLabels[i]) + '\t\t'+ str(data[i]) + '\n')
    f.write('\n')
    f.close()
    
########################################################################
from matplotlib.backends.backend_pdf import PdfPages

def generateReport(mousePath, pathLength, convFactor = 1):
        '''
        Generates the report of the current experiment.
        '''
        print 'Creando Reporte en PDF'
        print '--------------------------'
        i = datetime.now()
        with PdfPages('Mouse' + '-' + i.strftime('%Y-%m-%d_%H;%M;%S')
                        + '.pdf') as pdf:
                        
            fileName = 'Mouse' + '-' + i.strftime('%Y-%m-%d_%H;%M;%S') + '.txt'
                
            pylab.figure(0)
            plotMousePath(mousePath, 2, 2)
            
            pdf.savefig()
            pylab.close()
            
            (speedX, speedY, tX, tY, t) = computeSpeed(mousePath, convFactor)
            #(speedX, speedY, tb, t) = computeSpeed(mousePath, convFactor)
            
            t = (t * 100).astype(int) / 100.0
            tX = (tX * 100).astype(int) / 100.0            
            tY = (tY * 100).astype(int) / 100.0               
            
            printReport(mousePath[1:,:], t, 'Mouse\'s Position (x,y)', fileName, 'a')
            
            pylab.figure(1)
            pylab.title('X-Axis Speed')
            pylab.xlabel('Time [s]')
            pylab.ylabel('Speed [cm/s]')
            pylab.plot(tX,speedX)
            
            pdf.savefig()
            pylab.close()
            
            printReport(speedX, tX, 'Mouse\'s X-Axis Speed', fileName, 'a')
    
            pylab.figure(2)
            pylab.title('Y-Axis Speed')
            pylab.xlabel('Time [s]')
            pylab.ylabel('Speed [cm/s]')
            pylab.plot(tY,speedY)
            
            printReport(speedY, tY, 'Mouse\'s Y-Axis Speed', fileName, 'a')
            
            pdf.savefig()
            pylab.close()
    
            if len(speedX) > len(speedY):
                speedX = speedX[0:len(speedY)]
            else:
                speedY = speedY[0:len(speedX)]
            pylab.figure(3)
            pylab.title('Speed Dispersion')
            pylab.xlabel('X-Axis Speed [cm/s]')
            pylab.ylabel('Y-Axis Speed [cm/s]')
            pylab.plot(speedX,speedY,'.r')
            
            pdf.savefig()
            pylab.close()
            
            printReport([pathLength], ['Distance in cm:'], 'Path Distance', fileName, 'a')
        
        print 'Reporte Concluido'
        print '--------------------------'