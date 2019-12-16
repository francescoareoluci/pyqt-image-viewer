"""ImageViewHandler module
Author: Francesco Areoluci

This module contain a class to handle the GUI view 
regarding the image and its control buttons
"""
import os
from PyQt5.QtWidgets import QApplication
from PyQt5.QtQml import QQmlEngine
from PyQt5.QtCore import QObject


## Image GUI view management class
class ImageViewHandler:
    """ Class used to handle the view changes in GUI
    
    This class is used to update the GUI (image and its controls).
    It will use signals coming from ImageHandler module in order
    to correctly update the GUI elements

    Typical usage example:

    imageViewHandler = ImageViewHandler(imageHandlerInstance)
    someSignal.connect(imageViewHandler.someSlot)
    """

    ## Constructor
    def __init__(self, win, imageController):
        """ __init__

        ImageViewHandler constructor.
        Parameters: win: engine root object, 
        imageController: instance of imageController class
        This constructor will get all the elements for the
        engine root object that will need to be modified.
        """

        self._imageController = imageController

        ## Get GUI elements
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

        ## Current path
        self._pwd = os.getcwd()


    ## Slot to be called whenever a folder is selected and no image
    # has been found
    def imageFoundHandler(self):
        """ imageFoundHandler

        This handler will update the image source, set the 
        image file name and enable left/right image rotate controls
        """
        path = self._imageController.getImagePath()
        self._displayedImage.setProperty('source', 'file://' + path)
        self._fileNameLabel.setProperty('visible', 'true')
        self._fileNameLabel.setProperty('text', '<b>Image path:</b>: ' + path)
        self.enableRotateLeftImageHandler()
        self.enableRotateRightImageHandler()


    ## Slot to be called whenever a folder is selected and at least 
    # an image has been found
    def imageNotFoundHandler(self):
        """ imageFoundHandler

        This handler will be called whenever no image is found
        on a selected folder. It will set a default image and
        disables all the image controls
        """

        print('No images found in folder')
        self._fileNameLabel.setProperty('visible', 'true')
        self._fileNameLabel.setProperty('text', '<font color=\"#c23c2b\">No images found in folder</font>')
        self._displayedImage.setProperty('source', 'file://' + self._pwd + '/assets/default_image.png')
        self.disableNextImageHandler()
        self.disablePreviousImageHandler()
        self.disableRotateLeftImageHandler()
        self.disableRotateRightImageHandler()


    ## Private class used to handle GUI management
    def _manageButton(self, enabled, button, buttonRect, buttonImage, imageName):
        """ _manageButton

        This method is used to handle the image controls update
        (enable/disable)
        """

        imagePath = 'file://' + self._pwd + '/assets/' + imageName
        backgroundColor = '#8fbccc' if enabled else '#c9bfbf'
        
        button.setProperty('enabled', enabled)
        buttonRect.setProperty('color', backgroundColor) 
        buttonImage.setProperty('source', imagePath)


    ## Slot to be called whenever the next image
    # control needs to be enabled
    def enableNextImageHandler(self):
        self._manageButton(True, self._nextButton, self._nextButtonRect, self._nextButtonImage, 'skip_forward.png')


    ## Slot to be called whenever the next image
    # control needs to be disabled
    def disableNextImageHandler(self):
        self._manageButton(False, self._nextButton, self._nextButtonRect, self._nextButtonImage, 'skip_forward_disabled.png')


    ## Slot to be called whenever the previous image
    # control needs to be enabled
    def enablePreviousImageHandler(self):
        self._manageButton(True, self._previousButton, self._previousButtonRect, self._previousButtonImage, 'skip_backward.png')


    ## Slot to be called whenever the previous image
    # control needs to be disabled
    def disablePreviousImageHandler(self):
        self._manageButton(False, self._previousButton, self._previousButtonRect, self._previousButtonImage, 'skip_backward_disabled.png')


    ## Slot to be called whenever the left rotate
    # control needs to be enabled
    def enableRotateLeftImageHandler(self):
        self._manageButton(True, self._rotateLeft, self._rotateLeftRect, self._rotateLeftImage, 'rotate_left.png')


    ## Slot to be called whenever the left rotate
    # control needs to be disabled
    def disableRotateLeftImageHandler(self):
        self._manageButton(False, self._rotateLeft, self._rotateLeftRect, self._rotateLeftImage, 'rotate_left_disabled.png')


    ## Slot to be called whenever the right rotate
    # control needs to be enabled
    def enableRotateRightImageHandler(self):
        self._manageButton(True, self._rotateRight, self._rotateRightRect, self._rotateRightImage, 'rotate_right.png')


    ## Slot to be called whenever the right rotate
    # control needs to be disabled
    def disableRotateRightImageHandler(self):
        self._manageButton(False, self._rotateRight, self._rotateRightRect, self._rotateRightImage, 'rotate_right_disabled.png')