from src.model.chesspiece_types.pawn import Pawn
from src.model.chesspiece_types.rook import Rook
from src.model.chesspiece_types.king import King
from src.model.chesspiece_types.bishop import Bishop
from src.model.chesspiece_types.queen import Queen
from src.utils.helpers import update_possible_moves, get_key_by_value, PlayerSwitchObserver


def is_double_check(attackers_check_moves):
    """
    Determines if the current check situation is a double check.

    Args:
        attackers_check_moves (dict): Dictionary mapping attacking pieces to their moves causing check.

    Returns:
        bool: True if more than one piece is causing check, otherwise False.
    """
    if len(attackers_check_moves.keys()) > 1:
        return True
    else:
        return False


class MoveValidatorKing(PlayerSwitchObserver):

    def __init__(self, chessboard, attacker, defender, attackers_check_moves):
        self.chessboard = chessboard
        self.attacker = attacker
        self.defender = defender
        self.attackers_check_moves = attackers_check_moves

    def on_player_switch(self, new_attacker, new_defender):
        self.attacker = new_attacker
        self.defender = new_defender

    def only_king_can_move(self):
        """
        Clears the possible moves of all defending pieces except the king.

        Args:
            defender (Player): The player who is defending against the check.
        """
        for defending_piece in self.defender.alive_pieces:
            if not isinstance(defending_piece, King):
                defending_piece.possible_moves.clear()

    def simulate_king_move(self, king):
        moves_to_discard = set()
        for move in king.possible_moves.copy():
            # Temporarily update the board state to simulate the move.
            displaced_piece = self.chessboard.board_state.get(move)

            old_pos = get_key_by_value(self.chessboard.board_state, king)
            self.chessboard.board_state[move] = king
            self.chessboard.board_state[old_pos] = None

            # Evaluate if the move puts the king in danger.
            if self.evaluate_king_move(move):
                # If the move is dangerous, add it to the discard set.
                moves_to_discard.add(move)

            self.chessboard.board_state[old_pos] = king
            self.chessboard.board_state[move] = displaced_piece

        # Update the possible moves for the piece, excluding the dangerous ones.
        king.possible_moves.difference_update(moves_to_discard)

    def evaluate_king_move(self, king_pos):
        all_threatening_moves = set()
        for piece in self.attacker.coverage_areas.keys():
            if piece not in self.chessboard.board_state.values():
                continue

            piece.possible_moves.clear()

            if isinstance(piece, Pawn):
                piece.possible_movements(self.chessboard)
                all_threatening_moves.update(piece.possible_moves)

            else:
                list_of_new_moves = piece.possible_movements(self.chessboard)
                if list_of_new_moves:
                    for column, row in list_of_new_moves:
                        update_possible_moves(self.chessboard, column, row, piece)

                    all_threatening_moves.update(piece.possible_moves)

            # Check if the king is still threatened after the move.
        return king_pos in all_threatening_moves

    def filter_only_safe_moves(self, king):
        """
        Removes moves from the king's possible moves if those moves are still under attack.

        Args:
            king (King): The defending king piece.
            attackers_check_moves (dict): Dictionary of attacking pieces and their moves causing check.
        """
        moves_to_discard = set()

        for moves in self.attackers_check_moves.values():
            for move in moves:
                if move in king.possible_moves:
                    moves_to_discard.add(move)

        for piece, moves in self.attacker.coverage_areas.items():
            if isinstance(piece, Pawn):
                for move in moves:
                    if move[0] == king.position[0]:
                        continue
            else:
                for move in moves:
                    if move in king.possible_moves:
                        moves_to_discard.add(move)

        king.possible_moves.difference_update(moves_to_discard)
        self.simulate_king_move(king)

    def filter_moves_excluding_danger_line(self, king, attacking_piece):
        """
        Filters out moves from the king's possible moves that are along the line of attack.

        Args:
            king (King): The defending king piece.
            attackers_check_moves (dict): Dictionary of attacking pieces and their moves causing check.
            attacking_piece (ChessPiece): The attacking piece causing the check.
        """
        danger_line = calculate_danger_line(king, attacking_piece)
        attacking_piece.possible_moves.update(danger_line)
        self.filter_only_safe_moves(king)

    def filter_attacking_piece(self, king, attackers_check_moves):
        """
        Filters the king's possible moves based on the type of attacking pieces.

        Args:
            king (King): The defending king piece.
            attackers_check_moves (dict): Dictionary of attacking pieces and their moves causing check.
        """
        for attacking_piece in attackers_check_moves.keys():
            if isinstance(attacking_piece, (Bishop, Queen, Rook)):
                self.filter_moves_excluding_danger_line(king, attacking_piece)
            else:
                self.filter_only_safe_moves(king)

    def update_possible_moves_of_king(self, king, attackers_check_moves, check_handler):
        """
        Updates the possible moves of the king based on the current check situation.

        Args:
            king (King): The defending king piece.
            attackers_check_moves (dict): Dictionary of attacking pieces and their moves causing check.
            defender (Player): The player who is defending against the check.
            check_handler (CheckHandler): The handler object for check situations.
        """
        check_handler.double_check = is_double_check(attackers_check_moves)
        if check_handler.double_check:
            self.only_king_can_move()
            self.filter_attacking_piece(king, attackers_check_moves)
        else:
            self.filter_attacking_piece(king, attackers_check_moves)


def calculate_danger_line(king, attacking_piece):
    combined_danger_lines = []

    direction = get_attack_direction(king.position, attacking_piece.position)

    if direction == 'horizontal':
        combined_danger_lines.extend(get_horizontal_line(king.position, attacking_piece.position))
    elif direction == 'vertical':
        combined_danger_lines.extend(get_vertical_line(king.position, attacking_piece.position))
    elif direction == 'diagonal':
        combined_danger_lines.extend(get_diagonal_line(king.position, attacking_piece.position))

    return combined_danger_lines


def get_attack_direction(king_pos, attacker_pos):
    king_col, king_row = ord(king_pos[0]), int(king_pos[1])
    attacker_col, attacker_row = ord(attacker_pos[0]), int(attacker_pos[1])

    if king_row == attacker_row:
        return 'horizontal'

    elif king_col == attacker_col:
        return 'vertical'

    elif abs(king_col - attacker_col) == abs(king_row - attacker_row):
        return 'diagonal'

    else:
        return 'undefined'


def get_horizontal_line(king_pos, attacker_pos):
    horizontal_line = []
    row = king_pos[1]
    king_col = ord(king_pos[0])
    attacker_col = ord(attacker_pos[0])

    start_col = min(king_col, attacker_col)
    end_col = max(king_col, attacker_col)

    if king_col > attacker_col:
        for col in range(end_col + 1, ord('H') + 1):
            horizontal_line.append(chr(col) + row)

    elif king_col < attacker_col:
        for col in range(start_col - 1, ord('A') - 1, -1):
            horizontal_line.append(chr(col) + row)

    return horizontal_line


def get_vertical_line(king_pos, attacker_pos, board_size=8):
    vertical_line = []
    col = king_pos[0]
    king_row = int(king_pos[1])
    attacker_row = int(attacker_pos[1])

    start_row = min(king_row, attacker_row)
    end_row = max(king_row, attacker_row)

    if king_row > attacker_row:
        for row in range(end_row + 1, board_size + 1):
            vertical_line.append(col + str(row))

    elif king_row < attacker_row:
        for row in range(start_row - 1, 0, -1):
            vertical_line.append(col + str(row))

    return vertical_line


def get_diagonal_line(king_pos, attacker_pos, board_size=8):
    diagonal_line = []
    king_col, king_row = ord(king_pos[0]), int(king_pos[1])
    attacker_col, attacker_row = ord(attacker_pos[0]), int(attacker_pos[1])

    step_col = 1 if king_col > attacker_col else -1
    step_row = 1 if king_row > attacker_row else -1

    col = king_col + step_col
    row = king_row + step_row

    while 'A' <= chr(col) <= 'H' and 1 <= row <= board_size:
        diagonal_line.append(chr(col) + str(row))
        col += step_col
        row += step_row

    return diagonal_line
