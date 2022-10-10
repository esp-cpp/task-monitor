#!/usr/bin/python
import sys

from PyQt5.QtCore import *
from PyQt5.QtGui import QGuiApplication
from PyQt5.QtQml import QQmlApplicationEngine
from PyQt5.QtCore import QTimer, QObject, pyqtSignal

from task_table_model import TaskTableModel

from time import strftime, localtime

class Backend(QObject):
    updated = pyqtSignal(str, arguments=['time'])

    def __init__(self):
        super().__init__()

        # Define timer.
        self.timer = QTimer()
        self.timer.setInterval(100)  # msecs 100 = 1/10th sec
        self.timer.timeout.connect(self.update_time)
        self.timer.start()

    def update_time(self):
        # Pass the current time to QML.
        curr_time = strftime("%H:%M:%S", localtime())
        self.updated.emit(curr_time)

def main():
    app = QGuiApplication(sys.argv)
    engine = QQmlApplicationEngine()
    engine.quit.connect(app.quit)

    tasktablemodel = TaskTableModel()
    backend = Backend()

    engine.load('main.qml')

    # set the properties of the root
    engine.rootObjects()[0].setProperty('backend', backend)
    engine.rootObjects()[0].setProperty('tableModel', tasktablemodel)

    # ensure time is correct on first start
    backend.update_time()
    tasktablemodel.insertRow(["task 10", 15, 2047, 10])

    # run the app
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
