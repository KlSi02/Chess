from src.view.chessboard import UIChessboard
from src.controller.chessboard_controller import ChessboardController
from PySide6.QtWidgets import QLabel
from PySide6.QtGui import QDrag, QPixmap
from PySide6.QtCore import Qt, QMimeData, QByteArray, QBuffer, QIODevice, QObject, Signal, Qt


class UiController:
    chess_piece_clicked = Signal(str)

    def __init__(self):

        self.ui_chessboard = UIChessboard()
        self.chessboard_controller = ChessboardController()

    def mousePressEvent(self, event, label):
        if not (event.button() == Qt.LeftButton) and label.pixmap() is None:
            return

        clicked_square = label.objectName()

        for square, piece in self.chessboard_controller.chessboard.save_chars_and_positions.items():
            if square == clicked_square:
                new_list = piece.possible_movements(self.chessboard_controller.chessboard)
                self.highlight_possible_moves(new_list)

    def highlight_possible_moves(self, list_of_possible_moves):
        for alpha, numb in list_of_possible_moves:
            self.chessboard_controller.chess_piece_controller.update_possible_moves(self.chessboard_controller.chessboard, alpha, numb)
            for square in self.ui_chessboard.labels:
                if square.objectName() == f"{alpha}{numb}":
                    square.setStyleSheet("background-color: green; border: 1px solid black;")

    def initialize_labels_with_picture(self):
        for label in self.ui_chessboard.labels:
            label.setMinimumSize(100, 100)
            label.setScaledContents(True)
            square_name = label.objectName()
            from src.utils.helpers import get_piece_name_for_square
            piece_name = get_piece_name_for_square(square_name)

            if piece_name is not None:
                pixmap = QPixmap(f"C:\\Users\\simon\\Desktop\\ChessProject\\src\\assets\\{piece_name}.png")
                pixmap = pixmap.scaled(100, 100)
                label.setPixmap(pixmap)




