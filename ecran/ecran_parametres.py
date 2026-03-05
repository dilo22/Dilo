from librairie.graphique_interface import GraphiqueInterface
from enums.ecran_etat_enum import EcranEtat
from ecran.ecran import Ecran
from ecran.gestionnaire_etat_ecran import GestionnaireEtatEcran
import tkinter as tk
from tkinter import messagebox, Scrollbar, Canvas


class EcranParametre(Ecran):
    def __init__(self, graphique: GraphiqueInterface, gestionnaire_etat_ecran: GestionnaireEtatEcran):
        self.graphique = graphique
        self.gestionnaire_etat_ecran = gestionnaire_etat_ecran
        self.root = None

    def initialiser_interface(self):
        self.root = self.graphique.creer_fenetre("Paramètres ", 850, 450, "images/icone.ico")

        # Conteneur principal (scrollable)
        self.regles_container = tk.Canvas(self.root)
        self.scrollbar = tk.Scrollbar(self.root, orient="vertical", command=self.regles_container.yview)
        self.scrollbar.pack(side="right", fill="y")
        self.regles_container.pack(side="left", fill="both", expand=True)

        self.frame_niveaux = tk.Frame(self.regles_container)
        self.regles_container.create_window((0, 0), window=self.frame_niveaux, anchor="nw")

        self.frame_niveaux.bind(
            "<Configure>",
            lambda e: self.regles_container.config(scrollregion=self.regles_container.bbox("all"))
        )
        self.regles_container.config(yscrollcommand=self.scrollbar.set)

        # Liste des applications + descriptions
        applications = [
            ("Calculatrice",
             "Réalise des opérations mathématiques simples : addition, soustraction, multiplication, division."),

            ("Convertisseur de Devises",
             "Convertit des devises à partir d’un taux de change. Choix de la devise source et cible."),

            ("Jeu de Serpent",
             "Jeu classique type Snake : mange pour grandir et évite les collisions avec les murs et ton corps."),

            ("Caisse Rapide (Compteur de monnaie)",
             "Permet de compter rapidement une somme en pièces/billets et de vérifier une monnaie ou une caisse."),

            ("Liste des Couleurs",
             "Catalogue de couleurs : double-clic sur une couleur pour l’appliquer en arrière-plan."),

            ("Matrice des Couleurs",
             "Affiche un aperçu d’une couleur avec ses codes RGB et HEX."),

            ("Sélecteur de Couleurs (RGB)",
             "Trois tirettes Rouge/Vert/Bleu pour créer une couleur personnalisée avec aperçu en temps réel."),

            ("Horloge / Minuteur / Compte à rebours",
             "Affiche l’heure actuelle et propose un minuteur ainsi qu’un compte à rebours configurable."),

            ("Générateur de Mot de Passe",
             "Génère des mots de passe sécurisés selon tes critères (longueur, types de caractères, etc.)."),

            ("Générateur de QR Code",
             "Crée un QR Code à partir d’un lien (URL) ou d’un texte fourni."),

            ("Convertisseur YouTube",
             "Récupère l’audio depuis une vidéo YouTube pour l’exporter (ex : en MP3 selon ton implémentation)."),

            ("Lecteur de son",
             "Lecture de fichiers audio directement dans l’application (contrôles de lecture selon le module)."),

            ("Dessin (mini Paint)",
             "Espace de dessin type Paint : dessiner librement, changer d’outil/taille, effacer, etc."),

            ("Audio to Text",
             "Conversion d’un fichier audio en texte (transcription) selon la fonctionnalité intégrée."),

            ("Convertisseur WebP",
             "Conversion d’images WebP vers d’autres formats (PNG/JPG… selon ton implémentation)."),

            ("Météo",
             "Affiche la météo d’une ville (conditions et informations principales)."),
        ]

        # Ajouter les sections dans l’UI
        for titre, texte in applications:
            self.ajouter_niveau(titre, texte)

        # Défilement molette
        self.regles_container.bind_all("<MouseWheel>", self._on_mousewheel)

    def _on_mousewheel(self, event):
        self.regles_container.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def ajouter_niveau(self, titre: str, texte: str):
        niveau = tk.LabelFrame(self.frame_niveaux, text=titre, padx=10, pady=10)
        niveau.pack(padx=10, pady=10, fill="both", expand=True)

        label_niveau = tk.Label(niveau, text=texte, justify="left", wraplength=760)
        label_niveau.pack(anchor="w", padx=10, pady=5)

        return niveau

    def afficher(self):
        """Afficher l'écran"""
        self.graphique.ouvrir_fenetre(self.root)