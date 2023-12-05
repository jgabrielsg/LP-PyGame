import pygame

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, group, image_path=None):
        super().__init__(group)
        self.original_image = pygame.image.load(image_path).convert_alpha()
        self.image = self.original_image
        self.rect = self.image.get_rect(center = pos)
        self.direction = pygame.math.Vector2()
        self.speed = 3

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
        self.input()
        self.rect.center += self.direction * self.speed

    def draw(self, screen):
        screen.blit(self.image, self)
