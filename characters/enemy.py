import pygame
from characters.entity import Entity

class Enemy(Entity):
    def __init__(self, pos, groups, image_path):
        super().__init__(pos, groups, image_path)
        self.sprite_type = 'enemy'

        self.image = pygame.transform.scale(self.image, (self.image.get_width() // 10, self.image.get_height() // 10))
        self.speed = 1
        self.rect = self.image.get_rect(center = pos)
        self.hitbox = self.rect

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