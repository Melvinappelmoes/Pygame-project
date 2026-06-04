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
DARK_GREEN = (15, 155, 15)
LIGHTER_DARK_GREEN = (15, 175, 15)
LIGHTER_GREY = (100, 100, 100)

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
logo = pygame.transform.scale(pygame.image.load("tetris_logo.png"), (175.8*1.5, 122.2*1.5))
pygame.display.set_icon(logo)
clock = pygame.time.Clock()

play_rect = pygame.Rect(width_screen//2 - 100, y_grid + logo.get_height() + 20, 200, 50)
level_rect = pygame.Rect(width_screen//2 - 100, play_rect.bottom + 10, 200, 50)
settings_rect = pygame.Rect(x_grid + width_grid - 60, height_grid + y_grid - 60, 50, 50)
high_scores_rect = pygame.Rect(width_screen//2 - 140, level_rect.bottom + 10, width_grid - 20, settings_rect.top - 20 - level_rect.bottom)
game_over_rect = pygame.Rect(width_screen//2 - 100, heigth_screen//2 - 75, 200, 150)
home_rect = pygame.Rect(width_screen//2 - 90, heigth_screen//2 + 15, 50, 50)
replay_rect = pygame.Rect(width_screen//2 - 30, heigth_screen//2 + 15, 50, 50)

# kan je het geluidsniveau aanpassen (tussen 0.0 en 1.0)
geluidsniveau = 0.3
pygame.mixer.music.set_volume(geluidsniveau)

# maakt de standaard muziek
pygame.mixer.music.load("Tetris_muziek.mp3")
pygame.mixer.music.play(-1)

# maakt de sound effects
sound_stage_clear = pygame.mixer.Sound('Tetris_stage_clear.mp3')
sound_game_over = pygame.mixer.Sound('Tetris_game_over.mp3')
sound_stage_clear.set_volume(geluidsniveau)
sound_game_over.set_volume(geluidsniveau)

# font
font = pygame.font.SysFont("Kijs", 37)

fps = 60

fall_speeds = [
    0.800, 0.717, 0.633, 0.550, 0.467,
    0.383, 0.300, 0.217, 0.133, 0.100,
    0.100, 0.100, 0.083, 0.083, 0.083,
    0.067, 0.067, 0.067, 0.050, 0.050,
    0.050, 0.050, 0.050, 0.050, 0.050,
    0.050, 0.050, 0.050, 0.050, 0.017
]

# verstreken tijd sinds laatste keer op geroepen
delta_time = clock.tick(fps) / 1000