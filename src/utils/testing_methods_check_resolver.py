from src.model.chesspiece_types.pawn import Pawn
from src.model.chesspiece_types.king import King
from src.utils.helpers import get_key_by_value


def validate_defense_move(chessboard, move_to_check, attacking_piece):
    column, row = move_to_check
    new_move = column + str(row)

    if new_move not in chessboard.board_state.keys():
        return None

    piece_to_check = chessboard.board_state.get(new_move)

    if not piece_to_check:
        attacking_piece.possible_moves.add(new_move)
    else:
        if attacking_piece.team != piece_to_check.team:
            attacking_piece.possible_moves.add(new_move)
        else:
            return None


def simulate_move(chessboard, move_to_simulate, defending_piece, non_resolving_moves, chars_which_sets_check_dict,
                  defender_king_position, resolve_check_pos):
    if move_to_simulate not in chessboard.board_state.keys():
        return None

    chessboard.board_state[move_to_simulate] = defending_piece

    for attacking_piece in chars_which_sets_check_dict.keys():
        if non_resolving_moves.get(attacking_piece) == move_to_simulate:
            continue

        attacking_piece.possible_moves.clear()

        if isinstance(attacking_piece, Pawn):
            attacking_piece.possible_movements(chessboard)
        else:
            list_of_new_moves = attacking_piece.possible_movements(chessboard)

            for move_ in list_of_new_moves:
                validate_defense_move(chessboard, move_, attacking_piece)

        if defender_king_position in attacking_piece.possible_moves:
            non_resolving_moves[attacking_piece] = move_to_simulate
            continue

        else:
            resolve_check_pos.add(move_to_simulate)

    chessboard.board_state[move_to_simulate] = None


def update_defense_positions_against_check(chessboard, chars_which_sets_check_dict, resolve_check_pos,
                                           opponent_alive_chars_list):
    for attacker_piece in chars_which_sets_check_dict.keys():
        pos = get_key_by_value(chessboard.board_state, attacker_piece)

        if pos is not None:
            resolve_check_pos.add(pos)

    for defender_piece in opponent_alive_chars_list:
        if isinstance(defender_piece, King):
            continue
        moves_to_discard = set()

        for move in defender_piece.possible_moves:
            if move in resolve_check_pos:
                continue
            else:
                moves_to_discard.add(move)

        defender_piece.possible_moves.difference_update(moves_to_discard)


def find_resolve_check_positions(chessboard, chars_which_sets_check_dict, defender_coverage_areas, resolve_check_pos,
                                 defender_king_pos):

    non_resolving_moves = {}

    for attacking_piece in chars_which_sets_check_dict.keys():
        original_possible_moves = set(attacking_piece.possible_moves)
        chars_which_sets_check_dict[attacking_piece] = original_possible_moves

    for defending_piece, moves in defender_coverage_areas.items():
        moves_to_simulate = set(moves)
        for move_to_simulate in moves_to_simulate:
            could_move_resolve = any(move_to_simulate in moves for moves in chars_which_sets_check_dict.values())

            if could_move_resolve:
                simulate_move(chessboard, move_to_simulate, defending_piece, non_resolving_moves,
                              chars_which_sets_check_dict,
                              defender_king_pos, resolve_check_pos)
