# Runs our whole game

import pygame
from data.classes.Board import Board
from data.classes.Button import Button

pygame.init()

WINDOW_SIZE = (600, 600)
screen = pygame.display.set_mode(WINDOW_SIZE)
# promo_screen = pygame.display.set_mode([500, 500])
font = pygame.font.Font('freesansbold.ttf', 24)

board = Board(WINDOW_SIZE[0], WINDOW_SIZE[1])

def draw(display):
    display.fill("white")
    board.draw(display)
    pygame.display.update()

def draw_promo_menu(display, board):
    # Draw menu
    pygame.draw.rect(display, 'black', [100, 100, 300, 320])
    pygame.draw.rect(display, 'green', [100, 100, 300, 320], 5)
    pygame.draw.rect(display, 'white', [120, 120, 260, 40], 0, 5)
    pygame.draw.rect(display, 'gray', [120, 120, 260, 40], 5, 5)
    txt = font.render('Select Promotion', True, 'black')
    display.blit(txt, (135, 127))
    # Draw buttons on menu
    button1 = Button('Queen', (120, 180))
    button1.draw(display)
    button2 = Button('Rook', (120, 240))
    button2.draw(display)
    button3 = Button('Knight', (120, 300))
    button3.draw(display)
    button4 = Button('Bishop', (120, 360))
    button4.draw(display)
    pygame.display.update()
    # Handle button clicks
    if button1.check_clicked():
        board.promo_pick = "Queen"
    if button2.check_clicked():
        board.promo_pick = "Rook"
    if button3.check_clicked():
        board.promo_pick = "Knight"
    if button4.check_clicked():
        board.promo_pick = "Bishop"

if __name__ == "__main__":
    running = True
    while running:
        mx, my = pygame.mouse.get_pos()
        
        for event in pygame.event.get():
            # Quit the game if the user presses the close button
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # If the mouse is clicked
                if event.button == 1:
                    board.handle_click(mx, my)
        
        if board.is_in_checkmate("black"): # If black is in checkmate
            print("White wins!")
            running = False
        elif board.is_in_checkmate("white"): # If white is in checkmate
            print("Black wins!")
            running = False
        elif board.turn == "black" and not board.can_move("black"): # If black is in stalemate
            print("Stalemate!")
            running = False
        elif board.turn == "white" and not board.can_move("white"): # if white is in stalemate
            print("Stalemate!")
            running = False
        
        if board.promo == True:
            # Draw promo menu
            draw_promo_menu(screen, board)
            promo_piece = board.promo_piece
            promo_square = board.get_square_from_pos(promo_piece.pos)
            if board.promo_pick != None:
                if board.promo_pick == "Queen":
                    from data.classes.pieces.Queen import Queen
                    promo_square.occupying_piece = Queen(
                        (promo_piece.x, promo_piece.y),
                        promo_piece.color,
                        board
                    )
                elif board.promo_pick == "Rook":
                    from data.classes.pieces.Rook import Rook
                    promo_square.occupying_piece = Rook(
                        (promo_piece.x, promo_piece.y),
                        promo_piece.color,
                        board
                    )
                elif board.promo_pick == "Knight":
                    from data.classes.pieces.Knight import Knight
                    promo_square.occupying_piece = Knight(
                        (promo_piece.x, promo_piece.y),
                        promo_piece.color,
                        board
                    )
                elif board.promo_pick == "Bishop":
                    from data.classes.pieces.Bishop import Bishop
                    promo_square.occupying_piece = Bishop(
                        (promo_piece.x, promo_piece.y),
                        promo_piece.color,
                        board
                    )
                board.promo = False
                board.promo_pick = None
                board.promo_piece = None
        else:
            # Draw the board
            draw(screen)

