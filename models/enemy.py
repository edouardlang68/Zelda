import random
from models.character import Character


class Enemy(Character):
    def __init__(self):
        super().__init__()
        self.speed = random.randint(1, 1)
        self.health = 10  # Points de vie de l'ennemi

    def get_image_path(self) -> str:
        return 'img/enemy.png'
