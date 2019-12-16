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

    def __init__(self, name='', *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._name = ""
        self._value = ""

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


    def onExifDataReady(self):
        data = self._imageController.getExifData()

        exif = []
        for key in data:
            exifEntry = ExifEntry()
            exifEntry.name = str(key)
            exifEntry.value = str(data[key])
            exif.append(exifEntry)

        #for d in exif:
        #    print(d.name)
        #    print(d.value)

        self.exif = exif

        ## Show or hide the exif button on the GUI
        self.handleGuiButton(self._exifButton)