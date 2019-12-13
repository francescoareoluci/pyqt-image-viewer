import os
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

    #for d in exif:
    #    print(d.name)
    #    print(d.value)

    exifViewHandler.exif = exif

    ## Show or hide the exif button on the GUI
    exifViewHandler.handleGuiButton(exifButton)
    displayedImage.setProperty('source', 'file://' + path)
    fileNameLabel.setProperty('text', '<b>Image path:</b>: ' + path)


## Some view handlers... TODO: move these in proper class
def enableNextButtonHandler():
    nextButton.setProperty('enabled', 'true')
    nextButtonRect.setProperty('color', '#8fbccc')
    nextButtonImage.setProperty('source', 'file://' + pwd + '/assets/skip_forward.png')


def disableNextButtonHandler():
    nextButton.setProperty('enabled', 'false')
    nextButtonRect.setProperty('color', '#c9bfbf')
    nextButtonImage.setProperty('source', 'file://' + pwd + '/assets/skip_forward_disabled.png')


def enablePreviousButtonHandler():
    previousButton.setProperty('enabled', 'true')
    previousButtonRect.setProperty('color', '#8fbccc')
    previousButtonImage.setProperty('source', 'file://' + pwd + '/assets/skip_backward.png')


def disablePreviousButtonHandler():
    previousButton.setProperty('enabled', 'false')
    previousButtonRect.setProperty('color', '#c9bfbf')
    previousButtonImage.setProperty('source', 'file://' + pwd + '/assets/skip_backward_disabled.png')


def imageNotFoundHandler():
    ## TODO: update label to print out 
    ## 'no image found'
    print('No image in folder')


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

    folderSelector      = win.findChild(QObject, 'folderFileDialog')
    imageSelector       = win.findChild(QObject, 'imageFileDialog')
    exifButton          = win.findChild(QObject, 'exifButton')
    displayedImage      = win.findChild(QObject, 'displayedImage')
    previousButton      = win.findChild(QObject, 'skipBackward')
    nextButton          = win.findChild(QObject, 'skipForward')
    previousButtonRect  = win.findChild(QObject, 'skipBackwardRect')
    nextButtonRect      = win.findChild(QObject, 'skipForwardRect')
    previousButtonImage = win.findChild(QObject, 'skipBackwardImage')
    nextButtonImage     = win.findChild(QObject, 'skipForwardImage')
    fileNameLabel       = win.findChild(QObject, 'fileNameLabel')

    ## Connecting qml signals to our ImageHandler slots
    folderSelector.folderSelected.connect(imageHandler.onFolderPathUpdated)
    imageSelector.imageSelected.connect(imageHandler.onImagePathUpdated)
    previousButton.previousButtonPressed.connect(imageHandler.onPreviousButtonClicked)
    nextButton.nextButtonPressed.connect(imageHandler.onNextButtonClicked)

    ## Connecting ImageHandler signals to our slots
    imageHandler.exifDataReady.connect(onExifDataReady)
    imageHandler.disablePreviousButton.connect(disablePreviousButtonHandler)
    imageHandler.enablePreviousButton.connect(enablePreviousButtonHandler)
    imageHandler.disableNextButton.connect(disableNextButtonHandler)
    imageHandler.enableNextButton.connect(enableNextButtonHandler)
    imageHandler.imageNotFound.connect(imageNotFoundHandler)

    pwd = os.getcwd()

    ## Start the application
    app.exec_()