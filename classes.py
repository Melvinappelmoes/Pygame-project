from variables import *
class Tetrimino():
    def __init__(self, shape, color):
        self.x = grid_size * 3
        self.y = 0
        self.color = color
        self.shape = shape
        self.rotation = 0

    def draw(self):
        for y, row in enumerate(self.shape[self.rotation]):
            for x, cube in enumerate(row):
                if cube == 1:
                    rect = pygame.Rect(self.x + x * grid_size, self.y + y *grid_size, grid_size, grid_size)
                    pygame.draw.rect(screen, self.color, rect)

    def move_down(self):
        self.y += grid_size