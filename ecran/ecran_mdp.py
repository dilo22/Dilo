from librairie.graphique_interface import GraphiqueInterface
from enums.ecran_etat_enum import EcranEtat
from ecran.ecran import Ecran
from ecran.gestionnaire_etat_ecran import GestionnaireEtatEcran
import tkinter as tk
import random
import string
from tkinter import messagebox

class EcranMotDePasse(Ecran):
    def __init__(self, graphique: GraphiqueInterface, gestionnaire_etat_ecran: GestionnaireEtatEcran):
        self.graphique = graphique
        self.gestionnaire_etat_ecran = gestionnaire_etat_ecran
        self.fenetre_mot_de_passe = None
        self.longueur_var = None
        self.inclure_maj_var = None
        self.inclure_min_var = None
        self.inclure_chiffres_var = None
        self.inclure_symboles_var = None
        self.mot_de_passe = None

    def initialiser_interface(self):
        # Création de la fenêtre principale
        self.fenetre_mot_de_passe = self.graphique.creer_fenetre("Générateur de Mot de Passe", 400, 300, "images/icone.ico")

        # Initialisation des variables Tkinter après la création de la fenêtre
        self.longueur_var = tk.IntVar(value=12)  # Longueur du mot de passe par défaut
        self.inclure_maj_var = tk.BooleanVar(value=True)
        self.inclure_min_var = tk.BooleanVar(value=True)
        self.inclure_chiffres_var = tk.BooleanVar(value=True)
        self.inclure_symboles_var = tk.BooleanVar(value=False)
        self.mot_de_passe = tk.StringVar()

        # Bouton retour
        self.retour_image = self.graphique.creer_image("images/retour.png", width=30, height=30)
        retour_button = self.graphique.creer_button(self.fenetre_mot_de_passe, fonction=self.retour_action, image=self.retour_image)
        retour_button.pack(pady=10)

        # Création des options pour personnaliser le mot de passe
        options_frame = self.graphique.creer_frame(self.fenetre_mot_de_passe)
        options_frame.pack(pady=10)

        # Longueur du mot de passe
        longueur_label = self.graphique.creer_label(options_frame, text="Longueur :")
        longueur_label.grid(row=0, column=0, padx=10)
        longueur_spinbox = tk.Spinbox(options_frame, from_=8, to_=32, textvariable=self.longueur_var)
        longueur_spinbox.grid(row=0, column=1, padx=10)

        # Cases à cocher pour inclure les types de caractères
        tk.Checkbutton(options_frame, text="Inclure Majuscules", variable=self.inclure_maj_var).grid(row=1, column=0, sticky="w", padx=10)
        tk.Checkbutton(options_frame, text="Inclure Minuscules", variable=self.inclure_min_var).grid(row=2, column=0, sticky="w", padx=10)
        tk.Checkbutton(options_frame, text="Inclure Chiffres", variable=self.inclure_chiffres_var).grid(row=3, column=0, sticky="w", padx=10)
        tk.Checkbutton(options_frame, text="Inclure Symboles", variable=self.inclure_symboles_var).grid(row=4, column=0, sticky="w", padx=10)

        # Bouton pour générer le mot de passe
        generer_button = self.graphique.creer_button(self.fenetre_mot_de_passe, fonction=self.generer_mot_de_passe, label="Générer")
        generer_button.pack(pady=10)

        # Affichage du mot de passe généré
        mot_de_passe_entry = tk.Entry(self.fenetre_mot_de_passe, textvariable=self.mot_de_passe, state="readonly", width=50)
        mot_de_passe_entry.pack(pady=10)

    def generer_mot_de_passe(self):
        if self.longueur_var is None:
            # Vérification pour s'assurer que les variables sont initialisées
            messagebox.showerror("Erreur", "L'interface n'a pas été initialisée correctement.")
            return
        
        longueur = self.longueur_var.get()
        inclure_maj = self.inclure_maj_var.get()
        inclure_min = self.inclure_min_var.get()
        inclure_chiffres = self.inclure_chiffres_var.get()
        inclure_symboles = self.inclure_symboles_var.get()

        caracteres = ""
        if inclure_maj:
            caracteres += string.ascii_uppercase
        if inclure_min:
            caracteres += string.ascii_lowercase
        if inclure_chiffres:
            caracteres += string.digits
        if inclure_symboles:
            caracteres += string.punctuation

        if not caracteres:
            messagebox.showerror("Erreur", "Veuillez sélectionner au moins un type de caractère.")
            return

        mot_de_passe_genere = "".join(random.choice(caracteres) for _ in range(longueur))
        self.mot_de_passe.set(mot_de_passe_genere)

    def retour_action(self):
        self.graphique.fermer_fenetre(self.fenetre_mot_de_passe)
        self.gestionnaire_etat_ecran.set_etat(EcranEtat.MENU)
        self.gestionnaire_etat_ecran.afficher_etat()

    def afficher(self):
        # Assurer que l'interface est initialisée avant de l'afficher
        if self.fenetre_mot_de_passe is None:
            self.initialiser_interface()
        self.graphique.ouvrir_fenetre(self.fenetre_mot_de_passe)
