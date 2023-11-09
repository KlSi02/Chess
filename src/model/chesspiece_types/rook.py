from src.model.baseplayer.chesspiece import ChessPiece
from src.utils.helpers import CommonMovements


class Rook(ChessPiece, CommonMovements):

    def __init__(self, team):
        super().__init__(team)

    def possible_movements(self, chessboard):
        self.find_position_of_current_char(chessboard)
        alpha, numb = self.position
        numb = int(numb)

        self.possible_moves_without_knowing_board = []

        self.check_and_append_moves(self, chessboard, alpha, numb, 1, 0)
        self.check_and_append_moves(self, chessboard, alpha, numb, -1, 0)
        self.check_and_append_moves(self, chessboard, alpha, numb, 0, 1)
        self.check_and_append_moves(self, chessboard, alpha, numb, 0, -1)

        return self.possible_moves_without_knowing_board

