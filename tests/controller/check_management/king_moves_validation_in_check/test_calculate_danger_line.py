import pytest

from src.controller.check_management.move_validator_king_in_check import calculate_danger_line, get_attack_direction, \
    get_horizontal_line, get_vertical_line, get_diagonal_line
from src.model.chesspiece_types.king import King
from src.model.chesspiece_types.queen import Queen
from src.utils.helpers import PieceTeam


@pytest.fixture
def chess_pieces():
    """Fixture to create standard chess pieces for testing."""
    defender_king = King(PieceTeam.BLACK)
    attacker_queen = Queen(PieceTeam.WHITE)
    return defender_king, attacker_queen


def test_calculate_danger_line_vertical_up(chess_pieces):
    """Test calculation of the danger line vertically upwards from the king's position."""
    defender_king, attacker_queen = chess_pieces
    defender_king.position = "E6"
    attacker_queen.position = "E3"

    danger_line = calculate_danger_line(defender_king, attacker_queen)
    assert danger_line == ["E7", "E8"]


def test_calculate_danger_line_vertical_down(chess_pieces):
    """Test calculation of the danger line vertically downwards from the king's position."""
    defender_king, attacker_queen = chess_pieces
    attacker_queen.position = "E6"
    defender_king.position = "E3"

    danger_line = calculate_danger_line(defender_king, attacker_queen)
    assert danger_line == ["E2", "E1"]


def test_calculate_danger_line_diagonal_left_up(chess_pieces):
    """Test calculation of the danger line diagonally left upwards from the king's position."""
    defender_king, attacker_queen = chess_pieces
    attacker_queen.position = "G2"
    defender_king.position = "C6"

    danger_line = calculate_danger_line(defender_king, attacker_queen)
    assert danger_line == ["B7", "A8"]


def test_calculate_danger_line_diagonal_left_down(chess_pieces):
    """Test calculation of the danger line diagonally left downwards from the king's position."""
    defender_king, attacker_queen = chess_pieces
    attacker_queen.position = "D4"
    defender_king.position = "C3"

    danger_line = calculate_danger_line(defender_king, attacker_queen)
    assert danger_line == ["B2", "A1"]


def test_calculate_danger_line_diagonal_right_down(chess_pieces):
    """Test calculation of the danger line diagonally right downwards from the king's position."""
    defender_king, attacker_queen = chess_pieces
    attacker_queen.position = "E4"
    defender_king.position = "F3"

    danger_line = calculate_danger_line(defender_king, attacker_queen)
    assert danger_line == ["G2", "H1"]


def test_calculate_danger_line_diagonal_right_up(chess_pieces):
    """Test calculation of the danger line diagonally right downwards from the king's position."""
    defender_king, attacker_queen = chess_pieces
    attacker_queen.position = "B7"
    defender_king.position = "D5"

    danger_line = calculate_danger_line(defender_king, attacker_queen)
    assert danger_line == ["E4", "F3", "G2", "H1"]


def test_calculate_danger_line_horizontal_down(chess_pieces):
    """Test calculation of the danger line horizontally downwards from the king's position."""
    defender_king, attacker_queen = chess_pieces
    attacker_queen.position = "E6"
    defender_king.position = "E4"

    danger_line = calculate_danger_line(defender_king, attacker_queen)
    assert danger_line == ["E3", "E2", "E1"]


def test_calculate_danger_line_horizontal_up(chess_pieces):
    """Test calculation of the danger line vertically upwards from the king's position."""
    defender_king, attacker_queen = chess_pieces
    attacker_queen.position = "E4"
    defender_king.position = "E6"

    danger_line = calculate_danger_line(defender_king, attacker_queen)
    assert danger_line == ["E7", "E8"]


def test_get_attack_direction():
    """Test determination of attack direction (vertical, horizontal, diagonal)."""
    # Test for vertical direction
    defender_king_pos = "B2"
    attacker_pos = "B6"

    result = get_attack_direction(defender_king_pos, attacker_pos)
    assert result == "vertical"

    # Test for horizontal direction
    defender_king_pos = "A4"
    attacker_pos = "F4"

    result = get_attack_direction(defender_king_pos, attacker_pos)
    assert result == "horizontal"

    defender_king_pos = "C2"
    attacker_pos = "B1"

    result = get_attack_direction(defender_king_pos, attacker_pos)
    assert result == "diagonal"


def test_get_horizontal_line():
    defender_king_pos = "B2"
    attacker_pos = "C2"

    result = get_horizontal_line(defender_king_pos, attacker_pos)
    assert result == ["A2"]


def test_get_vertical_line():
    defender_king_pos = "A3"
    attacker_pos = "A5"

    result = get_vertical_line(defender_king_pos, attacker_pos)
    assert result == ["A2", "A1"]


def test_get_diagonal_line():
    defender_king_pos = "C3"
    attacker_pos = "E5"

    result = get_diagonal_line(defender_king_pos, attacker_pos)
    assert result == ["B2", "A1"]
