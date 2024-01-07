from src.model.chesspiece_types.pawn import Pawn
from src.model.chesspiece_types.queen import Queen
from src.model.chesspiece_types.rook import Rook
from src.model.chesspiece_types.bishop import Bishop
from src.model.chesspiece_types.knight import Knight
from src.utils.helpers import PieceTeam, PlayerSwitchObserver
from PyQt6.QtGui import QPixmap, QColor


def check_en_passant(chessboard, attacker, old_pos, new_pos):
    row_difference = int(new_pos[1]) - int(old_pos[1])

    if abs(row_difference) == 2:
        new_letter = chr(ord(new_pos[0]) - 1)
        checked_pos_left = new_letter + new_pos[1]

        if checked_pos_left in chessboard.board_state.keys():
            checked_piece_left = chessboard.board_state.get(checked_pos_left)
            if checked_piece_left:
                if isinstance(checked_piece_left, Pawn) and attacker.team != checked_piece_left.team:
                    checked_piece_left.en_passant = True

        new_letter = chr(ord(new_pos[0]) + 1)
        checked_pos_right = new_letter + new_pos[1]

        if checked_pos_right in chessboard.board_state.keys():
            checked_piece_right = chessboard.board_state.get(checked_pos_right)
            if checked_piece_right:
                if isinstance(checked_piece_right, Pawn) and attacker.team != checked_piece_right.team:
                    checked_piece_right.en_passant = True


def get_promotion_choice():
    """
    Prompt the user to choose a piece for pawn promotion.

    The function continually requests user input until a valid choice is made from
    the specified options: Queen, Rook, Bishop, Knight. The input is case-insensitive.

    Returns:
        str: The name of the chosen piece type.
    """
    valid_choices = ['Queen', 'Rook', 'Bishop', 'Knight']
    while True:
        choice = input("Your choice: (Queen, Rook, Bishop, Knight").capitalize()

        if choice in valid_choices:
            return choice
        else:
            print("Invalid choice. Please select again.")


def promote_pawn(pawn):
    """
    Checks if a pawn is eligible for promotion based on its position on the board.

    This function checks if the pawn has reached the opposite end of the board,
    triggering a promotion opportunity. If eligible, it prompts the user to choose
    the piece type for promotion.

    Args:
        pawn (Pawn): The pawn object to check for promotion eligibility.

    Returns:
        str or None: The chosen piece type for promotion or None if not eligible.
    """
    if (pawn.team.name == "WHITE" and pawn.position.endswith("8")) or (
            pawn.team.name == "BLACK" and pawn.position.endswith("1")):
        return True
    return False


def get_rooks(chessboard, attacker):
    rooks = []
    for piece in chessboard.board_state.values():
        if isinstance(piece, Rook) and piece.team == attacker.team:
            rooks.append(piece)

    return rooks


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
        old_label.set_svg("")  # Clear the old pixmap
        new_label.setPixmap(pixmap)  # Set the new pixmap


def setup_new_piece(piece_type, team):
    """
    Creates a new chess piece of the specified type.

    Args:
        piece_type (str): The type of the chess piece to create (e.g., 'Queen').

    Returns:
        ChessPiece: An instance of the specified chess piece type.
    """
    team_ = PieceTeam.WHITE if team.name == "WHITE" else PieceTeam.BLACK
    if piece_type == 'Queen':
        return Queen(team_)
    elif piece_type == 'Rook':
        return Rook(team_)
    elif piece_type == 'Bishop':
        return Bishop(team_)
    elif piece_type == 'Knight':
        return Knight(team_)


class SpecialRulesHandler(PlayerSwitchObserver):

    def __init__(self, view, chessboard, attacker, defender):
        self.chessboard = chessboard
        self.attacker = attacker
        self.defender = defender
        self.view = view
        self.stylesheets_castling = {}
        self.stylesheets_en_passant = {}

    def highlight_en_passant(self, pawn):
        if pawn.en_passant:
            old_pos, new_pos = self.chessboard.last_moves[-1]
            row_numb = 1 if pawn.team.name == "BLACK" else -1
            new_numb = int(new_pos[1]) - row_numb
            pos_to_mark = new_pos[0] + str(new_numb)

            for label in self.view.labels:
                if label.objectName() == pos_to_mark:
                    print("label wurde gefunden")
                    self.stylesheets_en_passant[label] = label._color
                    en_passant_color = QColor(130, 160, 200, 150)
                    label.start_pulsing(en_passant_color, en_passant_color.darker())
                    label.pulsing_color = "blue"

    def perform_en_passant(self, old_pawn_pos, new_pawn_pos):
        pos_of_last_mover, last_move = self.chessboard.last_moves[-1]
        pawn = self.chessboard.board_state.get(old_pawn_pos)
        enemy_pawn = self.chessboard.board_state.get(last_move)

        self.chessboard.board_state[new_pawn_pos] = pawn
        self.chessboard.board_state[old_pawn_pos] = None
        self.chessboard.board_state[last_move] = None

        self.defender.alive_pieces.remove(enemy_pawn)

        pawn.position = new_pawn_pos
        pawn.en_passant = False

        for label in self.view.labels:
            if label.objectName() == last_move:
                label.set_svg("")

    def check_pawn_promotion_(self, pos, callback):
        self.view.show_promotion_dialog(setup_new_piece, self.update_piece, callback, pos, self.attacker.team)

    def add_pawn_moves_to_coverage_areas(self):
        for piece in self.defender.alive_pieces:
            if isinstance(piece, Pawn):
                piece.add_diagonal_moves(self.chessboard)

    def update_piece(self, new_piece, pos):
        """
        Updates the chessboard with a new piece at the specified position.

        This function places the new piece on the board, updates the board state, and
        changes the corresponding UI label to reflect the new piece.

        Args:
            new_piece (ChessPiece): The chess piece to place on the board.
            pos (str): The board position (e.g., 'A1', 'B2') to place the piece.

        """
        self.chessboard.board_state[pos] = None
        self.chessboard.board_state[pos] = new_piece
        new_piece.position = pos

        print(self.chessboard.board_state.items())

        self.attacker.alive_pieces.append(new_piece)

        team = str(new_piece.team.name.lower())

        piece_class_name = new_piece.__class__.__name__.lower()
        piece_name = f"{team}_{piece_class_name}"
        image_path = f"assets/{piece_name}.svg"

        for label in self.view.labels:
            if label.objectName() == pos:
                label.set_svg(image_path)

        return True

    def check_pawn_promotion(self, callback):
        """
        Checks each pawn on the board for promotion eligibility.

        Iterates through all pawns on the board belonging to the current player
        (attacker) and checks if they have reached the promotion row. If a pawn is
        eligible for promotion, it prompts the user for a choice of new piece and
        updates the board accordingly.
        """
        for pos, piece in self.chessboard.board_state.items():
            if piece and isinstance(piece, Pawn) and piece.team.name == self.attacker.team.name:
                if promote_pawn(piece):
                    self.check_pawn_promotion_(pos, callback)
                    self.attacker.alive_pieces.remove(piece)
                    return True

    def is_castling_possible(self, king, rook):
        if king.has_moved or rook.has_moved:
            return False

        if self.attacker.in_check:
            return False
        # Bestimmen der Positionen zwischen König und Turm
        start_pos = min(king.position, rook.position)
        end_pos = max(king.position, rook.position)
        row_number = king.position[1]
        between_positions = [chr(i) + row_number for i in range(ord(start_pos[0]) + 1, ord(end_pos[0]))]

        # Überprüfen, ob die Felder zwischen König und Turm frei sind
        for pos in between_positions:
            if self.chessboard.board_state[pos] is not None:
                return False

        # Überprüfen, ob der König durch die Rochade über angegriffene Felder zieht
        for pos in between_positions + [king.position]:
            if any(pos in moves for moves in self.defender.coverage_areas.values()):
                return False

        if rook.position[0] < king.position[0]:  # Königsflügel-Rochade
            new_king_pos = chr(ord(king.position[0]) - 2) + king.position[1]

            for label in self.view.labels:
                if label.objectName() == new_king_pos:
                    self.stylesheets_castling[label] = label._color
                    castling_color = QColor(190, 180, 110, 150)
                    label.start_pulsing(castling_color, castling_color.darker())
                    label.pulsing_color = "yellow"

        else:  # Damenseite-Rochade
            new_king_pos = chr(ord(king.position[0]) + 2) + king.position[1]

            for label in self.view.labels:
                if label.objectName() == new_king_pos:
                    self.stylesheets_castling[label] = label._color
                    castling_color = QColor(190, 180, 110, 150)
                    label.start_pulsing(castling_color, castling_color.darker())
                    label.pulsing_color = "yellow"

        return True

    def move_rook_for_castling(self, rook_start_pos, new_king_pos):
        rook = self.chessboard.board_state.get(rook_start_pos)
        if rook is None:
            return None  # Sicherstellen, dass der Turm vorhanden ist

        if new_king_pos[1] == '1':  # Weiß
            new_rook_pos = 'D1' if new_king_pos == 'C1' else 'F1'
        else:  # Schwarz
            new_rook_pos = 'D8' if new_king_pos == 'C8' else 'F8'

        update_pixmap(self.view.labels, rook.position, new_rook_pos)
        return rook, new_rook_pos

    def perform_castling(self, old_king_pos, new_king_pos):
        king = self.chessboard.board_state.get(old_king_pos)
        if king is None:
            return False  # Sicherstellen, dass der König vorhanden ist

        if new_king_pos in ["C1", "C8"]:
            rook_start_pos = "A1" if new_king_pos == "C1" else "A8"
        else:
            rook_start_pos = "H1" if new_king_pos == "G1" else "H8"

        rook, new_rook_pos = self.move_rook_for_castling(rook_start_pos, new_king_pos)
        if rook is None:
            return False  # Abbruch, wenn kein Turm vorhanden ist

        # Bewegen von König und Turm
        self.chessboard.board_state[king.position] = None
        self.chessboard.board_state[rook.position] = None
        self.chessboard.board_state[new_king_pos] = king
        self.chessboard.board_state[new_rook_pos] = rook

        # Aktualisieren der Positionen und Bewegungsstatus
        king.position = new_king_pos
        rook.position = new_rook_pos
        king.has_moved = True
        rook.has_moved = True

        return True

    def on_player_switch(self, new_attacker, new_defender):
        self.attacker = new_attacker
        self.defender = new_defender
