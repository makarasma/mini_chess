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

class ChessManager():
    def __init__(self, **kwargs):
        super(ChessManager, self).__init__(**kwargs)
        self.pre_coords = list(range(1, 7))
        self.coords = list(itertools.product(self.pre_coords, self.pre_coords))
        self.start_coords = {
            (1, 1): ("bishop", "black"), (1, 2): ("knight", "black"), (1, 3): ("rook", "black"),
            (1, 4): ("king", "black"), (1, 5): ("knight", "black"), (1, 6): ("bishop", "black"),
            (2, 1): ("pawn", "black"), (2, 2): ("pawn", "black"), (2, 3): ("pawn", "black"), (2, 4): ("pawn", "black"),
            (2, 5): ("pawn", "black"), (2, 6): ("pawn", "black"), (6, 1): ("bishop", "white"),
            (6, 2): ("knight", "white"), (6, 3): ("rook", "white"), (6, 4): ("king", "white"),
            (6, 5): ("knight", "white"), (6, 6): ("bishop", "white"), (5, 1): ("pawn", "white"),
            (5, 2): ("pawn", "white"), (5, 3): ("pawn", "white"), (5, 4): ("pawn", "white"), (5, 5): ("pawn", "white"),
            (5, 6): ("pawn", "white")
        }
        self.figures = None
        self.move_cells = None
        self.moves = None
        self.piece_select = False
        self.piece_selected = None

    def show_moves(self):
        for move in self.moves:
            move_cell = self.get_cell(move,"move")
            move_cell.opacity = 0.7

    def deselect(self):
        for cell in self.move_cells.values():
            cell.opacity = 0

    def move(self, coord1, coord2):
        figure1 = self.get_cell(coord1,"figure")
        figure2 = self.get_cell(coord2,"figure")
        piece = figure1.piece
        figure1.piece = None
        figure1.source = figure1.update_figure()
        figure2.piece = piece
        figure2.source = figure2.update_figure()

    def get_cell(self,coord,cell_type):
        cells = self.figures if cell_type == "figure" else self.move_cells
        cell = cells[coord]
        return cell


class ChessGrid(GridLayout):
    def __init__(self, **kwargs):
        super(ChessGrid, self).__init__(**kwargs)
        self.cols = 6
        self.fill_board()

    def fill_board(self):
        figure_cells = {}
        move_cells = {}
        for coord in manager.coords:
            if coord in manager.start_coords.keys():
                anchor = Cell(coord=coord, piece=manager.start_coords[coord])
                figure_cells[coord] = anchor.chessCell
                move_cells[coord] = anchor.moveCell
                self.add_widget(anchor)
            else:
                anchor = Cell(coord=coord)
                figure_cells[coord] = anchor.chessCell
                move_cells[coord] = anchor.moveCell
                self.add_widget(anchor)
        manager.figures = figure_cells
        manager.move_cells = move_cells

class Cell(AnchorLayout):

    def __init__(self, coord, piece=None, occupied=False, **kwargs):
        super(Cell, self).__init__(**kwargs)
        self.chessCell = ChessCell(coord,piece)
        self.moveCell = MoveCell(coord)
        self.add_widget(self.moveCell)
        self.add_widget(self.chessCell)

class ChessCell(ButtonBehavior, Image):

    def __init__(self, coord, piece=None, **kwargs):
        super(ChessCell, self).__init__(**kwargs)
        self.size_hint = (0.7,0.7)
        self.coord = coord
        self.selected = False
        self.piece = self.get_figure(piece) if piece else None
        self.source = self.update_figure()

    def on_press(self):
        if manager.piece_select:
            manager.deselect()
            manager.piece_select = False
            if self.coord in manager.moves:
                manager.move(manager.piece_selected,self.coord)
        else:
            if self.piece:
                manager.piece_select = True
                manager.piece_selected = self.coord
                manager.moves = self.piece.get_moves(self.coord,manager.figures)
                manager.show_moves()

    def update_figure(self):
        picture = self.piece.picture if self.piece else "pics/empty.png"
        return picture

    def get_figure(self,piece):
        pieces = {
            "pawn": chessFigures.ChessPawn(side=piece[1]),
            "bishop": chessFigures.ChessBishop(side=piece[1]),
            "knight": chessFigures.ChessKnight(side=piece[1]),
            "rook": chessFigures.ChessRook(side=piece[1]),
            "king": chessFigures.ChessKing(side=piece[1]),
            "queen": chessFigures.ChessQueen(side=piece[1])
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
manager = ChessManager()
sm = ScreenManager()
sm.add_widget(MainWindow(name='main'))
sm.add_widget(GameWindow(name='game'))

class MiniChessApp(App):
    def build(self):
        return sm

if __name__ == '__main__':
    MiniChessApp().run()