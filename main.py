import pygame
from classes import *
from variables import *
pygame.init()

# to do:
# - Miss rij weghalen cleaner maken
# - Punten systeem met level up systeem
# - Game over systeem (checken of er een 1 in de bovenste rij zit)
# - Ghost piece
# - High score opslaan (SQL)
# - Menu
# - Volgende tetriminos laten zien
# - Een hold cel
# - MUZIEK

tetris = Tetris()

# main gameloop
running = True
while running:
    current = tetris.current_shape
    for event in pygame.event.get():
        if event.type == pygame.QUIT: 
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                current.rotate(tetris, 1)
            if event.key == pygame.K_z:
                current.rotate(tetris, -1)
            if event.key == pygame.K_SPACE:
                current.fall_speed = 0.0001
            if event.key == pygame.K_DOWN:
                current.fall_speed *= (1/20)
    
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_DOWN:
                current.fall_speed = (0.8 - ((tetris.level - 1) * 0.007))**(tetris.level-1)

    screen.fill(BLACK)
    
    current.draw()
    tetris.draw_grid()
    current.move_horizontal(tetris)
    current.move_down(tetris)
    

    clock.tick(60)
    pygame.display.flip()