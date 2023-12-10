import pygame
from characters.entity import Entity
from abc import abstractmethod
import math

class Enemy(Entity):
    def __init__(self, pos, groups, health, image_path):
        super().__init__(pos, groups, health, image_path)
        self.sprite_type = 'enemy'

        self.image = pygame.transform.scale(self.image, (self.image.get_width() // 10, self.image.get_height() // 10))
        self.speed = 4
        self.rect = self.image.get_rect(center = pos)
        self.shouldShoot = False # For shooterEnemies
        self.IsBoss = False

    #Função que diz pro inimigo a direção do player
    def set_direction(self, player):
        enemy_vec = pygame.math.Vector2(self.rect.center)
        player_vec = pygame.math.Vector2(player.rect.center)

        # Checa se o player e o inimigo estão na mesma posição
        if (player_vec - enemy_vec).magnitude() > 0:
            self.direction = (player_vec - enemy_vec).normalize()
        else:
            self.direction = pygame.math.Vector2()

        #graphics

        # self.image = pygame.surface((64,64))
    
    def deal_damage(self, damage_origin):
        if damage_origin.sprite_type == 'bullet':
            self.health -= damage_origin.get_damage()
        elif damage_origin.sprite_type == 'magic':
            self.health -= damage_origin.get_damage()
    
class Enemy_Tank(Enemy):
    def __init__(self, pos, groups, health, animation_images):
        super().__init__(pos, groups, health, image_path="assets/images/ogro_1.png")
        self.speed = 3

        # Usando as imagens pré carregadas
        self.animation_images = animation_images.copy()

        self.animation_index = 0
        self.facing_left = False

    def update(self):
        super().update()
        self.animate()

    def animate(self):
        animation_speed = 0.07
        self.animation_index = (self.animation_index + animation_speed) % len(self.animation_images)
        self.image = self.animation_images[int(self.animation_index)]

        if self.direction.x < 0:
            self.image = pygame.transform.flip(self.image, True, False)
    
class Enemy_Shooter(Enemy):
    def __init__(self, pos, groups, health, animation_images):
        super().__init__(pos, groups, health, image_path = "assets/images/fantasma_1.png")

        # Usando as imagens pré carregadas
        self.animation_images = animation_images
        self.animation_index = 0
        self.speed = 2

        self.facing_left = False

        self.cooldown = 5
        self.LastShot = 0
        # pygame.time.get_ticks()

    def update(self):
        super().update()
        self.animate()

        if not self.shouldShoot:
            if (pygame.time.get_ticks() - self.LastShot)/1000 > self.cooldown:
                self.shouldShoot = True
                self.LastShot = pygame.time.get_ticks()

    def animate(self):
        animation_speed = 0.07
        self.animation_index = (self.animation_index + animation_speed) % len(self.animation_images)
        self.image = self.animation_images[int(self.animation_index)]

        if self.direction.x < 0:
            self.image = pygame.transform.flip(self.image, True, False)

class Boss(Enemy):
    angulo = 0

    def __init__(self, pos, groups, animation_images):
        super().__init__(pos, groups, 250, image_path = "assets/images/vilao_1.png")
        self.sprite_type = 'enemy'

        self.image = pygame.transform.scale(self.image, (self.image.get_width() * 5, self.image.get_height() * 5))
        self.speed = 1
        self.rect = self.image.get_rect(center = pos)
        self.shouldShoot = False # For shooterEnemies
        self.shouldLaser = False

        self.IsBoss = True

        self.cooldown = 250 # Milisegundos
        self.LastShot = 0

        self.laser_cooldown = 3000
        self.LastLaser = 0

        self.animation_images = animation_images
        self.animation_index = 0

        self.facing_left = False

    def update(self):
        super().update()
        self.animate()

        if not self.shouldShoot:
            if (pygame.time.get_ticks() - self.LastShot) > self.cooldown:
                self.shouldShoot = True
                self.LastShot = pygame.time.get_ticks()

        if not self.shouldLaser:
            if (pygame.time.get_ticks() - self.LastLaser) > self.laser_cooldown:
                self.shouldLaser = True
                self.LastLaser = pygame.time.get_ticks()


    # def laser(self, player):
    #     laser = []
    #     laser_image = pygame.image.load("assets/images/laser.png").convert_alpha()
    #     laser_image = pygame.transform.scale(laser_image, (laser_image.get_width() * 100, laser_image.get_height() * 5))
    #     rect = laser_image.get_rect(center = player.rect.center)

    def animate(self):
        animation_speed = 0.07
        self.animation_index = (self.animation_index + animation_speed) % len(self.animation_images)
        self.image = self.animation_images[int(self.animation_index)]

        if self.direction.x < 0:
            self.image = pygame.transform.flip(self.image, True, False)

        