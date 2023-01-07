import sys
from misc.miscellaneous import stdPositionsToRowCol
from files.game import Game

from misc.constants import *
from misc.miscellaneous import rowColToStdPositions


def MoveGenerationTest(game, depth, og_depth=0):
    '''Function to check how many possible positions there are'''
    if depth == 0:
        return 1
    positions = 0
    temp = 0
    moves = game.move_list
    for move in moves:
        if move.get_promotion() and game.turn == 1:
            pass

        game.move(move.get_origin(), move.get_dest(), move=move)
        
        result = MoveGenerationTest(game, depth-1)
        positions += result
        
        promote = ""
        if move.get_promotion() != None:
            for key, val in symbol2num.items():
                if val == move.get_promotion():
                    promote = key
        game.unmove()
        if depth == og_depth:
            print(rowColToStdPositions(move.get_origin()) + rowColToStdPositions(move.get_dest()) + promote + ": " + str(positions-temp))
            temp = positions

    return positions

if __name__ == "__main__":
    game = None
    print("Test App")
    while True:
        user_input = input()
        if user_input:
            if user_input.startswith("position fen"):
                fen = user_input[13:]
                game = Game(fen, None)
            elif user_input.startswith("d"):
                if game:
                    print(game)
            elif user_input.startswith("go perft"):
                if game:
                    depth = int(user_input[8:])
                    positions = MoveGenerationTest(game, depth, depth)
                    print(positions)
            elif user_input.startswith("move"):
                origin , dest = stdPositionsToRowCol(user_input[5:7]), stdPositionsToRowCol(user_input[7:9])
                if game:
                    game.move(origin, dest, False)
            elif user_input.startswith("exit"):
                sys.exit()
            else:
                print("Not valid command")