from PyQt6.QtGui import QColor
from src.model.chesspiece_types.pawn import Pawn
from src.model.baseplayer.player import Player
from src.utils.helpers import PieceTeam
from src.controller.move_execution.move_executor import MoveExecutor
from src.controller.check_management.check_handler import ChessCheckHandler
from src.controller.move_execution.special_rules_handler import get_rooks
from src.utils.helpers import give_player_threatened_fields
from src.model.chesspiece_types.king import King
from src.view.chessboard import UIChessboard


class Controller:
    """
    Central controller class for managing the flow and rules of a chess game. This class coordinates
    interactions between the model, view, and various game logic handlers.
    """

    def __init__(self, model):
        """
        Initializes the Controller with the chess game model and sets up the game view and handlers.

        :param model: The model representing the state of the chess game.
        """

        self.model = model
        self.view = UIChessboard(self.if_piece_in_self_team)
        self.view.show()

        self.observers = []

        self.attacker = Player(PieceTeam.WHITE)
        self.defender = Player(PieceTeam.BLACK)

        self.move_executor = MoveExecutor(self.model, self.view, self.attacker, self.defender,
                                          self.update_state_of_game)
        self.check_handler = ChessCheckHandler(self.model, self.attacker, self.defender)
        self.check_handler.checkmate_signal.connect(self.on_checkmate)

        from src.controller.move_validation.move_validator import MoveValidator
        self.move_validator = MoveValidator(self.model, self.attacker, self.defender)
        self.move_validator.stalemate_signal.connect(self.on_stalemate)

        self.last_clicked_piece = None
        self.original_stylesheets = {}
        self.red_stylesheets = {}

        self.initialize_game()
        self.register_observer(self.move_validator)
        self.register_observer(self.move_validator.move_safety_checker)
        self.register_observer(self.check_handler)
        self.register_observer(self.check_handler.check_resolver)
        self.register_observer(self.check_handler.move_validator_king)
        self.register_observer(self.move_executor)
        self.register_observer(self.move_executor.special_rules_handler)

    def register_observer(self, observer):
        """
        Registers an observer to be notified during player switches.

        :param observer: The observer to be registered.
        """
        if observer not in self.observers:
            self.observers.append(observer)

    def player_switch(self):
        """
        Switches the roles of attacker and defender and notifies all observers.
        """
        self.attacker, self.defender = self.defender, self.attacker
        for observer in self.observers:
            observer.on_player_switch(self.attacker, self.defender)

    def initialize_chars_with_pictures(self):
        """
        Initializes the chessboard UI with images representing the chess pieces.
        Sets up signal connections for UI interactions.
        """
        for label in self.view.labels:
            label.setScaledContents(True)

            label.highlight_labels_signal.connect(self.handle_clicked_label)
            label.make_move_signal.connect(self.move_executor.move_execution)
            label.castling_signal.connect(self.move_executor.use_castling)
            label.en_passant_signal.connect(self.move_executor.use_en_passant)

            square_name = label.objectName()
            from src.utils.helpers import get_piece_name_for_square
            piece_name = get_piece_name_for_square(square_name)

            if piece_name is not None:
                label.set_svg(f"assets/{piece_name}.svg")

    def initialize_game(self):
        """
        Initializes the game state, updates king positions, alive pieces, and threatened fields.
        """
        self.initialize_chars_with_pictures()
        self.move_validator.update_king_positions()
        self.move_validator.update_alive_pieces()
        give_player_threatened_fields(self.model, self.attacker, self.defender)

    def start_new_game(self):
        """
        Resets the game state and starts a new game.
        """
        self.reset_data()
        self.model.reset()
        self.view.reset_ui_chessboard()

        if self.attacker.team != "WHITE":
            self.player_switch()

        self.attacker.reset()
        self.defender.reset()
        self.initialize_game()

    def close_game(self):
        """
        Closes the game view and performs any necessary cleanup.
        """
        self.view.close()

    def on_checkmate(self, winning_player):
        """
        Handles the checkmate event, displaying a dialog and offering options for the next steps.

        :param winning_player: The player who has won the game.
        """
        self.view.show_checkmate_dialog(winning_player, self.start_new_game, self.close_game)

    def on_stalemate(self, winning_player):
        """
        Handles the stalemate event, displaying a dialog and offering options for the next steps.

        :param winning_player: The player involved in the stalemate.
        """
        self.view.show_stalemate_dialog(winning_player, self.start_new_game, self.close_game)

    def clear_possible_moves_highlights(self):
        for square in self.view.labels:
            square.stop_pulsing()
            if square in self.original_stylesheets.keys():
                square.pulsing_color = None
                original_color = self.original_stylesheets[square]
                square.set_highlight_color(original_color)
        self.original_stylesheets.clear()

    def clear_check_highlights(self):
        for square, color in self.red_stylesheets.items():
            original_color = self.red_stylesheets[square]
            square.set_highlight_color(original_color)
            square.stop_pulsing()
        self.red_stylesheets.clear()

    def clear_en_passant_highlights(self):
        for square, color in self.move_executor.special_rules_handler.stylesheets_en_passant.items():
            original_color = self.move_executor.special_rules_handler.stylesheets_en_passant[square]
            square.set_highlight_color(original_color)
            square.stop_pulsing()
            square.pulsing_color = None
        self.move_executor.special_rules_handler.stylesheets_en_passant.clear()

    def clear_castling_highlights(self):
        for square, color in self.move_executor.special_rules_handler.stylesheets_castling.items():
            original_color = self.move_executor.special_rules_handler.stylesheets_castling[square]
            square.set_highlight_color(original_color)
            square.stop_pulsing()
            square.pulsing_color = None
        self.move_executor.special_rules_handler.stylesheets_castling.clear()

    def handle_clicked_label(self, square_name):
        """
        Handles the event when a label (chessboard square) is clicked in the UI.

        :param square_name: The name of the square that was clicked.
        """
        target_char = self.model.board_state.get(square_name)

        if not target_char or target_char.team != self.attacker.team:
            self.last_clicked_piece = None
            self.clear_possible_moves_highlights()
            return

        self.last_clicked_piece = target_char

        self.clear_possible_moves_highlights()

        self.clear_castling_highlights()

        self.clear_en_passant_highlights()

        try:
            self.highlight_possible_moves(target_char)
            if isinstance(target_char, Pawn):
                self.move_executor.special_rules_handler.highlight_en_passant(target_char)

            if isinstance(target_char, King):
                rooks = get_rooks(self.model, self.attacker)
                if len(rooks) >= 1 and target_char.has_moved is False:
                    for rook in rooks:
                        self.move_executor.special_rules_handler.is_castling_possible(target_char, rook)

        except Exception as e:
            print(f"Figur kann nicht bewegt werden, Fehler: {e}")

    def highlight_possible_moves(self, piece):
        """
        Highlights all possible moves for a selected piece on the chessboard.

        :param piece: The piece for which to highlight possible moves.
        """
        for square in self.view.labels:
            if square.objectName() in piece.possible_moves:
                if square not in self.original_stylesheets:
                    self.original_stylesheets[square] = square._color
                    possible_moves_color = QColor(120, 180, 120, 150)
                    square.start_pulsing(possible_moves_color, possible_moves_color.darker())
                    square.pulsing_color = "green"

    def style_square_red_if_check(self):
        """
        Styles the squares red if they are part of a check situation.
        """
        if self.defender.in_check is True:
            for label in self.view.labels:
                if label.objectName() in self.check_handler.positions_for_red_stylesheet:
                    if label not in self.red_stylesheets.keys():
                        self.red_stylesheets[label] = label._color
                    check_color = QColor(180, 120, 120, 150)
                    label.start_pulsing(check_color, check_color.darker())

    def reset_data(self):
        """
        Resets game data, clears highlights and cached stylesheets, and clears piece moves.
        """
        self.clear_possible_moves_highlights()

        self.attacker.coverage_areas.clear()
        self.defender.coverage_areas.clear()

        self.check_handler.attackers_check_moves.clear()
        self.check_handler.positions_for_red_stylesheet.clear()

        self.move_validator.move_safety_checker.pieces_to_check_moves.clear()
        self.move_validator.move_safety_checker.threatening_pieces.clear()

        self.clear_check_highlights()

        self.clear_castling_highlights()

        self.clear_en_passant_highlights()

        self.last_clicked_piece = None

        for piece in self.model.board_state.values():
            if piece:
                piece.possible_moves.clear()
                piece.original_possible_moves.clear()

    def update_state_of_game(self):
        self.reset_data()
        self.move_validator.update_king_positions()
        give_player_threatened_fields(self.model, self.attacker, self.defender)
        self.check_handler.handle_check_situation(self.style_square_red_if_check, self.view)
        self.style_square_red_if_check()
        self.player_switch()

        self.move_executor.special_rules_handler.add_pawn_moves_to_coverage_areas()

        if not self.attacker.in_check:
            self.move_validator.filter_king_moves()
            self.move_validator.move_safety_checker.get_surrounding_pieces()
            self.move_validator.check_for_stalemate(self.view)

    def if_piece_in_self_team(self, pos):
        for square, piece in self.model.board_state.items():
            if square == pos:
                piece_to_check = piece

                if piece_to_check and piece_to_check.team == self.attacker.team:
                    return True

        return False

