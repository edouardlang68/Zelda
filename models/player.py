import random
from models.character import Character


class Player(Character):
    def __init__(self):
        super().__init__()
        self.speed = random.randint(2, 3)
        self.health = 50  # Points de vie du joueur

    def get_image_path(self) -> str:
        return 'img/player.png'
