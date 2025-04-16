
import pygame
import random
import json
import os

# Initialisation de Pygame
pygame.init()

# Paramètres de la fenêtre
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600

# Couleurs pastel
COLORS = {
    'background': (230, 230, 255),  # Bleu clair
    'player': (255, 182, 193),      # Rose poudré
    'obstacle': (176, 224, 230),    # Bleu poudré
    'coin': (255, 218, 185),        # Saumon
    'text': (30, 30, 30)            # Noir
}

# Configuration du jeu
FPS = 60
PLAYER_SPEED = 5
OBSTACLE_SPEED = 3
COIN_VALUE = 10

# Paramètres du fond
NUM_PERSONNAGES = 3
PERSONNAGE_WIDTH = 30
PERSONNAGE_HEIGHT = 50
PERSONNAGE_SPEED = 2

# Paramètres des arbres
NUM_ARBRES = 20
ARBRE_WIDTH = 40
ARBRE_HEIGHT = 60
ARBRE_SPEED = 1

# Création de la fenêtre
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Pastel Subway Surfers")

class MenuButton:
    def __init__(self):
        self.width = 40
        self.height = 40
        self.x = 20
        self.y = 20
        self.color = (200, 200, 200)
        self.hover_color = (150, 150, 150)
        self.is_hover = False

    def check_hover(self, mouse_pos):
        return (self.x <= mouse_pos[0] <= self.x + self.width and
                self.y <= mouse_pos[1] <= self.y + self.height)

    def draw(self, screen):
        # Dessin du carré de la maison
        color = self.hover_color if self.is_hover else self.color
        pygame.draw.rect(screen, color, (self.x, self.y, self.width, self.height))
        
        # Dessin du toit de la maison
        points = [
            (self.x + self.width // 2, self.y - 5),
            (self.x - 5, self.y + self.height // 2),
            (self.x + self.width + 5, self.y + self.height // 2)
        ]
        pygame.draw.polygon(screen, color, points)
        
        # Contour
        pygame.draw.rect(screen, (100, 100, 100), (self.x, self.y, self.width, self.height), 2)
        pygame.draw.polygon(screen, (100, 100, 100), points, 2)

class Player:
    def __init__(self):
        self.width = 40
        self.height = 60
        self.x = WINDOW_WIDTH // 2 - self.width // 2
        self.y = WINDOW_HEIGHT - self.height - 20
        self.speed = PLAYER_SPEED
        self.jump_height = 15
        self.gravity = 0.5
        self.velocity = 0
        self.is_jumping = False

    def jump(self):
        if not self.is_jumping:
            self.velocity = -self.jump_height
            self.is_jumping = True

    def update(self):
        # Gestion de la gravité
        self.velocity += self.gravity
        self.y += self.velocity

        # Arrêter la chute quand on touche le sol
        if self.y > WINDOW_HEIGHT - self.height - 20:
            self.y = WINDOW_HEIGHT - self.height - 20
            self.velocity = 0
            self.is_jumping = False

    def draw(self):
        pygame.draw.rect(screen, COLORS['player'], (self.x, self.y, self.width, self.height))

class Obstacle:
    def __init__(self):
        self.width = 40
        self.height = 60
        self.x = WINDOW_WIDTH
        self.y = WINDOW_HEIGHT - self.height - 20
        self.speed = OBSTACLE_SPEED

    def update(self):
        self.x -= self.speed

    def draw(self):
        pygame.draw.rect(screen, COLORS['obstacle'], (self.x, self.y, self.width, self.height))

class Coin:
    def __init__(self):
        self.size = 20
        self.x = WINDOW_WIDTH
        self.y = random.randint(50, WINDOW_HEIGHT - self.size - 50)
        self.speed = OBSTACLE_SPEED

    def update(self):
        self.x -= self.speed

    def draw(self):
        pygame.draw.circle(screen, COLORS['coin'], (self.x, self.y), self.size // 2)

class Game:
    def __init__(self):
        self.player = Player()
        self.obstacles = []
        self.coins = []
        self.score = 0
        self.high_score = self.load_high_score()
        self.game_over = False
        self.paused = False
        self.clock = pygame.time.Clock()
        self.obstacle_timer = 0
        self.coin_timer = 0
        self.obstacle_interval = 100
        self.coin_interval = 200
        self.menu_button = MenuButton()
        self.pause_button = MenuButton()
        self.pause_button.x = WINDOW_WIDTH - self.pause_button.width - 20
        self.pause_button.y = 20
        self.pause_button.color = (200, 200, 200)
        self.pause_button.hover_color = (150, 150, 150)

    def get_score(self):
        return self.score

    def load_high_score(self):
        try:
            with open('highscores.json', 'r') as f:
                scores = json.load(f)
                return scores.get('subway', 0)
        except:
            return 0

    def save_high_score(self):
        try:
            with open('highscores.json', 'r') as f:
                scores = json.load(f)
        except:
            scores = {}
        
        scores['subway'] = self.high_score
        with open('highscores.json', 'w') as f:
            json.dump(scores, f)
        
        # Initialisation des personnages
        self.personnages = []
        for i in range(NUM_PERSONNAGES):
            x = i * (WINDOW_WIDTH // (NUM_PERSONNAGES + 1))
            y = WINDOW_HEIGHT - 100
            self.personnages.append({
                'x': x,
                'y': y,
                'dx': PERSONNAGE_SPEED,
                'dy': 0,
                'color': random.choice(COLORS['player'])
            })

        # Initialisation des arbres
        self.arbres = []
        for i in range(NUM_ARBRES):
            x = random.randint(0, WINDOW_WIDTH)
            y = WINDOW_HEIGHT - 150
            self.arbres.append({
                'x': x,
                'y': y,
                'dx': ARBRE_SPEED,
                'dy': 0
            })

    def load_high_score(self):
        try:
            with open('highscores.json', 'r') as f:
                scores = json.load(f)
                return int(scores.get('subway_surfers', 0))
        except:
            return 0

    def save_high_score(self):
        try:
            with open('highscores.json', 'r') as f:
                scores = json.load(f)
        except:
            scores = {}

        scores['subway_surfers'] = self.high_score
        with open('highscores.json', 'w') as f:
            json.dump(scores, f)

    def add_obstacle(self):
        self.obstacles.append(Obstacle())

    def add_coin(self):
        self.coins.append(Coin())

    def check_collision(self):
        for obstacle in self.obstacles:
            if (self.player.x < obstacle.x + obstacle.width and
                self.player.x + self.player.width > obstacle.x and
                self.player.y < obstacle.y + obstacle.height and
                self.player.y + self.player.height > obstacle.y):
                return True
        return False

    def check_coin_collection(self):
        for coin in self.coins[:]:
            if (self.player.x < coin.x + coin.size and
                self.player.x + self.player.width > coin.x and
                self.player.y < coin.y + coin.size and
                self.player.y + self.player.height > coin.y):
                self.coins.remove(coin)
                self.score += COIN_VALUE

    def update(self):
        self.player.update()
        
        # Mise à jour des obstacles
        for obstacle in self.obstacles[:]:
            obstacle.update()
            if obstacle.x + obstacle.width < 0:
                self.obstacles.remove(obstacle)

        # Vérification des collisions
        if self.check_collision():
            self.game_over = True
            if self.score > self.high_score:
                self.high_score = self.score
                self.save_high_score()

        # Mise à jour des pièces
        for coin in self.coins[:]:
            coin.update()
            if coin.x + coin.size < 0:
                self.coins.remove(coin)

        # Ajout de nouveaux obstacles
        self.obstacle_timer += 1
        if self.obstacle_timer >= self.obstacle_interval:
            self.add_obstacle()
            self.obstacle_timer = 0

        # Ajout de nouvelles pièces
        self.coin_timer += 1
        if self.coin_timer >= self.coin_interval:
            self.add_coin()
            self.coin_timer = 0

        # Vérification des collisions
        if self.check_collision():
            self.game_over = True
            if self.score > self.high_score:
                self.high_score = self.score
                self.save_high_score()

        # Vérification de la collecte des pièces
        self.check_coin_collection()

    def draw(self):
        # Dessin du fond
        screen.fill((100, 150, 200))  # Ciel bleu
        
        # Dessin de l'herbe
        pygame.draw.rect(screen, (50, 200, 50), (0, WINDOW_HEIGHT - 100, WINDOW_WIDTH, 100))
        
        # Mise à jour et dessin des personnages
        for personnage in self.personnages:
            # Mise à jour de la position
            personnage['x'] += personnage['dx']
            
            # Rebond sur les bords
            if personnage['x'] < 0 or personnage['x'] > WINDOW_WIDTH - PERSONNAGE_WIDTH:
                personnage['dx'] *= -1
                personnage['color'] = random.choice(COLORS['player'])  # Changement de couleur
            
            # Dessin du personnage
            pygame.draw.rect(screen, personnage['color'], 
                           (int(personnage['x']), int(personnage['y']), 
                            PERSONNAGE_WIDTH, PERSONNAGE_HEIGHT))
            
            # Dessin des yeux et du sourire
            eye_color = (255, 255, 255)
            eye_size = 3
            pygame.draw.circle(screen, eye_color, 
                             (int(personnage['x'] + PERSONNAGE_WIDTH // 4), 
                              int(personnage['y'] + PERSONNAGE_HEIGHT // 3)), 
                             eye_size)
            pygame.draw.circle(screen, eye_color, 
                             (int(personnage['x'] + 3 * PERSONNAGE_WIDTH // 4), 
                              int(personnage['y'] + PERSONNAGE_HEIGHT // 3)), 
                             eye_size)
            
            # Dessin du sourire
            pygame.draw.arc(screen, eye_color,
                          (int(personnage['x'] + PERSONNAGE_WIDTH // 4), 
                           int(personnage['y'] + 2 * PERSONNAGE_HEIGHT // 3), 
                           PERSONNAGE_WIDTH // 2, PERSONNAGE_HEIGHT // 3),
                          3.14, 2 * 3.14)
        
        # Mise à jour et dessin des arbres
        for arbre in self.arbres:
            # Mise à jour de la position
            arbre['x'] += arbre['dx']
            
            # Rebond sur les bords
            if arbre['x'] < 0 or arbre['x'] > WINDOW_WIDTH - ARBRE_WIDTH:
                arbre['dx'] *= -1
            
            # Dessin du tronc
            pygame.draw.rect(screen, (139, 69, 19),  # Marron
                           (int(arbre['x'] + ARBRE_WIDTH // 3), 
                            int(arbre['y']), 
                            ARBRE_WIDTH // 3, ARBRE_HEIGHT // 2))
            
            # Dessin des feuilles
            pygame.draw.circle(screen, (34, 139, 34),  # Vert
                             (int(arbre['x'] + ARBRE_WIDTH // 2), 
                              int(arbre['y'] - ARBRE_HEIGHT // 3)), 
                             ARBRE_WIDTH // 2)
            
            # Dessin des pommes
            if random.random() < 0.01:  # 1% de chance d'apparaître
                pygame.draw.circle(screen, (255, 0, 0),
                                (int(arbre['x'] + ARBRE_WIDTH // 2 + random.randint(-10, 10)),
                                 int(arbre['y'] - ARBRE_HEIGHT // 3 + random.randint(-10, 10))),
                                5)
        
        # Dessin du terrain
        pygame.draw.rect(screen, (100, 100, 100), (0, WINDOW_HEIGHT - 20, WINDOW_WIDTH, 20))
        
        # Dessin du joueur
        self.player.draw()
        
        # Dessin des obstacles
        for obstacle in self.obstacles:
            obstacle.draw()
        
        # Dessin des pièces
        for coin in self.coins:
            coin.draw()
        
        # Dessin du bouton retour
        mouse_pos = pygame.mouse.get_pos()
        self.menu_button.is_hover = self.menu_button.check_hover(mouse_pos)
        self.menu_button.draw(screen)
        
        # Dessin du bouton pause
        self.pause_button.is_hover = self.pause_button.check_hover(mouse_pos)
        self.pause_button.draw(screen)
        
        # Affichage du score
        font = pygame.font.Font(None, 36)
        score_text = font.render(f"Score: {self.score}", True, COLORS['text'])
        screen.blit(score_text, (10, 10))
        
        high_score_text = font.render(f"High Score: {self.high_score}", True, COLORS['text'])
        screen.blit(high_score_text, (10, 50))
        
        if self.game_over:
            game_over_text = font.render("GAME OVER! Press SPACE to restart", True, COLORS['text'])
            text_rect = game_over_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))
            screen.blit(game_over_text, text_rect)
        
        if self.paused:
            # Dessin du menu de pause
            pygame.draw.rect(screen, (100, 100, 100, 128), 
                           (WINDOW_WIDTH//4, WINDOW_HEIGHT//4, 
                            WINDOW_WIDTH//2, WINDOW_HEIGHT//2), 0)
            
            # Texte "PAUSE"
            pause_text = font.render("PAUSE", True, COLORS['text'])
            text_rect = pause_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 50))
            screen.blit(pause_text, text_rect)
            
            # Boutons du menu de pause
            resume_button = pygame.Rect(WINDOW_WIDTH//2 - 75, WINDOW_HEIGHT//2, 150, 40)
            pygame.draw.rect(screen, (200, 200, 200), resume_button)
            resume_text = font.render("Reprendre", True, (0, 0, 0))
            text_rect = resume_text.get_rect(center=resume_button.center)
            screen.blit(resume_text, text_rect)
            
            quit_button = pygame.Rect(WINDOW_WIDTH//2 - 75, WINDOW_HEIGHT//2 + 60, 150, 40)
            pygame.draw.rect(screen, (200, 200, 200), quit_button)
            quit_text = font.render("Menu Principal", True, (0, 0, 0))
            text_rect = quit_text.get_rect(center=quit_button.center)
            screen.blit(quit_text, text_rect)

def main():
    game = Game()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Clic gauche
                    if game.menu_button.check_hover(pygame.mouse.get_pos()):
                        running = False
                    elif game.pause_button.check_hover(pygame.mouse.get_pos()):
                        game.paused = not game.paused
                    elif game.paused:
                        mouse_pos = pygame.mouse.get_pos()
                        resume_button = pygame.Rect(WINDOW_WIDTH//2 - 75, WINDOW_HEIGHT//2, 150, 40)
                        quit_button = pygame.Rect(WINDOW_WIDTH//2 - 75, WINDOW_HEIGHT//2 + 60, 150, 40)
                        
                        if resume_button.collidepoint(mouse_pos):
                            game.paused = False
                        elif quit_button.collidepoint(mouse_pos):
                            running = False
                            
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if game.paused:
                        game.paused = False
                    else:
                        running = False
                elif event.key == pygame.K_p:
                    game.paused = not game.paused
                elif not game.paused:
                    if event.key == pygame.K_LEFT:
                        if not game.check_collision():
                            game.player.x -= game.player.speed
                    elif event.key == pygame.K_RIGHT:
                        if not game.check_collision():
                            game.player.x += game.player.speed
                    elif event.key == pygame.K_UP or event.key == pygame.K_SPACE:
                        game.player.jump()
                    elif event.key == pygame.K_DOWN:
                        if not game.check_collision():
                            game.player.y += game.player.speed

        keys = pygame.key.get_pressed()
        if not game.paused and not game.game_over:
            if keys[pygame.K_LEFT] and game.player.x > 0:
                game.player.x -= game.player.speed
            if keys[pygame.K_RIGHT] and game.player.x < WINDOW_WIDTH - game.player.width:
                game.player.x += game.player.speed

        if not game.paused and not game.game_over:
            game.update()
        game.draw()
        pygame.display.flip()
        game.clock.tick(FPS)

    pygame.quit()

if __name__ == "__main__":
    main()
