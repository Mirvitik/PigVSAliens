import time
from board import Board, Lava, Door_mingame
from hero import Hero, load_image, HeroMiniGame
import pygame
from reg_window import reg_window
import sys
import pygame_gui
import json

nick = None  # переменная с ником игрока


def win(screen):  # num-переменная со счётом игрока
    global time_start, nickname
    screen.fill(pygame.Color('black'))
    font = pygame.font.Font(None, 50)
    font2 = pygame.font.Font(None, 25)
    text = font.render('ВЫ ВЫЙГРАЛИ!', True, pygame.Color('yellow'))
    t = round(time.time() - time_start, 2)
    text_num = font2.render(f'ВАШ СЧЁТ: {t} секунд', True, pygame.Color('yellow'))
    with open('data/top.json') as file:
        data = json.load(file)
        print(data)
    print(data)
    data[nickname] = t
    with open('data/top.json', 'w') as file:
        json.dump(data, file, ensure_ascii=False)
    with open('data/top.json') as file:
        data = json.load(file)
    data = [[i, data[i]] for i in sorted(data, key=lambda x: data[x])][:10]
    print(data)
    text_top = font2.render(f'ТОП 10 ИГРОКОВ:\n {"\n".join([' '.join([str(j[0]), str(j[1])]) for j in data])}', True,
                            pygame.Color('yellow'))
    screen.blit(text, (25, 25))
    screen.blit(text_num, (50, 175))
    screen.blit(text_top, (50, 200))
    pygame.display.flip()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or pygame.key.get_pressed()[pygame.K_ESCAPE]:
                sys.exit()


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
    text_help = font2.render('Перемещайтесь по WASD, когда начнёте игру\nПробел-поставить мину', True, pygame.Color('green'))
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
            if event.type == pygame_gui.UI_CONFIRMATION_DIALOG_CONFIRMED:
                sys.exit()
            if event.type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == start_button:
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
        text_help = font2.render('Перемещайтесь по WASD, когда начнёте игру\nПробел-поставить мину', True, color)
        screen.blit(text_help, (25, 175))
        pygame.draw.rect(screen, (0, 255, 0), (text_x - 10, text_y - 10,
                                               text_w + 20, text_h + 20), 5)
        manager.update(time_delta)
        manager.draw_ui(screen)
        pygame.display.flip()


def lose(screen):  # функция выводит экран проигрыша
    global all_sprites, levels, lvl, board, size, hero, gamesound
    screen.fill(pygame.Color('black'))
    font = pygame.font.Font(None, 50)
    font2 = pygame.font.Font(None, 25)
    text = font.render('Вы проиграли', True, pygame.Color('red'))
    text_esc = font2.render('Нажмите клавишу "esc" для выхода из игры', True, pygame.Color('red'))
    text_f = font2.render('Нажмите клавишу "f" для перезапуска игры', True, pygame.Color('red'))
    screen.blit(text, (25, 25))
    screen.blit(text_esc, (50, 175))
    screen.blit(text_f, (50, 200))
    pygame.display.flip()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or pygame.key.get_pressed()[pygame.K_ESCAPE]:
                sys.exit()
            if pygame.key.get_pressed()[pygame.K_f]:
                all_sprites = pygame.sprite.Group()
                levels = [1, 2, 3, 4, 5, 6, 7]
                lvl = 0
                gamesound.stop()
                gamesound.play(loops=-1)
                if lvl == 5:
                    minigame()
                else:
                    board = Board(screen, all_sprites, lvl=levels[lvl])
                    hero = Hero(all_sprites, board.where_hero()[0], board.where_hero()[1], 50, load_image('pigs.png'),
                                0, 0)
                    size = (len(board.board[0]) * 50, len(board.board) * 50)
                    screen = pygame.display.set_mode(size)

                    ALIEN_EVENT = 30  # создаём событие того, что врагу надо переместиться
                    delay = 1000
                    pygame.time.set_timer(ALIEN_EVENT, delay)
                return


def minigame():
    global all_sprites, levels, lvl, board, size, hero
    for el in all_sprites:
        el.kill()
    screen.fill(pygame.Color('Gray'))
    all_sprites = pygame.sprite.Group()
    lavasps = pygame.sprite.Group()
    h = HeroMiniGame(all_sprites, load_image("pigs.png"), 0, 0, 'right')
    for i in range(5):
        Lava(lavasps, 50 * i, 100)
    for i in range(6, 15):
        Lava(lavasps, 50 * i, 100)
    for i in range(1, 15):
        Lava(lavasps, 50 * i, 200)
    for i in range(14):
        Lava(lavasps, 50 * i, 300)
    door = Door_mingame(all_sprites, 50, 350)
    running = True
    while running:
        screen.fill(pygame.Color('Gray'))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            for lava in lavasps:
                if pygame.sprite.collide_mask(h, lava):
                    running = False
            if pygame.sprite.collide_mask(h, door):
                win(screen)
                running = False
            if pygame.key.get_pressed()[pygame.K_d]:
                h_old = h
                h = HeroMiniGame(all_sprites, load_image("pigs.png"), min(screen.get_width() - 50, h_old.x + 5),
                                 h_old.y, 'right')
                h_old.kill()
            if pygame.key.get_pressed()[pygame.K_a]:
                h_old = h
                h = HeroMiniGame(all_sprites, load_image("pigs.png"), max(h_old.x - 5, 0), h_old.y, 'left')
                h_old.kill()
            if pygame.key.get_pressed()[pygame.K_w]:
                h_old = h
                h = HeroMiniGame(all_sprites, load_image("pigs.png"), h_old.x, max(h_old.y - 5, 0), 'up')
                h_old.kill()
            if pygame.key.get_pressed()[pygame.K_s]:
                h_old = h
                h = HeroMiniGame(all_sprites, load_image("pigs.png"), h_old.x,
                                 min(h_old.y + 5, screen.get_height() - 50), 'down')
                h_old.kill()
        all_sprites.update()
        lavasps.update()
        lavasps.draw(screen)
        all_sprites.draw(screen)
        pygame.display.flip()
    lose(screen)


def main(event, bomb=False):
    if event.type == pygame.QUIT:
        pygame.quit()
        sys.exit()
    if lvl >= 6:
        win(screen)
    if lvl == 5:
        minigame()
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
                if event.type == ALIEN_EVENT:
                    board.move_enemy()
                elif event.type == pygame.KEYDOWN:
                    main(event)
        boom1(last_hero_x, hero_y)

        # задержка 1 секунда
        start_time = time.time()
        while time.time() - start_time < 1:
            for event in pygame.event.get():
                if event.type == ALIEN_EVENT:
                    board.move_enemy()
                elif event.type == pygame.KEYDOWN:
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
        screen.fill((255, 255, 255))
        board.render()
        all_sprites.draw(screen)
        clock.tick(fps)
        pygame.display.flip()


def boom1(hero_x, hero_y):
    if hero_x < board.width - 1 and board.board[hero_y][hero_x + 1] == 4:
        board.board[hero_y][hero_x + 1] = 5
        if hero_y - 1 >= 0:
            if board.board[hero_y - 1][hero_x + 1] == 6:
                board.board[hero_y - 1][hero_x + 1] = 7
            elif board.board[hero_y - 1][hero_x + 1] != 7:
                board.board[hero_y - 1][hero_x + 1] = 5
        if hero_y - 2 >= 0:
            if board.board[hero_y - 2][hero_x + 1] == 6:
                board.board[hero_y - 2][hero_x + 1] = 7
            elif board.board[hero_y - 2][hero_x + 1] != 7:
                board.board[hero_y - 2][hero_x + 1] = 5
        if hero_y + 1 <= board.height - 1:
            if board.board[hero_y + 1][hero_x + 1] == 6:
                board.board[hero_y + 1][hero_x + 1] = 7
            elif board.board[hero_y + 1][hero_x + 1] != 7:
                board.board[hero_y + 1][hero_x + 1] = 5
        if hero_y + 2 <= board.height - 1:
            if board.board[hero_y + 2][hero_x + 1] == 6:
                board.board[hero_y + 2][hero_x + 1] = 7
            elif board.board[hero_y + 2][hero_x + 1] != 7:
                board.board[hero_y + 2][hero_x + 1] = 5

        if hero_x + 2 <= board.width - 1:
            if board.board[hero_y][hero_x + 2] == 6:
                board.board[hero_y][hero_x + 2] = 7
            elif board.board[hero_y][hero_x + 2] != 7:
                board.board[hero_y][hero_x + 2] = 5
        if hero_x + 3 <= board.width - 1:
            if board.board[hero_y][hero_x + 3] == 6:
                board.board[hero_y][hero_x + 3] = 7
            elif board.board[hero_y][hero_x + 3] != 7:
                board.board[hero_y][hero_x + 3] = 5
        board.board[hero_y][hero_x] = 5
        if hero_x - 1 >= 0:
            if board.board[hero_y][hero_x - 1] == 6:
                board.board[hero_y][hero_x - 1] = 7
            elif board.board[hero_y][hero_x - 1] != 7:
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
nickname = reg_window()
screen.fill((0, 0, 0))
start_window(screen)  # показываем стортовое окно
time_start = time.time()
all_sprites = pygame.sprite.Group()
levels = [1, 2, 3, 4, 5, 6, 7]
lvl = 0
board = Board(screen, all_sprites, lvl=levels[lvl])
hero = Hero(all_sprites, board.where_hero()[0], board.where_hero()[1], 50, load_image('pigs.png'), 0, 0)
size = (len(board.board[0]) * 50, len(board.board) * 50)
screen = pygame.display.set_mode(size)

ALIEN_EVENT = 30  # создаём событие того, что врагу надо переместиться
delay = 1000
pygame.time.set_timer(ALIEN_EVENT, delay)
gamesound = pygame.mixer.Sound('data/song.mp3')  # загрузка еще музыки
gamesound.set_volume(1)
gamesound.play(loops=-1)
start_time = time.time()
running = True
new_lvl = False
while running:
    if not board.where_hero():
        lose(screen)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if lvl == 5:
            minigame()
        if lvl >= 6:
            win(screen)
        if event.type == ALIEN_EVENT:
            board.move_enemy()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                try:
                    main(event, bomb=True)
                except TypeError:
                    lose(screen)
            else:
                try:
                    hero_x, hero_y = board.where_hero()
                except TypeError:
                    lose(screen)
                exit_xy = board.where_exit()
                if exit_xy and ((event.key == pygame.K_d and any(bool((hero_x + 1, hero_y) == xy) for xy in exit_xy)) or
                                (event.key == pygame.K_s and any(bool((hero_x, hero_y + 1) == xy) for xy in exit_xy)) or
                                (event.key == pygame.K_a and any(bool((hero_x - 1, hero_y) == xy) for xy in exit_xy)) or
                                (event.key == pygame.K_w and any(bool((hero_x, hero_y - 1) == xy) for xy in exit_xy))):
                    new_lvl = True
                else:
                    main(event)
    screen.fill((255, 255, 255))
    board.render()
    all_sprites.draw(screen)
    if new_lvl:
        lvl += 1
        if lvl == 5:
            minigame()
        else:
            board = Board(screen, all_sprites, lvl=levels[lvl])
            size = (len(board.board[0]) * 50, len(board.board) * 50)
            screen = pygame.display.set_mode(size)
        new_lvl = False
    pygame.display.flip()
pygame.quit()
sys.exit()
