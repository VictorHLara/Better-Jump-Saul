import pygame

class Character(pygame.sprite.Sprite):
    GRAVIDADE = 1
    DELAY_ANIMACAO = 3

    def __init__(self, x, y, largura, altura, sprites):
        super().__init__()
        self.__SPRITES = sprites
        self.__rect = pygame.Rect(x, y, largura, altura)
        self.__x_vel = 0
        self.__y_vel = 0
        self.__mask = None
        self.__direcao = "left"
        self.__animacao_contagem = 0
        self.__queda_contagem = 0
        self.__is_alive = True

    @property
    def SPRITES(self):
        return self.__SPRITES

    @SPRITES.setter
    def SPRITES(self, value):
        self.__SPRITES = value

    @property
    def rect(self):
        return self.__rect

    @rect.setter
    def rect(self, value):
        self.__rect = value

    @property
    def x_vel(self):
        return self.__x_vel

    @x_vel.setter
    def x_vel(self, value):
        self.__x_vel = value

    @property
    def y_vel(self):
        return self.__y_vel

    @y_vel.setter
    def y_vel(self, value):
        self.__y_vel = value

    @property
    def mask(self):
        return self.__mask

    @mask.setter
    def mask(self, value):
        self.__mask = value

    @property
    def direcao(self):
        return self.__direcao

    @direcao.setter
    def direcao(self, value):
        self.__direcao = value

    @property
    def animacao_contagem(self):
        return self.__animacao_contagem

    @animacao_contagem.setter
    def animacao_contagem(self, value):
        self.__animacao_contagem = value

    @property
    def queda_contagem(self):
        return self.__queda_contagem

    @queda_contagem.setter
    def queda_contagem(self, value):
        self.__queda_contagem = value

    @property
    def is_alive(self):
        return self.__is_alive

    @is_alive.setter
    def is_alive(self, value):
        self.__is_alive = value

    def move(self, dx, dy):
        self.rect.x += dx
        self.rect.y += dy

    def move_left(self, vel):
        self.x_vel = -vel
        if self.direcao != "left":
            self.direcao = "left"
            self.animacao_contagem = 0

    def move_right(self, vel):
        self.x_vel = vel
        if self.direcao != "right":
            self.direcao = "right"
            self.animacao_contagem = 0

    def apply_gravity(self, fps):
        self.y_vel += min(1, (self.queda_contagem / fps)) * self.GRAVIDADE
        self.move(self.x_vel, self.y_vel)
        self.queda_contagem += 1

    def update_sprite(self):
        spritesheet = "idle"
        if self.y_vel < 0:
            spritesheet = "jump"
        elif self.y_vel > self.GRAVIDADE * 2:
            spritesheet = "fall"
        elif self.x_vel != 0:
            spritesheet = "run"

        spritesheet_nome = spritesheet + "_" + self.direcao
        sprites = self.SPRITES[spritesheet_nome]
        sprite_index = (self.animacao_contagem // self.DELAY_ANIMACAO) % len(sprites)
        self.sprite = sprites[sprite_index]
        self.animacao_contagem += 1

        self.update_rect_and_mask()

    def update_rect_and_mask(self):
        self.rect = self.sprite.get_rect(topleft=(self.rect.x, self.rect.y))
        self.mask = pygame.mask.from_surface(self.sprite)

    def draw(self, win, offset_x):
        if self.is_alive:
            win.blit(self.sprite, (self.rect.x - offset_x, self.rect.y))

    def check_collisions(self, player, objects, enemies=None):
        if pygame.sprite.collide_mask(self, player):
            if player.rect.bottom <= self.rect.top + 30:
                self.is_alive = False
                if enemies:
                    enemies.remove(self)
            else:
                player.die()

        for obj in objects:
            if pygame.sprite.collide_mask(self, obj):
                self.reverse_direction()
                break

    def on_collision_with_character(self, character):
        pass

    def on_collision_with_object(self, obj):
        if self.y_vel > 0:
            self.rect.bottom = obj.rect.top
            self.landed()
        elif self.y_vel < 0:
            self.rect.top = obj.rect.bottom
            self.hit_head()
        elif self.x_vel > 0:
            self.rect.right = obj.rect.left
            self.x_vel = 0
        elif self.x_vel < 0:
            self.rect.left = obj.rect.right
            self.x_vel = 0

    def landed(self):
        self.queda_contagem = 0
        self.y_vel = 0

    def hit_head(self):
        self.y_vel = 0