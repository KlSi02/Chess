from src.utils.helpers import update_possible_moves, get_key_by_value
from src.model.chesspiece_types.pawn import Pawn


def find_threatening_pieces(defender, target_position, list_of_threatining_pieces):
    for piece, moves in defender.coverage_areas.items():
        for move in moves:
            if move == target_position:
                list_of_threatining_pieces.add(piece)


def check_surrounded_pieces(chessboard, attacker, defender, column, row, column_step, row_step, pieces_to_check_moves,
                            list_of_threatining_pieces):
    new_column, new_row = column, int(row)
    for _ in range(8):
        new_column = chr(ord(new_column) + column_step)
        new_row += row_step

        pos = new_column + str(new_row)
        if pos in chessboard.board_state.keys():
            target_piece = chessboard.board_state.get(pos)

            if target_piece and target_piece.team.name == attacker.team.name:
                threatened_field = any(pos in moves for moves in defender.coverage_areas.values())
                if threatened_field:
                    find_threatening_pieces(defender, pos, list_of_threatining_pieces)
                    pieces_to_check_moves.add(target_piece)
                else:
                    break
            else:
                break


def evaluate_move_impact_on_king(chessboard, move, list_of_threatend_pieces, king_pos):
    for piece in list_of_threatend_pieces:
        piece.possible_moves.clear()

        if isinstance(piece, Pawn):
            piece.possible_movements(chessboard)
        else:
            list_of_new_moves = piece.possible_movements(chessboard)
            for column, row in list_of_new_moves:
                update_possible_moves(chessboard, column, row, piece)

        is_king_threatened = any(king_pos in moves for moves in piece.possible_moves)

        if is_king_threatened:
            return move


def simulate_moves_of_important_piece(chessboard, attacker, pieces_to_check_moves, list_of_threatend_pieces):
    """
    Simulates moves of nearby characters and discards moves that would threaten the king.
    """
    moves_to_discard = set()
    king_pos = attacker.king_position

    for piece in pieces_to_check_moves:
        for move in piece.possible_moves:
            square_to_check = chessboard.board_state.get(move)
            if square_to_check in list_of_threatend_pieces:
                continue
            old_pos = get_key_by_value(chessboard.board_state, piece)
            chessboard.board_state[move] = piece
            chessboard.board_state[old_pos] = None

            danger = evaluate_move_impact_on_king(chessboard, move, list_of_threatend_pieces, king_pos)
            if danger:
                moves_to_discard.add(danger)
            chessboard.board_state[old_pos] = piece
            chessboard.board_state[move] = None

        piece.possible_moves.difference_update(moves_to_discard)


def get_pieces_that_surround_king(chessboard, attacker, pieces_to_check_moves, defender):
    """
    Identifies and simulates moves for characters surrounding the king.
    """
    king = chessboard.board_state.get(attacker.king_position)
    column, row = attacker.king_position

    pieces_to_check_moves.clear()
    pieces_to_check_moves.add(king)
    list_of_threatining_pieces = set()

    directions = [(1, 1), (1, -1), (-1, -1), (-1, 1), (1, 0), (-1, 0), (0, 1), (0, -1)]
    for column_step, row_step in directions:
        check_surrounded_pieces(chessboard, attacker, defender, column, row, column_step, row_step,
                                pieces_to_check_moves, list_of_threatining_pieces)

    simulate_moves_of_important_piece(chessboard, attacker, pieces_to_check_moves, list_of_threatining_pieces)
