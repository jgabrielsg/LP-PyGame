import pygame
from button import Button
import sys


class Options:
    def __init__(self, screen):
        self.screen = screen
        self.running = True

        # Botão aqui
        self.BACK_BUTTON = Button(image=None, pos=(640, 460), 
                                  text_input="BACK", font=pygame.font.Font(None, 75), base_color="Black", hovering_color="Green")

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if self.BACK_BUTTON.checkForInput(pygame.mouse.get_pos()):
                    return "main_menu"

    def update(self):
        pass  # Atualize o estado do menu aqui, se necessário

    def render(self):
        # Limpa a tela
        self.screen.fill((255, 255, 255))  # Preenche a tela com branco

        # Desenha o texto das opções
        OPTIONS_TEXT = pygame.font.Font(None, 45).render("This is the OPTIONS screen.", True, "Black")
        OPTIONS_RECT = OPTIONS_TEXT.get_rect(center=(640, 260))
        self.screen.blit(OPTIONS_TEXT, OPTIONS_RECT)

        # Desenha o botão e o texto do botão
        self.screen.blit(self.BACK_BUTTON.image, self.BACK_BUTTON.rect)
        self.screen.blit(self.BACK_BUTTON.text, self.BACK_BUTTON.text_rect)

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
