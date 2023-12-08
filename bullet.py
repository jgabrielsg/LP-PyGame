import pygame

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