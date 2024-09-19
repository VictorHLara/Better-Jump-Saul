import pygame

class Character(pygame.sprite.Sprite):
    GRAVITY = 1
    ANIMATION_DELAY = 3

    def __init__(self, x, y, width, height, sprites):
        super().__init__()
        self.__SPRITES = sprites
        self.__rect = pygame.Rect(x, y, width, height)
        self.__x_vel = 0
        self.__y_vel = 0
        self.__mask = None
        self.__direction = "left"
        self.__animation_count = 0
        self.__fall_count = 0
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
    def direction(self):
        return self.__direction

    @direction.setter
    def direction(self, value):
        self.__direction = value

    @property
    def animation_count(self):
        return self.__animation_count

    @animation_count.setter
    def animation_count(self, value):
        self.__animation_count = value

    @property
    def fall_count(self):
        return self.__fall_count

    @fall_count.setter
    def fall_count(self, value):
        self.__fall_count = value

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
        if self.direction != "left":
            self.direction = "left"
            self.animation_count = 0

    def move_right(self, vel):
        self.x_vel = vel
        if self.direction != "right":
            self.direction = "right"
            self.animation_count = 0

    def apply_gravity(self, fps):
        self.y_vel += min(1, (self.fall_count / fps)) * self.GRAVITY
        self.move(self.x_vel, self.y_vel)
        self.fall_count += 1

    def update_sprite(self):
        spritesheet = "idle"
        if self.y_vel < 0:
            spritesheet = "jump"
        elif self.y_vel > self.GRAVITY * 2:
            spritesheet = "fall"
        elif self.x_vel != 0:
            spritesheet = "run"

        spritesheet_nome = spritesheet + "_" + self.direction
        sprites = self.SPRITES[spritesheet_nome]
        sprite_index = (self.animation_count // self.ANIMATION_DELAY) % len(sprites)
        self.sprite = sprites[sprite_index]
        self.animation_count += 1

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
        self.fall_count = 0
        self.y_vel = 0

    def hit_head(self):
        self.y_vel = 0