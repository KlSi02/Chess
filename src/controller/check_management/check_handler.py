from src.utils.helpers import get_key_by_value, PlayerSwitchObserver
from src.controller.check_management.check_resolver import CheckResolver
from PyQt6.QtCore import QObject, pyqtSignal
from src.controller.check_management.move_validator_king_in_check import MoveValidatorKing


class ChessCheckHandler(QObject, PlayerSwitchObserver):
    """
    Handles the logic of checking and resolving check and checkmate situations for the king.
    """
    checkmate_signal = pyqtSignal(str)

    def __init__(self, chessboard, attacker, defender):
        """
        Initializes the ChessCheckHandler.

        :param chessboard: The chessboard object containing the game state.
        :param attacker: The current attacking player in the game.
        :param defender: The defending player in the game.
        """
        super().__init__()
        self.chessboard = chessboard
        self.attacker = attacker
        self.defender = defender
        self.check_resolver = CheckResolver(chessboard, attacker, defender)
        self.attackers_check_moves = {}
        self.move_validator_king = MoveValidatorKing(chessboard, attacker, defender, self.attackers_check_moves)

        self.positions_for_red_stylesheet = set()
        self.double_check = False

    def update_check_status_and_positions(self):
        """
        Updates the check status and positions for red highlighting in case of a check situation.
        """
        self.defender.in_check = False
        for attacking_piece, moves in self.attacker.coverage_areas.items():
            for move in moves:
                if move == self.defender.king_position:
                    self.defender.in_check = True
                    attacker_pos = get_key_by_value(self.chessboard.board_state, attacking_piece)
                    self.positions_for_red_stylesheet.add(attacker_pos)
                    self.positions_for_red_stylesheet.add(self.defender.king_position)
                    self.attackers_check_moves[attacking_piece] = attacking_piece.possible_moves

    def _update_view_and_notify_checkmate(self, callback, view):
        """
        Private method to update the UI view and notify about checkmate.
        """
        last_move, new_move = self.chessboard.last_moves[-1]
        piece_that_set_check = self.chessboard.board_state.get(new_move)
        piece_name = piece_that_set_check.__class__.__name__.lower()
        team_name = piece_that_set_check.team.name.lower()
        svg_path = f"assets/{team_name}_{piece_name}.svg"

        if last_move and new_move:
            for label in view.labels:
                if label:
                    if label.objectName() == last_move:
                        label.set_svg("")
                    elif label.objectName() == new_move:
                        label.set_svg(svg_path)

        callback()
        winning_player = f"Spieler {self.attacker.team.name.capitalize()}"
        self.checkmate_signal.emit(winning_player)

    def _assess_king_safety(self, callback, view):
        """
        Private method to assess if the king is safe or in checkmate.
        """
        king = self.chessboard.board_state.get(self.defender.king_position)

        if self.defender.in_check is True:

            self.move_validator_king.update_possible_moves_of_king(king, self.attackers_check_moves, self)
            self.check_resolver.find_resolve_check_positions(self.attackers_check_moves)

            self.defender.in_checkmate = True

            for piece in self.defender.alive_pieces:
                if len(piece.possible_moves) > 0:
                    self.defender.in_checkmate = False  # Found a legal move, not checkmate
                    break

            if self.defender.in_checkmate:
                self._update_view_and_notify_checkmate(callback, view)

    def handle_check_situation(self, callback, view):
        """
        Handles the check situation. Determines if the king is safe or in checkmate and updates the game state
        accordingly.
        """
        self.update_check_status_and_positions()
        if self.defender.in_check:
            self._assess_king_safety(callback, view)

    def on_player_switch(self, new_attacker, new_defender):
        """
        Handles the player switch, updating the attacker and defender.
        """
        self.attacker = new_attacker
        self.defender = new_defender
