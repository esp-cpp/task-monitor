#!/usr/bin/python
import sys
import threading
import serial, serial.tools.list_ports
from time import strftime, localtime
from PyQt5.QtCore import QTimer, QObject, pyqtSignal

class Backend(QObject):
    updated = pyqtSignal(str, arguments=['time'])
    # contains all the serial ports
    newPorts = pyqtSignal(list, arguments=['ports'])
    portOpened = pyqtSignal(str, arguments=['port'])
    portClosed = pyqtSignal(str, arguments=['port'])
    # contains all tasks
    updateTasks = pyqtSignal(list, arguments=['tasks'])
    # contains an additional task
    newTask = pyqtSignal(list, arguments=['task'])
    # contains additional tasks
    newTasks = pyqtSignal(list, arguments=['tasks'])

    def __init__(self):
        super().__init__()

        # define serial port & thread for it
        self.port = None
        self.serial_port = None
        self.baudrate = 115200
        self.serial_port_thread = None

        # Define timer.
        self.timer = QTimer()
        self.timer.setInterval(100)  # msecs
        self.timer.timeout.connect(self.update_time)
        self.timer.start()

    def list_serial_ports(self):
        """Lists serial port names
        :returns:
            A list of the serial ports available on the system
        """
        port_descriptors = ["USB Serial Port", "TTL232R-3V3", "USB to UART", "usbserial", "RS232", "USB-UART"]
        ports = list(serial.tools.list_ports.comports())
        result = []
        # print("Found {} ports:".format(len(ports)))
        for p in ports:
            is_correct_type_of_port = False
            for desc in port_descriptors:
                # print("\t{}".format(p.description))
                if desc in p.description:
                    is_correct_type_of_port = True
            if is_correct_type_of_port:
                result.append(p.device)
        self.newPorts.emit(result)
        return result

    def close_port(self):
        # stop it in case it's running
        self.run_thread = False
        if self.serial_port_thread:
            self.serial_port_thread.join()
        # close the port if it's open
        if self.serial_port:
            self.serial_port.close()
        # indicate that we have no port now
        self.port = None

    def open_port(self, port):
        self.close_port()
        self.port = port
        self.start_serial_port()

    def start_serial_port(self):
        # now start the thread to open and read
        self.serial_port_thread = threading.Thread(target=self.serial_port_thread_func)
        self.run_thread = True
        self.serial_port_thread.start()

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
            if len(task) and ',' in task:
                tasks.append(task.split(','))
        return tasks

    def serial_port_thread_func(self):
        if self.port and self.baudrate:
            print("Opening '{}' at {} bps".format(self.port, self.baudrate))
            self.serial_port = serial.Serial()
            self.serial_port.port = self.port
            self.serial_port.baudrate = self.baudrate
            # Disable hardware flow control
            self.serial_port.setRTS(False)
            self.serial_port.setDTR(False)
            try:
                self.serial_port.open()
                self.portOpened.emit(self.port)
                while self.run_thread:
                    if self.serial_port.inWaiting():
                        serial_port_data = self.serial_port.readline()
                        if sys.version_info >= (3, 0):
                            serial_port_data = serial_port_data.decode("utf-8", "backslashreplace")
                        serial_port_data = serial_port_data.strip()
                        # now parse the data and emit the task data if it matches
                        matches = self.parse_serial_data(serial_port_data)
                        # returns a list (tasks) of lists (entries)
                        if len(matches):
                            self.updateTasks.emit(matches)
            except Exception as e:
                print("Couldn't open '{}': {}".format(self.port, e))
            self.portClosed.emit(self.port)
        else:
            print("Couldn't start serial port thread, bad port/baud: {}/{}".format(self.port, self.baudrate))
        print("Port thread exiting!")

    def update_time(self):
        # Pass the current time to QML.
        curr_time = strftime("%H:%M:%S", localtime())
        self.updated.emit(curr_time)
