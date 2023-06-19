import pygame
import pygame.mixer
import random
from game.components.menu import main_menu
from game.components.spaceshitp import Spaceship
from game.components.enemies.enemy_manager import EnemyManager
from game.components.power_ups.power_up_manager import PowerUpManager
from game.utils.constants import TITLE, ICON, SCREEN_HEIGHT, SCREEN_WIDTH, BG, FPS
from game.utils.text import draw_message_component


class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption(TITLE)
        pygame.display.set_icon(ICON)
        self.display = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.playing = False
        self.running = False
        self.high_score = 0
        self.current_score = 0
        self.death_count = 0
        self.game_speed = 0
        self.background_y = 0
        self.player = Spaceship()  # adventure
        self.enemy_manager = EnemyManager()  # obstacule
        self.power_up_manager = PowerUpManager()
        self.music_list = [
            r'game/assets/sounds/doctor-who-lost-in-space-remix-mp3cut.mp3',
            r'game/assets/sounds/spaceunicorn.mp3'
        ]
        pygame.mixer.music.load(random.choice(self.music_list))
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(0.2)

    def execute(self):
        self.playing = True
        while self.playing:
            if not self.running:
                if self.death_count == 0:
                    self.run()
                else:
                    self.draw_restart_message()
                pygame.display.update()
                pygame.display.flip()
                self.handle_events_on_menu()  # controla eventos e el menu
        pygame.display.quit()
        pygame.quit()

    def show_initial_menu(self):
        self.display.blit(BG, (0, 0))
        if self.death_count >= 1:
            self.draw_restart_message()  # inicia eventos en el menu
        pygame.display.update()
        pygame.display.flip()
        self.handle_events_on_menu()

    def draw_restart_message(self):
        draw_message_component(
            "Press any key to restart the game",  # presionar tecla
            self.display,
            y_center=(SCREEN_HEIGHT // 2)
        )
        draw_message_component(
            f"HIGH SCORE: {int(self.high_score)}",  # da el emnsaje de mejor puntuacion
            self.display,
            y_center=(SCREEN_HEIGHT // 2) - 150
        )
        draw_message_component(
            f"LAST SCORE: {int(self.current_score)}",
            self.display,  # puntaje anterior
            y_center=(SCREEN_HEIGHT // 2) - 100
        )
        draw_message_component(
            f"DEATHS: {int(self.death_count)}",
            self.display,  # numero de muertes
            y_center=(SCREEN_HEIGHT // 2) - 50
        )
        draw_message_component(
            "Press ESC to menu",
            self.display,  # te manda el menu principal a terminar el juego
            y_center=(SCREEN_HEIGHT // 2) + 200
        )

    def handle_events_on_menu(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.player.run = False
                self.running = False
                self.playing = False  # controlador de eventos
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:

                    main_menu()
                else:
                    self.run()

    def run(self):
        self.running = True
        self.player.run = True
        # self.enemy_manager.reset_enemy()
        self.power_up_manager.reset_power_ups()
        self.game_speed = 15  # controlador decuando comienza el juego
        self.current_score = 0
        while self.running:
            self.events()
            self.update()
            self.draw()

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.player.run = False  # controlador del boton de salida
                self.running = False
                self.playing = False

    def update(self):
        user_input = pygame.key.get_pressed()
        self.player.update(user_input)
        self.enemy_manager.update(self)  ##controlador de actualizacion de los stacks
        self.update_current_score()
        self.power_up_manager.update(self.current_score, self.game_speed, self.player)

    def update_current_score(self):
        self.current_score += 1
        if self.high_score == 0 or self.high_score < self.current_score:
            self.high_score = self.current_score  # comparacion en puntuaje
        if self.current_score % 100 == 0:
            self.game_speed += 0.5
        elif self.player.has_power_up and self.player.rotten_rayo_active and not self.player.power_up_applied:
            self.game_speed += 5  # aplicacion del aumento en la velocidad
            self.player.power_up_applied = True

    def draw(self):
        self.clock.tick(FPS)
        self.draw_background()
        self.player.draw(self.display)
        self.enemy_manager.draw(self.display)

        if self.running:  # verifica si el juego se esta ejecutado
            self.draw_score()
            self.draw_power_up_time()

        self.power_up_manager.draw(self.display)
        pygame.display.update()
        pygame.display.flip()

    def draw_score(self):
        high_score_message = "HIGH SCORE: " + str(int(self.high_score))
        score_message = "SCORE: " + str(int(self.current_score))
        game_speed_massage = "SPEED: " + str(int(self.game_speed))
        draw_message_component(
            f'{high_score_message}',
            self.display,
            x_center=750,
            y_center=50
        )  # controlador del mensaje en panatalla
        draw_message_component(
            f'{score_message}',
            self.display,
            x_center=730,
            y_center=80
        )
        draw_message_component(
            f'{game_speed_massage}',
            self.display,
            x_center=750,
            y_center=110
        )

    def draw_power_up_time(self):
        if self.player.has_power_up:
            time_to_show = round((self.player.power_up_time - pygame.time.get_ticks()) / 1000, 2)
            if time_to_show >= 0:
                draw_message_component(
                    f"Power up enable for {time_to_show} seconds",  # controlador del tiempo de uso del poder
                    self.display,
                    font_size=16,
                    x_center=300,
                    y_center=40
                )
            else:
                self.player.has_power_up = False
