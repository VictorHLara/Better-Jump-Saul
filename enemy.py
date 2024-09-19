import pygame
from character import Character

class Enemy(Character):
    def __init__(self, x, y, width, height, speed, sprites):
        super().__init__(x, y, width, height, sprites)
        self.__speed = speed
        self.__direction = "left"

    @property
    def speed(self):
        return self.__speed

    @speed.setter
    def speed(self, value):
        self.__speed = value

    @property
    def direction(self):
        return self.__direction

    @direction.setter
    def direction(self, value):
        self.__direction = value

    def move(self):
        if self.direction == "left":
            self.move_left(self.speed)
        else:
            self.move_right(self.speed)

    def reverse_direction(self):
        self.direction = "right" if self.direction == "left" else "left"

    def update(self, player, objects, enemies):
        if self.is_alive:
            self.move()
            self.update_sprite()
            self.check_collisions(player, objects, enemies)

    def check_collisions(self, player, objects):
        if pygame.sprite.collide_mask(self, player):
            if player.rect.bottom <= self.rect.top + 30:
                self.is_alive = False
            else:
                pass

        for obj in objects:
            if pygame.sprite.collide_mask(self, obj):
                self.reverse_direction()
                break