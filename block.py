import pygame

class Block(pygame.Rect):
    def __init__(self, x, y, width, height, image_path=None):
        super().__init__(x, y, width, height)
        self._image = pygame.image.load(image_path).convert_alpha() if image_path else None

    @property
    def image(self):
        return self._image

    @image.setter
    def image(self, image_path):
        self._image = pygame.image.load(image_path).convert_alpha() if image_path else None

    def draw(self, screen):
        # Desenha a imagem por tiles de 64 por 64 pixels, tanto na horizontal como na vertical
        if self._image:
            for i in range(self.x, self.x + self.width, 64):
                for j in range(self.y, self.y + self.height, 64):
                    screen.blit(self._image, (i, j))
        else:
            pygame.draw.rect(screen, self.color, self)
