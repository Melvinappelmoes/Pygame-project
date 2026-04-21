import pygame
from classes import *
from variables import *
pygame.init()


# verschil maken tussen bewegende en permanente blokken
# detecten wanneer het de rand van scherm of een ander blok raakt
# dan moet het blok permanent gemaakt worden

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
                current.rotation = (current.rotation + 1) % len(current.shape)
            if event.key == pygame.K_z:
                current.min_x, current.max_x = 4,0
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