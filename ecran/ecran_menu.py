from librairie.graphique_interface import GraphiqueInterface
from enums.ecran_etat_enum import EcranEtat
from ecran.ecran import Ecran
from ecran.gestionnaire_etat_ecran import GestionnaireEtatEcran
from tkinter import messagebox
import tkinter as tk

class EcranMenu(Ecran):
    def __init__(self, graphique: GraphiqueInterface, gestionnaire_etat_ecran: GestionnaireEtatEcran):
        # Initialisation du parent
        super().__init__()
        self.view_menu = None
        self.fenetre_menu = None
        self.gestionnaire_etat_ecran = gestionnaire_etat_ecran
        self.graphique = graphique

        self.images = []  # Liste pour stocker les images

    def ouvrir_calculatrice(self):
        self.graphique.fermer_fenetre(self.fenetre_menu)
        self.gestionnaire_etat_ecran.set_etat(EcranEtat.CALCULATRICE)
        self.gestionnaire_etat_ecran.afficher_etat()

    def ouvrir_caisse(self):
        self.graphique.fermer_fenetre(self.fenetre_menu)
        self.gestionnaire_etat_ecran.set_etat(EcranEtat.CAISSE)
        self.gestionnaire_etat_ecran.afficher_etat()

    def ouvrir_convertisseur(self):
        self.graphique.fermer_fenetre(self.fenetre_menu)
        self.gestionnaire_etat_ecran.set_etat(EcranEtat.DEVISES)
        self.gestionnaire_etat_ecran.afficher_etat()

    def ouvrir_jeu(self):
        self.graphique.fermer_fenetre(self.fenetre_menu)
        self.gestionnaire_etat_ecran.set_etat(EcranEtat.JEU_SERPENT)
        self.gestionnaire_etat_ecran.afficher_etat()

    def ouvrir_liste_couleurs(self):
        self.graphique.fermer_fenetre(self.fenetre_menu)
        self.gestionnaire_etat_ecran.set_etat(EcranEtat.LISTE_COULEURS)
        self.gestionnaire_etat_ecran.afficher_etat()

    def ouvrir_matrice_couleurs (self):
        self.graphique.fermer_fenetre(self.fenetre_menu)
        self.gestionnaire_etat_ecran.set_etat(EcranEtat.MATRICE_COULEURS)
        self.gestionnaire_etat_ecran.afficher_etat()

    def ouvrir_scales (self):
        self.graphique.fermer_fenetre(self.fenetre_menu)
        self.gestionnaire_etat_ecran.set_etat(EcranEtat.SCALES)
        self.gestionnaire_etat_ecran.afficher_etat()

    def ouvrir_horloge (self):
        self.graphique.fermer_fenetre(self.fenetre_menu)
        self.gestionnaire_etat_ecran.set_etat(EcranEtat.HORLOGE)
        self.gestionnaire_etat_ecran.afficher_etat()

    def ouvrir_mdp (self):
        self.graphique.fermer_fenetre(self.fenetre_menu)
        self.gestionnaire_etat_ecran.set_etat(EcranEtat.MDP)
        self.gestionnaire_etat_ecran.afficher_etat()

    def ouvrir_qrcode (self):
        self.graphique.fermer_fenetre(self.fenetre_menu)
        self.gestionnaire_etat_ecran.set_etat(EcranEtat.QRCODE)
        self.gestionnaire_etat_ecran.afficher_etat()

    def ouvrir_youtube (self):
        self.graphique.fermer_fenetre(self.fenetre_menu)
        self.gestionnaire_etat_ecran.set_etat(EcranEtat.YOUTUBE)
        self.gestionnaire_etat_ecran.afficher_etat()

    def ouvrir_dj (self):
        self.graphique.fermer_fenetre(self.fenetre_menu)
        self.gestionnaire_etat_ecran.set_etat(EcranEtat.DJ)
        self.gestionnaire_etat_ecran.afficher_etat()

    def ouvrir_dessin (self):
        #self.graphique.fermer_fenetre(self.fenetre_menu)
        self.gestionnaire_etat_ecran.set_etat(EcranEtat.DESSIN)
        self.gestionnaire_etat_ecran.afficher_etat()

    def ouvrir_audio_text (self):
        self.graphique.fermer_fenetre(self.fenetre_menu)
        self.gestionnaire_etat_ecran.set_etat(EcranEtat.AUDIOTEXT)
        self.gestionnaire_etat_ecran.afficher_etat()

    def ouvrir_convertisseur_images (self):
        self.graphique.fermer_fenetre(self.fenetre_menu)
        self.gestionnaire_etat_ecran.set_etat(EcranEtat.CONVERTISSEUR_IMAGES)
        self.gestionnaire_etat_ecran.afficher_etat()

    def ouvrir_meteo (self):
        self.graphique.fermer_fenetre(self.fenetre_menu)
        self.gestionnaire_etat_ecran.set_etat(EcranEtat.METEO)
        self.gestionnaire_etat_ecran.afficher_etat()

    def retour_action(self):
        self.graphique.fermer_fenetre(self.fenetre_menu)
        self.gestionnaire_etat_ecran.set_etat(EcranEtat.MAIN)
        self.gestionnaire_etat_ecran.afficher_etat()

    def initialiser_interface(self):
        # Création de la fenêtre principale
        self.fenetre_menu = self.graphique.creer_fenetre("Menu", 820, 600, "images/icone.ico")


        # Création de la barre de menu
        self.menu_bar = tk.Menu(self.fenetre_menu)
        # Création du sous-menu "Fichier"
        menu_fichier = tk.Menu(self.menu_bar, tearoff=0)
        menu_fichier.add_command(label="Ouvrir", command=self.ouvrir_fichier)
        menu_fichier.add_command(label="Enregistrer", command=self.enregistrer_fichier)
        menu_fichier.add_separator()  # Ajoute une ligne de séparation
        menu_fichier.add_command(label="Quitter", command=self.fenetre_menu.quit)

        # Ajout du sous-menu "Fichier" à la barre de menu
        self.menu_bar.add_cascade(label="Fichier", menu=menu_fichier)

        # Création du sous-menu "Aide"
        menu_aide = tk.Menu(self.menu_bar, tearoff=0)
        menu_aide.add_command(label="À propos", command=self.a_propos)

        # Ajout du sous-menu "Aide" à la barre de menu
        self.menu_bar.add_cascade(label="Aide", menu=menu_aide)

        # Ajout de la barre de menu à la fenêtre principale
        self.fenetre_menu.config(menu=self.menu_bar)



        # On crée l'image retour
        self.retour_image = self.graphique.creer_image("images/retour.png", 50, 50)

        # On crée le bouton retour qui va contenir l'image retour
        retour_button = self.graphique.creer_button(frame=self.fenetre_menu, fonction=lambda: self.retour_action(), bg="#ffffff",
                                                    image=self.retour_image, width=50, height=50)
        retour_button.pack(side='left', pady=10, padx=10)

        # Créer un canvas et une scrollbar
        self.canvas = tk.Canvas(self.fenetre_menu, bg="#0b9eb5")
        scrollbar = tk.Scrollbar(self.fenetre_menu, orient="vertical", command=self.canvas.yview)

        # Créer un frame à l'intérieur du canvas pour contenir les boutons
        self.frame_projets = tk.Frame(self.canvas, bg="#0b9eb5")

        # Ajouter le frame au canvas
        self.canvas.create_window((0, 0), window=self.frame_projets, anchor="nw")
        self.canvas.update_idletasks()  # Mettre à jour les tâches d'attente pour avoir la bonne taille

        # Configuration de la scrollbar
        scrollbar.config(command=self.canvas.yview)
        self.canvas.config(yscrollcommand=scrollbar.set)

        # Disposer le canvas et la scrollbar
        self.canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
    
        # Ajouter un event pour mettre à jour la taille du canvas lorsque le frame change de taille
        self.frame_projets.bind("<Configure>", lambda e: self.canvas.config(scrollregion=self.canvas.bbox("all")))

        # Gérer le défilement avec la molette de la souris
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)

        # Création des boutons projets et stockage des images
        btn_calculatrice = self.creer_carre(self.frame_projets, "images/calculatrice.png", "Calculatrice", self.ouvrir_calculatrice)
        btn_convertisseur = self.creer_carre(self.frame_projets, "images/convertisseur.png", "Convertisseur", self.ouvrir_convertisseur)
        btn_jeu = self.creer_carre(self.frame_projets, "images/jeu.png", "Jeu de serpent", self.ouvrir_jeu)
        btn_caisse = self.creer_carre(self.frame_projets, "images/caisse.png", "Caisse rapide", self.ouvrir_caisse)
        btn_liste_couleurs = self.creer_carre(self.frame_projets, "images/listecouleurs.png", "Liste Couleurs", self.ouvrir_liste_couleurs)
        btn_matrice_couleurs = self.creer_carre(self.frame_projets, "images/matricecouleurs.png", "Matrice Couleurs", self.ouvrir_matrice_couleurs)
        btn_selecteur = self.creer_carre(self.frame_projets, "images/scales.png", "Tirettes", self.ouvrir_scales)
        btn_horloge = self.creer_carre(self.frame_projets, "images/horloge.png", "Horloge", self.ouvrir_horloge)
        btn_mdp = self.creer_carre(self.frame_projets, "images/mdp.png", "Mot de passe", self.ouvrir_mdp)
        btn_qrcode = self.creer_carre(self.frame_projets, "images/qrcode.png", "QR Code", self.ouvrir_qrcode)
        btn_youtube = self.creer_carre(self.frame_projets, "images/youtube.png", "Youtube", self.ouvrir_youtube)
        btn_dj = self.creer_carre(self.frame_projets, "images/dj.png", "Dj", self.ouvrir_dj)
        btn_dessin = self.creer_carre(self.frame_projets, "images/dessin.png", "Dessin", self.ouvrir_dessin)
        btn_audio_text = self.creer_carre(self.frame_projets, "images/audio_text.png", "Audio to Text", self.ouvrir_audio_text)
        btn_convertisseur_images = self.creer_carre(self.frame_projets, "images/webp.png", "Convertisseur Webp", self.ouvrir_convertisseur_images)
        btn_meteo = self.creer_carre(self.frame_projets, "images/meteo.png", "Météo", self.ouvrir_meteo)

        # Disposer les boutons dans le frame
        btn_calculatrice.grid(row=0, column=0, padx=10, pady=20)
        btn_convertisseur.grid(row=0, column=1, padx=10, pady=20)
        btn_jeu.grid(row=0, column=2, padx=10, pady=20)
        btn_caisse.grid(row=0, column=3, padx=10, pady=20)

        btn_liste_couleurs.grid(row=1, column=0, padx=10, pady=20)
        btn_matrice_couleurs.grid(row=1, column=1, padx=10, pady=20)
        btn_selecteur.grid(row=1, column=2, padx=10, pady=20)
        btn_horloge.grid(row=1, column=3, padx=10, pady=20)

        btn_mdp.grid(row=2, column=0, padx=10, pady=20)
        btn_qrcode.grid(row=2, column=1, padx=10, pady=20)
        btn_youtube.grid(row=2, column=2, padx=10, pady=20)
        btn_dj.grid(row=2, column=3, padx=10, pady=20)

        btn_dessin.grid(row=3, column=0, padx=10, pady=20)
        btn_audio_text.grid(row=3, column=1, padx=10, pady=20)
        btn_convertisseur_images.grid(row=3, column=2, padx=10, pady=20)
        btn_meteo.grid(row=3, column=3, padx=10, pady=20)

    def ouvrir_fichier(self):
        messagebox.showinfo("Ouvrir", "Fonction d'ouverture de fichier")

    def enregistrer_fichier(self):
        messagebox.showinfo("Enregistrer", "Fonction d'enregistrement de fichier")

    def a_propos(self):
        self.graphique.fermer_fenetre(self.fenetre_menu)
        self.gestionnaire_etat_ecran.set_etat(EcranEtat.AIDE)
        self.gestionnaire_etat_ecran.afficher_etat()

    def _on_mousewheel(self, event):
        """Gérer le défilement avec la molette de la souris"""
        self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units") 

    def creer_carre(self, frame, chemin_image: str, label: str, fonction):
        """
        Crée un bouton carré avec une image au-dessus et un texte en dessous.

        Args:
            frame : le frame où sera placé le bouton et le texte
            chemin_image (str) : le chemin de l'image à afficher
            label (str) : le texte à afficher sous l'image
            fonction : la fonction à appeler lors du clic sur le bouton

        Return:
            frame_bouton : Retourne un frame contenant l'image et le texte.
        """
        # Créer une image redimensionnée pour le bouton
        image = self.graphique.creer_image(chemin_image, width=100, height=100)
        self.images.append(image)
        # Créer un frame pour contenir le bouton et le label
        frame_bouton = tk.Frame(frame, padx=10, pady=10)

        # Créer le bouton avec l'image
        bouton = self.graphique.creer_button(
            frame_bouton, 
            fonction=fonction, 
            image=image, 
            width=100, 
            height=100
        )
        bouton.pack()

        # Créer le label avec le texte en dessous du bouton
        label_widget = self.graphique.creer_label(
            frame_bouton, 
            text=label, 
            font=("Arial", 12, "bold"),  # Texte en gras pour plus de visibilité
            padx=10, pady=5  # Ajout d'un padding pour espacer le texte de l'image
        )
        label_widget.pack()

        return frame_bouton

    def afficher(self):
        # Ouvrir la fenêtre du menu
        self.graphique.ouvrir_fenetre(self.fenetre_menu)
