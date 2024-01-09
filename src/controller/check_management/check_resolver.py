from src.utils.helpers import get_key_by_value, PlayerSwitchObserver
from src.model.chesspiece_types.king import King
from src.model.chesspiece_types.pawn import Pawn


class CheckResolver(PlayerSwitchObserver):
    """
    Handles the simulation of defensive moves in a chess game to assess if they can resolve a check condition.

    Attributes:
        chessboard (Chessboard): The current state of the chessboard.
        attacker (Player): The player who is currently attacking.
        defender (Player): The player who is defending against the check.
    """
    def __init__(self, chessboard, attacker, defender):
        """
        Initializes the CheckResolver.

        :param chessboard: The current chessboard state.
        :param attacker: The player who is currently attacking.
        :param defender: The player defending against the check.
        """
        self.chessboard = chessboard
        self.attacker = attacker
        self.defender = defender

    def validate_defense_move(self, move_to_check, attacking_piece):
        """
        Validates if a move by the attacking piece is a viable defense against the check.

        :param move_to_check: The move to be validated, represented as (column, row).
        :param attacking_piece: The piece attempting the defensive move.
        :return: True if the move is valid, False otherwise.
        """
        column, row = move_to_check
        new_move = column + str(row)

        if new_move not in self.chessboard.board_state.keys():
            return None

        piece_to_check = self.chessboard.board_state.get(new_move)

        if not piece_to_check:
            attacking_piece.possible_moves.add(new_move)
        else:
            if attacking_piece.team != piece_to_check.team:
                attacking_piece.possible_moves.add(new_move)
            else:
                return None

    def simulate_move(self, move_to_simulate, defending_piece, resolve_check_pos, defender_king_position):
        """
        Simulates a move to assess its impact on the current check situation.

        :param move_to_simulate: The move to simulate.
        :param defending_piece: The defending piece making the move.
        :param resolve_check_pos: A set to store moves that can resolve the check.
        :param defender_king_position: The position of the defender's king.
        :return: True if the move resolves the check, False otherwise.
        """
        if move_to_simulate not in self.chessboard.board_state.keys():
            return None

        original_position = get_key_by_value(self.chessboard.board_state, defending_piece)
        displaced_piece = self.chessboard.board_state.get(move_to_simulate)

        self.chessboard.board_state[move_to_simulate] = defending_piece
        self.chessboard.board_state[original_position] = None

        for enemy_piece in self.attacker.alive_pieces:
            enemy_piece.possible_moves.clear()

            if enemy_piece:

                if isinstance(enemy_piece, Pawn):
                    enemy_piece.possible_movements(self.chessboard)
                    self.attacker.coverage_areas[enemy_piece] = enemy_piece.possible_moves

                else:
                    list_of_new_moves = enemy_piece.possible_movements(self.chessboard)
                    if list_of_new_moves:
                        for move in list_of_new_moves:
                            if move:
                                self.validate_defense_move(move, enemy_piece)
                                self.attacker.coverage_areas[enemy_piece] = enemy_piece.possible_moves

        threatening_move = any(defender_king_position in moves for moves in self.attacker.coverage_areas.values())

        if not threatening_move:
            resolve_check_pos.add(move_to_simulate)

        self.chessboard.board_state[move_to_simulate] = displaced_piece
        self.chessboard.board_state[original_position] = defending_piece

    def find_resolve_check_positions(self, attackers_check_move_dict):
        """
        Identifies and stores positions that can potentially resolve the check.

        :param attackers_check_move_dict: Dict of attacking pieces causing the check.
        """
        defender_king_pos = self.defender.king_position
        positions_of_threatening_pieces = set()

        for attacking_piece, possible_moves in attackers_check_move_dict.items():
            save_possible_moves = possible_moves.copy()
            pos = get_key_by_value(self.chessboard.board_state, attacking_piece)
            positions_of_threatening_pieces.add(pos)
            attackers_check_move_dict[attacking_piece] = save_possible_moves

        attackers_check_move_dict["positions"] = positions_of_threatening_pieces

        for defending_piece, moves in self.defender.coverage_areas.items():
            if isinstance(defending_piece, King):
                continue

            resolve_check_pos = set()
            moves_to_simulate = set(moves)
            for move_to_simulate in moves_to_simulate:
                could_move_resolve = any(move_to_simulate in moves for moves in attackers_check_move_dict.values())

                if could_move_resolve:
                    self.simulate_move(move_to_simulate, defending_piece, resolve_check_pos, defender_king_pos)

            defending_piece.possible_moves = resolve_check_pos

    def on_player_switch(self, new_attacker, new_defender):
        """
        Handles the player switch, updating the attacker and defender.
        """
        self.attacker = new_attacker
        self.defender = new_defender
