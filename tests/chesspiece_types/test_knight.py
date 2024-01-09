import pytest
from src.model.chesspiece_types.knight import Knight
from src.model.chessboard import Chessboard
from src.utils.helpers import PieceTeam


@pytest.fixture
def knight():
    black_knight = Knight(PieceTeam.BLACK)
    return black_knight


def test_possible_movements(knight):
    chessboard = Chessboard()
    chessboard.board_state["E5"] = knight

    possible_moves = knight.possible_movements(chessboard)
    assert possible_moves == [('F', 7), ('G', 6), ('G', 4), ('F', 3), ('D', 3), ('C', 4), ('C', 6), ('D', 7)]
