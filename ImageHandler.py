import os
from ExifDataObservable import ObservableExifData
from ImagePathObservable import ObservableImagePath
import exifread


class ImageHandler:

    def __init__(self):
        ## Setting the observables, these will be 
        ## the image path of the actual image
        ## and the relative exif data
        self._observableExifData = ObservableExifData()
        self._observablePath = ObservableImagePath()

        ## Connecting observable signals
        self._observableExifData.observe(self.onExifDataCallback)
        self._observablePath.observe(self.onImageCallback)


    ## Extract exif data from image
    def getExifData(self, imagePath):

        ## Open image file for reading
        f = open(imagePath, 'rb')

        ## Return Exif tags
        tags = exifread.process_file(f)

        exifData = {}
        for tag in tags.keys():
            if tag not in ('JPEGThumbnail', 'TIFFThumbnail', 'Filename', 'EXIF MakerNote'):
                exifData.update({tag : tags[tag]})

        return exifData


    ## Slot for signal coming from qml FileSelector 
    def onImagePathUpdated(self, path):

        ## If the path is valid update the observable
        if os.path.isfile(path):
            ## Update observable
            self._observablePath.imagePath = path


    ## Callback called whenever the exif data are updated
    def onExifDataCallback(self, data):
        
        if not data:
            ## Data dict is empty
            print('Empty exif values')
            return

        for k in data.keys():
            print(k, data[k])


    ## Callback called whenever the image path is updated
    def onImageCallback(self, path):
        
        print(path)
        tmpExif = self.getExifData(path)
        self._observableExifData.exif = tmpExif