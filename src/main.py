import sys
from src.model.chessboard import Chessboard
from src.controller.controller import Controller
from PyQt6.QtWidgets import QApplication

if __name__ == "__main__":
    app = QApplication(sys.argv)
    model = Chessboard()
    controller = Controller(model)
    app.exec()
