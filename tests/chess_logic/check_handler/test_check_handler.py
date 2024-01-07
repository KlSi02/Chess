from src.model.baseplayer.player import Player
from src.utils.testing_methods_check_handler import update_check_status_and_positions
from src.model.chesspiece_types.rook import Rook
from src.model.chessboard import Chessboard
from src.model.chesspiece_types.king import King
from src.utils.helpers import PieceTeam
from controller.check_handler.check_handler import CheckHandler


def test_check_if_char_sets_check():
    # Create mock chessboard
    chessboard = Chessboard()  # Assuming Chessboard is a class you have defined
    # You will need to set up the chessboard state as required for the test

    # Create mock players
    attacker = Player(PieceTeam.WHITE)  # Assuming Player is a class with relevant attributes
    defender = Player(PieceTeam.BLACK)
    attacker_rook = Rook(PieceTeam.WHITE)
    attacker_rook.position = "D5"
    chessboard.board_state["D5"] = attacker_rook

    # Set initial conditions
    attacker.coverage_areas[attacker_rook] = ['E5', 'F5', "G5", "H5"]
    defender.king_position = 'G5'
    attackers_check_moves = {}
    resolve_check_moves = set()
    positions_for_red_stylesheet = set()

    # Call the function with mock data
    update_check_status_and_positions(attacker, defender, chessboard, attackers_check_moves, resolve_check_moves,
                                      positions_for_red_stylesheet)

    # Assert conditions after function execution
    assert defender.in_check is True
    assert 'D5' in resolve_check_moves
    assert 'D5' and "G5" in positions_for_red_stylesheet
    assert attackers_check_moves != {}  # or more specific conditions based on your logic


# Additional tests can be added to cover different scenarios like no check condition, different board states, etc.

def setup_chessboard():
    chessboard = Chessboard()
    # ... Initialize your chessboard setup here ...
    return chessboard


def test_check_if_king_safe():
    # Setup
    chessboard = setup_chessboard()
    king = King(PieceTeam.BLACK)
    king.position = 'E8'
    defender = Player(PieceTeam.BLACK)
    defender.king_position = "E8"
    attacker = Player(PieceTeam.WHITE)
    check_handler = CheckHandler(chessboard, attacker, defender)

    # Place the king in a checkmate position
    chessboard.board_state['E8'] = king
    defender.in_check = True
    # Mock other necessary board positions and states to simulate checkmate

    # Call the method
    check_handler.check_if_king_safe()

    # Validate the result
    assert defender.in_checkmate, "The king should be in checkmate but isn't marked as such."
