

from VideoStreamView import VideoStreamView
from FastVideoLoad import FastVideoLoad
from pyqtgraph.Qt import QtCore, QtGui


if __name__ == '__main__':
    import sys

    vidlist = [ '/Users/nickgravish/Dropbox/Harvard/HighThroughputExpt/2016-08-05_12.41.20/1_08-05-16_12-41-31.770_Fri_Aug_05_12-41-20.543_115.mp4',
                '/Users/nickgravish/Dropbox/Harvard/HighThroughputExpt/2016-08-05_12.41.20/2_08-05-16_12-41-30.951_Fri_Aug_05_12-41-20.548_115.mp4',
                '/Users/nickgravish/Dropbox/Harvard/HighThroughputExpt/2016-08-05_12.41.20/3_08-05-16_12-41-30.811_Fri_Aug_05_12-41-20.543_115.mp4',
                '/Users/nickgravish/Dropbox/Harvard/HighThroughputExpt/2016-08-05_12.41.20/4_08-05-16_12-41-31.777_Fri_Aug_05_12-41-20.543_115.mp4',
                '/Users/nickgravish/Dropbox/Harvard/HighThroughputExpt/2016-08-05_12.41.20/5_08-05-16_12-41-31.781_Fri_Aug_05_12-41-20.547_115.mp4',
                '/Users/nickgravish/Dropbox/Harvard/HighThroughputExpt/2016-08-05_12.41.20/6_08-05-16_12-41-31.797_Fri_Aug_05_12-41-20.547_115.mp4']


    # vidlist = vidlist[0:2]

    threads = [FastVideoLoad(kk, vid) for kk, vid in enumerate(vidlist)]
    [thread.start() for thread in threads]
    [thread.join() for thread in threads]

    app = QtGui.QApplication([])

    ## Define a top-level widget to hold everything
    w = QtGui.QWidget()
    w.resize(1200, 600)
    w.move(QtGui.QApplication.desktop().screen().rect().center() - w.rect().center())

    ## Create image view widgets
    imviews = [VideoStreamView(vid, transpose=True) for vid in threads]

    ## Create a grid layout to manage the widgets size and position
    layout = QtGui.QGridLayout()
    w.setLayout(layout)

    ## Add widgets to the layout in their proper positions
    [layout.addWidget(imv, kk % (len(imviews) / 2), int(kk >= len(imviews) / 2)) for kk, imv in enumerate(imviews)]

    w.show()

    # [imv.play(50) for imv in imviews]

    [imviews[0].sigIndexChanged.connect(imv.setCurrentIndex) for imv in imviews[1:]]

    imviews[0].play(50)

    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()

