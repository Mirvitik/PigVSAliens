from board import Board
from hero import Hero
import pygame


size = width, height = 500, 500
screen = pygame.display.set_mode(size)
pygame.display.set_caption('Свин против пришельцев')
fps = 165
clock = pygame.time.Clock()
pygame.init()
all_sprites = pygame.sprite.Group()
board = Board(screen, all_sprites)
board.board[0][0] = 1
hero = Hero(all_sprites, 0, 0, 50)
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_w:
            hero_x, hero_y = board.where_hero()
            if hero_y != 0:
                board.board[hero_y][hero_x] = 0
                board.board[hero_y - 1][hero_x] = 1
        if event.type == pygame.KEYDOWN and event.key == pygame.K_a:
            hero_x, hero_y = board.where_hero()
            if hero_x != 0:
                board.board[hero_y][hero_x] = 0
                board.board[hero_y][hero_x - 1] = 1
        if event.type == pygame.KEYDOWN and event.key == pygame.K_s:
            hero_x, hero_y = board.where_hero()
            if hero_y != board.height - 1:
                board.board[hero_y][hero_x] = 0
                board.board[hero_y + 1][hero_x] = 1
        if event.type == pygame.KEYDOWN and event.key == pygame.K_d:
            hero_x, hero_y = board.where_hero()
            if hero_x != board.width - 1:
                board.board[hero_y][hero_x] = 0
                board.board[hero_y][hero_x + 1] = 1
    screen.fill((255, 255, 255))
    board.render()
    all_sprites.draw(screen)
    clock.tick(fps)
    pygame.display.flip()
pygame.quit()
