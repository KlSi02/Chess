from src.utils.helpers import update_possible_moves, get_key_by_value, PlayerSwitchObserver
from src.model.chesspiece_types.pawn import Pawn


class MoveSafetyChecker(PlayerSwitchObserver):
    """
    Class for ensuring the king's safety by simulating potential moves of nearby characters
    and checking if these moves would put the king in danger.
    """

    def __init__(self, chessboard, current_player, opponent):
        # Initialize the MoveSafetyChecker with the chessboard, the current player (attacker),
        # and the opponent (defender).
        self.chessboard = chessboard
        self.attacker = current_player
        self.defender = opponent
        self.pieces_to_check_moves = set()
        self.threatening_pieces = set()

    def find_threatening_pieces(self, target_position):
        # Identify all pieces from the defender that are threatening a given position.
        for piece, moves in self.defender.coverage_areas.items():
            for move in moves:
                if move == target_position:
                    self.threatening_pieces.add(piece)

    def check_surrounded_pieces(self, column, row, column_step, row_step):
        # Check for pieces surrounding the king based on a given step direction.
        # Adds pieces to the pieces_to_check_moves set if they are potentially threatening.
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
                            self.find_threatening_pieces(pos)
                            self.pieces_to_check_moves.add(target_piece)

                        else:
                            break
                else:
                    continue

    def evaluate_move_impact_on_king(self, king_pos):
        # Evaluate the impact of a potential move on the safety of the king.
        # Clears and recalculates possible moves of threatening pieces.
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

    def simulate_moves_of_important_piece(self):
        """
        Simulates moves of nearby characters and discards moves that would threaten the king.
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

    def get_pieces_that_surround_king(self):
        """
        Identifies and simulates moves for characters surrounding the king.
        """
        king = self.chessboard.board_state.get(self.attacker.king_position)

        column, row = self.attacker.king_position

        directions = [(1, 1), (1, -1), (-1, -1), (-1, 1), (1, 0), (-1, 0), (0, 1), (0, -1)]
        for column_step, row_step in directions:
            self.check_surrounded_pieces(column, row, column_step, row_step)

        self.simulate_moves_of_important_piece()

    def on_player_switch(self, new_attacker, new_defender):
        self.attacker = new_attacker
        self.defender = new_defender

