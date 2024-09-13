import pygame

class Object(pygame.sprite.Sprite):
    def __init__(self, x, y, largura, altura, nome=None):
        super().__init__()
        self.__rect = pygame.Rect(x, y, largura, altura)
        self.__image = pygame.Surface((largura, altura), pygame.SRCALPHA)
        self.__largura = largura
        self.__altura = altura
        self.__nome = nome

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
        return self.__largura

    @width.setter
    def width(self, value):
        self.__largura = value

    @property
    def height(self):
        return self.__altura

    @height.setter
    def height(self, value):
        self.__altura = value

    @property
    def nome(self):
        return self.__nome

    @nome.setter
    def nome(self, value):
        self.__nome = value

    def draw(self, win, offset_x):
        win.blit(self.image, (self.rect.x - offset_x, self.rect.y))