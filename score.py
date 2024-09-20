import pygame

class Score:
    def __init__(self, window):
        self.__window = window

    @property
    def window(self):
        return self.__window

    @window.setter
    def window(self, value):
        self.__window = value

    def get_player_name_screen(self):
        from utils import WIDTH, HEIGHT

        font = pygame.font.Font('assets/others/font.ttf', 30)
        input_box = pygame.Rect(WIDTH // 2 - 200, HEIGHT // 2 - 25, 400, 50)
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

            self.window.fill((0, 0, 0))
            text_surface = font.render(player_name, True, color)

            text_rect = text_surface.get_rect(center=(input_box.x + input_box.width // 2, input_box.y + input_box.height // 2))
            self.window.blit(text_surface, text_rect)

            pygame.draw.rect(self.window, color, input_box, 2)

            prompt_text = font.render("INSIRA SEU NOME:", True, (255, 255, 255))
            self.window.blit(prompt_text, (WIDTH // 2 - prompt_text.get_width() // 2, HEIGHT // 2 - 100))

            pygame.display.flip()

        return player_name
    
    @staticmethod
    def format_time(seconds):
        minutes = int(seconds // 60)
        seconds = int(seconds % 60)
        return f"{minutes:02}:{seconds:02}"