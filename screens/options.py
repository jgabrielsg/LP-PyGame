import pygame
from button import Button
import sys
from config import SCREEN_HEIGHT, SCREEN_WIDHT

class Options:
    def __init__(self, screen):
        self.screen = screen
        self.running = True
        self.volume = 50

        # Botão aqui
        self.BACK_BUTTON = Button(image=None, pos=(640, 460),
                                  text_input="Main Menu", font=pygame.font.Font(None, 75), base_color="White",
                                  hovering_color="Yellow")

        self.INCREASE_VOLUME_BUTTON = Button(image=None, pos=(540, 360),
                                            text_input="+", font=pygame.font.Font(None, 50), base_color="White",
                                            hovering_color="Yellow")

        self.DECREASE_VOLUME_BUTTON = Button(image=None, pos=(740, 360),
                                            text_input="-", font=pygame.font.Font(None, 50), base_color="White",
                                            hovering_color="Yellow")
        
        self.background_image = pygame.image.load("assets/images/background_options.jpg")
        self.background_image = pygame.transform.scale(self.background_image, (SCREEN_WIDHT, SCREEN_HEIGHT))

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if self.BACK_BUTTON.checkForInput(pygame.mouse.get_pos()):
                    return "main_menu"
                elif self.INCREASE_VOLUME_BUTTON.checkForInput(pygame.mouse.get_pos()):
                    self.volume = min(100, self.volume + 10)  # Aumenta o volume em 10, limitado a 100
                elif self.DECREASE_VOLUME_BUTTON.checkForInput(pygame.mouse.get_pos()):
                    self.volume = max(0, self.volume - 10)  # Diminui o volume em 10, limitado a 0

    def update(self):
        self.MOUSE_POS = pygame.mouse.get_pos()
        self.BACK_BUTTON.changeColor(self.MOUSE_POS)
        self.BACK_BUTTON.update(self.screen)

        self.INCREASE_VOLUME_BUTTON.changeColor(self.MOUSE_POS)
        self.INCREASE_VOLUME_BUTTON.update(self.screen)

        self.DECREASE_VOLUME_BUTTON.changeColor(self.MOUSE_POS)
        self.DECREASE_VOLUME_BUTTON.update(self.screen)

    def render(self):
        # Desenha a imagem de fundo do menu
        self.screen.blit(self.background_image, (0, 0))

        # Desenha o texto das opções
        OPTIONS_TEXT = pygame.font.Font(None, 45).render("CONFIGURATIONS:", True, "White")
        OPTIONS_RECT = OPTIONS_TEXT.get_rect(center=(640, 260))
        self.screen.blit(OPTIONS_TEXT, OPTIONS_RECT)

        # Desenha o botão e o texto do botão
        self.screen.blit(self.BACK_BUTTON.image, self.BACK_BUTTON.rect)
        self.screen.blit(self.BACK_BUTTON.text, self.BACK_BUTTON.text_rect)

        # Desenha os botões de aumento e diminuição do volume
        self.screen.blit(self.INCREASE_VOLUME_BUTTON.image, self.INCREASE_VOLUME_BUTTON.rect)
        self.screen.blit(self.INCREASE_VOLUME_BUTTON.text, self.INCREASE_VOLUME_BUTTON.text_rect)

        self.screen.blit(self.DECREASE_VOLUME_BUTTON.image, self.DECREASE_VOLUME_BUTTON.rect)
        self.screen.blit(self.DECREASE_VOLUME_BUTTON.text, self.DECREASE_VOLUME_BUTTON.text_rect)

        # Exibe o valor do volume na tela
        VOLUME_TEXT = pygame.font.Font(None, 36).render(f"Volume: {self.volume}%", True, "White")
        VOLUME_RECT = VOLUME_TEXT.get_rect(center=(640, 360))
        self.screen.blit(VOLUME_TEXT, VOLUME_RECT)

        pygame.display.flip()  # Atualiza a tela

    def run(self):
        clock = pygame.time.Clock()

        while self.running:
            result = self.events()
            if result == 'main_menu':
                return 'main_menu'
            self.update()
            self.render()

            # Limita a taxa de quadros (FPS)
            clock.tick(60)

            # Atualiza a tela
            pygame.display.flip()

        pygame.quit()
        sys.exit()

    def get_volume(self):
        return self.volume