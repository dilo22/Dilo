from librairie.graphique_interface import GraphiqueInterface
from enums.ecran_etat_enum import EcranEtat
from ecran.ecran import Ecran
from ecran.gestionnaire_etat_ecran import GestionnaireEtatEcran
import random
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox, Scrollbar, Listbox
from tkinter import filedialog

class EcranListeCouleurs(Ecran):
    def __init__(self, graphique: GraphiqueInterface, gestionnaire_etat_ecran: GestionnaireEtatEcran):
        self.graphique = graphique
        self.gestionnaire_etat_ecran = gestionnaire_etat_ecran
        self.couleurs = []
        self.fenetre = None
        self.liste_couleurs = None
        self.frame_liste= None
    def charger_couleurs_depuis_fichier(self, fichier_path):
        try:
            with open(fichier_path, 'r') as fichier:
                for ligne in fichier:
                    rgb_valeurs, nom = ligne.strip().split("\t\t")
                    rgb = tuple(map(int, rgb_valeurs.split()))
                    self.couleurs.append((rgb, nom))
        except FileNotFoundError:
            messagebox.showerror("Erreur", "Fichier non trouvé")
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur de lecture du fichier: {e}")


    def initialiser_interface(self):
        # Création de la fenêtre principale
        #self.fenetre = tk.Tk()
        #self.fenetre.title("Sélection de Couleur")
        #self.fenetre.geometry("400x400")
        self.fenetre = self.graphique.creer_fenetre("Sélection des Couleurs", 400, 400,"images/icone.ico")


        # Bouton retour
        self.retour_image = self.graphique.creer_image("images/retour.png", width=30, height=30)
        retour_button = tk.Button(self.fenetre, image=self.retour_image, command=self.retour_action)
        retour_button.pack(pady=10)

        # Liste des couleurs avec scroll bar
        self.liste_couleurs = Listbox(self.fenetre)
        scrollbar = Scrollbar(self.fenetre)
        self.liste_couleurs.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.liste_couleurs.yview)
        scrollbar.pack(side="right", fill="y")
        self.liste_couleurs.pack(pady=20, padx=10, fill="both", expand=True)

        # Charger les couleurs depuis le fichier
        self.charger_couleurs_depuis_fichier("rgb.txt")

        # Remplir la liste avec les noms de couleur
        for _, nom in self.couleurs:
            self.liste_couleurs.insert(tk.END, nom)

        # Double clic pour changer la couleur de fond
        self.liste_couleurs.bind("<Double-Button-1>", self.changer_couleur)

    def changer_couleur(self, event):
        selection = self.liste_couleurs.get(self.liste_couleurs.curselection())
        self.liste_couleurs.config(bg=selection)
        self.fenetre.config(bg=selection)

        """selection = self.liste_couleurs.curselection()
        if selection:
            _, nom_couleur = self.couleurs[selection[0]]
            self.fenetre.config(bg=nom_couleur)"""

    def retour_action(self):
        self.graphique.fermer_fenetre(self.fenetre)
        self.gestionnaire_etat_ecran.set_etat(EcranEtat.MENU)  
        self.gestionnaire_etat_ecran.afficher_etat()

    def afficher(self):
        self.graphique.ouvrir_fenetre(self.fenetre)

