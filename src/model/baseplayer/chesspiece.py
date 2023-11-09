import uuid
from abc import ABC, abstractmethod


class ChessPiece(ABC):

    def __init__(self, team):
        self.position = None
        self.possible_moves_on_current_board = []
        self.team = team
        self.possible_moves_without_knowing_board = []
        self.piece_id = str(uuid.uuid4())
        self.possible_moves = []

    def find_position_of_char_by_id(self, piece_id, chessboard):
        for position, piece in chessboard.save_chars_and_positions.items():
            if piece and piece.piece_id == piece_id:
                return position
        return None

    def find_position_of_current_char(self, chessboard):
        self.position = self.find_position_of_char_by_id(self.piece_id, chessboard)

    @abstractmethod
    def possible_movements(self, chessboard):
        pass
