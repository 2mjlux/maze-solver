from tkinter import Tk, BOTH, Canvas
import time


class Window:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.__root = Tk()
        self.__root.title("Maze Solver")
        self.__canvas = Canvas(self.__root, bg="white", height=height, width=width)
        self.__canvas.pack(fill=BOTH, expand=1)
        self.__running = False
        self.__root.protocol("WM_DELETE_WINDOW", self.close)

    def redraw(self):
        self.__root.update_idletasks()
        self.__root.update()

    def wait_for_close(self):
        self.__running = True
        while self.__running:
            self.redraw()
        print("window closed...")

    def close(self):
        self.__running = False

    def draw_line(self, line, fill_color):
        line.draw(self.__canvas, fill_color)


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Line:
    def __init__(self, a, b):
        self.a = a
        self.b = b

    def draw(self, canvas, fill_color):
        canvas.create_line(
            self.a.x, self.a.y, self.b.x, self.b.y, fill=fill_color, width=2
        )


class Cell:
    def __init__(self, window=None):
        self.has_left_wall = True
        self.has_right_wall = True
        self.has_top_wall = True
        self.has_bottom_wall = True
        # no cell placed on the canvas yet
        # valid coordinates start at (0, 0)
        self.__x1 = -1.0
        self.__x2 = -1.0
        self.__y1 = -1.0
        self.__y2 = -1.0
        self.__win = window

    def draw(self, x1, y1, x2, y2):
        self.__x1 = x1
        self.__y1 = y1
        self.__x2 = x2
        self.__y2 = y2
        if self.__win is None:
            print("No window defined in cell (window = None).")
            return
        # left wall
        a = Point(self.__x1, self.__y1)
        b = Point(self.__x1, self.__y2)
        line_left = Line(a, b)
        if self.has_left_wall:
            self.__win.draw_line(line_left, "blue")
        else:
            self.__win.draw_line(line_left, "white")
        # right wall
        a = Point(self.__x2, self.__y1)
        b = Point(self.__x2, self.__y2)
        line_right = Line(a, b)
        if self.has_right_wall:
            self.__win.draw_line(line_right, "blue")
        else:
            self.__win.draw_line(line_right, "white")
        # top wall
        a = Point(self.__x1, self.__y1)
        b = Point(self.__x2, self.__y1)
        line_top = Line(a, b)
        if self.has_top_wall:
            self.__win.draw_line(line_top, "blue")
        else:
            self.__win.draw_line(line_top, "white")
        # bottom wall
        a = Point(self.__x1, self.__y2)
        b = Point(self.__x2, self.__y2)
        line_bottom = Line(a, b)
        if self.has_bottom_wall:
            self.__win.draw_line(line_bottom, "blue")
        else:
            self.__win.draw_line(line_bottom, "white")

    def draw_move(self, to_cell, undo=False):
        if self.__win is None:
            print("No window defined in cell (window = None).")
            return
        # middle of start cell
        center_x_a = (self.__x1 + self.__x2) / 2
        center_y_a = (self.__y1 + self.__y2) / 2
        a = Point(center_x_a, center_y_a)
        # middle of end cell
        center_x_b = (to_cell.__x1 + to_cell.__x2) / 2
        center_y_b = (to_cell.__y1 + to_cell.__y2) / 2
        b = Point(center_x_b, center_y_b)
        # declare line
        moving_line = Line(a, b)
        # draw line
        if undo:
            self.__win.draw_line(moving_line, "gray")
        else:
            self.__win.draw_line(moving_line, "red")


class Maze:
    def __init__(self, x1, y1, num_rows, num_cols, cell_size_x, cell_size_y, win=None):
        self.x1 = x1
        self.y1 = y1
        self.num_rows = num_rows
        self.num_cols = num_cols
        self.cell_size_x = cell_size_x
        self.cell_size_y = cell_size_y
        self.__win = win  # window
        self.__cells = []
        self.__create_cells()
        self.__break_entrance_and_exit()

    def __create_cells(self):
        for i in range(self.num_cols):
            col = []
            for j in range(self.num_rows):
                col.append(Cell(self.__win))
            self.__cells.append(col)

        for i in range(self.num_cols):
            for j in range(self.num_rows):
                self.__draw_cell(i, j)

    def __draw_cell(self, i, j):
        x1 = self.x1 + (i * self.cell_size_x)
        y1 = self.y1 + (j * self.cell_size_y)
        x2 = x1 + self.cell_size_x
        y2 = y1 + self.cell_size_y
        self.__cells[i][j].draw(x1, y1, x2, y2)
        if self.__win is None:
            print("No window defined in cell (window = None).")
            return
        self.__animate()

    def __animate(self):
        if self.__win is None:
            print("No window defined in cell (window = None).")
            return
        self.__win.redraw()
        time.sleep(0.05)

    def __break_entrance_and_exit(self):
        self.__cells[0][0].has_top_wall = False
        self.__draw_cell(0,0)
        self.__cells[self.num_cols-1][self.num_rows-1].has_bottom_wall = False
        self.__draw_cell((self.num_cols-1),(self.num_rows-1))
