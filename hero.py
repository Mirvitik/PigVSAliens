# файл со спрайтом игрока и игрока для последнего уровня

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


class Hero(pygame.sprite.Sprite):
    image = load_image('pig.png')
    cell_size = 50

    def __init__(self, group, x, y, cell_size, sheet, column, col):
        super().__init__(group)
        Hero.image = pygame.transform.scale(Hero.image, (50, 50))
        self.hero_image = Hero.image
        self.rect = self.hero_image.get_rect()
        self.rect.x = cell_size * x
        self.rect.y = cell_size * y
        self.x = x
        self.y = y
        self.frames = []
        columns = 9
        rows = 4
        self.col = col
        self.cut_sheet(sheet, columns, rows)
        self.cur_frame = column
        match self.col:
            case (0, -1):
                self.image = self.frames[self.cur_frame + 27]
            case (0, 1):
                self.image = self.frames[self.cur_frame]
            case (1, 0):
                self.image = self.frames[self.cur_frame + 18]
            case _:
                self.image = self.frames[self.cur_frame + 9]

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(self.x * self.cell_size, self.y * self.cell_size, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))


class HeroMiniGame(pygame.sprite.Sprite):
    def __init__(self, group, sheet, x, y, nap):
        super().__init__(group)
        self.napravlenie = nap
        self.frames = []
        self.sheet = sheet
        self.x, self.y = x, y
        columns, rows = 9, 4
        self.cut_sheet(sheet, columns, rows)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.mask = pygame.mask.from_surface(self.image)

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        match self.napravlenie:
            case 'right':
                j = 2
            case 'left':
                j = 1
            case 'down':
                j = 0
            case 'up':
                j = 3
        for i in range(columns - 6):
            frame_location = (self.rect.w * i, self.rect.h * j)
            self.frames.append(sheet.subsurface(pygame.Rect(
                frame_location, self.rect.size)))

    def update(self):
        self.cur_frame = (self.cur_frame + 1) % len(self.frames)
        self.image = self.frames[self.cur_frame]
