import pytest
import sys

sys.path.append("C:\\Users\\simon\\Desktop\\ChessProject")
from src.gui.ui_chessboard.chessboard import Chessboard

import pytest
from PyQt5.QtWidgets import QApplication

@pytest.fixture
def app():
    test_app = QApplication([])
    test_board = Chessboard()
    return test_app, test_board


def test_chessboard_creation(app):
    app, test_board = app
    assert app is not None
    assert test_board is not None
    assert test_board.windowTitle() == "Chessboard"
    assert len(test_board.labels) == 64




