from variables import *
class Tetrimino():
    def __init__(self, shape, color):
        self.x = 120
        self.y = 0
        self.color = color
        self.shape = shape
        self.rotation = 1

    def draw(self):
        for shape in self.shape[self.rotation]:
            for cube in shape:
                if cube == 1:
                    rect = pygame.Rect(self.x, self.y, grid_size, grid_size)
                    pygame.draw.rect(screen, self.color, rect)
                self.x += 30
            self.x = 120
            self.y += 30
        self.y = 0
        

    def move_down(self):
        pass
