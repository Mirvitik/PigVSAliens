import pygame
import os
import sys


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


class Alien(pygame.sprite.Sprite):
    image = load_image('alien3.jpg')

    def __init__(self, group, x, y, cell_size):
        super().__init__(group)
        Alien.image = pygame.transform.scale(Alien.image, (64, 64))
        self.image = Alien.image
        self.rect = self.image.get_rect()
        self.rect.x = cell_size * x
        self.rect.y = cell_size * y
        self.x = x
        self.y = y
