import pygame
from button import Button
import sys

class UpradeScreen:
    def __init__(self, screen):
        self.screen = screen
        self.running = True

        # Botão aqui
        self.OPTION_1 = Button(image=None, pos=(640, 300), 
                                  text_input="texto", font=pygame.font.Font(None, 75), base_color="Black", hovering_color="Green")
        
        self.OPTION_2 = Button(image=None, pos=(640, 400), 
                                  text_input="texto", font=pygame.font.Font(None, 75), base_color="Black", hovering_color="Green")
        
        self.OPTION_3 = Button(image=None, pos=(640, 500), 
                                  text_input="texto", font=pygame.font.Font(None, 75), base_color="Black", hovering_color="Green")

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if self.OPTION_1.checkForInput(pygame.mouse.get_pos()):
                    return "Option_1"
                if self.OPTION_2.checkForInput(pygame.mouse.get_pos()):
                    return "Option_2"
                if self.OPTION_3.checkForInput(pygame.mouse.get_pos()):
                    return "Option_3"

    def update(self):
        pass  # Atualize o estado do menu aqui, se necessário

    def render(self):
        # Limpa a tela
        self.screen.fill((255, 255, 255))  # Preenche a tela com branco

        # Desenha o texto das opções
        OPTIONS_TEXT = pygame.font.Font(None, 45).render("Choose one powerup.", True, "Black")
        OPTIONS_RECT = OPTIONS_TEXT.get_rect(center=(640, 240))
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
