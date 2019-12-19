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
    """ Class representing an entry for the qml list view model

    Each entry will have the following fields:
    name: Exif tag name
    value: Exif tag value
    isGeoTag: Boolean, true for longitude and latitude entries (if exising. If true, a mouse area will be created on the entry
    latitude: Entry latitude. Each entry will have this, even if they are not gps tags...
    longitude: Entry longitude. Each entry will have this, even if they are not gps tags...

    For each field a getter and a setter is provided. Each field have a signal which is fired
    each time it is modified.
    """

    nameChanged = pyqtSignal()
    valueChanged = pyqtSignal()
    isGeoTagChanged = pyqtSignal()
    latitudeChanged = pyqtSignal()
    longitudeChanged = pyqtSignal()

    def __init__(self, name='', *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._name = ""         # Tag name
        self._value = ""        # Tag value
        self._isGeoTag = False  # Boolean, true for longitude and latitude entries (if exising)
                                # If true, a mouse area will be created on the entry

        self._latitude = 0      # Entry latitude. Each entry will have this, even if they are not gps tags...
        self._longitude = 0     # Entry longitude. Each entry will have this, even if they are not gps tags...


    ## name field getter
    @pyqtProperty('QString', notify=nameChanged)
    def name(self):
        return self._name


    ## name field setter
    @name.setter
    def name(self, newName):
        if newName != self._name:
            self._name = newName


    ## value field getter
    @pyqtProperty('QString', notify=valueChanged)
    def value(self):
        return self._value


    ## value field setter
    @value.setter
    def value(self, newValue):
        if newValue != self._value:
            self._value = newValue


    ## isGeoTag field getter
    @pyqtProperty('bool', notify=isGeoTagChanged)
    def isGeoTag(self):
        return self._isGeoTag


    ## isGeoTag field setter
    @isGeoTag.setter
    def isGeoTag(self, isGeoTag):
        if isGeoTag != self._isGeoTag:
            self._isGeoTag = isGeoTag


    ## latitude field getter
    @pyqtProperty('float', notify=latitudeChanged)
    def latitude(self):
        return self._latitude


    ## latitude field setter
    @latitude.setter
    def latitude(self, newLat):
        if newLat != self._latitude:
            self._latitude = newLat


    ## longitude field getter
    @pyqtProperty('float', notify=longitudeChanged)
    def longitude(self):
        return self._longitude


    ## longitude field setter
    @longitude.setter
    def longitude(self, newLon):
        if newLon != self._longitude:
            self._longitude = newLon


## This class will contain the list of Exif data
# read from viewed image. This list will be used to 
# populate the qml list model
class ExifViewHandler(QObject):
    """ Class representing the exif data for the qml list view model

    An instance of this class will contains a list of ExifEntry.
    A getter and setter for this list are provided, and signal will 
    be fired when the list is updated.

    Each time the exif data are updated from the controller, the list
    will be populated and, if existing, gps coordinates are evaluated.
    """

    exifChanged = pyqtSignal()

    def __init__(self, imageController):
        super().__init__()

        self._exif = []
        self._imageController = imageController

        # Connecting imageController signal to slot
        self._imageController.exifDataReady.connect(self.onExifDataReady)


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
        latitudeFound = False
        longitudeFound = False

        # Iterate through exif data
        for key in data:
            exifEntry = ExifEntry()
            isGeoTag = False

            # Store latitude and longitude, if tag is existing
            if key == 'GPS GPSLatitude':
                degLatitude = data[key].values
                latitude = self.getDecimalCoords(degLatitude)
                latitudeFound = True
            elif key == 'GPS GPSLongitude':
                degLongitude = data[key].values
                longitude = self.getDecimalCoords(degLongitude)
                longitudeFound = True

            # Store latitude and longitude reference, if tag is existing
            if key == 'GPS GPSLatitudeRef':
                latitudeRef = data[key].values
            elif key == 'GPS GPSLongitudeRef':
                longitudeRef = data[key].values

            exifEntry.name = str(key)
            exifEntry.value = str(data[key])
            exifEntry.isGeoTag = isGeoTag
            exif.append(exifEntry)

        # Iterate again through the list to set both
        # latitude and longitude to the entry
        if latitudeFound == True and longitudeFound == True:
            self.setEntryCoordinates(exif, latitude, longitude, latitudeRef, longitudeRef)

        self.exif = exif

        # Show or hide the exif button on the GUI
        self.handleGuiButton(self._exifButton)


    def setEntryCoordinates(self, exif, latitude, longitude, latitudeRef, longitudeRef):
        for entry in exif:
            if entry.name == 'GPS GPSLatitude' or entry.name == 'GPS GPSLongitude':
                if latitudeRef == 'N':
                    entry.latitude = latitude
                else:
                    entry.latitude = -latitude

                if longitudeRef == 'E':
                    entry.longitude = longitude
                else:
                    entry.longitude = -longitude

                entry.isGeoTag = True
