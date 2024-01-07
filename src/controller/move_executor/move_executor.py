from src.model.chesspiece_types.pawn import Pawn
from src.model.chesspiece_types.king import King
from src.model.chesspiece_types.rook import Rook
from src.utils.helpers import PlayerSwitchObserver
from controller.move_executor.special_rules_handler import SpecialRulesHandler, check_en_passant


class MoveExecutor(PlayerSwitchObserver):
    """
    Class responsible for executing moves on the chessboard, handling piece capture,
    and updating the board state.
    """

    def __init__(self, chessboard, view, current_player, opponent, callback):
        self.chessboard = chessboard
        self.attacker = current_player
        self.defender = opponent
        self.special_rules_handler = SpecialRulesHandler(view, chessboard, self.attacker, self.defender)
        self.update_state_of_game = callback

    def handle_special_moves(self, piece, old_pos, new_pos):
        """
        Handles special moves for pieces like Pawn's first move, en passant, or castling.

        :param piece: The piece being moved.
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
        Executes a move from old_pos to new_pos, handles piece capture, and updates the board state.

        :param old_pos: Starting position of the piece to be moved.
        :param new_pos: Destination position of the piece.
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
        self.special_rules_handler.perform_castling(old_king_pos, new_king_pos)
        self.update_state_of_game()

    def use_en_passant(self, old_pawn_pos, new_pawn_pos):
        self.special_rules_handler.perform_en_passant(old_pawn_pos, new_pawn_pos)
        self.update_state_of_game()

    def on_player_switch(self, new_attacker, new_defender):
        self.attacker = new_attacker
        self.defender = new_defender
