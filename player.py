from character import Character
import pygame
import os

class Player(Character):
    def __init__(self, x, y, largura, altura, sprites):
        super().__init__(x, y, largura, altura, sprites)
        self.__pulo_contagem = 0
        self.__double_jump_ability = False
        self.__jump_sound = pygame.mixer.Sound(os.path.join("assets", "sons", "jump.wav"))

    @property
    def pulo_contagem(self):
        return self.__pulo_contagem

    @pulo_contagem.setter
    def pulo_contagem(self, value):
        self.__pulo_contagem = value

    @property
    def double_jump_ability(self):
        return self.__double_jump_ability

    @double_jump_ability.setter
    def double_jump_ability(self, value):
        self.__double_jump_ability = value

    @property
    def jump_sound(self):
        return self.__jump_sound

    @jump_sound.setter
    def jump_sound(self, value):
        self.__jump_sound = value

    def jump(self):
        if self.pulo_contagem == 0 or (self.pulo_contagem == 1 and self.double_jump_ability):
            self.jump_sound.play()
            self.jump_sound.set_volume(0.3)
            self.y_vel = -self.GRAVIDADE * 8
            self.animacao_contagem = 0
            self.pulo_contagem += 1
            if self.pulo_contagem == 1:
                self.queda_contagem = 0

    def landed(self):
        super().landed()
        self.pulo_contagem = 0

    def on_collision_with_character(self, character, enemies):
        from enemy import Enemy
        if isinstance(character, Enemy):
            if self.rect.bottom <= character.rect.top + 30 and self.y_vel > 0:
                character.is_alive = False
                self.y_vel = -self.GRAVIDADE * 8
                enemies.remove(character)
            else:
                self.die()

    def check_death(self, enemies, screen_height):
        if self.rect.top > screen_height:
            self.die()

        for enemy in enemies:
            if pygame.sprite.collide_mask(self, enemy):
                if not (self.rect.bottom <= enemy.rect.top + 30 and self.y_vel > 0):
                    self.die()

    def die(self):
        self.rect.x = 450
        self.rect.y = 400
        self.x_vel = 0
        self.y_vel = 0
        self.pulo_contagem = 0

    def loop(self, fps):
        from utils import ALTURA
        self.apply_gravity(fps)
        self.update_sprite()