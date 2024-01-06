import pytest
from src.model.chesspiece_types.pawn import Pawn
from src.model.chessboard import Chessboard
from utils.helpers import PieceTeam


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

    possible_moves = pawn.check_dash_movement(chessboard, "A", 2)
    assert ("B", "3") in possible_moves


def test_possible_movements(pawn):
    chessboard = Chessboard()
    chessboard.board_state["A2"] = pawn

    possible_moves = pawn.possible_movements(chessboard)

    assert ("A", 3) in possible_moves
    assert ("A", 4) in possible_moves
