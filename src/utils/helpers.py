from enum import Enum


def get_piece_name_for_square(square_name):
    if square_name is not None:

        piece_names = {
            "A1": "white_rook", "B1": "white_knight", "C1": "white_bishop", "D1": "white_queen", "E1": "white_king",
            "F1": "white_bishop", "G1": "white_knight", "H1": "white_rook",
            "A2": "white_pawn", "B2": "white_pawn", "C2": "white_pawn", "D2": "white_pawn",
            "E2": "white_pawn", "F2": "white_pawn", "G2": "white_pawn", "H2": "white_pawn",
            "A3": None, "B3": None, "C3": None, "D3": None,
            "E3": None, "F3": None, "G3": None, "H3": None,
            "A4": None, "B4": None, "C4": None, "D4": None,
            "E4": None, "F4": None, "G4": None, "H4": None,
            "A5": None, "B5": None, "C5": None, "D5": None,
            "E5": None, "F5": None, "G5": None, "H5": None,
            "A6": None, "B6": None, "C6": None, "D6": None,
            "E6": None, "F6": None, "G6": None, "H6": None,
            "A7": "black_pawn", "B7": "black_pawn", "C7": "black_pawn", "D7": "black_pawn",
            "E7": "black_pawn", "F7": "black_pawn", "G7": "black_pawn", "H7": "black_pawn",
            "A8": "black_rook", "B8": "black_knight", "C8": "black_bishop", "D8": "black_queen", "E8": "black_king",
            "F8": "black_bishop", "G8": "black_knight", "H8": "black_rook"
        }

        if square_name in piece_names.keys():
            if piece_names[square_name] is not None:
                return piece_names.get(square_name, "")
        else:
            print(square_name)
            raise ValueError

    return None


class PieceTeam(Enum):
    WHITE = "white"
    BLACK = "black"


class CommonMovements:

    def check_and_append_moves(self, chess_piece, chessboard, alpha, numb, alpha_step, numb_step):

        new_alpha, new_numb = alpha, numb

        for _ in range(8):
            new_alpha = chr(ord(new_alpha) + alpha_step)
            new_numb += numb_step

            target_char = chessboard.save_chars_and_positions.get((new_alpha + str(new_numb)))

            if target_char is not None:
                chess_piece.possible_moves_without_knowing_board.append((new_alpha, new_numb))
                return
            else:
                chess_piece.possible_moves_without_knowing_board.append((new_alpha, new_numb))
