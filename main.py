from PyQt5.QtWidgets import QApplication
from PyQt5.QtQml import qmlRegisterType, QQmlListProperty, QQmlComponent, QQmlEngine, QQmlApplicationEngine
from PyQt5.QtCore import QUrl, QObject, pyqtSignal, pyqtSlot, pyqtProperty, QCoreApplication
from PyQt5.QtQuick import QQuickView
from ImageHandler import ImageHandler

class ExifData(QObject):

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

class ExifViewHandler(QObject):

    exifChanged = pyqtSignal()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self._exif = []

    @pyqtProperty(QQmlListProperty, notify=exifChanged)
    def exif(self):
        return QQmlListProperty(ExifData, self, self._exif)

    @exif.setter
    def exif(self, newExif):
        if newExif != self._exif:
            self._exif = newExif
            self.exifChanged.emit()



def onExifDataReady():
    data = imageHandler.getExifData()
    path = imageHandler.getImagePath()

    exif = []
    for key in data:
        ed = ExifData()
        ed.name = str(key)
        ed.value = str(data[key])
        exif.append(ed)

    for d in exif:
        print(d.name)
        print(d.value)

    exifViewHandler.exif = exif


if __name__ == '__main__':

    ## Create a QApplication.
    app = QApplication([])

    exifViewHandler = ExifViewHandler()
    imageHandler = ImageHandler()
    imageHandler.exifDataReady.connect(onExifDataReady)

    qmlRegisterType(ExifViewHandler, 'Example', 1, 0, 'ExifViewHandler')

    engine = QQmlApplicationEngine()
    engine.rootContext().setContextProperty('exifViewHandler', exifViewHandler)
    engine.load('./qml/main_window.qml')

    ## Get the root window and fish out the buttons.
    win = engine.rootObjects()[0]
    fileSelector = win.findChild(QObject, 'fileDialog')

    ## Connecting qml signals to our slots
    fileSelector.imageSelected.connect(imageHandler.onImagePathUpdated)

    ## Start the application
    app.exec_()