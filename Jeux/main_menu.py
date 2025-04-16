import pygame
import json
import sys
import os
import random

# Initialisation de Pygame
pygame.init()

# Paramètres de la fenêtre
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600

# Couleurs pastel
COLORS = [
    (255, 182, 193),  # Rose poudré
    (176, 224, 230),  # Bleu poudré
    (255, 228, 196),  # Beige
    (221, 160, 221),  # Lavande
    (173, 216, 230),  # Bleu ciel
    (255, 218, 185),  # Saumon
    (147, 112, 219)   # Pourpre
]

# Paramètres du fond
NUM_PERSONNAGES = 3
PERSONNAGE_WIDTH = 30
PERSONNAGE_HEIGHT = 50
PERSONNAGE_SPEED = 1

# Paramètres des arbres
NUM_ARBRES = 20
ARBRE_WIDTH = 40
ARBRE_HEIGHT = 60
ARBRE_SPEED = 0.5

# Couleurs des boutons
BUTTON_COLOR = (50, 50, 50)
HOVER_COLOR = (70, 70, 70)
TEXT_COLOR = (255, 255, 255)

class MainMenu:
    def __init__(self):
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Menu des Jeux")
        
        # Création des boutons
        button_width = 300
        button_height = 50
        center_x = WINDOW_WIDTH // 2 - button_width // 2
        
        self.tetris_button = pygame.Rect(center_x, 200, button_width, button_height)
        self.subway_button = pygame.Rect(center_x, 270, button_width, button_height)
        self.future_game2_button = pygame.Rect(center_x, 340, button_width, button_height)
        self.quit_button = pygame.Rect(center_x, 500, button_width, button_height)
        
        self.load_scores()
        
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
                'color': random.choice(COLORS)
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

    def load_scores(self):
        try:
            with open('highscores.json', 'r') as f:
                self.scores = json.load(f)
        except:
            self.scores = {"scores": []}

    def draw_button(self, button, text, hover=False):
        color = HOVER_COLOR if hover else BUTTON_COLOR
        pygame.draw.rect(self.screen, color, button)
        font = pygame.font.Font(None, 32)
        text_surface = font.render(text, True, TEXT_COLOR)
        text_rect = text_surface.get_rect(center=button.center)
        self.screen.blit(text_surface, text_rect)

    def draw(self):
        # Dessin du fond
        self.screen.fill((100, 150, 200))  # Ciel bleu
        
        # Dessin de l'herbe
        pygame.draw.rect(self.screen, (50, 200, 50), (0, WINDOW_HEIGHT - 100, WINDOW_WIDTH, 100))
        
        # Mise à jour et dessin des personnages
        for personnage in self.personnages:
            # Mise à jour de la position
            personnage['x'] += personnage['dx']
            
            # Rebond sur les bords
            if personnage['x'] < 0 or personnage['x'] > WINDOW_WIDTH - PERSONNAGE_WIDTH:
                personnage['dx'] *= -1
                personnage['color'] = random.choice(COLORS)  # Changement de couleur
            
            # Dessin du personnage
            pygame.draw.rect(self.screen, personnage['color'], 
                           (int(personnage['x']), int(personnage['y']), 
                            PERSONNAGE_WIDTH, PERSONNAGE_HEIGHT))
            
            # Dessin des yeux et du sourire
            eye_color = (255, 255, 255)
            eye_size = 3
            pygame.draw.circle(self.screen, eye_color, 
                             (int(personnage['x'] + PERSONNAGE_WIDTH // 4), 
                              int(personnage['y'] + PERSONNAGE_HEIGHT // 3)), 
                             eye_size)
            pygame.draw.circle(self.screen, eye_color, 
                             (int(personnage['x'] + 3 * PERSONNAGE_WIDTH // 4), 
                              int(personnage['y'] + PERSONNAGE_HEIGHT // 3)), 
                             eye_size)
            
            # Dessin du sourire
            pygame.draw.arc(self.screen, eye_color,
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
            pygame.draw.rect(self.screen, (139, 69, 19),  # Marron
                           (int(arbre['x'] + ARBRE_WIDTH // 3), 
                            int(arbre['y']), 
                            ARBRE_WIDTH // 3, ARBRE_HEIGHT // 2))
            
            # Dessin des feuilles
            pygame.draw.circle(self.screen, (34, 139, 34),  # Vert
                             (int(arbre['x'] + ARBRE_WIDTH // 2), 
                              int(arbre['y'] - ARBRE_HEIGHT // 3)), 
                             ARBRE_WIDTH // 2)
            
            # Dessin des pommes
            if random.random() < 0.01:  # 1% de chance d'apparaître
                pygame.draw.circle(self.screen, (255, 0, 0),
                                (int(arbre['x'] + ARBRE_WIDTH // 2 + random.randint(-10, 10)),
                                 int(arbre['y'] - ARBRE_HEIGHT // 3 + random.randint(-10, 10))),
                                5)
        
        # Titre
        font_title = pygame.font.Font(None, 64)
        title = font_title.render("ARCADE DE JEUX", True, TEXT_COLOR)
        title_rect = title.get_rect(center=(WINDOW_WIDTH // 2, 100))
        self.screen.blit(title, title_rect)

        # Meilleurs scores Tetris
        font = pygame.font.Font(None, 36)
        score_title = font.render("Meilleurs Scores Tetris:", True, TEXT_COLOR)
        self.screen.blit(score_title, (50, 200))

        y = 250
        for i, score in enumerate(self.scores["scores"][:5]):
            text = font.render(f"{i+1}. {score}", True, TEXT_COLOR)
            self.screen.blit(text, (50, y))
            y += 40

        # Position de la souris pour l'effet hover
        mouse_pos = pygame.mouse.get_pos()

        # Boutons des jeux
        self.draw_button(self.tetris_button, "Tetris", self.tetris_button.collidepoint(mouse_pos))
        self.draw_button(self.subway_button, "Subway Surfers", self.subway_button.collidepoint(mouse_pos))
        self.draw_button(self.future_game2_button, "Jeu à venir...", self.future_game2_button.collidepoint(mouse_pos))
        self.draw_button(self.quit_button, "Quitter", self.quit_button.collidepoint(mouse_pos))

        pygame.display.flip()

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    return "QUIT"
                
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # Clic gauche
                        if self.tetris_button.collidepoint(event.pos):
                            return "TETRIS"
                        elif self.subway_button.collidepoint(event.pos):
                            return "SUBWAY"
                        elif self.quit_button.collidepoint(event.pos):
                            return "QUIT"

            self.draw()
            pygame.time.Clock().tick(60)

def main():
    menu = MainMenu()
    current_game = "MENU"
    scores = {'tetris': 0, 'subway': 0}

    while True:
        if current_game == "MENU":
            current_game = menu.run()
            if current_game == "QUIT":
                break
        elif current_game == "TETRIS":
            import tetris
            tetris.main()
            scores['tetris'] = tetris.get_score()
            current_game = "MENU"
        elif current_game == "SUBWAY":
            import subway_surfers
            subway_surfers.main()
            scores['subway'] = subway_surfers.get_score()
            current_game = "MENU"

    # Sauvegarde des scores avant de quitter
    with open('highscores.json', 'w') as f:
        json.dump(scores, f)

if __name__ == "__main__":
    main()
