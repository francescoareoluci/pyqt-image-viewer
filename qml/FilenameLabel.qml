import QtQuick 2.0
import QtQuick.Controls 2.0

Label {
    font.pointSize: 9
    font.family: webFont.name
    color: "#8fbccc"

    visible: false

    topPadding: 9
    bottomPadding: 9
    leftPadding: 30

    verticalAlignment: Text.AlignVCenter
    // This way we can handle multiline
    wrapMode: Label.WordWrap
    
    background: Rectangle {
        color: "white"
        width: mainWindow.width
    }
}