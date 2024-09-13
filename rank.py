import pygame
import json
import os
from os.path import isfile,join
from os import listdir
class Rank:

    def __init__(self, tela):
        self.__tela = tela

    @property
    def tela(self):
        return self.__tela

    @tela.setter
    def tela(self, value):
        self.__tela = value


    def save_score(player_name, total_time, filename="ranking.json"):
        try:
            if os.path.exists(filename) and os.path.getsize(filename) > 0:
                with open(filename, "r") as file:
                    try:
                        ranking = json.load(file)
                    except json.JSONDecodeError:
                        ranking = []
            else:
                raise FileNotFoundError
        except FileNotFoundError:
            print(f"Arquivo {filename} não encontrado. Nenhum ranking será salvo.")
            return [] 

        ranking.append({"name": player_name, "time": total_time})

        ranking = sorted(ranking, key=lambda x: x["time"])

        with open(filename, "w") as file:
            json.dump(ranking, file, indent=4)

        return ranking
    
    def display_rank(self, tela, ranking):
        from utils import LARGURA
        font = pygame.font.Font('assets/outros/font.ttf', 30)
        tela.fill((0, 0, 0))
        text = font.render("Ranking:", True, (255, 255, 255))
        tela.blit(text, (LARGURA // 2 - text.get_width() // 2, 50))

        for index, entry in enumerate(ranking[:5]):
            rank_text = f"{index + 1}. {entry['name']} - {entry['time']}"
            text = font.render(rank_text, True, (255, 255, 255))
            tela.blit(text, (LARGURA // 2 - text.get_width() // 2, 100 + index * 40))

        pygame.display.update()
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.KEYDOWN:
                    waiting = False