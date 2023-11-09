from PySide6.QtWidgets import QMainWindow, QWidget, QGridLayout, QLabel
from PySide6.QtGui import QIcon, QPixmap
from view.clickable_label import ClickableLabel


class UIChessboard(QMainWindow):
    labels = []

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Chessboard")

        icon = QIcon("/assets/Chess_Icon.png")
        self.setWindowIcon(icon)

        self.setGeometry(100, 100, 600, 600)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.grid_layout = QGridLayout(self.central_widget)
        self.grid_layout.setSpacing(0)

        self.create_ui()

    def create_ui(self):
        rows = 8
        cols = 8
        spalten_buchstaben = ["A", "B", "C", "D", "E", "F", "G", "H"]

        for row in range(rows):
            row_labels = []
            for col in range(cols):
                label = QLabel()
                label.resize(100, 100)
                if (row + col) % 2 == 0:
                    label.setStyleSheet("background-color: gray; border: 1px solid black;")
                else:
                    label.setStyleSheet("background-color: white; border: 1px solid black;")

                label_name = spalten_buchstaben[col] + str(8 - row)
                label.setObjectName(label_name)

                self.grid_layout.addWidget(label, row, col)
                row_labels.append(label)
                UIChessboard.labels.append(label)

