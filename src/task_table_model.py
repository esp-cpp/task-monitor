#!/usr/bin/python
from PyQt5.QtCore import *
from PyQt5.QtCore import QTimer, QObject, pyqtSlot, pyqtSignal, QAbstractTableModel, QModelIndex

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