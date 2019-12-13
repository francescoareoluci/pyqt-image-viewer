import QtQuick 2.0
import QtQuick.Dialogs 1.0

FileDialog {
    visible: false
    title: "Please choose a jpg image"
    folder: shortcuts.home
    //nameFilters: [ "Image files (*.jpg)" ]
    selectFolder: true
    
    onRejected: {
        console.log("File not selected")
    }
}