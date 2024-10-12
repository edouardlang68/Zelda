import pygame
import sys
import random
import math
import time

# Initialisation de Pygame
pygame.init()

# Dimensions de la fenêtre
WIDTH, HEIGHT = 1000, 700
win = pygame.display.set_mode((WIDTH, HEIGHT))

# Titre et icône
pygame.display.set_caption("Zelda")
icon = pygame.image.load(r"C:\Users\lange6\Projets\the-legend-of-zelda\icon.png")
pygame.display.set_icon(icon)

# Couleurs
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)

# Charger l'image de fond
background = pygame.image.load(r"C:\Users\lange6\Projets\the-legend-of-zelda\background.png")
background = pygame.transform.scale(background, (WIDTH, HEIGHT))

# Charger les images
player_image = pygame.image.load(r"C:\Users\lange6\Projets\the-legend-of-zelda\player.png").convert_alpha()
sword_image = pygame.image.load(r"C:\Users\lange6\Projets\the-legend-of-zelda\epee-de-legende.png").convert_alpha()
shield_image = pygame.image.load(r"C:\Users\lange6\Projets\the-legend-of-zelda\bouclier-d'hilya.png").convert_alpha()
health_item_image = pygame.image.load(r"C:\Users\lange6\Projets\the-legend-of-zelda\objets-de-soin.png").convert_alpha()
enemy_image = pygame.image.load(r"C:\Users\lange6\Projets\the-legend-of-zelda\enemy.png").convert_alpha()
sword_swing_image = pygame.image.load(r"C:\Users\lange6\Projets\the-legend-of-zelda\sword_swing.png").convert_alpha()

# Points du joueur
player_points = 0

# Charger les sprites d'animation du joueur
player_walk_right = [
    pygame.image.load(r"C:\Users\lange6\Projets\the-legend-of-zelda\walk_right_1.png").convert_alpha(),
    pygame.image.load(r"C:\Users\lange6\Projets\the-legend-of-zelda\walk_right_2.png").convert_alpha(),
    pygame.image.load(r"C:\Users\lange6\Projets\the-legend-of-zelda\walk_right_3.png").convert_alpha(),
    pygame.image.load(r"C:\Users\lange6\Projets\the-legend-of-zelda\walk_right_4.png").convert_alpha()
]

player_walk_left = [
    pygame.image.load(r"C:\Users\lange6\Projets\the-legend-of-zelda\walk_left_1.png").convert_alpha(),
    pygame.image.load(r"C:\Users\lange6\Projets\the-legend-of-zelda\walk_left_2.png").convert_alpha(),
    pygame.image.load(r"C:\Users\lange6\Projets\the-legend-of-zelda\walk_left_3.png").convert_alpha(),
    pygame.image.load(r"C:\Users\lange6\Projets\the-legend-of-zelda\walk_left_4.png").convert_alpha()
]

# Paramètres du joueur
player_width, player_height = player_image.get_size()
player_x = WIDTH // 2
player_y = HEIGHT // 2
player_speed = 1
player_health = 500
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
        self.is_charging = False
        self.charge_start_time = None

    def draw(self, win):
        win.blit(self.image, (self.x, self.y))

    def attack_normal(self, player_x, player_y):
        for enemy in enemies[:]:
            distance_to_enemy = math.sqrt((player_x - enemy.x)**2 + (player_y - enemy.y)**2)
            if distance_to_enemy < 70:  # Rayon de 50 pixels pour l'attaque normale
                enemy.take_damage(10)

    def start_charge(self):
        self.is_charging = True
        self.charge_start_time = time.time()
        print("Chargement de l'attaque en cours...")

    def attack_charged(self, player_x, player_y):
        if self.is_charging:
            charge_time = time.time() - self.charge_start_time
            if charge_time >= 2:  # L'attaque est chargée si la touche est maintenue pendant au moins 3 secondes
                print("Attaque chargée exécutée !")
                for enemy in enemies[:]:
                    distance_to_enemy = math.sqrt((player_x - enemy.x)**2 + (player_y - enemy.y)**2)
                    if distance_to_enemy < 300:  # Rayon de 300 pixels pour l'attaque chargée
                        enemy.take_damage(40)
            else:
                print("Attaque chargée annulée. Le temps de charge n'était pas suffisant.")
            self.is_charging = False
            self.charge_start_time = None

    # Variables pour gérer l'affichage du coup d'épée
sword_swing_visible = False
sword_swing_duration = 300  # Durée du coup d'épée en millisecondes
sword_swing_start_time = 0

def attack_with_sword(player_x, player_y):
    global sword_swing_visible, sword_swing_start_time

    # Début de l'attaque
    sword_swing_visible = True
    sword_swing_start_time = pygame.time.get_ticks()

    # Exécuter l'attaque normale (dommages aux ennemis)
    sword.attack_normal(player_x, player_y)

current_time = pygame.time.get_ticks()


#  pour le bouclier
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
        self.speed = random.uniform(0.2, 0.3)
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
shields = [initial_shield]  # Liste


# Liste des objets de soin
health_packs = [HealthPack() for _ in range(3)]

# Liste des ennemis
enemies = [Enemy() for _ in range(5)]

# Fonction pour dessiner la barre de santé
def draw_health_bar(win, health):
    pygame.draw.rect(win, RED, (10, 10, 100, 20))  # Barre de fond rouge
    pygame.draw.rect(win, GREEN, (10, 10, max(0, min(health, 1000)), 20))  # Barre de santé verte

# Fonction pour dessiner les points
def draw_points(win, points):
    font = pygame.font.SysFont(None, 36)  # Crée une police de taille 36
    text = font.render(f'Points: {points}', True, GREEN)  # Crée un objet texte avec la couleur blanche
    win.blit(text, (WIDTH - 150, 10))  # Affiche le texte en haut à droite de la fenêtre

def check_collision(obj1_x, obj1_y, obj1_width, obj1_height, obj2_x, obj2_y, obj2_width, obj2_height):
    """
    Vérifie si deux objets rectangulaires se chevauchent.
    """
    return (obj1_x < obj2_x + obj2_width and
            obj1_x + obj1_width > obj2_x and
            obj1_y < obj2_y + obj2_height and
            obj1_y + obj1_height > obj2_y)
# Fonction pour dessiner le bouton de redémarrage
def draw_restart_button(win):
    button_color = (0, 128, 0)  # Couleur du bouton (vert)
    button_rect = pygame.Rect((WIDTH // 2 - 100, HEIGHT // 2 + 50, 200, 50))  # Position du bouton
    pygame.draw.rect(win, button_color, button_rect)  # Dessiner le bouton

    font = pygame.font.SysFont(None, 36)
    text = font.render('Restart', True, WHITE)
    text_rect = text.get_rect(center=button_rect.center)  # Positionner le texte au centre du bouton
    win.blit(text, text_rect)

    return button_rect

# Fonction pour afficher l'écran de fin de jeu
def display_game_over(win):
    win.blit(game_over_image, (0, 0))  # Afficher l'image de fin de jeu
    restart_button_rect = draw_restart_button(win)  # Dessiner le bouton de redémarrage
    pygame.display.update()  # Mettre à jour l'affichage

    # Boucle pour vérifier les clics sur le bouton
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if restart_button_rect.collidepoint(mouse_pos):
                    return  # Sortir de la fonction pour redémarrer le jeu

# Fonction pour réinitialiser le jeu
def reset_game():
    global player_x, player_y, player_health, player_points
    global player_has_sword, player_has_shield
    global swords, shields, health_packs, enemies

    # Réinitialiser les variables du joueur
    player_x = WIDTH // 2
    player_y = HEIGHT // 2
    player_health = 500
    player_points = 0
    player_has_sword = False
    player_has_shield = False

    # Réinitialiser les objets du jeu
    swords = [Sword()]
    shields = [Shield()]
    health_packs = [HealthPack() for _ in range(3)]
    enemies = [Enemy() for _ in range(5)]



# Charger l'image de Game Over
game_over_image = pygame.image.load(r"C:\Users\lange6\Projets\the-legend-of-zelda\game_over.png").convert_alpha()
game_over_image = pygame.transform.scale(game_over_image, (WIDTH, HEIGHT))

def display_game_over(win):
    win.blit(game_over_image, (0, 0))
    pygame.display.update()
    pygame.time.wait(3000)  # Affiche l'écran de Game Over pendant 3 secondes


# Boucle principale du jeu
running = True
animation_speed = 5  # Change l'image d'animation tous les 5 frames

while running:
    frame_count = 0  # Compteur pour contrôler la vitesse d'animation
    while True :
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit

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

        # Gestion de l'attaque
        if keys[pygame.K_SPACE] and player_has_sword:
            attack_with_sword(player_x, player_y)


        # Détection du début du chargement
        if keys[pygame.K_m] and player_has_sword:
            if sword.charge_start_time is None:  # Commencer le chargement si ce n'est pas déjà fait
                sword.start_charge()

        # Détection de la fin du chargement et exécution de l'attaque chargée
        if not keys[pygame.K_m] and sword.is_charging:
            sword.attack_charged(player_x, player_y)

        # Limiter les coordonnées du joueur pour qu'elles restent dans les limites de la fenêtre
        player_x = max(0, min(player_x, WIDTH - player_width))
        player_y = max(0, min(player_y, HEIGHT - player_height))

        # Détection de collision avec les objets
        for sword in swords[:]:
            if check_collision(player_x, player_y, player_width, player_height, sword.x, sword.y, sword.width, sword.height):
                player_has_sword = True
                swords.remove(sword)

        for shield in shields[:]:
            if check_collision(player_x, player_y, player_width, player_height, shield.x, shield.y, shield.width, shield.height):
                player_has_shield = True
                shields.remove(shield)

        for health_pack in health_packs[:]:
            if check_collision(player_x, player_y, player_width, player_height, health_pack.x, health_pack.y, health_pack.width, health_pack.height):
                player_health = min(1000, player_health + 50)
                health_packs.remove(health_pack)

        # Déplacement des ennemis
        for enemy in enemies[:]:
            enemy.move_towards_player(player_x, player_y)

            # Détection de collision avec le joueur
            if check_collision(player_x, player_y, player_width, player_height, enemy.x, enemy.y, enemy.width, enemy.height):
                if player_has_shield:
                    player_has_shield = False
                else:
                    player_health -= 5

        # Mise à jour de la fenêtre de jeu
        win.blit(background, (0, 0))

        # Dessiner les objets
        for sword in swords:
            sword.draw(win)

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

        # Dessiner la barre de santé et le compteur de points
        draw_health_bar(win, player_health)
        draw_points(win, player_points)

        # Mise à jour de l'animation
        frame_count += 1
        if frame_count >= len(player_walk_right) * animation_speed:
            frame_count = 0

        # Afficher le coup d'épée si visible
        if sword_swing_visible:
            win.blit(sword_swing_image, (player_x, player_y))
            # Masquer le coup d'épée après la durée spécifiée
            if current_time - sword_swing_start_time > sword_swing_duration:
                sword_swing_visible = False

        # Mise à jour de l'affichage
        pygame.display.update()

        # Vérifier la condition de fin de jeu
        if player_health <= 0:
            display_game_over(win)
            reset_game()  # Réinitialiser l'état du jeu