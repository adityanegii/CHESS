from .constants import *


class Move:
    def __init__(self, origin, dest, enPassant=False, promotion=None, castle=False):
        self.origin = origin
        self.dest = dest
        self.promotion = promotion
        self.enPassant = enPassant
        self.castle = castle

    def get_origin(self):
        return self.origin

    def get_dest(self):
        return self.dest

    def get_promotion(self):
        return self.promotion

    def get_enpassant(self):
        return self.enPassant

    def get_castle(self):
        return self.castle
        
    def find_equivalent(self, move):
        origin, dest = move
        if origin == self.origin and dest == self.dest:
            return True
        else:
            return False
