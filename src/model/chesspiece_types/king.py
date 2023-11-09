from src.model.baseplayer.chesspiece import ChessPiece


class King(ChessPiece):

    def __init__(self, team):
        super().__init__(team)

    def possible_movements(self, chessboard):
        position = self.find_position_of_current_char(chessboard)
        alpha, numb = position
        numb = int(numb)

        self.possible_moves_without_knowing_board = [
            (alpha, numb + 1),  # 1 step forward
            (chr(ord(alpha) + 1), numb + 1),  # 1 step forward, right
            (chr(ord(alpha) + 1), numb),  # 1 step right
            (chr(ord(alpha) + 1), numb - 1),  # 1 step right, down
            (alpha, numb - 1),  # 1 step down
            (chr(ord(alpha) - 1), numb - 1),   # 1 step left, down
            (chr(ord(alpha) - 1), numb),  # 1 step left
            (chr(ord(alpha) - 1), numb + 1)   # 1 step left, up
        ]

        return self.possible_moves_without_knowing_board

    