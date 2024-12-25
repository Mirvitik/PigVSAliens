from hero import Hero
from alien import Alien
import os
import sys
import pygame

size = width, height = 500, 500
screen = pygame.display.set_mode(size)


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


class Cell(pygame.sprite.Sprite):
    image = load_image('grass.png')

    def __init__(self, group, x, y):
        super().__init__(group)
        Cell.image = pygame.transform.scale(Cell.image, (64, 64))
        self.cell_image = Cell.image
        self.rect = self.cell_image.get_rect()
        self.rect.x = x
        self.rect.y = y


class Board:
    def __init__(self, screen, group):
        super().__init__()
        self.cell_size = 50
        self.width_pix = screen.get_width()
        self.height_pix = screen.get_height()
        self.width = self.width_pix // self.cell_size
        self.height = self.height_pix // self.cell_size
        self.board = [[0] * self.width for _ in range(self.height)]
        self.all_sprites = group

    def render(self):
        for y in range(self.height):
            for x in range(self.width):
                Cell(self.all_sprites, x * self.cell_size, y * self.cell_size)
                if self.board[y][x] == 1:
                    Hero(self.all_sprites, x, y, self.cell_size)
                elif self.board[y][x] == 2:
                    Alien(self.all_sprites, x, y, self.cell_size)

    def where_hero(self):
        for y in range(self.height):
            for x in range(self.width):
                if self.board[y][x] == 1:
                    return x, y
