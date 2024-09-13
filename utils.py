import pygame
from os.path import isfile, join
from os import listdir

LARGURA = 1000
ALTURA = 800
FPS = 60
PLAYER_VELOCIDADE = 5


class Utils:
    def __init__(self):
        pass

    @staticmethod
    def flip(sprites):
        """Retorna uma lista dos sprites, mas invertida horizontalmente."""
        return [pygame.transform.flip(sprite, True, False) for sprite in sprites]

    @staticmethod
    def get_block(size):
        path = join("assets", "texturas", "Terrain.png")
        image = pygame.image.load(path).convert_alpha()
        surface = pygame.Surface((size, size), pygame.SRCALPHA, 32)
        rect = pygame.Rect(96, 0, size, size)
        surface.blit(image, (0, 0), rect)
        return pygame.transform.scale2x(surface)

    @staticmethod
    def load_spritesheets(dir1, dir2, largura, altura, direcao=False, scale_factor=2):
        path = join("assets", dir1, dir2)
        images = [f for f in listdir(path) if isfile(join(path, f))]

        all_sprites = {}
        for image in images:
            sprite_sheet = pygame.image.load(join(path, image)).convert_alpha()
            num_sprites = sprite_sheet.get_width() // largura
            sprites = []
            for i in range(num_sprites):
                surface = pygame.Surface((largura, altura), pygame.SRCALPHA, 32)
                rect = pygame.Rect(i * largura, 0, largura, altura)
                surface.blit(sprite_sheet, (0, 0), rect)
                
                surface = pygame.transform.scale(surface, (largura * scale_factor, altura * scale_factor))
                
                sprites.append(surface)

            if direcao:
                all_sprites[image.replace(".png", "") + "_right"] = sprites
                all_sprites[image.replace(".png", "") + "_left"] = Utils.flip(sprites)
            else:
                all_sprites[image.replace(".png", "")] = sprites

        return all_sprites

    @staticmethod
    def draw(tela, background, background_image, player, objects, enemies, powerup, offset_x):
        for tile in background:
            tela.blit(background_image, tile)

        for obj in objects:
            obj.draw(tela, offset_x)

        player.draw(tela, offset_x)
        powerup.draw(tela, offset_x)

        for e in enemies:
            e.draw(tela, offset_x)

        pygame.display.update()

    

    @staticmethod
    def handle_colisao_vertical(player, objects, dy):
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
            player.move_left(PLAYER_VELOCIDADE)
        if keys[pygame.K_d]:
            player.move_right(PLAYER_VELOCIDADE)

        Utils.handle_colisao_vertical(player, objects, player.y_vel)

    @staticmethod
    def get_background(nome):
        image = pygame.image.load(join("assets", "background", nome))
        _, _, largura, altura = image.get_rect()
        tiles = [(i * largura, j * altura) for i in range(LARGURA // largura + 1) for j in range(ALTURA // altura + 1)]
        return tiles, image