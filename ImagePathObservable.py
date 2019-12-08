from PyQt5.QtCore import QObject, pyqtSignal

## This observable is used to update the image
## path
class ObservableImagePath(QObject):

    valueChanged = pyqtSignal(object)

    def __init__(self):
        super().__init__()
        self._imagePath = ''
        
    def observe(self, slot):
        self.valueChanged.connect(slot)

    @property
    def imagePath(self):
        return self._imagePath

    @imagePath.setter
    def imagePath(self, newValue):
        self._imagePath = newValue
        self.valueChanged.emit(self.imagePath)