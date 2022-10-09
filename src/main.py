#!/usr/bin/python
import sys

from PyQt5.QtCore import *
from PyQt5.QtGui import QGuiApplication
from PyQt5.QtQml import QQmlApplicationEngine
from PyQt5.QtCore import QTimer, QObject, pyqtSlot, pyqtSignal, QAbstractTableModel, QModelIndex

from time import strftime, localtime

class TaskTableModel(QAbstractTableModel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._data = [
            ["Task 1",5,54,3],
            ["Task 2","<1",6,1],
            ["Task 3",23,5,2],
        ]
        self._header = ["Name", "CPU %", "High Water Mark (B)", "Priority"]

    def columnCount(self, parent=QModelIndex()):
        return len(self._header)

    def rowCount(self, parent=QModelIndex()):
        return len(self._data)

    def data(self, index, role=Qt.DisplayRole):
        i = index.row()
        j = index.column()
        if role == Qt.DisplayRole:
            return "{}".format(self._data[i][j])

    def update(self, dataIn):
        self._data = dataIn

    def insertRow(self, row):
        self.beginInsertRows(QModelIndex(), self.rowCount(), self.rowCount())
        self._data.append(row)
        self.endInsertRows()

    @pyqtSlot(int, Qt.Orientation, result="QVariant")
    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                return self._header[section]
            else:
                return str(section)

    def flags(self, index):
        return Qt.ItemIsEnabled

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
