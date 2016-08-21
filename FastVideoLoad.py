

import cv2 as cv
from threading import Thread
import numpy as np
from pyqtgraph.Qt import QtCore, QtGui
import pyqtgraph as pg



class FastVideoLoad(Thread):

    def __init__(self, thread_id, videoname):
        Thread.__init__(self)
        self.thread_id = thread_id

        self.videoname = videoname
        self.vid = cv.VideoCapture(self.videoname)

        self.NumFrames = self.vid.get(cv.CAP_PROP_FRAME_COUNT)
        self.Height = self.vid.get(cv.CAP_PROP_FRAME_HEIGHT)
        self.Width = self.vid.get(cv.CAP_PROP_FRAME_WIDTH)

        self.frames = np.zeros((self.NumFrames, self.Height, self.Width), np.uint8)

    def run(self):
        print("Starting " + self.name)


        for kk in range(int(self.NumFrames)):
            tru, ret = self.vid.read(1)
            self.frames[kk,:,:] = ret[:, :, 0]


            if (kk % 100) == 0:
                print('thread ', self.thread_id, '    ', kk)

    def getFrame(self, ind):
        return self.frames[ind, :, :]

    def getNumFrames(self):
        return self.NumFrames

    def getHeight(self):
        return self.Height

    def getWidth(self):
        return self.Width


if __name__ == '__main__':
    import sys

    # vidlist = ['/Users/nickgravish/Dropbox/Harvard/HighThroughputExpt/2016-08-05_12.41.20/1_08-05-16_12-41-31.770_Fri_Aug_05_12-41-20.543_115.mp4',
    #            '/Users/nickgravish/Dropbox/Harvard/HighThroughputExpt/2016-08-05_12.41.20/2_08-05-16_12-41-30.951_Fri_Aug_05_12-41-20.548_115.mp4']

    vidlist = [ '/Users/nickgravish/Dropbox/Harvard/HighThroughputExpt/2016-08-05_12.41.20/1_08-05-16_12-41-31.770_Fri_Aug_05_12-41-20.543_115.mp4',
                '/Users/nickgravish/Dropbox/Harvard/HighThroughputExpt/2016-08-05_12.41.20/2_08-05-16_12-41-30.951_Fri_Aug_05_12-41-20.548_115.mp4',
                '/Users/nickgravish/Dropbox/Harvard/HighThroughputExpt/2016-08-05_12.41.20/3_08-05-16_12-41-30.811_Fri_Aug_05_12-41-20.543_115.mp4',
                '/Users/nickgravish/Dropbox/Harvard/HighThroughputExpt/2016-08-05_12.41.20/4_08-05-16_12-41-31.777_Fri_Aug_05_12-41-20.543_115.mp4',
                '/Users/nickgravish/Dropbox/Harvard/HighThroughputExpt/2016-08-05_12.41.20/5_08-05-16_12-41-31.781_Fri_Aug_05_12-41-20.547_115.mp4',
                '/Users/nickgravish/Dropbox/Harvard/HighThroughputExpt/2016-08-05_12.41.20/6_08-05-16_12-41-31.797_Fri_Aug_05_12-41-20.547_115.mp4']


    vidlist = vidlist[0:5]

    threads = [FastVideoLoad(kk, vid) for kk, vid in enumerate(vidlist)]
    [thread.start() for thread in threads]
    [thread.join() for thread in threads]

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
    videos = [thread.frames for thread in threads]
    [imv.setImage(frame, xvals=np.linspace(0, frame[0].shape[0]/100, frame[0].shape[0])) for imv, frame in zip(imviews, videos)]

    w.show()


    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()

