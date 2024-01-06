from src.utils.helpers import CommonMovements
from src.model.baseplayer.chesspiece import ChessPiece


class Queen(ChessPiece, CommonMovements):

    def __init__(self, team):
        super().__init__(team)

    def possible_movements(self, chessboard):
        self.find_position_of_current_piece(chessboard)
        if self.position:
            alpha, numb = self.position
            numb = int(numb)

            self.possible_moves_without_knowing_board = []

            self.check_and_append_moves(self, chessboard, alpha, numb, 1, 1)  # step up, right
            self.check_and_append_moves(self, chessboard, alpha, numb, 1, -1)   # step down, right
            self.check_and_append_moves(self, chessboard, alpha, numb, -1, -1)  # step down, left
            self.check_and_append_moves(self, chessboard, alpha, numb, -1, 1)   # step up, left
            self.check_and_append_moves(self, chessboard, alpha, numb, 1, 0)    # step right
            self.check_and_append_moves(self, chessboard, alpha, numb, -1, 0)   # step left
            self.check_and_append_moves(self, chessboard, alpha, numb, 0, 1)    # step up
            self.check_and_append_moves(self, chessboard, alpha, numb, 0, -1)   # step down

            return self.possible_moves_without_knowing_board

