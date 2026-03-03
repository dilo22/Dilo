from librairie.graphique_interface import GraphiqueInterface
from enums.ecran_etat_enum import EcranEtat
from ecran.ecran import Ecran
from ecran.gestionnaire_etat_ecran import GestionnaireEtatEcran
import tkinter as tk
import yt_dlp as youtube_dl
from tkinter import messagebox

class EcranYoutube(Ecran):
    def __init__(self, graphique: GraphiqueInterface, gestionnaire_etat_ecran: GestionnaireEtatEcran):
        self.graphique = graphique
        self.gestionnaire_etat_ecran = gestionnaire_etat_ecran
        self.fenetre_youtube = None
        self.lien_var = None

    def initialiser_interface(self):
        # Création de la fenêtre principale
        self.fenetre_youtube = self.graphique.creer_fenetre("Télécharger Audio YouTube", 400, 200, "images/icone.ico")


        self.frame = self.graphique.creer_frame(self.fenetre_youtube, bg="#0b9eb5")
        self.frame.pack(fill='both', expand=True)

        self.top_frame = self.graphique.creer_frame(self.frame, bg="#0b9eb5")
        self.top_frame.pack(fill='x', anchor="w", pady=10)

        # Bouton retour avec une image
        self.retour_image = self.graphique.creer_image("images/retour.png", width=30, height=30)
        retour_button = self.graphique.creer_button(self.top_frame, fonction=self.retour_action, image=self.retour_image)
        retour_button.pack(side= "left", padx=10)


        # Initialisation de la variable Tkinter après la création de la fenêtre
        self.lien_var = tk.StringVar()

        # Bouton retour
        #self.retour_image = self.graphique.creer_image("images/retour.png", width=30, height=30)
        #retour_button = self.graphique.creer_button(self.frame, fonction=self.retour_action, image=self.retour_image)
        #retour_button.pack(pady=10)

        # Zone de saisie pour le lien YouTube
        lien_label = self.graphique.creer_label(self.frame, text="Lien YouTube :")
        lien_label.pack(pady=5)
        lien_entry = tk.Entry(self.frame, textvariable=self.lien_var, width=50)
        lien_entry.pack(pady=5)

        # Bouton pour télécharger l'audio
        telecharger_button = self.graphique.creer_button(self.frame, fonction=self.telecharger_audio, label="Télécharger")
        telecharger_button.pack(pady=10)

    def telecharger_audio(self):
        youtube_url = self.lien_var.get()
        if not youtube_url:
            messagebox.showerror("Erreur", "Veuillez entrer un lien YouTube valide.")
            return
        
        output_path = "C:/Users/hibah/Desktop/L3/Projet/musique"  # Répertoire de sauvegarde

        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': output_path + '/%(title)s.%(ext)s',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            #'ffmpeg_location': 'C:/ffmpeg-7.0.2/ffmpeg-7.0.2',  # Chemin vers ffmpeg
        }

        try:
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                ydl.download([youtube_url])
            messagebox.showinfo("Succès", "Téléchargement terminé avec succès.")
        except Exception as e:
            messagebox.showerror("Erreur", f"Le téléchargement a échoué : {e}")

    def retour_action(self):
        self.graphique.fermer_fenetre(self.fenetre_youtube)
        self.gestionnaire_etat_ecran.set_etat(EcranEtat.MENU)
        self.gestionnaire_etat_ecran.afficher_etat()

    def afficher(self):
        # Assurer que l'interface est initialisée avant de l'afficher
        if self.fenetre_youtube is None:
            self.initialiser_interface()
        self.graphique.ouvrir_fenetre(self.fenetre_youtube)
