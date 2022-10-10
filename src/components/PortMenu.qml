import QtQuick 2.15
import QtQuick.Controls 1.4
import QtQuick.Controls 2.3

Menu {
    signal refreshPorts
    signal openPort(variant port)
    signal closePort
    property QtObject portBackend

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

    ListModel{
        id:serialPorts
    }

    title: qsTr("&Ports")

    Component.onCompleted: {
        refreshPorts.connect(portBackend.list_serial_ports)
        openPort.connect(portBackend.open_port)
        closePort.connect(portBackend.close_port)
        portBackend.newPorts.connect(updatePorts)
        portBackend.portOpened.connect(openedPort)
        portBackend.portClosed.connect(closedPort)
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
