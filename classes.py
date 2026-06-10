import random, sqlite3
from variables import *
from shapes import shapes

class Tetris():
    def __init__(self):
        self.level = 1                      # het level dat je bent tijdens het spel
        self.level_check = 1                # is nodig om te checken of je level omhoog bent
        self.level_i = 0                    # gaat omhoog per row_cleared, zodat je level omhoog gaat als je 10 rijen hebt gecleared
        self.start_level = self.level       # voor als je met een ander level begint
        self.score = 0                      # de score die je hebt

        self.tetriminos = []                # Dit is de soort van bag
        self.current_shape = []             # Dit is de huidige blok

        self.hold_shape = []                # hier zit het blok die je vasthoudt
        self.hold_available = True          # of hold available is, je kan maar 1 keer hold doen per 'ronde'

        self.grid = []                      # dit maakt de lijst van de grid
        self.make_grid()                    # dit maakt de grid

        self.rows_to_clear = []             # een lijst die rijen bevat die gecleared moeten worden
        self.clearing = False               # een soort state die True is als hij bezig is met clearen
        self.clear_timer = 0                # zorgt ervoor dat het niet in één keer alle rijen weg haalt
        self.clear_delay = 0.1              # hoelang ertussen zit tussen rijen weghalen
        self.cleared_rows = 0               # variabele om bij te houden hoeveel rijen er gecleared zijn per 'ronde'
        self.total_rows_cleared = 0         # het aantal rijen die gecleared zijn, zodat je er bij 10 een nieuw level kan krijgen
        self.back_to_back = False           # of je tetris hebt
        self.back_true = 0                  # hoevaak je tetris hebt
        self.spawn_ready = False            # zegt of er een nieuw blok mag spawnen

        self.state = "menu"                 # zet de state op het begin op menu
        self.mute = ["sound_on", "mute"]    # welk plaatje het is
        self.mute_i = 0                     # hoeveelste in de mute lijst ^^
        self.naam = ""                      # de naam die je invult bij een highscore

    def random_tetriminos(self):
        # shuffled de shapes
        temp_shapes = shapes
        random.shuffle(temp_shapes)

        # voegt de shapes toe in de tetriminos-lijst
        for shape_and_color in temp_shapes:
            shape, color = shape_and_color
            self.tetriminos.append(Tetrimino(shape, color, self.level)) # elk blok heeft zijn eigen vorm en kleur, het level wordt meegegeven voor de valsnelheid

    def make_grid(self):
        # maakt een lijst met het grid, begint met de bovenste rij, dan naar beneden
        for y in range(0, (height_grid+2*grid_size) // grid_size):
            self.grid.append([])
            for x in range(0, width_grid // grid_size):
                self.grid[y].append(0)

        # maakt een copy van de grid die leeg blijft
        self.empty_grid = [row.copy() for row in self.grid]

    def draw_grid(self, grid):
        # maakt de grid door, door het hele bord in rijen te gaan met stapsgrootte = grid_size
        for row_index, row in enumerate(grid[2:]): # loopt door de rijen van het grid, behalve de bovenste twee
            for col_index, cell in enumerate(row): # loopt door de kolommen van het grid
                rect = pygame.Rect(col_index *grid_size + x_grid , (row_index) *grid_size + y_grid, grid_size, grid_size)
                if cell != 0:
                    pygame.draw.rect(screen, grid[row_index+2][col_index], rect) # tekent het blokje
                pygame.draw.rect(screen, GREY, rect, 1) # tekent border

    def check_full_rows(self):
        for row_id in range(2, 22):
            # als een rij vol is met blokken, wordt die wit en wordt er gekeken of je een level omhoog gaat
            if all(self.grid[row_id]):
                self.rows_to_clear.append(row_id)
                self.grid[row_id] = [WHITE, WHITE, WHITE, WHITE, WHITE, WHITE, WHITE, WHITE, WHITE, WHITE]
                self.level_i += 1
                self.calculate_level()

        # als hij rijen moet gaan clearen, gaat hij rows clearen
        if self.rows_to_clear:
            self.clearing = True
            self.cleared_rows = len(self.rows_to_clear)
            self.total_rows_cleared += len(self.rows_to_clear)
            self.calculate_score()

        # als niet rows clearen, mag een nieuw blok spawnen
        else:
            self.spawn_ready = True

    def clear_rows(self):
        # zorgt ervoor dat het niet in één keer alle rijen cleared
        self.clear_timer += delta_time
        if self.clear_timer < self.clear_delay:
            return
        
        # haalt de rijen eruit en voegt een nieuwe toe
        self.grid.pop(self.rows_to_clear[0])
        self.rows_to_clear.pop(0)
        self.grid.insert(1, [0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
        self.clear_timer = 0

        # als geen rijen meer te clearen, mag hij weer blok spawnen
        if not self.rows_to_clear:
            self.clearing = False      
            self.spawn_ready = True

    def spawn_block(self):
        # haalt de eerste shape uit de lijst en maakt de current shape de nieuwe eerste in de lijst
        self.tetriminos.pop(0)
        self.current_shape = self.tetriminos[0]

        # als de lengte van de lijst kleiner is dan 5, nieuwe shuffle doen
        if len(self.tetriminos) < 5:
            self.random_tetriminos()
        self.current_shape.x = x_grid + 3 * grid_size
        self.current_shape.y = -(2*grid_size) + y_grid

    def game_over(self, database):
        # checkt of er een blok in de bovenste twee rijen zit (niet zichtbaar op het scherm)
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
        # speelt het eindmuziekje
        sound_game_over.play()
        pygame.mixer.music.load('Tetris_ending.mp3')
        pygame.mixer.music.play(-1) # speelt in een loop
    
    def calculate_score(self):
        # checkt hoeveel rijen er weggehaald zijn
        # als er een tetris is gehaald (4 rijen weg) dan moet de volgende tetris *1.5
        score_back = {1:(100, False), 2:(300, False), 3:(500, False), 4:(800, True)}

        row_score = score_back[self.cleared_rows][0] # geeft de score bij het aantal rijen gecleared
        self.back_to_back = score_back[self.cleared_rows][1] # bij tetris is deze True

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

        # je kan niet boven level 30 komen
        self.level = min(30, self.level)

        # als je een ander level hebt dan eerst (als je level up bent) geluidje spelen
        if self.level_check != self.level:
            sound_stage_clear.play()
        self.level_check = self.level

    def print_text(self):
        # de x van de tekst is tussen de grid en rand van scherm in
        x_text = x_grid // 2
        # de y van de tekst is 3 * grid_size onder het midden van de grid
        y_text = height_grid // 2 + 3 * grid_size
        # bepaalt hoeveel ruimte er tussen de variabelen inzit
        spacing = 10

        score_text = font1.render("SCORE", True, WHITE) # rendered de tekst: "SCORE" en laat het op de juiste plek zien met blit
        screen.blit(score_text, (x_text - score_text.get_width() // 2, y_text))
        score = font1.render(f"{int(self.score)}", True, WHITE) # rendered de score en laat onder "SCORE" zien
        screen.blit(score, (x_text - score.get_width() // 2, y_text + grid_size))

        level_text = font1.render("LEVEL", True, WHITE) # rendered de tekst: "LEVEL" en laat het op de juiste plek zien met blit
        screen.blit(level_text, (x_text - level_text.get_width() // 2, y_text + 2 * grid_size + space))
        level = font1.render(f"{self.level}", True, WHITE) # rendered het level en laat onder "LEVEL" zien
        screen.blit(level, (x_text - level.get_width() // 2, y_text + 3 * grid_size + space))

        lines_text = font1.render("LINES", True, WHITE) # rendered de tekst: "LINES" en laat het op de juiste plek zien met blit
        screen.blit(lines_text, (x_text - lines_text.get_width() // 2, y_text + 4 * grid_size + 2 * space))
        lines = font1.render(f"{self.total_rows_cleared}", True, WHITE) # rendered het aantal rijen gecleared en laat onder "LINES" zien
        screen.blit(lines, (x_text - lines.get_width() // 2, y_text + 5 * grid_size + 2 * space))

        # vierkant om de tekst heen
        rect = pygame.Rect(x_text - 2.5 * grid_size, y_text - space, 5 * grid_size, 215)
        pygame.draw.rect(screen, GREY, rect, 2)

    def next_queue(self, filled):
        next_text = font1.render("NEXT", True, WHITE) # rendered de tekst: "NEXT" en laat het op de juiste plek zien met blit
        screen.blit(next_text, ((x_grid + width_grid + width_screen) // 2 - next_text.get_width()//2, 2 * grid_size))

        # drawt de rect op de goede plek
        rect = pygame.Rect((x_grid + width_grid + width_screen) // 2 - 2.5 * grid_size, 2 * grid_size - space, 5 * grid_size, 9*grid_size + next_text.get_height() + 3 * space)
        pygame.draw.rect(screen, GREY, rect, 2)

        # doet het alleen als het gevuld is
        if filled:
            for i in range(3):
                # laat de drie volgende shapes zien onder "NEXT"
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
        # als je kan holden (en c hebt ingedrukt) gaat hij dit doen
        if self.hold_available:
            self.hold_shape.append(self.current_shape)
            
            # als de toegevoegde shape de eerste is wordt hij gewoon toegevoegd aan de hold
            if len(self.hold_shape) == 1:
                self.tetriminos.pop(0)
                self.current_shape = self.tetriminos[0]
                self.current_shape.x = x_grid + 3 * grid_size
                self.current_shape.y = -(2*grid_size) + y_grid

            # als de toegevoegde shape niet de eerste is moet hij eerst een andere shape eruit halen en die als current shape doen
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

        rect = pygame.Rect(x_grid // 2 - 2.5 * grid_size, 2 * grid_size - space, 5 * grid_size, 3*grid_size + hcell_text.get_height() + 2*space)
        pygame.draw.rect(screen, GREY, rect, 2)

        if filled:
            if self.hold_shape:
                hold_piece = self.hold_shape[0]
                shape_matrix = hold_piece.shape[0]
                shape_width = (hold_piece.max_x - hold_piece.min_x + 1) * grid_size
                start_x = x_grid // 2 - shape_width // 2  # links uitlijnen vanaf center
                base_y = hcell_text.get_height() + 2 * grid_size + 2*space

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
        self.x = x_grid + 3 * grid_size    # plaatst het blok in het midden
        self.y = -(2*grid_size) + y_grid    # plaatst de tetrimino 2 blokjes boven de grid
        self.ghost_y = self.y               # zet de start van de ghost_y op de startpositie

        # maakt de kleur en shape de meegegeven variabelen
        self.color = color
        self.shape = shape

        self.rotation = 0 # de start rotatie is 0

        self.bounds() # bepaalt de min_x, max_x en max_y om daarmee de breedte van het blok te bepalen

        self.fall_time = 0                                          # houdt bij hoe lang het blok valt
        self.fall_speed = fall_speeds[level-1]                      # pakt de snelheid uit het tabel op basis van het level
        self.movement_time = 0                                      # houdt bij hoe lang geleden het blok voor het laatst bewogen is
        self.movement_delay_not_moving = 0.2                        # de delay als hij daarvoor niet bewogen heeft
        self.movement_delay_moving = 0.05                           # de delay als hij daarvoor wel bewogen heeft
        self.lock_delay = max(0.1, 0.3 - (level - 1) * 0.01)        # zet de lock delay op basis van het level

        # standaard waardes, want op het begin is hij niet aan het bewegen en niet aan het vastzetten
        self.moving = False
        self.is_locking = False

        # maakt de start_y en end_y om de afgelegde afstand te berekenen
        self.start_y = 0
        self.end_y = 0
        self.distance = 0

    def bounds(self):
        # start waardes, begint bij de meest uiterlijke waarde
        self.min_x = 4
        self.max_x = 0
        self.max_y = 0

        # loopt door de vorm van het blok
        for y, row in enumerate(self.shape[self.rotation]):
            for x, cube in enumerate(row):
                # als er een blokje zit kijkt het of de huidige x en y kleiner of groter is dan de opgeslagen waarde
                if cube == 1:
                    self.min_x = min(self.min_x, x)
                    self.max_x = max(self.max_x, x)
                    self.max_y = max(self.max_y, y)

    def draw(self):
        # loopt door de rij en kolom van de shape van de tetrimino
        for y, row in enumerate(self.shape[self.rotation]):
            for x, cube in enumerate(row):
                # alleen als de cel binnen de grid zit moet hij worden laten zien en dus niet er boven
                if self.y + y * grid_size >= y_grid:
                    if cube == 1:
                        # als hij aan het vastzetten is dan knippert hij wit
                        # anders wordt hij zijn eigen kleur
                        if self.is_locking:
                            # kijkt of de fall_time even of oneven is
                            # even = blok is eigen kleur
                            # oneven = blok is wit
                            visible = int(self.fall_time * 15) % 2 == 0
                            color = self.color if visible else WHITE
                        else:
                            color = self.color
                        
                        # tekent het blokje
                        rect = pygame.Rect(self.x + x * grid_size, self.y + y *grid_size, grid_size, grid_size)
                        pygame.draw.rect(screen, color, rect)
        
    def move_down(self, tetris, spatie, arrow_down):
        # pakt de y waar het blok start
        self.start_y = self.y
        self.fall_time += delta_time
        # voert dit uit als je hard drop hebt gedaan (spatie ingeklikt)
        if spatie:
            # beweegt het blok zo ver mogelijk naar beneden
            while not self.check_grid(tetris, self.y, 0, 1, 0):
                self.y += grid_size

            # wanneer hij beneden is wordt hij vastgezet in de grid en checkt hij op volle rijen
            self.lock(tetris)
            tetris.check_full_rows()

            # reset de fall_time
            self.fall_time = 0

            # pakt de y waar het blok is geïndigt
            self.end_y = self.y

            # berekent de afgelegde afstand
            self.distance = self.distance_traveled()
            tetris.score += self.distance * 2 * tetris.level # hard drop score = 2 punten per blokje * het level
            self.distance = 0 # reset de afstand
            return

        # voert dit uit als spatie niet is ingeklikt en de verstreken tijd groter of gelijk is aan de delay
        elif self.fall_time >= self.fall_speed:
            # checkt of als het blok 1 omlaag beweegt hij iets raakt
            if self.check_grid(tetris, self.y, 0, 1, 0):
                # zo ja wordt is_locking True om het blok te laten knipperen 
                self.is_locking = True
                # dan wordt gecontroleerd of er meer of evenveel tijd is verstreken als dat de delays groot zijn
                if self.fall_time >= self.fall_speed + self.lock_delay:
                    # zo ja dan wordt de fall_time gereset en is_locking weer False
                    self.fall_time = 0
                    self.is_locking = False
                    # blok wordt vastgezet en er wordt gecontroleerd of er volle rijen zijn
                    self.lock(tetris)
                    tetris.check_full_rows()
                return # gaat terug naar main gameloop
            
            # Dit gebeurt als hij nergens tegen aankomt
            self.is_locking = False # als hij eerst niet meer omlaag kan en daarna wel weer moet hij niet meer knipperen
            self.y += grid_size # 1 blokje omlaag
            self.fall_time = 0 # fall_time gereset

            # als pijltje omlaag is ingedrukt is dit True en krijg je er punten voor
            if arrow_down:
                tetris.score += 1 * tetris.level # soft drop score = 1 per block * level
    
    def lock(self, tetris):
        # de matrix van het blok is een 4 x 4 dus op deze manier kan je door de gehele matrix heen loopen
        for y in range(0, 4):
             for x in range(0, 4):
                # checkt of het blokje in de matrix een 1 is en dus dat daar een blokje zit
                if ((self.shape[self.rotation])[y])[x] == 1:
                    # op de plek waar een blokje in de matrix zit wordt de kleur van het blok in de grid opgeslagen
                    tetris.grid[((self.y - y_grid) // grid_size) + y + 2][(self.x - x_grid) // grid_size + x] = self.color

    def move_horizontal(self, tetris):
        self.movement_time += delta_time
        keys_pressed = pygame.key.get_pressed()

        # als hij vorige frame al bewogen heeft wordt de delay anders dan als hij nog niet bewogen heeft
        if self.moving:
            delay = self.movement_delay_moving
            print("wel")
        else:
            delay = self.movement_delay_not_moving
            print("niet")
        
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
        # gaat door alle cellen van het tetrimino stuk
        for x in range(0, 4):
            for y in range(0, 4):
                # berekent de nieuwe x en y positie op basis van de meegegeven beweging
                new_x = ((self.x - x_grid) // grid_size) + x + left_or_right
                new_y = ((huidige_y - y_grid) // grid_size) + y + 2 + down
                # alleen als er een blokje zit wordt er gecheckt
                if self.shape[(self.rotation+rotation) % len(self.shape)][y][x] == 1:
                    # checkt of het blok buiten de grid gaat of op een ander blok botst
                    if new_x * grid_size + grid_size > width_grid or new_x * grid_size < 0 or new_y >= 22 or tetris.grid[new_y][new_x] != 0:
                        return True
        # als hij nergens tegen aankomt returned hij False
        return False
    
    def ghost_piece(self, tetris):
        # reset de ghost_piece telkens naar de y van het blok, zodat hij elke frame weer opnieuw de locatie van de ghost block bepaalt
        self.ghost_y = self.y
        
        # beweegt het ghost blok naar beneden totdat hij niet meer kan
        while not self.check_grid(tetris, self.ghost_y, 0, 1, 0):
            self.ghost_y += grid_size

        for y, row in enumerate(self.shape[self.rotation]):
            for x, cube in enumerate(row):
                if cube == 1:
                    rect = pygame.Rect(self.x + x * grid_size, self.ghost_y + y *grid_size, grid_size, grid_size)
                    pygame.draw.rect(screen, self.color, rect, width_ghost)

    def distance_traveled(self):
        # berekent de afgelegde afstand door eind hoogte - start hoogte te doen
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
        # loopt door alle scores om te kijken of de gehaalde score hoger is dan één van de huidige highscores
        # zo ja returned True en zo nee dan returned hij False
        for score in [row[0] for row in scores]:
            if tetris.score > score:
                return True
        return False
    
    def update_highscores(self, tetris):
        # voegt de huidige score toe aan de database
        self.db.execute("INSERT INTO highscores (name, score) VALUES (?, ?)", [tetris.naam, tetris.score])
        # haalt de scores eruit zodat er maar 5 in de database zitten
        self.db.execute("DELETE FROM highscores WHERE id not in (SELECT id FROM highscores ORDER BY score DESC LIMIT 5)")
        self.db.commit()

    def get_highscores(self):
        # vraagt de highscores op uit de database en returned ze in een lijst met tuples
        highscores = self.db.execute("SELECT name, score FROM highscores ORDER BY score DESC").fetchall()
        return highscores
    
    def reset_database(self):
        # verwijdert alles van de database
        self.db.execute("DELETE FROM highscores")

        # stopt daarna weer de standaard waardes in de database
        scores = [5000, 4000, 3000, 2000, 1000]
        for score in scores:
            self.db.execute("INSERT INTO highscores (name, score) VALUES (?, ?)", ["", score])
        self.db.commit()