import pygame

# maakt alle benodigde kleuren
GREY = (75, 75, 75)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
LIGHT_BLUE = (0,191,255)
PURPLE = (128,0,128)
ORANGE = (255,165,0)
BLUE = (0,0,255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# maakt de variablen voor het scherm
width = 300
height = 2 * width
grid_size = 30

# maakt het scherm en de klok
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Tetris')
logo = pygame.image.load("tetris_logo.png")
pygame.display.set_icon(logo)
clock = pygame.time.Clock()

delta_time = clock.tick(60) / 1000

keys_pressed = pygame.key.get_pressed()