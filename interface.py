from solver import Solver
import tkinter as tk
from tkinter import messagebox
import time

class EightPuzzleGUI:
    def __init__(self, root, initial_state, goal_state):
        self.root = root
        self.root.title("Eight Puzzle Game")
        self.initial_state = initial_state
        self.goal_state = goal_state
        self.state = [row[:] for row in self.initial_state]
        self.solution_path = []
        self.solution_index = -1
        self.buttons = [[None for _ in range(3)] for _ in range(3)]
        self.create_widgets()

    def create_widgets(self):
        frame = tk.Frame(self.root)
        frame.pack()
        for i in range(3):
            for j in range(3):
                button = tk.Button(frame, text='', width=6, height=3, font=("Helvetica", 24), 
                                   bg='lightblue', fg='black', command=lambda i=i, j=j: self.move_tile(i, j))
                button.grid(row=i, column=j, padx=5, pady=5)
                self.buttons[i][j] = button
        self.update_buttons()

        control_frame = tk.Frame(self.root)
        control_frame.pack(pady=20)

        instructions = tk.Label(control_frame, text="Instructions: First choose a solution (BFS or A*), then use Next to see the solution.", font=("Helvetica", 14))
        instructions.grid(row=0, column=0, columnspan=4, pady=10)

        bfs_button = tk.Button(control_frame, text="Solve with BFS", width=15, font=("Helvetica", 14), bg='black', fg='white', command=self.solve_bfs)
        bfs_button.grid(row=1, column=0, padx=5)

        astar_button = tk.Button(control_frame, text="Solve with A*", width=15, font=("Helvetica", 14), bg='black', fg='white', command=self.solve_astar)
        astar_button.grid(row=1, column=1, padx=5)

        prev_button = tk.Button(control_frame, text="Previous", width=15, font=("Helvetica", 14), bg='black', fg='white', command=self.prev_state)
        prev_button.grid(row=1, column=2, padx=5)

        next_button = tk.Button(control_frame, text="Next", width=15, font=("Helvetica", 14), bg='black', fg='white', command=self.next_state)
        next_button.grid(row=1, column=3, padx=5)
        
        reset_button = tk.Button(control_frame, text="Reset", width=15, font=("Helvetica", 14), bg='black', fg='white', command=self.reset)
        reset_button.grid(row=2, column=0, columnspan=4, pady=10)

    def update_buttons(self):
        for i in range(3):
            for j in range(3):
                value = self.state[i][j]
                self.buttons[i][j].config(text=str(value) if value != Solver.EMPTY else '')

    def move_tile(self, i, j):
        empty = Solver.find_index(self.state, Solver.EMPTY)
        if abs(empty[0] - i) + abs(empty[1] - j) == 1:
            self.state = Solver.move(self.state, (i - empty[0], j - empty[1]))
            self.update_buttons()
            if self.state == self.goal_state:
                messagebox.showinfo("Congratulations", "You solved the puzzle!")

    def solve_bfs(self):
        start_time = time.time()
        self.solution_path = Solver.bfs(self.state, self.goal_state)
        end_time = time.time()
        elapsed_time = end_time - start_time

        self.solution_index = -1
        if self.solution_path:
            self.update_buttons()
            messagebox.showinfo("BFS", f"Solution found using BFS!\nTime taken: {elapsed_time:.4f} seconds")
        else:
            messagebox.showinfo("BFS", "No solution found with BFS.")

    def solve_astar(self):
        start_time = time.time()
        self.solution_path = Solver.a_star(self.state, self.goal_state)
        end_time = time.time()
        elapsed_time = end_time - start_time

        self.solution_index = -1
        if self.solution_path:
            self.update_buttons()
            messagebox.showinfo("A*", f"Solution found using A*!\nTime taken: {elapsed_time:.4f} seconds")
        else:
            messagebox.showinfo("A*", "No solution found with A*.")

    def prev_state(self):
        if self.solution_path and self.solution_index > 0:
            self.solution_index -= 1
            self.state = self.solution_path[self.solution_index]
            self.update_buttons()

    def next_state(self):
        if self.solution_path and self.solution_index < len(self.solution_path) - 1:
            self.solution_index += 1
            self.state = self.solution_path[self.solution_index]
            self.update_buttons()
            if self.state == self.goal_state:
                messagebox.showinfo("Congratulations", "You solved the puzzle!")
            
    def reset(self):
        self.state = [row[:] for row in self.initial_state]
        self.solution_path = []
        self.solution_index = -1
        self.update_buttons()