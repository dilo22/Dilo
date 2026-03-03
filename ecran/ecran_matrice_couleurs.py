from librairie.graphique_interface import GraphiqueInterface
from enums.ecran_etat_enum import EcranEtat
from ecran.ecran import Ecran
from ecran.gestionnaire_etat_ecran import GestionnaireEtatEcran
import tkinter as tk
from tkinter import messagebox, Scrollbar, Canvas

class Tooltip:
    """Classe pour gérer les Tooltips"""
    def __init__(self, widget, text=''):
        self.widget = widget
        self.text = text
        self.tooltip_window = None
        self.widget.bind("<Enter>", self.display_tooltip)
        self.widget.bind("<Leave>", self.remove_tooltip)

    def display_tooltip(self, event=None):
        x = self.widget.winfo_rootx() + 20
        y = self.widget.winfo_rooty() + 20
        self.tooltip_window = tw = tk.Toplevel(self.widget)
        tw.wm_overrideredirect(True)  # Supprime la bordure de la fenêtre
        tw.wm_geometry(f"+{x}+{y}")
        label = tk.Label(tw, text=self.text, background="yellow", relief='solid', borderwidth=1, font=("Arial", 10))
        label.pack(ipadx=1)

    def remove_tooltip(self, event=None):
        if self.tooltip_window:
            self.tooltip_window.destroy()
            self.tooltip_window = None

class EcranMatriceCouleurs(Ecran):
    def __init__(self, graphique: GraphiqueInterface, gestionnaire_etat_ecran: GestionnaireEtatEcran):
        self.graphique = graphique
        self.gestionnaire_etat_ecran = gestionnaire_etat_ecran
        self.couleurs = []
        self.fenetre = None
        self.canvas = None
        self.cadre_couleurs = None

    def charger_couleurs_depuis_fichier(self, fichier_path):
        """Chargement des couleurs depuis le fichier RGB en supprimant les doublons"""
        try:
            # Ensemble pour stocker les valeurs RGB, pour faciliter la vérification des doublons
            couleurs_uniques = set()
            with open(fichier_path, 'r') as fichier:
                for ligne in fichier:
                    # Supprime les espaces blancs au début et à la fin de la ligne
                    if ligne.strip():
                        # Suppression des doublons basés sur les valeurs RGB
                        rgb_valeurs, nom = ligne.strip().rsplit("\t\t", 1)
                        rgb = tuple(map(int, rgb_valeurs.strip().split()))
                        if rgb not in couleurs_uniques:
                            couleurs_uniques.add(rgb)
                            self.couleurs.append((rgb, nom))
        except FileNotFoundError:
            messagebox.showerror("Erreur", "Fichier non trouvé")
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur de lecture du fichier: {e}")

    def initialiser_interface(self):
        """Initialisation de l'interface graphique"""
        self.fenetre = self.graphique.creer_fenetre("Sélection des Couleurs", 412, 500, "images/icone.ico")

        # Bouton retour
        self.retour_image = self.graphique.creer_image("images/retour.png", width=30, height=30)
        retour_button = self.graphique.creer_button(self.fenetre, image=self.retour_image, fonction=self.retour_action)
        retour_button.pack(pady=10)

        # Canvas avec scrollbar pour permettre le défilement des couleurs
        self.canvas = self.graphique.creer_canvas(self.fenetre)
        self.canvas.pack(side="left", fill="both", expand=True)

        scrollbar = Scrollbar(self.fenetre, orient="vertical", command=self.canvas.yview)
        scrollbar.pack(side="right", fill="y")

        self.canvas.config(yscrollcommand=scrollbar.set)

        # Frame pour contenir les carreaux de couleur dans le Canvas
        self.cadre_couleurs = self.graphique.creer_frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.cadre_couleurs, anchor="nw")

        # Ajouter la prise en charge du scrolling avec la molette de la souris
        self.canvas.bind_all("<MouseWheel>", self.on_mousewheel)

        # Charger les couleurs depuis le fichier
        self.charger_couleurs_depuis_fichier("rgb.txt")

        # Afficher les couleurs en petits carreaux
        self.afficher_carreaux_couleurs()

        # Configurer le canvas pour ajuster la hauteur de défilement
        self.cadre_couleurs.update_idletasks()
        self.canvas.config(scrollregion=self.canvas.bbox("all"))

    def on_mousewheel(self, event):
        """Fonction pour gérer le scroll avec la molette"""
        self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")

    def afficher_carreaux_couleurs(self):
        """Affichage des petits carreaux de couleurs"""
        for idx, (rgb, nom) in enumerate(self.couleurs):
            r, g, b = rgb
            couleur_hex = f"#{r:02x}{g:02x}{b:02x}"

            # Créer un petit carré pour chaque couleur
            carre = tk.Frame(self.cadre_couleurs, bg=couleur_hex, width=30, height=30)
            carre.grid(row=idx // 10, column=idx % 10, padx=5, pady=5)

            # Ajouter le Tooltip
            Tooltip(carre, text=nom)

            # Ajouter le binding pour le double-clic
            carre.bind("<Double-Button-1>", lambda event, rgb=rgb, nom=nom, hex=couleur_hex: self.afficher_info_couleur(rgb, nom, hex))

    def afficher_info_couleur(self, rgb, nom, couleur_hex):
        """Affiche les informations de la couleur dans une fenêtre personnalisée avec un échantillon de couleur"""
        # Créer une nouvelle fenêtre
        info_fenetre = tk.Toplevel(self.fenetre)
        info_fenetre.title("Information")
        info_fenetre.geometry("300x300")
        info_fenetre.resizable(False, False)

        # Afficher les informations de la couleur
        label_nom = tk.Label(info_fenetre, text=f"Nom : {nom}", font=("Arial", 12))
        label_nom.pack(pady=10)

        r, g, b = rgb
        label_rgb = tk.Label(info_fenetre, text=f"RGB : {r}, {g}, {b}", font=("Arial", 12))
        label_rgb.pack(pady=5)

        label_hex = tk.Label(info_fenetre, text=f"Hex : {couleur_hex}", font=("Arial", 12))
        label_hex.pack(pady=5)

        # Afficher un échantillon de la couleur sous forme de triangle
        canvas = tk.Canvas(info_fenetre, width=100, height=100)
        canvas.pack(pady=10)
        points = [50, 10, 10, 90, 90, 90]
        canvas.create_polygon(points, fill=couleur_hex)

        # Bouton de fermeture
        bouton_fermer = tk.Button(info_fenetre, text="Fermer", command=info_fenetre.destroy)
        bouton_fermer.pack(pady=10)

    def retour_action(self):
        """Action pour le bouton retour"""
        self.graphique.fermer_fenetre(self.fenetre)
        self.gestionnaire_etat_ecran.set_etat(EcranEtat.MENU)
        self.gestionnaire_etat_ecran.afficher_etat()

    def afficher(self):
        """Afficher l'écran"""
        self.graphique.ouvrir_fenetre(self.fenetre)
