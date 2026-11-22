import sys

import numpy as np
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg, NavigationToolbar2QT
from matplotlib.figure import Figure
from PySide6.QtWidgets import (
    QApplication,
    QDialog,
    QFileDialog,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QPushButton,
    QVBoxLayout,
    QWidget,
)


class AboutDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("About")

        layout = QVBoxLayout()
        description = QLabel(
            "Explore how temperature relates to ice cream sales profits."
        )
        repository_link = QLabel(
            '<a href="https://github.com/idone2014-hub/homework_4_part2" '
            'style="color: #0B57D0; font-weight: bold;">'
            "Project repository</a>"
        )
        repository_link.setOpenExternalLinks(True)

        layout.addWidget(description)
        layout.addWidget(repository_link)
        self.setLayout(layout)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.temperatures = []
        self.profits = []

        self.setWindowTitle("Ice Cream Sales Profits")
        self.resize(900, 680)

        central_widget = QWidget()
        layout = QVBoxLayout(central_widget)

        heading = QLabel("Ice Cream Sales Profits")
        heading.setObjectName("heading")
        subtitle = QLabel("See how temperature affects daily sales profits.")
        subtitle.setObjectName("subtitle")

        buttons_layout = QHBoxLayout()
        load_button = QPushButton("Load CSV File")
        load_button.clicked.connect(self.open_file_dialog)
        about_button = QPushButton("About")
        about_button.clicked.connect(self.show_about_dialog)
        buttons_layout.addWidget(load_button)
        buttons_layout.addWidget(about_button)
        buttons_layout.addStretch()

        self.figure = Figure()
        self.axes = self.figure.add_subplot(111)
        self.canvas = FigureCanvasQTAgg(self.figure)
        toolbar = NavigationToolbar2QT(self.canvas, self)

        layout.addWidget(heading)
        layout.addWidget(subtitle)
        layout.addLayout(buttons_layout)
        layout.addWidget(toolbar)
        layout.addWidget(self.canvas)
        self.setCentralWidget(central_widget)

        self.plot_graph()

    def open_file_dialog(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Load CSV File",
            "",
            "CSV files (*.csv)",
        )
        if file_path:
            self.load_file(file_path)

    def show_about_dialog(self):
        dialog = AboutDialog()
        dialog.exec()

    def load_file(self, file_path):
        self.temperatures = []
        self.profits = []

        with open(file_path, "r") as f:
            lines = f.readlines()

        for line in lines[1:]:
            clean_line = line.strip()
            if clean_line != "":
                parts = clean_line.split(",")
                temperature = float(parts[0])
                revenue = float(parts[1])
                self.temperatures.append(temperature)
                self.profits.append(revenue)

        self.plot_graph()

    def plot_graph(self):
        self.axes.clear()
        self.axes.scatter(self.temperatures, self.profits, s=1)

        self.axes.spines["top"].set_visible(False)
        self.axes.spines["right"].set_visible(False)

        if len(self.temperatures) > 0:
            m, b = np.polyfit(self.temperatures, self.profits, 1)
            trend_temperatures = [
                min(self.temperatures),
                max(self.temperatures),
            ]
            trend_profits = [
                m * temperature + b for temperature in trend_temperatures
            ]
            if b >= 0:
                equation = f"y = {m:.2f}x + {b:.2f}"
            else:
                equation = f"y = {m:.2f}x - {abs(b):.2f}"
            self.axes.plot(
                trend_temperatures,
                trend_profits,
                color="red",
                label=equation,
            )
            self.axes.legend()

        self.axes.set_xlim(left=0)
        self.axes.set_ylim(bottom=0)
        self.axes.set_title("Ice Cream Sales Revenue vs. Temperature")
        self.axes.set_xlabel("Temperature (°C)")
        self.axes.set_ylabel("Revenue ($)")
        self.axes.grid(True, alpha=0.3)
        self.figure.tight_layout()
        self.figure.subplots_adjust(bottom=0.20)
        self.canvas.draw()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    with open("style.qss", "r") as f:
        app.setStyleSheet(f.read())
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
