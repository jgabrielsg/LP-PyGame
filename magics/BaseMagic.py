from typing import Any
import pygame
from random import randrange

class BaseMagic(pygame.sprite.Sprite):
    def __init__(self, pos, groups, level, image_path=None):
        super().__init__(groups)
        self.sprite_type = 'magic'
        self.image = pygame.image.load(image_path).convert_alpha()

        self.direction = pygame.math.Vector2()
        self.pos = pos

        self.StartTimer = pygame.time.get_ticks()

        self.level = level
        self.lifeSpam = 0

        self.damage = 0

        self.rect = self.image.get_rect(center = pos)

        self.CastMagic()

    def CastMagic(self):

        randX = randrange(-10,10)
        randY = randrange(-10,10)

        self.direction.x = self.pos[0] + randX
        self.direction.y = self.pos[1] + randY

        rand = pygame.math.Vector2(self.direction)
        player_vec = pygame.math.Vector2(self.pos)

        #Checa se o mouse não está em cima do player
        if (rand - player_vec).magnitude() > 0:
            self.direction = (rand - player_vec).normalize()
        else:
            self.direction = pygame.math.Vector2()

        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()

        if self.level == 0: pass

    def update(self):
        ...

    def get_damage(self):
        return self.damage