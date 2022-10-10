import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQml 2.15

ScrollView {
    id: scrollView
    anchors.fill: parent
    property QtObject logModel
    property string logData

    function scrollToBottom() {
        ScrollBar.vertical.position = 1.0 - ScrollBar.vertical.size
    }

    function onPortOpened() {
        // clear the text
        logData = ""
    }

    function onLogReceived(log) {
        // append the text and scroll
        logData += '\n' + log
        scrollToBottom()
    }

    Component.onCompleted: {
        logModel.newLog.connect(onLogReceived)
        logModel.portOpened.connect(onPortOpened)
    }

    Text {
        id: logText
        //cursorVisible: false
        //readOnly: true
        anchors.fill: parent
        text: logData
    }
}
