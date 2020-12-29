from kivy.config import Config
Config.set('graphics', 'resizable', '0')
Config.set('graphics', 'width', '900')
Config.set('graphics', 'height', '600')
Config.write()

import sys
import chessFigures
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.gridlayout import GridLayout
from kivy.uix.image import Image
from kivy.uix.behaviors.button import ButtonBehavior
from kivy.uix.anchorlayout import AnchorLayout
from kivy.properties import StringProperty
import itertools
import time
import threading


class MainWindow(Screen):
    """Game menu window, also manages exit."""
    def exit_game(self):
        manager.game = False
        sys.exit()


class GameModeWindow(Screen):
    """Game mode window, manages game start for a selected game mode"""
    def start_game(self, game_time=None):
        global manager, timer
        manager = ChessManager(game_time=game_time)
        timer = Timer()
        gw.init()
        if game_time:
            t1 = threading.Thread(target=timer.chess_timer)
            t1.start()


class GameWindow(Screen):
    """Game window that displays the game."""
    message_white = StringProperty()
    message_black = StringProperty()
    message_timer_white = StringProperty()
    message_timer_black = StringProperty()

    def change_message(self, message_white, message_black):
        """Changes the message shown for both players."""
        self.message_white = message_white
        self.message_black = message_black

    def exit_game(self):
        mw.exit_game()

    def init(self):
        """Initializes game messages and timer text for both players. Also fills the chess board with pieces."""
        self.message_white = "White Turn"
        self.message_black = ""
        if manager.game_time:
            self.message_timer_white = f"{manager.game_time}:00"
            self.message_timer_black = f"{manager.game_time}:00"
            print("")
        else:
            self.message_timer_white = ""
            self.message_timer_black = ""
        self.ids.chessGrid.fill_board()

    def reset(self):
        """Clears the chess board and resets the game when returning back to menu from the game."""
        self.ids.chessGrid.clear_widgets()
        manager.game = False
        time.sleep(0.2)


class Timer():
    """Chess timer that runs in parallel with the game when one of the blitz modes are played."""
    def chess_timer(self):
        time.sleep(2)
        while manager.game:
            if manager.timer_black <= 0:
                manager.game_won("white")
                break
            if manager.timer_white <= 0:
                manager.game_won("black")
                break
            if manager.turn == "white":
                time.sleep(0.1)
                manager.timer_white = manager.timer_white - 0.1
                manager.timer_white = 0 if manager.timer_white < 0 else manager.timer_white
                gw.message_timer_white = time.strftime('%M:%S', time.gmtime(manager.timer_white))
            if manager.turn == "black":
                time.sleep(0.1)
                manager.timer_black = manager.timer_black - 0.1
                manager.timer_black = 0 if manager.timer_black < 0 else manager.timer_black
                gw.message_timer_black = time.strftime('%M:%S', time.gmtime(manager.timer_black))


class ChessManager():
    """Manages the game and chess piece parameters."""
    def __init__(self, game_time, **kwargs):
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
        self.turn = "white"
        self.game = True
        self.game_time = game_time
        self.timer_white = None
        self.timer_black = None
        if game_time:
            self.timer_white = 60 * self.game_time
            self.timer_black = 60 * self.game_time

    def show_moves(self):
        """Highlights the chess cells where a move is available."""
        for move in self.moves:
            move_cell = self.get_cell(move, "move")
            move_cell.opacity = 0.7

    def deselect(self):
        """Removes the marking of available moves on the board when piece is deselected."""
        for cell in self.move_cells.values():
            cell.opacity = 0

    def move(self, coord1, coord2):
        """Performs a chess piece move"""
        figure1 = self.get_cell(coord1, "figure")
        figure2 = self.get_cell(coord2, "figure")
        if figure2.piece:
            if figure2.piece.type == "king":
                if figure2.piece.side == "black":
                    self.game_won("white")
                else:
                    self.game_won("black")
        if figure1.piece.side == "white" and coord2[0] == 1 and figure1.piece.type == "pawn":
            piece = figure2.get_figure(("queen", "white"))
        elif figure1.piece.side == "black" and coord2[0] == 6 and figure1.piece.type == "pawn":
            piece = figure2.get_figure(("queen", "black"))
        else:
            piece = figure1.piece
        figure1.piece = None
        figure2.piece = piece
        figure1.source = figure1.update_figure()
        figure2.source = figure2.update_figure()

    def get_cell(self, coord, cell_type):
        """Returns chess board cell to the manager given the coordinates."""
        cells = self.figures if cell_type == "figure" else self.move_cells
        cell = cells[coord]
        return cell

    def game_won(self, side):
        """A function that ends the game when won."""
        if side == "white":
            gw.change_message("White has won!", "")
        else:
            gw.change_message("", "Black has won!")
        manager.game = False


class ChessGrid(GridLayout):
    """A grid container that contains the cells of chess board."""
    def __init__(self, **kwargs):
        super(ChessGrid, self).__init__(**kwargs)
        self.cols = 6

    def fill_board(self):
        """Fills the board with chess cells."""
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
    """A chess cell object that contains a cell responsible for displaying a chess piece
    and a cell that is responsible for displaying the chess moves."""
    def __init__(self, coord, piece=None, **kwargs):
        super(Cell, self).__init__(**kwargs)
        self.chessCell = ChessCell(coord, piece)
        self.moveCell = MoveCell(coord)
        self.add_widget(self.moveCell)
        self.add_widget(self.chessCell)


class ChessCell(ButtonBehavior, Image):
    """A chess cell that contains chess piece, its coordinates and an image."""
    def __init__(self, coord, piece=None, **kwargs):
        super(ChessCell, self).__init__(**kwargs)
        self.size_hint = (0.7, 0.7)
        self.coord = coord
        self.selected = False
        self.piece = self.get_figure(piece) if piece else None
        self.source = self.update_figure()

    def on_press(self):
        """Coordinates the actions when a chess cell is pressed."""
        if not manager.game:
            return
        if manager.piece_select:
            manager.deselect()
            manager.piece_select = False
            if self.coord in manager.moves:
                manager.turn = "white" if manager.turn == "black" else "black"
                if manager.turn == "white":
                    gw.change_message("White Turn", "")
                else:
                    gw.change_message("", "Black Turn")
                manager.move(manager.piece_selected, self.coord)
        else:
            if self.piece:
                if self.piece.side != manager.turn:
                    return
                manager.piece_select = True
                manager.piece_selected = self.coord
                manager.moves = self.piece.get_moves(self.coord, manager.figures)
                manager.show_moves()

    def update_figure(self):
        """Updates the chess cell figure picture."""
        picture = self.piece.picture if self.piece else "pics/empty.png"
        return picture

    def get_figure(self, piece):
        """Retrieves a chess piece object."""
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
    """A chess cell that displays an available move."""
    def __init__(self, coord, **kwargs):
        super(MoveCell, self).__init__(**kwargs)
        self.source = "pics/green.png"
        self.size_hint = (0.7, 0.7)
        self.opacity = 0
        self.coord = coord


sm = ScreenManager()
kv = Builder.load_file("my.kv")
mw = MainWindow(name='main')
gw = GameWindow(name='game')
gm = GameModeWindow(name='gamemode')
sm.add_widget(mw)
sm.add_widget(gw)
sm.add_widget(gm)
manager = ChessManager(game_time=None)


class MiniChessApp(App):
    """A class that contains the app."""
    icon = "pics/icon.png"

    def build(self):
        return sm


if __name__ == '__main__':
    MiniChessApp().run()
    manager.game = False
