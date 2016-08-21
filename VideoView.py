# -*- coding: utf-8 -*-
"""
This example demonstrates the use of ImageView, which is a high-level widget for
displaying and analyzing 2D and 3D data. ImageView provides:

  1. A zoomable region (ViewBox) for displaying the image
  2. A combination histogram and gradient editor (HistogramLUTItem) for
     controlling the visual appearance of the image
  3. A timeline for selecting the currently displayed frame (for 3D data only).
  4. Tools for very basic analysis of image data (see ROI and Norm buttons)

"""
## Add path to library (just for examples; you do not need this)
import initExample

import numpy as np
from pyqtgraph.Qt import QtCore, QtGui
import pyqtgraph as pg

import cv2 as cv

app = QtGui.QApplication([])

## Create window with ImageView widget
win = QtGui.QMainWindow()
win.resize(800,800)
imv = pg.ImageView()
win.setCentralWidget(imv)
win.show()
win.setWindowTitle('pyqtgraph example: ImageView')

## Load a video
vid  = cv.VideoCapture('/Users/nickgravish/Dropbox/Harvard/HighThroughputExpt/2016-08-05_12.41.20/'
                       '1_08-05-16_12-41-31.770_Fri_Aug_05_12-41-20.543_115.mp4')
NUMFRAMES = vid.get(cv.CAP_PROP_FRAME_COUNT)
frames = []

for kk in range(int(NUMFRAMES)):
    tru, ret = vid.read(1)
    frames.append(ret[:,:,0])
    print(kk)

print(len(frames))

## convert to numpy array for setImage
frames = np.asarray(frames)
frames = frames.swapaxes(1,2)

## Display the data and assign each frame a time value from 1.0 to 3.0
imv.setImage(frames, xvals=np.linspace(1, NUMFRAMES/100, frames.shape[0]))

## Start Qt event loop unless running in interactive mode.
if __name__ == '__main__':
    import sys
    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()
