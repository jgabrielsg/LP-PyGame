import pygame
from characters.entity import Entity
from abc import abstractmethod
import math

class Enemy(Entity):
    def __init__(self, pos, groups, health, image_path):
        super().__init__(pos, groups, health, image_path)
        self.sprite_type = 'enemy'

        self.image = pygame.transform.scale(self.image, (self.image.get_width() // 10, self.image.get_height() // 10))
        self.speed = 2
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
    
    def get_damage(self, player, damage_origin):
        if damage_origin.sprite_type == 'bullet':
            self.health -= player.get_damage()
        elif damage_origin.sprite_type == 'magic':
            self.health -= damage_origin.get_damage()
    
class Enemy_Tank(Enemy):
    def __init__(self, pos, groups):
        super().__init__(pos, groups, 50, image_path = "assets/images/ogro_1.png")

        self.animation_images = [pygame.image.load(f"assets/images/ogro_{i}.png").convert_alpha() for i in range(1, 5)]

        new_width = 110
        new_height = 110 

        self.animation_images = [pygame.transform.scale(image, (new_width, new_height)) for image in self.animation_images]
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
    def __init__(self, pos, groups):
        super().__init__(pos, groups, 50, image_path = "assets/images/fantasma_1.png")

        self.animation_images = [pygame.image.load(f"assets/images/fantasma_{i}.png").convert_alpha() for i in range(1, 5)]

        new_width = 90
        new_height = 90 

        self.animation_images = [pygame.transform.scale(image, (new_width, new_height)) for image in self.animation_images]
        self.animation_index = 0

        self.facing_left = False

        self.cooldown = 5000 # Milisegundos
        self.LastShot = 0
        # pygame.time.get_ticks()

    def update(self):
        super().update()
        self.animate()

        if not self.shouldShoot:
            if (pygame.time.get_ticks() - self.LastShot) > self.cooldown:
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

    def __init__(self, pos, groups):
        super().__init__(pos, groups, 1000, image_path = "assets/images/boss.jpg")
        self.sprite_type = 'enemy'

        self.image = pygame.transform.scale(self.image, (self.image.get_width() * 5, self.image.get_height() * 5))
        self.speed = 1
        self.rect = self.image.get_rect(center = pos)
        self.shouldShoot = False # For shooterEnemies

        self.IsBoss = True

        self.cooldown = 1000 # Milisegundos
        self.LastShot = 0

    def update(self):
        super().update()
        # self.animate()

        if not self.shouldShoot:
            if (pygame.time.get_ticks() - self.LastShot) > self.cooldown:
                self.shouldShoot = True
                self.LastShot = pygame.time.get_ticks()

        