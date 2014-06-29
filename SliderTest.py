from PIL import Image,ImageTk
import Tkinter
import numpy as np
import cv2
from VideoFile import *

root = Tkinter.Toplevel()
label = Tkinter.Label(root)
label.pack()

def callBack(event):
    print "Inicio: " + str(slideStart.get())  + "\t Fin: " + str(slideStop.get())
    #print "Mueve Slider"

frameA = Tkinter.Frame(root)
frameA.pack()

pathLabel = Tkinter.Label(frameA, text = "PathFile: ")
pathLabel.pack(side = Tkinter.LEFT)

pathName = Tkinter.StringVar()
pathText = Tkinter.Entry(frameA, width = 50, textvariable = pathName)
pathText.pack(side = Tkinter.LEFT)

def loadVideoSequence():
    print "Cargando Video.."
    filePath = pathName.get()
    try:
        video = VideoFile(filePath)
    except:
        print "Error"
        pathName.set("")
        slideStop = Tkinter.Scale(frameB, from_ = 1600, to = 1900, orient = Tkinter.HORIZONTAL, label = "Fin de Video",
                length = 300, repeatdelay = 60)
        slideStop.pack(side = Tkinter.LEFT)
    print len(video.getVideoSequence())
    print "Video Cargado..."
    
loadButton = Tkinter.Button(frameA, text = "Load Video", command = loadVideoSequence)
loadButton.pack(side = Tkinter.LEFT)

frameB = Tkinter.Frame(root)
frameB.pack()

slideStart = Tkinter.Scale(frameB, from_ = 0, to = 300, orient = Tkinter.HORIZONTAL, label = "Inicio de Video",
                length = 300, repeatdelay = 60)

slideStart.pack(side = Tkinter.LEFT)



img = None
tkimg = [None]

cap = cv2.VideoCapture(1)

delay = 30

def startApp():
    print "Inicia Analisis..."
    cap.release()
    label.destroy()
    root.destroy()
    
startButton = Tkinter.Button(root, text = "Start Analysis", command = startApp)

startButton.pack()

def key(event):
    cap.release()
    global root
    global label
    label.destroy()
    root.destroy()
    
def loopCapture():
    ret, frame = cap.read()
    if ret:
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        #shrinkFrame = cv2.resize(frame, (frame.shape[1]/2, frame.shape[0]/2))
        mergedFrame = np.concatenate((frame, frame), axis = 1)
        img = Image.fromarray(mergedFrame)
        tkimg[0] = ImageTk.PhotoImage(img)
        label.config(image=tkimg[0])
    #print "Valor: " + str(slideStart.get())
    root.update_idletasks()
    root.after(delay, loopCapture)
    
#root.bind("<Key>", key)
#slideStop.bind("<ButtonRelease-1>", callBack)
#slideStart.bind("<ButtonRelease-1>", callBack)
loopCapture()
root.mainloop()