"""ImageController module
Author: Francesco Areoluci

This module contain a class to handle image state
"""
import os
import exifread
from PyQt5.QtCore import QObject, pyqtSignal
from Observables import ObservableExifData, ObservableImagePath


## Image state management class
class ImageController(QObject):
    """ Class used to handle signal regarding image coming from qml
    
    This class is used to manage all the image events that are coming
    from the view. It mantains a state in order to view the correct images.
    It support a folder selection and a single image selection.
    It also emit signal to notify if some button need to be enabled/disabled 

    Typical usage example:

    imageController = ImageController()
    imageController.exifDataReady.connect(someSlot)
    exif = imageController.getExifData()
    imagePath = imageController.getImagePath()
    """

    exifDataReady          = pyqtSignal()
    imageFound             = pyqtSignal()
    imageNotFound          = pyqtSignal()
    enablePreviousImage    = pyqtSignal()
    enableNextImage        = pyqtSignal()
    disablePreviousImage   = pyqtSignal()
    disableNextImage       = pyqtSignal()

    ## Constructor
    def __init__(self):
        """ __init__

        ImageController constructor. It set an initial state
        for handling image visualization and instantiate
        observables to manage the image path and its exif data. 
        """
        super().__init__()

        # State variables
        self._imageIndex = 0
        self._imageCount = 0
        self._images = []
        self._cachedExifData = {}

        # Setting the observables, these will be 
        # the image path of the actual image
        # and its exif data
        self._observableExifData = ObservableExifData()
        self._observablePath = ObservableImagePath()

        # Connecting observable signals
        self._observableExifData.observe(self._onExifDataCallback)
        self._observablePath.observe(self._onImageCallback)


    ## Public Getter
    def getImagePath(self):
        return self._observablePath.imagePath


    ## Public Getter
    def getExifData(self):
        return self._observableExifData.exif


    ## Method to reset the state of the handler
    def _resetState(self):
        self._images.clear()
        self._imageCount = 0 
        self._imageIndex = 0


    ## Callback called whenever the exif data are updated
    def _onExifDataCallback(self, data):
        """ _onExifDataCallback
        
        This callback is called whenever exif data are updated.
        ObservableExifData object will emit its signal whenever its
        field is updated
        """
        
        self._cachedExifData[self.getImagePath()] = data
        self.exifDataReady.emit()


    ## Callback called whenever the image path is updated
    def _onImageCallback(self, path):
        """ _onImageCallback
        
        This callback is called whenever ObservableImagePath
        object' field is updated.
        This method will evaluates exif data of the new image
        and will set the ObservableExifData field.
        """

        print("Displayed image: " + path)

        # Path has been set. Tell the controller
        # to show the image and image name
        self.imageFound.emit()

        # Extract exif data
        if path in self._cachedExifData:
            # Avoid to extract exif data if already
            # extracted
            tmpExif = self._cachedExifData[path]
        else:
            tmpExif = self._getExifData(path)

        self._observableExifData.exif = tmpExif


    ## Extract exif data from displayed image
    def _getExifData(self, imagePath):
        """ _getExifData

        Method used to extract exif data from image
        stored at imagePath. Returns exifData (list)
        """

        # Open image file for reading
        f = open(imagePath, 'rb')

        # Process file to get Exif data
        tags = exifread.process_file(f)
        #print(tags)

        exifData = {}
        for tag in tags.keys():
            #if tag not in ('JPEGThumbnail', 'TIFFThumbnail', 'Filename', 'EXIF MakerNote'):
            if tag not in ('JPEGThumbnail'):
                exifData.update({tag : tags[tag]})

        return exifData


    ## Slot for image selected signal coming from qml FileSelector 
    def onImagePathUpdated(self, path):
        """ onImagePathUpdated

        Callback to be connected to qml signal for 
        receiving events coming from a single image selection.
        It will instruct how to handle GUI button and
        update ObservableImagePath.
        """

        print("Selected image: " + path)
        self._resetState()

        if '.jpg' in path:
            # Selected an image
            self._imageCount = 1
            self._images.append(path)

            # Disable next and previous buttons
            self.disableNextImage.emit()
            self.disablePreviousImage.emit()

            # Update observable
            self._observablePath.imagePath = self._images[0]
        else:
            print('File format not supported')


    ## Slot for folder selected signal coming from qml FileSelector 
    def onFolderPathUpdated(self, path):
        """ onFolderPathUpdated

        Callback to be connected to qml signal for 
        receiving events coming from a folder selection.
        It will instruct how to handle GUI button and
        update ObservableImagePath with the first image
        of the folder (if exists).
        """

        print("Selected folder: " + path)
        self._resetState()

        fileList = os.listdir(path)
        for file in fileList:
            if '.jpg' in file:
                self._images.append(path + '/' + file)
                self._imageCount += 1
        
        if self._imageCount != 0:
            # Manage buttons
            if self._imageCount == 1:
                self.disablePreviousImage.emit()
                self.disableNextImage.emit()
            else:
                self.disablePreviousImage.emit()
                self.enableNextImage.emit()
            
            # Update observable
            #print(self._images[0])
            self._observablePath.imagePath = self._images[0]
        else:
            # No image found in folder
            self.imageNotFound.emit()


    ## Slot for handling user request to view the previous
    # image of a folder 
    def onPreviousImageRequested(self):
        """ onPreviousImageRequested

        Callback to be connected to qml signal for 
        receiving events coming from a previous image request.
        It will instruct how to handle GUI button and
        update ObservableImagePath with the previous image
        of the folder (if exists).
        """

        if self._imageIndex == 0:
            return

        self._imageIndex -= 1
        self._observablePath.imagePath = self._images[self._imageIndex]
        if self._imageIndex == 0:
            self.disablePreviousImage.emit()
        
        if self._imageCount > 1:
            self.enableNextImage.emit()


    ## Slot for handling user request to view the next
    # image of a folder
    def onNextImageRequested(self):
        """ onNextImageRequested

        Callback to be connected to qml signal for 
        receiving events coming from a next image request.
        It will instruct how to handle GUI button and
        update ObservableImagePath with the next image
        of the folder (if exists).
        """

        if self._imageIndex == self._imageCount - 1:
            return

        self._imageIndex += 1
        self._observablePath.imagePath = self._images[self._imageIndex]
        if self._imageIndex >= self._imageCount - 1:
            self.disableNextImage.emit()
            
        if self._imageIndex == 1 and self._imageCount > 1:
            self.enablePreviousImage.emit()
