import random, sqlite3
from variables import *
from shapes import shapes

class Tetris():
    def __init__(self):
        self.level = 1
        self.level_check = 1
        self.level_i = 0
        self.start_level = self.level
        self.tetriminos = [] # Dit is de soort van bag
        self.current_shape = []
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
        self.state = "menu"
        self.mute = ["sound_on", "mute"]
        self.mute_i = 0
        self.naam = ""

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
        
        # maakt een copy van de grid die leeg blijft
        self.empty_grid = [row.copy() for row in self.grid]

    def draw_grid(self, grid):
        # Maakt de grid door, door het hele bord in rijen te gaan met stapsgrootte = grid_size
        for row_index, row in enumerate(grid[2:]):
            for col_index, cell in enumerate(row):
                rect = pygame.Rect(col_index *grid_size + x_grid , (row_index) *grid_size + y_grid, grid_size, grid_size)
                if cell != 0:
                    pygame.draw.rect(screen, grid[row_index+2][col_index], rect)
                pygame.draw.rect(screen, GREY, rect, 1)

    def check_full_rows(self):
        for row_id in range(2, 22):
            if all(self.grid[row_id]):
                self.rows_to_clear.append(row_id)
                self.grid[row_id] = [WHITE, WHITE, WHITE, WHITE, WHITE, WHITE, WHITE, WHITE, WHITE, WHITE]
                self.level_i += 1
                self.calculate_level()
        if self.rows_to_clear:
            self.clearing = True
            self.cleared_rows = len(self.rows_to_clear)
            self.total_rows_cleared += len(self.rows_to_clear)
            self.calculate_score()
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

    def game_over(self, database):
        for i in range(2):
            for cell in self.grid[i]:
                if cell != 0:
                    self.sound_game_over_play()
                    new_highscore = database.check_new_highscore(self)
                    if new_highscore:
                        self.state = "highscore"
                    else:
                        self.state = "game over"

    def sound_game_over_play(self):
            sound_game_over.play()
            pygame.mixer.music.load('Tetris_ending.mp3')
            pygame.mixer.music.play(-1)
    
    def calculate_score(self):
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
        if self.level_i // 10 == 1:
            self.level += 1
            self.level_i = 0

        self.level = min(30, self.level)

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

        # rendered de text: "SCORE" en laat het op de juiste plek zien met blit
        score_text = font1.render("SCORE", True, WHITE)
        screen.blit(score_text, (x_text - score_text.get_width() // 2, y_text))
        score = font1.render(f"{int(self.score)}", True, WHITE)
        screen.blit(score, (x_text - score.get_width() // 2, y_text + grid_size))

        level_text = font1.render("LEVEL", True, WHITE)
        screen.blit(level_text, (x_text - level_text.get_width() // 2, y_text + 2 * grid_size + spacing))
        level = font1.render(f"{self.level}", True, WHITE)
        screen.blit(level, (x_text - level.get_width() // 2, y_text + 3 * grid_size + spacing))

        lines_text = font1.render("LINES", True, WHITE)
        screen.blit(lines_text, (x_text - lines_text.get_width() // 2, y_text + 4 * grid_size + 2 * spacing))
        lines = font1.render(f"{self.total_rows_cleared}", True, WHITE)
        screen.blit(lines, (x_text - lines.get_width() // 2, y_text + 5 * grid_size + 2 * spacing))

        #vierkant om de tekst heen
        rect = pygame.Rect(x_text - 2.5 * grid_size, y_text - spacing, 5 * grid_size, 215)
        pygame.draw.rect(screen, GREY, rect, 2)

    def next_queue(self, filled):
        next_text = font1.render("NEXT", True, WHITE)
        screen.blit(next_text, ((x_grid + width_grid + width_screen) // 2 - next_text.get_width()//2, 2 * grid_size))

        rect = pygame.Rect((x_grid + width_grid + width_screen) // 2 - 2.5 * grid_size, 2 * grid_size - space, 5 * grid_size, 9*grid_size + next_text.get_height() + 3 * space)
        pygame.draw.rect(screen, GREY, rect, 2)

        if filled:
            for i in range(3):
                piece = self.tetriminos[i + 1]
                shape = piece.shape[0]
                shape_width = (piece.max_x - piece.min_x + 1) * grid_size
                start_x = x_grid + width_screen // 2 + (next_text.get_width() - shape_width) // 2
                base_y = heigth_screen // 2 - height_grid // 2 + 3 * grid_size
                for y, row in enumerate(shape):
                    for x, cube in enumerate(row):
                        if cube == 1:
                            next_x = start_x + (x - piece.min_x) * grid_size
                            next_y = base_y + 3 * i * grid_size + y * grid_size
                            block_rect = pygame.Rect(next_x, next_y, grid_size, grid_size)
                            pygame.draw.rect(screen, piece.color, block_rect)
                            pygame.draw.rect(screen, GREY, block_rect, 1)
        

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
            
    def draw_hold_cell(self, filled):
        # tekent het woord "HOLD (C)" boven de hold cell
        hcell_text = font1.render("HOLD (C)", True, WHITE)
        screen.blit(hcell_text, (x_grid // 2 - hcell_text.get_width() // 2, 2 * grid_size))

        rect = pygame.Rect(x_grid // 2 - 2.5 * grid_size, 2* grid_size - 10, 5 * grid_size, 3*grid_size + hcell_text.get_height() + 20)
        pygame.draw.rect(screen, GREY, rect, 2)

        if filled:
            if self.hold_shape:
                hold_piece = self.hold_shape[0]
                shape_matrix = hold_piece.shape[0]
                shape_width = (hold_piece.max_x - hold_piece.min_x + 1) * grid_size
                start_x = x_grid // 2 - shape_width // 2  # links uitlijnen vanaf center
                base_y = hcell_text.get_height() + 2 * grid_size + 20

                for y, row in enumerate(shape_matrix):
                    for x, cube in enumerate(row):
                        if cube == 1:
                            hold_x = start_x + (x - hold_piece.min_x) * grid_size
                            hold_y = base_y + y * grid_size
                            block_rect = pygame.Rect(hold_x, hold_y, grid_size, grid_size)
                            pygame.draw.rect(screen, hold_piece.color, block_rect)
                            pygame.draw.rect(screen, GREY, block_rect, 1)

class Tetrimino():
    def __init__(self, shape, color, level):
        self.x = x_grid + 3 * grid_size # plaatst het blok in het midden
        self.y = -(2*grid_size) + y_grid # plaatst de tetrimino 2 blokjes boven de grid
        self.ghost_y = self.y # zet de start van de ghost_y op de 

        # maakt de kleur en shape de meegegeven variabelen
        self.color = color
        self.shape = shape

        self.rotation = 0 # de start rotatie is 0

        self.bounds() # bepaalt de min_x, max_x en max_y om daarmee de breedte van het blok te bepalen

        self.fall_time = 0
        self.fall_speed = fall_speeds[level-1] # pakt de snelheid uit het tabel op basis van het level
        self.movement_time = 0.20
        self.movement_delay_not_moving = 0.25
        self.movement_delay_moving = 0.05
        self.lock_delay = max(0.1, 0.3 - (level - 1) * 0.01)
        self.moving = False
        self.is_locking = False

        self.start_y = 0
        self.end_y = 0

        self.distance = 0

    def bounds(self):
        self.min_x = 4
        self.max_x = 0
        self.max_y = 0
        for y, row in enumerate(self.shape[self.rotation]):
            for x, cube in enumerate(row):
                    if cube == 1:
                        self.min_x = min(self.min_x, x)
                        self.max_x = max(self.max_x, x)
                        self.max_y = max(self.max_y, y)

    def draw(self):
        # loopt door de rij en colom van de shape van de tetrimino
        for y, row in enumerate(self.shape[self.rotation]):
            for x, cube in enumerate(row):
                # alleen als de cel binnen de grid zit moet hij worden laten zien
                if self.y + y * grid_size >= y_grid:
                    if cube == 1:
                        if self.is_locking:
                            # kijkt of de fall_time even of oneven is
                            # even = blok is zichtbaar
                            # oneven = blok is onzichtbaar
                            visible = int(self.fall_time * 15) % 2 == 0
                            color = self.color if visible else WHITE
                        else:
                            color = self.color

                        rect = pygame.Rect(self.x + x * grid_size, self.y + y *grid_size, grid_size, grid_size)
                        pygame.draw.rect(screen, color, rect)
        
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
                self.is_locking = True
                if self.fall_time >= self.fall_speed + self.lock_delay:
                    self.is_locking = False
                    for y in range(0, 4):
                        for x in range(0, 4):
                            if ((self.shape[self.rotation])[y])[x] == 1:
                                tetris.grid[((self.y - y_grid) // grid_size) + y + 2][(self.x - x_grid) // grid_size + x] = self.color
                    self.fall_time = 0
                    tetris.check_full_rows()
                return
            self.is_locking = False
            self.y += grid_size
            self.fall_time = 0

            if arrow_down:
                tetris.score += 1 * tetris.level
                # soft drop score

    def move_horizontal(self, tetris):
        self.movement_time += delta_time
        keys_pressed = pygame.key.get_pressed()
        if self.moving:
            delay = self.movement_delay_moving
        else:
            delay = self.movement_delay_not_moving
        
        if keys_pressed[pygame.K_RIGHT] or keys_pressed[pygame.K_LEFT]:
            if self.movement_time >= delay:
                if keys_pressed[pygame.K_RIGHT]:
                    if not self.check_grid(tetris, self.y, 1, 0, 0):
                        self.x += grid_size
                        self.movement_time = 0
                        self.moving = True
                elif keys_pressed[pygame.K_LEFT]:
                    if not self.check_grid(tetris, self.y, -1, 0, 0):
                        self.x -= grid_size
                        self.movement_time = 0
                        self.moving = True
                else:
                    self.moving = False
                    self.movement_time = self.movement_delay_not_moving
    
    def rotate(self, tetris, rotation):
        for x in range(0, 4):
            for y in range(0, 4):
                if self.shape[(self.rotation+rotation) % len(self.shape)][y][x] == 1:
                    if self.check_grid(tetris, self.y, 0, 0, 1):
                        return
        self.rotation = (self.rotation + rotation) % len(self.shape)
        self.bounds()
    
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
    
class Highscores():
    def __init__(self):
        self.db = sqlite3.connect("High_scores.s3db")
        # maakt het tabel als hij nog niet bestaat
        self.db.execute("CREATE TABLE IF NOT EXISTS highscores (`id` INTEGER PRIMARY KEY, name TEXT, score INT)")
        count = self.db.execute("SELECT COUNT(*) FROM highscores").fetchone()[0]

        # als er niks in de database zit stopt hij de standaard waardes erin
        if count == 0:
            scores = [5000, 4000, 3000, 2000, 1000]
            for score in scores:
                self.db.execute("INSERT INTO highscores (name, score) VALUES (?, ?)", ["", score])
            self.db.commit()
    
    def check_new_highscore(self, tetris):
        cursor = self.db.execute("SELECT score FROM highscores")
        scores = cursor.fetchall()
        # loopt door alle scores om te kijken of de gehaalde score hoger is dan één van de huidige highscores,
        # zo ja returned True en zo nee dan returned hij False
        for score in [row[0] for row in scores]:
            if tetris.score > score:
                return True
        return False
    
    def update_highscores(self, tetris):
        # voegt de huidige score toe aan de database
        self.db.execute("INSERT INTO highscores (name, score) VALUES (?, ?)", [tetris.naam, tetris.score])
        # haalt de 5 laagste scores uit de database
        self.db.execute("DELETE FROM highscores WHERE id not in (SELECT id FROM highscores ORDER BY score DESC LIMIT 5)")
        self.db.commit()

    def get_highscores(self):
        # vraagt de highscores op uit de database en returned ze in een lijst met tuples
        highscores = self.db.execute("SELECT name, score FROM highscores ORDER BY score DESC").fetchall()
        return highscores
    
    def reset_database(self):
        # verwijdert alles van de database
        self.db.execute("DELETE FROM highscores")

        # stopt daarna weer de standaard waardes is de database
        scores = [5000, 4000, 3000, 2000, 1000] # standaard waardes
        for score in scores:
                self.db.execute("INSERT INTO highscores (name, score) VALUES (?, ?)", ["", score]) # stopt een lege str en score in de database
        self.db.commit()