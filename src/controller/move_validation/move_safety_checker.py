from src.utils.helpers import update_possible_moves, get_key_by_value, PlayerSwitchObserver
from src.model.chesspiece_types.pawn import Pawn


class MoveSafetyChecker(PlayerSwitchObserver):
    """
    Ensures the king's safety by simulating potential moves of nearby pieces and checking
    if these moves would put the king in danger. The class identifies threatening pieces
    and evaluates their impact on the king's position.
    """

    def __init__(self, chessboard, attacker, defender):
        """
        Initializes the MoveSafetyChecker with the chessboard and the players.

        :param chessboard: The current state of the chessboard.
        :param attacker: The player currently making their move (attacker).
        :param defender: The opposing player (defender).
        """
        self.chessboard = chessboard
        self.attacker = attacker
        self.defender = defender
        self.pieces_to_check_moves = set()
        self.threatening_pieces = set()

    def identify_threatening_pieces(self, target_position):
        """
        Identifies all pieces from the defender that are threatening a given position.

        :param target_position: The position to check for threats.
        """
        for piece, moves in self.defender.coverage_areas.items():
            for move in moves:
                if move == target_position:
                    self.threatening_pieces.add(piece)

    def check_pieces_around_king(self, column, row, column_step, row_step):
        """
        Checks for pieces surrounding the king in a given step direction. It adds pieces
        to the pieces_to_check_moves set if they are potentially threatening.

        :param column: The column of the king's position.
        :param row: The row of the king's position.
        :param column_step: The horizontal step direction.
        :param row_step: The vertical step direction.
        """
        new_column, new_row = column, int(row)

        for _ in range(8):
            new_column = chr(ord(new_column) + column_step)
            new_row += row_step

            pos = new_column + str(new_row)
            if pos in self.chessboard.board_state.keys():
                target_piece = self.chessboard.board_state.get(pos)

                if target_piece:
                    if target_piece.team.name == self.attacker.team.name:
                        threatened_field = any(pos in moves for moves in self.defender.coverage_areas.values())

                        if threatened_field:
                            self.identify_threatening_pieces(pos)
                            self.pieces_to_check_moves.add(target_piece)

                        else:
                            break
                else:
                    continue

    def evaluate_move_impact_on_king(self, king_pos):
        """
        Evaluates the impact of potential moves on the safety of the king.

        :param king_pos: The position of the king to evaluate.
        :return: True if the move is unsafe for the king, False otherwise.
        """
        all_threatening_moves = set()
        for piece in self.threatening_pieces:
            if piece not in self.chessboard.board_state.values():
                continue

            piece.possible_moves.clear()

            if isinstance(piece, Pawn):
                piece.possible_movements(self.chessboard)
                all_threatening_moves.update(piece.possible_moves)

            else:
                list_of_new_moves = piece.possible_movements(self.chessboard)
                for column, row in list_of_new_moves:
                    update_possible_moves(self.chessboard, column, row, piece)

                all_threatening_moves.update(piece.possible_moves)

            # Check if the king is still threatened after the move.
        return king_pos in all_threatening_moves

    def simulate_and_filter_piece_moves(self):
        """
        Simulates moves of nearby pieces and discards moves that would threaten the king.
        """
        king_pos = self.attacker.king_position

        for piece in self.pieces_to_check_moves:
            moves_to_discard = set()
            for move in piece.possible_moves.copy():
                # Temporarily update the board state to simulate the move.
                displaced_piece = self.chessboard.board_state.get(move)

                old_pos = get_key_by_value(self.chessboard.board_state, piece)
                self.chessboard.board_state[move] = piece
                self.chessboard.board_state[old_pos] = None

                # Evaluate if the move puts the king in danger.
                if self.evaluate_move_impact_on_king(king_pos):
                    # If the move is dangerous, add it to the discard set.
                    moves_to_discard.add(move)

                self.chessboard.board_state[old_pos] = piece
                self.chessboard.board_state[move] = displaced_piece

            # Update the possible moves for the piece, excluding the dangerous ones.
            piece.possible_moves.difference_update(moves_to_discard)

    def get_surrounding_pieces(self):
        """
        Identifies and simulates moves for pieces surrounding the king to ensure his safety.
        """
        column, row = self.attacker.king_position

        directions = [(1, 1), (1, -1), (-1, -1), (-1, 1), (1, 0), (-1, 0), (0, 1), (0, -1)]
        for column_step, row_step in directions:
            self.check_pieces_around_king(column, row, column_step, row_step)

        self.simulate_and_filter_piece_moves()

    def on_player_switch(self, new_attacker, new_defender):
        """
        Handles the player switch, updating the attacker and defender.
        """
        self.attacker = new_attacker
        self.defender = new_defender

