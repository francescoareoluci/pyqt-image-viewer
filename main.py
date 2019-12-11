from PyQt5.QtWidgets import QApplication
from PyQt5.QtQml import qmlRegisterType, QQmlListProperty, QQmlComponent, QQmlEngine, QQmlApplicationEngine
from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot, pyqtProperty, QCoreApplication
from PyQt5.QtQuick import QQuickView
from ImageHandler import ImageHandler
from ExifViewHandler import ExifViewHandler, ExifEntry


## Callback to manage the exif data availability.
## This will update ExifViewHandler, that will
## signal the qml to update the list model
def onExifDataReady():
    data = imageHandler.getExifData()
    path = imageHandler.getImagePath()

    exif = []
    for key in data:
        exifEntry = ExifEntry()
        exifEntry.name = str(key)
        exifEntry.value = str(data[key])
        exif.append(exifEntry)

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