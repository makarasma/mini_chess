class ChessFigure():
    """Describes general methods and attributes of chess figure."""
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
        subtype = "_".join((self.type, self.side))
        return subtype

    def validate_moves(self, init_moves, figures):
        """Filters out invalid moves."""
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

    def validate_attack_moves(self, init_moves, figures):
        """Filters out invalid attack moves."""
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

    def axis(self, coord, figures, direction):
        """Returns available moves on the axis given the direction."""
        moves = []
        cell = coord
        while True:
            cell = (cell[0] + direction[0], cell[1] + direction[1])
            if cell not in figures.keys():
                break
            figure = figures[cell]
            if figure.piece:
                if figure.piece.side != self.side:
                    moves.append(cell)
                break
            moves.append(cell)
        return moves

    def axis_moves(self, coord, figures):
        """Returns moves in all the axis that lie on the available directions."""
        all_moves = []
        for direction in self.directions:
            moves = self.axis(coord, figures, direction)
            all_moves.extend(moves)
        return all_moves


class ChessPawn(ChessFigure):
    type = "pawn"

    def get_moves(self, coord, figures):
        """Returns all the available moves for the piece."""
        init_moves = []
        init_attack_moves = []
        if self.side == "white":
            move = (coord[0] - 1, coord[1])
            move1 = (coord[0] - 1, coord[1] + 1)
            move2 = (coord[0] - 1, coord[1] - 1)
        else:
            move = (coord[0] + 1, coord[1])
            move1 = (coord[0] + 1, coord[1] + 1)
            move2 = (coord[0] + 1, coord[1] - 1)
        init_moves.append(move)
        init_attack_moves.append(move1)
        init_attack_moves.append(move2)
        moves = self.validate_moves(init_moves, figures)
        attack_moves = self.validate_attack_moves(init_attack_moves,figures)
        result = moves + attack_moves
        return result


class ChessBishop(ChessFigure):
    type = "bishop"
    directions = [(1, 1), (-1, 1), (1, -1), (-1, -1)]

    def get_moves(self, coord, figures):
        moves = self.axis_moves(coord, figures)
        return moves


class ChessKnight(ChessFigure):
    type = "knight"
    directions = [(2, 1), (1, 2), (-1, 2), (-2, 1), (-2, -1), (-1, -2), (1, -2), (2, -1)]

    def get_moves(self, coord, figures):
        init_moves = []
        for direction in self.directions:
            init_moves.append((coord[0] + direction[0], coord[1] + direction[1]))
        attack_moves = self.validate_attack_moves(init_moves,figures)
        moves = self.validate_moves(init_moves,figures)
        result = attack_moves + moves
        return result


class ChessRook(ChessFigure):
    type = "rook"
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]

    def get_moves(self, coord, figures):
        moves = self.axis_moves(coord, figures)
        return moves


class ChessKing(ChessFigure):
    type = "king"
    directions = [(0, -1), (1, -1), (1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1)]

    def get_moves(self, coord, figures):
        moves = []
        for direction in self.directions:
            move = (coord[0] + direction[0], coord[1] + direction[1])
            if move in figures.keys():
                if figures[move].piece:
                    if figures[move].piece.side != self.side:
                        moves.append(move)
                else:
                    moves.append(move)
        return moves


class ChessQueen(ChessFigure):
    type = "queen"
    directions = [(1, 1), (-1, 1), (1, -1), (-1, -1), (0, 1), (0, -1), (1, 0), (-1, 0)]

    def get_moves(self, coord, figures):
        moves = self.axis_moves(coord, figures)
        return moves
