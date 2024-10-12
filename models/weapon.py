import random
from typing import List
from abc import ABC, abstractmethod

import pygame
from pygame import Surface


class Weapon(ABC):

    def __init__(self):
        self.height = 10
        self.width = 10
        self.x = 0
        self.y = 0
        self.is_charging = False  # Indique si l'épée est en cours de chargement
        self.charge_start_time = None  # Temps de début du chargement

    @abstractmethod
    def get_image_path(self) -> str:
        pass

    def draw(self, win: Surface):
        self.x = random.randint(0, win.get_width() - self.width)
        self.y = random.randint(0, win.get_height() - self.height)
        self.image = pygame.image.load(self.get_image_path())
        win.blit(self.image, (self.x, self.y))

    @abstractmethod
    def attack(self, enemies: List[int], is_special_attack: bool):
        pass