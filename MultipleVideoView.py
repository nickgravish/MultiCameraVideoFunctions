
import numpy as np
from pyqtgraph.Qt import QtCore, QtGui
import pyqtgraph as pg

import cv2 as cv

vidlist = ['/Users/nickgravish/Dropbox/Harvard/HighThroughputExpt/2016-08-05_12.41.20/1_08-05-16_12-41-31.770_Fri_Aug_05_12-41-20.543_115.mp4',
           '/Users/nickgravish/Dropbox/Harvard/HighThroughputExpt/2016-08-05_12.41.20/2_08-05-16_12-41-30.951_Fri_Aug_05_12-41-20.548_115.mp4']
           # '/Users/nickgravish/Dropbox/Harvard/HighThroughputExpt/2016-08-05_12.41.20/3_08-05-16_12-41-30.811_Fri_Aug_05_12-41-20.543_115.mp4',
           # '/Users/nickgravish/Dropbox/Harvard/HighThroughputExpt/2016-08-05_12.41.20/4_08-05-16_12-41-31.777_Fri_Aug_05_12-41-20.543_115.mp4',
           # '/Users/nickgravish/Dropbox/Harvard/HighThroughputExpt/2016-08-05_12.41.20/5_08-05-16_12-41-31.781_Fri_Aug_05_12-41-20.547_115.mp4',
           # '/Users/nickgravish/Dropbox/Harvard/HighThroughputExpt/2016-08-05_12.41.20/6_08-05-16_12-41-31.797_Fri_Aug_05_12-41-20.547_115.mp4']



def load_videos(vidname):
    vid = cv.VideoCapture(vidname)

    NUMFRAMES = vid.get(cv.CAP_PROP_FRAME_COUNT)
    frames = []

    for kk in range(int(NUMFRAMES)):
        tru, ret = vid.read(1)
        frames.append(ret[:, :, 0])
        print(kk)

    print(len(frames))

    ## convert to numpy array for setImage
    frames = np.asarray(frames)
    frames = frames.swapaxes(1, 2)

    return frames, vid, NUMFRAMES


## Always start by initializing Qt (only once per application)
app = QtGui.QApplication([])

## Define a top-level widget to hold everything
w = QtGui.QWidget()

## Create image view widgets
imviews = [pg.ImageView() for _ in vidlist]

## Create a grid layout to manage the widgets size and position
layout = QtGui.QGridLayout()
w.setLayout(layout)

## Add widgets to the layout in their proper positions
[layout.addWidget(imv, kk % (len(imviews)/2), int(kk >= len(imviews)/2)) for kk, imv in enumerate(imviews)]

## load in videos and set to imageviews
videos = [load_videos(vid) for vid in vidlist]
[imv.setImage(frame[0], xvals=np.linspace(1, frame[2]/100, frame[0].shape[0])) for imv, frame in zip(imviews, videos)]

w.show()



## Start Qt event loop unless running in interactive mode.
if __name__ == '__main__':
    import sys
    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()

