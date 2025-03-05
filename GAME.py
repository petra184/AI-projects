import pygame as pg
from sudoku_screen import main as sudoku_main
from puzzle_screen import main as puzzle_main

# Initialize pygame
pg.init()

# Set up the screen
WIDTH, HEIGHT = 750, 750
screen = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("Game")

# Set up font
font = pg.font.Font(None, 50)

def draw_text(text, size, x, y):
    font = pg.font.Font(None, size)
    text_render = font.render(text, True, (0, 0, 0))
    text_rect = text_render.get_rect(center=(x, y))
    screen.blit(text_render, text_rect)

def button(text, x, y):
    font = pg.font.Font(None, 24)
    button_surface = pg.Surface((250, 50)) 
    button_surface.fill((255, 243, 150))
    pg.draw.rect(button_surface, pg.Color("Black"), pg.Rect(0, 0, 250, 50), 1)
    text_render = font.render(text, True, (0, 0, 0))  
    text_rect = text_render.get_rect(center=(button_surface.get_width() // 2, button_surface.get_height() // 2))
    button_rect = pg.Rect(x, y, 250, 50)
    button_surface.blit(text_render, text_rect)
    screen.blit(button_surface, (button_rect.x, button_rect.y))
    return button_rect

def back_button():
    return draw_text("Back", 25, 30, 20)

# Game states
MENU = "AI Agents"
SUDOKU = "sudoku"
PUZZLE = "puzzle"
current_screen = MENU

# Main loop
running = True
while running:
    screen.fill((255, 255, 255))
    
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        elif event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
            mouse_pos = event.pos
            if current_screen == MENU:
                if sudoku_rect.collidepoint(mouse_pos):
                    current_screen = SUDOKU
                    sudoku_main(screen)
                    current_screen = MENU 
                elif puzzle_rect.collidepoint(mouse_pos):
                    current_screen = PUZZLE
                    puzzle_main(screen) 
                    current_screen = MENU
            else:
                if back_rect.collidepoint(mouse_pos):
                    current_screen = MENU
    
    if current_screen == MENU:
        draw_text("AI Agents", 50, WIDTH // 2, 50)
        sudoku_rect = button("Sudoku Solver", WIDTH // 2 - 130, 200)
        puzzle_rect = button("8 Puzzle Problem", WIDTH // 2 - 130, 300)
    elif current_screen == PUZZLE:
        draw_text("8 Puzzle Problem", 50, WIDTH // 2, 50)
        back_rect = back_button()
    
    pg.display.flip()
    
pg.quit()

