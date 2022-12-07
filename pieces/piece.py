import pygame

from misc.constants import *
from misc.miscellaneous import get_key
from abc import ABC, abstractmethod


class Piece (ABC):
    def __init__(self, number, row, col):
        self.row = row
        self.col = col
        if number > 0:
            self.color = black_piece
            self.type = number
        else:
            self.color = white_piece
            self.type = -number

        self.pos()
        self.position = self.row*8 + self.col

        self.pinned = False

    def pos(self):
        '''Method to calculate the position of the piece'''
        self.x = SQUARE_SIZE * self.col + SQUARE_SIZE // 2
        self.y = SQUARE_SIZE * self.row + SQUARE_SIZE // 2
        self.position = self.row*8 + self.col

    def draw(self, win):
        '''Method to draw out the piece'''
        if self.color == white_piece:
            width, height = W_IMGS[self.type - 1].get_size()
            win.blit(W_IMGS[self.type - 1], (self.x -
                     width // 2, self.y - height // 2))
        else:
            width, height = B_IMGS[self.type - 1].get_size()
            win.blit(B_IMGS[self.type - 1], (self.x -
                     width // 2, self.y - height // 2))

    def move(self, pos):
        '''Method to update a piece's position'''
        row, col = pos
        if self.type == pawn:
            if abs(row - self.row) == 2:
                self.en_passant = True
        self.row = row
        self.col = col
        self.pos()
        if self.type == king or self.type == rook:
            self.castle = False

    def get_pos(self):
        '''Method to get row and col'''
        return (self.row, self.col)

    @abstractmethod
    def find_moves(self, board):
        pass
    
    def __repr__(self) -> str:
        symbol = get_key(symbol2num, self.type)
        if self.color == white_piece:
            return symbol.upper()
        else:
            return symbol
