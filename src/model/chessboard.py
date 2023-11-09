from src.utils.helpers import PieceTeam

from src.model.chesspiece_types.rook import Rook
from src.model.chesspiece_types.knight import Knight
from src.model.chesspiece_types.bishop import Bishop
from src.model.chesspiece_types.queen import Queen
from src.model.chesspiece_types.king import King
from src.model.chesspiece_types.pawn import Pawn

white_rook1 = Rook(PieceTeam.WHITE)
white_rook2 = Rook(PieceTeam.WHITE)

black_rook1 = Rook(PieceTeam.BLACK)
black_rook2 = Rook(PieceTeam.BLACK)

white_knight1 = Knight(PieceTeam.WHITE)
white_knight2 = Knight(PieceTeam.WHITE)

black_knight1 = Knight(PieceTeam.BLACK)
black_knight2 = Knight(PieceTeam.BLACK)

white_bishop1 = Bishop(PieceTeam.WHITE)
white_bishop2 = Bishop(PieceTeam.WHITE)

black_bishop1 = Bishop(PieceTeam.BLACK)
black_bishop2 = Bishop(PieceTeam.BLACK)

white_queen = Queen(PieceTeam.WHITE)
black_queen = Queen(PieceTeam.BLACK)

white_king = King(PieceTeam.WHITE)
black_king = King(PieceTeam.BLACK)

white_pawn1 = Pawn(PieceTeam.WHITE)
white_pawn2 = Pawn(PieceTeam.WHITE)
white_pawn3 = Pawn(PieceTeam.WHITE)
white_pawn4 = Pawn(PieceTeam.WHITE)
white_pawn5 = Pawn(PieceTeam.WHITE)
white_pawn6 = Pawn(PieceTeam.WHITE)
white_pawn7 = Pawn(PieceTeam.WHITE)
white_pawn8 = Pawn(PieceTeam.WHITE)

black_pawn1 = Pawn(PieceTeam.BLACK)
black_pawn2 = Pawn(PieceTeam.BLACK)
black_pawn3 = Pawn(PieceTeam.BLACK)
black_pawn4 = Pawn(PieceTeam.BLACK)
black_pawn5 = Pawn(PieceTeam.BLACK)
black_pawn6 = Pawn(PieceTeam.BLACK)
black_pawn7 = Pawn(PieceTeam.BLACK)
black_pawn8 = Pawn(PieceTeam.BLACK)


class Chessboard:

    def __init__(self):
        self.save_chars_and_positions = {"A1": white_rook1, "B1": white_knight1, "C1": white_bishop1,
                                         "D1": white_queen,
                                         "E1": white_king, "F1": white_bishop2, "G1": white_knight2,
                                         "H1": white_rook2,

                                         "A2": white_pawn1, "B2": white_pawn2, "C2": white_pawn3, "D2": white_pawn4,
                                         "E2": white_pawn5, "F2": white_pawn6, "G2": white_pawn7, "H2": white_pawn8,

                                         "A3": None, "B3": None, "C3": None, "D3": None,
                                         "E3": None, "F3": None, "G3": None, "H3": None,

                                         "A4": None, "B4": None, "C4": None, "D4": None,
                                         "E4": None, "F4": None, "G4": None, "H4": None,

                                         "A5": None, "B5": None, "C5": None, "D5": None,
                                         "E5": None, "F5": None, "G5": None, "H5": None,

                                         "A6": None, "B6": None, "C6": None, "D6": None,
                                         "E6": None, "F6": None, "G6": None, "H6": None,

                                         "A7": black_pawn1, "B7": black_pawn2, "C7": black_pawn3, "D7": black_pawn4,
                                         "E7": black_pawn5, "F7": black_pawn6, "G7": black_pawn7, "H7": black_pawn8,

                                         "A8": black_rook1, "B8": black_knight1, "C8": black_bishop1,
                                         "D8": black_queen,
                                         "E8": black_king, "F8": black_bishop2, "G8": black_knight2,
                                         "H8": black_rook2,
                                         }

        self.save_all_steps = {}

