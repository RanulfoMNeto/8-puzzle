from collections import deque
import heapq

class Solver:

    EMPTY = 0 # Represents the value indicating an empty tile in the puzzle state.

    @staticmethod
    def find_index(state, value):
        """
        Finds the coordinates of the empty tile (represented by EMPTY) in the puzzle state.

        Args:
        - state (list of list): Current state of the puzzle.

        Returns:
        - tuple or None: Coordinates (row, column) of the empty tile if found,
        or None if the empty tile is not present in the state.
        """
        size = len(state)
        for i in range(size):
            for j in range(size):
                if state[i][j] == value:
                    return (i, j)
        
        return None

    @staticmethod
    def move(state, direction):
        """
        Moves the empty tile in the specified direction if valid.

        Args:
        - state (list of list): Current state of the puzzle.
        - direction (tuple): Movement direction (delta row, delta column).

        Returns:
        - list of list: New state after moving the empty tile in the specified direction,
        or None if movement is invalid.
        """
        size = len(state)
        empty = Solver.find_index(state, Solver.EMPTY)

        position = (empty[0] + direction[0], empty[1] + direction[1])

        if 0 <= position[0] < size and 0 <= position[1] < size:
            # Make a copy of the state as a list of lists to avoid modifying the original tuples.
            adjacent = [row[:] for row in state]
            adjacent[empty[0]][empty[1]] = adjacent[position[0]][position[1]]
            adjacent[position[0]][position[1]] = Solver.EMPTY
            return adjacent
        
        return None

    @staticmethod
    def adjacents(state):
        """
        Generates all possible states by moving the empty tile in all valid directions.

        Args:
        - state (list of list): Current state of the puzzle.

        Returns:
        - list of list: List of all adjacent states.
        """
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # [Up, down, left, right]
        states = []

        for direction in directions:
            adjacent = Solver.move(state, direction)
            if adjacent:
                states.append(adjacent)

        return states

    @staticmethod
    def bfs(initial, goal):
        """
        Performs Breadth-First Search (BFS) to find the shortest path from initial state to goal state.

        Args:
        - initial (list of list): Initial state of the puzzle.
        - goal (list of list): Goal state that we want to achieve.

        Returns:
        - list: List of states representing the shortest path from initial to goal state,
        or None if no solution is found.
        """
        queue = deque([(initial, [])])
        visited = set()

        while queue:
            current, path = queue.popleft() # Dequeue the first element in the queue

            for adjacent in Solver.adjacents(current):
                # Convert the state (list of lists) into a tuple of tuples for immutability and set compatibility.
                state_tuple = tuple(tuple(row) for row in adjacent)
                if state_tuple not in visited:
                    visited.add(state_tuple)
                    solution = path + [adjacent]
                    queue.append((adjacent, solution))
                    if adjacent == goal:
                        return solution
                    
        return None

    @staticmethod
    def a_star(initial, goal):
        """
        Performs A* search to find the shortest path from initial state to goal state.

        Args:
        - initial (list of list): Initial state of the puzzle.
        - goal (list of list): Goal state that we want to achieve.

        Returns:
        - list: List of states representing the shortest path from initial to goal state,
        or None if no solution is found.
        """
        queue = []
        heapq.heappush(queue, (0, initial, []))  # Start with initial state, priority 0, and empty path
        visited = set()

        while queue:
            _, current, path = heapq.heappop(queue)  # Pop the state with the lowest priority

            for adjacent in Solver.adjacents(current):
                # Convert the state (list of lists) into a tuple of tuples for immutability and set compatibility.
                state_tuple = tuple(tuple(row) for row in adjacent)
                if state_tuple not in visited:
                    visited.add(state_tuple)
                    # Calculate priority for A* search: path length so far + heuristic (manhattan distance to goal)
                    priority = len(path) + 1 + Solver.manhattan_distance(adjacent, goal)
                    solution = path + [adjacent]
                    heapq.heappush(queue, (priority, adjacent, solution))
                    if adjacent == goal:
                        return solution  # Return the solution path if goal state is reached
        
        return None  # Return None if no solution is found

    @staticmethod
    def manhattan_distance(state, goal):
        """
        Calculates the Manhattan distance between two puzzle states.

        Args:
        - state (list of list): Current state of the puzzle.
        - goal (list of list): Goal state of the puzzle.

        Returns:
        - int: Manhattan distance between the current state and the goal state.
        """
        distance = 0
        size = len(state)

        for i in range(size):
            for j in range(size):
                value = state[i][j]
                if value != Solver.EMPTY:  # Calculate distance only for non-empty tiles
                    x, y = Solver.find_index(goal, value)  # Find the position of the same tile in the goal state
                    distance += abs(i - x) + abs(j - y)  # Calculate Manhattan distance

        return distance