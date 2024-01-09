import pytest
from src.model.chesspiece_types.king import King
from src.model.chessboard import Chessboard
from src.utils.helpers import PieceTeam


@pytest.fixture
def king():
    black_king = King(PieceTeam.BLACK)
    return black_king


def test_possible_movements(king):
    chessboard = Chessboard()
    chessboard.board_state["E5"] = king

    possible_moves = king.possible_movements(chessboard)
    assert possible_moves == [('E', 6), ('F', 6), ('F', 5), ('F', 4), ('E', 4), ('D', 4), ('D', 5), ('D', 6)]
