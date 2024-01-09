import pytest
from src.model.chesspiece_types.pawn import Pawn
from src.model.chessboard import Chessboard
from src.utils.helpers import PieceTeam


@pytest.fixture
def pawn():
    pawn = Pawn(PieceTeam.WHITE)
    return pawn


def test_pawn_initialization(pawn):
    assert pawn.team == PieceTeam.WHITE
    assert pawn.first_turn is True


def test_check_dash_movement(pawn):
    chessboard = Chessboard()
    chessboard.board_state["B3"] = "black"
    chessboard.board_state["C3"] = "black"
    chessboard.board_state["A2"] = pawn


