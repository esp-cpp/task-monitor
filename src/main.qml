import QtQuick 2.15
import QtQuick.Controls 1.4
import QtQuick.Controls 2.3

import "components"

ApplicationWindow {
    visible: true
    width: 400
    height: 600
    title: "Task Monitor"
    property string currTime: "00:00:00"
    property QtObject tableModel
    property QtObject backend

    signal quit
    signal refreshPorts
    signal openPort(variant port)
    signal closePort

    function updatePorts(ports) {
        // Update the serial ports list
        serialPorts.clear()
        for (var p of ports) {
            serialPorts.append({text:p})
        }
    }
    function openedPort(port) {
        openMenu.enabled = false
        closeButton.enabled = true
        closeButton.text = qsTr("&Close " + port)
    }
    function closedPort(port) {
        openMenu.enabled = true
        closeButton.enabled = false
        closeButton.text = qsTr("&Close")
    }

    menuBar: MenuBar {
        Menu {
            title: qsTr("&File")
            Action { text: qsTr("&Save") }
            Action { text: qsTr("Save &As...") }
            MenuSeparator { }
            Action {
                text: qsTr("&Quit")
                onTriggered: quit()
            }
        }
        Menu {
            title: qsTr("&Ports")
            ListModel{
                id:serialPorts
            }

            Action {
                text: qsTr("&Refresh")
                onTriggered: refreshPorts()
            }
            Menu {
                id: openMenu
                title: "&Open"
                enabled: true
                Instantiator {
                    model: serialPorts
                    MenuItem {
                        text: model.text
                        onClicked: openPort(model.text)
                    }

                    // The trick is on those two lines
                    onObjectAdded: openMenu.insertItem(index, object)
                    onObjectRemoved: openMenu.removeItem(object)
                }
            }
            Action {
                enabled: false
                id: closeButton
                text: qsTr("&Close")
                onTriggered: closePort()
            }
        }
        Menu {
            title: qsTr("&Help")
            Action {
                text: qsTr("&About")
            }
        }
    }

    TabView {
        anchors.fill: parent
        Tab {
            title: "Tasks"
            anchors.fill: parent
            TaskTableView {
                anchors.fill: parent
                taskModel: tableModel
            }
        }
        Tab {
            title: "Info"
            anchors.fill: parent
            Rectangle {
                anchors.fill: parent
                color: "transparent"

                Image {
                    sourceSize.width: parent.width
                    sourceSize.height: parent.height
                    source: "./images/background.png"
                    fillMode: Image.PreserveAspectCrop
                }

                Rectangle {
                    anchors.fill: parent
                    color: "transparent"

                    Text {
                        anchors {
                            bottom: parent.bottom
                            bottomMargin: 12
                            left: parent.left
                            leftMargin: 12
                        }
                        text: currTime  // used to be; text: "16:38:33"
                        font.pixelSize: 48
                        color: "white"
                    }

                }
            }

        }
    }
    Connections {
        target: backend

        function onUpdated(msg) {
            currTime = msg;
        }
    }
}
