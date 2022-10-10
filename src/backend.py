#!/usr/bin/python
import sys
import re
import time
import threading
import serial, serial.tools.list_ports
from time import strftime, localtime
from datetime import datetime
from PyQt5.QtCore import QTimer, QObject, pyqtProperty, pyqtSlot, pyqtSignal
from ansi2html import Ansi2HTMLConverter

conv = Ansi2HTMLConverter()

class Backend(QObject):
    updated = pyqtSignal(str, arguments=['time'])
    newLog = pyqtSignal(str, arguments=['log'])
    logChanged = pyqtSignal()
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
    utilization = pyqtSignal(float, float, arguments=['time', 'utilization'])

    def __init__(self):
        super().__init__()

        self._logModel = []

        # define serial port & thread for it
        self.port = None
        self.serial_port = None
        self.start_time = datetime.now()
        self.baudrate = 115200
        self.serial_port_thread = None

        # Define timer.
        self.timer = QTimer()
        self.timer.setInterval(100)  # msecs
        self.timer.timeout.connect(self.update_time)
        self.timer.start()

    def __del__(self):
        try:
            if self.run_thread:
                self.close_port()
        except Exception as e:
            pass

    @pyqtProperty(list, notify=logChanged)
    def logModel(self):
        return self._logModel

    @pyqtSlot(result=list)
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

    @pyqtSlot()
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

    @pyqtSlot(str)
    def open_port(self, port):
        self.close_port()
        self._logModel.clear()
        self.logChanged.emit()
        self.port = port
        self.start_time = datetime.now()
        self.start_serial_port()

    def start_serial_port(self):
        # now start the thread to open and read
        self.serial_port_thread = threading.Thread(target=self.serial_port_thread_func)
        self.run_thread = True
        self.serial_port_thread.start()

    def get_task_utilization(self, task_entries):
        if len(task_entries) != 4:
            print("couldn't parse '{}'".format(task_entries))
            return 0.0
        [name, cpu_util, shwm, prio] = task_entries
        if 'IDLE' in name:
            return 0.0
        cpu_util = cpu_util.replace('%','')
        if '<' in cpu_util:
            cpu_util = '0.5'
        try:
            return float(cpu_util)
        except:
            print("exception parsing",cpu_util, "as float")
            return 0.0

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
        cpu = 0.0
        for task in task_data:
            if len(task) and ',' in task:
                entries = task.split(',')
                tasks.append(entries)
                cpu += self.get_task_utilization(entries)
        if cpu:
            cpu = cpu / 2.0 # we have two cores, so divide by 2
            t = (datetime.now() - self.start_time).total_seconds()
            self.utilization.emit(t,cpu)
        return tasks

    def escape_ansi(self, line):
        ansi_escape = re.compile(r"(?:\x1B[@-_]|[\x80-\x9F])[0-?]*[ -/]*[@-~]")
        return ansi_escape.sub("", str(line))

    def update_log(self, line):
        if not line or len(line) == 0:
            return
        # replace \r\n with \n
        l = line.replace('\r\n','')
        l = l.replace('\n','')
        self.newLog.emit(l)
        # convert to html
        html = conv.convert(l)
        self._logModel.append(html)
        self.logChanged.emit()

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
            except Exception as e:
                print("Couldn't open '{}': {}".format(self.port, e))
            try:
                has_data = True
                while self.run_thread:
                    if self.serial_port.inWaiting():
                        has_data = True
                        serial_port_data = self.serial_port.readline()
                        if sys.version_info >= (3, 0):
                            serial_port_data = serial_port_data.decode("utf-8", "backslashreplace")
                        self.update_log(serial_port_data)
                        serial_port_data = serial_port_data.strip()
                        serial_port_data = self.escape_ansi(serial_port_data)
                        # now parse the data and emit the task data if it matches
                        matches = self.parse_serial_data(serial_port_data)
                        # returns a list (tasks) of lists (entries)
                        if len(matches):
                            self.updateTasks.emit(matches)
                    else:
                        if not has_data:
                            break
                        else:
                            has_data = False
                        time.sleep(0.10)
            except Exception as e:
                print(e)
                pass
            try:
                # this may happen when being destroyed, at which point the
                # signal is no longer valid
                self.portClosed.emit(self.port)
            except:
                pass
        else:
            print("Couldn't start serial port thread, bad port/baud: {}/{}".format(self.port, self.baudrate))
        print("Port thread exiting!")

    def update_time(self):
        # Pass the current time to QML.
        curr_time = strftime("%H:%M:%S", localtime())
        self.updated.emit(curr_time)
