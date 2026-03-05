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
        self.fenetre_menu = self.graphique.creer_fenetre("Menu", 980, 640, "images/icone.ico")
        self.fenetre_menu.configure(bg="#F6F7FB")

        # ---- Menu bar (tu peux garder tel quel) ----
        self.menu_bar = tk.Menu(self.fenetre_menu)
        menu_fichier = tk.Menu(self.menu_bar, tearoff=0)
        menu_fichier.add_command(label="Ouvrir", command=self.ouvrir_fichier)
        menu_fichier.add_command(label="Enregistrer", command=self.enregistrer_fichier)
        menu_fichier.add_separator()
        menu_fichier.add_command(label="Quitter", command=self.fenetre_menu.quit)
        self.menu_bar.add_cascade(label="Fichier", menu=menu_fichier)

        menu_aide = tk.Menu(self.menu_bar, tearoff=0)
        menu_aide.add_command(label="À propos", command=self.a_propos)
        self.menu_bar.add_cascade(label="Aide", menu=menu_aide)
        self.fenetre_menu.config(menu=self.menu_bar)

        # ---- Header moderne ----
        header = tk.Frame(self.fenetre_menu, bg="#F6F7FB")
        header.pack(fill="x", padx=18, pady=(14, 10))

        self.retour_image = self.graphique.creer_image("images/retour.png", 26, 26)
        btn_retour = tk.Button(
            header,
            image=self.retour_image,
            command=self.retour_action,
            bd=0,
            bg="#F6F7FB",
            activebackground="#F6F7FB",
            cursor="hand2",
        )
        btn_retour.pack(side="left")

        title_block = tk.Frame(header, bg="#F6F7FB")
        title_block.pack(side="left", padx=12)

        tk.Label(
            title_block,
            text="Dilo — Menu",
            font=("Segoe UI", 18, "bold"),
            bg="#F6F7FB",
            fg="#111827",
        ).pack(anchor="w")

        tk.Label(
            title_block,
            text="Choisis une application à lancer",
            font=("Segoe UI", 10),
            bg="#F6F7FB",
            fg="#6B7280",
        ).pack(anchor="w")

        # ---- Barre de recherche ----
        search_wrap = tk.Frame(self.fenetre_menu, bg="#F6F7FB")
        search_wrap.pack(fill="x", padx=18, pady=(0, 12))

        self.search_var = tk.StringVar()
        self.search_entry = tk.Entry(
            search_wrap,
            textvariable=self.search_var,
            font=("Segoe UI", 11),
            relief="flat",
            bg="#FFFFFF",
            fg="#111827",
        )
        self.search_entry.pack(fill="x", ipady=10)
        self.search_entry.insert(0, "Rechercher une app…")
        self.search_entry.bind("<FocusIn>", self._search_focus_in)
        self.search_entry.bind("<FocusOut>", self._search_focus_out)

        # ---- Zone scrollable (canvas + frame) ----
        content = tk.Frame(self.fenetre_menu, bg="#F6F7FB")
        content.pack(fill="both", expand=True, padx=18, pady=(0, 14))

        self.canvas = tk.Canvas(content, bg="#F6F7FB", highlightthickness=0)
        scrollbar = tk.Scrollbar(content, orient="vertical", command=self.canvas.yview)
        scrollbar.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)
        self.canvas.configure(yscrollcommand=scrollbar.set)

        self.frame_projets = tk.Frame(self.canvas, bg="#F6F7FB")
        self.canvas_window = self.canvas.create_window((0, 0), window=self.frame_projets, anchor="nw")

        self.frame_projets.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.canvas.bind("<Configure>", self._on_canvas_resize)
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)

        # ---- Data apps ----
        self.apps = [
            ("Calculatrice", "images/calculatrice.png", self.ouvrir_calculatrice),
            ("Convertisseur", "images/convertisseur.png", self.ouvrir_convertisseur),
            ("Jeu de serpent", "images/jeu.png", self.ouvrir_jeu),
            ("Caisse rapide", "images/caisse.png", self.ouvrir_caisse),
            ("Liste Couleurs", "images/listecouleurs.png", self.ouvrir_liste_couleurs),
            ("Matrice Couleurs", "images/matricecouleurs.png", self.ouvrir_matrice_couleurs),
            ("Tirettes (RGB)", "images/scales.png", self.ouvrir_scales),
            ("Horloge", "images/horloge.png", self.ouvrir_horloge),
            ("Mot de passe", "images/mdp.png", self.ouvrir_mdp),
            ("QR Code", "images/qrcode.png", self.ouvrir_qrcode),
            ("YouTube", "images/youtube.png", self.ouvrir_youtube),
            ("DJ", "images/dj.png", self.ouvrir_dj),
            ("Dessin", "images/dessin.png", self.ouvrir_dessin),
            ("Audio to Text", "images/audio_text.png", self.ouvrir_audio_text),
            ("Convertisseur WebP", "images/webp.png", self.ouvrir_convertisseur_images),
            ("Météo", "images/meteo.png", self.ouvrir_meteo),
        ]

        # Précharger les images et créer les cartes
        self._cards = []
        self._images = []
        for name, icon_path, cmd in self.apps:
            img = self.graphique.creer_image(icon_path, 44, 44)
            self._images.append(img)
            card = self.creer_carte_modern(self.frame_projets, name, img, cmd)
            self._cards.append((name, card))

        # Layout initial + filtre en live
        self._layout_cards()
        self.search_var.trace_add("write", lambda *_: self._filter_cards())
    def creer_carte_modern(self, parent, titre, image, command):
        card = tk.Frame(parent, bg="#FFFFFF", bd=0, highlightthickness=1, highlightbackground="#E5E7EB")
        card.configure(cursor="hand2")

        # coins arrondis -> Tkinter ne gère pas nativement, mais ce style reste moderne sans.
        inner = tk.Frame(card, bg="#FFFFFF")
        inner.pack(fill="both", expand=True, padx=14, pady=14)

        icon_wrap = tk.Frame(inner, bg="#F3F4F6")
        icon_wrap.pack(anchor="w")
        tk.Label(icon_wrap, image=image, bg="#F3F4F6").pack(padx=10, pady=10)

        tk.Label(
            inner,
            text=titre,
            font=("Segoe UI", 11, "bold"),
            bg="#FFFFFF",
            fg="#111827",
        ).pack(anchor="w", pady=(10, 0))

        tk.Label(
            inner,
            text="Ouvrir",
            font=("Segoe UI", 9),
            bg="#FFFFFF",
            fg="#6B7280",
        ).pack(anchor="w", pady=(4, 0))

        # Clic partout
        def _click(_):
            command()

        card.bind("<Button-1>", _click)
        for w in (inner, icon_wrap):
            w.bind("<Button-1>", _click)

        # Hover
        def _enter(_):
            card.config(highlightbackground="#CBD5E1")
            card.config(bg="#FFFFFF")
        def _leave(_):
            card.config(highlightbackground="#E5E7EB")

        card.bind("<Enter>", _enter)
        card.bind("<Leave>", _leave)

        return card

    def _search_focus_in(self, event):
        if self.search_entry.get().strip() == "Rechercher une app…":
            self.search_entry.delete(0, tk.END)


    def _search_focus_out(self, event):
        if not self.search_entry.get().strip():
            self.search_entry.insert(0, "Rechercher une app…")


    def _on_canvas_resize(self, event):
        # Ajuster la largeur du frame interne au canvas
        self.canvas.itemconfig(self.canvas_window, width=event.width)
        self._layout_cards()


    def _layout_cards(self):
        # Layout responsive: nombre de colonnes dépend de la largeur
        w = self.canvas.winfo_width()
        if w <= 520:
            cols = 2
        elif w <= 820:
            cols = 3
        else:
            cols = 4

        for widget in self.frame_projets.grid_slaves():
            widget.grid_forget()

        visible_cards = [card for (_, card) in self._cards if card.winfo_viewable()]

        # Astuce: winfo_viewable peut être faux avant update, donc on calcule sur "mapped"
        visible_cards = [card for (_, card) in self._cards if str(card.winfo_ismapped()) == "1" or True]

        # On place uniquement celles qui ne sont pas "cachées"
        row = col = 0
        for name, card in self._cards:
            if getattr(card, "_hidden", False):
                continue
            card.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")
            col += 1
            if col >= cols:
                col = 0
                row += 1

        for c in range(cols):
            self.frame_projets.grid_columnconfigure(c, weight=1)


    def _filter_cards(self):
        q = self.search_var.get().strip().lower()
        if q == "rechercher une app…":
            q = ""

        for name, card in self._cards:
            show = (q in name.lower()) if q else True
            card._hidden = not show

        self._layout_cards()
    

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
