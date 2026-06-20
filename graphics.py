from tkinter import Tk, BOTH, Canvas


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
    def __init__(self, window):
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
