import pygame
pygame.init()

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
LIGHT_BLUE = (0,191,255)
PURPLE = (128,0,128)
ORANGE = (255,165,0)
BLUE = (0,0,255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

size = 300, 600
grid_size = 30

screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()

class Tetrimino():
    def __init__(self, shape):
        self.x = 150
        self.y = -60
        self.shape = shape
        self.rotation = 0

o_t = [[1, 1],
       [1, 1]],

i_t_1 = [[[1],
       [1],
       [1],
       [1]],

       [[1, 1, 1, 1]]]

i_t_2 = [[[0, 0, 1, 0],
         [0, 0, 1, 0],
         [0, 0, 1, 0],
         [0, 0, 1, 0]],
         
         [[0, 0, 0, 0],
          [0, 0, 0, 0],
          [1, 1, 1, 1],
          [0, 0, 0, 0]]]

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    screen.fill(BLACK)
    clock.tick(60)
    pygame.display.flip()