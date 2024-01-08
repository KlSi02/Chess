import pytest
from src.model.baseplayer.player import Player
from src.model.chessboard import Chessboard
from src.model.chesspiece_types.rook import Rook
from src.model.chesspiece_types.king import King
from src.model.chesspiece_types.bishop import Bishop
from src.utils.helpers import PieceTeam
from src.utils.testing_methods_move_safety_checker import check_surrounded_pieces, simulate_moves_of_important_piece, \
    get_pieces_that_surround_king


def test_check_surrounded_pieces():
    chessboard = Chessboard()
    attacker = Player(PieceTeam.WHITE)
    defender = Player(PieceTeam.BLACK)
    pieces_to_check_moves = set()
    list_of_threatining_pieces = set()

    threatining_piece1 = Rook(PieceTeam.BLACK)
    threatining_piece1.possible_moves.add("E4")
    defender.coverage_areas[threatining_piece1] = threatining_piece1.possible_moves
    threatining_piece2 = Rook(PieceTeam.BLACK)

    piece_to_check = Rook(PieceTeam.WHITE)

    chessboard.board_state["E4"] = piece_to_check
    chessboard.board_state["H4"] = threatining_piece1
    chessboard.board_state["H5"] = threatining_piece2

    check_surrounded_pieces(chessboard, attacker, defender, "D", 4, 1, 0,
                            pieces_to_check_moves, list_of_threatining_pieces)
    assert piece_to_check in pieces_to_check_moves
    assert threatining_piece1 in list_of_threatining_pieces
    assert threatining_piece2 not in list_of_threatining_pieces

    pieces_to_check_moves.clear()
    list_of_threatining_pieces.clear()
    chessboard.board_state["C4"] = piece_to_check
    check_surrounded_pieces(chessboard, attacker, defender, "D", 4, -1, 0,
                            pieces_to_check_moves, list_of_threatining_pieces)
    assert piece_to_check not in pieces_to_check_moves
    assert list_of_threatining_pieces == set()

    pieces_to_check_moves.clear()
    check_surrounded_pieces(chessboard, attacker, defender, "D", 4, 0, 1, pieces_to_check_moves, list_of_threatining_pieces)
    assert chessboard.board_state["D5"] not in pieces_to_check_moves

    pieces_to_check_moves.clear()
    check_surrounded_pieces(chessboard, attacker, defender, "D", 4, 0, -1, pieces_to_check_moves, list_of_threatining_pieces)
    assert len(pieces_to_check_moves) == 0

    pieces_to_check_moves.clear()
    check_surrounded_pieces(chessboard, attacker, defender, "D", 4, 1, 1, pieces_to_check_moves, list_of_threatining_pieces)
    assert len(pieces_to_check_moves) == 0


def test_simulate_move_of_important_piece():
    chessboard = Chessboard()
    white_rook = Rook(PieceTeam.WHITE)
    black_rook = Rook(PieceTeam.BLACK)
    white_king = King(PieceTeam.WHITE)
    white_king.position = "E5"

    chessboard.board_state["E5"] = white_king
    chessboard.board_state["D5"] = white_rook
    chessboard.board_state["A5"] = black_rook

    attacker = Player(PieceTeam.WHITE)
    attacker.king_position = "E5"

    moves_of_white_rook = ["D4", "D6", "C5"]
    white_rook.possible_moves.update(moves_of_white_rook)
    pieces_to_check_moves = [white_rook]
    list_of_threatened_pieces = [black_rook]

    simulate_moves_of_important_piece(chessboard, attacker, pieces_to_check_moves, list_of_threatened_pieces)

    assert "D4" not in white_rook.possible_moves
    assert "D6" not in white_rook.possible_moves
    assert "C5" in white_rook.possible_moves
    assert chessboard.board_state["D5"] == white_rook


def test_get_pieces_that_surround_king():
    chessboard = Chessboard()
    attacker = Player(PieceTeam.WHITE)
    attacker.king_position = "E5"

    white_king = King(PieceTeam.WHITE)
    white_king.position = "E5"

    white_rook1 = Rook(PieceTeam.WHITE)
    white_rook1.position = "D5"
    white_rook1_moves = ["D4", "D3", "C5", "B5", "A5"]
    white_rook1.possible_moves.update(white_rook1_moves)

    white_rook2 = Rook(PieceTeam.WHITE)
    white_rook2.position = "E6"
    white_rook2_moves = ["E7", "F6", "G6", "H6"]
    white_rook2.possible_moves.update(white_rook2_moves)

    white_rook3 = Rook(PieceTeam.WHITE)
    white_rook3.position = "D6"
    white_rook3_moves = ["D7", "C6", "B6", "A6"]
    white_rook3.possible_moves.update(white_rook3_moves)

    defender = Player(PieceTeam.BLACK)

    black_rook1 = Rook(PieceTeam.BLACK)
    black_rook1.position = "A5"
    black_rook1_moves = ["B5", "C5", "D5"]
    black_rook1.possible_moves.update(black_rook1_moves)

    black_rook2 = Rook(PieceTeam.BLACK)
    black_rook2.position = "E7"
    black_rook2.possible_moves.add("E6")

    black_bishop = Bishop(PieceTeam.BLACK)
    black_bishop.position = "C7"
    black_bishop.possible_moves.add("D6")

    defender.coverage_areas = {black_rook1: black_rook1.possible_moves, black_rook2: black_rook2.possible_moves, black_bishop: black_bishop.possible_moves}

    chessboard.board_state["E5"] = white_king
    chessboard.board_state["D5"] = white_rook1
    chessboard.board_state["E6"] = white_rook2
    chessboard.board_state["D6"] = white_rook3

    chessboard.board_state["A5"] = black_rook1
    chessboard.board_state["E7"] = black_rook2
    chessboard.board_state["C7"] = black_bishop

    pieces_to_check_moves = set()

    get_pieces_that_surround_king(chessboard, attacker, pieces_to_check_moves, defender)

    assert white_rook1.possible_moves == {"C5", "B5", "A5"}
    assert white_rook2.possible_moves == {"E7"}
    assert white_rook3.possible_moves == set()
