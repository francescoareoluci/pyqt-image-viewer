from PyQt5.QtWidgets import QApplication
from PyQt5.QtQml import qmlRegisterType, QQmlListProperty, QQmlComponent, QQmlEngine, QQmlApplicationEngine
from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot, pyqtProperty, QCoreApplication
from PyQt5.QtQuick import QQuickView
from ImageHandler import ImageHandler
from ExifViewHandler import ExifViewHandler, ExifEntry
from ImageViewHandler import ImageViewHandler


## Callback to manage the exif data availability.
## This will update ExifViewHandler, that will
## signal the qml to update the list model
def onExifDataReady():
    data = imageHandler.getExifData()

    exif = []
    for key in data:
        exifEntry = ExifEntry()
        exifEntry.name = str(key)
        exifEntry.value = str(data[key])
        exif.append(exifEntry)

    #for d in exif:
    #    print(d.name)
    #    print(d.value)

    exifViewHandler.exif = exif

    ## Show or hide the exif button on the GUI
    exifViewHandler.handleGuiButton(exifButton)


if __name__ == '__main__':

    ## Create a QApplication.
    app = QApplication([])

    exifViewHandler = ExifViewHandler()
    imageHandler = ImageHandler()

    qmlRegisterType(ExifViewHandler, 'Example', 1, 0, 'ExifViewHandler')

    engine = QQmlApplicationEngine()
    engine.rootContext().setContextProperty('exifViewHandler', exifViewHandler)
    engine.load('./qml/main_window.qml')

    ## Get the root window and fish out the buttons.
    win = engine.rootObjects()[0]

    imageViewHandler = ImageViewHandler(engine, imageHandler)

    folderSelector      = win.findChild(QObject, 'folderFileDialog')
    imageSelector       = win.findChild(QObject, 'imageFileDialog')
    exifButton          = win.findChild(QObject, 'exifButton')
    previousButton      = win.findChild(QObject, 'skipBackward')
    nextButton          = win.findChild(QObject, 'skipForward')

    ## Connecting qml signals to our ImageHandler slots
    folderSelector.folderSelected.connect(imageHandler.onFolderPathUpdated)
    imageSelector.imageSelected.connect(imageHandler.onImagePathUpdated)
    previousButton.previousButtonPressed.connect(imageHandler.onPreviousImageRequested)
    nextButton.nextButtonPressed.connect(imageHandler.onNextImageRequested)

    ## Connecting ImageHandler signals to our slots
    imageHandler.exifDataReady.connect(onExifDataReady)
    imageHandler.imageFound.connect(imageViewHandler.imageFoundHandler)
    imageHandler.imageNotFound.connect(imageViewHandler.imageNotFoundHandler)
    imageHandler.disablePreviousImage.connect(imageViewHandler.disablePreviousImageHandler)
    imageHandler.enablePreviousImage.connect(imageViewHandler.enablePreviousImageHandler)
    imageHandler.disableNextImage.connect(imageViewHandler.disableNextImageHandler)
    imageHandler.enableNextImage.connect(imageViewHandler.enableNextImageHandler)

    ## Start the application
    app.exec_()