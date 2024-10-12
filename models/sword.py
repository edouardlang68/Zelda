import math
import random
from typing import List

from pygame import Surface

from models.weapon import Weapon


class Sword(Weapon):

    def __init__(self):
        super().__init__()

    def get_image_path(self) -> str:
        return 'img/epee-de-legende.png'

    def attack(self, enemies: List[int], is_special_attack: bool):
        for enemy in enemies[:]:
            enemy.take_damage(100 if is_special_attack else 10)