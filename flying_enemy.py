from enemy import Enemy

class Flying_Enemy(Enemy):
    def __init__(self, x, y, width, height, speed, sprites):
        super().__init__(x, y, width, height, speed, sprites)
        self.__height_max = 350
        self.__height_min = 405
        self.__x_min = x - 200
        self.__x_max = x + 200
        self.__vertical_direction = "up"
        self.__horizontal_direction = "left"

    @property
    def height_max(self):
        return self.__height_max

    @height_max.setter
    def height_max(self, value):
        self.__height_max = value

    @property
    def height_min(self):
        return self.__height_min

    @height_min.setter
    def height_min(self, value):
        self.__height_min = value

    @property
    def x_min(self):
        return self.__x_min

    @x_min.setter
    def x_min(self, value):
        self.__x_min = value

    @property
    def x_max(self):
        return self.__x_max

    @x_max.setter
    def x_max(self, value):
        self.__x_max = value

    @property
    def vertical_direction(self):
        return self.__vertical_direction

    @vertical_direction.setter
    def vertical_direction(self, value):
        self.__vertical_direction = value

    @property
    def horizontal_direction(self):
        return self.__horizontal_direction

    @horizontal_direction.setter
    def horizontal_direction(self, value):
        self.__horizontal_direction = value

    def move(self):
        if self.vertical_direction == "up":
            self.rect.y -= self.speed
            if self.rect.y <= self.height_max:
                self.vertical_direction = "down"
        elif self.vertical_direction == "down":
            self.rect.y += self.speed
            if self.rect.y >= self.height_min:
                self.vertical_direction = "up"

        if self.horizontal_direction == "left":
            self.rect.x -= self.speed
            if self.rect.x <= self.x_min:
                self.horizontal_direction = "right"
        elif self.horizontal_direction == "right":
            self.rect.x += self.speed
            if self.rect.x >= self.x_max:
                self.horizontal_direction = "left"

    def update(self, player, objects, enemies):
        import pygame
        if self.is_alive:
            self.move()
            self.update_sprite()

            if pygame.sprite.collide_mask(self, player):
                if player.rect.bottom <= self.rect.top + 32:
                    self.is_alive = False
                    enemies.remove(self)
                    player.y_vel = -player.GRAVITY * 8
                else:
                    player.die()

            for obj in objects:
                if pygame.sprite.collide_mask(self, obj):
                    self.reverse_direction()
                    break