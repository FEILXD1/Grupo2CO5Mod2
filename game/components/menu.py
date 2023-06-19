import pygame, sys
import pygame.mixer
import random

from game.components.button import Button
from game.components.game import Game
from game.utils.constants import BG, SCREEN, ICON, TITLE
from game.utils.text import FONT_STYLE

pygame.init()

pygame.display.set_icon(ICON)
pygame.display.set_caption("The Adventurer's Journey")


def get_font(size):
    return pygame.font.Font(FONT_STYLE, size)


def wrap_text(text, font, max_width):
    words = text.split(" ")
    lines = []
    current_line = ""

    for word in words:
        if font.size(current_line + " " + word)[0] <= max_width:
            current_line += " " + word
        else:
            lines.append(current_line.lstrip())
            current_line = word

    lines.append(current_line.lstrip())
    return lines


def play():
    while True:
        PLAY_MOUSE_POS = pygame.mouse.get_pos()
        game = Game()
        game.execute()


def options():
    while True:
        OPTIONS_MOUSE_POS = pygame.mouse.get_pos()
        SCREEN.blit(BG, (0, 0))

        OPTIONS_TEXT = "Luis quería ser astronauta, pero nunca pudo. Cuando los alienígenas atacaron la Tierra, se ofreció para defenderla en el espacio. Luchó con valor y sacrificó su vida al estrellar su nave contra la nave enemiga más grande. Su acción cambió el destino de la batalla y salvó al planeta. Murió como un héroe y su sueño se cumplió."
        OPTIONS_LINES = wrap_text(OPTIONS_TEXT, get_font(13), 800)
        OPTIONS_Y = 80
        for line in OPTIONS_LINES:
            OPTIONS_LINE_TEXT = get_font(15).render(line, True, "White")
            OPTIONS_LINE_RECT = OPTIONS_LINE_TEXT.get_rect(center=(SCREEN.get_width() // 2, OPTIONS_Y))
            SCREEN.blit(OPTIONS_LINE_TEXT, OPTIONS_LINE_RECT)
            OPTIONS_Y += OPTIONS_LINE_TEXT.get_height() + 5

        OPTIONS_BACK = Button(image=None, pos=(463, 400),
                              text_input="BACK", font=get_font(20), base_color="White", hovering_color="Green")

        OPTIONS_BACK.changeColor(OPTIONS_MOUSE_POS)
        OPTIONS_BACK.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if OPTIONS_BACK.checkForInput(OPTIONS_MOUSE_POS):
                    main_menu()

        pygame.display.update()


def main_menu():
    while True:
        SCREEN.blit(BG, (0, 0))

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = get_font(35).render("SPACE SHITP", True, "#b68f40")
        MENU_RECT = MENU_TEXT.get_rect(center=(463, 70))

        PLAY_BUTTON = Button(image=pygame.image.load("game/assets/Options Rect.png"), pos=(463, 150),
                             text_input="PLAY", font=get_font(25), base_color="#d7fcd4", hovering_color="Green")
        OPTIONS_BUTTON = Button(image=pygame.image.load("game/assets/Options Rect.png"), pos=(463, 230),
                                text_input="History", font=get_font(25), base_color="#d7fcd4",
                                hovering_color="Green")  # uso del nombre spaceshipt
        QUIT_BUTTON = Button(image=pygame.image.load("game/assets/Options Rect.png"), pos=(463, 310),
                             text_input="QUIT", font=get_font(25), base_color="#d7fcd4", hovering_color="Green")

        SCREEN.blit(MENU_TEXT, MENU_RECT)

        for button in [PLAY_BUTTON, OPTIONS_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # es para utilizar el menu de acuerdo lo deseado por player
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    play()
                if OPTIONS_BUTTON.checkForInput(MENU_MOUSE_POS):
                    options()
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()
