import QtQuick 2.0
import QtQuick.Controls 2.0
import QtQuick.Layouts 1.3
import QtQuick.Controls.Material 2.0
import QtQuick.Dialogs 1.0

ApplicationWindow {
    id: window
    width: 800; height: 600
    minimumWidth: 480
    minimumHeight: 360
    visible: true; title: "Image Viewer"
	Material.theme: Material.Dark
    color: "#f7f7f7"

    ColumnLayout {
        // Setting the size and position of the main layout
        width: { parent.width - 60 }
        height: { parent.height - 60 } 
        anchors.centerIn: parent

        RowLayout {

		    // Define the spacing between the elements of the
		    // column layout
		    spacing: 100
            id: firstRow

            Button {
                id: dialogButton
                text: "Choose an image"
                padding: 10
                onClicked: {
                    fileDialog.visible = true
                }
                Layout.fillWidth: true; Layout.fillHeight: true

                // Add a background rectangle to set border radius
                background: Rectangle {
                    radius: 5
                    color: "#D2D5DD"
                    border.color: "gray"
				    border.width: 1
                }
            }

		    Button {
                id: exifButton
                text: "View EXIF data"
                enabled: false
                Layout.fillWidth: true; Layout.fillHeight: true
                padding: 10
                background: Rectangle {
                    radius: 5
                    color: "#D2D5DD"
                    border.color: "gray"
				    border.width: 1
                }
            }

            FileDialog {
                visible: false
                id: fileDialog
                title: "Please choose a file"
                folder: shortcuts.home
                onAccepted: {
                    console.log("You chose: " + fileDialog.fileUrls)
                    displayedImage.source = fileDialog.fileUrl
                    exifButton.enabled = true
                    skipForward.enabled = true
                    skipBackward.enabled = true
                    rotateLeft.enabled = true
                    rotateRight.enabled = true
                    fileNameLabel.visible = true
                    fileNameLabel.text = "Image name: " + fileDialog.fileUrl
                }
                onRejected: {
                    console.log("Canceled")
                }
            }
        }

        Image {
            id: displayedImage
            property var rotationAngle: 0
            source: "../assets/default_image.png"
            fillMode: Image.PreserveAspectFit
            Layout.fillWidth: true; Layout.fillHeight: true
            //anchors.fill: parent
            anchors.centerIn: parent
            transform: Rotation { origin.x: displayedImage.width / 2; origin.y: displayedImage.height / 2; angle: displayedImage.rotationAngle}
        }

        Label {
            id: fileNameLabel
            Layout.fillWidth: true; Layout.fillHeight: true
            text: ""
            visible: false
            padding: 0, 15, 0, 15
            color: "#066c9c"
        }
    		
        RowLayout {
			spacing: 30
            id: lastRow

            Button {
                id: skipForward
                text: "Next Image"
                enabled: false
                Layout.fillWidth: true; Layout.fillHeight: true
                padding: 10
                background: Rectangle {
                    radius: 5
                    color: "#D2D5DD"
                    border.color: "gray"
				    border.width: 1
                }
            }

            Button {
                id: skipBackward
                text: "Previous Image"
                enabled: false
                Layout.fillWidth: true; Layout.fillHeight: true
                padding: 10
                background: Rectangle {
                    radius: 5
                    color: "#D2D5DD"
                    border.color: "gray"
				    border.width: 1
                }
            }

            Button {
                id: rotateLeft
                padding: 10
                text: "Rotate Left"
                enabled: false
                Layout.fillWidth: true; Layout.fillHeight: true
                property var rotated: 0
                onClicked: {
                    if (rotated == 0) {
                        displayedImage.width = displayedImage.height
                        rotated = 1
                    }
                    else {
                        displayedImage.width = parent.width
                        rotated = 0
                    }
                    displayedImage.rotationAngle = displayedImage.rotationAngle - 90
                }
                background: Rectangle {
                    radius: 5
                    color: "#D2D5DD"
                    border.color: "gray"
				    border.width: 1
                }
            }

            Button {
                id: rotateRight
                padding: 10
                text: "Rotate Right"
                enabled: false
                Layout.fillWidth: true; Layout.fillHeight: true
                property var rotated: 0
                onClicked: {
                    if (rotated == 0 ) {
                        displayedImage.width = displayedImage.height
                        rotated = 1
                    }
                    else {
                        displayedImage.width = parent.width
                        rotated = 0
                    }
                    displayedImage.rotationAngle = displayedImage.rotationAngle + 90
                }
                background: Rectangle {
                    radius: 5
                    color: "#D2D5DD"
                    border.color: "gray"
				    border.width: 1
                }
            }
		}
    }
}