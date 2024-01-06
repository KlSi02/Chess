import pytest
from unittest.mock import MagicMock
from src.model.chesspiece_types.pawn import Pawn
from src.utils.helpers import PieceTeam


@pytest.fixture
def chess_piece():
    return Pawn(PieceTeam.WHITE)


def test_chess_piece_init(chess_piece):
    assert chess_piece.position is None
    assert chess_piece.possible_moves_on_current_board == []
    assert chess_piece.team == PieceTeam.WHITE
    assert chess_piece.possible_moves_without_knowing_board == []
    assert isinstance(chess_piece.piece_id, str)


def test_find_position_of_char_by_id(chess_piece):
    chessboard = MagicMock()
    chessboard.save_chars_and_positions = {
        "A1": None,
        "B1": chess_piece,
        "C1": None
    }
    result = chess_piece.find_position_of_piece_by_id(chess_piece.piece_id, chessboard)
    assert result == "B1"


def test_find_position_of_current_char(chess_piece):
    chessboard = MagicMock()
    chessboard.save_chars_and_positions = {
        "A1": None,
        "B1": chess_piece,
        "C1": None
    }
    chess_piece.find_position_of_piece_by_id = MagicMock(return_value="B1")
    chess_piece.find_position_of_current_piece(chessboard)
    assert chess_piece.position == "B1"
