import pygame

class CameraGroup(pygame.sprite.Group):
    def __init__(self, groundpath = None):
        super().__init__()
        self.display_surface = pygame.display.get_surface()

        # camera offset
        self.offset = pygame.math.Vector2()
        self.half_w = self.display_surface.get_size()[0] // 2 # // é divisão arredondada para nmr inteiro :0
        self.half_h = self.display_surface.get_size()[1] // 2

        # Ground
        self.ground_surf = pygame.image.load(groundpath).convert_alpha()
        self.ground_rect = self.ground_surf.get_rect(topleft = (0,0))

        # Map boundaries
        self.map_width = self.ground_rect.width
        self.map_height = self.ground_rect.height

    def center_target_camera(self, player):
        self.offset.x = max(0, min(player.rect.centerx - self.half_w, self.map_width - self.display_surface.get_width()))
        self.offset.y = max(0, min(player.rect.centery - self.half_h, self.map_height - self.display_surface.get_height()))

    # Desenha os sprites ordenados pela sua posição Y, então dá uma impressão de 3D
    def custom_draw(self):

        #Desenha o chão antes
        ground_offset = self.ground_rect.topleft - self.offset
        self.display_surface.blit(self.ground_surf, ground_offset)

        for sprite in sorted(self.sprites(), key = lambda sprite: sprite.rect.centery):
            offset_pos = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image, offset_pos)