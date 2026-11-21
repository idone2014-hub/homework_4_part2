import sys

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
            '<a href="https://github.com/your-username/your-repository">'
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
        pass

    def plot_graph(self):
        self.axes.clear()
        self.axes.plot([10, 20, 30, 40], [100, 180, 260, 340], marker="o")
        self.axes.set_title("Ice Cream Profits vs. Temperature")
        self.axes.set_xlabel("Temperature")
        self.axes.set_ylabel("Profit")
        self.axes.grid(True, alpha=0.3)
        self.figure.tight_layout()
        self.canvas.draw()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    with open("style.qss", "r") as f:
        app.setStyleSheet(f.read())
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
