import pygame
import sys
from button import Button  # Certifique-se de ter uma classe Button adequada
from config import SCREEN_HEIGHT, SCREEN_WIDHT, get_font

class Menu:
    def __init__(self, screen):
        self.screen = screen
        self.running = True

        # Crie os botões aqui
        self.PLAY_BUTTON = Button(image=pygame.image.load("assets/images/flop.png"), pos=(640, 250), 
                                  text_input="PLAY", font=get_font(36), base_color="Black", hovering_color="Green")
        self.OPTIONS_BUTTON = Button(image=pygame.image.load("assets/images/flop.png"), pos=(640, 400), 
                                     text_input="OPTIONS", font=get_font(36), base_color="Black", hovering_color="Green")
        self.QUIT_BUTTON = Button(image=pygame.image.load("assets/images/flop.png"), pos=(640, 550), 
                                  text_input="QUIT", font=get_font(36), base_color="Black", hovering_color="Green")

        self.background_image = pygame.image.load("assets/images/mapa.png")
        self.background_image = pygame.transform.scale(self.background_image, (SCREEN_WIDHT, SCREEN_HEIGHT))

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if self.PLAY_BUTTON.checkForInput(pygame.mouse.get_pos()):
                    return "play"
                elif self.OPTIONS_BUTTON.checkForInput(pygame.mouse.get_pos()):
                    return "options"
                elif self.QUIT_BUTTON.checkForInput(pygame.mouse.get_pos()):
                    self.running = False
                    pygame.quit()
                    sys.exit()

    def update(self):
        self.MOUSE_POS = pygame.mouse.get_pos()
        self.PLAY_BUTTON.changeColor(self.MOUSE_POS)
        self.PLAY_BUTTON.update(self.screen)

        self.OPTIONS_BUTTON.changeColor(self.MOUSE_POS)
        self.OPTIONS_BUTTON.update(self.screen)

        self.QUIT_BUTTON.changeColor(self.MOUSE_POS)
        self.QUIT_BUTTON.update(self.screen)

    def render(self):
        # Desenha a imagem de fundo do menu
        self.screen.blit(self.background_image, (0, 0))

        # Desenha os botões e o texto dos botões
        for button in [self.PLAY_BUTTON, self.OPTIONS_BUTTON, self.QUIT_BUTTON]:
            self.screen.blit(button.image, button.rect)
            self.screen.blit(button.text, button.text_rect)

        pygame.display.flip()  # Atualiza a tela


    def run(self):
        clock = pygame.time.Clock()

        while self.running:
            result = self.events()
            if result:
                return result
            self.update()
            self.render()

            # Limita a taxa de quadros (FPS)
            clock.tick(60)

            # Atualiza a tela
            pygame.display.flip()

        pygame.quit()
        sys.exit()