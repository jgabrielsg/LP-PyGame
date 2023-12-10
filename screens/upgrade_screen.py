import pygame
from button import Button
import sys
from config import SCREEN_WIDHT, SCREEN_HEIGHT

class UpradeScreen:
    def __init__(self, screen):
        self.screen = screen
        self.running = True

        # Botão aqui
        self.OPTION_1 = Button(image=None, pos=(720, 260), 
                                  text_input="texto", font=pygame.font.Font(None, 75), base_color="Black", hovering_color="White")
        
        self.OPTION_2 = Button(image=None, pos=(720, 440), 
                                  text_input="texto", font=pygame.font.Font(None, 75), base_color="Black", hovering_color="White")
        
        self.OPTION_3 = Button(image=None, pos=(720, 620), 
                                  text_input="texto", font=pygame.font.Font(None, 75), base_color="Black", hovering_color="White")

        self.background_image = pygame.image.load("assets/images/upgrade_background.jpg")
        self.background_image = pygame.transform.scale(self.background_image, (SCREEN_WIDHT, SCREEN_HEIGHT))

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if self.OPTION_1.checkForInput(pygame.mouse.get_pos()):
                    return self.OPTION_1.get_text()
                if self.OPTION_2.checkForInput(pygame.mouse.get_pos()):
                    return self.OPTION_2.get_text()
                if self.OPTION_3.checkForInput(pygame.mouse.get_pos()):
                    return self.OPTION_3.get_text()

    def update(self):
        self.MOUSE_POS = pygame.mouse.get_pos()
        self.OPTION_1.changeColor(self.MOUSE_POS)
        self.OPTION_1.update(self.screen)

        self.OPTION_2.changeColor(self.MOUSE_POS)
        self.OPTION_2.update(self.screen)

        self.OPTION_3.changeColor(self.MOUSE_POS)
        self.OPTION_3.update(self.screen)

    def render(self):
        # Limpa a tela
        self.screen.blit(self.background_image, (0, 0))

        # Desenha o texto das opções
        OPTIONS_TEXT = pygame.font.Font(None, 45).render("Choose one powerup.", True, "Black")
        OPTIONS_RECT = OPTIONS_TEXT.get_rect(center=(640, 100))
        self.screen.blit(OPTIONS_TEXT, OPTIONS_RECT)

        # Desenha o botão e o texto do botão
        self.screen.blit(self.OPTION_1.image, self.OPTION_1.rect)
        self.screen.blit(self.OPTION_1.text, self.OPTION_1.text_rect)
        self.screen.blit(self.OPTION_2.image, self.OPTION_2.rect)
        self.screen.blit(self.OPTION_2.text, self.OPTION_2.text_rect)
        self.screen.blit(self.OPTION_3.image, self.OPTION_3.rect)
        self.screen.blit(self.OPTION_3.text, self.OPTION_3.text_rect)

        pygame.display.flip()  # Atualiza a tela

    def run(self, offset, option1, option2, option3):

        self.OPTION_1.set_text(option1)
        self.OPTION_2.set_text(option2)
        self.OPTION_3.set_text(option3)

        clock = pygame.time.Clock()

        while self.running:
            result = self.events()
            if result: return result
            self.update()
            self.render()

            # Limita a taxa de quadros (FPS)
            clock.tick(60)

            # Atualiza a tela
            pygame.display.flip()

        pygame.quit()
        sys.exit()
