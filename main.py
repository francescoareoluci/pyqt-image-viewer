from PyQt5.QtQml import qmlRegisterType, QQmlComponent, QQmlEngine, QQmlApplicationEngine
from PyQt5.QtCore import QUrl, QObject, pyqtSignal, pyqtSlot, pyqtProperty, QCoreApplication
from PyQt5.QtQuick import QQuickView
import exifread


## This observable value is used
## to update the exif values
class ObservableCalcValue(QObject):
    
    valueChanged = pyqtSignal(object)
    
    def __init__(self):
        super().__init__()
        self._exifData = {}
        
    def observe(self, slot):
        self.valueChanged.connect(slot)

    @property
    def exif(self):
        return self._exifData

    @exif.setter
    def exif(self, newValues):
        self._exifData = newValues
        self.valueChanged.emit(self.exif)


def onChangeCallback(data):
    print(data)
    for k in data.keys():
        print(k, data[k])


if __name__ == '__main__':

    observable = ObservableCalcValue()
    observable.valueChanged.connect(onChangeCallback)
    
    # Open image file for reading (binary mode)
    f = open('/home/francesco/Pictures/test2.jpg', 'rb')

    # Return Exif tags
    tags = exifread.process_file(f)

    tmpExif = {}
    for tag in tags.keys():
        if tag not in ('JPEGThumbnail', 'TIFFThumbnail', 'Filename', 'EXIF MakerNote'):
            #print("Key: %s, value %s" % (tag, tags[tag]))
            tmpExif.update({tag : tags[tag]})

    observable.exif = tmpExif