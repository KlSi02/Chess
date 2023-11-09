import sys
from PySide6.QtWidgets import QApplication
from view.chessboard import UIChessboard


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = UIChessboard()
    window.show()
    sys.exit(app.exec())
