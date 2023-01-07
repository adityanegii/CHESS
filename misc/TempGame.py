import pygame
from misc.constants import*
from misc.miscellaneous import *
from files.board import Board
from files.FEN import board_to_fen
from files.MoveGenerator import MoveGenerator

class TempGame():
    def __init__(self, fen, win):
        self.board = Board(fen)
        self.turn = self.board.turn
        self.num_of_moves = 0
        self.win = win

        self.winner = None

    def draw(self):
        '''Method to draw board, call draw method of Board object'''
        self.board.draw_squares(self.win)