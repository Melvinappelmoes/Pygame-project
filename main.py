import pygame
import random
from tetriminoes import tetriminoes
from classes import *
from variables import *
pygame.init()

def make_grid():
    # maakt de grid door, door het hele bord in rijen te gaan met stapsgrootte = grid_size
    for x in range(0, width // grid_size):
        for y in range(0, height // grid_size):
            rect = pygame.Rect(x*grid_size, y*grid_size, grid_size, grid_size)
            pygame.draw.rect(screen, GREY, rect, 1)

def random_tetrimino():
    letter = random.choice(list(tetriminoes.keys()))
    return tetriminoes[letter]

t = random_tetrimino()

# main gameloop (moet miss nog in een class)
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                t.rotation = (t.rotation + 1) % len(t.shape)
            if event.key == pygame.K_n:
                t = random_tetrimino()

    screen.fill(BLACK)
    
    t.draw()
    make_grid()

    # moet nog vertraagd worden
    # t.move_down() !!!

    clock.tick(30)
    pygame.display.flip()