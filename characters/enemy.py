import pygame
from characters.entity import Entity
from bullet import Enemy_Bullet
from abc import abstractmethod

class Enemy(Entity):
    projectiles = []

    def __init__(self, pos, groups, health, image_path):
        super().__init__(pos, groups, health, image_path)
        self.sprite_type = 'enemy'

        self.image = pygame.transform.scale(self.image, (self.image.get_width() // 10, self.image.get_height() // 10))
        self.speed = 2
        self.rect = self.image.get_rect(center = pos)
        self.StartTimer = pygame.time.get_ticks()
        self.AtackTimer = 0

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
    
    def get_damage(self, player, attack_type):
        if attack_type == 'bullet':
            self.health -= player.get_damage()
    
class Enemy_Tank(Enemy):
    def __init__(self, pos, groups):
        super().__init__(pos, groups, 100, image_path="assets/images/pokemon.png")

    def update(self, player_pos=None, group=None, health=None, camera=None, image_path=None):
        super().update()

    def _atack(self,player): ...
    
class Enemy_Shooter(Enemy):
    def __init__(self, pos, groups):
        super().__init__(pos, groups, 50, image_path = "assets/images/fantasma_1.png")

        self.animation_images = [pygame.image.load(f"assets/images/fantasma_{i}.png").convert_alpha() for i in range(1, 5)]

        new_width = 90
        new_height = 90 

        self.animation_images = [pygame.transform.scale(image, (new_width, new_height)) for image in self.animation_images]
        self.animation_index = 0

        self.facing_left = False

    def update(self, player_pos, group, health, camera, image_path):
        super().update()
        self.animate()
        self.AtackTimer = (pygame.time.get_ticks() - self.StartTimer)/1000
        if self.AtackTimer >= 3:
            self._atack(player_pos, group, health, camera, image_path)

    def animate(self):
        animation_speed = 0.07
        self.animation_index = (self.animation_index + animation_speed) % len(self.animation_images)
        self.image = self.animation_images[int(self.animation_index)]

        if self.direction.x < 0:
            self.image = pygame.transform.flip(self.image, True, False)

    def _atack(self, player_pos, group, health, camera, image_path): 
        EnemyProjectile = Enemy_Bullet(player_pos, group, health, camera, image_path)
        Enemy.projectiles.append(EnemyProjectile)
        self.StartTimer = pygame.time.get_ticks()