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
    assert len(chessboard.board_state) == 64
    assert chessboard.save_all_steps == {}


def test_if_pawn_on_board(chessboard):
    target_char = chessboard.board_state.get("H2")
    assert isinstance(target_char, Pawn)
    assert target_char.team == PieceTeam.WHITE

    target_char = chessboard.board_state.get("A7")
    assert isinstance(target_char, Pawn)
    assert target_char.team == PieceTeam.BLACK


def test_if_king_on_board(chessboard):
    target_char = chessboard.board_state.get("E8")
    assert isinstance(target_char, King)
    assert target_char.team == PieceTeam.BLACK

    target_char = chessboard.board_state.get("E1")
    assert isinstance(target_char, King)
    assert target_char.team == PieceTeam.WHITE


def test_if_queen_on_board(chessboard):
    target_char = chessboard.board_state.get("D1")
    assert isinstance(target_char, Queen)
    assert target_char.team == PieceTeam.WHITE

    target_char = chessboard.board_state.get("D8")
    assert isinstance(target_char, Queen)
    assert target_char.team == PieceTeam.BLACK
