import pytest

from src.model.baseplayer.player import Player
from src.model.chesspiece_types.king import King
from src.model.chesspiece_types.rook import Rook
from src.model.chesspiece_types.queen import Queen
from src.model.chesspiece_types.pawn import Pawn
from src.model.chesspiece_types.bishop import Bishop
from src.utils.helpers import PieceTeam
from controller.check_handling.move_validator_king_in_check import is_double_check, only_king_can_move, filter_only_safe_moves, \
    filter_moves_excluding_danger_line, filter_attacking_piece, update_possible_moves_of_king


@pytest.fixture
def setup_defender():
    # Fixture to set up a defender with two rooks and a king
    defender = Player(PieceTeam.WHITE)
    defender_rook1 = Rook(PieceTeam.WHITE)
    defender_rook1.possible_moves.add("H4")
    defender_rook2 = Rook(PieceTeam.WHITE)
    defender_rook2.possible_moves.add("E3")
    defender_king = King(PieceTeam.WHITE)
    defender_king.possible_moves.add("E2")
    defender.alive_pieces.extend([defender_king, defender_rook1, defender_rook2])
    return defender, defender_king, defender_rook1, defender_rook2


def test_is_double_check():
    # Testing whether the is_double_check function correctly identifies a double check scenario
    attacker_rook1 = Rook(PieceTeam.WHITE)
    attacker_rook2 = Rook(PieceTeam.WHITE)
    attacker_check_moves = {attacker_rook1: "", attacker_rook2: ""}
    assert is_double_check(attacker_check_moves) is True

    del attacker_check_moves[attacker_rook2]
    assert is_double_check(attacker_check_moves) is False


def test_only_king_can_move(setup_defender):
    # Testing that only the king is allowed to move when only_king_can_move is called
    defender, defender_king, defender_rook1, defender_rook2 = setup_defender

    assert "H4" in defender_rook1.possible_moves
    assert "E3" in defender_rook2.possible_moves
    assert "E2" in defender_king.possible_moves

    only_king_can_move(defender)

    assert defender_rook1.possible_moves == set()
    assert defender_rook2.possible_moves == set()
    assert defender_king.possible_moves == {"E2"}


def test_filter_only_safe_moves():
    # Testing the filter_only_safe_moves function to ensure it correctly filters out unsafe moves for the king
    defender_king = King(PieceTeam.BLACK)
    king_moves_to_add = ["C2", "D2", "E1", "C1"]
    defender_king.possible_moves.update(king_moves_to_add)

    attacker_rook = Rook(PieceTeam.WHITE)
    rook_moves_to_add = ["C2", "D2", "E1", "F2"]
    attacker_rook.possible_moves.update(rook_moves_to_add)
    attacker_check_moves = {attacker_rook: attacker_rook.possible_moves}

    filter_only_safe_moves(defender_king, attacker_check_moves)

    assert len(defender_king.possible_moves) == 1
    assert "C1" in defender_king.possible_moves


def test_filter_moves_excluding_danger_line_horizontally():
    # Testing filter_moves_excluding_danger_line function for a horizontal attack
    defender_king = King(PieceTeam.BLACK)
    defender_king.position = "F4"
    moves_of_king = ["F3", "E3", "E4", "E5", "F5", "G5", "G4", "G3"]
    defender_king.possible_moves.update(moves_of_king)

    attacker_rook = Rook(PieceTeam.WHITE)
    attacker_rook.position = "B4"
    moves_of_rook = ["C4", "D4", "E4", "F4"]
    attacker_rook.possible_moves.update(moves_of_rook)
    attacker_check_moves = {attacker_rook: attacker_rook.possible_moves}

    filter_moves_excluding_danger_line(defender_king, attacker_check_moves, attacker_rook)
    assert defender_king.possible_moves == {'E3', 'G3', 'E5', 'F5', 'G5', 'F3'}
    for pos in ["G4", "H4"]:
        assert pos in attacker_rook.possible_moves


def test_filter_moves_excluding_danger_line_vertically():
    # Testing filter_moves_excluding_danger_line function for a vertical attack
    defender_king = King(PieceTeam.BLACK)
    defender_king.position = "F4"
    moves_of_king = ["F3", "E3", "E4", "E5", "F5", "G5", "G4", "G3"]
    defender_king.possible_moves.update(moves_of_king)

    attacker_rook = Rook(PieceTeam.WHITE)
    attacker_rook.position = "F6"
    moves_of_rook = ["F5", "F4"]
    attacker_rook.possible_moves.update(moves_of_rook)
    attacker_check_moves = {attacker_rook: attacker_rook.possible_moves}

    filter_moves_excluding_danger_line(defender_king, attacker_check_moves, attacker_rook)
    assert defender_king.possible_moves == {"E3", "E4", "E5", "G5", "G4", "G3"}
    for pos in ["F3", "F2", "F1"]:
        assert pos in attacker_rook.possible_moves


def test_filter_moves_excluding_danger_line_diagonally():
    # Testing filter_moves_excluding_danger_line function for a diagonal attack
    defender_king = King(PieceTeam.BLACK)
    defender_king.position = "F4"
    moves_of_king = ["F3", "E3", "E4", "E5", "F5", "G5", "G4", "G3"]
    defender_king.possible_moves.update(moves_of_king)

    attacker_queen = Queen(PieceTeam.WHITE)
    attacker_queen.position = "E5"
    moves_of_queen = ["F4", "G3", "H2", "E3", "E4", "E2", "E1", "F5", "G5", "H5"]
    attacker_queen.possible_moves.update(moves_of_queen)
    attacker_check_moves = {attacker_queen: attacker_queen.possible_moves}

    filter_moves_excluding_danger_line(defender_king, attacker_check_moves, attacker_queen)
    assert defender_king.possible_moves == {"E5", "F3", "G4"}
    for pos in ["G3", "H2"]:
        assert pos in attacker_queen.possible_moves


def test_filter_attacking_piece():
    # Testing filter_attacking_piece to ensure it correctly filters moves based on the type of attacking piece
    defender_king = King(PieceTeam.BLACK)
    defender_king.position = "E2"
    moves_of_king = ["E1", "E3", "D2", "D1", "D3", "F3", "F2", "F1"]
    defender_king.possible_moves.update(moves_of_king)

    attacker_queen = Queen(PieceTeam.WHITE)
    attacker_queen.position = "E6"
    moves_of_queen = ["E5", "E4", "E3", "E2"]
    attacker_queen.possible_moves.update(moves_of_queen)

    attacker_check_moves = {attacker_queen: attacker_queen.possible_moves}

    filter_attacking_piece(defender_king, attacker_check_moves)

    assert "E1" not in defender_king.possible_moves
    assert "E1" in attacker_queen.possible_moves

    del attacker_check_moves[attacker_queen]

    attacker_pawn = Pawn(PieceTeam.WHITE)
    attacker_pawn.position = "F3"
    moves_of_pawn = ["E2", "F2"]
    attacker_pawn.possible_moves.update(moves_of_pawn)

    attacker_check_moves[attacker_pawn] = attacker_pawn.possible_moves

    defender_king.possible_moves.update(moves_of_king)

    filter_attacking_piece(defender_king, attacker_check_moves)

    assert "E1" in defender_king.possible_moves


def test_update_possible_moves_of_king_double_check():
    # Testing update_possible_moves_of_king in a double check scenario
    defender = Player(PieceTeam.BLACK)

    defender_king = King(PieceTeam.BLACK)
    defender_king.position = "C6"
    moves_of_king = ["C7", "C5", "D6", "D7", "D5", "B7", "B5", "B6"]
    defender_king.possible_moves.update(moves_of_king)

    defender_rook = Rook(PieceTeam.BLACK)
    defender_rook.possible_moves.add("E1")

    defender_bishop = Bishop(PieceTeam.BLACK)
    defender_bishop.possible_moves.add("H5")

    defender.alive_pieces = [defender_king, defender_bishop, defender_rook]

    attacker_rook = Rook(PieceTeam.WHITE)
    attacker_rook.position = "D6"
    moves_of_rook = ["C6", "D5", "D7"]
    attacker_rook.possible_moves.update(moves_of_rook)

    attacker_bishop = Bishop(PieceTeam.WHITE)
    attacker_bishop.position = "E8"
    moves_of_bishop = ["D7", "C6"]
    attacker_bishop.possible_moves.update(moves_of_bishop)

    attacker_check_moves = {attacker_rook: attacker_rook.possible_moves,
                            attacker_bishop: attacker_bishop.possible_moves}

    update_possible_moves_of_king(defender_king, attacker_check_moves, defender)

    assert defender_rook.possible_moves == set()
    assert defender_bishop.possible_moves == set()
    assert defender_king.possible_moves == {'B7', 'D6', 'C7', 'C5'}


def test_update_possible_moves_of_king_single_check():
    # Testing update_possible_moves_of_king in a single check scenario
    defender = Player(PieceTeam.BLACK)

    defender_king = King(PieceTeam.BLACK)
    defender_king.position = "C6"
    moves_of_king = ["C7", "C5", "D6", "D7", "D5", "B7", "B5", "B6"]
    defender_king.possible_moves.update(moves_of_king)

    defender_rook = Rook(PieceTeam.BLACK)
    defender_rook.possible_moves.add("D6")

    defender_bishop = Bishop(PieceTeam.BLACK)
    defender_bishop.possible_moves.add("D6")

    defender.alive_pieces = [defender_king, defender_bishop, defender_rook]

    attacker_rook = Rook(PieceTeam.WHITE)
    attacker_rook.position = "D6"
    moves_of_rook = ["C6", "D5", "D7"]
    attacker_rook.possible_moves.update(moves_of_rook)

    attacker_check_moves = {attacker_rook: attacker_rook.possible_moves}

    update_possible_moves_of_king(defender_king, attacker_check_moves, defender)

    assert "D6" in defender_rook.possible_moves
    assert "D6" in defender_bishop.possible_moves
    assert "B6" not in defender_king.possible_moves
