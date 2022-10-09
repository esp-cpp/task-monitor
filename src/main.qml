import QtQuick 2.15
import QtQuick.Controls 1.4

import "components"

ApplicationWindow {
    visible: true
    width: 400
    height: 600
    title: "Task Monitor"
    property string currTime: "00:00:00"
    property QtObject tableModel
    property QtObject backend

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
