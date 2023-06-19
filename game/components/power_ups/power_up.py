import random
import pygame

from pygame.sprite import Sprite
from game.utils.constants import SCREEN_WIDTH,SCREEN_HEIGHT


class PowerUp(Sprite):
    def __init__(self, images, index):
        self.images = images
        self.index = index
        self.image = self.images[self.index].convert_alpha()
        self.rect = self.image.get_rect()
        self.enemy_mask = pygame.mask.from_surface(self.image)
        self.mask = self.enemy_mask.to_surface()
        self.rect.x = SCREEN_WIDTH + random.randint(800, 1000)
        self.rect.y = random.randint(SCREEN_WIDTH //2 ,SCREEN_HEIGHT)
        self.start_time = 0
        self.duration = random.randint(3, 5)

    def update(self, game_speed, power_ups):
        self.rect.x -= game_speed
        if self.rect.x < self.rect.width:
            power_ups.pop()

    def draw(self, display):
        self.image = self.images[self.index].convert_alpha()#para crear pixeles de una imagen
        self.enemy_mask = pygame.mask.from_surface(self.image)#para darle los pixeles exactos de la imagen
        self.mask = self.enemy_mask.to_surface(unsetcolor=(0, 0, 0, 0))#metodo para poner un mascara en cima o en este caso un color
        display.blit(self.image, (self.rect.x, self.rect.y))#dibuja