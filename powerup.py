import pygame
from object import Object
import os

class PowerUp(Object):
    def __init__(self, x, y, largura, altura, sprites):
        super().__init__(x, y, largura, altura)
        self.__sprites = sprites
        self.__image = sprites["idle_left"][0]
        self.__rect = self.image.get_rect()
        self.__rect.topleft = (x, y)
        self.__is_collected = False
        self.__collect_sound = pygame.mixer.Sound(os.path.join("assets", "sons", "powerup.wav"))

    @property
    def sprites(self):
        return self.__sprites

    @sprites.setter
    def sprites(self, value):
        self.__sprites = value

    @property
    def image(self):
        return self.__image

    @image.setter
    def image(self, value):
        self.__image = value

    @property
    def rect(self):
        return self.__rect

    @rect.setter
    def rect(self, value):
        self.__rect = value

    @property
    def rect(self):
        return self.__rect

    @rect.setter
    def rect(self, value):
        self.__rect = value

    @property
    def is_collected(self):
        return self.__is_collected

    @is_collected.setter
    def is_collected(self, value):
        self.__is_collected = value

    @property
    def collect_sound(self):
        return self.__collect_sound

    @collect_sound.setter
    def collect_sound(self, value):
        self.__collect_sound = value


    def update(self, player):
        if not self.is_collected:
            self.check_collisions(player)

    def check_collisions(self, player):
        if pygame.sprite.collide_mask(self, player):
            self.is_collected = True
            self.apply_effect(player)

    def draw(self, screen, offset_x):
        if not self.is_collected:
            screen.blit(self.image, (self.rect.x - offset_x, self.rect.y))

    def apply_effect(self, player):
        self.collect_sound.play()
        self.collect_sound.set_volume(1)
        player.double_jump_ability = True