# task-monitor
GUI frontend for parsing and plotting performance logging output for esp-cpp

This app receives information from a running ESP32 system, which runs the
TaskMonitor component. The TaskMonitor component outputs usage in the form of:

> task name, cpu%, high_water_mark, priority;;

In a single line, prepended with `[TM]` and ending with a newline `\n`.

Inspiration:
- [TaskManager-pyqt4](https://github.com/HighTemplar-wjiang/TaskManager-pyqt4)
- [pyqt-system-tool](https://github.com/lowstz/pyqt-system-tool)
- [SystemMonitorApp](https://github.com/earthinversion/SystemMonitorApp)
- [uart_serial_plotter](https://github.com/appliedinnovation/uart_serial_plotter)
