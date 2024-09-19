import pygame

class Menu:

    def __init__(self, window, wallpaper_image_path):
        self.__window = window

    @property
    def window(self):
        return self.__window

    @window.setter
    def window(self, value):
        self.__window = value

    def show_initial_menu(self, window, wallpaper_image_path):
        from utils import WIDTH, HEIGHT
        wallpaper = pygame.image.load(wallpaper_image_path)
        wallpaper = pygame.transform.scale(wallpaper, (WIDTH, HEIGHT))

        window.blit(wallpaper, (0, 0))
        pygame.display.update()

        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.KEYDOWN:
                    waiting = False