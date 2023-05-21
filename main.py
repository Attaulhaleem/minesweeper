from tkinter import *
from tkinter import ttk
import random
import utils
import config


class Cell(ttk.Button):
    def __init__(self, master):
        # define button styles
        style = ttk.Style()
        # themes: "winnative", "clam", "alt", "default", "classic", "vista", "xpnative"
        style.theme_use("alt")
        # normal style
        style.configure(config.NORMAL_STYLE, background="white")
        style.map(
            config.NORMAL_STYLE,
            background=[("active", "#6EB1D6")],
        )
        # sweeped style
        style.map(
            config.SWEEPED_STYLE,
            background=[("disabled", "lightgreen")],
            foreground=[("disabled", "black")],
        )
        # flag style
        style.configure(config.FLAG_STYLE, background="white", focuscolor="none")
        # mine style
        style.map(
            config.MINE_STYLE,
            background=[("disabled", "red")],
            foreground=[("disabled", "black")],
        )
        # transparent image to define button size
        self.image = utils.get_tk_image(None, config.ICON_SIZE)
        super().__init__(
            master,
            style=config.NORMAL_STYLE,
            compound="center",
            image=self.image,
            text=None,
        )
        # coordinate for locating in grid
        self.coord = None
        # cell status
        self.is_mine = False
        self.is_flagged = False
        self.is_sweeped = False
        # bind events
        self.bind("<Button-1>", self.on_left_click)
        self.bind("<Button-3>", self.on_right_click)

    def sweep(self):
        # when to stop opening cells
        if self.is_sweeped or self.is_flagged or self.is_mine:
            return
        # remove bindings
        self.unbind("<Button-1>")
        self.unbind("<Button-3>")
        # disable button
        self.state(["disabled"])
        # count mines
        mines = Grid.count_neighboring_mines(self.coord)
        # clear image and show mine count
        self.image = utils.get_tk_image(None, config.ICON_SIZE)
        self.configure(style=config.SWEEPED_STYLE, image=self.image, text=str(mines))
        # set status
        self.is_sweeped = True
        # if all cells sweeped
        if Grid.get_sweeped_cells() == config.WIN_CELLS:
            # TODO: Game won
            Grid.disable()
            Grid.show_mines()

        # if not surrounded by mines
        if mines == 0:
            self.configure(text="")
            # open neighboring cells
            for neighbor in Grid.get_neighbors(self.coord):
                Grid.at(neighbor).sweep()

    def on_left_click(self, event):
        # clicked on mine
        if self.is_mine:
            self.image = utils.get_tk_image(config.MINE_ICON, config.ICON_SIZE)
            self.configure(style=config.MINE_STYLE, image=self.image)
            Grid.disable()
            Grid.show_mines()
            # TODO: Game lost
        else:
            self.sweep()

    def on_right_click(self, event):
        # toggle flag
        self.is_flagged = not self.is_flagged
        if self.is_flagged:
            self.image = utils.get_tk_image(config.FLAG_ICON, config.ICON_SIZE)
            # unbind sweeping action on flag
            self.unbind("<Button-1>")
            self.configure(style=config.FLAG_STYLE, image=self.image)
        else:
            self.image = utils.get_tk_image(None, config.ICON_SIZE)
            # allow sweeping action on no flag
            self.bind("<Button-1>", self.on_left_click)
            self.configure(style=config.NORMAL_STYLE, image=self.image)


class Grid:
    cells = list()

    def __init__(self, master):
        # populate the grid
        for row in range(config.ROWS):
            for col in range(config.COLS):
                cell = Cell(master)
                cell.coord = (row, col)
                cell.grid(row=row, column=col, sticky="nsew")
                cell.rowconfigure(0, weight=1)
                cell.columnconfigure(0, weight=1)
                Grid.cells.append(cell)
        # place mines randomly
        for cell in random.sample(Grid.cells, config.NUM_OF_MINES):
            cell.is_mine = True

    @staticmethod
    def get_sweeped_cells():
        return sum(1 for cell in Grid.cells if cell.is_sweeped)

    @staticmethod
    def count_neighboring_mines(coord):
        mines = 0
        for neighbor in Grid.get_neighbors(coord):
            if Grid.at(neighbor).is_mine:
                mines += 1
        return mines

    @staticmethod
    def get_neighbors(coord):
        row = coord[0]
        col = coord[1]
        neighbors = [
            (row, col - 1),  # left
            (row - 1, col - 1),  # up left
            (row - 1, col),  # up
            (row - 1, col + 1),  # up right
            (row, col + 1),  # right
            (row + 1, col + 1),  # down right
            (row + 1, col),  # down
            (row + 1, col - 1),  # down left
        ]
        # return valid neighbors
        return list(filter(Grid.is_valid_coord, neighbors))

    @staticmethod
    def is_valid_coord(coord):
        row = coord[0]
        col = coord[1]
        return row >= 0 and row < config.ROWS and col >= 0 and col < config.COLS

    @staticmethod
    def at(coord):
        row = coord[0]
        col = coord[1]
        index = (row * config.COLS) + col
        return Grid.cells[index]

    @staticmethod
    def disable():
        for cell in Grid.cells:
            cell.unbind("<Button-1>")
            cell.unbind("<Button-3>")
            cell.state(["disabled"])

    @staticmethod
    def show_mines():
        for cell in Grid.cells:
            if cell.is_mine:
                cell.image = utils.get_tk_image(config.MINE_ICON, config.ICON_SIZE)
                cell.configure(style=config.MINE_STYLE, image=cell.image)


class Window(Tk):
    def __init__(self):
        super().__init__()
        self.title(config.WINDOW_TITLE)
        self.iconbitmap(config.WINDOW_ICON)
        self.resizable(False, False)
        try:
            self.state("zoomed")  # works on Windows and macOS
        except:
            self.attributes("-zoomed", True)  # works on Linux

    @property
    def width(self):
        return self.winfo_screenwidth()

    @property
    def height(self):
        return self.winfo_screenheight()


class App:
    def __init__(self):
        self.window = Window()
        self.grid = Grid(self.window)
        self.window.mainloop()


if __name__ == "__main__":
    app = App()
