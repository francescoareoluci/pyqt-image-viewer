from PyQt5.QtWidgets import QApplication
from PyQt5.QtQml import qmlRegisterType, QQmlComponent, QQmlEngine, QQmlApplicationEngine
from PyQt5.QtCore import QUrl, QObject, pyqtSignal, pyqtSlot, pyqtProperty, QCoreApplication
from PyQt5.QtQuick import QQuickView
from ImageHandler import ImageHandler

if __name__ == '__main__':

    ## Create a QApplication.
    app = QApplication([])
    engine = QQmlApplicationEngine(QUrl('./qml/main_window.qml'))

    imageHandler = ImageHandler()

    imageHandler.onImagePathUpdated('/home/francesco/Pictures/test2.jpg')
    imageHandler.onImagePathUpdated('/home/francesco/Pictures/test.jpeg')
    imageHandler.onImagePathUpdated('/home/francesco/Pictures/test3.jpg')

    ## Start the application
    app.exec_()