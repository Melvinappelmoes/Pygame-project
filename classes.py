import random
from variables import *
from shapes import tetriminos

class Tetris():
    def __init__(self):
        self.level = 1
        self.tetriminos = self.random_tetriminos()
        self.current_shape = self.shapes[0]
        self.score = 0
        self.game_over = False

    def random_tetriminos(self):
        self.shapes = []
        for i in range(0, 4):
            shape, color = random.choice(list(tetriminos.values()))
            self.shapes.append(Tetrimino(shape, color, self.level))

class Tetrimino():
    def __init__(self, shape, color, level):
        self.x = grid_size * 3
        self.max_x = 0
        self.min_x = 4
        self.y = 0
        self.max_y = 0
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
                    self.max_y = max(self.max_y, y)
                    rect = pygame.Rect(self.x + x * grid_size, self.y + y *grid_size, grid_size, grid_size)
                    pygame.draw.rect(screen, self.color, rect)

    def move_down(self):
        self.fall_time += delta_time
        if self.fall_time >= self.fall_speed:
            if self.y + (self.max_y+1) * grid_size >= height:
                self.fall_time = 0
            else:
                self.y += grid_size
                self.fall_time = 0

    def move_horizontal(self):
        self.movement_time += delta_time
        if self.movement_time >= self.movement_delay:
            keys_pressed = pygame.key.get_pressed()
            if keys_pressed[pygame.K_RIGHT]:
                if self.x + (self.max_x + 1) * grid_size >= width:
                    pass
                else:
                    self.x += grid_size
            if keys_pressed[pygame.K_LEFT]:
                if self.x + self.min_x * grid_size <= 0:
                    pass
                else:
                    self.x -= grid_size
            self.movement_time = 0