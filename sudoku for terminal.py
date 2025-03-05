def find_empty(aa):
    for i in range(9):
        for j in range(9):
            if aa[i][j] == 0:
                return (i, j)
    return None

def check(aa, option, row, col):
    if option in aa[row]:
        return False
    
    if option in [aa[i][col] for i in range(9)]:
        return False
    
    row_block, col_block = (row//3)*3, (col//3)*3
    for i in range(row_block, row_block+3):
        for j in range(col_block, col_block+3):
            if option == aa[i][j]:
                return False
    return True

def solve(aa):
    empty = find_empty(aa)
    if not empty:
        return True
    
    row, col = empty
    for option in range(1, 10):
        if check(aa, option, row, col):
            aa[row][col] = option
            if solve(aa):
                return True
            aa[row][col] = 0
    
    return False

def valid_move(grid, row, col, num):
    num = str(num)
    if num in grid[row] or num in [grid[i][col] for i in range(9)]:
        return False
    
    start_row, start_col = 3 * (row // 3), 3 * (col // 3)
    for i in range(start_row, start_row + 3):
        for j in range(start_col, start_col + 3):
            if grid[i][j] == num:
                return False
    return True

def print_grid(grid):
    for row in grid:
        print("+---" * 9 + "+")
        print("| " + " | ".join(str(num) if num != 0 else ' ' for num in row) + " |")
    print("+---" * 9 + "+")

def check_bounds(row, col):
    return 0 <= row < 9 and 0 <= col < 9

def create_grid():
    grid = [[0 for _ in range(9)] for _ in range(9)]
    print("Enter the Sudoku puzzle row by row (use 0 for empty spaces):")
    
    for i in range(9):
        grid[i] = list(map(int, input(f"Row {i+1}: ").split()))
    
    print("\nGrid before solving:")
    print_grid(grid)
    return grid

def main():
    grid = create_grid()
    if solve(grid):
        print("\nSolved Sudoku:")
        print_grid(grid)
    else:
        print("No solution exists.")

if __name__ == "__main__":
    main()