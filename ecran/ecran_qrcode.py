import qrcode
from PIL import Image, ImageTk
import tkinter as tk
from tkinter import colorchooser, filedialog, messagebox
from librairie.graphique_interface import GraphiqueInterface
from enums.ecran_etat_enum import EcranEtat
from ecran.ecran import Ecran
from ecran.gestionnaire_etat_ecran import GestionnaireEtatEcran
import pyperclip

class EcranQRCode(Ecran):
    def __init__(self, graphique: GraphiqueInterface, gestionnaire_etat_ecran: GestionnaireEtatEcran):
        self.graphique = graphique
        self.gestionnaire_etat_ecran = gestionnaire_etat_ecran
        self.fenetre = None
        self.qr_image = None
        self.qr_image_pil = None  # Pour stocker l'image PIL du QR code

    def initialiser_interface(self):
        self.fenetre = self.graphique.creer_fenetre("Générateur de QR Code", 500, 650, "images/icone.ico")


        self.frame = self.graphique.creer_frame(self.fenetre, bg="#0b9eb5")
        self.frame.pack(fill='both', expand=True)

        self.top_frame = self.graphique.creer_frame(self.frame, bg="#0b9eb5")
        self.top_frame.pack(fill='x', anchor="w", pady=10)

        # Bouton retour avec une image
        self.retour_image = self.graphique.creer_image("images/retour.png", width=30, height=30)
        retour_button = self.graphique.creer_button(self.top_frame, fonction=self.retour_action, image=self.retour_image)
        retour_button.pack(side= "left", padx=10)



        # Champ pour entrer le texte à encoder
        self.label = self.graphique.creer_label(self.frame, text="Entrez le texte/URL :")
        self.label.pack(pady=5)
        self.texte_entry = tk.Entry(self.frame)
        self.texte_entry.pack(pady=5)

        # Bouton pour choisir la couleur du QR code
        self.couleur_bouton = self.graphique.creer_button(self.frame, fonction=self.choisir_couleur, label="Choisir la couleur")
        self.couleur_bouton.pack(pady=5)

        # Bouton pour générer le QR code
        self.generer_bouton = self.graphique.creer_button(self.frame, fonction=self.generer_qr_code, label="Générer QR Code")
        self.generer_bouton.pack(pady=5)

        # Affichage du QR code
        self.qr_label = tk.Label(self.frame)
        self.qr_label.pack(pady=5)

        # Boutons pour sauvegarder et copier le QR code
        self.sauvegarder_bouton = self.graphique.creer_button(self.frame, fonction=self.sauvegarder_qr_code, label="Sauvegarder")
        self.sauvegarder_bouton.pack(pady=5)
        self.copier_bouton = self.graphique.creer_button(self.frame, fonction=self.copier_qr_code, label="Copier")
        self.copier_bouton.pack(pady=5)


        # Couleur par défaut pour le QR code
        self.qr_couleur = 'black'

    def choisir_couleur(self):
        color = colorchooser.askcolor(title="Choisir la couleur du QR Code")
        if color[1]:
            self.qr_couleur = color[1]

    def generer_qr_code(self):
        texte = self.texte_entry.get()
        if not texte:
            messagebox.showwarning("Attention", "Le champ texte est vide.")
            return

        qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=10, border=4)
        qr.add_data(texte)
        qr.make(fit=True)

        # Créer l'image PIL du QR code
        self.qr_image_pil = qr.make_image(fill_color=self.qr_couleur, back_color="white")

        # Convertir l'image PIL en PhotoImage pour l'affichage dans Tkinter
        self.qr_image = ImageTk.PhotoImage(self.qr_image_pil)
        self.qr_label.config(image=self.qr_image)

    def sauvegarder_qr_code(self):
        if self.qr_image_pil:
            fichier_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")])
            if fichier_path:
                self.qr_image_pil.save(fichier_path)
        else:
            messagebox.showwarning("Attention", "Aucun QR code à sauvegarder.")

    def copier_qr_code(self):
        texte = self.texte_entry.get()
        if texte:
            # Copier le texte dans le presse-papiers
            pyperclip.copy(texte)
            messagebox.showinfo("Succès", "Le texte du QR code a été copié dans le presse-papiers.")
        else:
            messagebox.showwarning("Attention", "Aucun texte à copier.")

    def retour_action(self):
        self.graphique.fermer_fenetre(self.fenetre)
        self.gestionnaire_etat_ecran.set_etat(EcranEtat.MENU)
        self.gestionnaire_etat_ecran.afficher_etat()

    def afficher(self):
        self.graphique.ouvrir_fenetre(self.fenetre)
