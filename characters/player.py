import pygame
from characters.entity import Entity

class Player(Entity):
    def __init__(self, pos, group, health, image_paths):
        super().__init__(pos, group, health, image_paths[0])  # Inicializa com a primeira imagem
        self.sprite_type = 'player'
        
        # Carrega as duas imagens e as dimensiona
        self.images = [pygame.transform.scale(pygame.image.load(path), (self.image.get_width() * 1.5, self.image.get_height() * 1.5)) for path in image_paths]
        self.image_index = 0  # Índice da imagem
        self.original_image = pygame.transform.scale(self.image, (self.image.get_width() * 1.5, self.image.get_height() * 1.5))
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

        if self.health <= 0:
            return True # Se o jogo acaba
        else: return False

    def get_damage(self):
        return self.base_damage
    
    def get_xp(self):
        return self.xp
    
    def xp_up(self, amount):
        self.xp += amount

    def reset_xp(self):
        self.xp = 0

class HealthBar(pygame.sprite.Sprite):
    def __init__(self, initial_player_pos, groups):
        super().__init__(groups)
        self.position = initial_player_pos
        self.image = pygame.image.load("assets/images/health_bar10.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (self.image.get_width() * 6, self.image.get_height() * 6))
        self.rect = self.image.get_rect(center = self.position,left = 10)

    def update_health(self, health_now):
        i = health_now/10
        self.image = pygame.image.load(f"assets/images/health_bar{i}.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (self.image.get_width() * 6, self.image.get_height() * 6))
        self.rect = self.image.get_rect(center = self.position,left = 10)
