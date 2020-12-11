import sys
import chessFigures
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image
from kivy.uix.behaviors.button import ButtonBehavior
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.label import Label
from kivy.graphics import Rectangle, Color
import itertools



class MainWindow(Screen):
    def exit_game(self):
        sys.exit()

class GameWindow(Screen):
    pass

# class ChessManager():
#     def __init__(self, **kwargs):
#         super(ChessManager, self).__init__(**kwargs)
#         self.pre_coords = list(range(1, 7))
#         self.coords = list(itertools.product(self.pre_coords, self.pre_coords))
#         self.start_coords = {
#             (1, 1): ("bishop", "black"), (1, 2): ("knight", "black"), (1, 3): ("rook", "black"),
#             (1, 4): ("king", "black"), (1, 5): ("knight", "black"), (1, 6): ("bishop", "black"),
#             (2, 1): ("pawn", "black"), (2, 2): ("pawn", "black"), (2, 3): ("pawn", "black"), (2, 4): ("pawn", "black"),
#             (2, 5): ("pawn", "black"), (2, 6): ("pawn", "black"), (6, 1): ("bishop", "white"),
#             (6, 2): ("knight", "white"), (6, 3): ("rook", "white"), (6, 4): ("king", "white"),
#             (6, 5): ("knight", "white"), (6, 6): ("bishop", "white"), (5, 1): ("pawn", "white"),
#             (5, 2): ("pawn", "white"), (5, 3): ("pawn", "white"), (5, 4): ("pawn", "white"), (5, 5): ("pawn", "white"),
#             (5, 6): ("pawn", "white")
#         }
#         self.cells = self.fill_board()
#         self.piece_select = False
#         self.piece_selected = None
#
#         def fill_board(self):
#             chess_cells = []
#             move_cells = []
#             for coord in self.coords:
#                 if coord in self.start_coords.keys():
#                     anchor = Cell(coord=coord, piece=self.start_coords[coord], occupied=True)
#                     chess_cells.append(anchor.chessCell)
#                     move_cells.append(anchor.moveCell)
#                     self.add_widget(anchor)
#                 else:
#                     anchor = Cell(coord=coord)
#                     chess_cells.append(anchor.chessCell)
#                     move_cells.append(anchor.moveCell)
#                     self.add_widget(anchor)
#             return (chess_cells, move_cells)
#
#         def show_moves(self):
#             for move in self.moves:
#                 for cell in self.cells[1]:
#                     if cell.coord == move:
#                         cell.opacity = 0.7
#
#         def deselect(self):
#             for cell in self.cells[1]:
#                 cell.opacity = 0
#
#         def attack(self, cell1, cell2):
#             pass

class ChessGrid(GridLayout):
    def __init__(self, **kwargs):
        super(ChessGrid, self).__init__(**kwargs)
        self.cols = 6
        self.pre_coords = list(range(1,7))
        self.coords = list(itertools.product(self.pre_coords, self.pre_coords))
        self.start_coords = {
            (1, 1): ("bishop","black"), (1, 2): ("knight", "black"), (1, 3): ("rook", "black"),
            (1, 4): ("king", "black"), (1, 5): ("knight", "black"), (1, 6) : ("bishop", "black"),
            (2, 1): ("pawn", "black"), (2, 2): ("pawn", "black"), (2, 3): ("pawn", "black"), (2, 4): ("pawn", "black"),
            (2, 5): ("pawn", "black"), (2, 6): ("pawn", "black"), (6, 1): ("bishop", "white"),
            (6, 2): ("knight", "white"), (6, 3): ("rook", "white"), (6, 4): ("king", "white"),
            (6, 5): ("knight", "white"), (6, 6): ("bishop", "white"), (5, 1): ("pawn", "white"),
            (5, 2): ("pawn","white"), (5, 3): ("pawn", "white"), (5, 4): ("pawn", "white"), (5, 5): ("pawn", "white"),
            (5, 6): ("pawn", "white")
        }
        self.cells = self.fill_board()
        self.piece_select = False
        self.piece_selected = None

    def fill_board(self):
        chess_cells = []
        move_cells = []
        for coord in self.coords:
            if coord in self.start_coords.keys():
                anchor = Cell(coord=coord, piece=self.start_coords[coord], occupied=True)
                chess_cells.append(anchor.chessCell)
                move_cells.append(anchor.moveCell)
                self.add_widget(anchor)
            else:
                anchor = Cell(coord=coord)
                chess_cells.append(anchor.chessCell)
                move_cells.append(anchor.moveCell)
                self.add_widget(anchor)
        return (chess_cells, move_cells)

    def show_moves(self):
        for move in self.moves:
            for cell in self.cells[1]:
                if cell.coord == move:
                    cell.opacity = 0.7

    def deselect(self):
        for cell in self.cells[1]:
            cell.opacity = 0

    def attack(self,cell1,cell2):
        pass

class Cell(AnchorLayout):

    def __init__(self, coord, piece=None, occupied=False, **kwargs):
        super(Cell, self).__init__(**kwargs)
        self.chessCell = ChessCell(coord,piece,occupied)
        self.moveCell = MoveCell(coord)
        self.add_widget(self.moveCell)
        self.add_widget(self.chessCell)


class ChessCell(ButtonBehavior, Image):

    def __init__(self, coord, piece=None, occupied=False, **kwargs):
        super(ChessCell, self).__init__(**kwargs)
        self.size_hint = (0.7,0.7)
        self.coord = coord
        self.selected = False
        self.occupied = occupied
        self.piece = self.get_figure(piece, self.coord) if piece else None
        self.source = self.piece.picture if piece else "pics/empty.png"

    def on_press(self):
        if self.parent.parent.piece_select:
            self.parent.parent.deselect()
            self.parent.parent.piece_select = False
            if self.coord in self.parent.parent.moves:
                self.parent.parent.attack(self.parent.parent.piece_selected,self.coord)
        else:
            if self.piece:
                self.parent.parent.piece_select = True
                self.parent.parent.piece_selected = self.coord
                self.parent.parent.moves = self.piece.get_moves()
                self.parent.parent.show_moves()

    def get_figure(self,piece,coord):
        pieces = {
            "pawn": chessFigures.ChessPawn(side=piece[1], coord=coord),
            "bishop": chessFigures.ChessBishop(side=piece[1], coord=coord),
            "knight": chessFigures.ChessKnight(side=piece[1], coord=coord),
            "rook": chessFigures.ChessRook(side=piece[1], coord=coord),
            "king": chessFigures.ChessKing(side=piece[1], coord=coord),
            "queen": chessFigures.ChessQueen(side=piece[1],coord=coord)
        }
        return pieces[piece[0]]


class MoveCell(ButtonBehavior, Image):
    def __init__(self, coord, **kwargs):
        super(MoveCell, self).__init__(**kwargs)
        self.source = "pics/green.png"
        self.size_hint = (0.7, 0.7)
        self.opacity = 0
        self.coord = coord


kv = Builder.load_file("my.kv")
sm = ScreenManager()
sm.add_widget(MainWindow(name='main'))
sm.add_widget(GameWindow(name='game'))

class MiniChessApp(App):
    def build(self):
        return sm

if __name__ == '__main__':
    MiniChessApp().run()