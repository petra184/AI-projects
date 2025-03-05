def find_empty(aa):
    for i in range(9):
        for j in range(9):
            if aa[i][j] == 0:
                return (i, j)
    return None

def check(aa,option,row,col):
    row_options = aa[row]
    if option in row_options:
        return False

    col_options = []
    for i in range(9):
        col_options.append(aa[i][col])
    if option in col_options:
        return False

    row_block = (row//3)*3
    col_block = (col//3)*3
    for i in range(row_block, row_block+3):
        for j in range(col_block, col_block+3):
            if option == aa[i][j]:
                return False
    return True
     

def solve(aa):
    if find_empty(aa) == None:
        return True
    
    row,col = find_empty(aa)
    for option in range (1,10):
        if check(aa,option,row,col):
            aa[row][col] = option
            if solve(aa):
                return True

    aa[row][col] = 0
    return False

def valid_move(grid, row, col, num):
    for i in range(9):
        if grid[row][i] == str(num) or grid[i][col] == str(num):
            return False
    
    start_row, start_col = 3 * (row // 3), 3 * (col // 3)
    for i in range(start_row, start_row + 3):
        for j in range(start_col, start_col + 3):
            if grid[i][j] == str(num):
                return False
    return True