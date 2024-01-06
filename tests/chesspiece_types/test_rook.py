import pytest
from src.model.chesspiece_types.rook import Rook
from src.model.chesspiece_types.pawn import Pawn
from src.model.chessboard import Chessboard
from src.utils.helpers import PieceTeam


@pytest.fixture
def setup_rook():
    black_rook = Rook(PieceTeam.BLACK)
    return black_rook


white_pawn1 = Pawn(PieceTeam.WHITE)
white_pawn2 = Pawn(PieceTeam.WHITE)


def test_possible_movements(setup_rook):
    chessboard = Chessboard()
    chessboard.board_state["E5"] = setup_rook
    del chessboard.board_state["E7"]
    chessboard.board_state["E8"] = white_pawn1
    del chessboard.board_state["E2"]
    chessboard.board_state["E1"] = white_pawn2

    possible_moves = setup_rook.possible_movements(chessboard)
    assert possible_moves == [('F', 5),
                              ('G', 5),
                              ('H', 5),
                              ('I', 5),
                              ('J', 5),
                              ('K', 5),
                              ('L', 5),
                              ('M', 5),
                              ('D', 5),
                              ('C', 5),
                              ('B', 5),
                              ('A', 5),
                              ('@', 5),
                              ('?', 5),
                              ('>', 5),
                              ('=', 5),
                              ('E', 6),
                              ('E', 7),
                              ('E', 8),
                              ('E', 4),
                              ('E', 3),
                              ('E', 2),
                              ('E', 1)]
