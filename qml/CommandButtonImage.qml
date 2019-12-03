import QtQuick 2.0
import QtQuick.Controls 2.0

Image {
    fillMode: Image.PreserveAspectFit
    scale: Qt.KeepAspectRatio

    anchors.right: parent.right
    anchors.left: parent.left
    anchors.top: parent.top
    anchors.bottom: parent.bottom
}