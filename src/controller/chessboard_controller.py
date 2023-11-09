from src.model.chessboard import Chessboard
from view.chessboard import Chessboard
from src.utils.helpers import PieceTeam


class ChessboardController:

    def __init__(self):
        self.chessboard = Chessboard()
        self.ui_chessboard = Chessboard()
        self.current_player = None

    def make_move(self, player, selected_char, old_pos, new_pos):
        if (selected_char not in self.chessboard.save_chars_and_positions.values()) or \
                (old_pos not in self.chessboard.save_chars_and_positions.keys()) or \
                (new_pos not in self.chessboard.save_chars_and_positions.keys()):
            return

        for position, char in self.chessboard.save_chars_and_positions.items():
            if selected_char == char and old_pos == position:
                if self.chessboard.save_chars_and_positions[new_pos] is not None:
                    target_char = self.chessboard.save_chars_and_positions.get(new_pos)
                    if (target_char.startswith("white") and char.team == PieceTeam.BLACK) or \
                            (target_char.startswith("black") and char.team == PieceTeam.WHITE):
                        player.captured_chars.append(target_char)
                        del player.alive_chars[new_pos]
                    break

                self.chessboard.save_chars_and_positions[new_pos] = selected_char
                self.chessboard.save_all_steps[new_pos] = selected_char

                if (char.startswith("white") and player.team == PieceTeam.WHITE) or \
                        (char.startswith("black") and player.team == PieceTeam.BLACK):
                    player.moved_chars[new_pos] = selected_char
                    del player.threatened_fields[old_pos]

