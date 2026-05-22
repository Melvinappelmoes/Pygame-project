import pygame
pygame.font.init()
pygame.init()

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
width_screen = 780
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

# kan je het geluidsniveau aanpassen (tussen 0.0 en 1.0)
geluidsniveau = 0.3
pygame.mixer.music.set_volume(geluidsniveau)

# maakt de standaard muziek
pygame.mixer.music.load("Tetris_muziek.mp3")
pygame.mixer.music.play(-1)

# maakt de sound effects
sound_stage_clear = pygame.mixer.Sound('Tetris_stage_clear.mp3')
sound_game_over = pygame.mixer.Sound('Tetris_game_over.mp3')

# font
font = pygame.font.SysFont("arial", 25)

fps = 60

# verstreken tijd sinds laatste keer op geroepen
delta_time = clock.tick(60) / 1000