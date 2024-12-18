from kivy.uix.progressbar import ProgressBar
from kivy.clock import Clock
import pygame

class AudioPlayer:
    def __init__(self):
        # Initialisation de pygame mixer
        pygame.mixer.init()

        self.progress_bar = ProgressBar(max=100)
        self.manual_position = None  # Variable pour stocker la position définie manuellement

        # Charger un fichier audio (remplacez par le chemin de votre fichier)
        pygame.mixer.music.load("musique/2Pac - Changes.mp3")
        pygame.mixer.music.play()

        # Mettre à jour la barre de progression périodiquement
        Clock.schedule_interval(self.update_progress_bar, 0.1)

    def get_position(self):
        # Retourne soit la position actuelle, soit la position définie manuellement
        if self.manual_position is not None:
            return self.manual_position
        return pygame.mixer.music.get_pos() / 1000.0

    def set_position(self, new_position):
        # Définit une nouvelle position et marque qu'une interaction a eu lieu
        print(f"Position ajustée à {new_position} secondes")
        pygame.mixer.music.set_pos(new_position)
        self.manual_position = new_position  # Enregistre la position définie manuellement

    def update_progress_bar(self, dt):
        # Met à jour la barre de progression
        current_position = self.get_position()
        duration = 200  # Exemple de durée totale, en secondes (mettez ici la durée réelle)

        if duration > 0:
            self.progress_bar.value = (current_position / duration) * 100

        # Réinitialise la position manuelle si elle est utilisée temporairement
        if self.manual_position is not None and pygame.mixer.music.get_pos() / 1000.0 > self.manual_position:
            self.manual_position = None
