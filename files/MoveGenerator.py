from re import L
from misc.Move import Move
from misc.constants import*

ROW = 0
COL = 1

def pin_move_validator(p_row, p_col, k_row, k_col, d_pos):
    '''Check if the move to be made will undo a pin. Return True if the move does not undo a pin, False otherwise.'''
    # Find the piece's position relative to the king
    d_row, d_col = pos_getter[d_pos]
    if p_row*8+p_col < k_row*8+k_col:
        # Left
        if p_row == k_row:
            if d_row == k_row and d_col < k_col:
                return True
        # Top
        elif p_col == k_col:
            if d_col == k_col and d_row < k_row:
                return True
        # Top left
        elif abs(p_row - k_row) == abs(p_col - k_col) and p_col < k_col:
            if abs(d_row - k_row) == abs(d_col - k_col) and d_col < k_col:
                return True
        # Top right
        elif abs(p_row - k_row) == abs(p_col - k_col) and p_col > k_col:
            if abs(d_row - k_row) == abs(d_col - k_col) and d_col > k_col:
                return True
    else:
        # Right
        if p_row == k_row:
            if d_row == k_row and d_col > k_col:
                return True
        # Bottom
        elif p_col == k_col:
            if d_col == k_col and d_row > k_row:
                return True
        # Bottom left
        elif abs(p_row - k_row) == abs(p_col - k_col) and p_col < k_col:
            if abs(d_row - k_row) == abs(d_col - k_col) and d_col < k_col:
                return True
        # Bottom right
        elif abs(p_row - k_row) == abs(p_col - k_col) and p_col > k_col:
            if abs(d_row - k_row) == abs(d_col - k_col) and d_col > k_col:
                return True
    return False

def check_blocker_move(a_row, a_col, k_row, k_col, d_pos):
    '''Check if the move is blocking the check or not'''  
    # If checking piece is right next to the king (no way to block)
    if abs(a_row-k_row) == 1 and abs(a_col-k_col) == 1:
        return False
    d_row, d_col = pos_getter[d_pos]
    if a_row*8+a_col < k_row*8+k_col:
        # Left check
        if a_row == k_row:
            if d_col in range(a_col, k_col) and d_row == k_row:
                return True
        # Top check
        elif a_col == k_col:
            if d_row in range(a_row, k_row) and d_col == k_col:
                return True
        # Top left check
        elif abs(a_row - k_row) == abs(a_col - k_col) and a_col < k_col:
            if abs(d_row - k_row) == abs(d_col - k_col) and d_col in range(a_col, k_col) and d_row in range(a_row, k_row):
                return True
        # Top right check
        elif abs(a_row - k_row) == abs(a_col - k_col) and a_col > k_col:
            if abs(d_row - k_row) == abs(d_col - k_col) and d_col in range(k_col, a_col) and d_row in range(a_row, k_row):
                return True
    else:
        # Right check
        if a_row == k_row:
            if d_col in range(k_col+1, a_col) and d_row == k_row:
                return True
        # Down check
        elif a_col == k_col:
            if d_row in range(k_row+1, a_row) and d_col == k_col:
                return True
        # Bottom left check
        elif abs(a_row - k_row) == abs(a_col - k_col) and a_col < k_col:
            if abs(d_row - k_row) == abs(d_col - k_col) and d_col in range(a_col, k_col) and d_row in range(k_row+1, a_row):
                return True
        # Bottom right check
        elif abs(a_row - k_row) == abs(a_col - k_col) and a_col > k_col:
            if abs(d_row - k_row) == abs(d_col - k_col) and d_col in range(k_col, a_col) and d_row in range(k_row+1, a_row):
                return True
    return False

def validate_en_passant(pRow, pCol, cap_piece_pos, kRow, kCol, game):
    '''Function to validate en passant moves. Returns True if the move is valid, False otherwise.'''
    # pS = []     # list of pieces on that particular row between the king and the rook/queen of there is one
    # if pRow == kRow:
    #     if pCol < kCol:
    #         for i in range(1, pCol + 1):
    #             nCol = pCol - i
    #             piece = game.get_piece((pRow, nCol))
    #             if piece != 0:
    #                 pS.append(piece)
    #                 if piece.type == pawn and pRow * 8 + nCol == cap_piece_pos:
    #                     continue
    #                 elif piece.type != rook and piece.type != queen:
    #                     return True
    #                 else:
    #                     return False
    #     else:
    #         for i in range(1, ROWS-pCol+1):
    #             nCol = pCol + i
    #             piece = game.get_piece((pRow, nCol))
    #             if piece!= 0:
    #                 if piece.type == pawn and pRow * 8 + nCol == cap_piece_pos:
    #                     continue
    #                 elif piece.type != rook and piece.type != queen:
    #                     return True
    #                 else:
    #                     return False
    # return True
    if pRow == kRow:
        found = 0
        if pCol < kCol:
            for i in range(1, kCol + 1):
                nCol = kCol - i
                p = game.get_piece((pRow, nCol))
                if p != 0:
                    found += 1
                    if (p.type == rook or p.type == queen) and p.color != game.turn and found == 3:
                        return False
                if found == 3:
                    break
        else:
            for i in range(kCol, COLS):
                nCol = pCol + i
                p = game.get_piece((pRow, nCol))
                if p != 0:
                    found += 1
                    if (p.type == rook or p.type == queen) and p.color != game.turn and found == 3:
                        return False
                if found == 3:
                    break
    return True    

def MoveGenerator(game):
    '''This function generates all the moves according to the attack maps for the color that is moving.
    It contains sub-functions to generate the moves for each type of piece.'''
    # Setup the move generator
    move_list = []  # Return this

    if game.turn == white_piece:
        pieces = game.whitePieces
        kingLocation = game.get_white_king_location()
        aMap = game.blackThreatMap
    else:
        pieces = game.blackPieces
        kingLocation = game.get_black_king_location()
        aMap = game.whiteThreatMap
    
    k_row, k_col = kingLocation
    k_pos = k_row*8 + k_col

    checkers = game.checkers
    if len(checkers) > 0:
        attacker = checkers[0]
        a_row, a_col, a_pos = attacker.row, attacker.col, attacker.position


    # Nested functions to get moves for the pieces
    # Case 1: normal
    # Case 2: 1 checker (not knight)
    # Case 3: 1 checker (knight) --> not blockable

    def pawn_moves(piece, case):
        valid = True
        pos = piece.position

        m1 = pos+8*piece.color
        if piece.color == black_piece:
            m2 = pos+7*piece.color
            m3 = pos+9*piece.color
        else:
            m2 = pos+9*piece.color
            m3 = pos+7*piece.color
        m4 = None

        move1 = game.get_piece_from_pos(m1)
        cap1 = None
        cap2 = None

        # Starting move (2 spaces)
        move2 = None
        if (piece.color == white_piece and piece.row == 6) or (piece.color == black_piece and piece.row == 1):
            if move1 == 0:
                if game.get_piece_from_pos(m1+8*piece.color) == 0:
                    m4 = pos+8*2*piece.color
                    move2 = game.get_piece_from_pos(m4)

            
        enp1 = None
        enp2 = None
        enpd1 = None
        enpd2 = None

        if piece.col < 7 and ((piece.row == 4 and piece.color == black_piece) or (piece.row == 3 and piece.color == white_piece)):
            enp_piece1 = game.get_piece_from_pos(piece.row*8+piece.col+1)
            if enp_piece1 != 0:
                if enp_piece1.color != piece.color and enp_piece1.type == pawn:
                    pO, pD = game.p_move
                    pOx, pOy = pO
                    pDx, pDy = pD
                    if pDy == pOy and abs(pOx - pDx) == 2 and pD == (enp_piece1.row, enp_piece1.col):
                        enp1 = (piece.row+piece.color)*8+piece.col+1
        
        if piece.col > 0 and ((piece.row == 4 and piece.color == black_piece) or (piece.row == 3 and piece.color == white_piece)):
            enp_piece2 = game.get_piece_from_pos(piece.row*8+piece.col-1)
            if enp_piece2 != 0:
                if enp_piece2.color != piece.color and enp_piece2.type == pawn:
                    pO, pD = game.p_move
                    pOx, pOy = pO
                    pDx, pDy = pD
                    if pDy == pOy and abs(pOx - pDx) == 2 and pD == (enp_piece2.row, enp_piece2.col):
                        enp1 = (piece.row+piece.color)*8+piece.col-1   

        if piece.col < 7:
            cap2 = game.get_piece_from_pos(m3)
        if piece.col > 0:
            cap1 = game.get_piece_from_pos(m2)
        if cap2 == 0 or cap2 is None:
            m3 = None
        if cap1 == 0 or cap1 is None:
            m2 = None

        moves = [m1, m2, m3, m4, enp1, enp2]
        dests = [move1, cap1, cap2, move2, enpd1, enpd2]
        
        for move, dest in zip(moves, dests):
            if move is not None:
                valid = True
                if piece.pinned:
                    valid = pin_move_validator(piece.row, piece.col, k_row, k_col, move)
                if valid:
                    # Promoting moves
                    new_move = []
                    if (piece.row == 6 and piece.color == black_piece) or (piece.row == 1 and piece.color == white_piece):
                        if move in (m2, m3):
                            if dest != 0:
                                if dest.color != piece.color:
                                    for code in promotion_list:
                                        new_move.append(Move((piece.row, piece.col), (dest.row, dest.col), promotion=code))
                        else:
                            for code in promotion_list:
                                if game.get_piece_from_pos(move) == 0:
                                    new_move.append(Move((piece.row, piece.col), (piece.row + piece.color, piece.col), promotion=code))
                    # En passant move
                    elif move in (enp1, enp2):
                        if validate_en_passant(piece.row, piece.col, move-8*piece.color, k_row, k_col, game):
                            new_move.append(Move((piece.row, piece.col), pos_getter[move], enPassant=True))
                    else:
                        # Capturing move
                        if move in (m2, m3):
                            if dest != 0:
                                if dest.color != piece.color:
                                    new_move.append(Move((piece.row, piece.col), (dest.row, dest.col)))
                        else:
                            if game.get_piece_from_pos(move) == 0:
                                new_move.append(Move((piece.row, piece.col), pos_getter[move]))
                    
                    if new_move:
                        if len(new_move) == 1:
                            if case == 1:
                                move_list.append(new_move[0])
                            if case == 2:
                                if dest == attacker:
                                    move_list.append(new_move[0])
                                elif check_blocker_move(a_row, a_col, k_row, k_col, move):
                                    move_list.append(new_move[0])
                                elif move in (enp1, enp2) and attacker.type == pawn:
                                    move_list.append(new_move[0])
                            if case == 3:
                                if dest == attacker:
                                    move_list.append(new_move[0])
                        else:
                            if case == 1:
                                for n_m in new_move:
                                    move_list.append(n_m)
                            if case == 2:
                                if dest == attacker:
                                    for n_m in new_move:
                                        move_list.append(n_m)
                                elif check_blocker_move(a_row, a_col, k_row, k_col, move):
                                    for n_m in new_move:
                                        move_list.append(n_m)
                            if case == 3:
                                if dest == attacker:
                                    for n_m in new_move:
                                        move_list.append(n_m)

    def knight_moves(piece, case):
        if not piece.pinned:
            t_moves = k_moves
            for move in t_moves:
                x, y = move
                x += piece.row
                y += piece.col
                dest = game.get_piece((x, y))
                if x >= 0 and y >= 0 and x <= 7 and y <= 7:
                    if case == 1:
                        if dest != 0:
                            if dest.color == piece.color:
                                continue
                            else:
                                move_list.append(Move((piece.row, piece.col), (x, y)))
                        else:
                            move_list.append(Move((piece.row, piece.col), (x, y)))
                    elif case == 2:
                        if dest == attacker:
                            move_list.append(Move((piece.row, piece.col), (x, y)))
                        elif check_blocker_move(a_row, a_col, k_row, k_col, x*8+y):
                            move_list.append(Move((piece.row, piece.col), (x, y)))
                    elif case == 3:
                        if dest == attacker:
                            move_list.append(Move((piece.row, piece.col), (x, y)))
                            
    def diag_sliding_moves(piece, case):
        pos = piece.position
        start_rem = pos % 8
        for direction in diagonal_squares:
            for i in range(1, 8):
                n_pos = pos + direction * i
                n_rem = n_pos % 8
                if n_pos not in range(0, 64):
                    break
                if n_rem > start_rem and (direction == -9 or direction == 7):
                    break
                if n_rem < start_rem and (direction == -7 or direction == 9):
                    break
                dest = game.get_piece_from_pos(n_pos)
                if dest != 0:
                    if dest.color == piece.color:
                        break
                valid = True
                if piece.pinned:
                    valid = pin_move_validator(piece.row, piece.col, k_row, k_col, n_pos)
                if valid:
                    if case == 1:
                        move_list.append(Move((piece.row, piece.col), pos_getter[n_pos]))
                        if dest != 0:
                            if dest.color != piece.color:
                                break
                    elif case == 2:
                        if dest == attacker:
                            move_list.append(Move((piece.row, piece.col), pos_getter[n_pos]))
                            if dest != 0:
                                if dest.color != piece.color:
                                    break
                        elif check_blocker_move(a_row, a_col, k_row, k_col, n_pos):
                            move_list.append(Move((piece.row, piece.col), pos_getter[n_pos]))
                    elif case == 3:
                        if dest == attacker:
                            move_list.append(Move((piece.row, piece.col), pos_getter[n_pos]))
                            if dest != 0:
                                if dest.color != piece.color:
                                    break
    def hor_sliding_moves(piece, case):
        pos = piece.position
        start_rem = pos % 8
        for direction in orthogonal_squares:
            for i in range(1, 8):
                n_pos = pos + direction * i
                n_rem = n_pos % 8
                if n_pos not in range(0, 64):
                    break
                if n_rem > start_rem and direction == -1:
                    break
                if n_rem < start_rem and direction == 1:
                    break
                dest = game.get_piece_from_pos(n_pos)
                if dest != 0:
                    if dest.color == piece.color:
                        break
                valid = True
                if piece.pinned:
                    valid = pin_move_validator(piece.row, piece.col, k_row, k_col, n_pos)
                if valid:
                    if case == 1:
                        move_list.append(Move((piece.row, piece.col), pos_getter[n_pos]))
                        if dest != 0:
                            if dest.color != piece.color:
                                break
                    elif case == 2:
                        if dest == 0:
                            if check_blocker_move(a_row, a_col, k_row, k_col, n_pos):
                                move_list.append(Move((piece.row, piece.col), pos_getter[n_pos]))
                        else:
                            if dest == attacker:
                                move_list.append(Move((piece.row, piece.col), pos_getter[n_pos]))
                            break
                    elif case == 3:
                        if dest == attacker:
                            move_list.append(Move((piece.row, piece.col), pos_getter[n_pos]))
                            # if dest != 0:
                            #     if dest.color != piece.color:
                            #         break
    def king_moves(piece):
        if piece.type == king:
            pos = piece.position
            start_rem = pos % 8
            for direction in orthogonal_squares+diagonal_squares:
                for i in range(1, 2):
                    n_pos = pos + direction * i
                    n_rem = n_pos % 8
                    if n_pos not in range(0, 64):
                        break
                    if n_rem > start_rem and direction == -1:
                        break
                    if n_rem < start_rem and direction == 1:
                        break
                    if n_rem > start_rem and (direction == -9 or direction == 7):
                        break
                    if n_rem < start_rem and (direction == -7 or direction == 9):
                        break
                    dest = game.get_piece_from_pos(n_pos)
                    if dest != 0:
                        if dest.color == piece.color:
                            break
                    if aMap[n_pos] == 0:
                        if dest == 0:
                            move_list.append(Move((piece.row, piece.col), pos_getter[n_pos]))
                        elif dest!=0:
                            if dest.color != piece.color:
                                move_list.append(Move((piece.row, piece.col), pos_getter[n_pos]))

    for piece in pieces:
        if len(checkers) > 1:
            if piece.type == king:
                king_moves(piece)
        elif len(checkers) == 1:
            case = 2
            if attacker.type == knight:
                case = 3
            if piece.type == pawn:
                pawn_moves(piece, case)
            if piece.type == knight:
                knight_moves(piece, case)
            if piece.type in (bishop, queen):
                diag_sliding_moves(piece, case)
            if piece.type in (rook, queen):
                hor_sliding_moves(piece, case)
            if piece.type == king:
                king_moves(piece)
        else:
            case = 1
            if piece.type == pawn:
                pawn_moves(piece,case)
            if piece.type == knight:
                knight_moves(piece, case)
            if piece.type in (bishop, queen):
                diag_sliding_moves(piece, case)
            if piece.type in (rook, queen):
                hor_sliding_moves(piece, case)
            if piece.type == king:
                king_moves(piece)

        

    # Add castling moves
    if game.check == 0:
        if game.turn == white_piece:
            if game.whiteKingSideCastle == True and game.get_piece((7, 5)) == game.get_piece((7, 6)) and game.blackThreatMap[7*8+5] == game.blackThreatMap[7*8+6] == 0 and game.get_piece((7,7)) != 0:
                if game.get_piece((7,7)).type == rook:
                    move_list.append(Move((7, 4), (7, 6), castle=True))
            if game.whiteQueenSideCastle == True and game.get_piece((7, 3)) == game.get_piece((7, 2)) ==  game.get_piece((7, 1)) and game.blackThreatMap[7*8+3] == game.blackThreatMap[7*8+2] == 0 and game.get_piece((7,0)) != 0:
                if game.get_piece((7,0)).type == rook:
                    move_list.append(Move((7, 4), (7, 2), castle=True))
        else:
            if game.blackKingSideCastle == True and game.get_piece((0, 5)) == game.get_piece((0, 6)) and game.whiteThreatMap[0*8+5] == game.whiteThreatMap[0*8+6] == 0 and game.get_piece((0,7)) != 0:
                if game.get_piece((0,7)).type == rook:
                    move_list.append(Move((0, 4), (0, 6), castle=True))
            if game.blackQueenSideCastle == True and game.get_piece((0, 3)) == game.get_piece((0, 2)) == game.get_piece((0, 1)) and game.whiteThreatMap[0*8+3] == game.whiteThreatMap[0*8+2] == 0 and game.get_piece((0,0))!= 0:
                if game.get_piece((0,0)).type == rook:
                    move_list.append(Move((0, 4), (0, 2), castle=True))
            
    return move_list

