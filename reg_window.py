import sys

import pygame as pg
import sqlite3
import pygame
import pygame_gui
from pygame.locals import *

pg.init()
screen = pg.display.set_mode((640, 480))
COLOR_INACTIVE = pg.Color('darkgreen')
COLOR_ACTIVE = pg.Color('green')
WHITE = (255, 255, 255)
FONT = pg.font.Font(None, 32)
db = sqlite3.connect("data.db")
sql = db.cursor()
sql.execute("""CREATE TABLE IF NOT EXISTS "users" (
    "username"  TEXT,
    "password"  TEXT)""")
db.commit()
font = pygame.font.Font(None, 20)


class InputBox:

    def __init__(self, x, y, w, h, text=''):
        self.rect = pg.Rect(x, y, w, h)
        self.color = COLOR_INACTIVE
        self.text = text
        self.txt_surface = FONT.render(text, True, self.color)
        self.active = False
        self.te = ''
        self.text_surface = font.render(self.te, True, COLOR_ACTIVE)

    def handle_event(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            # If the user clicked on the input_box rect.
            if self.rect.collidepoint(event.pos):
                # Toggle the active variable.
                self.active = not self.active
            else:
                self.active = False
            # Change the current color of the input box.
            self.color = COLOR_ACTIVE if self.active else COLOR_INACTIVE
        if event.type == pg.KEYDOWN:
            if self.active:
                if event.key == pg.K_RETURN:
                    print(self.text)
                    self.text = ''
                elif event.key == pg.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                # Re-render the text.
                self.txt_surface = FONT.render(self.text, True, self.color)

    def update(self):
        # Resize the box if the text is too long.
        width = max(200, self.txt_surface.get_width() + 10)
        self.rect.w = width

    def draw_box(self, screen):
        # Blit the text.
        screen.blit(self.txt_surface, (self.rect.x + 5, self.rect.y + 5))
        # Blit the rect.
        pg.draw.rect(screen, self.color, self.rect, 2)

    def reg(self, username, password):
        sql.execute(f"SELECT username, password FROM users WHERE username = '{username}' AND password = '{password}'")

        if sql.fetchone() is None:
            sql.execute(f"INSERT INTO users VALUES (?,?)", (username, password))
            db.commit()
            self.te = 'You have registered'
            self.text_surface = font.render(self.te, True, COLOR_ACTIVE)
        else:
            self.te = 'Такая запись уже существует'
            self.text_surface = font.render(self.te, True, COLOR_ACTIVE)

            # for i in sql.execute('SELECT * FROM users'):
            #     print(i)

    def login(self, username, password):
        a = sql.execute(
            f"SELECT username, password FROM users WHERE username = '{username}' AND password = '{password}'")
        db.commit()
        if not a.fetchone():
            print("Нет такой записи")
            return False
        else:
            print('Welcome')
            return True

    def draw(self, surface):
        # Изменение цвета кнопки при наведении мыши
        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            pygame.draw.rect(surface, COLOR_ACTIVE, self.rect)
        else:
            pygame.draw.rect(surface, self.color, self.rect)

        # Отображение текста на кнопке
        text_surface = font.render(self.text, True, WHITE)
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)

    def is_clicked(self):
        mouse_click = pygame.mouse.get_pressed()
        if mouse_click[0] and self.rect.collidepoint(pygame.mouse.get_pos()):
            return True
        return False

    def t(self):
        print(1)

    def get_te(self):
        return self.te


def reg_window():
    ter = InputBox
    clock = pg.time.Clock()
    input_box1 = InputBox(200, 130, 140, 32)
    input_box2 = InputBox(200, 200, 140, 32)
    text_surface1 = font.render('Имя:', True, COLOR_ACTIVE)
    text_rect1 = text_surface1.get_rect(center=(150, 145))
    text_surface2 = font.render('Пароль:', True, COLOR_ACTIVE)
    text_rect2 = text_surface2.get_rect(center=(150, 215))
    button = InputBox(150, 280, 140, 40, "Войти")
    button1 = InputBox(300, 280, 140, 40, "Зарегистрироваться")
    input_boxes = [input_box1, input_box2]
    text_surface = font.render(input_box1.get_te(), True, COLOR_ACTIVE)
    text_rect = text_surface.get_rect(center=(300, 350))
    done = False
    pr = True

    while not done:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                sys.exit()
            for box in input_boxes:
                box.handle_event(event)
            if button.is_clicked():
                if button.login(input_box1.text, input_box2.text):
                    done = True
            if button1.is_clicked():
                button1.reg(input_box1.text, input_box2.text)
        for box in input_boxes:
            box.update()

        screen.fill((30, 30, 30))
        for box in input_boxes:
            box.draw_box(screen)
        screen.blit(text_surface, text_rect)
        screen.blit(text_surface2, text_rect2)
        screen.blit(text_surface1, text_rect1)
        button.draw(screen)
        button1.draw(screen)
        pg.display.flip()
        clock.tick(30)


# if __name__ == '__main__':
#     main()
#     pg.quit()
