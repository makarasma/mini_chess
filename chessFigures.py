

class ChessFigure():
    type = ""
    pictures = {
        "pawn_white": "pics/pawn_white.png",
        "pawn_black": "pics/pawn_black.png",
        "bishop_white": "pics/bishop_white.png",
        "bishop_black": "pics/bishop_black.png",
        "knight_white": "pics/knight_white.png",
        "knight_black": "pics/knight_black.png",
        "rook_white": "pics/rook_white.png",
        "rook_black": "pics/rook_black.png",
        "king_white": "pics/king_white.png",
        "king_black": "pics/king_black.png",
        "queen_white": "pics/queen_white.png",
        "queen_black": "pics/queen_black.png"
    }

    def __init__(self, side):
        self.side = side
        self.subtype = self.get_subtype()
        self.picture = self.pictures[self.subtype]

    def get_subtype(self):
        subtype = "_".join((self.type,self.side))
        return subtype

    def get_moves(self,coord,figures):
        init_moves = []
        if self.side == "white":
            move = (coord[0] - 1, coord[1])
        else:
            move = (coord[0] + 1, coord[1])
        init_moves.append(move)
        moves = self.validate_moves(init_moves, figures)
        init_attack_moves = []
        if self.side == "white":
            move1 = (coord[0] - 1, coord[1] + 1)
            move2 = (coord[0] - 1, coord[1] - 1)
        else:
            move1 = (coord[0] + 1, coord[1] + 1)
            move2 = (coord[0] + 1, coord[1] - 1)
        init_attack_moves.append(move1)
        init_attack_moves.append(move2)
        attack_moves = self.validate_attack_moves(init_attack_moves,figures)
        result = moves + attack_moves
        return result

    def validate_moves(self,init_moves,figures):
        removes = []
        for move in init_moves:
            if move not in figures.keys():
                removes.append(move)
                continue
            figure = figures[move]
            if figure.piece:
                removes.append(move)
        moves = [m for m in init_moves if m not in removes]
        return moves

    def validate_attack_moves(self,init_moves,figures):
        removes = []
        for move in init_moves:
            if move not in figures.keys():
                removes.append(move)
                continue
            figure = figures[move]
            if not figure.piece:
                removes.append(move)
                continue
            if figure.piece.side == self.side:
                removes.append(move)
        attack_moves = [m for m in init_moves if m not in removes]
        return attack_moves



class ChessPawn(ChessFigure):
    type = "pawn"
    def __init__(self,**kwargs):
        super(ChessPawn, self).__init__(**kwargs)


class ChessBishop(ChessFigure):
    type = "bishop"
    def __init__(self,**kwargs):
        super(ChessBishop, self).__init__(**kwargs)


class ChessKnight(ChessFigure):
    type = "knight"
    def __init__(self,**kwargs):
        super(ChessKnight, self).__init__(**kwargs)

class ChessRook(ChessFigure):
    type = "rook"
    def __init__(self,**kwargs):
        super(ChessRook, self).__init__(**kwargs)

class ChessKing(ChessFigure):
    type = "king"
    def __init__(self,**kwargs):
        super(ChessKing, self).__init__(**kwargs)

class ChessQueen(ChessFigure):
    type = "queen"
    def __init__(self,**kwargs):
        super(ChessQueen, self).__init__(**kwargs)


#piece = ChessPawn(side="white")
