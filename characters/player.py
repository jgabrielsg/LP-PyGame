import pygame
from characters.entity import Entity

class Player(Entity):
    def __init__(self, pos, group, image_path):
        super().__init__(pos, group, image_path)
        self.sprite_type = 'player'
        
        self.original_image = pygame.transform.scale(self.image, (self.image.get_width() // 1.2, self.image.get_height() // 1.2))
        self.image = self.original_image

        self.speed = 3
        self.hitbox = self.rect.inflate(0,-10)

    def input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            self.direction.x = -1
            self.image = self.original_image
        elif keys[pygame.K_RIGHT]:
            self.direction.x = 1
            self.image = pygame.transform.flip(self.original_image, True, False)
        else:
            self.direction.x = 0

        if keys[pygame.K_UP]:
            self.direction.y = -1
        elif keys[pygame.K_DOWN]:
            self.direction.y = 1
        else:
            self.direction.y = 0

    def update(self):
        super().update()
        self.input()