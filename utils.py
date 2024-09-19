import pygame
from os.path import isfile, join
from os import listdir

WIDTH = 1000
HEIGHT = 800
FPS = 60
PLAYER_SPEED = 5

class Utils:
    def __init__(self):
        pass

    @staticmethod
    def flip(sprites):
        return [pygame.transform.flip(sprite, True, False) for sprite in sprites]

    @staticmethod
    def get_block(size):
        path = join("assets", "textures", "Terrain.png")
        image = pygame.image.load(path).convert_alpha()
        surface = pygame.Surface((size, size), pygame.SRCALPHA, 32)
        rect = pygame.Rect(96, 0, size, size)
        surface.blit(image, (0, 0), rect)
        return pygame.transform.scale2x(surface)

    @staticmethod
    def load_spritesheets(dir1, dir2, width, height, direction=False, scale_factor=2):
        path = join("assets", dir1, dir2)
        images = [f for f in listdir(path) if isfile(join(path, f))]

        all_sprites = {}
        for image in images:
            sprite_sheet = pygame.image.load(join(path, image)).convert_alpha()
            num_sprites = sprite_sheet.get_width() // width
            sprites = []
            for i in range(num_sprites):
                surface = pygame.Surface((width, height), pygame.SRCALPHA, 32)
                rect = pygame.Rect(i * width, 0, width, height)
                surface.blit(sprite_sheet, (0, 0), rect)
                
                surface = pygame.transform.scale(surface, (width * scale_factor, height * scale_factor))
                
                sprites.append(surface)

            if direction:
                all_sprites[image.replace(".png", "") + "_right"] = sprites
                all_sprites[image.replace(".png", "") + "_left"] = Utils.flip(sprites)
            else:
                all_sprites[image.replace(".png", "")] = sprites

        return all_sprites

    @staticmethod
    def draw(window, background, background_image, player, objects, enemies, powerup, offset_x):
        for tile in background:
            window.blit(background_image, tile)

        for obj in objects:
            obj.draw(window, offset_x)

        player.draw(window, offset_x)
        powerup.draw(window, offset_x)

        for e in enemies:
            e.draw(window, offset_x)

        pygame.display.update()

    @staticmethod
    def handle_vertical_collision(player, objects, dy):
        collided_objects = []
        for obj in objects:
            if pygame.sprite.collide_mask(player, obj):
                if dy > 0:
                    player.rect.bottom = obj.rect.top
                    player.landed()
                elif dy < 0:
                    player.rect.top = obj.rect.bottom
                    player.hit_head()
            
            collided_objects.append(obj)

        return collided_objects
    @staticmethod
    def handle_move(player, objects):
        keys = pygame.key.get_pressed()

        player.x_vel = 0
        if keys[pygame.K_a]:
            player.move_left(PLAYER_SPEED)
        if keys[pygame.K_d]:
            player.move_right(PLAYER_SPEED)

        Utils.handle_vertical_collision(player, objects, player.y_vel)

    @staticmethod
    def get_background(nome):
        image = pygame.image.load(join("assets", "background", nome))
        _, _, width, height = image.get_rect()
        tiles = [(i * width, j * height) for i in range(WIDTH // width + 1) for j in range(HEIGHT // height + 1)]
        return tiles, image