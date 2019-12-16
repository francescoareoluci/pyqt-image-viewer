import QtQuick 2.5
import QtQuick.Controls 2.0
import QtQuick.Layouts 1.3
import QtQuick.Controls.Material 2.0
import QtQuick.Dialogs 1.0
import QtQuick.Window 2.1
import QtGraphicalEffects 1.0

import Example 1.0

QtObject {

    property var controlWindow: ApplicationWindow {
        id: mainWindow
        width: 800; height: 600
        minimumWidth: 600
        minimumHeight: 400
        visible: true; title: "Image Viewer"
        FontLoader { id: webFont; source: "../assets/Lato-Regular.ttf" }

        // Setting the mainWindow background image
        background: BorderImage { 
                z: -3
                horizontalTileMode: BorderImage.Repeat
                verticalTileMode: BorderImage.Repeat
                source: "../assets/cream_pixels.png"
        }

        onClosing: {
            // Close any other existing windows
            exifWindow.visible = false
        }

        // Setting the header of main page,
        // which contains the title, the image
        // selection button and exif data button
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
                id: headerRect
                color: "#8fbccc"
                Layout.fillWidth: true; Layout.fillHeight: true
                //width: parent.width
            }            

            RowLayout {
                anchors.right: parent.right
            
                Button {
                    id: exifButton
                    objectName: 'exifButton'
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

                    background: Rectangle {
                        radius: 5
                        color: "#8fbccc"
                    }

                    onClicked: {
                        exifWindow.visible = true
                    }

                    // Ctrl+e hotkey binding
                    Shortcut {
                        sequence: "Ctrl+e"
                        onActivated: {
                            if (exifButton.visible == false) {
                                return
                            }
                            exifWindow.visible = true
                        }
                    }
                }

                Button {
                    id: imageButton
                    // TODO: how to set font color without this trick?
                    text: "<font color=\"#8fbccc\">Choose an image</font>"
                    padding: 10
                    width: 170
                    font.pointSize: 10
                    font.family: webFont.name
                    Layout.topMargin: 10
                    Layout.rightMargin: 5
                    
                    background: Rectangle {
                        radius: 5
                        color: "white"
                    }

                    onClicked: {
                        imageFileDialog.visible = true
                    }

                    // Ctrl+i hotkey binding
                    Shortcut {
                        sequence: "Ctrl+i"
                        onActivated: {
                            imageFileDialog.visible = true
                        }
                    }
                }

                Button {
                    id: folderButton
                    // TODO: how to set font color without this trick?
                    text: "<font color=\"#8fbccc\">Select a folder</font>"
                    padding: 10
                    width: 170
                    font.pointSize: 10
                    font.family: webFont.name
                    Layout.topMargin: 10
                    Layout.rightMargin: 30
                    
                    background: Rectangle {
                        radius: 5
                        color: "white"
                    }

                    onClicked: {
                        folderFileDialog.visible = true
                    }

                    // Ctrl+f hotkey binding
                    Shortcut {
                        sequence: "Ctrl+f"
                        onActivated: {
                            folderFileDialog.visible = true
                        }
                    }
                }
            }
        }

        // File dialog used to select an image
        ImageSelector {
            id: imageFileDialog
            objectName: "imageFileDialog"
            signal imageSelected(string path)

            // Handle GUI update and emit signal for our controller
            onAccepted: {
                console.log("Image selected: " + imageFileDialog.fileUrls)

                // Cleaning the file url
                var path = imageFileDialog.fileUrl.toString();
                path = path.replace(/^(file:\/{3})/,"/");
                var cleanPath = decodeURIComponent(path);

                // Emit signal
                imageSelected(cleanPath)

                // Resetting the state of right and left rotate buttons
                rotateLeft.rotated = 0
                rotateRight.rotated = 0
                // Resetting the rotation angle
                displayedImage.rotationAngle = 0
            }
        }

        // File dialog used to select an image
        FolderSelector {
            id: folderFileDialog
            objectName: "folderFileDialog"
            signal folderSelected(string path)

            // Handle GUI update and emit signal for our controller
            onAccepted: {
                console.log("Folder selected: " + folderFileDialog.fileUrls)

                // Cleaning the file url
                var path = folderFileDialog.fileUrl.toString();
                path = path.replace(/^(file:\/{3})/,"/");
                var cleanPath = decodeURIComponent(path);

                // Emit signal
                folderSelected(cleanPath)

                // Resetting the state of right and left rotate buttons
                rotateLeft.rotated = 0
                rotateRight.rotated = 0
                // Resetting the rotation angle
                displayedImage.rotationAngle = 0
            }
        }

        Item {
            anchors.fill: parent
        
            ColumnLayout {
                // Setting the size and position of the layout
                width: { parent.width - 60 }
                height: { parent.height - 60}

                anchors.top: parent.top
                anchors.left: parent.left
                anchors.right: parent.right
                anchors.bottom: parent.bottom

                // Label containing the filename
                FilenameLabel {
                    id: fileNameLabel
                    objectName: 'fileNameLabel'
                    z: -2
                }

                Image {
                    id: displayedImage
                    objectName: 'displayedImage'
                    property var rotationAngle: 0

                    source: "../assets/default_image.png"
                    fillMode: Image.PreserveAspectFit

                    //Layout.fillWidth: true; Layout.fillHeight: true
                    Layout.preferredWidth: parent.width - 50
                    Layout.preferredHeight: parent.height - 120

                    Layout.topMargin: 5
                    Layout.bottomMargin: 20
                    
                    // By centering the image in the center
                    // we can rotate it easily
                    anchors.centerIn: parent
                    // The rotation state is managed directly via qml
                    transform: Rotation { origin.x: displayedImage.width / 2; origin.y: displayedImage.height / 2; angle: displayedImage.rotationAngle}
                }

                // Layout containing image command buttons
                RowLayout {
		        	spacing: 30
                    anchors.left: parent.left
                    anchors.right: parent.right
                    anchors.bottom: parent.bottom

                    // Spacer item
                    Item {
                        Layout.fillWidth: true
                        Layout.fillHeight: true
                    }

                    DropShadow {
                        anchors.fill: skipBackward
                        horizontalOffset: 2
                        verticalOffset: 2
                        radius: 5.0
                        samples: 17
                        color: "#80000000"
                        source: skipBackward
                    }

                    DropShadow {
                        anchors.fill: rotateLeft
                        horizontalOffset: 2
                        verticalOffset: 2
                        radius: 5.0
                        samples: 17
                        color: "#80000000"
                        source: rotateLeft
                    }

                    GenericCommandButton {
                        id: skipBackward
                        objectName: 'skipBackward'
                        signal previousButtonPressed()

                        function handlePreviousImage() {
                            previousButtonPressed()
                            
                            // Resetting the state of right and left rotate buttons
                            rotateLeft.rotated = 0
                            rotateRight.rotated = 0
                            // Resetting the rotation angle
                            displayedImage.rotationAngle = 0
                        }

                        Layout.preferredWidth: 30
                        Layout.topMargin: 50
                        Layout.leftMargin: 45
                        Layout.bottomMargin: 20

                        background: CommandButtonRect {
                            id: skipBackwardRect
                            objectName: 'skipBackwardRect'

                            CommandButtonImage {
                                id: skipBackwardImage
                                objectName: 'skipBackwardImage'
                                source: "../assets/skip_backward_disabled.png"
                            }
                        }

                        onClicked: {
                            handlePreviousImage()
                        }

                        // Left arrow hotkey binding
                        Shortcut {
                            sequence: "left"
                            onActivated: { 
                                if (skipBackward.enabled == false) {
                                    return                                
                                }
                                skipBackward.handlePreviousImage() 
                            }
                        }
                    }

                    GenericCommandButton {
                        id: rotateLeft
                        objectName: 'rotateLeft'
                        property var rotated: 0

                        function handleLeftRotate() {
                            // Handling the image rotation, evaluating the right rotate
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

                        Layout.topMargin: 50
                        Layout.preferredWidth: 30
                        Layout.bottomMargin: 20

                        background: CommandButtonRect {
                            id: rotateLeftRect
                            objectName: 'rotateLeftRect'

                            CommandButtonImage {
                                id: rotateLeftImage
                                objectName: 'rotateLeftImage'
                                source: "../assets/rotate_left_disabled.png"
                            }
                        }

                        onClicked: {
                            handleLeftRotate()
                        }

                        // Ctrl+L hotkey binding
                        Shortcut {
                            sequence: "Ctrl+L"
                            onActivated: {
                                if (rotateLeft.enabled == false) {
                                    return                                
                                } 
                                rotateLeft.handleLeftRotate() 
                            }
                        }
                    }

                    GenericCommandButton {
                        id: rotateRight
                        objectName: 'rotateRight'
                        property var rotated: 0

                        function handleRightRotate() {
                            // Handling the image rotation, evaluating the left rotate
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

                        Layout.topMargin: 50
                        Layout.preferredWidth: 30
                        Layout.bottomMargin: 20

                        background: CommandButtonRect {
                            id: rotateRightRect
                            objectName: 'rotateRightRect'

                            CommandButtonImage {
                                id: rotateRightImage
                                objectName: 'rotateRightImage'
                                source: "../assets/rotate_right_disabled.png"
                            }
                        }

                        onClicked: {
                            handleRightRotate()
                        }

                        // Ctrl+R hotkey binding
                        Shortcut {
                            sequence: "Ctrl+R"
                            onActivated: {
                                if (rotateRight.enabled == false) {
                                    return                                
                                } 
                                rotateRight.handleRightRotate() 
                            }
                        }
                    }

                    GenericCommandButton {
                        id: skipForward
                        objectName: 'skipForward'
                        signal nextButtonPressed()

                        function handleNextImage() {
                            if (skipForward.enabled == 'false') {
                                return                                
                            }

                            nextButtonPressed()
                            
                            // Resetting the state of right and left rotate buttons
                            rotateLeft.rotated = 0
                            rotateRight.rotated = 0
                            // Resetting the rotation angle
                            displayedImage.rotationAngle = 0
                        }

                        Layout.preferredWidth: 30
                        Layout.topMargin: 50
                        Layout.rightMargin: 45
                        Layout.bottomMargin: 20

                        background: CommandButtonRect {
                            id: skipForwardRect
                            objectName: 'skipForwardRect'

                            CommandButtonImage {
                                id: skipForwardImage
                                objectName: 'skipForwardImage'
                                source: "../assets/skip_forward_disabled.png"
                            }
                        }

                        onClicked: {
                            handleNextImage()
                        }

                        // Right arrow hotkey binding
                        Shortcut {
                            sequence: "right"
                            onActivated: {
                                if (skipForward.enabled == false) {
                                    return                                
                                } 
                                skipForward.handleNextImage() 
                            }
                        }
                    }

                    // Spacer item
                    Item {
                        Layout.fillWidth: true
                        Layout.fillHeight: true
                    }

                    DropShadow {
                        anchors.fill: skipForward
                        horizontalOffset: 2
                        verticalOffset: 2
                        radius: 5.0
                        samples: 17
                        color: "#80000000"
                        source: skipForward
                    }

                    DropShadow {
                        anchors.fill: rotateRight
                        horizontalOffset: 2
                        verticalOffset: 2
                        radius: 5.0
                        samples: 17
                        color: "#80000000"
                        source: rotateRight
                    }
                }
    		}
        }
    }

    // A new window that will contains exif data of
    // selected image
    property var testWindow: ApplicationWindow {
        id: exifWindow
        width: 600; height: 400
        minimumWidth: 400
        minimumHeight: 300
        visible: false; title: "Exif Data"
        color: "#f7f7f7"
        // TODO: dialog or window?
        flags: Qt.Dialog

        header: Label {
            text: "Name"
            font.pointSize: 11
            topPadding: 10
            bottomPadding: 10
            leftPadding: 15
            color: "white"
            background: Rectangle {
                color: "#8fbccc"
                Layout.fillWidth: true; Layout.fillHeight: true
            }            

            Label {
                anchors.right: parent.right
                text: "Value"
                font.pointSize: 11
                topPadding: 10
                bottomPadding: 10
                rightPadding: 15
                color: "white"
            }
        }

        ListView {
            id: exifView
            anchors.fill: parent
            model: exifViewHandler.exif
            // This negative spacing is used to manage
            // the overlapping border of rectangles
            spacing: -1
            delegate: Rectangle {
                id: delegateRect

                width: exifView.width
                height: exifView.height / 6
                border.width: 1
                border.color: '#d9d9d9'

                RowLayout {
                    spacing: 20
                    anchors.left: parent.left
                    anchors.right: parent.right

                    Label {
                        text: name
                        Layout.topMargin: delegateRect.height / 2.5
                        Layout.leftMargin: 15
                    }

                    // Spacer item
                    Item {
                        Layout.fillWidth: true
                        Layout.fillHeight: true
                    }

                    Label {
                        text: value
                        Layout.topMargin: delegateRect.height / 2.5
                        Layout.rightMargin: 15
                    }
                }
            }

            ScrollBar.vertical: ScrollBar {}
        }
    }
}