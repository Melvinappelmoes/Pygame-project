from variables import *
class Tetrimino():
    def __init__(self, shape, color):
        self.x = grid_size * 3
        self.y = 0
        self.color = color
        self.shape = shape
        self.rotation = 0

        self.level = 1
        self.fall_time = 0
        self.fall_speed = (0.8 - ((self.level - 1) * 0.007))**(self.level-1)
        self.movement_time = 0
        self.movement_delay = 0.1

    def draw(self):
        for y, row in enumerate(self.shape[self.rotation]):
            for x, cube in enumerate(row):
                if cube == 1:
                    rect = pygame.Rect(self.x + x * grid_size, self.y + y *grid_size, grid_size, grid_size)
                    pygame.draw.rect(screen, self.color, rect)

    def move_down(self):
        self.fall_time += delta_time
        if self.fall_time >= self.fall_speed:
            self.y += grid_size
            self.fall_time = 0

    def move_horizontal(self):
        self.movement_time += delta_time
        if self.movement_time >= self.movement_delay:
            if keys_pressed[pygame.K_RIGHT]:
                self.x += grid_size
            if keys_pressed[pygame.K_LEFT]:
                self.x -= grid_size
            if keys_pressed[pygame.K_DOWN]:
                self.fall_speed *= 20
            self.movement_time = 0
            self.fall_speed = (0.8 - ((self.level - 1) * 0.007))**(self.level-1)