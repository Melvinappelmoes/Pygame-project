import pygame
from tetriminoes import *
from classes import *
from variables import *
pygame.init()

def make_grid():
    # maakt de grid door, door het hele bord in rijen te gaan met stapsgrootte = grid_size
    for x in range(0, window_width // grid_size):
        for y in range(0, window_height // grid_size):
            rect = pygame.Rect(x*grid_size, y*grid_size, grid_size, grid_size)
            pygame.draw.rect(screen, GREY, rect, 1)

# main gameloop (moet miss in een class)
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    i_t.draw()
    make_grid()
    clock.tick(1)
    pygame.display.flip()