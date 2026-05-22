import pygame
from classes import *
from variables import *
pygame.init()


# to do:
# - Shapes in database??
# - High score opslaan (SQL)
# - Menu
# - Volgende tetriminos laten zien (miss nog ietsje mooier)
# - MUZIEK

tetris = Tetris()
arrow_down = False

# main gameloop
running = True
while running:
    running,end_screen = tetris.game_over()
    current = tetris.current_shape
    tetris.calculate_level()
    for event in pygame.event.get():
        if event.type == pygame.QUIT: 
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                current.rotate(tetris, 1)
            if event.key == pygame.K_z:
                current.rotate(tetris, -1)
            if event.key == pygame.K_SPACE:
                current.move_down(tetris, True, arrow_down)
            if event.key == pygame.K_DOWN:
                current.fall_speed *= (1/20)
                arrow_down = True
            if event.key == pygame.K_ESCAPE:
                running = tetris.pause()
            if event.key == pygame.K_c:
                tetris.hold_cell()
                tetris.hold_available = False
    
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_DOWN:
                current.fall_speed = (0.8 - ((tetris.level - 1) * 0.007))**(tetris.level-1)
                arrow_down = False

    screen.fill(DARK_GREY)
    pygame.draw.rect(screen, BLACK, rect_grid)

    tetris.print_text()
    tetris.next_queue()
    tetris.draw_hold_cell()
    if tetris.clearing:
        tetris.clear_rows()
    elif tetris.spawn_ready:
        tetris.spawn_block()
        tetris.hold_available = True
        tetris.spawn_ready = False
        current = tetris.current_shape
    else: 
        current.draw()
        current.ghost_piece(tetris)
        current.move_down(tetris, False, arrow_down)
        current.move_horizontal(tetris)

    tetris.draw_grid()

    clock.tick(fps)
    pygame.display.flip()



while end_screen:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: 
            end_screen = False
    screen.fill(DARK_GREY)
    game_over_text = font.render("GAME OVER", True, WHITE)
    screen.blit(game_over_text, (width_screen//2 - game_over_text.get_width()//2, heigth_screen//2 - grid_size))
    score = font.render(f"SCORE: {int(tetris.score)} ", True, WHITE)
    screen.blit(score, (width_screen//2 - score.get_width()//2, heigth_screen//2))
    clock.tick(fps)
    pygame.display.flip()