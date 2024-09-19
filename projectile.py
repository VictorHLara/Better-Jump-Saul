from object import Object
import pygame

class Projectile(Object):
    def __init__(self, x, y, direction, speed, image):
        super().__init__(x, y, image.get_width(), image.get_height())
        self.__image = image
        self.__rect = self.image.get_rect(topleft=(x, y))
        self.__speed = speed
        self.__direction = direction
        self.__mask = pygame.mask.from_surface(self.image)

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

    @property
    def mask(self):
        return self.__mask

    @mask.setter
    def mask(self, value):
        self.__mask = value

    def update(self):
        self.rect.x += self.speed * self.direction

        if self.rect.right < -2180 or self.rect.left > -1250:
            self.kill()

    def check_collision(self, player):
        if pygame.sprite.collide_mask(self, player):
            player.die()
            self.kill()