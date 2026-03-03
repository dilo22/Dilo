from librairie.graphique_interface import GraphiqueInterface
from enums.ecran_etat_enum import EcranEtat
from ecran.ecran import Ecran
from ecran.gestionnaire_etat_ecran import GestionnaireEtatEcran
import tkinter as tk

class EcranSelecteurCouleur(Ecran):
    def __init__(self, graphique: GraphiqueInterface, gestionnaire_etat_ecran: GestionnaireEtatEcran):
        self.graphique = graphique
        self.gestionnaire_etat_ecran = gestionnaire_etat_ecran
        self.fenetre = None
        self.scale_rouge = None
        self.scale_vert = None
        self.scale_bleu = None
        self.canvas = None
        self.rectangle = None

    def initialiser_interface(self):
        # Création de la fenêtre principale
        self.fenetre = self.graphique.creer_fenetre("Sélecteur de Couleur RGB", 500, 400, "images/icone.ico")

        # Bouton retour
        self.retour_image = self.graphique.creer_image("images/retour.png", width=30, height=30)
        retour_button = self.graphique.creer_button(self.fenetre, image=self.retour_image, fonction=self.retour_action)
        retour_button.pack(pady=10)
        

        # Échelle pour Rouge
        self.scale_rouge = tk.Scale(self.fenetre, from_=0, to=255, orient='horizontal', label='Rouge', command=self.update_color)
        self.scale_rouge.pack(fill='x')

        # Échelle pour Vert
        self.scale_vert = tk.Scale(self.fenetre, from_=0, to=255, orient='horizontal', label='Vert', command=self.update_color)
        self.scale_vert.pack(fill='x')

        # Échelle pour Bleu
        self.scale_bleu = tk.Scale(self.fenetre, from_=0, to=255, orient='horizontal', label='Bleu', command=self.update_color)
        self.scale_bleu.pack(fill='x')

        # Canvas pour afficher la couleur
        self.canvas = self.graphique.creer_canvas(self.fenetre, width=300, height=200)
        self.canvas.pack(pady=20)

        # Rectangle pour afficher la couleur
        self.rectangle = self.canvas.create_rectangle(10, 10, 190, 90, fill="#000000", outline="#000000")

    def update_color(self, event):
        """Met à jour la couleur du rectangle selon les valeurs des curseurs"""
        r = self.scale_rouge.get()
        v = self.scale_vert.get()
        b = self.scale_bleu.get()

        # Convertir les valeurs RGB en une couleur hexadécimale
        couleur = f'#{r:02x}{v:02x}{b:02x}'

        # Mettre à jour la couleur du rectangle
        self.canvas.itemconfig(self.rectangle, fill=couleur, outline=couleur)

    def retour_action(self):
        """Action pour le bouton retour"""
        self.graphique.fermer_fenetre(self.fenetre)
        self.gestionnaire_etat_ecran.set_etat(EcranEtat.MENU)
        self.gestionnaire_etat_ecran.afficher_etat()

    def afficher(self):
        """Afficher l'écran"""
        self.graphique.ouvrir_fenetre(self.fenetre)
