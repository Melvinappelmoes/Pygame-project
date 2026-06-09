import pygame
from classes import *
from variables import *
pygame.init()


# to do:
# - Pauze menu
# - Eind menu
# - MUZIEK zelluf


tetris = Tetris()
highscores = Highscores()
arrow_down = False

# main gameloop
running = True
while running:
    # verstreken tijd sinds laatste keer op geroepen
    delta_time = clock.tick(fps) / 1000
    pygame.mixer.music.set_volume(geluidsniveau)
    mouse = pygame.mouse.get_pos()
    if tetris.state == "menu":
        for event in pygame.event.get():
            if event.type == pygame.QUIT: 
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DELETE:
                    highscores.reset_database()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_rect.collidepoint(mouse):
                    tetris.random_tetriminos() 
                    tetris.current_shape = tetris.tetriminos[0]
                    tetris.state = "main"
                if level_rect.collidepoint(mouse):
                    tetris.level = tetris.level%30 + 1
                    tetris.start_level = tetris.level + 1
                if mute_rect.collidepoint(mouse):
                    tetris.mute_i = (tetris.mute_i + 1)%2
                    geluidsniveau = (geluidsniveau + 0.3)%0.6
                    sound_stage_clear.set_volume(geluidsniveau)
                    sound_game_over.set_volume(geluidsniveau)
        screen.fill(DARK_GREY)
        
        tetris.print_text()
        tetris.next_queue(False)
        tetris.draw_hold_cell(False)

        pygame.draw.rect(screen, BLACK, rect_grid)

        screen.blit(logo, (x_grid + width_grid//2 - logo.get_width()//2, y_grid + 10))

        draw_button(play_rect, "PLAY", font1, DARK_GREEN, LIGHTER_DARK_GREEN, mouse)
        draw_button(level_rect, f"LEVEL: {tetris.level}", font1, GREY, LIGHTER_GREY, mouse)
        draw_button(mute_rect, "", font1, GREY, LIGHTER_GREY, mouse)

        pygame.draw.rect(screen, LIGHTER_GREY, high_scores_rect, 1)
        mute = pygame.transform.scale(pygame.image.load(f"{tetris.mute[tetris.mute_i]}.png"), (40, 40))
        screen.blit(mute, (mute_rect.x + 5, mute_rect.y + 5))

        highscore_text = font1.render("HIGHSCORES", True, WHITE)
        screen.blit(highscore_text, (width_screen//2 - highscore_text.get_width()//2, high_scores_rect.top + space))

        highscores_list = highscores.get_highscores()
        for i, naam_en_score in enumerate(highscores_list):
            naam_text = font2.render(f"{naam_en_score[0].upper()}", True, WHITE)
            score_text = font2.render(f"{naam_en_score[1]}", True, WHITE)
            screen.blit(naam_text, (high_scores_rect.left + 2*space, high_scores_rect.top + space + i * 3*space + 40))
            screen.blit(score_text, (high_scores_rect.right - 2*space - score_text.get_width(), high_scores_rect.top + space + i * 3*space + 40))

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
        pygame.draw.rect(screen, BLACK, pause_rect)
        pygame.draw.rect(screen, WHITE, pause_rect, 1)
        paused_text = font1.render("PAUSED", True, WHITE)
        screen.blit(paused_text, (pause_rect.centerx - paused_text.get_width()//2, pause_rect.centery - paused_text.get_height()//2))

        clock.tick(fps)
        pygame.display.flip()

    elif tetris.state == "main":
        tetris.game_over(highscores)
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
                    current.fall_speed = fall_speeds[tetris.level-1]
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
        restart = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT: 
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if home_rect.collidepoint(mouse):
                    pygame.mixer.music.load("Tetris_muziek.mp3")
                    pygame.mixer.music.play(-1)
                    tetris = Tetris()
                    tetris.state = "menu"
                    restart = True
                if replay_rect.collidepoint(mouse):
                    pygame.mixer.music.load("Tetris_muziek.mp3")
                    pygame.mixer.music.play(-1)
                    tetris = Tetris()
                    tetris.level = tetris.start_level
                    tetris.random_tetriminos() 
                    tetris.current_shape = tetris.tetriminos[0]
                    tetris.state = "main"
                    restart = True
        if not restart:
            screen.fill(DARK_GREY)

            tetris.print_text()
            tetris.next_queue(True)
            tetris.draw_hold_cell(True)
            pygame.draw.rect(screen, BLACK, rect_grid)
            tetris.draw_grid(tetris.grid)
            
            pygame.draw.rect(screen, BLACK, game_over_rect)
            pygame.draw.rect(screen, WHITE, game_over_rect, 1)
        
            game_over_text = font1.render("GAME OVER", True, WHITE)
            screen.blit(game_over_text, (width_screen//2 - game_over_text.get_width()//2, heigth_screen//2 - 60))
            score = font1.render(f"SCORE: {int(tetris.score)} ", True, WHITE)
            screen.blit(score, (width_screen//2 - score.get_width()//2, heigth_screen//2 - 30))

            draw_button(home_rect, "", font1, GREY, LIGHTER_GREY, mouse)
            screen.blit(home_button, (home_rect.x + 5, home_rect.y + 5))

            draw_button(replay_rect, "", font1, DARK_GREEN, LIGHTER_DARK_GREEN, mouse)
            screen.blit(replay_button, (replay_rect.x + 5, replay_rect.y + 5))

            clock.tick(fps)
            pygame.display.flip()

    elif tetris.state == "highscore":
        for event in pygame.event.get():
            if event.type == pygame.QUIT: 
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    tetris.naam = tetris.naam[:-1]
                elif len(tetris.naam) < 3:
                    if event.unicode.isalpha():
                        tetris.naam += event.unicode
            if event.type == pygame.MOUSEBUTTONDOWN:    
                if ok_rect.collidepoint(mouse):
                    tetris.state = "initials entered"
                    highscores.update_highscores(tetris)

        screen.fill(DARK_GREY)

        tetris.print_text()
        tetris.next_queue(True)
        tetris.draw_hold_cell(True)
        pygame.draw.rect(screen, BLACK, rect_grid)
        tetris.draw_grid(tetris.grid)
        
        pygame.draw.rect(screen, BLACK, new_highscore_rect)
        pygame.draw.rect(screen, WHITE, new_highscore_rect, 1)
        draw_button(ok_rect, "OK", font1, GREY, LIGHTER_GREY, mouse)
        
        new_highscore_text = font1.render("NEW HIGHSCORE!", True, WHITE)
        screen.blit(new_highscore_text, (width_screen//2 - new_highscore_text.get_width()//2, heigth_screen//2 - 110))
        score = font1.render(f"SCORE: {int(tetris.score)} ", True, WHITE)
        screen.blit(score, (width_screen//2 - score.get_width()//2, heigth_screen//2 - 80))
        enter_initials_text = font2.render("ENTER YOUR INITIALS:", True, WHITE)
        screen.blit(enter_initials_text, ((width_screen//2 - enter_initials_text.get_width()//2, heigth_screen//2 - 40)))

        pygame.draw.rect(screen, BLACK, initials_rect)
        pygame.draw.rect(screen, GREY, initials_rect, 2)

        naam_text = font1.render(f"{tetris.naam.upper()}", True, WHITE)
        screen.blit(naam_text, (initials_rect.centerx - naam_text.get_width()//2, initials_rect.centery - naam_text.get_height()//2))

        clock.tick(fps)
        pygame.display.flip()

    elif tetris.state == "initials entered":
        restart = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT: 
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if home_rect.collidepoint(mouse):
                    pygame.mixer.music.load("Tetris_muziek.mp3")
                    pygame.mixer.music.play(-1)
                    tetris = Tetris()
                    tetris.state = "menu"
                    restart = True
                if replay_rect.collidepoint(mouse):
                    pygame.mixer.music.load("Tetris_muziek.mp3")
                    pygame.mixer.music.play(-1)
                    tetris = Tetris()
                    tetris.level = tetris.start_level
                    tetris.random_tetriminos() 
                    tetris.current_shape = tetris.tetriminos[0]
                    tetris.state = "main"
                    restart = True

        if not restart:
            screen.fill(DARK_GREY)

            tetris.print_text()
            tetris.next_queue(True)
            tetris.draw_hold_cell(True)
            pygame.draw.rect(screen, BLACK, rect_grid)
            tetris.draw_grid(tetris.grid)

            draw_button(home_rect, "", font1, GREY, LIGHTER_GREY, mouse)
            screen.blit(home_button, (home_rect.x + 5, home_rect.y + 5))

            draw_button(replay_rect, "", font1, DARK_GREEN, LIGHTER_DARK_GREEN, mouse)
            screen.blit(replay_button, (replay_rect.x + 5, replay_rect.y + 5))

            clock.tick(fps)
            pygame.display.flip()