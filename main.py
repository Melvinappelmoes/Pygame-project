import pygame, sqlite3
from classes import *
from variables import *
pygame.init()


# to do:
# - Shapes in database??
# - High score opslaan (SQL)
# - Menu
# - Volgende tetriminos laten zien (miss nog ietsje mooier)
# - MUZIEK
# beginnen op een ander level

tetris = Tetris()
high_scores = Highscores()
arrow_down = False

# main gameloop
running = True
while running:
    pygame.mixer.music.set_volume(geluidsniveau)
    if tetris.state == "menu":
        mouse = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT: 
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_rect.left <= mouse[0] <= play_rect.right and play_rect.top <= mouse[1] <= play_rect.bottom:
                    tetris.state = "main"
                if level_rect.left <= mouse[0] <= level_rect.right and level_rect.top <= mouse[1] <= level_rect.bottom:
                    print("Dit zou eigenlijk de level moeten verhogen")
                if settings_rect.left <= mouse[0] <= settings_rect.right and settings_rect.top <= mouse[1] <= settings_rect.bottom:
                    tetris.mute_i = (tetris.mute_i + 1)%2
                    geluidsniveau = (geluidsniveau + 0.3)%0.6
                    sound_stage_clear.set_volume(geluidsniveau)
                    sound_game_over.set_volume(geluidsniveau)
        screen.fill(DARK_GREY)
        
        tetris.start_screen(mouse)

        clock.tick(fps)
        pygame.display.flip()

    elif tetris.state == "paused":
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    tetris.state = "main"
        screen.fill(DARK_GREY)
        pygame.draw.rect(screen, BLACK, rect_grid)

        tetris.draw_grid(tetris.empty_grid)
        tetris.print_text()
        tetris.next_queue(False)
        tetris.draw_hold_cell(False)

        clock.tick(fps)
        pygame.display.flip()

    elif tetris.state == "main":
        tetris.game_over()
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
                    tetris.state = "paused"
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
        tetris.next_queue(True)
        tetris.draw_hold_cell(True)
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

        tetris.draw_grid(tetris.grid)

        clock.tick(fps)
        pygame.display.flip()
    
    elif tetris.state == "game over":
        mouse = pygame.mouse.get_pos()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT: 
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if home_rect.left <= mouse[0] <= home_rect.right and home_rect.top <= mouse[1] <= home_rect.bottom:
                    tetris = Tetris()
                    tetris.state = "menu"
                if replay_rect.left <= mouse[0] <= replay_rect.right and replay_rect.top <= mouse[1] <= replay_rect.bottom:
                    tetris = Tetris()
                    tetris.state = "main"
        
        screen.fill(DARK_GREY)

        tetris.print_text()
        tetris.next_queue(True)
        tetris.draw_hold_cell(True)
        pygame.draw.rect(screen, BLACK, rect_grid)
        tetris.draw_grid(tetris.grid)
        
        pygame.draw.rect(screen, BLACK, game_over_rect)
        pygame.draw.rect(screen, WHITE, game_over_rect, 1)
     
        game_over_text = font.render("GAME OVER", True, WHITE)
        screen.blit(game_over_text, (width_screen//2 - game_over_text.get_width()//2, heigth_screen//2 - 60))
        score = font.render(f"SCORE: {int(tetris.score)} ", True, WHITE)
        screen.blit(score, (width_screen//2 - score.get_width()//2, heigth_screen//2 - 30))

        if home_rect.left <= mouse[0] <= home_rect.right and home_rect.top <= mouse[1] <= home_rect.bottom:
            pygame.draw.rect(screen, LIGHTER_GREY, home_rect)
            pygame.draw.rect(screen, WHITE, home_rect, 1)
        else:
            pygame.draw.rect(screen, GREY, home_rect)
        home_button = pygame.transform.scale(pygame.image.load("home_button.png"), (40, 40))
        screen.blit(home_button, (home_rect.x + 5, home_rect.y + 5))

        if replay_rect.left <= mouse[0] <= replay_rect.right and replay_rect.top <= mouse[1] <= replay_rect.bottom:
            pygame.draw.rect(screen, LIGHTER_DARK_GREEN, replay_rect)
            pygame.draw.rect(screen, WHITE, replay_rect, 1)
        else:
            pygame.draw.rect(screen, DARK_GREEN, replay_rect)
        replay_button = pygame.transform.scale(pygame.image.load("replay.png"), (40, 40))
        screen.blit(replay_button, (replay_rect.x + 5, replay_rect.y + 5))

        clock.tick(fps)
        pygame.display.flip()