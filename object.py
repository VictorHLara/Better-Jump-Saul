import pygame

class Object(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, name=None):
        super().__init__()
        self.__rect = pygame.Rect(x, y, width, height)
        self.__image = pygame.Surface((width, height), pygame.SRCALPHA)
        self.__width = width
        self.__height = height
        self.__name = name

    @property
    def rect(self):
        return self.__rect

    @rect.setter
    def rect(self, value):
        self.__rect = value

    @property
    def image(self):
        return self.__image

    @image.setter
    def image(self, value):
        self.__image = value

    @property
    def width(self):
        return self.__width

    @width.setter
    def width(self, value):
        self.__width = value

    @property
    def height(self):
        return self.__height

    @height.setter
    def height(self, value):
        self.__height = value

    @property
    def nome(self):
        return self.__name

    @nome.setter
    def nome(self, value):
        self.__name = value

    def draw(self, win, offset_x):
        win.blit(self.image, (self.rect.x - offset_x, self.rect.y))