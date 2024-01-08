from src.model.baseplayer.player import Player
from src.utils.testing_methods_check_handler import update_check_status_and_positions
from src.model.chesspiece_types.rook import Rook
from src.model.chessboard import Chessboard
from src.model.chesspiece_types.king import King
from src.utils.helpers import PieceTeam
from src.controller.check_handling.check_handler import CheckHandler


def test_check_if_char_sets_check():
    chessboard = Chessboard()

    attacker = Player(PieceTeam.WHITE)
    defender = Player(PieceTeam.BLACK)
    attacker_rook = Rook(PieceTeam.WHITE)
    attacker_rook.position = "D5"
    chessboard.board_state["D5"] = attacker_rook

    attacker.coverage_areas[attacker_rook] = ['E5', 'F5', "G5", "H5"]
    defender.king_position = 'G5'
    attackers_check_moves = {}
    resolve_check_moves = set()
    positions_for_red_stylesheet = set()

    update_check_status_and_positions(attacker, defender, chessboard, attackers_check_moves, resolve_check_moves,
                                      positions_for_red_stylesheet)

    assert defender.in_check is True
    assert 'D5' in resolve_check_moves
    assert 'D5' and "G5" in positions_for_red_stylesheet
    assert attackers_check_moves != {}


def setup_chessboard():
    chessboard = Chessboard()
    return chessboard


def test_check_if_king_safe():
    chessboard = setup_chessboard()
    king = King(PieceTeam.BLACK)
    king.position = 'E8'
    defender = Player(PieceTeam.BLACK)
    defender.king_position = "E8"
    attacker = Player(PieceTeam.WHITE)
    check_handler = CheckHandler(chessboard, attacker, defender)

    chessboard.board_state['E8'] = king
    defender.in_check = True

    check_handler.check_if_king_safe()

    assert defender.in_checkmate, "The king should be in checkmate but isn't marked as such."
