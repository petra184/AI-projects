import pygame as pg
import sys
from BFS import *

def main(screen):
    # Get screen dimensions
    screen_width, screen_height = screen.get_size()
    
    # Calculate center positions
    center_x = screen_width // 2
    center_y = screen_height // 2
    
    # Calculate grid position (centered)
    grid_size = 300  # 3x3 grid, each cell 100x100
    grid_x = center_x - grid_size // 2
    grid_y = center_y - grid_size // 2 - 50  # Shift up a bit to make room for buttons
    
    clock = pg.time.Clock()
    base_font = pg.font.Font(None, 48)
    title_font = pg.font.Font(None, 48)
    info_font = pg.font.Font(None, 24)

    grid = [[' ' for _ in range(3)] for _ in range(3)]
    active_cell = [0, 0]
    active_color = pg.Color(230, 230, 230)
    back_button_rect = pg.Rect(20, 20, 60, 30)
    
    # States for the game
    SETUP = 0
    SOLVING = 1
    SOLUTION = 2
    
    game_state = SETUP
    solution_states = []
    current_state_index = 0
    iteration_count = 0
    break_flag = [False]  # Using a list so it can be modified by reference
    
    # Stats
    total_states = 0
    frontier_count = 0
    explored_count = 0
    
    def draw_grid(current_grid=None):
        if current_grid is None:
            current_grid = grid
            
        for i in range(3):
            for j in range(3):
                rect = pg.Rect(grid_x + j * 100, grid_y + i * 100, 100, 100)
                color = active_color if [i, j] == active_cell and game_state == SETUP else pg.Color("White")
                pg.draw.rect(screen, color, rect)
                pg.draw.rect(screen, pg.Color("Black"), rect, 2)
                if current_grid[i][j] != ' ':
                    text = base_font.render(str(current_grid[i][j]), True, pg.Color("Black"))
                    text_rect = text.get_rect(center=rect.center)
                    screen.blit(text, text_rect)

    def draw_button(text, x, y, width=100, height=50, color=(173, 216, 230)):
        button_surface = pg.Surface((width, height))
        button_surface.fill(color)
        pg.draw.rect(button_surface, pg.Color("Black"), pg.Rect(0, 0, width, height), 1)
        text_surf = pg.font.Font(None, 24).render(text, True, (0, 0, 0))
        text_rect = text_surf.get_rect(center=(button_surface.get_width() // 2, button_surface.get_height() // 2))
        button_surface.blit(text_surf, text_rect)
        button_rect = pg.Rect(x, y, width, height)
        screen.blit(button_surface, (button_rect.x, button_rect.y))
        return button_rect

    def back_button():
        font = pg.font.Font(None, 24)
        text = font.render("Back", True, (0, 30, 20))
        screen.blit(text, (back_button_rect.x + 10, back_button_rect.y + 5))

    def draw_title():
        title_surface = title_font.render("8-PUZZLE SOLVER", True, (0, 0, 0))
        title_rect = title_surface.get_rect(center=(center_x, 40))
        screen.blit(title_surface, title_rect)
        
    def draw_info():
        if game_state == SOLVING:
            info_text = f"Iteration: {iteration_count}"
            info_surface = info_font.render(info_text, True, (0, 0, 0))
            screen.blit(info_surface, (grid_x, grid_y - 30))
        elif game_state == SOLUTION:
            info_text = f"Step: {current_state_index + 1}/{len(solution_states)}"
            info_surface = info_font.render(info_text, True, (0, 0, 0))
            screen.blit(info_surface, (grid_x, grid_y - 30))
            
        # Display stats at the bottom of the screen
        if game_state == SOLUTION:
            stats_text = f"Total States: {total_states} | Frontier: {frontier_count} | Explored: {explored_count}"
            stats_surface = info_font.render(stats_text, True, (0, 0, 0))
            stats_rect = stats_surface.get_rect(center=(center_x, screen_height - 30))
            screen.blit(stats_surface, stats_rect)

    def move_active_cell(direction):
        if direction == 'up' and active_cell[0] > 0:
            active_cell[0] -= 1
        elif direction == 'down' and active_cell[0] < 2:
            active_cell[0] += 1
        elif direction == 'left' and active_cell[1] > 0:
            active_cell[1] -= 1
        elif direction == 'right' and active_cell[1] < 2:
            active_cell[1] += 1

    def update_display_callback(current_grid, iteration):
        nonlocal iteration_count
        iteration_count = iteration
        screen.fill(pg.Color("White"))
        draw_title()
        draw_grid(current_grid)
        draw_info()
        
        # Draw break button in the middle during solving
        break_button = draw_button("BREAK", center_x - 50, center_y + grid_size // 2 + 30, color=(255, 100, 100))
        
        pg.display.flip()
        
        # Check for break button click
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                if break_button.collidepoint(event.pos):
                    break_flag[0] = True
        
        pg.time.delay(200) 
        
    def solve_puzzle():
        nonlocal game_state, solution_states, current_state_index, break_flag
        nonlocal total_states, frontier_count, explored_count
        
        game_state = SOLVING
        break_flag[0] = False  # Reset break flag
        
        # Run BFS and get all states
        solution_found, solution_states, total_states, frontier_count, explored_count = bfs(grid, update_display_callback, break_flag)
        
        if solution_found:
            game_state = SOLUTION
            current_state_index = len(solution_states) - 1  # Show the final solution state
        else:
            game_state = SETUP
            
    running = True
    
    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()

            if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = event.pos

                if back_button_rect.collidepoint(mouse_pos):
                    running = False 

                if solve_button.collidepoint(mouse_pos) and game_state == SETUP:
                    solve_puzzle()

                if clear_button.collidepoint(mouse_pos):
                    grid = [[' ' for _ in range(3)] for _ in range(3)]
                    active_cell = [0, 0]
                    game_state = SETUP
                    solution_states = []
                    current_state_index = 0
                    iteration_count = 0

                for i in range(3):
                    for j in range(3):
                        rect = pg.Rect(grid_x + j * 100, grid_y + i * 100, 100, 100)
                        if rect.collidepoint(mouse_pos) and game_state == SETUP:
                            active_cell = [i, j]
                                
            if event.type == pg.KEYDOWN and game_state == SETUP:
                if event.key == pg.K_UP:
                    move_active_cell('up')
                elif event.key == pg.K_DOWN:
                    move_active_cell('down')
                elif event.key == pg.K_LEFT:
                    move_active_cell('left')
                elif event.key == pg.K_RIGHT:
                    move_active_cell('right')
                elif event.key == pg.K_BACKSPACE:
                    grid[active_cell[0]][active_cell[1]] = ' '  # Allow clearing the cell
                elif event.unicode.isdigit():
                    num = int(event.unicode)
                    if 1 <= num <= 8:
                        # Check if the number is already present in the grid
                        if str(num) not in [item for sublist in grid for item in sublist]:
                            grid[active_cell[0]][active_cell[1]] = str(num)
                    elif num == 0:
                        grid[active_cell[0]][active_cell[1]] = ' '  # Use space for empty cell

        screen.fill(pg.Color("White"))
        draw_title()
        draw_info()
        
        # Draw the grid based on the current state
        if game_state == SETUP:
            draw_grid()
        elif game_state == SOLUTION and solution_states:
            current_grid, _, _ = solution_states[current_state_index]
            draw_grid(current_grid)
        
        # Always show SOLVE and CLEAR buttons
        solve_button = draw_button("SOLVE", center_x - 110, grid_y + grid_size + 20)
        clear_button = draw_button("CLEAR", center_x + 10, grid_y + grid_size + 20)
        
        back_button()

        pg.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    pg.init()
    screen = pg.display.set_mode([700, 600])
    pg.display.set_caption('8-PUZZLE SOLVER')
    main(screen)
    pg.quit()

