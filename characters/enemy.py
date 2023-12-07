import pygame
from characters.entity import Entity
from abc import abstractmethod

class Enemy(Entity):
    def __init__(self, pos, groups, health, image_path):
        super().__init__(pos, groups, health, image_path)
        self.sprite_type = 'enemy'

        self.image = pygame.transform.scale(self.image, (self.image.get_width() // 10, self.image.get_height() // 10))
        self.speed = 2
        self.rect = self.image.get_rect(center = pos)

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
    
    @abstractmethod
    def _atack(self,player): ...
    
class Enemy_Tank(Enemy):
    def __init__(self, pos, groups):
        super().__init__(pos, groups, 100, image_path="assets/images/pokemon.png")

    def _atack(self,player): ...
    
class Enemy_Shooter(Enemy):
    def __init__(self, pos, groups):
        super().__init__(pos, groups, 50, image_path="assets/images/fantasma_1.png")
        self.image = pygame.transform.scale(self.image, (int(self.image.get_width() * 1.5),
                                                         int(self.image.get_height() * 1.5)))

    def _atack(self, player): ...