import pygame
from classes import *
from variables import *
pygame.init()

# to do:
# - Punten systeem met level up systeem
# - Game over systeem (checken of er een 1 in de bovenste rij zit)
# - High score opslaan (SQL)
# - Menu
# - Volgende tetriminos laten zien
# - Een hold cel
# - MUZIEK

tetris = Tetris()

# main gameloop
running = True
while running:
    running = tetris.game_over()
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
                current.move_down(tetris, True)
            if event.key == pygame.K_DOWN:
                current.fall_speed *= (1/20)
            if event.key == pygame.K_ESCAPE:
                tetris.pause()
    
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_DOWN:
                current.fall_speed = (0.8 - ((tetris.level - 1) * 0.007))**(tetris.level-1)

    screen.fill(BLACK)
    
    if tetris.clearing:
        tetris.clear_rows()
    elif tetris.spawn_ready:
        tetris.spawn_block()
        tetris.spawn_ready = False
    else: 
        current.draw(tetris)
        current.ghost_piece(tetris)
        current.move_down(tetris, False)
        current.move_horizontal(tetris)

    tetris.draw_grid()

    clock.tick(fps)
    pygame.display.flip()