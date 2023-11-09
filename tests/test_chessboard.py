import pytest
from src.model.chessboard import Chessboard
from src.model.chesspiece_types.pawn import Pawn
from src.model.chesspiece_types.king import King
from src.model.chesspiece_types.queen import Queen
from src.utils.helpers import PieceTeam

white_pawn8 = Pawn(PieceTeam.WHITE)


@pytest.fixture
def chessboard():
    return Chessboard()


def test_initialization(chessboard):
    assert len(chessboard.save_chars_and_positions) == 64
    assert chessboard.save_all_steps == {}


def test_if_pawn_on_board(chessboard):
    target_char = chessboard.save_chars_and_positions.get("H2")
    assert isinstance(target_char, Pawn)
    assert target_char.team == PieceTeam.WHITE

    target_char = chessboard.save_chars_and_positions.get("A7")
    assert isinstance(target_char, Pawn)
    assert target_char.team == PieceTeam.BLACK


def test_if_king_on_board(chessboard):
    target_char = chessboard.save_chars_and_positions.get("E8")
    assert isinstance(target_char, King)
    assert target_char.team == PieceTeam.BLACK

    target_char = chessboard.save_chars_and_positions.get("E1")
    assert isinstance(target_char, King)
    assert target_char.team == PieceTeam.WHITE


def test_if_queen_on_board(chessboard):
    target_char = chessboard.save_chars_and_positions.get("D1")
    assert isinstance(target_char, Queen)
    assert target_char.team == PieceTeam.WHITE

    target_char = chessboard.save_chars_and_positions.get("D8")
    assert isinstance(target_char, Queen)
    assert target_char.team == PieceTeam.BLACK
