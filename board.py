from hero import Hero
from alien import Alien
import os
import sys
import pygame
from stone import Stone
from bomb import Bomb
from boom import Boom
from door import Door


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


def load_level(filename):
    filename = "data/" + filename
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]
    in_strings = list(map(lambda x: [i for i in x.ljust(max(map(len, level_map)), '.')], level_map))
    out = []
    for el in in_strings:
        new_el = []
        for value in el:
            new_value = 0
            if value == '@':
                new_value = 1
            elif value == 'e':
                new_value = 2
            elif value == '+':
                new_value = 3
            elif value == 'Q':
                new_value = 6
            new_el.append(new_value)
        out.append(new_el)
    return out


class Cell(pygame.sprite.Sprite):
    image = load_image('grass.png')

    def __init__(self, group, x, y):
        super().__init__(group)
        Cell.image = pygame.transform.scale(Cell.image, (64, 64))
        self.cell_image = Cell.image
        self.rect = self.cell_image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.mask = pygame.mask.from_surface(Cell.image)


class Lava(pygame.sprite.Sprite):
    image = load_image('lava.jpg')

    def __init__(self, group, x, y):
        super().__init__(group)
        Lava.image = pygame.transform.scale(Lava.image, (50, 50))
        self.lava_image = Lava.image
        self.rect = self.lava_image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.mask = pygame.mask.from_surface(Lava.image)


class Door_mingame(pygame.sprite.Sprite):
    image = load_image('door.png')

    def __init__(self, group, x, y):
        super().__init__(group)
        Door_mingame.image = pygame.transform.scale(Door_mingame.image, (50, 50))
        self.lava_image = Door_mingame.image
        self.rect = self.lava_image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.mask = pygame.mask.from_surface(Door_mingame.image)


class Board:
    def __init__(self, screen, group, lvl):
        super().__init__()
        self.cell_size = 50
        self.board = []
        self.board = load_level(f'lvl{lvl}.txt')
        self.lvl = lvl
        self.width = len(self.board[0])
        self.height = len(self.board)
        self.all_sprites = group
        self.cords = self.where_enemy()
        self.column, self.col = 0, 0
        self.posy = (0, 0)

    def render(self):
        for y in range(self.height):
            for x in range(self.width):
                Cell(self.all_sprites, x * self.cell_size, y * self.cell_size)
                if self.board[y][x] == 1:
                    self.column += 1
                    if self.column >= 3:
                        self.column = 0
                    if self.posy[0] - self.where_hero()[0] > 0:
                        self.col = (-1, 0)
                    if self.posy[0] - self.where_hero()[0] < 0:
                        self.col = (1, 0)
                    if self.posy[1] - self.where_hero()[1] > 0:
                        self.col = (0, -1)
                    if self.posy[1] - self.where_hero()[1] < 0:
                        self.col = (0, 1)
                    Hero(self.all_sprites, x, y, self.cell_size, load_image('pigs.png'), self.column, self.col)
                    self.posy = self.where_hero()
                elif self.board[y][x] == 2:
                    Alien(self.all_sprites, x, y, self.cell_size)
                elif self.board[y][x] == 3:
                    Stone(self.all_sprites, x, y, self.cell_size)
                elif self.board[y][x] == 4:
                    Bomb(self.all_sprites, x, y, self.cell_size)
                elif self.board[y][x] == 5:
                    Boom(self.all_sprites, x, y, self.cell_size)
                elif self.board[y][x] == 6:
                    Stone(self.all_sprites, x, y, self.cell_size)
                elif self.board[y][x] == 7:
                    Door(self.all_sprites, x, y, self.cell_size)

    def where_hero(self):
        for y in range(self.height):
            for x in range(self.width):
                if self.board[y][x] == 1:
                    return x, y
        return False

    def move_enemy(self):  # эта функция и все нижние отвечают за волновой алгоритм
        self.cords = self.where_enemy()
        for i in range(len(self.cords)):
            x, y = self.cords.pop(0)
            self.board[y][x] = 0
            next_pos = self.find_path_step((x, y), self.where_hero())
            self.board[next_pos[1]][next_pos[0]] = 2
            self.cords.append(next_pos)

    def find_path_step(self, start,
                       target):  # волновой алгоритм, находит ближайшую координату(не вдавайся в подробности, я сам
        # не очень его понял)
        if target is False:
            return start
        INF = 1000
        x, y = start
        distance = [[INF] * self.width for _ in range(self.height)]
        try:
            distance[x][y] = 0
        except Exception:
            return start
        distance[x][y] = 0
        prev = [[None] * self.width for _ in range(self.height)]  # хранит начальные клетки
        queue = [(x, y)]
        while queue:
            x, y = queue.pop(0)
            for dx, dy in (1, 0), (0, 1), (-1, 0), (0, -1):
                next_x, next_y = x + dx, y + dy
                if 0 <= next_x < self.width and 0 < next_y < self.height and \
                        self.is_free((next_x, next_y)) and distance[next_y][next_x] == INF:
                    distance[next_y][next_x] = distance[y][x] + 1
                    prev[next_y][next_x] = (x, y)
                    queue.append((next_x, next_y))
        x, y = target
        if distance[y][x] == INF or start == target:
            return start
        while prev[y][x] != start:
            if prev[y][x] is None:
                return start
            try:
                x, y = prev[y][x]
            except Exception:
                return start
        if self.board[y][x] == 3 or self.board[y][x] == 6 or self.board[y][x] == 7:
            return start
        return x, y

    def is_free(self, pos):
        if self.board[pos[1]][pos[0]] == 2:
            return False
        return True

    def where_enemy(self):
        out = []
        for y in range(self.height):
            for x in range(self.width):
                if self.board[y][x] == 2:
                    out.append((x, y))
        return out

    def where_exit(self):
        exits = []
        for y in range(self.height):
            for x in range(self.width):
                if self.board[y][x] == 7:
                    exits.append((x, y))
        return exits
