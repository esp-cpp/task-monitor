#!/usr/bin/python
import serial
import threading
from time import strftime, localtime
from PyQt5.QtCore import QTimer, QObject, pyqtSignal

class Backend(QObject):
    updated = pyqtSignal(str, arguments=['time'])
    newTask = pyqtSignal(list, arguments=['task'])
    newTasks = pyqtSignal(list, arguments=['tasks'])

    def __init__(self):
        super().__init__()

        # define serial port & thread for it
        self.port = None
        self.baudrate = None
        self.serial_port_thread = None

        # Define timer.
        self.timer = QTimer()
        self.timer.setInterval(100)  # msecs
        self.timer.timeout.connect(self.update_time)
        self.timer.start()

    def start_serial_port(self):
        # stop it in case it's running
        self.run_thread = False
        if self.serial_port_thread:
            self.serial_port_thread.join()
        # close the port if it's open
        if self.serial_port:
            self.serial_port.close()
        # now start the thread to open and read
        self.serial_port_thread = threading.Thread(target=self.serial_port_thread_func)

    def parse_serial_data(self, strdata):
        if not strdata.startswith('[TM]'):
            return []
        if ';;' not in strdata:
            return []
        # remove the prefix
        strdata = strdata.replace('[TM]','')
        # the tasks are separated by ';;'
        task_data = strdata.split(';;')
        tasks = []
        for task in task_data:
            tasks.append(task.split(','))

    def serial_port_thread_func(self):
        if self.port and self.baudrate:
            print("Opening '{}' at {} bps".format(self.port, self.baudrate))
            self.serial_port = serial.Serial()
            self.serial_port.port = self.port
            self.serial_port.baudrate = self.baudrate
            try:
                self.serial_port.open()
                while self.run_thread:
                    if self.serial_port.inWaiting():
                        serial_port_data = self.serial_port.readline()
                        if sys.version_info >= (3, 0):
                            serial_port_data = serial_port_data.decode("utf-8", "backslashreplace")
                        serial_port_data = serial_port_data.strip()
                        # now parse the data and emit the task data if it matches
                        matches = self.parse_serial_data(serial_port_data)
                        # returns a list (tasks) of lists (entries)
                        for match in matches:
                            self.newTask.emit(match)
            except Exception as e:
                print("Couldn't open '{}': {}".format(self.port, e))

    def test_emit(self):
        self.newTask.emit(["task 10", 15, 2047, 10])

    def test_emit_multiple(self):
        self.newTasks.emit([
            ["task 11", 15, 2047, 10],
            ["task 12", 15, 2047, 11],
            ["task 13", 15, 8192, 13]
        ])

    def update_time(self):
        # Pass the current time to QML.
        curr_time = strftime("%H:%M:%S", localtime())
        self.updated.emit(curr_time)
