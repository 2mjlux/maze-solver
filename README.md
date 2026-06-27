# Maze Solver

A Python application that generates random mazes and solves them visually using a recursive depth-first search (DFS) algorithm with backtracking.


## Features

- Generates a random maze on a grid
- Renders the maze in a graphical window
- Solves the maze step by step
- Visually shows backtracking from dead ends
- Highlights the successful path to the exit

## Technical Highlights

- Implemented recursive depth-first search to find a path through the maze
- Used backtracking to reverse incorrect paths and continue the search
- Applied object-oriented programming to model the maze and its cells
- Built a simple graphical interface using Tkinter
- Managed grid-based traversal with boundary, wall, and visited-cell checks

## How It Works

The program first creates a maze by building a grid of cells and removing walls between them to create valid paths. It then solves the maze recursively.

The solving algorithm:

1. Starts at the entrance cell
2. Marks each visited cell
3. Tries moving left, right, up, and down
4. Skips visited cells and blocked paths
5. Backtracks when it reaches a dead end
6. Stops when it reaches the exit

This project demonstrates **depth-first search (DFS)** and **backtracking** in a visual and practical way.

## Project Structure

- `main.py`: starts the application and runs the maze solver
- `graphics.py`: contains the window, maze, cells, and drawing logic
- `tests.py`: contains test cases for the project

## Technologies Used

- Python 3
- Tkinter

## Concepts Practised

- Object-oriented programming
- Recursion
- Depth-first search
- Backtracking
- Grid traversal
- Basic GUI rendering and animation

## Run the Project

Make sure Python 3 is installed, then run:

```bash
python3 main.py
```

## Challenges and Lessons Learned
One of the main challenges in this project was implementing the recursive solver correctly while tracking visited cells and visually undoing failed paths. Building this project strengthened my understanding of recursion, backtracking, and state management in grid-based algorithms.

## Background
This project was originally built as part of the Boot.dev curriculum and then refined as a portfolio project to strengthen algorithmic thinking and visual problem solving.

