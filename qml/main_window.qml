import QtQuick 2.0
import QtQuick.Controls 2.0
import QtQuick.Layouts 1.3
import QtQuick.Controls.Material 2.0
import QtQuick.Dialogs 1.0
import QtQuick.Window 2.1

QtObject {

    property var controlWindow: ApplicationWindow {
        id: mainWindow
        width: 800; height: 600
        minimumWidth: 600
        minimumHeight: 400
        visible: true; title: "Image Viewer"
	    Material.theme: Material.Dark
        //color: "#f7f7f7"
        FontLoader { id: webFont; source: "../assets/Lato-Regular.ttf" }

        // Setting the mainWindow background image
        background: BorderImage { 
                horizontalTileMode: BorderImage.Repeat
                verticalTileMode: BorderImage.Repeat
                source: "../assets/silver_scales.png"
        }

        onClosing: {
            // Close any other existing windows
            exifWindow.visible = false
        }

        // This prevents the user to maximize the window
        // TODO: fixme
        flags: Qt.Dialog

        // Setting the header of main page,
        // which contains the title, the image
        // selection button and the exif data button
        header: Label {
            id: titleLabel
            text: "Image Viewer"
            font.family: webFont.name
            font.pointSize: 15
            topPadding: 15
            bottomPadding: 15
            leftPadding: 30
            color: "white"
            background: Rectangle {
                color: "#8fbccc"
                Layout.fillWidth: true; Layout.fillHeight: true
            }            

            RowLayout {
                anchors.right: parent.right
            
                Button {
                    id: exifButton
                    // TODO: how to set font color without this trick?
                    text: "<font color=\"#ffffff\"><u>View EXIF data</u></font>"
                    enabled: false
                    font.pointSize: 10
                    font.family: webFont.name
                    visible: false
                    padding: 10
                    width: 170
                    Layout.topMargin: 10
                    Layout.rightMargin: 5
                    // Add a background rectangle to set border radius
                    background: Rectangle {
                        radius: 5
                        color: "#8fbccc"
                    }
                    onClicked: {
                        exifWindow.visible = true
                    }
                }

                Button {
                    id: buttonImage
                    text: "<font color=\"#8fbccc\">Choose an image</font>"
                    padding: 10
                    width: 170
                    font.pointSize: 10
                    font.family: webFont.name
                    onClicked: {
                        fileDialog.visible = true
                    }
                    Layout.topMargin: 10
                    Layout.rightMargin: 30
                    // Add a background rectangle to set border radius
                    background: Rectangle {
                        radius: 5
                        color: "white"
                    }
                }

            }
        }

        // File dialog used to select an image
        // TODO: add jpg filter
        FileDialog {
            visible: false
            id: fileDialog
            title: "Please choose a file"
            folder: shortcuts.home
            nameFilters: [ "Image files (*.jpg)" ]
            onAccepted: {
                console.log("You chose: " + fileDialog.fileUrls)
                
                // Cleaning the file url
                var path = fileDialog.fileUrl.toString();
                path = path.replace(/^(file:\/{3})/,"");
                var cleanPath = decodeURIComponent(path);

                exifButton.enabled = true
                exifButton.visible = true
                skipForward.enabled = true
                skipBackward.enabled = true
                rotateLeft.enabled = true
                rotateRight.enabled = true
                fileNameLabel.visible = true

                rotateLeftRect.color = "#8fbccc"
                rotateLeftImage.source = "../assets/rotate_left.png"
                rotateRightRect.color = "#8fbccc"
                rotateRightImage.source = "../assets/rotate_right.png"
                skipBackwardRect.color = "#8fbccc"
                skipBackwardImage.source = "../assets/skip_backward.png"
                skipForwardRect.color = "#8fbccc"
                skipForwardImage.source = "../assets/skip_forward.png"

                fileNameLabel.text = cleanPath

                // Resetting the state of right and left rotate buttons
                rotateLeft.rotated = 0
                rotateRight.rotated = 0
                // Resetting the rotation angle
                displayedImage.rotationAngle = 0

                // Setting the image source
                displayedImage.source = fileDialog.fileUrl
            }
            onRejected: {
                console.log("Canceled")
            }
        }

        ColumnLayout {
            // Setting the size and position of the layout
            width: { parent.width - 60 }
            height: { parent.height - 60}
            anchors.top: parent.top
            anchors.left: parent.left
            anchors.right: parent.right
            anchors.bottom: parent.bottom

            Label {
                id: fileNameLabel
                //Layout.fillWidth: true; Layout.fillHeight: true
                font.pointSize: 9
                font.family: webFont.name
                text: ""
                visible: false
                topPadding: 9
                bottomPadding: 9
                leftPadding: 30
                color: "#8fbccc"
                verticalAlignment: Text.AlignVCenter
                // This way we can handle multiline
                wrapMode: Label.WordWrap
                background: Rectangle {
                    color: "white"
                    width: mainWindow.width
                }
            }
            
            Image {
                id: displayedImage
                property var rotationAngle: 0

                source: "../assets/default_image.png"
                fillMode: Image.PreserveAspectFit
                Layout.fillWidth: true; Layout.fillHeight: true
                Layout.topMargin: 5
                Layout.leftMargin: 55
                Layout.bottomMargin: 20
    
                //anchors.top: parent.top
                //anchors.left: parent.left
                //anchors.right: parent.right
                //anchors.bottom: parent.bottom
                
                // By centering the image in the center
                // we can rotate it easily
                anchors.centerIn: parent
                transform: Rotation { origin.x: displayedImage.width / 2; origin.y: displayedImage.height / 2; angle: displayedImage.rotationAngle}
            }
    		
            RowLayout {
		    	spacing: 30

                GenericCommandButton {
                    id: skipBackward

                    Layout.preferredWidth: 50
                    Layout.topMargin: 50
                    Layout.leftMargin: 45
                    Layout.bottomMargin: 20

                    background: CommandButtonRect {
                        id: skipBackwardRect

                        CommandButtonImage {
                            id: skipBackwardImage
                            source: "../assets/skip_backward_disabled.png"
                        }
                    }
                }

                // Spacer item
                Item {
                    Layout.fillWidth: true
                    Layout.fillHeight: true
                }

                GenericCommandButton {
                    id: rotateLeft
                    property var rotated: 0

                    Layout.topMargin: 50
                    Layout.preferredWidth: 50
                    Layout.bottomMargin: 20

                    background: CommandButtonRect {
                        id: rotateLeftRect

                        CommandButtonImage {
                            id: rotateLeftImage
                            source: "../assets/rotate_left_disabled.png"
                        }
                    }

                    onClicked: {
                        // Handling the image rotation, considering the right rotate
                        // button state
                        if (rotated == 0 && rotateRight.rotated == 0) {
                            displayedImage.width = displayedImage.height
                            rotated = 1
                        }
                        else if (rotated == 0 && rotateRight.rotated == 1) {
                            displayedImage.width = parent.width
                            rotateRight.rotated = 0
                            rotated = 0
                        }
                        else if (rotated == 1 && rotateRight.rotated == 1) {
                            displayedImage.width = displayedImage.height
                            rotateRight.rotated = 0
                            rotated = 0 
                        }
                        else {
                            displayedImage.width = parent.width
                            rotated = 0
                        }
                        // Setting the angle
                        displayedImage.rotationAngle = displayedImage.rotationAngle - 90
                    }
                }

                GenericCommandButton {
                    id: rotateRight
                    property var rotated: 0

                    Layout.topMargin: 50
                    Layout.preferredWidth: 50
                    Layout.bottomMargin: 20
                    
                    background: CommandButtonRect {
                        id: rotateRightRect

                        CommandButtonImage {
                            id: rotateRightImage
                            source: "../assets/rotate_right_disabled.png"
                        }
                    }

                    onClicked: {
                        // Handling the image rotation, considering the left rotate
                        // button state
                        if (rotated == 0 && rotateLeft.rotated == 0) {
                            displayedImage.width = displayedImage.height
                            rotated = 1
                        }
                        else if (rotated == 0 && rotateLeft.rotated == 1) {
                            displayedImage.width = parent.width
                            rotateLeft.rotated = 0
                            rotated = 0
                        }
                        else if (rotated == 1 && rotateLeft.rotated == 1) {
                            displayedImage.width = displayedImage.height
                            rotateLeft.rotated = 0
                            rotated = 0 
                        }
                        else {
                            displayedImage.width = parent.width
                            rotated = 0
                        }
                        // Setting the angle
                        displayedImage.rotationAngle = displayedImage.rotationAngle + 90
                    }
                }

                // Spacer item
                Item {
                    Layout.fillWidth: true
                    Layout.fillHeight: true
                }

                GenericCommandButton {
                    id: skipForward

                    Layout.preferredWidth: 50
                    Layout.topMargin: 50
                    Layout.rightMargin: 45
                    Layout.bottomMargin: 20

                    background: CommandButtonRect {
                        id: skipForwardRect

                        CommandButtonImage {
                            id: skipForwardImage
                            source: "../assets/skip_forward_disabled.png"
                        }
                    }
                }
    		}
        }
    }

    // A new window that will contains exif data of
    // selected image
    property var testWindow: ApplicationWindow {
        id: exifWindow
        width: 300; height: 400
        minimumWidth: 200
        minimumHeight: 400
        visible: false; title: "Exif Data"
	    Material.theme: Material.Dark
        color: "#f7f7f7"
        flags: Qt.Dialog

         header: Label {
            text: "Exif Data"
            font.pointSize: 10
            topPadding: 10
            bottomPadding: 10
            leftPadding: 15
            color: "white"
            background: Rectangle {
                color: "#8fbccc"
                Layout.fillWidth: true; Layout.fillHeight: true
            }            
         }

        ListView {
        id: listView
        anchors.fill: parent
        model: listModel
        spacing: -1
        delegate: Rectangle {
            width: listView.width
            height: listView.height / 6
            border.width: 1
            border.color: "black"

            Text {
                text: "Hour: " + hour
                anchors.centerIn: parent
            }
        }

        ScrollBar.vertical: ScrollBar {}
        }

        ListModel {
            id: listModel

            Component.onCompleted: {
                for (var i = 0; i < 24; i++) {
                    append(createListElement(i));
                }
            }

            function createListElement(index) {
                return {
                    hour: index
                };
            }
        }
    }
}