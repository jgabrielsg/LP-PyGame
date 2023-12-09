import pygame
from characters.entity import Entity

class Player(Entity):
    def __init__(self, pos, group, health, image_path):
        super().__init__(pos, group, health, image_path)
        self.sprite_type = 'player'
        
        self.original_image = pygame.transform.scale(self.image, (self.image.get_width() // 1.2, self.image.get_height() // 1.2))
        self.image = self.original_image

        self.speed = 5
        self.xp = 0

        #Cuida da invencibilidade do player
        self.LastTimeHit = 0
        self.InvencibleTime = 2
        self.invencible = False

    def input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.direction.x = -1
            self.image = self.original_image
        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.direction.x = 1
            self.image = pygame.transform.flip(self.original_image, True, False)
        else:
            self.direction.x = 0

        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.direction.y = -1
        elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.direction.y = 1
        else:
            self.direction.y = 0

    def update(self):
        super().update()
        self.input()

        if (pygame.time.get_ticks() - self.LastTimeHit)/1000 > self.InvencibleTime:
            self.image.set_alpha(255)
            self.invencible = False
    
    def deal_damage(self):
        if not self.invencible:
            self.LastTimeHit = pygame.time.get_ticks()
            self.image.set_alpha(150)
            self.health -= 10
            self.invencible = True

    def get_damage(self):
        return self.base_damage
    
    def get_xp(self):
        return self.xp
    
    def xp_up(self, amount):
        self.xp += amount

    def reset_xp(self):
        self.xp = 0