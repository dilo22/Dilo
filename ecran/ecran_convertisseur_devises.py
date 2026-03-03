import tkinter as tk
from tkinter import messagebox
from librairie.graphique_interface import GraphiqueInterface
from enums.ecran_etat_enum import EcranEtat
from ecran.ecran import Ecran
from ecran.gestionnaire_etat_ecran import GestionnaireEtatEcran

class EcranConvertisseurDevises(Ecran):
    def __init__(self, graphique: GraphiqueInterface, gestionnaire_etat_ecran: GestionnaireEtatEcran):
        self.graphique = graphique
        self.gestionnaire_etat_ecran = gestionnaire_etat_ecran
        self.fenetre_convertisseur = None

    def initialiser_interface(self):
        # Création de la fenêtre principale
        self.fenetre_convertisseur = self.graphique.creer_fenetre("Convertisseur de devises", 400, 300, "images/icone.ico")

        # Ajouter un bouton pour revenir en arrière
        self.retour_image = self.graphique.creer_image("images/retour.png", width=30, height=30)
        retour_button = tk.Button(self.fenetre_convertisseur, image=self.retour_image, command=self.retour_action)
        retour_button.grid(row=0, column=0, padx=10, pady=10, sticky="nw")

        # Labels et champs pour la conversion
        tk.Label(self.fenetre_convertisseur, text="Montant à convertir:").grid(row=1, column=0, padx=10, pady=10, sticky="e")
        self.montant_entry = tk.Entry(self.fenetre_convertisseur)
        self.montant_entry.grid(row=1, column=1, padx=10, pady=10)

        tk.Label(self.fenetre_convertisseur, text="Devise source:").grid(row=2, column=0, padx=10, pady=10, sticky="e")
        self.devise_source = tk.StringVar(value="USD")
        tk.OptionMenu(self.fenetre_convertisseur, self.devise_source, "USD", "EUR", "GBP").grid(row=2, column=1, padx=10, pady=10)

        tk.Label(self.fenetre_convertisseur, text="Devise cible:").grid(row=3, column=0, padx=10, pady=10, sticky="e")
        self.devise_cible = tk.StringVar(value="EUR")
        tk.OptionMenu(self.fenetre_convertisseur, self.devise_cible, "USD", "EUR", "GBP").grid(row=3, column=1, padx=10, pady=10)

        tk.Button(self.fenetre_convertisseur, text="Convertir", command=self.convertir).grid(row=4, column=0, columnspan=2, pady=20)

        self.resultat_label = tk.Label(self.fenetre_convertisseur, text="Résultat:")
        self.resultat_label.grid(row=5, column=0, columnspan=2, pady=10)

    def convertir(self):
        try:
            montant = float(self.montant_entry.get())
            source = self.devise_source.get()
            cible = self.devise_cible.get()

            # Conversion fictive
            taux_de_change = {
                ("USD", "EUR"): 0.85,
                ("EUR", "USD"): 1.18,
                ("USD", "GBP"): 0.75,
                ("GBP", "USD"): 1.33,
                ("EUR", "GBP"): 0.88,
                ("GBP", "EUR"): 1.14
            }

            if source == cible:
                resultat = montant
            else:
                taux = taux_de_change.get((source, cible), 1)
                resultat = montant * taux

            self.resultat_label.config(text=f"Résultat: {resultat:.2f} {cible}")

        except ValueError:
            messagebox.showerror("Erreur", "Veuillez entrer un montant valide.")

    def retour_action(self):
        self.graphique.fermer_fenetre(self.fenetre_convertisseur)
        self.gestionnaire_etat_ecran.set_etat(EcranEtat.MENU)  # Retour à l'écran menu ou autre état approprié
        self.gestionnaire_etat_ecran.afficher_etat()

    def afficher(self):
        self.graphique.ouvrir_fenetre(self.fenetre_convertisseur)
