import os
import re
import exifread
from PyQt5.QtCore import QObject, pyqtSignal
from ExifDataObservable import ObservableExifData
from ImagePathObservable import ObservableImagePath


class ImageHandler(QObject):

    exifDataReady           = pyqtSignal()
    enablePreviousButton    = pyqtSignal()
    enableNextButton        = pyqtSignal()
    disablePreviousButton   = pyqtSignal()
    disableNextButton       = pyqtSignal()
    imageNotFound           = pyqtSignal()

    def __init__(self):
        super().__init__()

        ## State variables
        self._imageIndex = 0
        self._imageCount = 0
        self._images = []

        ## Setting the observables, these will be 
        ## the image path of the actual image
        ## and its exif data
        self._observableExifData = ObservableExifData()
        self._observablePath = ObservableImagePath()

        ## Connecting observable signals
        self._observableExifData.observe(self._onExifDataCallback)
        self._observablePath.observe(self._onImageCallback)


    ## Public Getter
    def getImagePath(self):
        return self._observablePath.imagePath


    ## Public Getter
    def getExifData(self):
        return self._observableExifData.exif


    def resetState(self):
        self._images.clear()
        self._imageCount = 0 
        self._imageIndex = 0


    ## Extract exif data from displayed image
    def _getExifData(self, imagePath):

        ## Open image file for reading
        f = open(imagePath, 'rb')

        ## Process file to get Exif data
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
        print(path)
        self.resetState()

        if '.jpg' in path:
            ## Selected an image
            self._imageCount = 1
            self._images.append(path)

            ## Disable next and previous buttons
            self.disableNextButton.emit()
            self.disablePreviousButton.emit()

            ## Update observable
            self._observablePath.imagePath = self._images[0]
        else:
            print('Format file not supported')


    ## Slot for folder selected signal coming from qml FileSelector 
    def onFolderPathUpdated(self, path):
        print(path)
        self.resetState()

        fileList = os.listdir(path)
        for file in fileList:
            if '.jpg' in file:
                self._images.append(path + '/' + file)
                self._imageCount += 1
        
        ## Manage buttons
        if self._imageCount != 0:
            if self._imageCount == 1:
                self.disablePreviousButton.emit()
                self.disableNextButton.emit()
            else:
                self.disablePreviousButton.emit()
                self.enableNextButton.emit()
            
            ## Update observable
            print(self._images[0])
            self._observablePath.imagePath = self._images[0]
        else:
            self.imageNotFound.emit()


    def onPreviousButtonClicked(self):
        if self._imageIndex == 0:
            return

        self._imageIndex -= 1
        self._observablePath.imagePath = self._images[self._imageIndex]
        if self._imageIndex == 0:
            self.disablePreviousButton.emit()
        else:
            self.enableNextButton.emit()

    def onNextButtonClicked(self):
        if self._imageIndex == self._imageCount - 1:
            return

        self._imageIndex += 1
        self._observablePath.imagePath = self._images[self._imageIndex]
        if self._imageIndex >= self._imageCount - 1:
            self.disableNextButton.emit()
            
        if self._imageIndex == 1 and self._imageCount != 1:
            self.enablePreviousButton.emit()

    ## Callback called whenever the exif data are updated
    def _onExifDataCallback(self, data):
        
        ## TODO: To be removed, otherwise
        ## list model will not be updated if selected
        ## image not contains exif data
        #if not data:
        #    ## Data dict is empty
        #    print('Empty exif values')
        #    return

        self.exifDataReady.emit()


    ## Callback called whenever the image path is updated
    def _onImageCallback(self, path):
        
        print(path)
        tmpExif = self._getExifData(path)
        self._observableExifData.exif = tmpExif