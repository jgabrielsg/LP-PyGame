import pygame
import sys

import math
import random

from characters.player import Player
from characters.enemy import Enemy
from camera import CameraGroup
from bullet import Bullet

from block import Block
from config import SCREEN_HEIGHT, SCREEN_WIDHT

from screens.main_menu import Menu
from screens.options import Options

from music import Music

music_player = Music()

class Game:
    def __init__(self):
        pygame.init()

        self.clock = pygame.time.Clock()

        # Window settings
        self.screen = pygame.display.set_mode((SCREEN_WIDHT, SCREEN_HEIGHT))
        pygame.display.set_caption("Pygame Window")

        # Camera setup
        self.camera = CameraGroup(groundpath='assets/images/mapa.png')

        initial_pos = (SCREEN_WIDHT/2, SCREEN_HEIGHT/2)

        # Game objects
        self.player = Player(initial_pos, self.camera, 100, image_path="assets/images/player.png")
        self.projectiles = []

        # Proriedades de Ataque
        self.attack_sprites = pygame.sprite.Group()
        self.attackable_sprites = pygame.sprite.Group()

        # Controle de Inimigos
        self.enemies = []
        self.cooldown = 1
        self.enemyOnCooldown = True
        self.tempoInicio = 0
        
        self.running = True
    
    # Aqui ficam os handlers de eventos
    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                pygame.quit()
                sys.exit()

            #Cuida dos tiros do player
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if self.running == True:
                    PlayerProjectile = Bullet(self.player.rect.center, [self.attack_sprites, self.camera], 1, self.camera.offset, image_path="assets/images/bullet.png")
                    self.projectiles.append(PlayerProjectile)

    def collisions(self):
        #Função que cuida das colisões de dano (inimigo - player), (tiro - inimigo)

        #Dano nos inimigos 
        if self.attack_sprites:
            for attack_sprite in self.attack_sprites:
                collision_sprites = pygame.sprite.spritecollide(attack_sprite, self.attackable_sprites, False)
                if collision_sprites:
                    for target_sprite in collision_sprites:
                        target_sprite.get_damage(self.player, attack_sprite.sprite_type)
                        if attack_sprite.sprite_type == 'bullet':
                            attack_sprite.kill()
    
    # Qualquer atualização de posição ou animação ficam aqui.
    def update(self):
        tempo = (pygame.time.get_ticks() - self.start_time) / 1000

        # Spawna os inimigos em intervalos de tempo aleatórios.
        if not self.enemyOnCooldown:
            self.enemyOnCooldown = True
            self.cooldown = random.randint(1,5)
            self.tempoInicio = tempo
        elif tempo > (self.tempoInicio + self.cooldown):
            self.criar_inimigos(random.randint(1,2))
            self.enemyOnCooldown = False

        for enemy in self.enemies:
            enemy.set_direction(self.player)
            enemy.update()

        # Descobri que o pygame chama sozinho todos os métodos update(), mas vou deixar só pra deixar bonito
        for projectile in self.projectiles:
            projectile.update()

        # Atualiza o player
        self.player.update()

        self.collisions()

        self.screen.fill((0,0,0)) 

        # Cuida da câmera
        self.camera.update()
        self.camera.center_target_camera(self.player)
        self.camera.custom_draw()  

    # Cria inimigos fora do campo de visão do player
    def criar_inimigos(self, type=1):
        distancia = 1500
        angle = random.uniform(0, 2 * math.pi)
        x = self.player.rect.centerx + distancia * math.cos(angle)
        y = self.player.rect.centery + distancia * math.sin(angle)

        #Cria os inimigos com base no tipo deles
        if type == 1:
            NewEnemy = Enemy((x, y), [self.attackable_sprites, self.camera], 50, image_path="assets/images/applejack.png")
            self.enemies.append(NewEnemy)
        elif type == 2:
            NewEnemy = Enemy((x, y), [self.attackable_sprites, self.camera], 50, image_path="assets/images/pokemon.png")
            self.enemies.append(NewEnemy)
            

    # Chama todas as funções de game
    def run(self):
        clock = pygame.time.Clock()
        self.start_time = pygame.time.get_ticks()

        while self.running:
            self.events()
            self.update()

            # Limita a taxa de quadros (FPS)
            clock.tick(60)

            # Atualiza a tela
            pygame.display.flip()

        pygame.quit()
        sys.exit()

# Cria o game e roda ele
if __name__ == "__main__":
    game = Game()
    menu = Menu(game.screen)
    options = Options(game.screen)
    while True:
        result = menu.run()
        if result == 'play':
            music_player.background
            game.run()
        elif result == 'options':
            options.run()