from librairie.graphique_interface import GraphiqueInterface
from enums.ecran_etat_enum import EcranEtat
from ecran.ecran import Ecran
from ecran.gestionnaire_etat_ecran import GestionnaireEtatEcran
import tkinter as tk
from tkinter import filedialog, messagebox, Menu, Toplevel, Text

class EcranDessin(Ecran):
    def __init__(self, graphique: GraphiqueInterface, gestionnaire_etat_ecran: GestionnaireEtatEcran):
        super().__init__()
        self.graphique = graphique
        self.gestionnaire_etat_ecran = gestionnaire_etat_ecran
        self.fenetre_dessin = None

    def initialiser_interface(self):
        self.fenetre_dessin = self.graphique.creer_fenetre("DESSIN", 300, 400, "images/icone.ico")



        ###################### MENU #########################################################################################################
        # Barre de menu
        self.menu_bar = tk.Menu(self.fenetre_dessin)
        #self.config(menu=self.menu_bar)

        # Menu Fichier
        self.file_menu = Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Fichier", menu=self.file_menu)
        self.file_menu.add_command(label="Nouveau", command=self.nouveau_dessin)
        self.file_menu.add_command(label="Ouvrir", command=self.ouvrir_fichier)
        self.sauver_item = self.file_menu.add_command(label="Sauver", state="disabled", command=self.sauver_fichier)  # Sauver est désactivé
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Quitter", command=self.quitter_application)

        # Menu Aide
        aide_menu = Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Aide", menu=aide_menu)
        aide_menu.add_command(label="Aide", command=self.afficher_aide)

        self.fenetre_dessin.config(menu=self.menu_bar)

        # Canvas pour le dessin
        self.canvas = self.graphique.creer_canvas(self.fenetre_dessin)
        #self.canvas = tk.Canvas(self, bg="white")
        self.canvas.pack(fill=tk.BOTH, expand=True)


        #######################################################################################################################################  


        # Barre d'état (label)
        self.status_var = tk.StringVar()
        self.status_var.set("Barre d'état")
        self.status_label = self.graphique.creer_label(self.fenetre_dessin, text=self.status_var, relief=tk.SUNKEN, anchor=tk.W)
        self.status_label.pack(side=tk.BOTTOM, fill=tk.X)

        # Variables pour dessiner à main levée
        self.trace_en_cours = None
        self.coords = []

        # Activation de la gestion des événements de dessin
        self.canvas.bind("<Control-B1-Motion>", self.dessiner_trace)
        self.canvas.bind("<ButtonRelease-1>", self.fin_trace)

    def nouveau_dessin(self):
        """Efface le contenu du canvas."""
        self.canvas.delete("all")
        self.status_var.set("Nouveau dessin créé.")
        self.coords.clear()
        self.file_menu.entryconfig(2, state="disabled")  # Désactiver "Sauver"

    def ouvrir_fichier(self):
        """Ouvre un fichier via une boîte de dialogue."""
        fichier = filedialog.askopenfilename(title="Ouvrir un fichier")
        if fichier:
            self.status_var.set(f"Fichier ouvert: {fichier}")
            self.file_menu.entryconfig(2, state="normal")  # Activer "Sauver"

    def sauver_fichier(self):
        """Sauvegarde le contenu du canvas."""
        fichier = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Fichiers Texte", "*.txt")])
        if fichier:
            # Sauvegarder les traces ici (enregistrement des coords)
            with open(fichier, 'w') as f:
                for obj in self.canvas.find_all():
                    coords = self.canvas.coords(obj)
                    f.write(f"{coords}\n")
            self.status_var.set(f"Fichier sauvegardé: {fichier}")

    def quitter_application(self):
        """Demande confirmation avant de quitter."""
        if self.canvas.find_all():
            if messagebox.askyesno("Quitter", "Voulez-vous quitter sans sauvegarder ?"):
                self.destroy()
        else:
            self.destroy()

    def flatten(self, coords):
        """Aplatit une liste de tuples en une liste plate."""
        return [coord for pair in coords for coord in pair]

    def dessiner_trace(self, event):
        """Dessiner une ligne brisée à main levée."""
        if self.trace_en_cours is None:
            self.coords.append((event.x, event.y))
            self.trace_en_cours = self.canvas.create_line(event.x, event.y, event.x, event.y, fill="black")
        else:
            self.coords.append((event.x, event.y))
            self.canvas.coords(self.trace_en_cours, *self.flatten(self.coords))
        self.file_menu.entryconfig(2, state="normal")  # Activer "Sauver"

    def fin_trace(self, event):
        """Terminer le dessin de la ligne."""
        self.trace_en_cours = None

    def afficher_aide(self):
        """Afficher une fenêtre d'aide."""
        fenetre_aide = Toplevel(self)
        fenetre_aide.title("Aide")
        texte_aide = Text(fenetre_aide, wrap="word")
        texte_aide.insert(tk.END, "Ceci est une application de dessin .\n\nAuteur: DILO\n\n")
        texte_aide.pack(expand=True, fill=tk.BOTH)

    def afficher(self):
        if self.fenetre_dessin is None:
            self.initialiser_interface()
        self.graphique.ouvrir_fenetre(self.fenetre_dessin)
