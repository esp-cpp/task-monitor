import QtQuick 2.15
import QtQuick.Controls 2.15

Item {
    anchors.fill: parent
    property QtObject taskModel

    HorizontalHeaderView {
        id: header
        syncView: tableView
        anchors.top: parent.top
    }

    TableView {
        id: tableView
        model: taskModel
        width: parent.width
        height: parent.height - header.height
        anchors.top: header.bottom
        columnSpacing: 1
        rowSpacing: 1
        // boundsBehavior: Flickable.StopAtBounds
        clip: true

        columnWidthProvider: function (_) {
            return parent.width / 4
        }

        delegate: TaskTableViewDelegate {}
        ScrollIndicator.horizontal: ScrollIndicator { }
        ScrollIndicator.vertical: ScrollIndicator { }
    }
}
