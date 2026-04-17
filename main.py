import pygame
pygame.init()

WHITE = (255, 255, 255)
size = (300, 600)
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill(WHITE)
    clock.tick(60)
    pygame.display.flip()