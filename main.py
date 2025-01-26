import time
from board import Board
from hero import Hero
import pygame
from reg_window import reg_window
import sys

'''я узнал о бибилиотеке pygame_gui из видеоурока
https://lms.yandex.ru/courses/1180/groups/23622/lessons/6992/materials/20704
установи её через pip
'''
import pygame_gui

nick = None  # переменная с ником игрока


def start_window(screen):
    global nick
    font = pygame.font.Font(None, 50)
    font2 = pygame.font.Font(None, 25)
    text = font.render('Свин против пришельцев', True, pygame.Color('green'))
    manager = pygame_gui.UIManager((width, height))
    start_button = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((180, 275), (110, 50)),
        text='Начать игру',
        manager=manager
    )
    exit_button = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((180, 325), (110, 50)),
        text='Выйти из игры',
        manager=manager
    )
    nickname_field = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((180, 225), (110, 50)),
                                                         manager=manager)
    text_help = font2.render('Введите свой никнейм, нажмите Enter и начните игру', True, pygame.Color('green'))
    screen.blit(text, (25, 25))
    screen.blit(text_help, (25, 175))
    text_x = width // 2 - text.get_width() // 2
    text_y = 25
    text_w = text.get_width()
    text_h = text.get_height()
    pygame.draw.rect(screen, (0, 255, 0), (text_x - 10, text_y - 10,
                                           text_w + 20, text_h + 20), 5)
    running = True
    pygame.display.flip()
    color = pygame.Color('green')
    while running:
        time_delta = clock.tick(60) / 1000
        for event in pygame.event.get():
            if event.type == pygame.QUIT or pygame.key.get_pressed()[pygame.K_ESCAPE]:
                dialog = pygame_gui.windows.UIConfirmationDialog(rect=pygame.Rect((200, 200), (300, 200)),
                                                                 manager=manager,
                                                                 window_title='Подтверждение',
                                                                 action_long_desc='Вы уверены, что хотите выйти?',
                                                                 action_short_name='OK',
                                                                 blocking=True)
            if event.type == pygame_gui.UI_TEXT_ENTRY_FINISHED:
                nick = event.text
            if event.type == pygame_gui.UI_CONFIRMATION_DIALOG_CONFIRMED:
                sys.exit()
            if event.type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == start_button:
                    if nick is None or ''.join(nick.split()) == '':
                        color = pygame.Color('red')
                    else:
                        running = False
                        break
                if event.ui_element == exit_button:
                    dialog = pygame_gui.windows.UIConfirmationDialog(rect=pygame.Rect((200, 200), (300, 200)),
                                                                     manager=manager,
                                                                     window_title='Подтверждение',
                                                                     action_long_desc='Вы уверены, что хотите выйти?',
                                                                     action_short_name='OK',
                                                                     blocking=True)
            manager.process_events(event)
        screen.fill(pygame.Color('black'))
        screen.blit(text, (25, 25))
        text_help = font2.render('Введите свой никнейм, нажмите Enter и начните игру', True, color)
        screen.blit(text_help, (25, 175))
        pygame.draw.rect(screen, (0, 255, 0), (text_x - 10, text_y - 10,
                                               text_w + 20, text_h + 20), 5)
        manager.update(time_delta)
        manager.draw_ui(screen)
        pygame.display.flip()


def lose(screen):  # функция выводит экран проигрыша
    screen.fill(pygame.Color('black'))
    font = pygame.font.Font(None, 50)
    font2 = pygame.font.Font(None, 25)
    text = font.render('Вы проиграли', True, pygame.Color('red'))
    text_esc = font2.render('Нажмите клавишу "esc" для выхода из игры', True, pygame.Color('red'))
    screen.blit(text, (25, 25))
    screen.blit(text_esc, (50, 175))
    pygame.display.flip()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or pygame.key.get_pressed()[pygame.K_ESCAPE]:
                sys.exit()
            if pygame.key.get_pressed()[pygame.K_a]:
                return


def main(event, bomb=False):
    if event.type == pygame.QUIT:
        pygame.quit()
        sys.exit()
    if event.type == pygame.KEYDOWN and event.key == pygame.K_w:
        try:  # если игрок захочет нажать на кнопки, когда пришелец занял его клетку
            hero_x, hero_y = board.where_hero()
        except TypeError:
            lose(screen)
            return
        if hero_y != 0 and board.board[hero_y - 1][hero_x] == 0:
            if board.board[hero_y - 1][hero_x] != 2:
                board.board[hero_y][hero_x] = 0
                board.board[hero_y - 1][hero_x] = 1
            else:
                lose(screen)
    if event.type == pygame.KEYDOWN and event.key == pygame.K_a:
        hero_x, hero_y = board.where_hero()
        if hero_x != 0 and board.board[hero_y][hero_x - 1] == 0:
            if board.board[hero_y][hero_x - 1] != 2:
                board.board[hero_y][hero_x] = 0
                board.board[hero_y][hero_x - 1] = 1
            else:
                lose(screen)
    if event.type == pygame.KEYDOWN and event.key == pygame.K_s:
        hero_x, hero_y = board.where_hero()
        if hero_y != board.height - 1 and board.board[hero_y + 1][hero_x] == 0:
            if board.board[hero_y + 1][hero_x] != 2:
                board.board[hero_y][hero_x] = 0
                board.board[hero_y + 1][hero_x] = 1
            else:
                lose(screen)
    if event.type == pygame.KEYDOWN and event.key == pygame.K_d:
        hero_x, hero_y = board.where_hero()
        if hero_x != board.width - 1 and board.board[hero_y][hero_x + 1] == 0:
            if board.board[hero_y][hero_x + 1] != 2:
                board.board[hero_y][hero_x] = 0
                board.board[hero_y][hero_x + 1] = 1
            else:
                lose(screen)

    # нужно оптимизировать
    if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and bomb:
        hero_x, hero_y = board.where_hero()
        boom0(hero_x, hero_y)

        last_hero_x = hero_x
        # задержка 2 секунды
        start_time = time.time()
        while time.time() - start_time < 2:
            for event in pygame.event.get():
                main(event)
        boom1(last_hero_x, hero_y)

        # задержка 1 секунда
        start_time = time.time()
        while time.time() - start_time < 1:
            for event in pygame.event.get():
                main(event)

        boom2()
    screen.fill((255, 255, 255))
    board.render()
    all_sprites.draw(screen)
    clock.tick(fps)
    pygame.display.flip()


def boom0(hero_x, hero_y):
    if hero_x < board.width - 1 and board.board[hero_y][hero_x + 1] == 0:
        board.board[hero_y][hero_x + 1] = 4


def boom1(hero_x, hero_y):
    if hero_x < board.width - 1 and board.board[hero_y][hero_x + 1] == 4:
        board.board[hero_y][hero_x + 1] = 5
        if hero_y - 1 >= 0:
            if board.board[hero_y - 1][hero_x + 1] == 6:
                board.board[hero_y - 1][hero_x + 1] = 7
            else:
                board.board[hero_y - 1][hero_x + 1] = 5
        if hero_y - 2 >= 0:
            if board.board[hero_y - 2][hero_x + 1] == 6:
                board.board[hero_y - 2][hero_x + 1] = 7
            else:
                board.board[hero_y - 2][hero_x + 1] = 5
        if hero_y + 1 <= board.height - 1:
            if board.board[hero_y + 1][hero_x + 1] == 6:
                board.board[hero_y + 1][hero_x + 1] = 7
            else:
                board.board[hero_y + 1][hero_x + 1] = 5
        if hero_y + 2 <= board.height - 1:
            if board.board[hero_y + 2][hero_x + 1] == 6:
                board.board[hero_y + 2][hero_x + 1] = 7
            else:
                board.board[hero_y + 2][hero_x + 1] = 5

        if hero_x + 2 <= board.width - 1:
            if board.board[hero_y][hero_x + 2] == 6:
                board.board[hero_y][hero_x + 2] = 7
            else:
                board.board[hero_y][hero_x + 2] = 5
        if hero_x + 3 <= board.width - 1:
            if board.board[hero_y][hero_x + 3] == 6:
                board.board[hero_y][hero_x + 3] = 7
            else:
                board.board[hero_y][hero_x + 3] = 5
        board.board[hero_y][hero_x] = 5
        if hero_x - 1 >= 0:
            if board.board[hero_y][hero_x - 1] == 6:
                board.board[hero_y][hero_x - 1] = 7
            else:
                board.board[hero_y][hero_x - 1] = 5

    screen.fill((255, 255, 255))
    board.render()
    all_sprites.draw(screen)
    clock.tick(fps)
    pygame.display.flip()


def boom2():
    for y in range(board.height):
        for x in range(board.width):
            if board.board[y][x] == 5:
                board.board[y][x] = 0


size = width, height = 500, 500
screen = pygame.display.set_mode(size)
pygame.display.set_caption('Свин против пришельцев')
fps = 165
clock = pygame.time.Clock()
pygame.init()
screen.fill(pygame.Color('Black'))
reg_window()
screen.fill((0, 0, 0))
start_window(screen)  # показываем стортовое окно

all_sprites = pygame.sprite.Group()
levels = [1, 2, 3, 4, 5, 6, 7]
lvl = 0
board = Board(screen, all_sprites, lvl=levels[lvl])
hero = Hero(all_sprites, board.where_hero()[0], board.where_hero()[1], 50)
size = (550, 500)
screen = pygame.display.set_mode(size)

ALIEN_EVENT = 30  # создаём событие того, что врагу надо переместиться
delay = 1000
pygame.time.set_timer(ALIEN_EVENT, delay)

running = True
new_lvl = False
while running:
    if not board.where_hero():
        lose(screen)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == ALIEN_EVENT:
            board.move_enemy()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                main(event, bomb=True)
            else:
                hero_x, hero_y = board.where_hero()
                exit_xy = board.where_exit()
                if exit_xy and ((event.key == pygame.K_d and (hero_x + 1, hero_y) == exit_xy) or
                                (event.key == pygame.K_s and (hero_x, hero_y + 1) == exit_xy) or
                                (event.key == pygame.K_a and (hero_x - 1, hero_y) == exit_xy) or
                                (event.key == pygame.K_w and (hero_x, hero_y - 1) == exit_xy)):
                    new_lvl = True
                else:
                    main(event)
    screen.fill((255, 255, 255))
    board.render()
    all_sprites.draw(screen)
    if new_lvl:
        lvl += 1
        board = Board(screen, all_sprites, lvl=levels[lvl])
        new_lvl = False
    pygame.display.flip()
pygame.quit()
sys.exit()
