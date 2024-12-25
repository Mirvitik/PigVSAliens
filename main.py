from board import Board
from hero import Hero
import pygame
import sys


def lose(screen):  # функция выводит экран проигрыша
    screen.fill(pygame.Color('black'))
    font = pygame.font.Font(None, 50)
    font2 = pygame.font.Font(None, 25)
    text = font.render('Вы проиграли', True, pygame.Color('red'))
    text_play = font2.render('Нажмите "A" для продолжения игры', True, pygame.Color('red'))
    text_esc = font2.render('Нажмите клавишу "esc" для выхода из игры', True, pygame.Color('red'))
    screen.blit(text, (25, 25))
    screen.blit(text_play, (50, 150))
    screen.blit(text_esc, (50, 175))
    pygame.display.flip()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or pygame.key.get_pressed()[pygame.K_ESCAPE]:
                sys.exit()
            if pygame.key.get_pressed()[pygame.K_a]:
                return


size = width, height = 500, 500
screen = pygame.display.set_mode(size)
pygame.display.set_caption('Свин против пришельцев')
fps = 165
clock = pygame.time.Clock()
pygame.init()
screen.fill(pygame.Color('Black'))
font = pygame.font.Font(None, 50)
font2 = pygame.font.Font(None, 25)
text = font.render('Свин против пришельцев', True, pygame.Color('green'))
text_play = font2.render('Нажмите "A" для начала игры', True, pygame.Color('green'))
text_esc = font2.render('Нажмите клавишу "esc" для выхода из игры', True, pygame.Color('green'))
screen.blit(text, (25, 25))
screen.blit(text_play, (50, 150))
screen.blit(text_esc, (50, 175))
text_x = width // 2 - text.get_width() // 2
text_y = 25
text_w = text.get_width()
text_h = text.get_height()
pygame.draw.rect(screen, (0, 255, 0), (text_x - 10, text_y - 10,
                                       text_w + 20, text_h + 20), 5)
pygame.display.flip()
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT or pygame.key.get_pressed()[pygame.K_ESCAPE]:
            sys.exit()
        if pygame.key.get_pressed()[pygame.K_a]:
            running = False
            break
all_sprites = pygame.sprite.Group()
board = Board(screen, all_sprites)
board.board[0][0] = 1
board.board[1][1] = 2
board.board[4][5] = 2
hero = Hero(all_sprites, 0, 0, 50)
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_w:
            hero_x, hero_y = board.where_hero()
            if hero_y != 0:
                if board.board[hero_y - 1][hero_x] != 2:
                    board.board[hero_y][hero_x] = 0
                    board.board[hero_y - 1][hero_x] = 1
                else:
                    lose(screen)
        if event.type == pygame.KEYDOWN and event.key == pygame.K_a:
            hero_x, hero_y = board.where_hero()
            if hero_x != 0:
                if board.board[hero_y][hero_x - 1] != 2:
                    board.board[hero_y][hero_x] = 0
                    board.board[hero_y][hero_x - 1] = 1
                else:
                    lose(screen)
        if event.type == pygame.KEYDOWN and event.key == pygame.K_s:
            hero_x, hero_y = board.where_hero()
            if hero_y != board.height - 1:
                if board.board[hero_y + 1][hero_x] != 2:
                    board.board[hero_y][hero_x] = 0
                    board.board[hero_y + 1][hero_x] = 1
                else:
                    lose(screen)
        if event.type == pygame.KEYDOWN and event.key == pygame.K_d:
            hero_x, hero_y = board.where_hero()
            if hero_x != board.width - 1:
                if board.board[hero_y][hero_x + 1] != 2:
                    board.board[hero_y][hero_x] = 0
                    board.board[hero_y][hero_x + 1] = 1
                else:
                    lose(screen)
    screen.fill((255, 255, 255))
    board.render()
    all_sprites.draw(screen)
    clock.tick(fps)
    pygame.display.flip()
pygame.quit()
