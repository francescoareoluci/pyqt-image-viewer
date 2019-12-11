import os
import exifread
from PyQt5.QtCore import QObject, pyqtSignal
from ExifDataObservable import ObservableExifData
from ImagePathObservable import ObservableImagePath


class ImageHandler(QObject):

    exifDataReady = pyqtSignal()

    def __init__(self):
        super().__init__()

        ## Setting the observables, these will be 
        ## the image path of the actual image
        ## and the relative exif data
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


    ## Extract exif data from image
    def _getExifData(self, imagePath):

        ## Open image file for reading
        f = open(imagePath, 'rb')

        ## Process file to get Exif data
        tags = exifread.process_file(f)
        print(tags)

        exifData = {}
        for tag in tags.keys():
            #if tag not in ('JPEGThumbnail', 'TIFFThumbnail', 'Filename', 'EXIF MakerNote'):
            if tag not in ('JPEGThumbnail'):
                exifData.update({tag : tags[tag]})

        return exifData


    ## Slot for signal coming from qml FileSelector 
    def onImagePathUpdated(self, path):
        
        ## If the path is valid update the observable
        if os.path.isfile(path):
            ## Update observable
            self._observablePath.imagePath = path


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