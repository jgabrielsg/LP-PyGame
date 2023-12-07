import pygame
from magics.BaseMagic import BaseMagic

class LazerBeam(BaseMagic):
    def __init__(self, pos, groups, level, image_path=None):
        super().__init__(pos, groups, level, image_path=image_path)

        self.speed = 30
        self.lifeSpam = 3
    
    def move(self):
        #Impede que a entidade se mova mais rápido na diagonal
        self.rect.x += self.direction.x * self.speed
        self.rect.y += self.direction.y * self.speed

    def CastMagic(self):
        super().CastMagic()
        if self.level > 3: 
            self.damage = 100
        else: self.damage = 50

    def update(self):
        self.move()

        self.LifeSpam = (pygame.time.get_ticks() - self.StartTimer)/1000
        if self.LifeSpam > 5:
            self.kill()