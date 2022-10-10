import QtQuick 2.15
import QtQuick.Controls 2.15

ListView {
    id: view
    anchors.fill: parent
    model: logModel
    clip: true
    delegate: TextArea {
        id: delegateRoot
        padding: 0
        width: ListView.view.width
        textFormat: TextEdit.RichText
        wrapMode: Text.Wrap
        readOnly: true
        cursorVisible: false

        text: modelData
    }

    onCountChanged: {
	    if (true) {
		    Qt.callLater( view.positionViewAtEnd )
	    }
    }
    ScrollBar.vertical: ScrollBar { active: true; visible: true }
}
