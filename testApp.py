import sys
from misc.miscellaneous import stdPositionsToRowCol
from test import MoveGenerationTest
from files.game import Game

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
                    positions = MoveGenerationTest(game, depth, depth)[0]
                    print(positions)
            elif user_input.startswith("move"):
                origin , dest = stdPositionsToRowCol(user_input[5:7]), stdPositionsToRowCol(user_input[7:9])
                if game:
                    game.move(origin, dest, False)
            elif user_input.startswith("exit"):
                sys.exit()
            else:
                print("Not valid command")