import random

import pygame

from game.components.power_ups.Rotten_rayo import RottenRayo

from game.components.power_ups.shiled import Shield


class PowerUpManager:
    def __init__(self):
        self.power_ups = [] #lista de aparicion
        self.when_appears = 0 #tasa de aparicion


    def generate_power_up(self, score):
        if len(self.power_ups) == 0 and self.when_appears == score: #poderes = 0 y tasa de aparicion = puntaje
            self.when_appears += random.randint(200, 300)
            power_up_type = random.choice([Sword, Shield, RottenRayo])#paderes
            self.power_ups.append(power_up_type())


    def update(self, score, game_speed, player):
        self.generate_power_up(score)
        for power_up in self.power_ups:
            power_up.update(game_speed, self.power_ups)
            offset = (power_up.rect.x - player.rect.x), (power_up.rect.y - player.rect.y)
            if player.spaceshitp_mask.overlap(power_up.enemy_mask, offset):
                power_up.start_time = pygame.time.get_ticks()#duracion del poder
                player.has_power_up = True
                player.power_up_time = power_up.start_time + (power_up.duration * 1000)
                #lo que activa el poder
                if isinstance(power_up, Sword):
                    player.sword_active = True
                    player.shield_active = False
                    player.rotten_apple_active = False
                elif isinstance(power_up, Shield):
                    player.shield_active = True
                    player.sword_active = False
                    player.rotten_apple_active = False
                elif isinstance(power_up, RottenRayo):
                    player.rotten_apple_active = True
                    player.shield_active = True
                    player.sword_active = False

                self.power_ups.remove(power_up)#remueve el poder


    def draw(self, screen):
        for power_up in self.power_ups:
            power_up.draw(screen)


    def reset_power_ups(self):
        self.power_ups = []
        self.when_appears = random.randint(200, 300)