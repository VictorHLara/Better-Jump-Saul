import pygame

class Placar:
    def __init__(self, tela):
        self.__tela = tela

    @property
    def tela(self):
        return self.__tela

    @tela.setter
    def tela(self, value):
        self.__tela = value


    def get_player_name_screen(self):
        from utils import LARGURA, ALTURA

        font = pygame.font.Font('assets/outros/font.ttf', 30)
        input_box = pygame.Rect(LARGURA // 2 - 200, ALTURA // 2 - 25, 400, 50)
        color_inactive = pygame.Color('lightskyblue3')
        color_active = pygame.Color('dodgerblue2')
        color = color_inactive
        active = False
        player_name = ''
        done = False

        while not done:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if input_box.collidepoint(event.pos):
                        active = not active
                    else:
                        active = False
                    color = color_active if active else color_inactive
                if event.type == pygame.KEYDOWN:
                    if active:
                        if event.key == pygame.K_RETURN:
                            done = True
                        elif event.key == pygame.K_BACKSPACE:
                            player_name = player_name[:-1]
                        else:
                            player_name += event.unicode

            self.tela.fill((0, 0, 0))
            text_surface = font.render(player_name, True, color)

            text_rect = text_surface.get_rect(center=(input_box.x + input_box.width // 2, input_box.y + input_box.height // 2))
            self.tela.blit(text_surface, text_rect)

            pygame.draw.rect(self.tela, color, input_box, 2)

            prompt_text = font.render("Digite seu nome:", True, (255, 255, 255))
            self.tela.blit(prompt_text, (LARGURA // 2 - prompt_text.get_width() // 2, ALTURA // 2 - 100))

            pygame.display.flip()

        return player_name
    
    @staticmethod
    def format_time(seconds):
        minutes = int(seconds // 60)
        seconds = int(seconds % 60)
        return f"{minutes:02}:{seconds:02}"
    

    
