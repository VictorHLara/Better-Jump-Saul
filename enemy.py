import pygame
from character import Character

class Enemy(Character):
    def __init__(self, x, y, largura, altura, velocidade, sprites):
        super().__init__(x, y, largura, altura, sprites)
        self.__velocidade = velocidade
        self.__direcao = "left"

    @property
    def velocidade(self):
        return self.__velocidade

    @velocidade.setter
    def velocidade(self, value):
        self.__velocidade = value

    @property
    def direcao(self):
        return self.__direcao

    @direcao.setter
    def direcao(self, value):
        self.__direcao = value

    def move(self):
        if self.direcao == "left":
            self.move_left(self.velocidade)
        else:
            self.move_right(self.velocidade)

    def reverse_direction(self):
        self.direcao = "right" if self.direcao == "left" else "left"

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