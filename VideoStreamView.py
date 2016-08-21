

import numpy as np
from pyqtgraph.Qt import QtCore, QtGui
import pyqtgraph as pg
from FastVideoLoad import FastVideoLoad

import cv2 as cv
import os


class VideoStreamView(pg.ImageView):
    """
    This will take in a video container that will handle the loading. This way
    VideoStreamView class is agnostic to how videos are handled/loaded


    """
    sigIndexChanged = QtCore.Signal(object)

    def __init__(self, video, transpose = False):
        super().__init__()

        self.video = video
        self.transpose = transpose
        self.NumFrames = self.video.getNumFrames()
        self.Height = self.video.getHeight()
        self.Width = self.video.getWidth()

        self.image = None
        self.loadFrame(1)
        self.setImage(self.image)

        # override the wheel event zoom functionality so that can be used for timeline changnig
        self.ui.roiPlot.wheelEvent = self.wheelEvent


    def wheelEvent(self, ev):
        sc = ev.delta()
        self.jumpFrames(sc)

    def loadFrame(self, index):

        img = self.video.getFrame(index)

        if self.transpose:
            img = img.T

        self.image = img


        #
        # if self.videomode == True :
        #     self.vid.set(cv.CAP_PROP_POS_FRAMES, index)
        #     tru, img = self.vid.read(1)
        #     img = img[:, :, 0]
        #
        # else:
        #     img = cv.imread(os.path.join(self.videostream, self.file_list[index]), cv.IMREAD_GRAYSCALE)
        #     self.image = np.array(img)
        #
        #     if self.image is not None:
        #         tru = True
        #
        # if tru:
        #     if self.transpose:
        #         img = img.T
        #
        #     self.image = img


    def jumpFrames(self, n):
        """Move video frame ahead n frames (may be negative)"""
        self.setCurrentIndex(self.currentIndex + n)

    # override so that will draw times
    def setImage(self, img, autoRange=True, autoLevels=True, levels=None, axes=None, xvals=None, pos=None, scale=None,
                 transform=None, autoHistogramRange=True):
        """
        Set the image to be displayed in the widget.

        ================== =======================================================================
        **Arguments:**
        img                (numpy array) the image to be displayed.
        xvals              (numpy array) 1D array of z-axis values corresponding to the third axis
                           in a 3D image. For video, this array should contain the time of each frame.
        autoRange          (bool) whether to scale/pan the view to fit the image.
        autoLevels         (bool) whether to update the white/black levels to fit the image.
        levels             (min, max); the white and black level values to use.
        axes               Dictionary indicating the interpretation for each axis.
                           This is only needed to override the default guess. Format is::

                               {'t':0, 'x':1, 'y':2, 'c':3};

        pos                Change the position of the displayed image
        scale              Change the scale of the displayed image
        transform          Set the transform of the displayed image. This option overrides *pos*
                           and *scale*.
        autoHistogramRange If True, the histogram y-range is automatically scaled to fit the
                           image data.
        ================== =======================================================================
        """

        if hasattr(img, 'implements') and img.implements('MetaArray'):
            img = img.asarray()

        if not isinstance(img, np.ndarray):
            required = ['dtype', 'max', 'min', 'ndim', 'shape', 'size']
            if not all([hasattr(img, attr) for attr in required]):
                raise TypeError("Image must be NumPy array or any object "
                                "that provides compatible attributes/methods:\n"
                                "  %s" % str(required))

        self.image = img
        self.imageDisp = None

        self.tVals = np.arange(self.NumFrames)


        self.axes = {'t': 0, 'x': 1, 'y': 2, 'c': None}

        for x in ['t', 'x', 'y', 'c']:
            self.axes[x] = self.axes.get(x, None)


        self.currentIndex = 0
        self.updateImage(autoHistogramRange=autoHistogramRange)
        if levels is None and autoLevels:
            self.autoLevels()
        if levels is not None:  ## this does nothing since getProcessedImage sets these values again.
            self.setLevels(*levels)

        if self.ui.roiBtn.isChecked():
            self.roiChanged()


        if self.axes['t'] is not None:
            # self.ui.roiPlot.show()
            self.ui.roiPlot.setXRange(self.tVals.min(), self.tVals.max())
            self.timeLine.setValue(0)
            # self.ui.roiPlot.setMouseEnabled(False, False)
            if len(self.tVals) > 1:
                start = self.tVals.min()
                stop = self.tVals.max() + abs(self.tVals[-1] - self.tVals[0]) * 0.02
            elif len(self.tVals) == 1:
                start = self.tVals[0] - 0.5
                stop = self.tVals[0] + 0.5
            else:
                start = 0
                stop = 1
            for s in [self.timeLine, self.normRgn]:
                s.setBounds([start, stop])
                # else:
                # self.ui.roiPlot.hide()

        self.imageItem.resetTransform()
        if scale is not None:
            self.imageItem.scale(*scale)
        if pos is not None:
            self.imageItem.setPos(*pos)
        if transform is not None:
            self.imageItem.setTransform(transform)


        if autoRange:
            self.autoRange()
        self.roiClicked()


    def updateImage(self, autoHistogramRange=True):
        ## Redraw image on screen
        if self.image is None:
            return

        image = self.getProcessedImage()

        if autoHistogramRange:
            self.ui.histogram.setHistogramRange(self.levelMin, self.levelMax)

        self.imageItem.updateImage(self.image)
        self.ui.roiPlot.show()


    def setCurrentIndex(self, ind):
        """Set the currently displayed frame index."""
        self.currentIndex = np.clip(ind, 0, self.NumFrames - 1)

        self.loadFrame(self.currentIndex)

        self.updateImage()
        self.ignoreTimeLine = True
        self.timeLine.setValue(self.tVals[self.currentIndex])
        self.ignoreTimeLine = False
        self.sigIndexChanged.emit(self.currentIndex)

    def timeLineChanged(self):
        # (ind, time) = self.timeIndex(self.ui.timeSlider)
        if self.ignoreTimeLine:
            return
        self.play(0)
        (ind, time) = self.timeIndex(self.timeLine)
        if ind != self.currentIndex:
            self.setCurrentIndex(ind)
            self.updateImage()
        # self.timeLine.setPos(time)
        # self.emit(QtCore.SIGNAL('timeChanged'), ind, time)
        self.sigTimeChanged.emit(ind, time)


## Start Qt event loop unless running in interactive mode.
if __name__ == '__main__':

    import sys

    # vidlist = ['/Users/nickgravish/Dropbox/Harvard/HighThroughputExpt/2016-08-05_12.41.20/1_08-05-16_12-41-31.770_Fri_Aug_05_12-41-20.543_115.mp4',
    #            '/Users/nickgravish/Dropbox/Harvard/HighThroughputExpt/2016-08-05_12.41.20/2_08-05-16_12-41-30.951_Fri_Aug_05_12-41-20.548_115.mp4']

    vidlist = ['/Users/nickgravish/Dropbox/Harvard/HighThroughputExpt/2016-08-05_12.41.20/1/',
               '/Users/nickgravish/Dropbox/Harvard/HighThroughputExpt/2016-08-05_12.41.20/2/']

    ## Always start by initializing Qt (only once per application)
    app = QtGui.QApplication([])

    ## Define a top-level widget to hold everything
    w = QtGui.QWidget()
    w.resize(1200, 600)
    w.move(QtGui.QApplication.desktop().screen().rect().center() - w.rect().center())

    ## Create image view widgets
    imviews = [VideoStreamView(vid, transpose=True) for vid in vidlist]

    ## Create a grid layout to manage the widgets size and position
    layout = QtGui.QGridLayout()
    w.setLayout(layout)

    ## Add widgets to the layout in their proper positions
    [layout.addWidget(imv, kk % (len(imviews) / 2), int(kk >= len(imviews) / 2)) for kk, imv in enumerate(imviews)]

    w.show()

    # [imv.play(50) for imv in imviews]

    imviews[0].sigIndexChanged.connect(imviews[1].setCurrentIndex)
    # imviews[1].sigIndexChanged.connect(imviews[0].setCurrentIndex)

    imviews[0].sigTimeChanged.connect(imviews[1].setCurrentIndex)
    imviews[1].sigTimeChanged.connect(imviews[0].setCurrentIndex)

    imviews[0].play(50)


    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()

