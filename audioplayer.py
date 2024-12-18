import pygame
from mutagen.mp3 import MP3
pygame.mixer.init()


class AudioPlayer:
    def __init__(self, song_path):
        self.song_path = song_path
        self.is_playing = False
        self.manual_position = None
        self.position = None
        # Si vous utilisez pygame, par exemple, initialisez-le
        pygame.mixer.music.load(song_path)


    def play(self):
        pygame.mixer.music.play()
        self.is_playing = True

    def pause(self):
        pygame.mixer.music.pause()
        self.is_playing = False

    def resume(self):
        pygame.mixer.music.unpause()
        self.is_playing = True

    def stop(self):
        pygame.mixer.music.stop()
        self.is_playing = False

    def get_position(self):
        self.position = pygame.mixer.music.get_pos() / 1000.0
        return self.position

    def set_position(self,new_position):
        self.position = pygame.mixer.music.set_pos(new_position)
        self.position = pygame.mixer.music.get_pos() / 1000.0
        return self.position

    def get_audio_length(self):
        """Récupère la durée du fichier MP3"""
        try:
            audio = MP3(self.song_path)
            return audio.info.length  # Retourne la durée du fichier en secondes

        except Exception as e:
            print(f"[ERREUR] Impossible d'obtenir la durée du fichier : {e}")
            return 0

    def is_audio_playing(self):
        """Vérifie si la musique est en lecture"""
        if pygame.mixer.music.get_busy():
            return True
        return False
