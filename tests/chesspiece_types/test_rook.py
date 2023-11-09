import pytest
from engine.engine_chessboard.e_chessboard import EngineChessboard as Chessboard
from engine.engine_character_rules.e_black_rook import black_rook
from engine.engine_baseplayer.e_baseplayer_player import player_black


@pytest.fixture
def setup_black_rook():
    chessboard = Chessboard()
    rook = black_rook()
    return chessboard, rook


def test_black_rook_attributes(setup_black_rook):
    chessboard, rook = setup_black_rook
    assert hasattr(rook, "is_left_rochade_possible")
    assert hasattr(rook, "is_right_rochade_possible")
    assert hasattr(rook, "possible_movements_list")


def test_is_rochade_possible(setup_black_rook):
    chessboard, rook = setup_black_rook
    assert rook.is_rochade_possible is True  # pos black_king = E8, pos black_rook = H8, passed 100%
    #  pos black_king = E8, pos black_rook = A8, passed 100%


def test_player_set_checkmate(setup_black_rook):
    chessboard, rook = setup_black_rook
    rook.position = "F4"
    rook.possible_movements()
    assert player_black.set_checkmate is True


def test_possible_movements(setup_black_rook):  # rook position is F4
    chessboard, rook = setup_black_rook
    rook.possible_movements()
    assert len(rook.possible_movements_list) == 11
    # list output: [('F', 5), ('F', 6), ('F', 3), ('F', 2), ('E', 4), ('D', 4), ('C', 4), ('B', 4), ('A', 4), ('G',
    # 4), ('H', 4)]
    assert all(1 <= move[1] <= 8 and "A" <= move[0] <= "H" for move in rook.possible_movements_list)
    assert rook.possible_moves == ['F5', 'F6', 'F3', 'F2', 'E4', 'D4', 'C4', 'B4', 'A4', 'G4', 'H4']
    # list output: ['F5', 'F6', 'F3', 'F2', 'E4', 'D4', 'C4', 'B4', 'A4', 'G4', 'H4']
