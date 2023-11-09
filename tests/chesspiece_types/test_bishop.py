import pytest
from src.model.chesspiece_types.bishop import Bishop
from src.model.chesspiece_types.pawn import Pawn
from src.model.chessboard import Chessboard
from src.utils.helpers import PieceTeam


@pytest.fixture
def setup_bishop():
    black_bishop = Bishop(PieceTeam.BLACK)
    return black_bishop


white_pawn1 = Pawn(PieceTeam.WHITE)
white_pawn2 = Pawn(PieceTeam.WHITE)
white_pawn3 = Pawn(PieceTeam.WHITE)
white_pawn4 = Pawn(PieceTeam.WHITE)


def test_possible_movements(setup_bishop):
    chessboard = Chessboard()
    chessboard.save_chars_and_positions["E5"] = setup_bishop
    chessboard.save_chars_and_positions["A5"] = white_pawn3
    chessboard.save_chars_and_positions["H5"] = white_pawn4
    del chessboard.save_chars_and_positions["E7"]
    chessboard.save_chars_and_positions["E8"] = white_pawn1
    del chessboard.save_chars_and_positions["E2"]
    chessboard.save_chars_and_positions["E1"] = white_pawn2

    possible_moves = setup_bishop.possible_movements(chessboard)
    assert possible_moves == [('F', 6),
                              ('G', 7),
                              ('F', 4),
                              ('G', 3),
                              ('H', 2),
                              ('D', 4),
                              ('C', 3),
                              ('B', 2),
                              ('D', 6),
                              ('C', 7)]
