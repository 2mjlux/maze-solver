from graphics import Window, Maze


def main():
    # 1. Create a window (e.g., 800x600 pixels)
    win = Window(800, 600)

    # 2. Define your maze parameters
    margin = 50
    num_rows = 10
    num_cols = 12
    cell_size_x = 50
    cell_size_y = 50

    # 3. Initialize the Maze
    # This will automatically trigger __create_cells and __draw_cell
    maze = Maze(margin, margin, num_rows, num_cols, cell_size_x, cell_size_y, win)

    # 4. Keep the window open
    win.wait_for_close()


if __name__ == "__main__":
    main()
