from files.FEN import board_to_fen
from files.game import Game
from files.fen_strings import *
from misc.constants import *
from misc.miscellaneous import rowColToStdPositions
from misc.TempGame import TempGame

import pygame
import cProfile
import time
import pandas as pd
import csv

WIN = None
DEPTH = 5

POS_FILE = r"test/positions.txt"
POS_SPEC_FILE = r"test/pos_spec.txt"

def MoveGenerationTest(game, depth):
    '''Function to check how many possible positions there are'''
    if depth == 0:
        return 1, 0, 0, 0, 0, 0, 0
    positions = 0
    checks = 0
    castles = 0
    captures = 0
    enpassant = 0
    checkmates = 0
    promotions = 0
    moves = game.move_list 
    
    for move in moves:
        if move.get_promotion() and game.turn == 1:
            pass
        origin, dest = move.get_origin(), move.get_dest()
        
        o_piece = game.get_piece(origin)
        d_piece = game.get_piece(dest)

        if depth == 1:
            if o_piece != 0:
                if o_piece.type == king:
                    if abs(origin[1] - dest[1]) == 2:
                        castles += 1

            if d_piece != 0:
                captures += 1

            if o_piece != 0:
                if o_piece.type == pawn:
                    if d_piece == 0 and abs(dest[0] - origin[0]) == abs(dest[1] - origin[1]):
                        captures += 1
                        enpassant += 1
                    if move.get_promotion():
                        promotions += 1
            game.move(origin, dest, generate=True, move=move)

            if game.check != 0: 
                checks += 1
                # pos.write(board_to_fen(game.board.board))
                if game.winner:
                    if game.winner != 0:
                        # sp.write(board_to_fen(game.board.board))
                        checkmates+=1    
        
        else:
            game.move(origin, dest, move=move)
        
        result = MoveGenerationTest(game, depth-1)
        positions += result[0]
        captures += result[1]
        castles += result[2]
        enpassant += result[4]
        promotions += result[6]
        checks += result[3]
        checkmates += result[5]
        game.unmove()

    return positions, captures, castles, checks, enpassant, checkmates, promotions


def test():
    '''Main program for running the game'''

    run = True

    # Create board
    # game = Game(start_pos_fen, WIN)
    game = Game("r3k2r/Pppp1ppp/1b3nbN/nP6/BBP1P3/q4N2/Pp1P2PP/R2Q1RK1 w kq - 0 1", WIN)

    while run:

        game.generate_all_moves()
        print(game)
        for i in range(3, 4):
        # for i in range(0, DEPTH+1):
            print("Depth ", i, " ", end=" ")
            start = time.time()
            positions, captures, castles, checks, enpassant, checkmates, promotions = MoveGenerationTest(game, i)
            print("Positions: ", positions, " -- Captures: ", captures, " -- Castles: ", castles, " -- Checks: ", checks, " -- E.p: ", enpassant,
             " -- Checkmates: ", checkmates, " -- Promotions", promotions, " ", end="")
            end = time.time()
            print("Time: ", end-start)
            run = False


def rigourous_test():
    pos_num,depth,positions,captures,castles,checks,enpassant,checkmates,promotions = "pos_num","depth","positions","captures","castles","checks","enpassant","checkmates","promotions"
    perft = pd.read_csv("test\short_perft_test.csv")
    pos = []
    for i, row in perft.iterrows():
        if pos:
            if row[pos_num] != pos[-1]:
                pos.append(row[pos_num])
        else:
            pos.append(row[pos_num])
    output = open("test/output.csv", "w", newline="")
    w = csv.writer(output)
    w.writerow(["FEN", "depth", "positions", "captures", "castles", "checks","enpassant", "checkmates", "promotions"])
    
    count = 1
    for fen in pos:
        df = perft[(perft[pos_num] == fen)]
        depths = df[depth]
        depths = list(dict.fromkeys(depths))

        game = Game(fen, WIN)
        for d in depths:
            rs = df[df[depth] == d]
            positionsA, capturesA, castlesA, checksA, enpassantA, checkmatesA, promotionsA = MoveGenerationTest(game, int(d))
            results = [fen, d, positionsA, capturesA, castlesA, checksA, enpassantA, checkmatesA, promotionsA]
            w.writerow(results)
            print(count)
            count += 1
    
    output.close()

if __name__ == "__main__":
    inp = input("Test type: ")

    if inp == "n":
        # pos = open(POS_FILE, "w")
        # sp = open(POS_SPEC_FILE, "w")
        test()
        # sp.close()
        # pos.close()

    if inp == "r":
        rigourous_test()

    if inp == "t":
        pr = cProfile.Profile()
        pr.enable()

        # rigourous_test()
        test()
        pr.disable()
        pr.print_stats(sort='cumtime')

