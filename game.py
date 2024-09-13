import pygame
import os
from os.path import join
from player import Player
from inimigo_voador import Inimigo_Voador
from block import Block
from powerup import PowerUp
from inimigo_terrestre import Inimigo_Terrestre
import time
from inimigo_atirador import Inimigo_Atirador
from placar import Placar
from menu import Menu
from rank import Rank
from utils import Utils


class Game:
    def __init__(self, largura, altura):
        self.__largura = largura
        self.__altura = altura
        self.__fps = 60
        self.__clock = pygame.time.Clock()
        self.__window = pygame.display.set_mode((largura, altura))
        self.__player = None
        self.__enemies = []
        self.__objects = []
        self.__background = None
        self.__background_image = None
        self.__placar = None
        self.__menu = None
        self.__rank = None
        self.__powerup = None
        self.__offset_x = 0
        self.__scrolling_largura = 500
        self.__run = True
        self.__player_name = None  # Novo atributo para o nome do jogador
        self.__start_time = None  # Atributo para armazenar o tempo de início

    @property
    def largura(self):
        return self.__largura

    @largura.setter
    def largura(self, value):
        self.__largura = value

    @property
    def altura(self):
        return self.__altura

    @altura.setter
    def altura(self, value):
        self.__altura = value

    @property
    def fps(self):
        return self.__fps

    @fps.setter
    def fps(self, value):
        self.__fps = value

    @property
    def clock(self):
        return self.__clock

    @clock.setter
    def clock(self, value):
        self.__clock = value

    @property
    def window(self):
        return self.__window

    @window.setter
    def window(self, value):
        self.__window = value

    @property
    def player(self):
        return self.__player

    @player.setter
    def player(self, value):
        self.__player = value

    @property
    def enemies(self):
        return self.__enemies

    @enemies.setter
    def enemies(self, value):
        self.__enemies = value

    @property
    def objects(self):
        return self.__objects

    @objects.setter
    def objects(self, value):
        self.__objects = value

    @property
    def background(self):
        return self.__background

    @background.setter
    def background(self, value):
        self.__background = value

    @property
    def background_image(self):
        return self.__background_image

    @background_image.setter
    def background_image(self, value):
        self.__background_image = value

    @property
    def placar(self):
        return self.__placar

    @placar.setter
    def placar(self, value):
        self.__placar = value

    @property
    def menu(self):
        return self.__menu

    @menu.setter
    def menu(self, value):
        self.__menu = value

    @property
    def rank(self):
        return self.__rank

    @rank.setter
    def rank(self, value):
        self.__rank = value

    @property
    def powerup(self):
        return self.__powerup

    @powerup.setter
    def powerup(self, value):
        self.__powerup = value

    @property
    def offset_x(self):
        return self.__offset_x

    @offset_x.setter
    def offset_x(self, value):
        self.__offset_x = value

    @property
    def scrolling_largura(self):
        return self.__scrolling_largura

    @scrolling_largura.setter
    def scrolling_largura(self, value):
        self.__scrolling_largura = value

    @property
    def run(self):
        return self.__run

    @run.setter
    def run(self, value):
        self.__run = value

    @property
    def player_name(self):
        return self.__player_name

    @player_name.setter
    def player_name(self, value):
        self.__player_name = value

    @property
    def start_time(self):
        return self.__start_time

    @start_time.setter
    def start_time(self, value):
        self.__start_time = value


    def init(self):
        
        pygame.init()
        pygame.mixer.init()
        pygame.mixer.music.load(os.path.join("assets", "sons", "music.wav"))
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(0.3)

        self.placar, self.menu, self.rank = self.init_game_elements()
        self.menu.show_initial_menu(self.window, join("assets", "background", "betterjumpsaul.png"))
        # Pergunta o nome do jogador logo no início
        self.player_name = self.placar.get_player_name_screen()

        self.player, self.enemies, self.powerup, self.objects, self.background, self.background_image = self.create_game_objects()

        # Registra o tempo de início do jogo
        self.start_time = time.time()

    def init_game_elements(self):
        placar = Placar(self.window)
        menu = Menu(self.window, join("assets", "background", "betterjumpsaul.png"))
        rank = Rank(self.window)
        return placar, menu, rank

    def create_game_objects(self):
        background, background_image = Utils.get_background("yellow.png")
        block_size = 96
        chao = [Block(i * block_size, self.altura - block_size, block_size) for i in range(-self.largura // block_size, (self.largura * 2) // block_size)]
        final_chao_position = chao[-1].rect.x + block_size
        for i in range(10):
            x_position = final_chao_position + 375 + i * block_size
            chao.append(Block(x_position, 800 - block_size, block_size))

        plataformas = [
            Block(-850, 400, 48), Block(-1280, 600, block_size), Block(-1580, 600, block_size),
            Block(-1880, 600, block_size), Block(-2180, 600, block_size), Block(-2400, 500, block_size),
            Block(-2700, 400, block_size), Block(-3000, 400, block_size)
        ]

        player = Player(450, 400, 50, 50, Utils.load_spritesheets("player", "SaulGoodman", 32, 32, True))
        enemies = [
            Inimigo_Terrestre(1200, 640, 50, 50, 2, Utils.load_spritesheets("inimigos", "Heisenberg", 32, 32, True)),
            Inimigo_Voador(-500, 400, 50, 50, 2, Utils.load_spritesheets("inimigos", "Fantasma", 32, 32, True)),
            Inimigo_Terrestre(2800, 640, 50, 50, 2, Utils.load_spritesheets("inimigos", "Heisenberg", 32, 32, True)),
            Inimigo_Atirador(-2140, 537, 50, 50, Utils.load_spritesheets("inimigos", "Gus", 32, 32, True), pygame.image.load(os.path.join("assets", "outros", "bala.png")).convert_alpha(), 6)
        ]
        powerup = PowerUp(-2975, 335, 32, 32, Utils.load_spritesheets("outros", "powerup", 32, 32, True))

        return player, enemies, powerup, chao + plataformas, background, background_image

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.run = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and self.player.pulo_contagem < 2:
                    self.player.jump()

    def update_game_state(self):
        self.player.loop(self.fps)
        for enemy in self.enemies:
            enemy.update_sprite()
        self.player.check_death(self.enemies, self.altura)
        self.offset_x = self.player.rect.centerx - self.largura // 2
        Utils.handle_move(self.player, self.objects)
        self.powerup.update(self.player)
        for enemy in self.enemies[:]:
            enemy.update(self.player, self.objects, self.enemies)

    def render(self):
        Utils.draw(self.window, self.background, self.background_image, self.player, self.objects, self.enemies, self.powerup, self.offset_x)

    def check_game_state(self):
        if all(not enemy.is_alive for enemy in self.enemies):
            end_time = time.time()
            total_time = end_time - self.start_time  # Calcula o tempo total do jogo
            formatted_time = self.placar.format_time(total_time)
            ranking = Rank.save_score(self.player_name, formatted_time)
            self.rank.display_rank(self.window, ranking)
            self.run = False

    def run_game(self):
        self.init()
        while self.run:
            self.clock.tick(self.fps)
            self.handle_events()
            self.update_game_state()
            self.render()
            self.check_game_state()

def main():
    game = Game(1000, 800)
    game.run_game()

if __name__ == "__main__":
    main()
