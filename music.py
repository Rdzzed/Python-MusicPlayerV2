import os
from kivy.clock import Clock
from mutagen.mp3 import MP3
from pygame.sprite import collide_rect
import pygame
import audioplayer
from kivy.properties import NumericProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen, SlideTransition
from kivy.uix.slider import Slider
from list import list_of_title, list_of_songs, list_of_cover
from bg import BackgroundFloatLayout
from audioplayer import AudioPlayer
from home import *



class MusicScreen(Screen):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.main_layout = FloatLayout(size_hint=(1, 1))
        pygame.init()


        back_button = Button(size_hint=(None, None), size=(35, 25),pos_hint={'center_x': 0.1, 'center_y': 0.9},
                             background_normal='sign/bas.png', border=(0, 0, 0, 0))
        back_button.bind(on_press=self.go_back)
        self.main_layout.add_widget(back_button)

        # Sous-layout pour l'image de la musique
        self.cover_image = Image(size_hint=(None,None), size=(300,300),
                                 allow_stretch=True, pos_hint={'center_x': 0.5,'center_y': 0.65})
        self.main_layout.add_widget(self.cover_image)

        # Sous-layout pour le label
        self.label = Label(text="", font_size=25, width=20,height=20,pos_hint={'center_x': 0.5,'center_y': 0.35},size_hint=(None,None))
        self.main_layout.add_widget(self.label)

        # Sous-layout pour la barre de progression
        self.progress_bar_bg = Slider(size_hint=(None,None),width=350,height= 10, pos_hint={'center_x': 0.5,'center_y': 0.25},)
        self.progress_bar_bg.value_track_color = (0.62, 0.62, 0.62, 0)
        self.progress_bar_bg.cursor_size = (0, 0)

        self.progress_bar = Slider(max=100, min=0, value=0, size_hint=(None, None), width=350, height= 10,
                                   pos_hint={'center_x': 0.5,'center_y': 0.25}, )
        self.progress_bar.background_width = 0
        self.progress_bar.value_track = True
        self.progress_bar.value_track_color = (1, 1, 1, 1)
        self.progress_bar.cursor_image = 'rond.png'
        self.progress_bar.cursor_size = (20, 20)



        self.main_layout.add_widget(self.progress_bar_bg)
        self.main_layout.add_widget(self.progress_bar)


        # Sous-layout pour les boutons (prev, play/pause, next)
        prev_button = Button(size_hint=(None, None), size=(60, 60),pos_hint={'center_x': 0.3,'center_y': 0.15},
                             background_normal='sign/prev.png', border=(0, 0, 0, 0))
        prev_button.bind(on_press=self.prev_song)

        self.play_pause_button = Button(size_hint=(None, None), size=(60, 60),pos_hint={'center_x': 0.5,'center_y': 0.15},
                                        background_normal='sign/play.png', border=(0, 0, 0, 0))
        self.play_pause_button.bind(on_press=self.toggle_play_pause)

        next_button = Button(size_hint=(None, None), size=(60, 60),pos_hint={'center_x': 0.7,'center_y': 0.15},
                             background_normal='sign/next.png', border=(0, 0, 0, 0))
        next_button.bind(on_press=self.next_song)

        self.main_layout.add_widget(prev_button)
        self.main_layout.add_widget(next_button)
        self.main_layout.add_widget(self.play_pause_button)

        # Ajoutez l'image de fond et le layout principal
        self.layout = BackgroundFloatLayout()
        self.layout.add_widget(self.main_layout)
        self.add_widget(self.layout)


        self.audio_player = None
        self.current_song_path = None
        self.is_playing = False
        self.update_event = None
        self.is_user_interacting = False
        self.current_duration = 0
        self.manual_position = None
        self.progression = None


        self.progress_bar.bind(on_touch_down=self.on_slider_touch_down)
        self.progress_bar.bind(on_touch_up=self.on_slider_touch_up)
        self.progress_bar.bind(value=self.on_slider_value_change)




    def on_slider_touch_down(self,instance, touch):
        """Détecter quand l'utilisateur commence à interagir avec le slider."""
        if self.progress_bar.collide_point(*touch.pos):
            self.is_user_interacting = True  # Bloque la mise à jour automatique pendant l'interaction


    def on_slider_touch_up(self,instance, touch):
        """Détecter quand l'utilisateur arrête d'interagir avec le slider."""
        if self.progress_bar.collide_point(*touch.pos):
            self.is_user_interacting = False
            self.manual_position = self.progress_bar.value
            self.progression = self.manual_position
            self.audio_player.set_position(self.manual_position)





            print(f'Progres : {self.manual_position}')


    def on_slider_value_change(self, instance, value):
        """Mettre à jour la position en temps réel si l'utilisateur modifie le slider."""
        if self.is_user_interacting:
            self.progression = value




    def update_progress_bar(self, dt):

        if self.is_playing:
            if not self.is_user_interacting:
                self.progression = self.audio_player.get_position()
                if self.is_user_interacting:
                    self.progression = self.audio_player.set_position(self.progression)



                self.progress_bar.value = self.progression

            print(f"duration : {self.current_duration}")
            print(f"Progress: {self.progress_bar.value}")
            print(f"get_position() : {self.progression}")






    def pause_music(self):
        """Mettre la musique en pause."""
        if self.audio_player:
            self.audio_player.pause()
            self.is_playing = False
            if self.update_event:
                self.update_event.cancel()
            self.is_user_interacting = False

    def resume_music(self):
        """Reprendre la musique."""
        if self.audio_player:
            self.audio_player.resume()
            self.is_playing = True
            if self.update_event:
                self.update_event.cancel()


    def toggle_play_pause(self, instance):
        if self.is_playing:
            self.pause_music()
        else:
            self.resume_music()
        self.update_play_pause_buttons()

    def show_music_screen(self, cover, title):
        """Afficher l'écran de la musique sans relancer la lecture."""
        self.cover_image.source = cover
        self.label.text = title if title else self.list_of_title[self.current_song_index]
        self.manager.transition = SlideTransition(direction='up')
        self.manager.current = 'music'


    def play_music(self, song, cover):

        for index, current_song in enumerate(list_of_songs):
            if current_song == song:
                self.manager.current_song_index = index
                break

        if self.current_song_path == song and self.is_playing:
            self.show_music_screen(cover,title)
            return

        if self.current_song_path == song and not self.is_playing:
            self.resume_music()
            return

        if self.audio_player:
            self.audio_player.stop()

        try:
            print(f"Essayer de jouer la musique: {song}")  # Debug log
            self.audio_player = AudioPlayer(song)
            self.audio_player.play()
            self.current_duration =  self.audio_player.get_audio_length()

            self.progress_bar.max = self.current_duration

            self.progress_bar.value = 0

            if self.update_event:
                self.update_event.cancel()
            Clock.schedule_interval(self.update_progress_bar, 0.1)


        except Exception as e:
            print(f"Erreur lors de la lecture de la musique: {e}")  # Capture l'erreur
            self.audio_player = None
            return

        self.cover_image.source = cover
        self.manager.current_song_index = list_of_songs.index(song)
        self.label.text = list_of_title[self.manager.current_song_index]
        self.current_song_path = song
        self.is_playing = True
        self.play_pause_button.background_normal = 'sign/pause.png'
        self.update_play_pause_buttons()

        Clock.schedule_interval(self.update_progress_bar, 0.1)

    def next_song(self, instance):
        for index, song in enumerate(list_of_songs):
            if index == self.manager.current_song_index:
                self.manager.current_song_index = (index + 1) % len(list_of_songs)
                break
        self.play_music(list_of_songs[self.manager.current_song_index], list_of_cover[self.manager.current_song_index])

    def prev_song(self, instance):
        for index, song in enumerate(list_of_songs):
            if index == self.manager.current_song_index:
                self.manager.current_song_index = (index - 1) % len(list_of_songs)
                break
        self.play_music(list_of_songs[self.manager.current_song_index], list_of_cover[self.manager.current_song_index])

    def go_back(self, instance):
        self.manager.transition = SlideTransition(direction='down')
        self.manager.current = 'home'

        # Vérifier si 'home' a bien été initialisé avant de tenter d'accéder à ses méthodes
        home_screen = self.manager.get_screen('home')
        home_screen.show_mini_bar(self.cover_image.source, list_of_title[self.manager.current_song_index])

    def update_play_pause_buttons(self):
        """Mets à jour les icônes des boutons play/pause sur tous les écrans."""
        icon = 'sign/pause.png' if self.is_playing else 'sign/play.png'
        # Bouton play/pause de l'écran principal
        self.play_pause_button.background_normal = icon
        # Bouton play/pause du mini lecteur
        home_screen = self.manager.get_screen('home')
        home_screen.mini_bar_play_pause.background_normal = icon

