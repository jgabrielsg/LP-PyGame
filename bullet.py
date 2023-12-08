import pygame
from abc import abstractmethod

class Bullet(pygame.sprite.Sprite):
    def __init__(self, pos, groups, offset, image_path=None):
        super().__init__(groups)
        self.sprite_type = 'bullet'
        self.pos = pos
        self.cameraOffset = offset

        self.direction = pygame.math.Vector2()

        self.image = pygame.image.load(image_path).convert_alpha()
        self.rect = self.image.get_rect(center = pos)
        self.speed = 20

        self.StartTimer = pygame.time.get_ticks()
        self.DestroyTimer = 0

    @abstractmethod
    def shoot(self): ...

    def update(self):
        #Destrói o tiro dps dele ir pra fora da tela
        self.shoot()

        self.DestroyTimer = (pygame.time.get_ticks() - self.StartTimer)/1000
        if self.DestroyTimer > 5:
            self.kill()

class Player_Bullet(Bullet):
    def __init__(self, pos, groups, level, offset, image_path):
        super().__init__(pos, groups, offset, image_path)
        self.level = level

        #Pega a posição ajustada do mouse de acordo com a camera
        mouse_pos = pygame.mouse.get_pos()
        self.mousepos = (mouse_pos[0] + self.cameraOffset.x, mouse_pos[1] + self.cameraOffset.y)
    
    def shoot(self):
        mousevec = pygame.math.Vector2(self.mousepos)
        player_vec = pygame.math.Vector2(self.pos)

        #Checa se o mouse não está em cima do player
        if (mousevec - player_vec).magnitude() > 0:
            self.direction = (mousevec - player_vec).normalize()
        else:
            self.direction = pygame.math.Vector2()

        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()

        self.rect.x += self.direction.x * self.speed
        self.rect.y += self.direction.y * self.speed

class Enemy_Bullet(Bullet):
    def __init__(self, enemy_pos, player_direction, groups, offset, image_path):
        super().__init__(enemy_pos, groups, offset, image_path)
        self.player_direction = player_direction

    def shoot(self):
        self.rect.x += self.player_direction.x * self.speed
        self.rect.y += self.player_direction.y * self.speed