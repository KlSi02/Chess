from src.model.baseplayer.chesspiece import ChessPiece


class Knight(ChessPiece):

    def __init__(self, team):
        super().__init__(team)

    def possible_movements(self, chessboard):
        self.find_position_of_current_char(chessboard)
        alpha, numb = self.position
        numb = int(numb)

        self.possible_moves_without_knowing_board = []

        self.possible_moves_without_knowing_board = [
            (chr(ord(alpha) + 1), numb + 2),  # 2 steps forward, 1 step right
            (chr(ord(alpha) + 2), numb + 1),  # 1 step forward, 2 steps right
            (chr(ord(alpha) + 2), numb - 1),  # 1 step backward, 2 steps right
            (chr(ord(alpha) + 1), numb - 2),  # 2 steps backward, 1 step right
            (chr(ord(alpha) - 1), numb - 2),  # 2 steps backward, 1 step left
            (chr(ord(alpha) - 2), numb - 1),  # 1 step backward, 2 steps left
            (chr(ord(alpha) - 2), numb + 1),  # 1 step forward, 2 steps left
            (chr(ord(alpha) - 1), numb + 2)   # 2 steps forward, 1 step left
        ]

        return self.possible_moves_without_knowing_board
