import pytest
from src.model.chesspiece_types.queen import Queen
from src.model.chesspiece_types.pawn import Pawn
from src.model.chessboard import Chessboard
from src.utils.helpers import PieceTeam


@pytest.fixture
def setup_queen():
    black_queen = Queen(PieceTeam.BLACK)
    return black_queen


white_pawn1 = Pawn(PieceTeam.WHITE)
white_pawn2 = Pawn(PieceTeam.WHITE)
white_pawn3 = Pawn(PieceTeam.WHITE)
white_pawn4 = Pawn(PieceTeam.WHITE)


def test_possible_movements(setup_queen):
    chessboard = Chessboard()
    chessboard.board_state["E5"] = setup_queen
    chessboard.board_state["A5"] = white_pawn3
    chessboard.board_state["H5"] = white_pawn4
    del chessboard.board_state["E7"]
    chessboard.board_state["E8"] = white_pawn1
    del chessboard.board_state["E2"]
    chessboard.board_state["E1"] = white_pawn2

    possible_moves = setup_queen.possible_movements(chessboard)
    assert possible_moves == [('F', 6),
                              ('G', 7),
                              ('F', 4),
                              ('G', 3),
                              ('H', 2),
                              ('D', 4),
                              ('C', 3),
                              ('B', 2),
                              ('D', 6),
                              ('C', 7),
                              ('F', 5),
                              ('G', 5),
                              ('H', 5),
                              ('D', 5),
                              ('C', 5),
                              ('B', 5),
                              ('A', 5),
                              ('E', 6),
                              ('E', 7),
                              ('E', 8),
                              ('E', 4),
                              ('E', 3),
                              ('E', 2),
                              ('E', 1)]
