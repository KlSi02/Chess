from src.model.chesspiece_types.pawn import Pawn
from src.model.chesspiece_types.queen import Queen
from src.model.chesspiece_types.rook import Rook
from src.model.chesspiece_types.bishop import Bishop
from src.model.chesspiece_types.knight import Knight
from src.utils.helpers import PieceTeam
from PyQt6.QtGui import QPixmap


def get_promotion_choice():
    valid_choices = ['Queen', 'Rook', 'Bishop', 'Knight']
    while True:
        choice = input("Your choice: ").capitalize()

        if choice in valid_choices:
            return choice
        else:
            print("Invalid choice. Please select again.")


def promote_pawn(pawn):
    if (pawn.team.name == "WHITE" and pawn.position[1] == "8") or (
            pawn.team.name == "BLACK" and pawn.position[1] == "1"):
        return get_promotion_choice()
    return None


def setup_new_piece(piece_type, attacker):
    team = PieceTeam.WHITE if attacker.team.name == "WHITE" else PieceTeam.BLACK
    if piece_type == 'Queen':
        return Queen(team)
    elif piece_type == 'Rook':
        return Rook(team)
    elif piece_type == 'Bishop':
        return Bishop(team)
    elif piece_type == 'Knight':
        return Knight(team)


def update_piece(chessboard, view, new_piece, pos):
    chessboard.board_state[pos] = None
    chessboard.board_state[pos] = new_piece

    team = str(new_piece.team.name.lower())
    piece_class_name = new_piece.__class__.__name__.lower()
    piece_name = f"{team}_{piece_class_name}"

    for label in view.labels:
        if label.objectName() == pos:
            label.setPixmap(f"C:\\Users\\simon\\Desktop\\ChessProject\\src\\assets\\{piece_name}.png")


def check_pawn_promotion(chessboard, attacker, view):
    for pos, piece in chessboard.board_state.items():
        if piece:
            if isinstance(piece, Pawn):
                if piece.team.name == attacker.team.name:
                    piece_type = promote_pawn(piece)
                    if piece_type:
                        new_piece = setup_new_piece(piece_type, attacker)
                        update_piece(chessboard, view, new_piece, pos)


# ROOK

def is_castling_possible(chessboard, view, attacker, defender, king, rook, list_of_stylesheets):
    if king.has_moved or rook.has_moved:
        return False

    if attacker.in_check:
        return False
    start_pos = min(king.position, rook.position)
    end_pos = max(king.position, rook.position)
    row_number = king.position[1]
    between_positions = [chr(i) + row_number for i in range(ord(start_pos[0]) + 1, ord(end_pos[0]))]

    for pos in between_positions:
        if chessboard.board_state[pos] is not None:
            return False

    for pos in between_positions + [king.position]:
        if any(pos in moves for moves in defender.coverage_areas.values()):
            return False

    if rook.position[0] < king.position[0]:
        new_king_pos = chr(ord(king.position[0]) - 2) + king.position[1]

        for label in view.labels:
            if label.objectName() == new_king_pos:
                label.setStyleSheet("background-color: yellow; border: 1px solid black;")

    else:
        new_king_pos = chr(ord(king.position[0]) + 2) + king.position[1]

        for label in view.labels:
            if label.objectName() == new_king_pos:
                list_of_stylesheets[label] = label.styleSheet()
                label.setStyleSheet("background-color: yellow; border: 1px solid black;")

    return True


def update_pixmap(labels, old_pos, new_pos):
    """
    Updates the pixmap from an old position to a new position on the UI.

    :param labels: A list of label objects on the UI.
    :param old_pos: The old position of the piece (e.g., 'A1').
    :param new_pos: The new position of the piece (e.g., 'B1').
    """
    old_label, new_label = None, None

    # Find the labels corresponding to the old and new positions
    for label in labels:
        if label.objectName() == old_pos:
            old_label = label
        elif label.objectName() == new_pos:
            new_label = label

    # If both labels are found, move the pixmap from the old to the new label
    if old_label and new_label:
        pixmap = old_label.pixmap().copy()
        old_label.setPixmap(QPixmap())  # Clear the old pixmap
        new_label.setPixmap(pixmap)  # Set the new pixmap


def move_rook_for_castling(chessboard, view, rook_start_pos, new_king_pos):
    rook = chessboard.board_state.get(rook_start_pos)
    if rook is None:
        return None

    if new_king_pos[1] == '1':
        new_rook_pos = 'D1' if new_king_pos == 'C1' else 'F1'
    else:
        new_rook_pos = 'D8' if new_king_pos == 'C8' else 'F8'

    update_pixmap(view.labels, rook.position, new_rook_pos)
    return rook, new_rook_pos


def perform_castling(chessboard, view, old_king_pos, new_king_pos):
    king = chessboard.board_state.get(old_king_pos)
    if king is None:
        return False

    if new_king_pos in ["C1", "C8"]:
        rook_start_pos = "A1" if new_king_pos == "C1" else "A8"
    else:
        rook_start_pos = "H1" if new_king_pos == "G1" else "H8"

    rook, new_rook_pos = move_rook_for_castling(chessboard, view, rook_start_pos, new_king_pos)
    if rook is None:
        return False

    chessboard.board_state[king.position] = None
    chessboard.board_state[rook.position] = None
    chessboard.board_state[new_king_pos] = king
    chessboard.board_state[new_rook_pos] = rook

    king.position = new_king_pos
    rook.position = new_rook_pos
    king.has_moved = True
    rook.has_moved = True

    return True
