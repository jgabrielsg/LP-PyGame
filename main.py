import pygame
import sys
from random import randint

from characters.player import Player
from camera import CameraGroup
from arvore import Tree

from block import Block
from config import SCREEN_HEIGHT, SCREEN_WIDHT

from screens.main_menu import Menu
from screens.options import Options

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
        self.player = Player(initial_pos, self.camera, image_path="assets/images/player.png")

        self.trees = []

        for i in range(20):
            random_x = randint(0,1000)
            random_y = randint(0,1000)
            tree = Tree((random_x, random_y), self.camera, image_path='assets/images/wall.png')
            self.trees.append(tree)

        self.running = True

    # Aqui ficam os handlers de eventos
    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if self.PLAY_BUTTON.checkForInput(pygame.mouse.get_pos()):
                    return 'play'
                elif self.OPTIONS_BUTTON.checkForInput(pygame.mouse.get_pos()):
                    pass  # Adicione a lógica para abrir a tela de opções aqui
                elif self.QUIT_BUTTON.checkForInput(pygame.mouse.get_pos()):
                    self.running = False
                    pygame.quit()
                    sys.exit()


    # Qualquer atualização de posição ou animação ficam aqui.
    def update(self):
        dt = self.clock.tick(120) / 1000.0

        # Atualiza o player
        self.player.update()

        # Cuida da câmera
        self.camera.update()

        self.camera.center_target_camera(self.player)
        self.camera.custom_draw()  

    # Checa colisão entre objetos (Como player e paredes)
    def is_collision(self, obj1, obj2):
        return obj1.colliderect(obj2)

    # Desenhas as coisas na tela
    def render(self):
        # Limpa a tela
        self.screen.fill((0,0,0))

        # Preenche a tela com a imagem de fundo
        # for i in range(0, SCREEN_WIDHT, 64):
        #     for j in range(0, SCREEN_HEIGHT, 64):
        #         self.screen.blit(self.background, (i, j))      

        
    # Chama todas as funções de game
    def run(self):
        clock = pygame.time.Clock()

        while self.running:
            self.events()
            self.render()
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
            game.run()
        elif result == 'options':
            options.run()