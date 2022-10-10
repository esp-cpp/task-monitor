#!/usr/bin/python
import sys

from PyQt5.QtGui import QGuiApplication
from PyQt5.QtQml import QQmlApplicationEngine

from task_table_model import TaskTableModel
from backend import Backend

def main():
    app = QGuiApplication(sys.argv)
    engine = QQmlApplicationEngine()
    engine.quit.connect(app.quit)

    tasktablemodel = TaskTableModel()
    backend = Backend()
    backend.newTask.connect(tasktablemodel.insertRow)
    backend.newTasks.connect(tasktablemodel.insertRows)

    engine.load('main.qml')

    # set the properties of the root
    engine.rootObjects()[0].setProperty('backend', backend)
    engine.rootObjects()[0].setProperty('tableModel', tasktablemodel)

    # ensure time is correct on first start
    backend.update_time()
    # tasktablemodel.insertRow(["task 10", 15, 2047, 10])
    backend.newTask.emit(["task 10", 15, 2047, 10])
    backend.newTasks.emit([
        ["task 11", 15, 2047, 10],
        ["task 12", 25, 2047, 11],
        ["task 13", 85, 8192, 13]
    ])

    # run the app
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
