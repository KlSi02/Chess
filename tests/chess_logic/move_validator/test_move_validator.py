import pytest
from src.model.chessboard import Chessboard
from src.model.chesspiece_types.king import King
from src.model.chesspiece_types.rook import Rook
from src.model.baseplayer.player import Player
from src.utils.helpers import PieceTeam
from controller.move_validator import MoveValidator


@pytest.fixture
def setup():
    chessboard = Chessboard()
    attacker = Player(PieceTeam.WHITE)
    defender = Player(PieceTeam.BLACK)
    move_validator = MoveValidator(chessboard, attacker, defender)

    return chessboard, attacker, defender, move_validator


def test_give_king_pos(setup):
    chessboard, attacker, defender, move_validator = setup

    move_validator.give_king_pos()

    # Verify that the kings' positions are correctly assigned
    assert attacker.king_position == "E1"
    assert defender.king_position == "E8"
    print(f"White King's position: {attacker.king_position}")
    print(f"Black King's position: {defender.king_position}")


def test_get_alive_pieces(setup):
    chessboard, attacker, defender, move_validator = setup
    move_validator.get_alive_pieces()

    assert len(attacker.alive_pieces) == 16
    assert len(defender.alive_pieces) == 16


def test_filter_king_moves(setup):
    chessboard, attacker, defender, move_validator = setup
    chessboard.board_state["E1"] = None

    white_king = King(PieceTeam.WHITE)
    white_king.position = "E5"
    attacker.king_position = "E5"
    black_rook = Rook(PieceTeam.BLACK)

    chessboard.board_state["E5"] = white_king
    white_king.possible_moves.update(["E4", "E6", "D4", "D5", "D6", "F4", "F5", "F6"])

    chessboard.board_state["A6"] = black_rook
    black_rook.possible_moves.update(["A7", "A6", "A5", "A4", "A3", "B6", "C6", "D6", "E6", "F6", "G6", "H6"])

    defender.coverage_areas = {
        black_rook: black_rook.possible_moves
    }

    move_validator.filter_king_moves()

    assert white_king.possible_moves == {"E4", "D4", "D5", "F4", "F5"}
