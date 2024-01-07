from PyQt6.QtCore import pyqtSignal, QObject

from src.model.chesspiece_types.pawn import Pawn
from src.model.chesspiece_types.king import King
from src.model.baseplayer.player import Player
from controller.move_validator.move_safety_checker import MoveSafetyChecker
from utils.helpers import get_key_by_value, update_possible_moves, PlayerSwitchObserver


class MoveValidator(QObject, PlayerSwitchObserver):
    stalemate_signal = pyqtSignal(str)
    """
    The MoveValidator class is responsible for validating chess piece movements and
    updating potential moves based on the current state of the chessboard.
    """

    def __init__(self, chessboard, current_player, opponent):

        super().__init__()
        self.chessboard = chessboard
        self.attacker = current_player
        self.defender = opponent
        self.move_safety_checker = MoveSafetyChecker(chessboard, current_player, opponent)

    def give_king_pos(self):
        for pos, piece in self.chessboard.board_state.items():
            if isinstance(piece, King):
                if isinstance(self.attacker, Player) and self.attacker.team == piece.team:
                    self.attacker.king_position = pos
                elif isinstance(self.defender, Player):
                    self.defender.king_position = pos

    def get_alive_pieces(self):
        for player in [self.attacker, self.defender]:
            player.get_alive_pieces(self.chessboard)

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
        for piece in self.defender.coverage_areas.keys():
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

    def filter_king_moves(self):
        moves_to_discard = set()
        king = self.chessboard.board_state.get(self.attacker.king_position)

        for piece, moves in self.defender.coverage_areas.items():
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

    def stalemate(self, view):
        stalemate = True

        for piece in self.attacker.alive_pieces:
            if piece:
                if len(piece.possible_moves) >= 1:
                    stalemate = False
                    break

        if stalemate:
            last_move, new_move = self.chessboard.last_moves[-1]

            piece_that_set_check = self.chessboard.board_state.get(new_move)
            piece_name = piece_that_set_check.__class__.__name__.lower()
            team_name = piece_that_set_check.team.name.lower()
            svg_path = f"assets/{team_name}_{piece_name}.svg"

            if last_move and new_move:

                for label in view.labels:
                    if label:
                        if label.objectName() == last_move:
                            label.set_svg("")

                        elif label.objectName() == new_move:
                            label.set_svg(svg_path)

            winning_player = f"Spieler {self.defender.team.name.capitalize()}"
            self.stalemate_signal.emit(winning_player)

    def on_player_switch(self, new_attacker, new_defender):
        self.attacker = new_attacker
        self.defender = new_defender
