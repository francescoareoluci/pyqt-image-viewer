import os
from PyQt5.QtWidgets import QApplication
from PyQt5.QtQml import QQmlEngine
from PyQt5.QtCore import QObject

class ImageViewHandler:

    ## Constructor
    def __init__(self, engine, imageHandler):
        self._imageHandler = imageHandler

        ## Get the root window and fish out the buttons.
        win = engine.rootObjects()[0]

        self._fileNameLabel       = win.findChild(QObject, 'fileNameLabel')
        self._displayedImage      = win.findChild(QObject, 'displayedImage')
        self._previousButton      = win.findChild(QObject, 'skipBackward')
        self._nextButton          = win.findChild(QObject, 'skipForward')
        self._previousButtonRect  = win.findChild(QObject, 'skipBackwardRect')
        self._nextButtonRect      = win.findChild(QObject, 'skipForwardRect')
        self._previousButtonImage = win.findChild(QObject, 'skipBackwardImage')
        self._nextButtonImage     = win.findChild(QObject, 'skipForwardImage')
        self._rotateLeft          = win.findChild(QObject, 'rotateLeft')
        self._rotateRight         = win.findChild(QObject, 'rotateRight')
        self._rotateRightRect     = win.findChild(QObject, 'rotateRightRect')
        self._rotateLeftRect      = win.findChild(QObject, 'rotateLeftRect')
        self._rotateRightImage    = win.findChild(QObject, 'rotateRightImage')
        self._rotateLeftImage     = win.findChild(QObject, 'rotateLeftImage')

        self._pwd = os.getcwd()


    def imageFoundHandler(self):
        path = self._imageHandler.getImagePath()
        self._displayedImage.setProperty('source', 'file://' + path)
        self._fileNameLabel.setProperty('visible', 'true')
        self._fileNameLabel.setProperty('text', '<b>Image path:</b>: ' + path)
        self.enableRotateLeftImageHandler()
        self.enableRotateRightImageHandler()


    def imageNotFoundHandler(self):
        print('No image in folder')
        self._fileNameLabel.setProperty('visible', 'true')
        self._fileNameLabel.setProperty('text', '<font color=\"#c23c2b\">No images found in folder</font>')
        self._displayedImage.setProperty('source', 'file://' + self._pwd + '/assets/default_image.png')
        self.disableNextImageHandler()
        self.disablePreviousImageHandler()
        self.disableRotateLeftImageHandler()
        self.disableRotateRightImageHandler()


    def enableNextImageHandler(self):
        self._nextButton.setProperty('enabled', 'true')
        self._nextButtonRect.setProperty('color', '#8fbccc')
        self._nextButtonImage.setProperty('source', 'file://' + self._pwd + '/assets/skip_forward.png')


    def disableNextImageHandler(self):
        self._nextButton.setProperty('enabled', 'false')
        self._nextButtonRect.setProperty('color', '#c9bfbf')
        self._nextButtonImage.setProperty('source', 'file://' + self._pwd + '/assets/skip_forward_disabled.png')


    def enablePreviousImageHandler(self):
        self._previousButton.setProperty('enabled', 'true')
        self._previousButtonRect.setProperty('color', '#8fbccc')
        self._previousButtonImage.setProperty('source', 'file://' + self._pwd + '/assets/skip_backward.png')


    def disablePreviousImageHandler(self):
        self._previousButton.setProperty('enabled', 'false')
        self._previousButtonRect.setProperty('color', '#c9bfbf')
        self._previousButtonImage.setProperty('source', 'file://' + self._pwd + '/assets/skip_backward_disabled.png')


    def enableRotateLeftImageHandler(self):
        self._rotateLeft.setProperty('enabled', 'true')
        self._rotateLeftRect.setProperty('color', '#8fbccc')
        self._rotateLeftImage.setProperty('source', 'file://' + self._pwd + '/assets/rotate_left.png')


    def disableRotateLeftImageHandler(self):
        self._rotateLeft.setProperty('enabled', 'false')
        self._rotateLeftRect.setProperty('color', '#c9bfbf')
        self._rotateLeftImage.setProperty('source', 'file://' + self._pwd + '/assets/rotate_left_disabled.png')


    def enableRotateRightImageHandler(self):
        self._rotateRight.setProperty('enabled', 'true')
        self._rotateRightRect.setProperty('color', '#8fbccc')
        self._rotateRightImage.setProperty('source', 'file://' + self._pwd + '/assets/rotate_right.png')


    def disableRotateRightImageHandler(self):
        self._rotateRight.setProperty('enabled', 'false')
        self._rotateRightRect.setProperty('color', '#c9bfbf')
        self._rotateRightImage.setProperty('source', 'file://' + self._pwd + '/assets/rotate_right_disabled.png')