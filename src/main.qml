import QtQuick 2.15
import QtQuick.Controls 1.4

import "components"

ApplicationWindow {
    visible: true
    width: 400
    height: 600
    title: "Task Monitor"
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
    }
}
