import pygame
pygame.font.init()

# maakt alle benodigde kleuren
GREY = (75, 75, 75)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
LIGHT_BLUE = (0,191,255)
PURPLE = (191,0,255)
ORANGE = (255,130,0)
BLUE = (0,50,210)
GREEN = (0, 230, 0)
RED = (250, 0, 0)
WHITE = (255, 255, 255)
DARK_GREY = (25, 25, 25)

# maakt de variablen voor de grid
width_grid = 300
height_grid = width_grid * 2
grid_size = width_grid // 10
width_ghost = 2

# screen
width_screen = 800
heigth_screen = 600 + 2*grid_size

# location grid
x_grid = (width_screen // 2) - (width_grid // 2)
y_grid = grid_size

# maakt het scherm en de klok
screen = pygame.display.set_mode((width_screen, heigth_screen))
rect_grid = pygame.Rect(x_grid, y_grid, width_grid, height_grid)

pygame.display.set_caption('Tetris')
logo = pygame.image.load("tetris_logo.png")
pygame.display.set_icon(logo)
clock = pygame.time.Clock()

font = pygame.font.SysFont("arial", 25)

fps = 60

delta_time = clock.tick(60) / 1000