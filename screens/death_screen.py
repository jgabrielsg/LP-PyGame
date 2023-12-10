import pygame
import sys
from button import Button 
from config import SCREEN_HEIGHT, SCREEN_WIDHT, get_font

class DeathScreen:
    def __init__(self, screen):
        self.screen = screen
        self.running = True

        self.MENU_TEXT = get_font(60).render(f"You survived: {0}", True, "#b68f40")

        self.PLAY_BUTTON = Button(image=pygame.image.load("assets/images/flop.png"), pos=(640, 450), 
                                  text_input="PLAY AGAIN", font=get_font(36), base_color="Black", hovering_color="White")
        self.QUIT_BUTTON = Button(image=pygame.image.load("assets/images/flop.png"), pos=(640, 600), 
                                  text_input="QUIT", font=get_font(36), base_color="Black", hovering_color="White")

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
                elif self.QUIT_BUTTON.checkForInput(pygame.mouse.get_pos()):
                    self.running = False
                    pygame.quit()
                    sys.exit()

    def update(self):
        self.MOUSE_POS = pygame.mouse.get_pos()
        self.PLAY_BUTTON.changeColor(self.MOUSE_POS)
        self.PLAY_BUTTON.update(self.screen)

        self.QUIT_BUTTON.changeColor(self.MOUSE_POS)
        self.QUIT_BUTTON.update(self.screen)

    def render(self):
        # Desenha a imagem de fundo do menu
        self.screen.blit(self.background_image, (0, 0))

        self.screen.blit(self.MENU_TEXT, (200, 130))

        # Desenha os botões e o texto dos botões
        for button in [self.PLAY_BUTTON, self.QUIT_BUTTON]:
            self.screen.blit(button.image, button.rect)
            self.screen.blit(button.text, button.text_rect)

        pygame.display.flip()  # Atualiza a tela


    def run(self, time_survived):
        clock = pygame.time.Clock()

        self.MENU_TEXT = get_font(40).render(f"You survived: {time_survived/1000:.2f} s", True, "#b68f40")

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