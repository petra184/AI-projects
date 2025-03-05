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

def create_grid():
    grid = [[' ' for _ in range(3)] for _ in range(3)]
    print("Enter grid location that will be empty:")
    empty_row = int(input("Row: ")) - 1
    empty_col = int(input("Column: ")) - 1

    str(empty_row)
    str(empty_col)
    
    for i in range(3):
        for j in range(3):
            if i == empty_row and j == empty_col:
                continue
            else:
                grid[i][j] = input("Enter a number from 1 to 8: ")
                
    print("\nGrid after setting:")
    print_grid(grid)
                
    return grid

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
            

    
def bfs(grid):
    goal_state = [[' ', "1", "2"],["3","4","5"],["6","7","8"]]
    counter = 0
    empty_row, empty_col = locate_empty(grid)
    visited = Queue()
    unvisited = Queue()
    unvisited.add(empty_row, empty_col, grid)

    while not unvisited.isEmpty():
        counter+=1
        parent_grid, (empty_row, empty_col) = unvisited.pop()
        
        print(f"\n\nIteration {counter}, empty position is {empty_row, empty_col}:\n")
        print_grid(parent_grid)
        
        if parent_grid == goal_state:
            print(f"Solution found after {counter} iterations")
            return True
        
        get_neighbors(parent_grid, empty_row, empty_col, unvisited, visited)
        visited.add(empty_row, empty_col, parent_grid)
        
        visited.print("visited")
        unvisited.print("unvisited")   
        
    print("No solution found")
    return False
      
            
def main():
    grid= create_grid()
    print("\n")
    bfs(grid)

if __name__ == "__main__":
    main()