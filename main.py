import pygame
from classes import *
from variables import *
pygame.init()



# verschil maken tussen bewegende en permanente blokken
# detecten wanneer het de rand van scherm of een ander blok raakt
# dan moet het blok permanent gemaakt worden



def make_grid():
    # maakt de grid door, door het hele bord in rijen te gaan met stapsgrootte = grid_size
    for x in range(0, width // grid_size):
        for y in range(0, height // grid_size):
            rect = pygame.Rect(x*grid_size, y*grid_size, grid_size, grid_size)
            pygame.draw.rect(screen, GREY, rect, 1)

tetris = Tetris()
current = tetris.current_shape

# main gameloop
running = True
while running:
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
    make_grid()
    current.move_down()
    current.move_horizontal()

    clock.tick(60)
    pygame.display.flip()