from src.model.baseplayer.chesspiece import ChessPiece


class Pawn(ChessPiece):

    def __init__(self, team):
        super().__init__(team)

        self.first_turn = True
        self.en_passant = False

    def possible_movements(self, chessboard):
        self.find_position_of_current_piece(chessboard)
        if self.position is None:
            return

        alpha, numb = self.position
        numb = int(numb)

        direction = -1 if self.team.name == "BLACK" else 1

        numb1 = numb + direction
        square = alpha + str(numb1)

        if square in chessboard.board_state.keys():

            if chessboard.board_state.get(square) is None:
                self.possible_moves.add(square)

                numb2 = numb + 2 * direction
                square = alpha + str(numb2)

                if self.first_turn and chessboard.board_state.get(square) is None:
                    self.possible_moves.add(square)

        for offset in [-1, 1]:
            new_alpha = chr(ord(alpha) + offset)
            new_numb = numb + direction
            if 'A' <= new_alpha <= 'H':
                diag_square = new_alpha + str(new_numb)

                if diag_square in chessboard.board_state:
                    target_char = chessboard.board_state.get(diag_square)
                    if target_char is not None and self.team.name != target_char.team.name:
                        self.possible_moves.add(diag_square)

    def add_diagonal_moves(self, chessboard):
        self.find_position_of_current_piece(chessboard)
        if self.position:
            alpha, numb = self.position
            numb = int(numb)
            direction = -1 if self.team.name == "BLACK" else 1

            for offset in [-1, 1]:
                new_alpha = chr(ord(alpha) + offset)
                new_numb = numb + direction
                if 'A' <= new_alpha <= 'H':
                    diag_square = new_alpha + str(new_numb)

                    if diag_square in chessboard.board_state:
                        self.possible_moves.add(diag_square)

