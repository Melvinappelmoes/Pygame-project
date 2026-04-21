import random
from variables import *
from shapes import tetriminos

class Tetris():
    def __init__(self):
        self.level = 1
        self.tetriminos = self.random_tetriminos(4)
        self.current_shape = self.tetriminos[0]
        self.score = 0
        self.grid = []
        self.make_grid()
        self.game_over = False

    def random_tetriminos(self, how_many):
        self.shapes = []
        for i in range(0, how_many):
            shape, color = random.choice(list(tetriminos.values()))
            self.shapes.append(Tetrimino(shape, color, self.level))
        return self.shapes

    def make_grid(self):
        for y in range(0, (height+2*grid_size) // grid_size):
            self.grid.append([])
            for x in range(0, width // grid_size):
                self.grid[y].append(0)

    def draw_grid(self):
        # maakt de grid door, door het hele bord in rijen te gaan met stapsgrootte = grid_size
        for row_index, row in enumerate(self.grid):
            for col_index, cell in enumerate(row):
                rect = pygame.Rect(col_index *grid_size , (row_index-2) *grid_size, grid_size, grid_size)
                if cell != 0:
                    pygame.draw.rect(screen, self.grid[row_index][col_index], rect)
                pygame.draw.rect(screen, GREY, rect, 1)

class Tetrimino():
    def __init__(self, shape, color, level):
        self.x = grid_size * 3
        self.max_x = 0
        self.min_x = 4
        self.y = -(2*grid_size)
        self.max_y = 0
        self.min_y = 4
        self.color = color
        self.shape = shape
        self.rotation = 0

        self.fall_time = 0
        self.fall_speed = (0.8 - ((level - 1) * 0.007))**(level-1)
        self.movement_time = 0
        self.movement_delay = 0.1

    def draw(self):
        for y, row in enumerate(self.shape[self.rotation]):
            for x, cube in enumerate(row):
                if cube == 1:
                    self.min_x = min(self.min_x, x)
                    self.max_x = max(self.max_x, x)
                    self.min_y = min(self.min_y, y)
                    self.max_y = max(self.max_y, y)
                    rect = pygame.Rect(self.x + x * grid_size, self.y + y *grid_size, grid_size, grid_size)
                    pygame.draw.rect(screen, self.color, rect)

    def move_down(self, tetris):
        self.fall_time += delta_time
        if self.fall_time >= self.fall_speed:
            if self.y + (self.max_y+1) * grid_size >= height or self.check_grid(tetris, 0, 1):
                for x in range(self.min_x, self.max_x+1):
                    for y in range(self.min_y, self.max_y+1):
                        if ((self.shape[self.rotation])[y])[x] == 1:
                            tetris.grid[(self.y // grid_size) + y + 2][(self.x // grid_size)+ x] = self.color
                self.fall_time = 0
                tetris.tetriminos.pop(0)
                tetris.current_shape = tetris.tetriminos[0]
                tetris.tetriminos.append(tetris.random_tetriminos(1)[0])
                self.x = grid_size*3
                self.y = -(2*grid_size)
            else:
                self.y += grid_size
                self.fall_time = 0

    def move_horizontal(self, tetris):
        self.movement_time += delta_time
        if self.movement_time >= self.movement_delay:
            keys_pressed = pygame.key.get_pressed()
            if keys_pressed[pygame.K_RIGHT]:
                if self.x + (self.max_x + 1) * grid_size >= width or self.check_grid(tetris, 1, 0):
                    pass
                else:
                    self.x += grid_size
            if keys_pressed[pygame.K_LEFT]:
                if self.x + self.min_x * grid_size <= 0 or self.check_grid(tetris, -1, 0):
                    pass
                else:
                    self.x -= grid_size
            self.movement_time = 0
    
    def check_grid(self, tetris, l_r, o):
        # l_r staat voor links recht
        # o staat voor omlaag
        for x in range(self.min_x, self.max_x+1):
            for y in range(self.min_y, self.max_y+1):
                if ((self.shape[self.rotation])[y])[x] == 1:
                    if tetris.grid[(self.y // grid_size) + y + 2 + o][(self.x // grid_size)+ x + l_r] != 0:
                        return True
        return False