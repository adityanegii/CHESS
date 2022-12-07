import pygame
from misc.constants import ROWS, WIDTH, HEIGHT
from files.game import Game
from files.fen_strings import *
import time
from files.FEN import board_to_fen


FPS = 60

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('CHESS')

pygame.font.init()
font = pygame.font.SysFont('Comic Sans MS', 60)


def get_click_pos(pos):
    '''Get the row and col that were clicked on'''
    col = pos[0] // 100
    row = pos[1] // 100
    return (row, col)


def end_screen(game, run):
    '''Get the end screen when game is won'''
    if game.winner == -1:
        print("White Wins")
        time.sleep(2)
        return False
    elif game.winner == 1:
        print("Black Wins")
        time.sleep(2)
        return False
    elif game.winner == 0:
        print("Stalemate")
        time.sleep(2)
        return False
    return True


def main():
    '''Main program for running the game'''
    run = True
    clock = pygame.time.Clock()

    # Create board
    game = Game(start_pos_fen, WIN) 
    # game = Game("r3k2r/p1ppqpb1/bn2pnp1/3PN3/1p2P3/2N2Q1p/PPPBBPPP/R3K2R w KQkq - 0 1", WIN) 
    #game.board.draw_squares(WIN)
    piece_pos = None

    while run:
        game.draw()
        game.draw_moves(piece_pos)
        clock.tick(FPS)
        pygame.display.update()

        if game.winner != None:
            run = end_screen(game, run)

        for event in pygame.event.get():

            # Quit the game
            if event.type == pygame.QUIT:
                run = False

            # If mouse button is clicked
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                temp_pos = get_click_pos(mouse_pos)
                if piece_pos == None:
                    piece_pos = temp_pos
                else:
                    game.move(piece_pos, temp_pos, False)
                    piece_pos = None

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    game.unmove()
                elif event.key == pygame.K_RIGHT:
                    print(game)
                elif event.key == pygame.K_DOWN:
                    print(board_to_fen(game.board.board))
                elif event.key == pygame.K_UP:
                    prev = 0
                    print("White Threat Map")
                    for row in range(ROWS):
                        print(game.whiteThreatMap[prev:prev+8])
                        prev += 8
                    print("Black Threat Map")
                    prev = 0
                    for row in range(ROWS):
                        print(game.blackThreatMap[prev:prev+8])
                        prev += 8
                elif event.key == pygame.K_a:
                    prev = 0
                    for row in range(ROWS):
                        next = prev+8
                        print(game.list_of_pieces[prev:next])
                        prev = next
    pygame.quit()


main()
