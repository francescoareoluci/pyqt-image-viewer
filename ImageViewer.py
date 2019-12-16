""" ImageViewer.py
Author: Francesco Areoluci

Main python module
This module is the entry point of the application.
It will instantiates the QApplication, connect some signals
and launch the application.
"""

from PyQt5.QtWidgets import QApplication
from PyQt5.QtQml import qmlRegisterType, QQmlListProperty, QQmlComponent, QQmlEngine, QQmlApplicationEngine
from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot, pyqtProperty, QCoreApplication
from PyQt5.QtQuick import QQuickView
from ImageHandler import ImageHandler
from ExifViewHandler import ExifViewHandler, ExifEntry
from ImageViewHandler import ImageViewHandler


if __name__ == '__main__':

    # Create a QApplication.
    app = QApplication([])

    imageHandler = ImageHandler()
    exifViewHandler = ExifViewHandler(imageHandler)

    qmlRegisterType(ExifViewHandler, 'Example', 1, 0, 'ExifViewHandler')

    engine = QQmlApplicationEngine()
    engine.rootContext().setContextProperty('exifViewHandler', exifViewHandler)
    engine.load('./qml/main_window.qml')
    
    # Get the root window
    win = engine.rootObjects()[0]

    # Get GUI elements
    folderSelector      = win.findChild(QObject, 'folderFileDialog')
    imageSelector       = win.findChild(QObject, 'imageFileDialog')
    exifButton          = win.findChild(QObject, 'exifButton')
    previousButton      = win.findChild(QObject, 'skipBackward')
    nextButton          = win.findChild(QObject, 'skipForward')

    # Create the image view handler
    imageViewHandler = ImageViewHandler(win, imageHandler)
    # Set the exif button to be handled in exif view handler
    exifViewHandler.setExifButton(exifButton)

    # Connecting qml signals to ImageHandler slots
    folderSelector.folderSelected.connect(imageHandler.onFolderPathUpdated)
    imageSelector.imageSelected.connect(imageHandler.onImagePathUpdated)
    previousButton.previousButtonPressed.connect(imageHandler.onPreviousImageRequested)
    nextButton.nextButtonPressed.connect(imageHandler.onNextImageRequested)

    # Connecting ImageHandler signals to our slots
    imageHandler.exifDataReady.connect(exifViewHandler.onExifDataReady)
    imageHandler.imageFound.connect(imageViewHandler.imageFoundHandler)
    imageHandler.imageNotFound.connect(imageViewHandler.imageNotFoundHandler)
    imageHandler.disablePreviousImage.connect(imageViewHandler.disablePreviousImageHandler)
    imageHandler.enablePreviousImage.connect(imageViewHandler.enablePreviousImageHandler)
    imageHandler.disableNextImage.connect(imageViewHandler.disableNextImageHandler)
    imageHandler.enableNextImage.connect(imageViewHandler.enableNextImageHandler)

    # Start the application
    app.exec_()