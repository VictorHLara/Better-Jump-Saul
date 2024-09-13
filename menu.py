import pygame

class Menu:
    '''Classe para mostrar o menu inicial'''

    def __init__(self, tela, wallpaper_image_path):
        self.__tela = tela

    @property
    def tela(self):
        return self.__tela

    @tela.setter
    def tela(self, value):
        self.__tela = value

    def show_initial_menu(self, tela, wallpaper_image_path):
        from utils import LARGURA, ALTURA
        wallpaper = pygame.image.load(wallpaper_image_path)
        wallpaper = pygame.transform.scale(wallpaper, (LARGURA, ALTURA))

        tela.blit(wallpaper, (0, 0))
        pygame.display.update()

        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.KEYDOWN:
                    waiting = False

    
 

    