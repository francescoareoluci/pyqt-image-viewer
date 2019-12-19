import QtQuick 2.0
import QtQuick.Dialogs 1.0

FileDialog {
    visible: false
    title: "Please choose an image"
    folder: shortcuts.home
    nameFilters: [ "Image files (*.jpg *.jpeg *.png *.tiff)" ]
    
    onRejected: {
        console.log("File not selected")
    }
}