import tkinter as tk
from librairie.graphique_interface import GraphiqueInterface
from enums.ecran_etat_enum import EcranEtat
from ecran.ecran import Ecran
from ecran.gestionnaire_etat_ecran import GestionnaireEtatEcran
from tkinter import messagebox

class EcranCalculatrice(Ecran):
    def __init__(self, graphique: GraphiqueInterface, gestionnaire_etat_ecran: GestionnaireEtatEcran):
        super().__init__()
        self.graphique = graphique
        self.gestionnaire_etat_ecran = gestionnaire_etat_ecran
        self.fenetre_calculatrice = None

    def initialiser_interface(self):
        # Création de la fenêtre principale
        self.fenetre_calculatrice = self.graphique.creer_fenetre("Calculatrice", 300, 400, "images/icone.ico")

        # Création de l'écran pour afficher les calculs
        self.ecran = tk.Entry(self.fenetre_calculatrice, font=("Arial", 18), borderwidth=2, relief="solid")
        self.ecran.grid(row=1, column=0, columnspan=4, padx=10, pady=10)

        # Définition des boutons de la calculatrice
        buttons = [
            ('7', 2, 0), ('8', 2, 1), ('9', 2, 2), ('/', 2, 3),
            ('4', 3, 0), ('5', 3, 1), ('6', 3, 2), ('*', 3, 3),
            ('1', 4, 0), ('2', 4, 1), ('3', 4, 2), ('-', 4, 3),
            ('0', 5, 0), ('.', 5, 1), ('+', 5, 2), ('=', 5, 3),
        ]

        for (text, row, col) in buttons:
            if text == "=":
                button = tk.Button(self.fenetre_calculatrice, text=text, command=self.calculate)
            else:
                button = tk.Button(self.fenetre_calculatrice, text=text, command=lambda t=text: self.button_click(t))
            button.grid(row=row, column=col, padx=5, pady=5, sticky="nsew")

        self.retour_image = self.graphique.creer_image("images/retour.png", width=30, height=30)
        retour_button = tk.Button(self.fenetre_calculatrice, image=self.retour_image, command=self.retour_action)
        retour_button.grid(row=0, column=0, padx=10, pady=10, sticky="nw")

        # Ajuster les poids pour que les boutons s'ajustent correctement
        for i in range(6):
            self.fenetre_calculatrice.grid_rowconfigure(i, weight=1)
            self.fenetre_calculatrice.grid_columnconfigure(i, weight=1)

    def button_click(self, text):
        current = self.ecran.get()
        self.ecran.delete(0, tk.END)
        self.ecran.insert(0, current + text)

    def calculate(self):
        try:
            expression = self.ecran.get()
            result = eval(expression)
            self.ecran.delete(0, tk.END)
            self.ecran.insert(0, result)
        except Exception:
            self.ecran.delete(0, tk.END)
            self.ecran.insert(0, "Erreur")

    def retour_action(self):
        self.graphique.fermer_fenetre(self.fenetre_calculatrice)
        self.gestionnaire_etat_ecran.set_etat(EcranEtat.MENU)  # Ou l'état approprié pour revenir à l'écran précédent
        self.gestionnaire_etat_ecran.afficher_etat()

    def afficher(self):
        self.graphique.ouvrir_fenetre(self.fenetre_calculatrice)
