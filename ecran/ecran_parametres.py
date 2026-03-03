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
        # Conteneur principal pour les niveaux
        self.regles_container = tk.Canvas(self.root)
        self.scrollbar = tk.Scrollbar(self.root, orient="vertical", command=self.regles_container.yview)
        self.scrollbar.pack(side="right", fill="y")
        self.regles_container.pack(side="left", fill="both", expand=True)

        # Frame qui contient tous les niveaux
        self.frame_niveaux = tk.Frame(self.regles_container)
        self.regles_container.create_window((0, 0), window=self.frame_niveaux, anchor='nw')

        self.frame_niveaux.bind("<Configure>", lambda e: self.regles_container.config(scrollregion=self.regles_container.bbox("all")))
        self.regles_container.config(yscrollcommand=self.scrollbar.set)

        # Ajouter les niveaux pour chaque application
        self.ajouter_niveau("Calculatrice", "Cette application permet de réaliser des opérations mathématiques simples comme l'addition, la soustraction, la multiplication et la division.")
        self.ajouter_niveau("Convertisseur de Devises", "Convertit des devises à partir d'un taux de change mis à jour. Vous pouvez choisir les devises sources et cibles.")
        self.ajouter_niveau("Jeu de Serpent", "C'est un jeu classique où le serpent mange des objets pour grandir. Vous devez éviter les collisions avec les murs et avec le serpent lui-même.")
        self.ajouter_niveau("Compteur de Caisse", "Cette application permet de suivre les transactions et de compter la somme dans la caisse.")
        self.ajouter_niveau("Liste des Couleurs", "Affiche une liste de couleurs avec leurs noms et valeurs RGB. Vous pouvez sélectionner une couleur en double-cliquant.")
        self.ajouter_niveau("Matrice des Couleurs", "Affiche une grille de couleurs où chaque cellule représente une couleur. Le nom et la valeur RGB sont affichés au survol de la souris.")
        self.ajouter_niveau("Sélecteur de Couleurs", "Permet de choisir une couleur en ajustant trois tirettes pour les composantes Rouge, Vert, et Bleu (RGB). La couleur résultante est affichée en temps réel.")
        self.ajouter_niveau("Horloge", "Affiche l'heure actuelle. Comprend également un minuteur et un compte à rebours que vous pouvez configurer.")
        self.ajouter_niveau("Générateur de Mot de Passe", "Génère des mots de passe sécurisés en combinant des lettres majuscules, minuscules, des chiffres et des symboles selon vos critères.")
        self.ajouter_niveau("Générateur de QR Code", "Crée des QR Codes à partir de texte ou d'URL fournis par l'utilisateur.")
        self.ajouter_niveau("Convertisseur YouTube", "Télécharge des vidéos depuis YouTube et les convertit en fichier MP3, en extrayant seulement l'audio.")

        # Gérer le défilement avec la molette de la souris
        self.regles_container.bind_all("<MouseWheel>", self._on_mousewheel)

    def _on_mousewheel(self, event):
        self.regles_container.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def ajouter_niveau(self, titre: str, texte: str):
        niveau = tk.LabelFrame(self.frame_niveaux, text=titre, padx=10, pady=10)
        niveau.pack(padx=10, pady=10, fill="both", expand=True)

        label_niveau = tk.Label(niveau, text=texte, justify="left")
        label_niveau.pack(anchor="w", padx=10, pady=5)

        return niveau
    
    def afficher(self):
        """Afficher l'écran"""
        self.graphique.ouvrir_fenetre(self.root)


