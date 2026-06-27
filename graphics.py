from tkinter import Tk, BOTH, Canvas
import time
import random


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
        self.visited = False

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
    def __init__(
        self, x1, y1, num_rows, num_cols, cell_size_x, cell_size_y, win=None, seed=None
    ):
        self.x1 = x1
        self.y1 = y1
        self.num_rows = num_rows
        self.num_cols = num_cols
        self.cell_size_x = cell_size_x
        self.cell_size_y = cell_size_y
        self.__win = win  # window
        self.__cells = []
        self.__create_cells()
        if seed is not None:
            random.seed(seed)
        self.__break_entrance_and_exit()
        self.__break_walls_r(0, 0)
        self.__reset_cells_visited()

    def __create_cells(self):
        for i in range(self.num_cols):
            col = []
            for j in range(self.num_rows):
                col.append(Cell(self.__win))
            self.__cells.append(col)  # self.__cells is a list of columns, where each
            # column is itself a list of cells. So the structure looks like this:
            # self.__cells[col][row]
        for i in range(self.num_cols):
            for j in range(self.num_rows):
                self.__draw_cell(i, j)

    def __draw_cell(self, i, j):
        x1 = self.x1 + (
            i * self.cell_size_x
        )  # pixel x = maze offset + column * cell width
        y1 = self.y1 + (
            j * self.cell_size_y
        )  # pixel y = maze offset + row * cell height
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
        self.__draw_cell(0, 0)
        self.__cells[self.num_cols - 1][self.num_rows - 1].has_bottom_wall = False
        self.__draw_cell((self.num_cols - 1), (self.num_rows - 1))

    def __break_walls_r(self, i, j):
        self.__cells[i][j].visited = True
        while True:
            self.__cells_to_visit = []
            # left neighbour exists?
            if i > 0 and not self.__cells[i - 1][j].visited:
                self.__cells_to_visit.append((i - 1, j))
            # right neighbour exists?
            if i < (self.num_cols - 1) and not self.__cells[i + 1][j].visited:
                self.__cells_to_visit.append((i + 1, j))
            # up neighbour exists?
            if j > 0 and not self.__cells[i][j - 1].visited:
                self.__cells_to_visit.append((i, j - 1))
            # down neighbour exists?
            if j < (self.num_rows - 1) and not self.__cells[i][j + 1].visited:
                self.__cells_to_visit.append((i, j + 1))
            if not self.__cells_to_visit:  # base case
                self.__draw_cell(i, j)  # draw the cell in its final wall state
                return  # this call ends; control goes back to the previous call
                # this is part of recursion unwinding
                # previous calls resume and check their cells again
            else:
                direction_index = random.randrange(len(self.__cells_to_visit))
                next_i, next_j = self.__cells_to_visit[direction_index]
                # moving right
                if next_i == i + 1:
                    self.__cells[i][j].has_right_wall = False
                    self.__cells[next_i][next_j].has_left_wall = False
                # moving left
                if next_i == i - 1:
                    self.__cells[i][j].has_left_wall = False
                    self.__cells[next_i][next_j].has_right_wall = False
                # moving down
                if next_j == j + 1:
                    self.__cells[i][j].has_bottom_wall = False
                    self.__cells[next_i][next_j].has_top_wall = False
                # moving up
                if next_j == j - 1:
                    self.__cells[i][j].has_top_wall = False
                    self.__cells[next_i][next_j].has_bottom_wall = False
                # recursive step: move into the chosen neighbour and continue carving
                self.__break_walls_r(next_i, next_j)

    def __reset_cells_visited(self):
        for i in range(self.num_cols):
            for j in range(self.num_rows):
                self.__cells[i][j].visited = False

    def solve(self):
        return self._solve_r(0, 0)

    def _solve_r(self, i=0, j=0):
        self.__animate()
        self.__cells[i][j].visited = True
        # base case
        if i == self.num_cols - 1 and j == self.num_rows - 1:
            return True
        # try left
        if (
            i > 0
            and not self.__cells[i][j].has_left_wall
            and not self.__cells[i - 1][j].visited
        ):
            self.__cells[i][j].draw_move(self.__cells[i - 1][j])
            if self._solve_r(i - 1, j):
                return True
            else:
                self.__cells[i][j].draw_move(self.__cells[i - 1][j], undo=True)
        # try right
        if (
            i < (self.num_cols - 1)
            and not self.__cells[i][j].has_right_wall
            and not self.__cells[i + 1][j].visited
        ):
            self.__cells[i][j].draw_move(self.__cells[i + 1][j])
            if self._solve_r(i + 1, j):
                return True
            else:
                self.__cells[i][j].draw_move(self.__cells[i + 1][j], undo=True)
        # try top
        if (
            j > 0
            and not self.__cells[i][j].has_top_wall
            and not self.__cells[i][j - 1].visited
        ):
            self.__cells[i][j].draw_move(self.__cells[i][j - 1])
            if self._solve_r(i, j - 1):
                return True
            else:
                self.__cells[i][j].draw_move(self.__cells[i][j - 1], undo=True)
        # try bottom
        if (
            j < (self.num_rows - 1)
            and not self.__cells[i][j].has_bottom_wall
            and not self.__cells[i][j + 1].visited
        ):
            self.__cells[i][j].draw_move(self.__cells[i][j + 1])
            if self._solve_r(i, j + 1):
                return True
            else:
                self.__cells[i][j].draw_move(self.__cells[i][j + 1], undo=True)
        return False
