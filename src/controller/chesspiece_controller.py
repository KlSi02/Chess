from src.model.baseplayer.chesspiece import ChessPiece


class ChessPieceController:

    def __init__(self, team):
        self.chess_piece = ChessPiece(team)

    def update_possible_moves(self, chessboard, alpha, numb):
        checked_position = (alpha + str(numb))
        if checked_position not in chessboard.save_chars_and_positions.keys():
            pass

        if chessboard.save_chars_and_positions[checked_position] is None:
            self.chess_piece.possible_moves.append(checked_position)

        else:
            target_char = chessboard.save_chars_and_positions.get(checked_position)

            if self.chess_piece.team != target_char.team:
                self.chess_piece.possible_moves.append(checked_position)
                if target_char == "King":

                    player_black.set_checkmate = True if check_team_of_class == "black" else False
                    player_white.set_checkmate = True if check_team_of_class == "white" else False

        return True
