class Queue:
    def __init__(self):
        self.queue = list()
        self.dictionary = {}
        
    def isEmpty(self):
        return len(self.queue) == 0
    
    def add(self, row, col, grid):
        key = tuple(tuple(row) for row in grid)
        value = (row, col)
        if key not in self.dictionary:
            self.queue.append(key)
            self.dictionary[key] = value
        
    def pop(self):
        if not self.isEmpty():
            key = self.queue.pop(0)
            return [list(row) for row in key], self.dictionary.pop(key)
        else:
            return None, None
    
    def check_grid(self, grid):
        key = tuple(tuple(row) for row in grid)
        return key in self.dictionary
    
    def size(self):
        return len(self.dictionary)
    
    def print(self, title):
        print(title)
        for key, position in self.dictionary.items():
            print(f"Key {key}: {position}")


        
def print_grid(grid):
    for row in grid:
        print("+---" * 3 + "+")
        print("| " + " | ".join(row) + " |")
    print("+---" * 3 + "+")

def locate_empty(grid):
    for row in range(len(grid)):
        for col in range(len(grid[row])):
            if grid[row][col] == ' ':
                return row, col
    return None

def check_bounds(row,col):
    if 0<=row<=2 and 0<=col<=2:
        return True
    else:
        return False

def swap_positions(grid, empty_row, empty_col, new_row, new_col):
    new_grid = [row[:] for row in grid] 
    new_grid[empty_row][empty_col], new_grid[new_row][new_col] = new_grid[new_row][new_col], new_grid[empty_row][empty_col]
    return new_grid

def get_neighbors(grid, empty_row, empty_col, unvisited, visited):
    # Left
    if check_bounds(empty_row, empty_col - 1):
        new_grid = swap_positions(grid, empty_row, empty_col, empty_row, empty_col - 1)
        if not visited.check_grid(new_grid) and not unvisited.check_grid(new_grid):
            unvisited.add(empty_row, empty_col - 1, new_grid)
        
    # Right
    if check_bounds(empty_row, empty_col + 1):
        new_grid = swap_positions(grid, empty_row, empty_col, empty_row, empty_col + 1)
        if not visited.check_grid(new_grid) and not unvisited.check_grid(new_grid):
            unvisited.add(empty_row, empty_col + 1, new_grid)
        
    # Up
    if check_bounds(empty_row - 1, empty_col):
        new_grid = swap_positions(grid, empty_row, empty_col, empty_row - 1, empty_col)
        if not visited.check_grid(new_grid) and not unvisited.check_grid(new_grid):
            unvisited.add(empty_row - 1, empty_col, new_grid)
        
    # Down
    if check_bounds(empty_row + 1, empty_col):
        new_grid = swap_positions(grid, empty_row, empty_col, empty_row + 1, empty_col)
        if not visited.check_grid(new_grid) and not unvisited.check_grid(new_grid):
            unvisited.add(empty_row + 1, empty_col, new_grid)
            

    
def bfs(grid, callback=None, break_flag=None):
    goal_state = [[' ', "1", "2"],["3","4","5"],["6","7","8"]]
    counter = 0
    empty_row, empty_col = locate_empty(grid)
    visited = Queue()
    unvisited = Queue()
    unvisited.add(empty_row, empty_col, grid)
    
    # Store all states for visualization
    all_states = []

    while not unvisited.isEmpty():
        # Check if break flag is set
        if break_flag and break_flag[0]:
            print("BFS algorithm interrupted by user")
            break
            
        counter+=1
        parent_grid, (empty_row, empty_col) = unvisited.pop()
        
        print(f"\n\nIteration {counter}, empty position is {empty_row, empty_col}:\n")
        print_grid(parent_grid)
        
        # Add current state to the list
        all_states.append((parent_grid, empty_row, empty_col))
        
        # Call the callback function if provided
        if callback:
            callback(parent_grid, counter)
        
        if parent_grid == goal_state:
            print(f"Solution found after {counter} iterations")
            
            # Get the counts of states in frontier and explored set
            frontier_count = unvisited.size()
            explored_count = visited.size()
            total_states = frontier_count + explored_count
            
            print(f"Total states saved: {total_states}")
            print(f"States in frontier: {frontier_count}")
            print(f"States in explored set: {explored_count}")
            
            return True, all_states, total_states, frontier_count, explored_count
        
        get_neighbors(parent_grid, empty_row, empty_col, unvisited, visited)
        visited.add(empty_row, empty_col, parent_grid)
        
        visited.print("visited")
        unvisited.print("unvisited")   
    
    # Get the counts of states in frontier and explored set
    frontier_count = unvisited.size()
    explored_count = visited.size()
    total_states = frontier_count + explored_count
    
    print(f"Total states saved: {total_states}")
    print(f"States in frontier: {frontier_count}")
    print(f"States in explored set: {explored_count}")
    
    print("No solution found")
    return False, all_states, total_states, frontier_count, explored_count
      