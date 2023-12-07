import pygame
from abc import abstractmethod

class Entity(pygame.sprite.Sprite):
    def __init__(self, pos, groups, health, image_path=None):
        super().__init__(groups)
        self.image = pygame.image.load(image_path).convert_alpha()
        self.direction = pygame.math.Vector2()

        self.health = health

        self.rect = self.image.get_rect(center = pos)
        self.speed = 0
        
    def move(self, speed):
        #Impede que a entidade se mova mais rápido na diagonal
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()

        self.rect.x += self.direction.x * speed
        self.rect.y += self.direction.y * speed

    def check_death(self):
        if self.health <= 0:
            self.kill()

    def update(self):
        self.check_death()
        self.move(self.speed)

