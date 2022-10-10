#!/usr/bin/python
from PyQt5.QtCore import *
from PyQt5.QtCore import QTimer, QObject, pyqtSlot, pyqtSignal, QAbstractTableModel, QModelIndex

class TaskTableModel(QAbstractTableModel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._data = []
        self._header = ["Name", "CPU %", "High Water Mark (B)", "Priority"]

    def columnCount(self, parent=QModelIndex()):
        return len(self._header)

    def rowCount(self, parent=QModelIndex()):
        return len(self._data)

    def data(self, index, role=Qt.DisplayRole):
        i = index.row()
        j = index.column()
        if role == Qt.DisplayRole and i < len(self._data) and j < len(self._data[i]):
            return "{}".format(self._data[i][j])
        else:
            return QVariant()

    @pyqtSlot(list)
    def update(self, dataIn):
        self.beginRemoveRows(QModelIndex(), 0, self.rowCount())
        self._data = []
        self.endRemoveRows()
        self.beginInsertRows(QModelIndex(), 0, len(dataIn))
        self._data = dataIn
        self.endInsertRows()

    @pyqtSlot(list)
    def insertRow(self, row):
        self.beginInsertRows(QModelIndex(), self.rowCount(), self.rowCount())
        self._data.append(row)
        self.endInsertRows()

    @pyqtSlot(list)
    def insertRows(self, rows):
        numRows = len(rows)
        self.beginInsertRows(QModelIndex(), self.rowCount(), self.rowCount() + numRows)
        for row in rows:
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
