from PyQt5.QtCore import QObject, pyqtSignal

## This observable is used
## to update the exif values
class ObservableExifData(QObject):
    
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