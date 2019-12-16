""" ExifViewHandler module
Author: Francesco Areoluci

This module contains classes to handle the GUI view
regarding exif data visualization
"""
from PyQt5.QtCore import QObject, pyqtSignal, pyqtProperty
from PyQt5.QtQml import QQmlListProperty


## This class is used to store a single Exif entry
# of the viewed image. This is used to populate the
# qml list model
class ExifEntry(QObject):

    nameChanged = pyqtSignal()
    valueChanged = pyqtSignal()
    isGeoTagChanged = pyqtSignal()
    latitudeChanged = pyqtSignal()
    longitudeChanged = pyqtSignal()

    def __init__(self, name='', *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._name = ""
        self._value = ""
        self._isGeoTag = False
        self._latitude = 0
        self._longitude = 0

    @pyqtProperty('QString', notify=nameChanged)
    def name(self):
        return self._name

    @name.setter
    def name(self, newName):
        if newName != self._name:
            self._name = newName

    @pyqtProperty('QString', notify=valueChanged)
    def value(self):
        return self._value

    @value.setter
    def value(self, newValue):
        if newValue != self._value:
            self._value = newValue

    @pyqtProperty('bool', notify=isGeoTagChanged)
    def isGeoTag(self):
        return self._isGeoTag

    @isGeoTag.setter
    def isGeoTag(self, isGeoTag):
        if isGeoTag != self._isGeoTag:
            self._isGeoTag = isGeoTag

    @pyqtProperty('float', notify=latitudeChanged)
    def latitude(self):
        return self._latitude

    @latitude.setter
    def latitude(self, newLat):
        if newLat != self._latitude:
            self._latitude = newLat

    @pyqtProperty('float', notify=longitudeChanged)
    def longitude(self):
        return self._longitude

    @longitude.setter
    def longitude(self, newLon):
        if newLon != self._longitude:
            self._longitude = newLon


## This class will contain the list of Exif data
# read from viewed image. This list will be used to 
# populate the qml list model
class ExifViewHandler(QObject):

    exifChanged = pyqtSignal()

    def __init__(self, imageController):
        super().__init__()

        self._exif = []
        self._imageController = imageController


    @pyqtProperty(QQmlListProperty, notify=exifChanged)
    def exif(self):
        return QQmlListProperty(ExifEntry, self, self._exif)


    @exif.setter
    def exif(self, newExif):
        if newExif != self._exif:
            self._exif = newExif
            self.exifChanged.emit()


    def setExifButton(self, exifButton):
        self._exifButton = exifButton
        

    def handleGuiButton(self, button):
        if self._exif:
            button.setProperty("enabled", 'true')
            button.setProperty("visible", 'true')
        else:
            button.setProperty("enabled", 'false')
            button.setProperty("visible", 'false')


    def getDecimalCoords(self, coords):
        decimal = coords[0].num + (coords[1].num / 60)
        numSeconds = coords[2].num
        denSeconds = coords[2].den
        if denSeconds != 0:
            seconds = numSeconds / denSeconds
        else:
            seconds = numSeconds
        decimal += (seconds / 3600)
        return decimal


    def onExifDataReady(self):
        data = self._imageController.getExifData()

        exif = []
        for key in data:
            exifEntry = ExifEntry()
            isGeoTag = False
            if 'GPSLongitude' in key or 'GPSLatitude' in key:
                isGeoTag = True
            if key == 'GPS GPSLatitude':
                degLatitude = data[key].values
                exifEntry.latitude = self.getDecimalCoords(degLatitude)
            elif key == 'GPS GPSLongitude':
                degLongitude = data[key].values
                exifEntry.longitude = self.getDecimalCoords(degLongitude)

            exifEntry.name = str(key)
            exifEntry.value = str(data[key])
            exifEntry.isGeoTag = isGeoTag
            exif.append(exifEntry)

        #for d in exif:
        #    print(d.name)
        #    print(d.value)

        self.exif = exif

        # Show or hide the exif button on the GUI
        self.handleGuiButton(self._exifButton)