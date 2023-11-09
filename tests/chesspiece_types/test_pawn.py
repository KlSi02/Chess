import pytest
from engine.engine_character_rules.e_black_pawn import black_pawn, player_black
from engine.engine_chessboard.e_chessboard import EngineChessboard as Chessboard



@pytest.fixture
def setup_black_pawn():
    chessboard = Chessboard()
    pawn = black_pawn()
    return player_black, chessboard, pawn


def test_check_team(setup_black_pawn):  # passed
    player_black, chessboard, pawn = setup_black_pawn
    pawn.check_team()
    assert pawn.team == "black"


def test_check_dash_movement(setup_black_pawn):  # passed
    player_black, chessboard, pawn = setup_black_pawn
    pawn.position = ('A', 7)
    pawn.check_dash_movement('B', 6)
    assert pawn.possible_moves == ["B6"]
    assert player_black.set_checkmate is True


def test_possible_movements(setup_black_pawn):  # passed
    player_black, chessboard, pawn = setup_black_pawn
    pawn.position = "A7"
    pawn.first_turn = True
    pawn.possible_movements()
    assert pawn.possible_moves == ["B6", "A6", "A5"]
