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


def simulate_king_moves(old_pos, move, king, chessboard, attacker):
    if not move:
        return

    displaced_piece = chessboard.board_state.get(move)
    chessboard.board_state[move] = king
    chessboard.board_state[old_pos] = None
    attacker.coverage_areas.clear()
    opponent_threatened_fields(chessboard, attacker)
    threatened_field = any(move in moves for moves in attacker.coverage_areas.values())
    if threatened_field:
        king.possible_moves.discard(move)
    chessboard.board_state[old_pos] = king
    chessboard.board_state[move] = displaced_piece


def only_king_can_move(defender):
    """
    Clears the possible moves of all defending pieces except the king.

    Args:
        defender (Player): The player who is defending against the check.
    """
    for defending_piece in defender.alive_pieces:
        if not isinstance(defending_piece, King):
            defending_piece.possible_moves.clear()


def filter_only_safe_moves(king, attackers_check_moves, chessboard, attacker):
    """
    Removes moves from the king's possible moves if those moves are still under attack.

    Args:
        king (King): The defending king piece.
        attackers_check_moves (dict): Dictionary of attacking pieces and their moves causing check.
    """
    for moves in attackers_check_moves.values():
        king.possible_moves.difference_update(moves)

    old_pos = king.position
    possible_moves_copy = king.possible_moves.copy()
    for move in possible_moves_copy:
        simulate_king_moves(old_pos, move, king, chessboard, attacker)


def filter_moves_excluding_danger_line(king, attackers_check_moves, attacking_piece, chessboard, attacker):
    """
    Filters out moves from the king's possible moves that are along the line of attack.

    Args:
        king (King): The defending king piece.
        attackers_check_moves (dict): Dictionary of attacking pieces and their moves causing check.
        attacking_piece (ChessPiece): The attacking piece causing the check.
    """
    danger_line = calculate_danger_line(king, attacking_piece)
    attacking_piece.possible_moves.update(danger_line)
    filter_only_safe_moves(king, attackers_check_moves, chessboard, attacker)


def filter_attacking_piece(king, attackers_check_moves, chessboard, attacker):
    """
    Filters the king's possible moves based on the type of attacking pieces.

    Args:
        king (King): The defending king piece.
        attackers_check_moves (dict): Dictionary of attacking pieces and their moves causing check.
    """
    for attacking_piece in attackers_check_moves.keys():
        if isinstance(attacking_piece, (Bishop, Queen, Rook)):
            filter_moves_excluding_danger_line(king, attackers_check_moves, attacking_piece, chessboard, attacker)
        else:
            filter_only_safe_moves(king, attackers_check_moves, chessboard, attacker)


def update_possible_moves_of_king(king, attackers_check_moves, defender, check_handler, chessboard, attacker):
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
        check_handler.double_check = True
        only_king_can_move(defender)
        filter_attacking_piece(king, attackers_check_moves, chessboard, attacker)
    else:
        filter_attacking_piece(king, attackers_check_moves, chessboard, attacker)


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