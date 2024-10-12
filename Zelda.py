import pygame
import sys
import random
import math
import time

# Initialisation de Pygame
pygame.init()

# Dimensions de la fenêtre
WIDTH, HEIGHT = 1400, 1000
win = pygame.display.set_mode((WIDTH, HEIGHT))

# Charger l'image de fond
background = pygame.image.load('img/background.png')
background = pygame.transform.scale(background, (WIDTH, HEIGHT))
win.blit(background, (0, 0))
pygame.display.update()

# Titre et icône
pygame.display.set_caption("Zelda")
icon = pygame.image.load("img/icon.png")
pygame.display.set_icon(icon)

# Couleurs
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)


# Charger les images
player_image = pygame.image.load("img/player.png").convert_alpha()
sword_image = pygame.image.load("img/epee-de-legende.png").convert_alpha()
shield_image = pygame.image.load("img/bouclier-d'hilya.png").convert_alpha()
health_item_image = pygame.image.load("img/objets-de-soin.png").convert_alpha()
enemy_image = pygame.image.load("img/enemy.png").convert_alpha()

# Points du joueur
player_points = 0

# Charger les sprites d'animation du joueur
player_walk_right = [
    pygame.image.load("img/walk_right_1.png").convert_alpha(),
    pygame.image.load("img/walk_right_2.png").convert_alpha(),
    pygame.image.load("img/walk_right_3.png").convert_alpha(),
    pygame.image.load("img/walk_right_4.png").convert_alpha()
]

player_walk_left = [
    pygame.image.load("img/walk_left_1.png").convert_alpha(),
    pygame.image.load("img/walk_left_2.png").convert_alpha(),
    pygame.image.load("img/walk_left_3.png").convert_alpha(),
    pygame.image.load("img/walk_left_4.png").convert_alpha()
]

# Paramètres du joueur
player_width, player_height = player_image.get_size()
player_x = WIDTH // 2
player_y = HEIGHT // 2
player_speed = 3
player_health = 100
player_has_sword = False
player_has_shield = False
player_index = 0  # Index pour l'image d'animation actuelle
player_moving_right = False
player_moving_left = False

# Classe pour l'épée
class Sword:
    def __init__(self):
        self.width = 40
        self.height = 10
        self.x = random.randint(0, WIDTH - self.width)
        self.y = random.randint(0, HEIGHT - self.height)
        self.image = sword_image
        self.is_charging = False  # Indique si l'épée est en cours de chargement
        self.charge_start_time = None  # Temps de début du chargement

    def draw(self, win):
        win.blit(self.image, (self.x, self.y))

    def attack_normal(self, player_x, player_y):
        # Inflige 10 dégâts aux ennemis dans un rayon de 10 pixels
        for enemy in enemies[:]:
            distance_to_enemy = math.sqrt((player_x - enemy.x)**2 + (player_y - enemy.y)**2)
            if distance_to_enemy < 10:  # Rayon de 10 pixels pour l'attaque normale
                enemy.take_damage(10)

    def start_charge(self):
        """
        Commence le processus de chargement de l'attaque.
        """
        self.is_charging = True
        self.charge_start_time = time.time()

    def attack_charged(self, player_x, player_y):
        """
        Exécute une attaque chargée si elle a été chargée pendant au moins 5 secondes.
        L'attaque inflige 20 dégâts dans un rayon de 50 pixels.
        """
        if self.is_charging:
            charge_time = time.time() - self.charge_start_time
            if charge_time >= 5:  # Si l'attaque a été chargée pendant au moins 5 secondes
                for enemy in enemies[:]:
                    distance_to_enemy = math.sqrt((player_x - enemy.x)**2 + (player_y - enemy.y)**2)
                    if distance_to_enemy < 50:  # Rayon de 50 pixels pour l'attaque chargée
                        enemy.take_damage(20)
            self.is_charging = False  # Réinitialiser le statut de charge
            self.charge_start_time = None

# Classe pour le bouclier
class Shield:
    def __init__(self):
        self.width = 30
        self.height = 30
        self.x = random.randint(0, WIDTH - self.width)
        self.y = random.randint(0, HEIGHT - self.height)
        self.image = shield_image

    def draw(self, win):
        win.blit(self.image, (self.x, self.y))

# Classe pour les objets de soin
class HealthPack:
    def __init__(self):
        self.width = 30
        self.height = 30
        self.x = random.randint(0, WIDTH - self.width)
        self.y = random.randint(0, HEIGHT - self.height)
        self.image = health_item_image

    def draw(self, win):
        win.blit(self.image, (self.x, self.y))

# Classe pour les ennemis
class Enemy:
    def __init__(self):
        self.width = 20
        self.height = 20
        self.x = random.randint(0, WIDTH - self.width)
        self.y = random.randint(0, HEIGHT - self.height)
        self.speed = random.randint(1, 1)
        self.image = enemy_image
        self.health = 10  # Points de vie de l'ennemi

    def move_towards_player(self, player_x, player_y):
        direction_x = player_x - self.x
        direction_y = player_y - self.y
        distance = math.sqrt(direction_x ** 2 + direction_y ** 2)

        if distance != 0:
            direction_x /= distance
            direction_y /= distance

        self.x += direction_x * self.speed
        self.y += direction_y * self.speed

        self.x = max(0, min(self.x, WIDTH - self.width))
        self.y = max(0, min(self.y, HEIGHT - self.height))

    def take_damage(self, amount):
        """
        Réduit la santé de l'ennemi par le montant spécifié et vérifie s'il est éliminé.
        """
        self.health -= amount
        
        if self.health <= 0:
            enemies.remove(self)  # Retirer l'ennemi de la liste
            global player_points
            player_points += 10  # Ajouter 10 points au joueur

    def draw(self, win):
        win.blit(self.image, (self.x, self.y))

# Créer une épée et un bouclier au début du niveau
sword = Sword()  # L'épée principale que le joueur utilise
initial_shield = Shield()  # Crée un bouclier
swords = [sword]  # Liste des épées, ajout de l'épée initiale
shields = [initial_shield]  # Liste des boucliers, ajout du bouclier initial

# Liste des objets de soin
health_packs = [HealthPack() for _ in range(3)]

# Liste des ennemis
enemies = [Enemy() for _ in range(5)]

# Fonction pour dessiner la barre de santé
def draw_health_bar(win, health):
    pygame.draw.rect(win, RED, (10, 10, 100, 20))  # Barre de fond rouge
    pygame.draw.rect(win, GREEN, (10, 10, health, 20))  # Barre de santé verte

# Fonction pour vérifier les collisions
def check_collision(obj1_x, obj1_y, obj1_width, obj1_height, obj2_x, obj2_y, obj2_width, obj2_height):
    return (obj1_x < obj2_x + obj2_width and
            obj1_x + obj1_width > obj2_x and
            obj1_y < obj2_y + obj2_height and
            obj1_y + obj1_height > obj2_y)

def draw_points(win, points):
    global frame_count
    """
    Dessine le compteur de points à l'écran.

    Args:
        win (pygame.Surface): La surface de la fenêtre où dessiner les points.
        points (int): Le nombre de points à afficher.
    """
    font = pygame.font.SysFont(None, 36)  # Crée une police de taille 36
    text = font.render(f'Points: {points}', True, WHITE)  # Crée un objet texte avec la couleur blanche
    win.blit(text, (WIDTH - 150, 10))  # Affiche le texte en haut à droite de la fenêtre



# Boucle principale du jeu
running = True
frame_count = 0  # Compteur pour contrôler la vitesse d'animation
animation_speed = 5  # Change l'image d'animation tous les 5 frames

# Créer une instance de l'épée au début du niveau
sword = Sword()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Gestion des touches enfoncées
    keys = pygame.key.get_pressed()

    # Gérer les mouvements du joueur
    if keys[pygame.K_LEFT]:
        player_x -= player_speed
        player_moving_left = True
        player_moving_right = False
    elif keys[pygame.K_RIGHT]:
        player_x += player_speed
        player_moving_right = True
        player_moving_left = False
    else:
        player_moving_right = False
        player_moving_left = False

    if keys[pygame.K_UP]:
        player_y -= player_speed
    if keys[pygame.K_DOWN]:
        player_y += player_speed

    # Gestion des attaques
    if keys[pygame.K_SPACE] and player_has_sword:
        sword.attack_normal(player_x, player_y)

    if keys[pygame.K_c] and player_has_sword:
        sword.start_charge()

    if not keys[pygame.K_c] and sword.is_charging:
        sword.attack_charged(player_x, player_y)

    # Détection de collision avec les objets
    for sword in swords:
        if check_collision(player_x, player_y, player_width, player_height, sword.x, sword.y, sword.width, sword.height):
            player_has_sword = True
            swords.remove(sword)

    for shield in shields:
        if check_collision(player_x, player_y, player_width, player_height, shield.x, shield.y, shield.width, shield.height):
            player_has_shield = True
            shields.remove(shield)

    for health_pack in health_packs:
        if check_collision(player_x, player_y, player_width, player_height, health_pack.x, health_pack.y, health_pack.width, health_pack.height):
            player_health = min(100, player_health + 20)
            health_packs.remove(health_pack)

   # Déplacement des ennemis
for enemy in enemies:
    enemy.move_towards_player(player_x, player_y)

    # Détection de collision avec le joueur
    if check_collision(player_x, player_y, player_width, player_height, enemy.x, enemy.y, enemy.width, enemy.height):
        if player_has_shield:
            player_has_shield = False  # Le bouclier est utilisé, mais le joueur ne perd pas de vie
        else:
            player_health -= 10  # Réduit la vie du joueur

    # Mise à jour de la fenêtre de jeu
    win.blit(background, (0, 0))

    # Dessiner les objets
    if not player_has_sword:
        for sword in swords:
            sword.draw(win)

    if not player_has_shield:
        for shield in shields:
            shield.draw(win)

    for health_pack in health_packs:
        health_pack.draw(win)

    for enemy in enemies:
        enemy.draw(win)

    # Dessiner le joueur avec animation
    if player_moving_right:
        win.blit(player_walk_right[frame_count // animation_speed], (player_x, player_y))
    elif player_moving_left:
        win.blit(player_walk_left[frame_count // animation_speed], (player_x, player_y))
    else:
        win.blit(player_image, (player_x, player_y))

    # Fonction pour dessiner le compteur de points
    draw_points(win, player_points)

    # Dessiner la barre de santé et le compteur de points
    draw_health_bar(win, player_health)

    # Mise à jour de l'animation
    frame_count += 1
    if frame_count >= len(player_walk_right) * animation_speed:
        frame_count = 0

    # Vérifier la condition de fin de jeu
    if player_health <= 0:
        running = False

    # Contrôle du FPS
    pygame.time.Clock().tick(60)

    # Mise à jour de l'affichage
    pygame.display.update()

# Quitter Pygame
pygame.quit()
sys.exit()
