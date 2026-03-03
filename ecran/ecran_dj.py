from librairie.graphique_interface import GraphiqueInterface
from enums.ecran_etat_enum import EcranEtat
from ecran.ecran import Ecran
from ecran.gestionnaire_etat_ecran import GestionnaireEtatEcran
import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog
import pygame
import os

class EcranDJ(Ecran):
    def __init__(self, graphique: GraphiqueInterface, gestionnaire_etat_ecran: GestionnaireEtatEcran):
        self.graphique = graphique
        self.gestionnaire_etat_ecran = gestionnaire_etat_ecran
        self.fenetre_principale = None

    def initialiser_interface(self):
        self.fenetre_principale = self.graphique.creer_fenetre("DJ APP", 800, 600, "images/icone.ico")

        self.frame = self.graphique.creer_frame(self.fenetre_principale, bg="#2b2b2b")
        self.frame.pack(fill='both', expand=True)

        self.top_frame = self.graphique.creer_frame(self.frame, bg="#2b2b2b")
        self.top_frame.pack(fill='x', anchor="w", pady=10)

        # Bouton retour avec une image
        self.retour_image = self.graphique.creer_image("images/retourdj.png", width=30, height=30)
        retour_button = self.graphique.creer_button(self.top_frame, fonction=self.retour_action, image=self.retour_image)
        retour_button.pack(side= "left", padx=10)

        # Initialiser pygame pour jouer la musique
        pygame.mixer.init()

        # Variables
        self.current_track = None
        self.volume = tk.DoubleVar(value=0.5)  # Volume de la musique
        self.is_paused = False
        self.is_playing = False

        # Label de titre
        title_label = tk.Label(self.frame, text="DJ Mixer", font=("Helvetica", 24, "bold"), bg="#2b2b2b", fg="white")
        title_label.pack(pady=20)

        # Bouton pour charger la musique
        load_button = tk.Button(self.frame, text="Charger une musique", command=self.load_music, font=("Helvetica", 16), bg="#4CAF50", fg="white", width=20)
        load_button.pack(pady=20)

        # Label pour afficher le nom de la chanson
        self.track_label = tk.Label(self.frame, text="", font=("Helvetica", 14), bg="#2b2b2b", fg="white")
        self.track_label.pack(pady=10)

        # Slider pour ajuster le volume
        volume_label = tk.Label(self.frame, text="Volume", font=("Helvetica", 14), bg="#2b2b2b", fg="white")
        volume_label.pack(pady=10)
        volume_slider = tk.Scale(self.frame, from_=0, to=1.0, resolution=0.01, orient=tk.HORIZONTAL, variable=self.volume, command=self.adjust_volume, length=400, bg="#2b2b2b", fg="white", troughcolor="gray", sliderlength=20)
        volume_slider.pack(pady=10)

        # Boutons de contrôle
        control_frame = tk.Frame(self.frame, bg="#2b2b2b")
        control_frame.pack(pady=20)

        play_button = tk.Button(control_frame, text="Play", command=self.play_music, font=("Helvetica", 16), bg="#4CAF50", fg="white", width=10)
        play_button.grid(row=0, column=0, padx=10)

        pause_button = tk.Button(control_frame, text="Pause/Replay", command=self.pause_music, font=("Helvetica", 16), bg="#FFC107", fg="white", width=15)
        pause_button.grid(row=0, column=1, padx=10)

        stop_button = tk.Button(control_frame, text="Stop", command=self.stop_music, font=("Helvetica", 16), bg="#f44336", fg="white", width=10)
        stop_button.grid(row=0, column=2, padx=10)

    def load_music(self):
        chemin = "C:/Users/hibah/Desktop/L3/Projet/musique"
        # Charger un fichier audio
        file_path = filedialog.askopenfilename(initialdir=chemin, filetypes=[("Fichiers audio", "*.mp3 *.wav *.ogg")])
        if file_path:
            try:
                self.current_track = file_path
                pygame.mixer.music.load(file_path)
                pygame.mixer.music.set_volume(self.volume.get())

                # Extraire et afficher le nom du fichier
                track_name = os.path.basename(file_path)
                self.track_label.config(text=f"Chanson: {track_name}")

                messagebox.showinfo("Chargement", "La musique a été chargée avec succès.")
                self.is_playing = False
                self.is_paused = False
            except Exception as e:
                messagebox.showerror("Erreur", f"Erreur lors du chargement de la musique : {e}")

    def play_music(self):
        if self.current_track:
            if not self.is_playing:
                pygame.mixer.music.play()
                self.is_playing = True
                self.is_paused = False

    def pause_music(self):
        if self.is_playing:
            if self.is_paused:
                pygame.mixer.music.unpause()
                self.is_paused = False
            else:
                pygame.mixer.music.pause()
                self.is_paused = True

    def stop_music(self):
        if self.is_playing:
            pygame.mixer.music.stop()
            self.is_playing = False
            self.is_paused = False

    def adjust_volume(self, volume):
        pygame.mixer.music.set_volume(self.volume.get())

    def retour_action(self):
        if self.is_playing:
            pygame.mixer.music.stop()
            self.is_playing = False
            self.is_paused = False
        self.graphique.fermer_fenetre(self.fenetre_principale)
        self.gestionnaire_etat_ecran.set_etat(EcranEtat.MENU)
        self.gestionnaire_etat_ecran.afficher_etat()

    def afficher(self):
        if self.fenetre_principale is None:
            self.initialiser_interface()
        self.graphique.ouvrir_fenetre(self.fenetre_principale)