""" ImageViewer.py
Author: Francesco Areoluci

Main python module
This module is the entry point of the application.
It will instantiates the QApplication, connect some signals
and launch the application.
"""
from PyQt5.QtWidgets import QApplication
from PyQt5.QtQml import qmlRegisterType, QQmlComponent, QQmlEngine, QQmlApplicationEngine
from PyQt5.QtCore import QObject
from PyQt5.QtGui import QIcon
from ImageController import ImageController
from ExifViewHandler import ExifViewHandler, ExifEntry
from ImageViewHandler import ImageViewHandler


if __name__ == '__main__':

    # Create a QApplication.
    app = QApplication([])

    imageController = ImageController()
    exifViewHandler = ExifViewHandler(imageController)

    qmlRegisterType(ExifViewHandler, 'ExifViewHandler', 1, 0, 'ExifViewHandler')

    engine = QQmlApplicationEngine()
    engine.rootContext().setContextProperty('exifViewHandler', exifViewHandler)
    
    engine.load('./qml/ImageViewerWindow.qml')

    # Get the root window
    win = engine.rootObjects()[0]

    # Get GUI elements
    folderSelector      = win.findChild(QObject, 'folderFileDialog')
    imageSelector       = win.findChild(QObject, 'imageFileDialog')
    exifButton          = win.findChild(QObject, 'exifButton')
    previousButton      = win.findChild(QObject, 'skipBackward')
    nextButton          = win.findChild(QObject, 'skipForward')

    # Create the image view handler
    imageViewHandler = ImageViewHandler(win, imageController)

    # Set the exif button to be handled in exif view handler
    exifViewHandler.setExifButton(exifButton)

    # Connecting qml signals to imageController slots
    folderSelector.folderSelected.connect(imageController.onFolderPathUpdated)
    imageSelector.imageSelected.connect(imageController.onImagePathUpdated)
    previousButton.previousButtonPressed.connect(imageController.onPreviousImageRequested)
    nextButton.nextButtonPressed.connect(imageController.onNextImageRequested)

    # Set application icon
    app.setWindowIcon(QIcon('./assets/logo.bmp'))

    # Start the application
    app.exec_()