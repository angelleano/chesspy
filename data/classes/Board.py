# Board class to handle tiles and board

import pygame
from data.classes.Square import Square
from data.classes.pieces.Bishop import Bishop
from data.classes.pieces.King import King
from data.classes.pieces.Knight import Knight
from data.classes.pieces.Pawn import Pawn
from data.classes.pieces.Queen import Queen
from data.classes.pieces.Rook import Rook

# Gets available positions between 2 positions connected in straight line
def get_coordinates_between(start, end):
    
    start_x, start_y = start
    end_x, end_y = end

    # Calculate the direction of the line
    dx = end_x - start_x
    dy = end_y - start_y
    
    # Ensure that the line is diagonal or horizontal/vertical
    if abs(dx) != abs(dy) and dx != 0 and dy != 0:
        return None
    
    # Determine the step size for x and y
    step_x = 1 if dx > 0 else -1 if dx < 0 else 0
    step_y = 1 if dy > 0 else -1 if dy < 0 else 0
    
    coordinates = []
    start_x += step_x
    start_y += step_y
    x, y = start_x, start_y
    
    while x != end_x or y != end_y:
        coordinates.append((x, y))
        x += step_x
        y += step_y
    
    return coordinates

# Game state checker
class Board:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.tile_width = width // 8
        self.tile_height = height // 8
        self.selected_piece = None
        self.turn = "white"
        self.config = [
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
            ["bP", "bP", "bP", "bP", "bP", "bP", "bP", "bP"],
            ["", "", "", "", "", "", "", ""],
            ["", "", "", "", "", "", "", ""],
            ["", "", "", "", "", "", "", ""],
            ["", "", "", "", "", "", "", ""],
            ["wP", "wP", "wP", "wP", "wP", "wP", "wP", "wP"],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"],
        ]
        self.squares = self.generate_squares()
        self.setup_board()

    def generate_squares(self):
        output = []
        for y in range(8):
            for x in range(8):
                output.append(
                    Square(x, y, self.tile_width, self.tile_height)
                    )
        return output
    
    def get_square_from_pos(self, pos):
        for square in self.squares:
            if (square.x, square.y) == (pos[0], pos[1]):
                return square
            
    def get_piece_from_pos(self, pos):
        return self.get_square_from_pos(pos).occupying_piece
    
    def setup_board(self):
        for y, row in enumerate(self.config):
            for x, piece in enumerate(row):
                if piece != "":
                    square = self.get_square_from_pos((x, y))
                    
                    if piece[1] == "R":
                        square.occupying_piece = Rook(
                            (x, y), "white" if piece[0] == "w" else "black", self
                        )
                    elif piece[1] == "N":
                        square.occupying_piece = Knight(
                            (x, y), "white" if piece[0] == "w" else "black", self
                        )
                    elif piece[1] == "B":
                        square.occupying_piece = Bishop(
                            (x, y), "white" if piece[0] == "w" else "black", self
                        )
                    elif piece[1] == "Q":
                        square.occupying_piece = Queen(
                            (x, y), "white" if piece[0] == "w" else "black", self
                        )
                    elif piece[1] == "K":
                        square.occupying_piece = King(
                            (x, y), "white" if piece[0] == "w" else "black", self
                        )
                    elif piece[1] == "P":
                        square.occupying_piece = Pawn(
                            (x, y), "white" if piece[0] == "w" else "black", self
                        )
    
    def handle_click(self, mx, my):
        x = mx // self.tile_width
        y = my //self.tile_height
        clicked_square = self.get_square_from_pos((x, y))
        if self.selected_piece is None:
            if clicked_square.occupying_piece is not None:
                if clicked_square.occupying_piece.color == self.turn:
                    self.selected_piece = clicked_square.occupying_piece
        elif self.selected_piece.move(self, clicked_square):
            self.turn = "white" if self.turn == "black" else "black"
        elif clicked_square.occupying_piece is not None:
            if clicked_square.occupying_piece.color == self.turn:
                self.selected_piece = clicked_square.occupying_piece

    def can_block(self, start, end): # (start, end) = ((x1, y1), (x2, y2))
        attack_line = get_coordinates_between(start, end)
        if attack_line == None:
            return False
        
        pos_scope = {
            square.occupying_piece: [move.pos for move in square.occupying_piece.get_moves(self)] 
            for square in self.squares 
            if square.occupying_piece is not None and len(square.occupying_piece.get_moves(self)) > 0
            }

        for atpos in attack_line:
            for scope in pos_scope.values():
                if atpos in scope:
                    return True
        return False

    def get_agro_agents(self, target): # target = (x, y)
        # All pieces and their valid moves
        pos_scope = {
            square.occupying_piece: [move.pos for move in square.occupying_piece.get_valid_moves(self)] 
            for square in self.squares 
            if square.occupying_piece is not None and len(square.occupying_piece.get_valid_moves(self)) > 0
            }
        possible_attackers = []

        # Find which pieces can attack target
        for piece, scope in pos_scope.items():
            try:
                if scope.index(target) >= 0:
                    possible_attackers.append(piece)
            except ValueError:
                pass

        return possible_attackers # possible_attackers = [Piece(), Piece()]

    def is_in_check(self, color, board_change=None): # board_change = [(x1, y1), (x2, y2)]
        output = False
        king_pos = None
        changing_piece = None
        old_square = None
        new_square = None
        new_square_old_piece = None
        if board_change is not None:
            for square in self.squares:
                if square.pos == board_change[0]:
                    changing_piece = square.occupying_piece
                    old_square = square
                    old_square.occupying_piece = None
            for square in self.squares:
                if square.pos == board_change[1]:
                    new_square = square
                    new_square_old_piece = new_square.occupying_piece
                    new_square.occupying_piece = changing_piece
        pieces = [
            i.occupying_piece for i in self.squares if i.occupying_piece is not None
        ]
        if changing_piece is not None:
            if changing_piece.notation == "K":
                king_pos = new_square.pos
        if king_pos == None:
            for piece in pieces:
                if piece.notation == "K" and piece.color == color:
                    king_pos = piece.pos
        for piece in pieces:
            if piece.color != color:
                for square in piece.attacking_squares(self):
                    if square.pos == king_pos:
                        output = True
        if board_change is not None:
            old_square.occupying_piece = changing_piece
            new_square.occupying_piece = new_square_old_piece
        return output
    
    def is_in_checkmate(self, color):
        output = False
        for piece in [i.occupying_piece for i in self.squares]:
            if piece != None:
                if piece.notation == "K" and piece.color == color:
                    king = piece
        if king.get_valid_moves(self) == []:
            if self.is_in_check(color):
                aggresors = self.get_agro_agents(king.pos)
                if len(aggresors) == 1:
                    if len(self.get_agro_agents(aggresors[0].pos)) > 0:
                        pass
                    elif not self.can_block(aggresors[0].pos, king.pos):
                        output = True
                else:
                    output = True
        return output
    
    def draw(self, display):
        if self.selected_piece is not None:
            self.get_square_from_pos(self.selected_piece.pos).highlight = True
            for square in self.selected_piece.get_valid_moves(self):
                square.highlight = True
        for square in self.squares:
            square.draw(display)