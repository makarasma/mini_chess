

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
        moves = []
        if self.side == "white":
            move = (coord[0] - 1, coord[1])
            moves.append(move)
        else:
            move = (coord[0] + 1, coord[1])
            moves.append(move)

        for move in moves:
            figure = figures[move]
            if figure.piece and figure.piece.side == self.side:
                moves.remove(move)
        return moves

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
