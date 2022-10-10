import QtQuick.Controls.Material 2.15
import QtQuick 2.15
import QtQuick.Controls 1.4
import QtQuick.Controls 2.3
import QtQuick.Controls.Styles 1.4

import "components"

// note this requires two context objects: tableModel and bakend
ApplicationWindow {
    visible: true
    width: 400
    height: 600
    title: "Task Monitor"
    property string currTime: "00:00:00"
    signal quit

    menuBar: MenuBar {
        id: menu
        Menu {
            title: qsTr("&File")
            Action { text: qsTr("&Save") }
            Action { text: qsTr("Save &As...") }
            MenuSeparator { }
            Action {
                text: qsTr("Quit")
                onTriggered: quit()
            }
        }
        PortMenu {
            portBackend: backend
        }
        Menu {
            title: qsTr("&Help")
            Action {
                text: qsTr("&About")
            }
        }
    }

    TabView {
        anchors {
            top: menu.bottom
            right: parent.right
            left: parent.left
            bottom: parent.bottom
        }
        Tab {
            title: "Tasks"
            anchors.fill: parent
            TaskTableView {
                anchors.fill: parent
                taskModel: tableModel
            }
        }
        Tab {
            title: "Utilization"
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

                    ProcessGraph {
                        processModel: backend
                    }

                    Text {
                        id: timeText
                        anchors {
                            bottom: parent.bottom
                            bottomMargin: 12
                            left: parent.left
                            leftMargin: 12
                        }
                        text: currTime
                        font.pixelSize: 48
                        color: "white"
                    }

                }
            }
        }
        Tab {
            title: "Log"
            anchors.fill: parent
            LogView {
                logModel: backend
            }
        }

        style: TabViewStyle {
            frameOverlap: 1
            tab: Rectangle {
                color: styleData.selected ? "steelblue" :"lightsteelblue"
                border.color:  "steelblue"
                implicitWidth: Math.max(text.width + 4, 80)
                implicitHeight: 20
                radius: 2
                Text {
                    id: text
                    anchors.centerIn: parent
                    text: styleData.title
                    color: styleData.selected ? "white" : "black"
                }
            }
            frame: Rectangle { color: "steelblue" }
        }
    }
    Connections {
        target: backend

        function onUpdated(msg) {
            currTime = msg;
        }
    }
}
