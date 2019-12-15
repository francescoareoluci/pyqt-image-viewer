import QtQuick 2.0
import QtQuick.Dialogs 1.0

FileDialog {
    visible: false
    title: "Please select a folder"
    folder: shortcuts.home
    selectFolder: true
    
    onRejected: {
        console.log("File not selected")
    }
}