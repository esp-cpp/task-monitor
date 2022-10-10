#!/usr/bin/python
import sys

from PyQt5.QtGui import QGuiApplication
from PyQt5.QtQml import QQmlApplicationEngine
from PyQt5.QtCore import QObject, QUrl
from PyQt5.QtWidgets import QApplication, QStyleFactory

from task_table_model import TaskTableModel
from backend import Backend

def main():
    app = QApplication(sys.argv)
    engine = QQmlApplicationEngine()

    tasktablemodel = TaskTableModel()
    backend = Backend()

    ctx = engine.rootContext()
    ctx.setContextProperty('backend', backend)
    ctx.setContextProperty('logModel', backend.logModel)
    ctx.setContextProperty('tableModel', tasktablemodel)

    def update_log_model():
        ctx.setContextProperty('logModel', backend.logModel)

    engine.load(QUrl('main.qml'))

    root = engine.rootObjects()[0]

    print(QStyleFactory.keys())
    app.setStyle('Windows')

    # connect all the signals / slots
    engine.quit.connect(app.quit)

    root.quit.connect(backend.close_port)
    root.quit.connect(engine.quit)
    backend.updateTasks.connect(tasktablemodel.update)
    backend.newTask.connect(tasktablemodel.insertRow)
    backend.newTasks.connect(tasktablemodel.insertRows)
    backend.logChanged.connect(update_log_model)

    # ensure data is correct on first start
    backend.update_time()
    backend.list_serial_ports()

    # run the app
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
