import pygame

from game.utils.constants import RAYO
from game.components.power_ups.power_up import PowerUp

#da velocidad a los a la nave
class RottenRayo(PowerUp):
    def __init__(self):
        self.sprite_index = 0
        super().__init__(RAYO, self.sprite_index)

    def draw(self, display):
        self.image = self.images[self.sprite_index % len(self.images)].convert_alpha()
        self.enemy_mask = pygame.mask.from_surface(self.image)
        self.mask = self.enemy_mask.to_surface(unsetcolor=(0, 0, 0, 0))
        display.blit(self.image, self.rect)
        self.sprite_index += 1