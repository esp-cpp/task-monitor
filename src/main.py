#!/usr/bin/python
import sys

from PyQt5.QtGui import QGuiApplication
from PyQt5.QtQml import QQmlApplicationEngine
from PyQt5.QtCore import QObject

from task_table_model import TaskTableModel
from backend import Backend

def main():
    app = QGuiApplication(sys.argv)
    engine = QQmlApplicationEngine()

    tasktablemodel = TaskTableModel()
    backend = Backend()

    engine.load('main.qml')

    ctx = engine.rootContext()
    root = engine.rootObjects()[0]
    # connect all the signals / slots
    engine.quit.connect(app.quit)

    portMenu = root.findChild(QObject, "portMenu")
    portMenu.refreshPorts.connect(backend.list_serial_ports)
    portMenu.openPort.connect(backend.open_port)
    portMenu.closePort.connect(backend.close_port)
    backend.newPorts.connect(portMenu.updatePorts)
    backend.portOpened.connect(portMenu.openedPort)
    backend.portClosed.connect(portMenu.closedPort)

    root.quit.connect(backend.close_port)
    root.quit.connect(engine.quit)
    backend.updateTasks.connect(tasktablemodel.update)
    backend.newTask.connect(tasktablemodel.insertRow)
    backend.newTasks.connect(tasktablemodel.insertRows)

    # set the properties of the root
    root.setProperty('backend', backend)
    root.setProperty('tableModel', tasktablemodel)

    # ensure data is correct on first start
    backend.update_time()
    backend.list_serial_ports()

    '''
    backend.newTask.emit(["task 10", 15, 2047, 10])
    backend.newTasks.emit([
        ["task 11", 15, 2047, 10],
        ["task 12", 25, 2047, 11],
        ["task 13", 85, 8192, 13]
    ])
    '''

    # run the app
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
