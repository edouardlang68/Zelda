import math
import random
from abc import ABC, abstractmethod
from typing import List

import pygame
from pygame import Surface

from models.weapon import Weapon


class Character(ABC):

    def __init__(self):
        self.height = 0
        self.width = 0
        self.x = 0
        self.max_x = -1
        self.y = 0
        self.max_y = -1
        self.speed = random.randint(1, 1)
        self.health = 0
        self.weapons: List[Weapon] = []
        self.is_charging = False  # Indique si l'épée est en cours de chargement
        self.charge_start_time = None  # Temps de début du chargement
        self.image = None

    @abstractmethod
    def get_image_path(self) -> str:
        pass

    def draw(self, win: Surface):
        # Chargement de l'image
        self.image = pygame.image.load(self.get_image_path())
        self.width = self.image.get_width()
        self.height = self.image.get_height()

        # Definition des coordonnées X et Y maximales
        self.max_x = win.get_width() - self.width
        self.max_y = win.get_height() - self.height

        # Positionnement aléatoire dans la fenêtre de jeu
        self.x = random.randint(0, self.max_x)
        self.y = random.randint(0, self.max_y)
        win.blit(self.image, (self.x, self.y))

    def draw_update(self, win: Surface):
        self.max_x = win.get_width() - self.width
        self.max_y = win.get_height() - self.height
        win.blit(self.image, (self.x, self.y))

    def attack(self, enemies: List[int], is_special_attack: bool):
       if self.weapons:
           self.weapons[0].attack(enemies, is_special_attack)

    def move_towards(self, x: int, y: int):
        direction_x = x - self.x
        direction_y = y - self.y
        distance = math.sqrt(direction_x ** 2 + direction_y ** 2)

        if distance != 0:
            direction_x /= distance
            direction_y /= distance

        self.x += direction_x * self.speed
        self.y += direction_y * self.speed

        self.x = max(0, min(self.x, self.max_x))
        self.y = max(0, min(self.y, self.max_y))

    def take_damage(self, amount):
        """
        Réduit la santé de l'ennemi par le montant spécifié et vérifie s'il est éliminé.
        """
        self.health -= amount

    def __str__(self):
        return f"{self.__class__.__name__}: {self.health} -> {self.speed}"
