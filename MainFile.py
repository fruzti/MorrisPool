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

from MainApp import *
from MorrisPool import *
from BasicClases import *
from Pool import *
from DrawOutput import *
import cv2

def createBasePhoto(filePath,img):
    '''
    Helper function to create the image to mark the target's position.
    '''
    basePath = ''
    pathParts = filePath.split('/')
    for el in pathParts[:-1]:
        basePath += el + '/'
    basePath += 'basePhoto.png'
    
    return cv2.imwrite(basePath, img)
    
def convListToTuple(l):
    t = []
    for e in  l:
        t.append((e[0],e[1]))
    return t
    
#-------------------------------------------------------------------------------
videoSequence = None
start, end = (0,0)
mousePath = None
morrisPool = None
#-------------------------------------------------------------------------------

print 'Iniciando Aplicacion'
w = MainApp()

videoSequence = w.getVideoSequence()
(start,end) = w.getSequenceBoundaries()

print 'Creando Entorno'
print '---------------------------'
morrisPool = MorrisPool(videoSequence, start, end)

print 'Comenzando Deteccion'
print '---------------------------'
morrisPool.startTracking(None)

morrisPool.getRealDistance2(w.getPathName())

mousePath = morrisPool.getMousePath()

generateReport(mousePath, morrisPool.getRealDistance(), morrisPool.getConvFactor())

print 'Total Swimming Time[s]: ' + str(morrisPool.getVideoTimeInS())

op = raw_input('Transfer Experiment? [y/n]: ')
op = op.lower()

if op == 'y':
    print 'Continue with Transference Analysis'
    print '------------------------------------'
    (centre, rad) = morrisPool.getPoolPosition()
    p = Pool(centre, convListToTuple(mousePath), w.getPathName())
    p.analyseMousePath()
    p.showPath()
    d = DrawOutput(morrisPool.poolRadio, morrisPool.poolCenter,
        p.targetPosition,morrisPool.mousePathA)
    p.generateReport()
    print 'Analysis Finished'
    print '------------------------------------'
    print 'Done!'
    
else:
    print 'Creating Base Image...'
    print '------------------------------------'
    createBasePhoto(w.getPathName(), videoSequence[0])
    (centre, rad) = morrisPool.getPoolPosition()
    p = Pool(centre, convListToTuple(mousePath), w.getPathName())
    d = DrawOutput(morrisPool.poolRadio, morrisPool.poolCenter,
        p.targetPosition,morrisPool.mousePathA)
    print 'Done!'

