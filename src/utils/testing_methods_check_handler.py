from src.utils.helpers import get_key_by_value


def update_check_status_and_positions(attacker, defender, chessboard, attackers_check_moves, resolve_check_moves,
                                      positions_for_red_stylesheet):
    defender.in_check = False
    print(attacker.coverage_areas)
    print(defender.king_position)
    for attacking_piece, moves in attacker.coverage_areas.items():
        for move in moves:
            if move == defender.king_position:
                defender.in_check = True
                attacker_pos = get_key_by_value(chessboard.board_state, attacking_piece)
                resolve_check_moves.add(attacker_pos)
                positions_for_red_stylesheet.add(attacker_pos)
                positions_for_red_stylesheet.add(defender.king_position)
                attackers_check_moves[attacking_piece] = attacking_piece.possible_moves
