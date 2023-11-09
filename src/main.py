import sys
from PySide6.QtWidgets import QApplication
from view.chessboard import Chessboard


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Chessboard()
    window.show()
    sys.exit(app.exec())
