from projectile import Projectile
from enemy import Enemy
import pygame

class Shooter_Enemy(Enemy):
    def __init__(self, x, y, width, height, sprites, projectile_image, projectile_speed):
        super().__init__(x, y, width, height, 0, sprites)
        self.__projectile_image = projectile_image
        self.__projectile_speed = projectile_speed
        self.__shoot_cooldown = 1000 
        self.__last_shot = pygame.time.get_ticks()
        self.__projectiles = pygame.sprite.Group()

    @property
    def projectile_image(self):
        return self.__projectile_image

    @projectile_image.setter
    def projectile_image(self, value):
        self.__projectile_image = value

    @property
    def projectile_speed(self):
        return self.__projectile_speed

    @projectile_speed.setter
    def projectile_speed(self, value):
        self.__projectile_speed = value

    @property
    def shoot_cooldown(self):
        return self.__shoot_cooldown

    @shoot_cooldown.setter
    def shoot_cooldown(self, value):
        self.__shoot_cooldown = value

    @property
    def last_shot(self):
        return self.__last_shot

    @last_shot.setter
    def last_shot(self, value):
        self.__last_shot = value

    @property
    def projectiles(self):
        return self.__projectiles

    @projectiles.setter
    def projectiles(self, value):
        self.__projectiles = value

    def shoot(self):
        current_time = pygame.time.get_ticks()
        self.direction = "left"
        if current_time - self.last_shot >= self.shoot_cooldown:
            direction = -1 if self.direction == "right" else 1
            new_projectile = Projectile(self.rect.centerx, self.rect.centery, direction, self.projectile_speed, self.projectile_image)
            self.projectiles.add(new_projectile)
            self.last_shot = current_time

    def update(self, player, objects, enemies):
        if self.is_alive:
            self.update_sprite()
            self.shoot()

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

        self.projectiles.update()
        for projectile in self.projectiles:
            projectile.check_collision(player)

    def draw(self, window, offset_x):
        super().draw(window, offset_x) 
        for projectile in self.projectiles:
            projectile.draw(window, offset_x)