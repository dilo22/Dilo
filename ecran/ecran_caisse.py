import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk  # Pour manipuler les images
from librairie.graphique_interface import GraphiqueInterface
from enums.ecran_etat_enum import EcranEtat
from ecran.ecran import Ecran
from ecran.gestionnaire_etat_ecran import GestionnaireEtatEcran

class EcranCaisse(Ecran):
    def __init__(self, graphique: GraphiqueInterface, gestionnaire_etat_ecran: GestionnaireEtatEcran):
        self.graphique = graphique
        self.gestionnaire_etat_ecran = gestionnaire_etat_ecran
        self.fenetre_caisse = None
        self.montants = {}
        self.images = []
        self.totaux_monnaie = {}

    def initialiser_interface(self):
        # Création de la fenêtre principale
        self.fenetre_caisse = self.graphique.creer_fenetre("Comptage de Caisse", 600, 700, "images/icone.ico")
        #self.fenetre_caisse.configure(bg="#0b9eb5")
        # Bouton retour en haut à gauche
        self.retour_image = self.graphique.creer_image("images/retour.png", width=30, height=30)
        retour_button = tk.Button(self.fenetre_caisse, image=self.retour_image, command=self.retour_action)
        retour_button.grid(row=0, column=0, padx=10, pady=10, sticky="nw")

        # Champs pour entrer le nombre de pièces et billets avec les images
        self.creer_champs_pour_monnaie()

        # Bouton Reset pour réinitialiser les champs
        btn_reset = tk.Button(self.fenetre_caisse, text="Reset", command=self.reset_champs, bg="#0b9eb5")
        btn_reset.grid(row=0, column=2, columnspan=1, pady=20)

        # Label pour afficher le total général
        self.resultat_label = tk.Label(self.fenetre_caisse, text="Total: 0.00€", font=("Arial", 16))
        self.resultat_label.grid(row=0, column=3, columnspan=2, pady=10)

    def creer_champs_pour_monnaie(self):
        # Définition des valeurs pour les pièces et billets et leur chemin d'image
        monnaies = [
            ("1 centime", 0.01, "images/1_centime.png"),
            ("2 centimes", 0.02, "images/2_centime.png"),
            ("5 centimes", 0.05, "images/5_centime.png"),
            ("10 centimes", 0.10, "images/10_centime.png"),
            ("20 centimes", 0.20, "images/20_centime.png"),
            ("50 centimes", 0.50, "images/50_centime.png"),
            ("1 euro", 1.00, "images/1_euro.png"),
            ("2 euros", 2.00, "images/2_euro.png"),
            ("5 euros", 5.00, "images/5-euro.png"),
            ("10 euros", 10.00, "images/10-euro.png"),
            ("20 euros", 20.00, "images/20-euro.png"),
            ("50 euros", 50.00, "images/50-euro.png")
        ]

        # Créer les champs pour chaque pièce et billet avec une disposition sur une ligne
        for idx, (label, valeur, chemin_image) in enumerate(monnaies):
            # Charger l'image et l'afficher dans un label
            image = Image.open(chemin_image)
            image = image.resize((30, 30))  # Redimensionner les images à une taille plus petite
            photo = ImageTk.PhotoImage(image)
            self.images.append(photo)  # Stocker la référence pour éviter la suppression

            # Affichage de l'image
            image_label = tk.Label(self.fenetre_caisse, image=photo)
            image_label.grid(row=idx + 1, column=0, padx=10, pady=5)

            # Label du texte de la monnaie
            tk.Label(self.fenetre_caisse, text=label).grid(row=idx + 1, column=1, padx=10, pady=5, sticky="w")

            # Spinbox pour la quantité
            spinbox = tk.Spinbox(self.fenetre_caisse, from_=0, to=1000, width=5, command=self.mettre_a_jour_totaux)
            spinbox.grid(row=idx + 1, column=2, padx=10, pady=5)
            spinbox.bind("<KeyRelease>", lambda event, valeur=valeur: self.mettre_a_jour_totaux(event, valeur))  # Lier l'événement KeyRelease
            self.montants[valeur] = spinbox

            # Label pour afficher le total de la monnaie
            total_monnaie_label = tk.Label(self.fenetre_caisse, text="0.00€")
            total_monnaie_label.grid(row=idx + 1, column=3, padx=10, pady=5)
            self.totaux_monnaie[valeur] = total_monnaie_label

    def mettre_a_jour_totaux(self, event=None, valeur=None):
        try:
            total_general = 0
            for valeur, spinbox in self.montants.items():
                quantite = int(spinbox.get()) if spinbox.get() else 0
                total_monnaie = quantite * valeur
                self.totaux_monnaie[valeur].config(text=f"{total_monnaie:.2f}€")  # Mettre à jour le total de chaque monnaie
                total_general += total_monnaie
            self.resultat_label.config(text=f"Total: {total_general:.2f}€")  # Mettre à jour le total général
        except ValueError:
            messagebox.showerror("Erreur", "Veuillez entrer des quantités valides.")

    def reset_champs(self):
        # Remet tous les champs à zéro et réinitialise les totaux
        for valeur, spinbox in self.montants.items():
            spinbox.delete(0, tk.END)
            spinbox.insert(0, "0")
            self.totaux_monnaie[valeur].config(text="0.00€")
        # Réinitialiser l'affichage du total général
        self.resultat_label.config(text="Total: 0.00€")

    def retour_action(self):
        self.graphique.fermer_fenetre(self.fenetre_caisse)
        self.gestionnaire_etat_ecran.set_etat(EcranEtat.MENU)
        self.gestionnaire_etat_ecran.afficher_etat()

    def afficher(self):
        self.graphique.ouvrir_fenetre(self.fenetre_caisse)
