from src.utils.helpers import get_key_by_value, PlayerSwitchObserver
from controller.check_handler.check_resolver import CheckResolver
from PyQt6.QtCore import QObject, pyqtSignal
from controller.check_handler.move_validator_king import MoveValidatorKing


class CheckHandler(QObject, PlayerSwitchObserver):
    checkmate_signal = pyqtSignal(str)
    """
    Handles the logic of checking and resolving check situations for the king.
    """

    def __init__(self, chessboard, attacker, defender):
        """
        Initializes the KingCheckHandler.

        :param chessboard: The chessboard object containing the game state.
        :param current_player: The current player in the game.
        :param opponent: The defender player in the game.
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
        self.defender.in_check = False
        for attacking_piece, moves in self.attacker.coverage_areas.items():
            for move in moves:
                if move == self.defender.king_position:
                    self.defender.in_check = True
                    attacker_pos = get_key_by_value(self.chessboard.board_state, attacking_piece)
                    self.positions_for_red_stylesheet.add(attacker_pos)
                    self.positions_for_red_stylesheet.add(self.defender.king_position)
                    self.attackers_check_moves[attacking_piece] = attacking_piece.possible_moves

    def check_if_king_safe(self, callback, view):
        """
        Checks if the king is safe or in checkmate. Updates the game state accordingly.
        """
        king = self.chessboard.board_state.get(self.defender.king_position)

        if self.defender.in_check is True:

            self.move_validator_king.update_possible_moves_of_king(king, self.attackers_check_moves, self)
            self.check_resolver.find_resolve_check_positions(self.attackers_check_moves)
            # if self.double_check is False:
            #    self.check_resolver.update_defense_positions_against_check(self.attackers_check_moves)

            self.defender.in_checkmate = True

            for piece in self.defender.alive_pieces:
                if len(piece.possible_moves) > 0:
                    self.defender.in_checkmate = False  # Found a legal move, not checkmate
                    break

            if self.defender.in_checkmate:
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
                                print("pfad für checkmate piece wurde gesetzt")

                callback()
                winning_player = f"Spieler {self.attacker.team.name.capitalize()}"
                self.checkmate_signal.emit(winning_player)

    def if_check(self, callback, view):
        self.update_check_status_and_positions()
        if self.defender.in_check:
            self.check_if_king_safe(callback, view)

    def on_player_switch(self, new_attacker, new_defender):
        self.attacker = new_attacker
        self.defender = new_defender
