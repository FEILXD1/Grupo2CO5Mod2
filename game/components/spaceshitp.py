import pygame
from pygame.sprite import Sprite
from game.components.Balas.bullet import Bullet
from game.utils.constants import SCREEN_HEIGHT, SCREEN_WIDTH, SPACESHIP
class Spaceship(Sprite):
    SHIP_WIDTH = 40
    SHIP_HEIGHT = 60
    X_POS = (SCREEN_WIDTH // 2) - SHIP_WIDTH
    Y_POS = 500
    SHIP_SPEED = 10

    def __init__(self):
        self.image = SPACESHIP
        self.image = pygame.transform.scale(self.image,(self.SHIP_WIDTH, self.SHIP_HEIGHT))
        self.rect = self.image.get_rect()
        self.rect.x = self.X_POS
        self.rect.y = self.Y_POS
        self.type = 'player'
        self.power_up_applied = False
        self.shield_active = False
        self.sword_active = False
        self.rotten_rayo_active = False
        self.pew = pygame.mixer.Sound('game/assets/sounds/pew-pew-lame-sound-effect.mp3')
        self.setup_state()#estado inicial

    def setup_state(self):
        self.has_power_up = False
        self.show_text = False
        self.shield_time_up = 0

    def update(self, user_input, game):

        if (user_input[pygame.K_LEFT] or user_input[pygame.K_d]):
            self.move_left()
        elif (user_input[pygame.K_RIGHT]or user_input[pygame.K_a]):
            self.move_right()
        elif (user_input[pygame.K_UP]or user_input[pygame.K_w]):
            self.move_up()
        elif (user_input[pygame.K_DOWN]or user_input[pygame.K_s]):
            self.move_down()
        elif user_input[pygame.K_SPACE]:
            self.shoot(game)

    def move_left(self):
        self.rect.x -= self.SHIP_SPEED
        if self.rect.left < 0:
            self.rect.x = SCREEN_WIDTH - self.SHIP_WIDTH

    def move_right(self):
        self.rect.x += self.SHIP_SPEED
        if self.rect.right >= SCREEN_WIDTH - self.SHIP_WIDTH:
            self.rect.x = 0

    def move_up(self):
        if self.rect.y > SCREEN_HEIGHT // 2:
            self.rect.y -= self.SHIP_SPEED

    def move_down(self):
        if self.rect.y < SCREEN_HEIGHT - 70:
            self.rect.y +=  self.SHIP_SPEED   

    def draw(self, screen):
        screen.blit(self.image, (self.rect.x, self.rect.y))

    def shoot(self, game):
        bullet = Bullet(self)
        game.bullet_manager.add_bullet(bullet)
        self.pew.play()
        self.pew.set_volume(0.06)