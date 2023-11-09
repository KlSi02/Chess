from src.model.baseplayer.player import Player


class PlayerController:

    def __init__(self, team):
        self.player = Player(team)

    def check_alive_chars(self, chessboard):
        for pos, char in chessboard.save_chars_and_positions.items():
            if str(char).startswith("white"):
                self.player.alive_chars[pos] = char

    def game_over(self):
        if self.player.set_checkmate is True:
            pass  # ...

    def get_threatened_fields(self):
        for char in self.player.alive_chars:
            char.possible_movements()
            self.player.threatened_fields[char] = char.possible_moves

    def update_threatened_fields(self):
        for pos, char in self.player.moved_chars.items():
            char.possible_movements()
            self.player.threatened_fields[char] = char.possible_moves
            del self.player.moved_chars[pos]

    def promotion_pawn(self):
        for pos in self.alive_chars.keys():
            if pos[1] == "8":
                if chessboard.save_chars_and_positions[pos] == "white_pawn":
                    self.pawn_promotion = True
                    #  pawn.promotion() ...

            else:
                pass

    def rochade(self):
        pass


