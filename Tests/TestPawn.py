from data.classes.pieces.Pawn import Pawn
from data.classes.Board import Board


WINDOW_SIZE = (600, 600)
# screen = pygame.display.set_mode(WINDOW_SIZE)

board = Board(WINDOW_SIZE[0], WINDOW_SIZE[1])

position = board.config = [
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
            ["bP", "bP", "bP", "bP", "bP", "bP", "bP", "bP"],
            ["", "", "", "", "", "", "", ""],
            ["", "", "", "", "", "", "", ""],
            ["", "", "", "", "", "", "", ""],
            ["", "", "bQ", "", "", "", "", ""],
            ["wP", "wP", "wP", "wP", "wP", "wP", "wP", "wP"],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"],
        ]
# print(position)

board.setup_board()

b6 = board.get_square_from_pos((1, 5))
# print(f"b6: {b6.occupying_piece}")

pawn = Pawn((1, 6), "white", board)
# pawn2 = Pawn((0,5), "white", board)

moves = pawn.get_moves(board)

print(f"Moves: {[i.coord for i in moves]}")

possible_moves = [i.coord for i in pawn.get_possible_moves(board)]

print(f"Possible Moves: {possible_moves}")

attacking_squares = pawn.attacking_squares(board)

print(f"Attacking Moves: {[i.coord for i in moves if i.x != pawn.x]}")
