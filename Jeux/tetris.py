import pygame
import random
import math
import json
import sys
import os
import json
import os

# Initialisation de Pygame
pygame.init()

# Paramètres de la fenêtre
WINDOW_WIDTH = 400
WINDOW_HEIGHT = 600
GRID_SIZE = 25
GRID_WIDTH = 10
GRID_HEIGHT = 20

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

# Configuration du jeu
FPS = 60
DROP_SPEED = 20

# Création de la fenêtre
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Tetris Pastel")

def load_highscores():
    try:
        with open('highscores.json', 'r') as f:
            return json.load(f)
    except:
        return {"scores": []}

def save_highscores(scores):
    with open('highscores.json', 'w') as f:
        json.dump(scores, f)

def add_score(score):
    scores = load_highscores()
    scores["scores"].append(score)
    scores["scores"].sort(reverse=True)
    scores["scores"] = scores["scores"][:5]  # Garder uniquement les 5 meilleurs scores
    save_highscores(scores)

class Piece:
    def __init__(self):
        self.shape = self.generate_shape()
        self.color = random.choice(COLORS)
        self.x = GRID_WIDTH // 2 - 1
        self.y = 0
        self.rotation = 0

    def generate_shape(self):
        shapes = [
            [[1, 1], [1, 1]],  # Carré
            [[1, 1, 1], [0, 1, 0]],  # T
            [[1, 1, 1, 1]],  # Ligne
            [[1, 1, 0], [0, 1, 1]],  # S
            [[0, 1, 1], [1, 1, 0]],  # Z
            [[1, 1, 1], [1, 0, 0]],  # L
            [[1, 1, 1], [0, 0, 1]]   # J
        ]
        return random.choice(shapes)

    def rotate(self):
        self.rotation = (self.rotation + 1) % 4
        new_shape = [[0] * len(self.shape) for _ in range(len(self.shape[0]))]
        for y in range(len(self.shape)):
            for x in range(len(self.shape[y])):
                new_shape[x][len(self.shape) - 1 - y] = self.shape[y][x]
        self.shape = new_shape

class Game:
    def __init__(self):
        self.grid = [[None for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
        self.current_piece = Piece()
        self.next_piece = Piece()
        self.game_over = False
        self.paused = False
        self.in_menu = False
        self.score = 0
        self.level = 1
        self.lines_cleared = 0
        self.health = 100
        self.drop_timer = 0
        self.fall_speed = DROP_SPEED
        self.move_delay = 0
        self.move_repeat_delay = 5
        self.home_button = pygame.Rect(20, 20, 30, 30)
        # Création des rectangles des boutons du menu
        self.resume_button = pygame.Rect(WINDOW_WIDTH // 2 - 100, 450, 200, 40)
        self.quit_button = pygame.Rect(WINDOW_WIDTH // 2 - 100, 500, 200, 40)

    def check_collision(self, piece, offset_x=0, offset_y=0):
        for y, row in enumerate(piece.shape):
            for x, cell in enumerate(row):
                if cell:
                    new_x = piece.x + x + offset_x
                    new_y = piece.y + y + offset_y
                    if (new_x < 0 or new_x >= GRID_WIDTH or 
                        new_y >= GRID_HEIGHT or 
                        (new_y >= 0 and self.grid[new_y][new_x])):
                        return True
        return False

    def lock_piece(self):
        for y, row in enumerate(self.current_piece.shape):
            for x, cell in enumerate(row):
                if cell:
                    grid_y = self.current_piece.y + y
                    grid_x = self.current_piece.x + x
                    if grid_y >= 0:
                        self.grid[grid_y][grid_x] = self.current_piece.color

        self.clear_lines()
        self.current_piece = self.next_piece
        self.next_piece = Piece()
        self.drop_timer = 0

        if self.check_collision(self.current_piece):
            self.game_over = True

    def clear_lines(self):
        lines_cleared = 0
        for y in range(GRID_HEIGHT):
            if all(cell is not None for cell in self.grid[y]):
                del self.grid[y]
                self.grid.insert(0, [None] * GRID_WIDTH)
                lines_cleared += 1

        if lines_cleared > 0:
            self.score += lines_cleared * 100
            self.lines_cleared += lines_cleared
            self.health = min(100, self.health + 20 * lines_cleared)
            self.level = self.lines_cleared // 10 + 1
            self.fall_speed = max(5, DROP_SPEED - self.level * 2)

    def draw_home_button(self):
        # Dessin du carré de la maison
        pygame.draw.rect(screen, (200, 200, 200), self.home_button)
        
        # Dessin du toit de la maison
        points = [
            (self.home_button.x + self.home_button.width // 2, self.home_button.y - 5),
            (self.home_button.x - 5, self.home_button.y + self.home_button.height // 2),
            (self.home_button.x + self.home_button.width + 5, self.home_button.y + self.home_button.height // 2)
        ]
        pygame.draw.polygon(screen, (200, 200, 200), points)
        
        # Contour
        pygame.draw.rect(screen, (100, 100, 100), self.home_button, 2)
        pygame.draw.polygon(screen, (100, 100, 100), points, 2)

    def draw_menu(self):
        screen.fill((30, 30, 30))
        
        # Titre
        font_title = pygame.font.Font(None, 48)
        title = font_title.render("TETRIS PASTEL", True, (255, 255, 255))
        title_rect = title.get_rect(center=(WINDOW_WIDTH // 2, 100))
        screen.blit(title, title_rect)

        # Meilleurs scores
        font = pygame.font.Font(None, 36)
        scores = load_highscores()["scores"]
        
        score_text = font.render("Meilleurs Scores:", True, (255, 255, 255))
        score_rect = score_text.get_rect(center=(WINDOW_WIDTH // 2, 200))
        screen.blit(score_text, score_rect)

        y = 250
        for i, score in enumerate(scores):
            text = font.render(f"{i+1}. {score}", True, (255, 255, 255))
            rect = text.get_rect(center=(WINDOW_WIDTH // 2, y))
            screen.blit(text, rect)
            y += 40

        # Boutons
        button_font = pygame.font.Font(None, 32)
        
        # Bouton Retour au jeu
        pygame.draw.rect(screen, (50, 50, 50), self.resume_button)
        resume_text = button_font.render("Retour au jeu", True, (255, 255, 255))
        resume_rect = resume_text.get_rect(center=self.resume_button.center)
        screen.blit(resume_text, resume_rect)
        
        # Bouton Quitter
        pygame.draw.rect(screen, (50, 50, 50), self.quit_button)
        quit_text = button_font.render("Quitter", True, (255, 255, 255))
        quit_rect = quit_text.get_rect(center=self.quit_button.center)
        screen.blit(quit_text, quit_rect)

    def draw(self):
        if self.in_menu:
            self.draw_menu()
            return

        screen.fill((30, 30, 30))

        # Dessin de la grille
        grid_offset_x = (WINDOW_WIDTH - GRID_WIDTH * GRID_SIZE) // 2
        grid_offset_y = 100

        # Dessin du rectangle de la zone de jeu
        pygame.draw.rect(
            screen,
            (50, 50, 50),
            (grid_offset_x - 2, grid_offset_y - 2, 
             GRID_WIDTH * GRID_SIZE + 4, GRID_HEIGHT * GRID_SIZE + 4),
            2
        )

        for y in range(GRID_HEIGHT):
            for x in range(GRID_WIDTH):
                if self.grid[y][x]:
                    # Dessin du contour noir
                    pygame.draw.circle(
                        screen,
                        (0, 0, 0),
                        (x * GRID_SIZE + GRID_SIZE // 2 + grid_offset_x,
                         y * GRID_SIZE + GRID_SIZE // 2 + grid_offset_y),
                        GRID_SIZE // 2
                    )
                    # Dessin du cercle coloré
                    pygame.draw.circle(
                        screen,
                        self.grid[y][x],
                        (x * GRID_SIZE + GRID_SIZE // 2 + grid_offset_x,
                         y * GRID_SIZE + GRID_SIZE // 2 + grid_offset_y),
                        GRID_SIZE // 2 - 2
                    )

        # Dessin du bloc actuel
        if not self.paused:
            for y, row in enumerate(self.current_piece.shape):
                for x, cell in enumerate(row):
                    if cell:
                        # Dessin du contour noir
                        pygame.draw.circle(
                            screen,
                            (0, 0, 0),
                            ((self.current_piece.x + x) * GRID_SIZE + GRID_SIZE // 2 + grid_offset_x,
                             (self.current_piece.y + y) * GRID_SIZE + GRID_SIZE // 2 + grid_offset_y),
                            GRID_SIZE // 2
                        )
                        # Dessin du cercle coloré
                        pygame.draw.circle(
                            screen,
                            self.current_piece.color,
                            ((self.current_piece.x + x) * GRID_SIZE + GRID_SIZE // 2 + grid_offset_x,
                             (self.current_piece.y + y) * GRID_SIZE + GRID_SIZE // 2 + grid_offset_y),
                            GRID_SIZE // 2 - 2
                        )

        # Dessin du bouton maison
        self.draw_home_button()

        # Barre de vie
        pygame.draw.rect(screen, (50, 50, 50), (grid_offset_x, 20, 150, 15))
        pygame.draw.rect(screen, (0, 255, 0), (grid_offset_x, 20, self.health * 1.5, 15))

        # Score et niveau
        font = pygame.font.Font(None, 30)
        score_text = font.render(f"Score: {self.score}", True, (255, 255, 255))
        level_text = font.render(f"Level: {self.level}", True, (255, 255, 255))
        screen.blit(score_text, (grid_offset_x, 40))
        screen.blit(level_text, (grid_offset_x, 65))

        # Menu pause
        if self.paused:
            s = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
            s.set_alpha(128)
            s.fill((0, 0, 0))
            screen.blit(s, (0, 0))

            font = pygame.font.Font(None, 48)
            pause_text = font.render("PAUSE", True, (255, 255, 255))
            resume_text = font.render("Appuyez sur ECHAP", True, (255, 255, 255))
            
            pause_rect = pause_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 30))
            resume_rect = resume_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 30))
            
            screen.blit(pause_text, pause_rect)
            screen.blit(resume_text, resume_rect)

        pygame.display.flip()

def main():
    game = Game()
    clock = pygame.time.Clock()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Clic gauche
                    if game.home_button.collidepoint(event.pos):
                        running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:  # Retour au menu avec Echap
                    running = False
                elif event.key == pygame.K_LEFT:
                    if not game.check_collision(game.current_piece, -1):
                        game.current_piece.x -= 1
                elif event.key == pygame.K_RIGHT:
                    if not game.check_collision(game.current_piece, 1):
                        game.current_piece.x += 1
                elif event.key == pygame.K_DOWN:
                    if not game.check_collision(game.current_piece, 0, 1):
                        game.current_piece.y += 1
                elif event.key == pygame.K_UP:
                    game.current_piece.rotate()
                    if game.check_collision(game.current_piece):
                        game.current_piece.rotate()
                        game.current_piece.rotate()
                        game.current_piece.rotate()

        game.drop_timer += 1
        if game.drop_timer >= game.fall_speed:
            if not game.check_collision(game.current_piece, 0, 1):
                game.current_piece.y += 1
            else:
                game.lock_piece()
            game.drop_timer = 0

        game.draw()
        clock.tick(FPS)

    # Sauvegarder le score
    try:
        with open('highscores.json', 'r') as f:
            scores = json.load(f)
    except:
        scores = {"scores": []}

    scores["scores"].append(str(game.score))
    scores["scores"].sort(reverse=True)
    scores["scores"] = scores["scores"][:10]  # Garder les 10 meilleurs scores

    with open('highscores.json', 'w') as f:
        json.dump(scores, f)

    pygame.quit()
    os.system('python main_menu.py')  # Retour au menu principal

if __name__ == "__main__":
    main()
