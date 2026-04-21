import pygame
from classes import *
from variables import *
pygame.init()

# to do:
# - Zorgen dat wanneer je draait je niet in andere blokken kan komen
# - Rij weghalen wanneer hij vol zit (onderste rij uit grid en nieuwe bovenaan (denk ik))
# - Punten systeem met level up systeem
# - Game over systeem
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
                current.min_x, current.max_x = 4,0
                # HOORT NIET ZO MAAR TE KUNNEN DRAAIEN!!!
                current.rotation = (current.rotation + 1) % len(current.shape)
            if event.key == pygame.K_z:
                current.min_x, current.max_x = 4,0
                # HOORT NIET ZO MAAR TE KUNNEN DRAAIEN!!!
                current.rotation = (current.rotation - 1) % len(current.shape)
    
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
    current.move_down(tetris)
    current.move_horizontal(tetris)

    clock.tick(60)
    pygame.display.flip()