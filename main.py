import tkinter as tk
from interface import EightPuzzleGUI

def main():
    initial_state = [
        [7, 3, 8],
        [4, 5, 6],
        [1, 0, 2]
    ]
    goal_state = [
        [1, 2, 3],
        [8, 0, 4],
        [7, 6, 5]
    ]
    root = tk.Tk()
    gui = EightPuzzleGUI(root, initial_state, goal_state)
    root.mainloop()

if __name__ == "__main__":
    main()