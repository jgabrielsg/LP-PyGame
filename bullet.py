import pygame
from abc import abstractmethod
import math
from characters.enemy import Boss

class Bullet(pygame.sprite.Sprite):
    def __init__(self, pos, target_pos, groups, level, offset = pygame.math.Vector2(), image_path=None):
        super().__init__(groups)
        self.sprite_type = 'bullet'
        self.level = level
        self.pos = pos
        self.cameraOffset = offset

        self.direction = pygame.math.Vector2()

        #Pega a posição ajustada do mouse de acordo com a camera
        self.target_pos = target_pos
        self.target_pos = (target_pos[0] + self.cameraOffset.x, target_pos[1] + self.cameraOffset.y)

        self.image = pygame.image.load(image_path).convert_alpha()
        self.rect = self.image.get_rect(center = pos)
        self.speed = 10

        self.StartTimer = pygame.time.get_ticks()
        self.LifeSpam = 0

    def shoot(self):
        target_vec = pygame.math.Vector2(self.target_pos)
        player_vec = pygame.math.Vector2(self.pos)

        #Checa se o mouse não está em cima do player
        if (target_vec - player_vec).magnitude() > 0:
            self.direction = (target_vec - player_vec).normalize()
        else:
            self.direction = pygame.math.Vector2()

        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()

        self.rect.x += self.direction.x * self.speed
        self.rect.y += self.direction.y * self.speed

    def update(self):
        self.shoot()

        #Destrói o tiro dps dele ir pra fora da tela
        self.LifeSpam = (pygame.time.get_ticks() - self.StartTimer)/1000
        if self.LifeSpam > 5:
            self.kill()

class Boss_Bullet(Bullet):
    def __init__(self, type, pos, target_pos, groups, level, offset = pygame.math.Vector2(), image_path=None):
        super().__init__(pos, target_pos, groups, level, offset = offset, image_path=image_path)
        self.image = pygame.transform.scale(self.image, (self.image.get_width() * 5, self.image.get_height() * 5))
        self.updated = False

        #Vetores unitarios da direção do tiro.
        self.vx = 0
        self.vy = 0

        self.type = type

    def shoot(self):
        if self.type == 1:
            self.vx = 2 * math.cos(Boss.angulo)
            self.vy = 2 * math.sin(Boss.angulo)
        else:
            self.vx = 2 * math.cos(Boss.angulo + math.pi)
            self.vy = 2 * math.sin(Boss.angulo + math.pi)

        Boss.angulo = Boss.angulo + 0.25

    def update(self):
        if not self.updated:
            self.shoot()
            self.updated = True

        self.rect.x += self.vx * self.speed
        self.rect.y += self.vy * self.speed

        #Destrói o tiro dps dele ir pra fora da tela
        self.LifeSpam = (pygame.time.get_ticks() - self.StartTimer)/1000
        if self.LifeSpam > 5:
            self.kill()

class Boss_Laser(pygame.sprite.Sprite):
    def __init__(self, pos, groups, level):
        super().__init__(groups)
        self.sprite_type = 'bullet'
        self.level = level
        self.pos = pos

        self.image = pygame.image.load("assets/images/laser.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (self.image.get_width() * 100, self.image.get_height() * 2))
        self.rect = self.image.get_rect(center = pos)

        self.StartTimer = pygame.time.get_ticks()
        self.LifeSpam = 0
    
    def update(self):
        #Destrói o tiro dps de um tempo
        self.LifeSpam = (pygame.time.get_ticks() - self.StartTimer)/1000
        if self.LifeSpam > 2:
            self.kill()