
class Player:

    def __init__(self, team):

        self.team = team
        self.captured_chars = []
        self.lost = False
        self.pawn_promotion = False
        self.alive_chars = {}
        self.set_checkmate = False
        self.set_check = {}
        self.threatened_fields = {}
        self.moved_chars = {}
        self.actual_king_position = None
        self.is_rochade_possible = False

    def check_position_of_king(self):
        for square, char in self.alive_chars.items():
            if char == "white_king":
                self.actual_king_position = square
