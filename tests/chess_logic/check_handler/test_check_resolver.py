import pytest
from src.model.chessboard import Chessboard
from src.utils.helpers import PieceTeam
from src.utils.testing_methods_check_resolver import validate_defense_move
from src.model.chesspiece_types.rook import Rook
from src.model.chesspiece_types.pawn import Pawn
from src.model.chesspiece_types.king import King
from src.utils.testing_methods_check_resolver import (simulate_move, update_defense_positions_against_check,
                                                      find_resolve_check_positions)


def test_validate_defense_move():
    # Setup a chessboard and pieces for testing
    chessboard = Chessboard()
    attacking_piece = Rook(PieceTeam.WHITE)
    defending_piece = Rook(PieceTeam.BLACK)

    # Szenario 1: Zielfeld ist leer
    move_to_check = ("A", 3)
    attacking_piece.position = "A2"
    chessboard.board_state["A2"] = attacking_piece
    validate_defense_move(chessboard, move_to_check, attacking_piece)
    assert "A3" in attacking_piece.possible_moves, "A3 should be a valid move"

    # Scenario 2: Target square has an opposing piece
    attacking_piece.position = "B5"
    chessboard.board_state["B5"] = attacking_piece
    move_to_check = ("B", 6)
    chessboard.board_state["B6"] = defending_piece
    validate_defense_move(chessboard, move_to_check, attacking_piece)
    assert "B6" in attacking_piece.possible_moves, "B6 should be a valid move"

    # Scenario 3: Target square has own piece
    attacking_piece.position = "D4"
    chessboard.board_state["D5"] = attacking_piece
    chessboard.board_state["D4"] = attacking_piece
    move_to_check = ("D", 5)
    validate_defense_move(chessboard, move_to_check, attacking_piece)
    assert "D5" not in attacking_piece.possible_moves, "D5 should not be a valid move"


@pytest.fixture
def setup_chessboard():
    return Chessboard()


def test_simulate_move():
    chessboard = Chessboard()
    defending_piece = Rook(PieceTeam.WHITE)
    attacking_piece = Rook(PieceTeam.BLACK)
    non_resolving_moves = {}
    chars_which_sets_check = {attacking_piece: ""}
    resolve_check_pos = set()
    defender_king_position = "E1"

    # Place pieces on the chessboard
    chessboard.board_state["E5"] = attacking_piece
    chessboard.board_state["D2"] = defending_piece

    move_to_simulate = "E2"
    simulate_move(chessboard, move_to_simulate, defending_piece, non_resolving_moves, chars_which_sets_check,
                  defender_king_position,
                  resolve_check_pos)
    assert move_to_simulate in resolve_check_pos, "E2 should resolve the check"
    assert move_to_simulate not in non_resolving_moves, "E2 should not be in non_resolving_moves"
    assert chessboard.board_state[move_to_simulate] is None, "E2 should be reset on the board"

    # Stellen Sie sicher, dass das Schachbrett zurückgesetzt wurde
    assert chessboard.board_state[move_to_simulate] is None

    # Simulate a move already in non_resolving_moves
    move_to_simulate = "D3"
    simulate_move(chessboard, move_to_simulate, defending_piece, non_resolving_moves, chars_which_sets_check,
                  defender_king_position,
                  resolve_check_pos)
    assert move_to_simulate not in resolve_check_pos, "D3 should not resolve the check"
    assert defending_piece, move_to_simulate in non_resolving_moves.items()  #"D3 should be in non_resolving_moves"
    assert chessboard.board_state[move_to_simulate] is None, "D3 should be reset on the board"

    # Simulate a move on a non-existing square
    move_to_simulate = "D9"
    result = simulate_move(chessboard, move_to_simulate, defending_piece, non_resolving_moves, chars_which_sets_check,
                           defender_king_position,
                           resolve_check_pos)
    assert result is None, "D9 is a non-existing square"


def test_update_defense_positions_against_check():
    chessboard = Chessboard()
    defender_king = King(PieceTeam.BLACK)
    defender_king.possible_moves.add("D3")

    attacker_rook = Rook(PieceTeam.WHITE)
    defender_rook1 = Rook(PieceTeam.BLACK)
    defender_rook1.possible_moves.update(["H2", "A1", "E3"])

    defender_rook2 = Rook(PieceTeam.BLACK)
    defender_rook2.possible_moves.update(["H1", "F2", "F6"])

    defender_rook3 = Rook(PieceTeam.BLACK)
    defender_rook3.possible_moves.update(["D7", "E8", "H1"])
    chars_which_sets_check_dict = {}

    for attacking_piece in chessboard.board_state.values():
        if isinstance(attacking_piece, Pawn):
            if attacking_piece.team == attacker_rook.team:
                chars_which_sets_check_dict[attacking_piece] = ""

    resolve_check_pos = {"H5", "E3", "F6"}
    defender_chars = [defender_king, defender_rook1, defender_rook2, defender_rook3]

    update_defense_positions_against_check(chessboard, chars_which_sets_check_dict, resolve_check_pos, defender_chars)

    positions = ["A2", "B2", "C2", "D2", "E2", "F2", "G2", "H2"]
    for position in positions:
        assert position in resolve_check_pos

    assert {"D3"} not in defender_king.possible_moves
    assert {"E3"} not in defender_rook1.possible_moves
    assert {"F6"} not in defender_rook2.possible_moves
    assert {"H5"} not in defender_rook3.possible_moves


def test_find_resolve_check_positions(setup_chessboard):
    chessboard = setup_chessboard
    white_rook = Rook(PieceTeam.WHITE)
    black_king = King(PieceTeam.BLACK)
    black_rook = Rook(PieceTeam.BLACK)

    # Update possible moves for the pieces.
    white_rook.possible_moves.update(["E4", "E3", "E2", "E1"])
    black_king.possible_moves.add("D1")
    black_rook.possible_moves.update(["D3", "D4", "E2"])

    # Setup the board state with the white rook attacking and the black pieces defending.
    chessboard.board_state["E2"] = None
    chessboard.board_state["E1"] = black_king
    chessboard.board_state["E5"] = white_rook
    chessboard.board_state["D2"] = black_rook

    # Define the pieces that are putting the opponent in check.
    chars_which_sets_check = {white_rook: white_rook.possible_moves}

    # Define the threatened areas of the defender.
    defender_coverage_areas = {black_rook: black_rook.possible_moves}

    # A set to store positions that can resolve the check situation.
    resolve_check_positions = set()
    defender_king_position = "E1"

    # Aufrufen der zu testenden Methode
    find_resolve_check_positions(chessboard, chars_which_sets_check, defender_coverage_areas, resolve_check_positions,
                                 defender_king_position)

    # Assert that the correct positions for resolving the check are identified.
    assert "E2" in resolve_check_positions
    assert len(resolve_check_positions) == 1
    assert "D1" in black_king.possible_moves
