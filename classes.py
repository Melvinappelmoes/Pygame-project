import random
from variables import *
from shapes import shapes

class Tetris():
    def __init__(self):
        self.level = 1
        self.level_check = 1
        self.tetriminos = [] # Dit is de soort van bag
        self.random_tetriminos() 
        self.current_shape = self.tetriminos[0]
        self.hold_shape = []
        self.hold_available = True
        self.score = 0
        self.grid = []
        self.make_grid()
        self.rows_to_clear = []
        self.clearing = False
        self.clear_timer = 0
        self.clear_delay = 0.1
        self.spawn_ready = False
        self.cleared_rows = 0
        self.total_rows_cleared = 0
        self.back_to_back = False
        self.back_true = 0


    def random_tetriminos(self):
        temp_shapes = shapes
        random.shuffle(temp_shapes)
        for shape_and_color in temp_shapes:
            shape, color = shape_and_color
            self.tetriminos.append(Tetrimino(shape, color, self.level))

    def make_grid(self):
        for y in range(0, (height_grid+2*grid_size) // grid_size):
            self.grid.append([])
            for x in range(0, width_grid // grid_size):
                self.grid[y].append(0)

    def draw_grid(self):
        # Maakt de grid door, door het hele bord in rijen te gaan met stapsgrootte = grid_size
        for row_index, row in enumerate(self.grid[2:]):
            for col_index, cell in enumerate(row):
                rect = pygame.Rect(col_index *grid_size + x_grid , (row_index) *grid_size + y_grid, grid_size, grid_size)
                if cell != 0:
                    pygame.draw.rect(screen, self.grid[row_index+2][col_index], rect)
                pygame.draw.rect(screen, GREY, rect, 1)

    def check_full_rows(self):
        for row_id in range(2, 22):
            if all(self.grid[row_id]):
                self.rows_to_clear.append(row_id)
                self.grid[row_id] = [WHITE, WHITE, WHITE, WHITE, WHITE, WHITE, WHITE, WHITE, WHITE, WHITE]

        if self.rows_to_clear:
            self.clearing = True
            self.cleared_rows = len(self.rows_to_clear)
            self.total_rows_cleared += len(self.rows_to_clear)
            self.calculate_score(self.current_shape)
        else:
            self.spawn_ready = True


    def clear_rows(self):
        self.clear_timer += delta_time
        if self.clear_timer < self.clear_delay:
            return
        
        self.grid.pop(self.rows_to_clear[0])
        self.rows_to_clear.pop(0)
        self.grid.insert(1, [0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
        self.clear_timer = 0

        if not self.rows_to_clear:
            self.clearing = False      
            self.spawn_ready = True

    def spawn_block(self):
        self.tetriminos.pop(0)
        self.current_shape = self.tetriminos[0]
        if len(self.tetriminos) < 5:
            self.random_tetriminos()
        self.current_shape.x = x_grid + 3 * grid_size
        self.current_shape.y = -(2*grid_size) + y_grid

    def game_over(self):
        for cell in self.grid[0]:
            if cell != 0:
                self.sound_game_over_play()
                return False, True

        for cell in self.grid[1]:
            if cell != 0:
                self.sound_game_over_play()
                return False, True
        return True, False
    
    def sound_game_over_play(self):
            sound_game_over.play()
            pygame.mixer.music.load('Tetris_ending.mp3')
            pygame.mixer.music.play(-1)

    def pause(self):
        # ff kijken hoe we een pauze menu kunnen maken
        # blijft in de loop totdat er weer op esc geklikt wordt, daarna gaat het spel verder
        paused = True
        while paused:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        paused = False
                        return True
    
    def calculate_score(self, tetrimino):

        # checkt hoeveel rijen er weggehaald zijn
        # als er een tetris is gehaald (4 rijen weg) dan moet de volgende tetris *1.5
        row_score = 0

        score_back = {1:(100, False), 2:(300, False), 3:(500, False), 4:(800, True)}

        row_score = score_back[self.cleared_rows][0]
        self.back_to_back = score_back[self.cleared_rows][1]

        # als er een back to back is dan gaat de score * 1.5 en level en anders alleen de level
        
        if self.back_to_back:
            self.back_true += 1
            if self.back_true == 2:
                self.score += row_score * 1.5 * self.level
                self.back_true = 1
            else:
                self.score += row_score * self.level

        else: 
            self.score += row_score * self.level
            self.back_true = 0

        self.cleared_rows = 0

    def calculate_level(self):
        # doet 1 level per 10 rows cleared
        self.level = 1 + self.total_rows_cleared // 10

        if self.level_check != self.level:
            sound_stage_clear.play()
        self.level_check = self.level

    def print_text(self):
        # de x van de tekst is tussen de grid en rand van scherm in
        x_text = x_grid // 2
        # de y van de tekst is 3 * grid_size onder het midden van de grid
        y_text =  height_grid // 2 + 3 * grid_size
        # bepaalt hoeveel ruimte er tussen de variabelen inzit
        spacing = 10

        # miss om een vierkant om de tekst heen te stoppen
        rect = pygame.Rect(x_text - 2 * grid_size, y_text - spacing, 4 * grid_size, 220)
        pygame.draw.rect(screen, WHITE, rect, 1)

        # rendered de text: "SCORE" en laat het op de juiste plek zien met blit
        score_text = font.render("SCORE", True, WHITE)
        screen.blit(score_text, (x_text - score_text.get_width() // 2, y_text))
        score = font.render(f"{int(self.score)}", True, WHITE)
        screen.blit(score, (x_text - score.get_width() // 2, y_text + grid_size))

        level_text = font.render("LEVEL", True, WHITE)
        screen.blit(level_text, (x_text - level_text.get_width() // 2, y_text + 2 * grid_size + spacing))
        level = font.render(f"{self.level}", True, WHITE)
        screen.blit(level, (x_text - level.get_width() // 2, y_text + 3 * grid_size + spacing))

        lines_text = font.render("LINES", True, WHITE)
        screen.blit(lines_text, (x_text - lines_text.get_width() // 2, y_text + 4 * grid_size + 2 * spacing))
        lines = font.render(f"{self.total_rows_cleared}", True, WHITE)
        screen.blit(lines, (x_text - lines.get_width() // 2, y_text + 5 * grid_size + 2 * spacing))

    def next_queue(self):
        for i in range(0, 3):
            for y, row in enumerate(self.tetriminos[i+1].shape[0]):
                for x, cube in enumerate(row):
                    if cube == 1:
                        # tekent de volgende 3 blokken naast de grid door door de tetriminos lijst heen te lopen
                        next_x = width_screen // 2 + width_grid // 2 + x * grid_size + 2 * grid_size
                        next_y = heigth_screen // 2 - height_grid// 2 + y * grid_size + 3 * i * grid_size + 3 * grid_size
                        rect = pygame.Rect(next_x, next_y, grid_size, grid_size)
                        pygame.draw.rect(screen, self.tetriminos[i+1].color, rect)
                        pygame.draw.rect(screen, GREY, rect, 1)

        # tekent het woord "NEXT" boven de tetriminos
        next_text = font.render("NEXT", True, WHITE)
        screen.blit(next_text, (x_grid + width_screen // 2, 2 * grid_size))      



    def hold_cell(self):
        if self.hold_available:
            self.hold_shape.append(self.current_shape)
            
            if len(self.hold_shape) == 1:
                self.tetriminos.pop(0)
                self.current_shape = self.tetriminos[0]
                self.current_shape.x = x_grid + 3 * grid_size
                self.current_shape.y = -(2*grid_size) + y_grid

            elif len(self.hold_shape) >= 2:
                self.tetriminos.pop(0)
                self.current_shape = self.hold_shape[0]
                self.hold_shape.pop(0)
                self.current_shape.x = x_grid + 3 * grid_size
                self.current_shape.y = -(2*grid_size) + y_grid
            
            
    def draw_hold_cell(self):
        # tekent het woord "HOLD (C)" boven de hold cell
        hcell_text = font.render("HOLD (C)", True, WHITE)
        screen.blit(hcell_text, (x_grid // 2 - hcell_text.get_width() // 2, 2 * grid_size))

        if self.hold_shape:
            for y, row in enumerate(self.hold_shape[0].shape[0]):
                for x, cube in enumerate(row):
                    if cube == 1:
        
                        hold_x = (x_grid // 2) - (hcell_text.get_width() // 2) + (x * grid_size)
                        hold_y = (4 * grid_size) + (y * grid_size)
                        rect = pygame.Rect(hold_x, hold_y, grid_size, grid_size)
                        pygame.draw.rect(screen, self.hold_shape[0].color, rect)
                        pygame.draw.rect(screen, GREY, rect, 1)


class Tetrimino():
    def __init__(self, shape, color, level):
        self.x = x_grid + 3 * grid_size
        self.max_x = 0
        self.min_x = 4
        # plaatst de tetrimino 2 blokjes boven de grid
        self.y = -(2*grid_size) + y_grid
        self.max_y = 0

        self.ghost_y = self.y

        self.color = color
        self.shape = shape
        self.rotation = 0

        self.fall_time = 0
        # formule om de val snelheid te berekenen
        self.fall_speed = (0.8 - ((level - 1) * 0.007))**(level-1)
        self.movement_time = 0
        self.movement_delay = 0.1

        self.start_y = 0
        self.end_y = 0

        self.distance = 0

    def draw(self):
        # loopt door de rij en colom van de shape van de tetrimino
        for y, row in enumerate(self.shape[self.rotation]):
            for x, cube in enumerate(row):
                # alleen als de cel binnen de grid zit moet hij worden laten zien
                if self.y + y * grid_size >= y_grid:
                    if cube == 1:
                        self.min_x = min(self.min_x, x)
                        self.max_x = max(self.max_x, x)
                        self.max_y = max(self.max_y, y)
                        rect = pygame.Rect(self.x + x * grid_size, self.y + y *grid_size, grid_size, grid_size)
                        pygame.draw.rect(screen, self.color, rect)
        

    def move_down(self, tetris, spatie, arrow_down):
        self.start_y = self.y
        self.fall_time += delta_time
        if spatie:
            while not self.check_grid(tetris, self.y, 0, 1, 0):
                self.y += grid_size

            for y in range(0, 4):
                for x in range(0, 4):
                    if ((self.shape[self.rotation])[y])[x] == 1:
                        tetris.grid[((self.y - y_grid) // grid_size) + y + 2][((self.x - x_grid) // grid_size)+ x] = self.color

            self.end_y = self.y
            self.fall_time = 0
            tetris.check_full_rows()
            self.distance = self.distance_traveled()
            tetris.score += self.distance * 2 * tetris.level
            self.distance = 0
            return

        elif self.fall_time >= self.fall_speed:
            if self.y - y_grid + (self.max_y+1) * grid_size >= height_grid or self.check_grid(tetris, self.y, 0, 1, 0):
                for y in range(0, 4):
                    for x in range(0, 4):
                        if ((self.shape[self.rotation])[y])[x] == 1:
                            tetris.grid[((self.y - y_grid) // grid_size) + y + 2][(self.x - x_grid) // grid_size + x] = self.color
                self.fall_time = 0
                tetris.check_full_rows()
                return
            self.y += grid_size
            self.fall_time = 0

            if arrow_down:
                tetris.score += 1 * tetris.level
                # soft drop score

    def move_horizontal(self, tetris):
        self.movement_time += delta_time
        if self.movement_time >= self.movement_delay:
            keys_pressed = pygame.key.get_pressed()
            if keys_pressed[pygame.K_RIGHT]:
                if self.check_grid(tetris, self.y, 1, 0, 0):
                    pass
                else:
                    self.x += grid_size
                    self.movement_time = 0
            if keys_pressed[pygame.K_LEFT]:
                if self.check_grid(tetris, self.y, -1, 0, 0):
                    pass
                else:
                    self.x -= grid_size
                    self.movement_time = 0
    
    def rotate(self, tetris, rotation):
        for x in range(0, 4):
            for y in range(0, 4):
                if self.shape[(self.rotation+rotation) % len(self.shape)][y][x] == 1:
                    if self.check_grid(tetris, self.y, 0, 0, 1):
                        return
        self.rotation = (self.rotation + rotation) % len(self.shape)
        self.min_x, self.max_x, self.max_y = 4,0,0
    
    def check_grid(self, tetris, huidige_y, left_or_right, down, rotation):
        # Gaat door alle cellen van de tetromino stuk
        for x in range(0, 4):
            for y in range(0, 4):
                # maakt een x en y waarmee gecheckt wordt of de tetrimino buiten de grid gaat
                new_x = ((self.x - x_grid) // grid_size) + x + left_or_right
                new_y = ((huidige_y - y_grid) // grid_size) + y + 2 + down
                if self.shape[(self.rotation+rotation) % len(self.shape)][y][x] == 1:
                    if new_x * grid_size + grid_size > width_grid or new_x * grid_size < 0 or new_y >= 22 or tetris.grid[new_y][new_x] != 0:
                            return True
        return False
    
    def ghost_piece(self, tetris):
        self.ghost_y = self.y
        while not self.check_grid(tetris, self.ghost_y, 0, 1, 0):
                self.ghost_y += grid_size

        for y, row in enumerate(self.shape[self.rotation]):
            for x, cube in enumerate(row):
                if self.ghost_y + y * grid_size >= y_grid:
                    if cube == 1:
                        rect = pygame.Rect(self.x + x * grid_size, self.ghost_y + y *grid_size, grid_size, grid_size)
                        pygame.draw.rect(screen, self.color, rect, width_ghost)

    def distance_traveled(self):
        return (self.end_y - self.start_y) // grid_size