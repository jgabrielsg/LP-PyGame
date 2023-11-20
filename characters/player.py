import pygame

class Player(pygame.Rect):
    def __init__(self, x, y, width, height, image_path=None):
        super().__init__(x, y, width, height)
        self.color = (0, 128, 255)  # Azul
        self.speed = 5
        self.image = pygame.image.load(image_path).convert_alpha()
        self.rect = pygame.Rect(x, y, width, height)

    def update_position(self, blocks):
        keys = pygame.key.get_pressed()

        dx, dy = 0, 0
        if keys[pygame.K_LEFT]:
            dx -= self.speed
        if keys[pygame.K_RIGHT]:
            dx += self.speed
        if keys[pygame.K_UP]:
            dy -= self.speed
        if keys[pygame.K_DOWN]:
            dy += self.speed

        # Atualiza a posição do retângulo de colisão para o movimento horizontal
        self.rect.x += dx

        # Verificar colisões com os blocos para o movimento horizontal
        for block in blocks:
            if self.rect.colliderect(block):
                # Se houver colisão, não atualize a posição horizontal
                self.rect.x -= dx
                dx = 0

        # Atualiza a posição do retângulo de colisão para o movimento vertical
        self.rect.y += dy

        # Verificar colisões com os blocos para o movimento vertical
        for block in blocks:
            if self.rect.colliderect(block):
                # Se houver colisão, não atualize a posição vertical
                self.rect.y -= dy
                dy = 0

        # Se não houver colisão, atualize a posição
        self.x += dx
        self.y += dy



    def draw(self, screen):
        screen.blit(self.image, self)
