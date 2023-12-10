import pygame

class Mana(pygame.sprite.Sprite):
    def __init__(self, pos, groups, type, image_path, size = (100,100)):
        super().__init__(groups)
        self.sprite_type = 'xp'
        self.size = size

        original_image = pygame.image.load(image_path).convert_alpha()
        self.image = pygame.transform.scale(original_image, self.size)

        self.rect = self.image.get_rect(center=pos)

        if type == 1:
            self.xp = 35
        elif type == 2: 
            self.xp = 50
        else:
            self.xp = 100
