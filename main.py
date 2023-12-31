import pygame
import sys

import math
import random
from pytmx.util_pygame import load_pygame

from characters.player import Player, HealthBar
from characters.enemy import Boss, Enemy_Tank, Enemy_Shooter

from magics.lazerbeam import LazerBeam

from camera import CameraGroup
from bullet import Bullet, Boss_Bullet, Boss_Laser
from mana import Mana

from block import Block
from config import SCREEN_HEIGHT, SCREEN_WIDHT

from screens.death_screen import DeathScreen
from screens.main_menu import Menu
from screens.options import Options
from screens.upgrade_screen import UpradeScreen

from music import Music

class Tile(pygame.sprite.Sprite):
    def __init__(self,pos,surf, groups):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_rect(topleft = pos)

class Game:
    def __init__(self):
        pygame.init()

        self.clock = pygame.time.Clock()

        # Window settings
        self.screen = pygame.display.set_mode((SCREEN_WIDHT, SCREEN_HEIGHT))
        pygame.display.set_caption("Pygame Window")

        # Camera setup
        self.camera = CameraGroup(groundpath='assets/images/mapa.png')

        # Cria os objetos do mapa
        tmx_data = load_pygame('assets/maptile/mapa.tmx')
        for obj in tmx_data.objects:
            pos = obj.x, obj.y
            if obj.image:
                Tile(pos, obj.image, self.camera)

        object_layer = tmx_data.get_layer_by_name("Objetos")

        initial_pos = (SCREEN_WIDHT/2, SCREEN_HEIGHT/2)

        # Player related
        player_images = ["assets/images/player1.png", "assets/images/player2.png"]
        self.player = Player(initial_pos, self.camera, 100, image_paths=player_images)
        self.projectiles = []
        self.xp_levelup = 100

        # Cria grupos (listas) de sprites para iteração
        self.attack_sprites = pygame.sprite.Group()
        self.damagePlayer_sprites = pygame.sprite.Group()
        self.attackable_sprites = pygame.sprite.Group()
        self.item_sprites = pygame.sprite.Group()
        self.ghost_sprite = pygame.sprite.Group()

        #Health Bar
        self.health_bar = HealthBar(self.screen)

        # Controle de Mana
        self.manaGenerationCooldown = 1
        self.MaxMana = 25
        self.manaCount = 0
        self.manaTime = 0

        # Controle de Inimigos
        self.enemies = []
        self.maxEnemies = 100 #Limita o número de inimigos
        self.enemyGenerationCooldown = 0.8
        self.enemyTime = 0
        self.LastBossTime = 0

        # Pré carregando as imagens dos inimigos para não ter que fazer em toda vez que spawna
        self.Ogre_animation_images = [pygame.image.load(f"assets/images/ogro_{i}.png").convert_alpha() for i in range(1, 5)]
        new_width = 110
        new_height = 110
        self.Ogre_animation_images = [pygame.transform.scale(image, (new_width, new_height)) for image in self.Ogre_animation_images]

        self.Ghost_animation_images = [pygame.image.load(f"assets/images/fantasma_{i}.png").convert_alpha() for i in range(1, 5)]
        new_width = 90
        new_height = 90 
        self.Ghost_animation_images = [pygame.transform.scale(image, (new_width, new_height)) for image in self.Ghost_animation_images]
        
        self.Boss_animation_images = [pygame.image.load(f"assets/images/vilao_{i}.png").convert_alpha() for i in range(1, 5)]
        new_width = 230
        new_height = 230 
        self.Boss_animation_images = [pygame.transform.scale(image, (new_width, new_height)) for image in self.Boss_animation_images]

        # Controle de Upgrades
        self.Upgrading = False
        self.upgradeScreen = UpradeScreen(self.screen)
        self.Magics = {"Stronger Attacks": 0, "Laser Beam": 0, "Fire Rate": 0}

        # Controle de Poderes
        self.LazerBeamCooldown = 3
        self.LazerTime = 0

        self.playerCooldown = 0.3
        self.playerLastShot = 0

        self.running = True

        # Fim de jogo
        self.UltimoTempo = 0
        self.GameOver = False
        self.dead_menu = DeathScreen(self.screen)
        self.font = pygame.font.Font(None, 36)
        
    # Chama todas as funções de game
    def run(self):
        clock = pygame.time.Clock()
        self.start_time = pygame.time.get_ticks()

        while self.running:
            self.events()

            if not self.GameOver:

                if not self.Upgrading and self.running:
                    self.update()
                elif self.Upgrading:   
                    upgrade_1 = random.choice(list(self.Magics.keys()))
                    upgrade_2 = random.choice(list(self.Magics.keys()))
                    upgrade_3 = random.choice(list(self.Magics.keys()))
                    upgrade = self.upgradeScreen.run(self.camera.offset, upgrade_1, upgrade_2, upgrade_3)
                    
                    self.Magics[upgrade] += 1      
                    self.playerCooldown = 0.3 - (self.Magics["Fire Rate"]/20)
                    self.LazerBeamCooldown = 3 - (self.Magics["Laser Beam"]/5)      
                    self.Upgrading = False  

            else:
                    self.dead_menu.run(self.UltimoTempo)
                    
                    for i in self.enemies:
                        i.kill()
                    self.enemies.clear()

                    for i in self.projectiles:
                        i.kill()
                    self.projectiles.clear()

                    self.player.health = 100
                    self.enemyTime = 0
                    self.LazerTime = 0
                    self.manaTime = 0

                    self.Magics = {"Stronger Attacks": 0, "Laser Beam": 0, "Fire Rate": 0}

                    self.start_time = pygame.time.get_ticks()

                    self.GameOver = False

            # Limita a taxa de quadros (FPS)
            clock.tick(60)

            # Atualiza a tela
            pygame.display.flip()

        pygame.quit()
        sys.exit()
    
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

                    if (pygame.time.get_ticks() - self.playerLastShot)/1000 > self.playerCooldown:
                        PlayerProjectile = Bullet(self.player.rect.center, pygame.mouse.get_pos(), [self.attack_sprites, self.camera], self.Magics["Stronger Attacks"], self.camera.offset, image_path="assets/images/bullet.png")
                        self.projectiles.append(PlayerProjectile)
                        self.playerLastShot = pygame.time.get_ticks()
                        music_player.shot

    def collisions(self):
        #Função que cuida das colisões de dano (inimigo - player), (tiro - inimigo)

        #Dano no Player
        collision_sprites = pygame.sprite.spritecollide(self.player, self.damagePlayer_sprites, False)
        if collision_sprites:
            for enemy_sprite in collision_sprites:
                if enemy_sprite.sprite_type == 'bullet':
                    enemy_sprite.kill()
                self.GameOver = self.player.deal_damage()

        #Coleta de Mana
        if self.item_sprites:
            collision_sprites = pygame.sprite.spritecollide(self.player, self.item_sprites, True)
            if collision_sprites:
                for mana in collision_sprites:
                    self.player.xp_up(mana.xp)
                    mana.kill()
                    self.manaCount -= 1
                    music_player.mana
        
        #Dano nos inimigos 
        if self.attack_sprites:
            for attack_sprite in self.attack_sprites:
                collision_sprites = pygame.sprite.spritecollide(attack_sprite, self.attackable_sprites, False)
                if collision_sprites:
                    for target_sprite in collision_sprites:
                        target_sprite.deal_damage(attack_sprite)
                        if attack_sprite.sprite_type == 'bullet':
                            attack_sprite.kill()
    
    # Qualquer atualização de posição ou animação ficam aqui.
    def update(self):
        tempo = (pygame.time.get_ticks() - self.start_time) / 1000 

        # Cria mana a cada dois segundos (se já não estiver muita mana no mapa)
        if self.manaCount < self.MaxMana: self.randomizador_mana(tempo)
        
        # Spawna os inimigos em intervalos de tempo aleatórios.
        if len(self.enemies) < self.maxEnemies:
            self.randomizador_inimigos(tempo)

        # Cuida dos inimigos 
        for enemy in self.enemies:
            if enemy.health <= 0:
                enemy.kill()
                self.enemies.remove(enemy)
                break
            enemy.set_direction(self.player)

            # Inimigos Shooters atiram
            if not enemy.IsBoss:
                if enemy.shouldShoot:
                    EnemyBullet = Bullet(enemy.rect.center, self.player.rect.center, [self.camera, self.damagePlayer_sprites], 1, image_path="assets/images/bullet.png")
                    self.projectiles.append(EnemyBullet)
                    enemy.shouldShoot = False
            else: 
                if enemy.shouldShoot:
                    EnemyBullet1 = Boss_Bullet(1,enemy.rect.center, self.player.rect.center, [self.camera, self.damagePlayer_sprites], 1, image_path="assets/images/screw.png")
                    EnemyBullet2 = Boss_Bullet(2,enemy.rect.center, self.player.rect.center, [self.camera, self.damagePlayer_sprites], 1, image_path="assets/images/screw.png")
                    self.projectiles.append(EnemyBullet1)
                    self.projectiles.append(EnemyBullet2)
                    enemy.shouldShoot = False

                if enemy.shouldLaser:
                    EnemyLaser = Boss_Laser(self.player.rect.center, [self.camera, self.ghost_sprite], [self.camera, self.damagePlayer_sprites], 1)
                    self.projectiles.append(EnemyLaser)
                    enemy.shouldLaser = False

        for projectile in self.projectiles:
            if projectile.LifeSpam > 4:
                self.projectiles.remove(projectile)

        # Cria um lazer
        if self.Magics["Laser Beam"] != 0:
            self.Cast_Lazer(tempo)

        # Aumenta o nível do player
        if self.player.get_xp() > self.xp_levelup:
            self.xp_levelup *= 1.1
            self.player.reset_xp()
            self.Upgrading = True

        self.collisions()

        # Cuida da câmera
        self.camera.update() # O camera.update() dá update em todos os outros sprites que estão no seu grupo por default do pygame
                             # então não é necessário chamar self.player.update(), por exemplo
        self.camera.center_target_camera(self.player)
        self.camera.custom_draw()  

        text_surface = self.font.render(f"Survival Time: {tempo:.2f} seconds", True, (255, 0, 0))  # Black text
        text_rect = text_surface.get_rect(left = 10)  # Adjust the position as needed

        self.health_bar.update(self.player.health)

        # Blit the text onto the screen
        self.screen.blit(text_surface, text_rect)

        if self.GameOver:
            self.UltimoTempo = tempo

    def randomizador_inimigos(self, tempo):
        if (tempo - self.LastBossTime) > 60:
            self.spawn_enemy(tempo, 4)
            self.LastBossTime = tempo

        elif tempo > (self.enemyTime + self.enemyGenerationCooldown):

            self.enemyTime = tempo
            self.spawn_enemy(tempo, random.randint(1,3))

            #Dificultando com o passar do tempo
            if tempo > 90: self.enemyGenerationCooldown = 0.1
            elif tempo > 60: self.enemyGenerationCooldown = 0.5
            elif tempo > 30: self.enemyGenerationCooldown = random.randint(0,1)
            elif tempo > 15: self.enemyGenerationCooldown = random.randint(0,2)
            elif tempo > 7: self.enemyGenerationCooldown = random.randint(0,3)
            else: self.enemyGenerationCooldown = 3

    #Define quando uma mana deve ser spawnada 
    def randomizador_mana(self, tempo):
        if tempo > (self.manaTime + self.manaGenerationCooldown):
            self.manaTime = tempo

            odds = random.randint(1,10)
            if odds > 4: self.spawn_mana(type = 1)
            elif odds > 1: self.spawn_mana(type = 2)
            else: self.spawn_mana(type = 3)

    # Cria inimigos fora do campo de visão do player
    def spawn_enemy(self, tempo, type=1):
        distancia = 1000
        angle = random.uniform(0, 2 * math.pi)
        x = self.player.rect.centerx + distancia * math.cos(angle)
        y = self.player.rect.centery + distancia * math.sin(angle)

        #Cria os inimigos com base no tipo deles
        if type < 3:
            NewEnemy = Enemy_Tank((x, y), [self.attackable_sprites, self.camera, self.damagePlayer_sprites], (100 + tempo/3), self.Ogre_animation_images)
            self.enemies.append(NewEnemy)
        elif type == 3:
            NewEnemy = Enemy_Shooter((x, y), [self.attackable_sprites, self.camera, self.damagePlayer_sprites], (50 + tempo/3), self.Ghost_animation_images)
            self.enemies.append(NewEnemy)
        elif type == 4:
            NewEnemy = Boss((x, y), [self.attackable_sprites, self.camera, self.damagePlayer_sprites], self.Boss_animation_images)
            self.enemies.append(NewEnemy)

    # Cria mana fora do campo de visão do jogador
    def spawn_mana(self, type=1):
        distancia = 1000
        angle = random.uniform(0, 2 * math.pi)
        x = self.player.rect.centerx + distancia * math.cos(angle)
        y = self.player.rect.centery + distancia * math.sin(angle)

        #Cria os inimigos com base no tipo deles
        NewMana = Mana((x, y), [self.camera, self.item_sprites], type, image_path="assets/images/mana.png")
        self.manaCount +=1

    #Define quando o lazer será
    def Cast_Lazer(self, tempo):
        if tempo > (self.LazerTime + self.LazerBeamCooldown):
            self.LazerTime = tempo

            #Spawnando mais lazers se o nível estiver alto
            if self.Magics["Laser Beam"] > 6:
                for i in range (3):
                    lazer = LazerBeam(self.player.rect.center, [self.attack_sprites, self.camera], self.Magics["Laser Beam"], image_path="assets/images/LaserBeam.png")
                    lazer.CastMagic()
                self.projectiles.append(lazer)

            elif self.Magics["Laser Beam"] > 3:
                for i in range (2):
                    lazer = LazerBeam(self.player.rect.center, [self.attack_sprites, self.camera], self.Magics["Laser Beam"], image_path="assets/images/LaserBeam.png")
                    lazer.CastMagic()

                self.projectiles.append(lazer)
            else:
                lazer = LazerBeam(self.player.rect.center, [self.attack_sprites, self.camera], self.Magics["Laser Beam"], image_path="assets/images/LaserBeam.png")
                lazer.CastMagic()

# Cria o game e roda ele
if __name__ == "__main__":
    music_player = Music()
    game = Game()
    menu = Menu(game.screen)
    options = Options(game.screen)
    while True:
        result = menu.run()
        if result == 'play':
            music_player.set_volume(options.get_volume())
            music_player.background
            game.run()
        elif result == 'options':
            options.run()