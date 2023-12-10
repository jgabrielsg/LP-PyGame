import pygame

class Block(pygame.Rect):
    def __init__(self, x, y, width, height, image_path=None):
        super().__init__(x, y, width, height)
        if image_path:
            self.image = pygame.image.load(image_path).convert_alpha()
        else:
            self.image = None

    def draw(self, screen):
        if self.image:
            for i in range(self.x, self.x + self.width, 64):
                for j in range(self.y, self.y + self.height, 64):
                    screen.blit(self.image, (i, j))
        else:
            pygame.draw.rect(screen, self.color, self)

