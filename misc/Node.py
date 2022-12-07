from misc.constants import*


class Node:
    def __init__(self, move, p_move, move_list, enPassantPiece, enPassant, check, cap_piece, p_piece, blackQueenSideCastle, blackKingSideCastle, whiteQueenSideCastle, whiteKingSideCastle, whiteThreatMap, blackThreatMap, promotion, winner):
        self.move = move
        self.cap_piece = cap_piece
        self.move_list = move_list
        self.enPassant = enPassant
        self.check = check
        self.p_piece = p_piece
        self.p_move = p_move
        self.enPassantPiece = enPassantPiece

        self.blackKingSideCastle = blackKingSideCastle
        self.blackQueenSideCastle = blackQueenSideCastle
        self.whiteKingSideCastle = whiteKingSideCastle
        self.whiteQueenSideCastle = whiteQueenSideCastle

        self.whiteThreatMap = whiteThreatMap
        self.blackThreatMap = blackThreatMap

        self.promotion = promotion

        self.winner = winner

    def getCapPiece(self):
        return self.cap_piece

    def getMove(self):
        return self.move

    def getMoveList(self):
        return self.move_list

    def getEnPassant(self):
        return self.enPassant

    def getCheck(self):
        return self.check

    def getP_piece(self):
        return self.p_piece

    def getP_move(self):
        return self.p_move

    def getEnPassantPiece(self):
        return self.enPassantPiece

    def getBlackQueenSideCastle(self):
        return self.blackQueenSideCastle

    def getBlackKingSideCastle(self):
        return self.blackKingSideCastle

    def getWhiteQueenSideCastle(self):
        return self.whiteQueenSideCastle

    def getWhiteKingSideCastle(self):
        return self.whiteKingSideCastle

    def getWhiteThreatMap(self):
        return self.whiteThreatMap

    def getBlackThreatMap(self):
        return self.blackThreatMap

    def getPromotion(self):
        return self.promotion
    
    def getWinner(self):
        return self.winner
