from src.model.chesspiece_types.pawn import Pawn
from src.model.chesspiece_types.king import King
from src.model.chesspiece_types.rook import Rook
from src.utils.helpers import PlayerSwitchObserver
from controller.move_execution.special_rules_handler import SpecialRulesHandler, check_en_passant


class MoveExecutor(PlayerSwitchObserver):
    """
    Class responsible for executing moves on the chessboard. This includes handling piece capture,
    updating the board state, and dealing with special move scenarios such as castling or en passant.
    """

    def __init__(self, chessboard, view, current_player, opponent, game_state_update_callback):
        """
        Initializes the MoveExecutor with the necessary game components.

        :param chessboard: The Chessboard object representing the current game state.
        :param view: The game view, used for handling special rule scenarios.
        :param current_player: The player currently taking their turn.
        :param opponent: The opposing player.
        :param game_state_update_callback: A callback function to update the game state after a move.
        """
        self.chessboard = chessboard
        self.attacker = current_player
        self.defender = opponent
        self.special_rules_handler = SpecialRulesHandler(view, chessboard, self.attacker, self.defender)
        self.update_state_of_game = game_state_update_callback

    def handle_special_moves(self, piece, old_pos, new_pos):
        """
        Handles special moves for pieces such as the Pawn's first move, en passant, or castling.

        :param piece: The chess piece being moved.
        :param old_pos: The original position of the piece before the move.
        :param new_pos: The new position of the piece after the move.
        :return: True if a pawn promotion occurs, otherwise None.
        """
        for char in self.chessboard.board_state.values():
            if char and isinstance(char, Pawn):
                if char.en_passant:
                    char.en_passant = False

        if isinstance(piece, Pawn):
            if piece.first_turn:
                check_en_passant(self.chessboard, self.attacker, old_pos, new_pos)
                piece.first_turn = False

        if isinstance(piece, King) or isinstance(piece, Rook):
            piece.has_moved = True

        if self.special_rules_handler.check_pawn_promotion(self.update_state_of_game):
            return True

    def move_execution(self, old_pos, new_pos):
        """
        Executes a move from old_pos to new_pos on the chessboard. This method handles piece capture,
        updates the board state, and invokes special move handling.

        :param old_pos: The starting position of the piece to be moved.
        :param new_pos: The destination position of the piece.
        :return: False if the move is invalid, True otherwise.
        """
        if not (old_pos and new_pos) or new_pos not in self.chessboard.board_state.keys():
            return False

        target_piece = self.chessboard.board_state.get(old_pos)

        captured_piece = self.chessboard.board_state.get(new_pos)

        if captured_piece:
            self.defender.captured_pieces.append(captured_piece)
            self.defender.alive_pieces.remove(captured_piece)

        self.chessboard.board_state[new_pos] = target_piece
        target_piece.position = new_pos
        self.chessboard.board_state[old_pos] = None
        if self.handle_special_moves(target_piece, old_pos, new_pos):
            return
        self.chessboard.last_moves.append((old_pos, new_pos))
        self.update_state_of_game()

    def use_castling(self, old_king_pos, new_king_pos):
        """
        Executes the castling move, updating the positions of the king and rook.

        :param old_king_pos: The original position of the king.
        :param new_king_pos: The new position of the king after castling.
        """
        self.special_rules_handler.perform_castling(old_king_pos, new_king_pos)
        self.update_state_of_game()

    def use_en_passant(self, old_pawn_pos, new_pawn_pos):
        """
        Executes the en passant move, capturing the opponent's pawn.

        :param old_pawn_pos: The original position of the pawn making the en passant move.
        :param new_pawn_pos: The new position of the pawn after completing the en passant move.
        """
        self.special_rules_handler.perform_en_passant(old_pawn_pos, new_pawn_pos)
        self.update_state_of_game()

    def on_player_switch(self, new_attacker, new_defender):
        """
        Handles the player switch, updating the attacker and defender.
        """
        self.attacker = new_attacker
        self.defender = new_defender
