from src.model.baseplayer.chesspiece import ChessPiece
from utils.helpers import PieceTeam


class Pawn(ChessPiece):

    def __init__(self, team):
        super().__init__(team)

        self.first_turn = True

    def check_dash_movement(self, chessboard, alpha, numb):

        new_alpha = chr(ord(alpha) + 1)
        new_numb = numb + 1
        check_position_right = new_alpha + str(new_numb)

        new_alpha1 = chr(ord(alpha) - 1)
        new_numb1 = numb + 1
        check_position_left = new_alpha1 + str(new_numb1)

        possible_movements = [check_position_right, check_position_left]

        for dash in possible_movements:
            if dash not in chessboard.save_chars_and_positions.keys():
                return False

            target_char = chessboard.save_chars_and_positions.get(dash)

            if target_char is not None:
                if (target_char.startswith("white") and self.team == PieceTeam.BLACK) or \
                        (target_char.startswith("black") and self.team == PieceTeam.WHITE):
                    alpha, numb = dash
                    self.possible_moves_without_knowing_board.append((alpha, numb))
            else:
                return False
        return True

    def possible_movements(self, chessboard):
        self.find_position_of_current_char(chessboard)
        alpha, numb = self.position
        numb = int(numb)

        self.possible_moves_without_knowing_board = []

        if self.team == PieceTeam.BLACK:
            self.possible_moves_without_knowing_board.append((alpha, numb - 1))
            if self.first_turn is True:
                self.possible_moves_without_knowing_board.append((alpha, numb - 2))
            else:
                pass
        else:
            self.possible_moves_without_knowing_board.append((alpha, numb + 1))
            if self.first_turn is True:
                self.possible_moves_without_knowing_board.append((alpha, numb + 2))
            else:
                pass

        self.check_dash_movement(chessboard, alpha, numb)

        return self.possible_moves_without_knowing_board
