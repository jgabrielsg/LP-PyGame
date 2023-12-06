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
                    PlayerProjectile = Bullet(self.player.hitbox.center, self.camera, 1, self.camera.offset, image_path="assets/images/bullet.png")
                    self.projectiles.append(PlayerProjectile)
    
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

        # Atualiza o player
        self.player.update()
        
        for enemy in self.enemies:
            enemy.set_direction(self.player)
            enemy.update()
            if (enemy.hitbox.colliderect(self.player.hitbox)):
                # print("Colisão funfando")
                pass
        
        for projectile in self.projectiles:
            # Loops de todos os projéteis, pensei em tacar aqui a colisão mas talvez isso não seja mt ótimo, teria q iterar sobre todos os
            # projéteis e todos os inimigos
            #TODO ver como checar a interação dos tiros e dos inimigos
            pass

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
            NewEnemy = Enemy((x, y), self.camera, 50, image_path="assets/images/applejack.png")
            self.enemies.append(NewEnemy)
        elif type == 2:
            NewEnemy = Enemy((x, y), self.camera, 50, image_path="assets/images/pokemon.png")
            self.enemies.append(NewEnemy)
            

    # Chama todas as funções de game
    def run(self):
        clock = pygame.time.Clock()
        self.start_time = pygame.time.get_ticks()

        while self.running:
            self.events()
            self.update()
            # self.criar_inimigos()

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