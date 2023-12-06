import pygame

class Mana(pygame.sprite.Sprite):
    def __init__(self, pos, groups, type, image_path):
        super().__init__(groups)
        self.sprite_type = 'xp'

        self.image = pygame.image.load(image_path).convert_alpha()

        self.rect = self.image.get_rect(center = pos)

        if type == 1:
            self.xp = 10
        elif type == 2: 
            self.xp = 25
        else:
            self.xp = 50
