import string
from src.model.chesspiece_types.pawn import Pawn
from src.model.chesspiece_types.king import King
from src.model.chesspiece_types.rook import Rook
from src.model.chesspiece_types.queen import Queen
from src.utils.helpers import PieceTeam
from src.model.chessboard import Chessboard
from src.view.chessboard import UIChessboard
from src.model.baseplayer.player import Player
from controller.move_executor.special_rules_handler import SpecialRulesHandler, get_promotion_choice, promote_pawn
from src.utils.testing_methods_special_rules_handler import setup_new_piece, update_piece, check_pawn_promotion, \
    is_castling_possible
import pytest
from PyQt6.QtGui import QPixmap
from unittest.mock import MagicMock, Mock, patch


def mock_input(prompt):
    """
    Diese Funktion simuliert Benutzereingaben. Sie können sie anpassen,
    um verschiedene Eingaben zu testen.
    """
    return "Queen"


def test_get_promotion_choice(monkeypatch):
    monkeypatch.setattr("builtins.input", mock_input)
    choice = get_promotion_choice()
    assert choice == "Queen"


def test_promote_pawn(monkeypatch):
    monkeypatch.setattr("builtins.input", mock_input)
    white_pawn = Pawn(PieceTeam.WHITE)
    white_pawn.position = "A8"

    piece_choice = promote_pawn(white_pawn)
    assert piece_choice == "Queen"

    white_pawn.position = "A7"
    piece_choice = promote_pawn(white_pawn)
    assert piece_choice is None


@pytest.fixture
def setup():
    chessboard = Chessboard()
    view = UIChessboard()
    attacker = Player(PieceTeam.WHITE)
    defender = Player(PieceTeam.BLACK)
    special_rules_handler = SpecialRulesHandler(view, attacker, defender)
    return chessboard, view, attacker, defender, special_rules_handler


def test_setup_new_piece():
    attacker = Player(PieceTeam.WHITE)
    piece_type = "Queen"

    piece = setup_new_piece(piece_type, attacker)
    assert isinstance(piece, Queen)
    assert piece.team.name == "WHITE"


def setup_uichessboard_mock():
    view = MagicMock()
    labels = []

    for letter in string.ascii_uppercase[:8]:
        for number in range(1, 9):
            label_name = f"{letter}{number}"

            mock_label = Mock()
            mock_label.objectName.return_value = label_name
            mock_label.pixmap.return_value = QPixmap()
            labels.append(mock_label)

    view.labels = labels
    return view


def test_update_piece():
    chessboard = Chessboard()
    mock_view = setup_uichessboard_mock()
    pos = "A8"
    piece = Queen(PieceTeam.WHITE)

    update_piece(chessboard, mock_view, piece, pos)

    piece_to_check = chessboard.board_state.get(pos)
    assert piece_to_check == piece

    for label in mock_view.labels:
        if label.objectName() == pos:
            label.setPixmap.assert_called_with(f"C:\\Users\\simon\\Desktop\\ChessProject\\src\\assets\\white_queen.png")


@patch("builtins.input", return_value="Queen")
def test_check_pawn_promotion(input_mock):
    chessboard = Chessboard()
    view = setup_uichessboard_mock()
    attacker = Player(PieceTeam.WHITE)
    white_pawn = Pawn(PieceTeam.WHITE)
    white_pawn.position = "A8"

    for pos, piece in chessboard.board_state.items():
        if piece:
            piece.position = pos

    chessboard.board_state["A8"] = None
    chessboard.board_state["A8"] = white_pawn

    check_pawn_promotion(chessboard, attacker, view)

    promoted_piece = chessboard.board_state.get("A8")
    assert isinstance(promoted_piece, Queen)


@pytest.fixture
def chessboard_setup():
    chessboard = Chessboard()
    attacker = Player(PieceTeam.WHITE)
    defender = Player(PieceTeam.BLACK)
    king = King(PieceTeam.WHITE)
    rook = Rook(PieceTeam.WHITE)
    return chessboard, attacker, defender, king, rook


def test_castling_possible(chessboard_setup):
    # Mock-Objekte erstellen
    chessboard, attacker, defender, king, rook = chessboard_setup
    list_of_stylesheets = {}
    view = setup_uichessboard_mock()

    # Konfigurieren der Mock-Objekte
    king.has_moved = False
    rook.has_moved = False
    attacker.in_check = False
    king.position = 'E1'
    rook.position = 'H1'
    chessboard.board_state = {"E1": king, 'F1': None, 'G1': None, "H1": rook}
    defender.coverage_areas = {}
    view.labels[0].setObjectName("G1")

    # Testen der Methode
    result = is_castling_possible(chessboard, view, attacker, defender, king, rook, list_of_stylesheets)

    # Überprüfen, ob die Rochade möglich ist
    assert result is True

    # Überprüfen, ob das Stylesheet des Labels geändert wurde
    expected_stylesheet = "background-color: yellow; border: 1px solid black;"
    if rook.position[0] < king.position[0]:  # Königsflügel-Rochade
        new_king_pos = chr(ord(king.position[0]) - 2) + king.position[1]
    else:  # Damenseite-Rochade
        new_king_pos = chr(ord(king.position[0]) + 2) + king.position[1]

    for label in view.labels:
        if label.objectName() == new_king_pos:
            label.setStyleSheet.assert_called_with(expected_stylesheet)


@pytest.fixture
def mock_labels():
    # Erstellen von Mock-Labels
    labels = [MagicMock(name=f"Label_{chr(65 + i)}{j}") for i in range(8) for j in range(1, 9)]
    for label in labels:
        label.objectName.return_value = label.name
        label.pixmap.return_value = QPixmap()  # Erstellen eines leeren Pixmaps für jedes Label
    return labels


def update_positions(old_pos, new_pos, positions):
    """
    Hilfsfunktion, die die Logik der Positionsänderung abbildet.
    :param old_pos: Alte Position.
    :param new_pos: Neue Position.
    :param positions: Dictionary der Positionen.
    """
    if old_pos in positions and new_pos not in positions:
        positions[new_pos] = positions[old_pos]
        del positions[old_pos]
    return positions


def test_update_positions():
    positions = {"A1": "some_pixmap", "B1": None}
    updated_positions = update_positions("A1", "B1", positions)
    assert updated_positions == {"B1": "some_pixmap"}


# Test ausführen
test_update_positions()
