import pygame
import sys

from characters.player import Player
from characters.pokemon import Pokemon

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

        # Game objects
        self.player = Player(SCREEN_WIDHT/2, SCREEN_HEIGHT/2, 48, 64, image_path="assets/images/player.png")
        self.blocks = [Block(0, 0, 64, 800, image_path="assets/images/wall.png"),  # Bloco vermelho
                    Block(0, SCREEN_HEIGHT-64, 1200, 64, image_path="assets/images/wall.png"), # o verde
                    Block(SCREEN_WIDHT-64, 0, 64, 800, image_path="assets/images/wall.png"), # o amarelo
                    Block(0, 0, 576, 64, image_path="assets/images/wall.png"), 
                    Block(640, 0, 640, 64, image_path="assets/images/wall.png")] 
        
        self.pokemons = [Pokemon("assets/images/pokemon.png","Shrek","Lama", 0, 1, 5, 10, 20, 100, 300, 300, True),
                         Pokemon("assets/images/applejack.png", "Applejack", "Terra", 0, 1, 30, 20, 30, 80, 600, 300, True)]

        self.background = pygame.image.load('assets/images/woodtile.png').convert()

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

        # Atualiza a posição do jogador
        self.player.update_position(self.blocks)

        # Atualiza os Pokémons
        for pokemon in self.pokemons:
            pokemon.update(dt, self.screen, SCREEN_WIDHT, SCREEN_HEIGHT)

            # Verifica a colisão com os Pokémons
            if self.is_collision(self.player.rect, pokemon.rect) and pokemon.visible:
                print(f"Você colidiu com {pokemon.nome}!")


    # Checa colisão entre objetos (Como player e paredes)
    def is_collision(self, obj1, obj2):
        return obj1.colliderect(obj2)


    # Desenhas as coisas na tela
    def render(self):
        # Limpa a tela
        self.screen.fill((0, 0, 0))

        # Preenche a tela com a imagem de fundo
        for i in range(0, SCREEN_WIDHT, 64):
            for j in range(0, SCREEN_HEIGHT, 64):
                self.screen.blit(self.background, (i, j))        

        # Desenha o jogador
        self.player.draw(self.screen)

        # Desenha os blocos
        for block in self.blocks:
            block.draw(self.screen)

        # Desenha os Pokémons
        for pokemon in self.pokemons:
            if pokemon.visible:
                self.screen.blit(pokemon.image, pokemon.rect)


    # Chama todas as funções de game
    def run(self):
        clock = pygame.time.Clock()

        while self.running:
            self.events()
            self.update()
            self.render()

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


