import QtQuick 2.0
import QtCharts 2.0

ChartView {
    function onUtilization(t, cpu) {
        utilizationLineSeries.append(t,cpu)
        xAxis.max = Math.max(10, Math.ceil(t))
        xAxis.min = Math.min(0, xAxis.max - 10)
    }
    function onPortOpened() {
        utilizationLineSeries.clear()
        xAxis.max = 10
        xAxis.min = 0
    }

    property QtObject processModel

    Component.onCompleted: {
        processModel.utilization.connect(onUtilization)
        processModel.portOpened.connect(onPortOpened)
    }

    title: "Running Process Info"
    anchors {
        top: parent.top
        left: parent.left
        right: parent.right
        bottom: timeText.top
    }
    antialiasing: true

    // theme: ChartView.ChartThemeBrownSand

    // Define x-axis to be used with the series instead of default one
    ValueAxis {
        id: xAxis
        min: 0.0
        max: 10.0
        tickCount: 7
        labelFormat: "%.0f"
    }
    ValueAxis {
        id: yAxis
        min: 0.0
        max: 100.0
        tickCount: 6
    }

    AreaSeries {
        name: "CPU Utilization (%)"
        axisX: xAxis
        axisY: yAxis
        upperSeries: LineSeries {
            id: utilizationLineSeries
        }
    }
}
