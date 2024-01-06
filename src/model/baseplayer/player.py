from src.model.chesspiece_types.pawn import Pawn


class Player:

    def __init__(self, team):

        self.team = team
        self.captured_pieces = []
        self.alive_pieces = []
        self.set_check = {}
        self.in_check = False
        self.in_checkmate = False
        self.coverage_areas = {}
        self.king_position = None

    def get_alive_pieces(self, chessboard):
        for pos, piece in chessboard.board_state.items():
            if piece and piece.team == self.team:
                self.alive_pieces.append(piece)

    def reset(self):
        self.captured_pieces.clear()
        self.alive_pieces.clear()
        self.set_check.clear()
        self.in_check = False
        self.in_checkmate = False
        self.coverage_areas.clear()
        self.king_position = None

