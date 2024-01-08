from src.utils.helpers import PieceTeam

from src.model.chesspiece_types.rook import Rook
from src.model.chesspiece_types.knight import Knight
from src.model.chesspiece_types.bishop import Bishop
from src.model.chesspiece_types.queen import Queen
from src.model.chesspiece_types.king import King
from src.model.chesspiece_types.pawn import Pawn


def create_empty_board():
    empty_board = {}
    for row in range(1, 9):
        for col in range(65, 73):
            empty_board[f"{chr(col)}{row}"] = None
    return empty_board


class Chessboard:

    def __init__(self):
        self.board_state = create_empty_board()
        self.setup_board()
        self.last_moves = []

    def create_pieces_for_team(self, team):
        return {
            "rooks": [Rook(team), Rook(team)],
            "knights": [Knight(team), Knight(team)],
            "bishops": [Bishop(team), Bishop(team)],
            "queen": [Queen(team)],
            "king": [King(team)],
            "pawns": [Pawn(team) for _ in range(8)]
        }

    def get_initial_positions_for_team(self, team, pieces):
        if team == "white":
            self.board_state["A1"] = pieces["rooks"][0]
            self.board_state["B1"] = pieces["knights"][0]
            self.board_state["C1"] = pieces["bishops"][0]
            self.board_state["D1"] = pieces["queen"][0]
            self.board_state["E1"] = pieces["king"][0]
            self.board_state["F1"] = pieces["bishops"][1]
            self.board_state["G1"] = pieces["knights"][1]
            self.board_state["H1"] = pieces["rooks"][1]
            for i in range(8):
                self.board_state[f"{chr(65 + i)}2"] = pieces["pawns"][i]
        else:
            self.board_state["A8"] = pieces["rooks"][0]
            self.board_state["B8"] = pieces["knights"][0]
            self.board_state["C8"] = pieces["bishops"][0]
            self.board_state["D8"] = pieces["queen"][0]
            self.board_state["E8"] = pieces["king"][0]
            self.board_state["F8"] = pieces["bishops"][1]
            self.board_state["G8"] = pieces["knights"][1]
            self.board_state["H8"] = pieces["rooks"][1]
            for i in range(8):
                self.board_state[f"{chr(65 + i)}7"] = pieces["pawns"][i]

    def setup_board(self):
        white_pieces = self.create_pieces_for_team(PieceTeam.WHITE)
        black_pieces = self.create_pieces_for_team(PieceTeam.BLACK)

        self.get_initial_positions_for_team("white", white_pieces)
        self.get_initial_positions_for_team("black", black_pieces)

    def reset(self):
        self.last_moves.clear()
        self.board_state.clear()
        self.board_state = create_empty_board()
        self.setup_board()


