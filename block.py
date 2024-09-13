import pygame
from object import Object
from utils import Utils

class Block(Object):
    
    def __init__(self, x, y, tamanho):
        super().__init__(x, y, tamanho, tamanho)
        block = Utils.get_block(tamanho)
        self.image.blit(block, (0, 0))
        self.mask = pygame.mask.from_surface(self.image)