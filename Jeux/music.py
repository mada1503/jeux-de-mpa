import pygame
import os

class MusicPlayer:
    def __init__(self):
        pygame.mixer.init()
        self.menu_music = pygame.mixer.Sound(os.path.join("music", "menu_music.wav"))
        self.game_music = pygame.mixer.Sound(os.path.join("music", "game_music.wav"))
        self.coin_sound = pygame.mixer.Sound(os.path.join("music", "coin.wav"))
        self.jump_sound = pygame.mixer.Sound(os.path.join("music", "jump.wav"))
        self.game_over_sound = pygame.mixer.Sound(os.path.join("music", "game_over.wav"))
        
        # Réglage des volumes
        self.menu_music.set_volume(0.5)
        self.game_music.set_volume(0.5)
        self.coin_sound.set_volume(0.3)
        self.jump_sound.set_volume(0.3)
        self.game_over_sound.set_volume(0.5)

    def play_menu_music(self):
        self.menu_music.play(-1)  # -1 pour une boucle infinie

    def stop_menu_music(self):
        self.menu_music.stop()

    def play_game_music(self):
        self.game_music.play(-1)

    def stop_game_music(self):
        self.game_music.stop()

    def play_coin_sound(self):
        self.coin_sound.play()

    def play_jump_sound(self):
        self.jump_sound.play()

    def play_game_over_sound(self):
        self.game_over_sound.play()
