
class ChessFigure():
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

    def __init__(self, side, coord):
        self.side = side
        self.type = ""
        self.coord = coord

    def get_subtype(self):
        subtype = "_".join((self.type,self.side))
        return subtype

    def get_moves(self):
        moves = []
        if self.side == "white":
            move = (self.coord[0] - 1, self.coord[1])
            moves.append(move)
        else:
            move = (self.coord[0] + 1, self.coord[1])
            moves.append(move)
        return moves


class ChessPawn(ChessFigure):
    def __init__(self,**kwargs):
        super(ChessPawn, self).__init__(**kwargs)
        self.type = "pawn"
        self.subtype = self.get_subtype()
        self.picture = self.pictures[self.subtype]


class ChessBishop(ChessFigure):
    def __init__(self,**kwargs):
        super(ChessBishop, self).__init__(**kwargs)
        self.type = "bishop"
        self.subtype = self.get_subtype()
        self.picture = self.pictures[self.subtype]


class ChessKnight(ChessFigure):
    def __init__(self,**kwargs):
        super(ChessKnight, self).__init__(**kwargs)
        self.type = "knight"
        self.subtype = self.get_subtype()
        self.picture = self.pictures[self.subtype]

class ChessRook(ChessFigure):
    def __init__(self,**kwargs):
        super(ChessRook, self).__init__(**kwargs)
        self.type = "rook"
        self.subtype = self.get_subtype()
        self.picture = self.pictures[self.subtype]

class ChessKing(ChessFigure):
    def __init__(self,**kwargs):
        super(ChessKing, self).__init__(**kwargs)
        self.type = "king"
        self.subtype = self.get_subtype()
        self.picture = self.pictures[self.subtype]

class ChessQueen(ChessFigure):
    def __init__(self,**kwargs):
        super(ChessQueen, self).__init__(**kwargs)
        self.type = "queen"
        self.subtype = self.get_subtype()
        self.picture = self.pictures[self.subtype]


#piece = ChessPawn(side="white")
