# -*- coding: utf-8 -*-
"""
Tests the speed of image updates for an ImageItem and RawImageWidget.
The speed will generally depend on the type of data being shown, whether
it is being scaled and/or converted by lookup table, and whether OpenGL
is used by the view widget
"""


import initExample ## Add path to library (just for examples; you do not need this)


from pyqtgraph.Qt import QtGui, QtCore, USE_PYSIDE
import numpy as np
import pyqtgraph as pg
import pyqtgraph.ptime as ptime

import cv2 as cv

if USE_PYSIDE:
    import VideoTemplate_pyside as VideoTemplate
else:
    import VideoTemplate_pyqt as VideoTemplate


#QtGui.QApplication.setGraphicsSystem('raster')
app = QtGui.QApplication([])
#mw = QtGui.QMainWindow()
#mw.resize(800,800)

win = QtGui.QMainWindow()
win.setWindowTitle('pyqtgraph example: VideoSpeedTest')
ui = VideoTemplate.Ui_MainWindow()
ui.setupUi(win)
win.show()
ui.maxSpin1.setOpts(value=255, step=1)
ui.minSpin1.setOpts(value=0, step=1)

#ui.graphicsView.useOpenGL()  ## buggy, but you can try it if you need extra speed.

vb = pg.ViewBox()
ui.graphicsView.setCentralItem(vb)
vb.setAspectLocked()
img = pg.ImageItem()
vb.addItem(img)
vb.setRange(QtCore.QRectF(0, 0, 512, 512))


ptr = 0
lastTime = ptime.time()
fps = None

vid = cv.VideoCapture('/Users/nickgravish/Dropbox/Harvard/HighThroughputExpt/2016-08-05_12.41.20/'
                      '1_08-05-16_12-41-31.770_Fri_Aug_05_12-41-20.543_115.mp4')

NUMFRAMES = vid.get(cv.CAP_PROP_FRAME_COUNT)

direction = 0

def update():
    global ui, ptr, lastTime, fps, LUT, img


    # vid.set(cv.CAP_PROP_POS_FRAMES, ptr % NUMFRAMES)

    ret, data = vid.read(1)

    img.setImage(data, autoLevels=False)
    ui.stack.setCurrentIndex(0)
    ptr += 1

    now = ptime.time()
    dt = now - lastTime
    lastTime = now
    if fps is None:
        fps = 1.0/dt
    else:
        s = np.clip(dt*3., 0, 1)
        fps = fps * (1-s) + (1.0/dt) * s
    ui.fpsLabel.setText('%0.2f fps' % fps)
    app.processEvents()  ## force complete redraw for every plot
timer = QtCore.QTimer()
timer.timeout.connect(update)
timer.start(0)



## Start Qt event loop unless running in interactive mode or using pyside.
if __name__ == '__main__':
    import sys
    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()
