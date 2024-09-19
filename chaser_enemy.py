from enemy import Enemy

class Chaser_Enemy(Enemy):
    def __init__(self, x, y, width, height, speed, sprites):
        super().__init__(x, y, width, height, speed, sprites)
        self.__detection_range = 300

    @property
    def detection_range(self):
        return self.__detection_range

    @detection_range.setter
    def detection_range(self, value):
        self.__detection_range = value

    def follow_player(self, player):
        if abs(self.rect.x - player.rect.x) < self.detection_range:
            if self.rect.x > player.rect.x:
                self.x_vel = -self.speed
                self.direction = "left"
            elif self.rect.x < player.rect.x:
                self.x_vel = self.speed
                self.direction = "right"
        else:
            self.x_vel = 0

    def move(self):
        self.rect.x += self.x_vel

    def update(self, player, objects, enemies):
        import pygame
        if self.is_alive:
            self.follow_player(player)
            self.move()
            self.update_sprite()

        
            if pygame.sprite.collide_mask(self, player):
                if player.rect.bottom <= self.rect.top + 32:
                    self.is_alive = False
                    enemies.remove(self)  
                    player.y_vel = -player.GRAVITY * 8  
                else:
                    player.die()