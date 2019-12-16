""" Observables module
Author: Francesco Areoluci

This module contains classes to be used as observable objects.
"""
from PyQt5.QtCore import QObject, pyqtSignal


## This observable is used
# to update the exif values
class ObservableExifData(QObject):
    """ Class used as an observable to monitor changes
    to exif data to be visualized in GUI. Each time exif
    data are modified, the signal valueChanged will be fired.

    Typical usage example:
    obsExifData = ObservableExifData()
    obsExifData.observe(someSlot)
    obsExifData.exif = newExif
    """
    
    valueChanged = pyqtSignal(object)
    
    def __init__(self):
        super().__init__()
        self._exifData = {}
        
    def observe(self, slot):
        self.valueChanged.connect(slot)

    @property
    def exif(self):
        return self._exifData

    @exif.setter
    def exif(self, newValues):
        self._exifData = newValues
        self.valueChanged.emit(self.exif)


## This observable is used to update the 
# image path
class ObservableImagePath(QObject):
    """ Class used as an observable to monitor changes
    to image path to be visualized in GUI. Each time image
    path is modified, the signal valueChanged will be fired.

    Typical usage example:
    obsImagePath = ObservableImagePath()
    obsImagePath.observe(someSlot)
    obsImagePath.imagePath = newImagePath
    """

    valueChanged = pyqtSignal(object)

    def __init__(self):
        super().__init__()
        self._imagePath = ''
        
    def observe(self, slot):
        self.valueChanged.connect(slot)

    @property
    def imagePath(self):
        return self._imagePath

    @imagePath.setter
    def imagePath(self, newValue):
        self._imagePath = newValue
        self.valueChanged.emit(self.imagePath)