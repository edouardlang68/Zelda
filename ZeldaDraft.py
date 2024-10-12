from typing import List
import pygame
import sys
import random
import math
import time

from models.sword import Sword
from models.character import Character
from models.enemy import Enemy
from models.player import Player


def create_characters():
    characters: List[Character] = []

    e1 = Enemy('img/enemy.png')
    characters.append(e1)

    e2 = Enemy('img/enemy.png')
    characters.append(e2)

    e3 = Enemy('img/enemy.png')
    characters.append(e3)

    p1 = Player('img/player.png')
    characters.append(p1)

    for c in characters:
        print(c)

def run_game():
    # Initialisation de Pygame
    pygame.init()

    # Dimensions de la fenêtre
    WIDTH, HEIGHT = 1400, 1000
    win = pygame.display.set_mode((WIDTH, HEIGHT))

    # Charger l'image de fond
    background = pygame.image.load('img/background.png')
    background = pygame.transform.scale(background, (WIDTH, HEIGHT))
    win.blit(background, (0, 0))

    # Titre et icône
    pygame.display.set_caption("Zelda")
    icon = pygame.image.load("img/icon.png")
    pygame.display.set_icon(icon)

    # Boucle principale du jeu
    running = True
    frame_count = 0  # Compteur pour contrôler la vitesse d'animation
    animation_speed = 5  # Change l'image d'animation tous les 5 frames

    e1 = Enemy()
    e2 = Enemy()
    p1 = Player()
    s1 = Sword()

    e1.draw(win=win)
    e2.draw(win=win)
    p1.draw(win=win)
    s1.draw(win=win)




    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        pygame.display.update()


if __name__ == '__main__':
    run_game()