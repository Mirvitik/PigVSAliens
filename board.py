import random

from hero import Hero
from alien import Alien
import os
import sys
import pygame
from stone import Stone
from bomb import Bomb
from boom import Boom

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
        self.board = []
        for y in range(self.height):
            self.board.append([])
            for x in range(self.width):
                self.board[y].append(random.choice([0, 0, 0, 0, 3]))
        self.all_sprites = group
        self.cords = [(1, 1), (5, 4)] # добавил список координат всех пришельцев

    def render(self):
        for y in range(self.height):
            for x in range(self.width):
                Cell(self.all_sprites, x * self.cell_size, y * self.cell_size)
                if self.board[y][x] == 1:
                    Hero(self.all_sprites, x, y, self.cell_size)
                elif self.board[y][x] == 2:
                    Alien(self.all_sprites, x, y, self.cell_size)
                elif self.board[y][x] == 3:
                    Stone(self.all_sprites, x, y, self.cell_size)
                elif self.board[y][x] == 4:
                    Bomb(self.all_sprites, x, y, self.cell_size)
                elif self.board[y][x] == 5:
                    Boom(self.all_sprites, x, y, self.cell_size)

    def where_hero(self):
        for y in range(self.height):
            for x in range(self.width):
                if self.board[y][x] == 1:
                    return x, y
        return False

    def move_enemy(self):  # эта функция и все нижние отвечают за волновой алгоритм
        for i in range(len(self.cords)):
            x, y = self.cords.pop(i)
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
            x, y = prev[y][x]
        return x, y

    def is_free(self, pos):
        if self.board[pos[1]][pos[0]] == 2:
            return False
        return True
