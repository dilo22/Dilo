from librairie.graphique_interface import GraphiqueInterface
from enums.ecran_etat_enum import EcranEtat
from ecran.ecran import Ecran
from ecran.gestionnaire_etat_ecran import GestionnaireEtatEcran
import tkinter as tk
from tkinter import ttk
import time
from tkinter import messagebox

class EcranHorloge(Ecran):
    def __init__(self, graphique: GraphiqueInterface, gestionnaire_etat_ecran: GestionnaireEtatEcran):
        self.graphique = graphique
        self.gestionnaire_etat_ecran = gestionnaire_etat_ecran
        self.fenetre = None
        self.label_heure = None
        self.minuteur_label = None
        self.compte_a_rebours_label = None
        self.minuteur_seconds = 0
        self.compte_a_rebours_seconds = 0
        self.is_counting_down = False

    def initialiser_interface(self):
        """Initialisation de l'interface graphique"""
        self.fenetre = self.graphique.creer_fenetre("Horloge", 400, 300, "images/icone.ico")

        # Bouton retour
        self.retour_image = self.graphique.creer_image("images/retour.png", width=30, height=30)
        retour_button = self.graphique.creer_button(self.fenetre, image=self.retour_image, fonction=self.retour_action)
        retour_button.pack(side="top", anchor="nw", pady=10, padx=10)

        # Créer un notebook pour contenir les différentes vues (onglets)
        notebook = ttk.Notebook(self.fenetre)
        notebook.pack(expand=True, fill="both")

        # Onglet Horloge
        frame_horloge = ttk.Frame(notebook)
        notebook.add(frame_horloge, text="Horloge")

        # Label pour afficher l'heure
        self.label_heure = tk.Label(frame_horloge, font=("Arial", 40), background="#f0f0f0")
        self.label_heure.pack(expand=True)

        # Mise à jour de l'heure
        self.mettre_a_jour_heure()

        # Onglet Minuteur
        frame_minuteur = ttk.Frame(notebook)
        notebook.add(frame_minuteur, text="Minuteur")

        # Champ pour entrer le temps du minuteur en secondes
        self.minuteur_entry = tk.Entry(frame_minuteur, width=10)
        self.minuteur_entry.pack(pady=10)
        self.minuteur_entry.insert(0, "60")  # Valeur par défaut

        # Bouton pour démarrer le minuteur
        start_minuteur_button = tk.Button(frame_minuteur, text="Démarrer", command=self.demarrer_minuteur)
        start_minuteur_button.pack(pady=5)

        # Label pour afficher le minuteur
        self.minuteur_label = tk.Label(frame_minuteur, font=("Arial", 30))
        self.minuteur_label.pack(pady=10)

        # Onglet Compte à Rebours
        frame_compte_a_rebours = ttk.Frame(notebook)
        notebook.add(frame_compte_a_rebours, text="Compte à Rebours")

        # Champs pour entrer les minutes et secondes pour le compte à rebours
        self.minutes_entry = tk.Entry(frame_compte_a_rebours, width=5)
        self.minutes_entry.pack(side="left", padx=5, pady=10)
        self.minutes_entry.insert(0, "1")  # Valeur par défaut

        tk.Label(frame_compte_a_rebours, text=":").pack(side="left")

        self.seconds_entry = tk.Entry(frame_compte_a_rebours, width=5)
        self.seconds_entry.pack(side="left", padx=5, pady=10)
        self.seconds_entry.insert(0, "30")  # Valeur par défaut

        # Bouton pour démarrer le compte à rebours
        start_compte_a_rebours_button = tk.Button(frame_compte_a_rebours, text="Démarrer", command=self.demarrer_compte_a_rebours)
        start_compte_a_rebours_button.pack(pady=5)

        # Label pour afficher le compte à rebours
        self.compte_a_rebours_label = tk.Label(frame_compte_a_rebours, font=("Arial", 30))
        self.compte_a_rebours_label.pack(pady=10)

    def mettre_a_jour_heure(self):
        """Mettre à jour l'affichage de l'heure"""
        current_time = time.strftime('%H:%M:%S')
        self.label_heure.config(text=current_time)
        self.fenetre.after(1000, self.mettre_a_jour_heure)  # Mise à jour toutes les secondes

    def demarrer_minuteur(self):
        """Démarrer le minuteur"""
        try:
            self.minuteur_seconds = int(self.minuteur_entry.get())
            self.mettre_a_jour_minuteur()
        except ValueError:
            messagebox.showerror("Erreur", "Veuillez entrer un nombre valide de secondes.")

    def mettre_a_jour_minuteur(self):
        """Mettre à jour l'affichage du minuteur"""
        if self.minuteur_seconds > 0:
            self.minuteur_label.config(text=f"{self.minuteur_seconds} s")
            self.minuteur_seconds -= 1
            self.fenetre.after(1000, self.mettre_a_jour_minuteur)  # Mise à jour toutes les secondes
        else:
            self.minuteur_label.config(text="Terminé!")

    def demarrer_compte_a_rebours(self):
        """Démarrer le compte à rebours"""
        try:
            minutes = int(self.minutes_entry.get())
            seconds = int(self.seconds_entry.get())
            self.compte_a_rebours_seconds = minutes * 60 + seconds
            self.mettre_a_jour_compte_a_rebours()
        except ValueError:
            messagebox.showerror("Erreur", "Veuillez entrer des nombres valides pour les minutes et les secondes.")

    def mettre_a_jour_compte_a_rebours(self):
        """Mettre à jour l'affichage du compte à rebours"""
        if self.compte_a_rebours_seconds > 0:
            minutes = self.compte_a_rebours_seconds // 60
            seconds = self.compte_a_rebours_seconds % 60
            self.compte_a_rebours_label.config(text=f"{minutes:02d}:{seconds:02d}")
            self.compte_a_rebours_seconds -= 1
            self.fenetre.after(1000, self.mettre_a_jour_compte_a_rebours)  # Mise à jour toutes les secondes
        else:
            self.compte_a_rebours_label.config(text="Terminé!")

    def retour_action(self):
        """Action pour le bouton retour"""
        self.graphique.fermer_fenetre(self.fenetre)
        self.gestionnaire_etat_ecran.set_etat(EcranEtat.MENU)
        self.gestionnaire_etat_ecran.afficher_etat()

    def afficher(self):
        """Afficher l'écran"""
        self.graphique.ouvrir_fenetre(self.fenetre)
