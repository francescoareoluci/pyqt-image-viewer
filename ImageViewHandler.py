"""ImageViewHandler module
Author: Francesco Areoluci

This module contain a class to handle the GUI view 
regarding the image and its control buttons
"""
import os
from PyQt5.QtCore import QObject, pyqtSignal
from PyQt5.QtWidgets import QApplication
from PyQt5.QtQml import QQmlEngine
from PyQt5.QtCore import QObject


## Image GUI view management class
class ImageViewHandler(QObject):
    """ Class used to handle the view changes in GUI
    
    This class is used to update the GUI (image and its controls).
    It will use signals coming from ImageHandler module in order
    to correctly update the GUI elements

    Typical usage example:

    imageViewHandler = ImageViewHandler(imageHandlerInstance)
    someSignal.connect(imageViewHandler.someSlot)
    """

    updateImageFound        = pyqtSignal(str)   # Emitted when an image has been found, used to update the qml image source
    updateImageNotFound     = pyqtSignal()      # Emitted when no image has been found, used to update the qml image source
    updateImageFoundName    = pyqtSignal(str)   # Emitted when an image has been found, used to update the qml filename label
    updateImageNotFoundName = pyqtSignal(str)   # Emitted when no image has been found, used to update the qml filename label
    enableLeftRotate        = pyqtSignal()      # Emitted when the control to rotate left the image should be enabled
    enableRightRotate       = pyqtSignal()      # Emitted when the control to rotate right the image should be enabled
    disableLeftRotate       = pyqtSignal()      # Emitted when the control to rotate left the image should be disabled
    disableRightRotate      = pyqtSignal()      # Emitted when the control to rotate right the image should be disabled

    ## Constructor
    def __init__(self, win, imageController):
        """ __init__

        ImageViewHandler constructor.
        Parameters: win: engine root object, 
        imageController: instance of imageController class
        This constructor will get all the elements for the
        engine root object that will need to be modified.
        """
        super().__init__()

        self._imageController = imageController

        # Get GUI elements
        self._fileNameLabel       = win.findChild(QObject, 'fileNameLabel')
        self._displayedImage      = win.findChild(QObject, 'displayedImage')
        self._previousButton      = win.findChild(QObject, 'skipBackward')
        self._nextButton          = win.findChild(QObject, 'skipForward')
        self._rotateLeft          = win.findChild(QObject, 'rotateLeft')
        self._rotateRight         = win.findChild(QObject, 'rotateRight')

        # Current path
        self._pwd = os.getcwd()

        # Connecting controller signals to qml functions (slots)
        self._imageController.enableNextImage.connect(self._nextButton.enableButton)
        self._imageController.disableNextImage.connect(self._nextButton.disableButton)
        self._imageController.enablePreviousImage.connect(self._previousButton.enableButton)
        self._imageController.disablePreviousImage.connect(self._previousButton.disableButton)

        # Connecting internal signals to qml functions (slots)
        self.updateImageFound.connect(self._displayedImage.handleImageUpdate)
        self.updateImageNotFound.connect(self._displayedImage.handleImageNotFoundUpdate)
        self.updateImageFoundName.connect(self._fileNameLabel.handleImageFound)
        self.updateImageNotFoundName.connect(self._fileNameLabel.handleImageNotFound)
        self.enableRightRotate.connect(self._rotateRight.enableButton)
        self.disableRightRotate.connect(self._rotateRight.disableButton)
        self.enableLeftRotate.connect(self._rotateLeft.enableButton)
        self.disableLeftRotate.connect(self._rotateLeft.disableButton)


    ## Slot to be called whenever a folder is selected and no image
    # has been found
    def imageFoundHandler(self):
        """ imageFoundHandler

        This handler will fire signals to update image, filename label
        and to enable rotate controls.
        """
        path = self._imageController.getImagePath()

        # Emit signals
        self.updateImageFound.emit(path)
        self.updateImageFoundName.emit(path)
        self.enableLeftRotate.emit()
        self.enableRightRotate.emit()


    ## Slot to be called whenever a folder is selected and at least 
    # an image has been found
    def imageNotFoundHandler(self, path):
        """ imageFoundHandler

        This handler will be called whenever no image is found
        on a selected folder. It will fire signal to update image,
        filename label and to disable rotate controls.

        Parameters 
        path: folder path
        """

        print('No images found in folder')

        # Emit signals
        self.updateImageNotFound.emit()
        self.updateImageNotFoundName.emit(path)
        self.disableLeftRotate.emit()
        self.disableRightRotate.emit()