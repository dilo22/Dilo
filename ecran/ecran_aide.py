from librairie.graphique_interface import GraphiqueInterface
from enums.ecran_etat_enum import EcranEtat
from ecran.ecran import Ecran
from ecran.gestionnaire_etat_ecran import GestionnaireEtatEcran
import tkinter as tk
from tkinter import messagebox

class EcranAide(Ecran):
    def __init__(self, graphique: GraphiqueInterface, gestionnaire_etat_ecran: GestionnaireEtatEcran):
        self.graphique = graphique
        self.gestionnaire_etat_ecran = gestionnaire_etat_ecran
        self.root = None
        

    def initialiser_interface(self):

        self.root = tk.Tk()
        self.root.title("Styles de Tkinter")
        self.root.geometry("800x600")


        self.retour_image = self.graphique.creer_image("images/retour.png", width=30, height=30)
        retour_button = self.graphique.creer_button(self.root, fonction=self.retour_action, image=self.retour_image)

        retour_button.place(x=10, y=10)

        # Titre principal
        self.titre_principal = tk.Label(self.root, text="Styles de Tkinter", font=("Helvetica", 16, "bold"))
        self.titre_principal.pack(pady=10)

        # Création du canvas et de la scrollbar
        self.canvas = tk.Canvas(self.root)
        self.scrollbar = tk.Scrollbar(self.root, orient="vertical", command=self.canvas.yview)
        self.scrollbar.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)

        # Créer un Frame dans le Canvas
        self.main_frame = tk.Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.main_frame, anchor='nw')

        # Lier le canvas à la scrollbar
        self.canvas.config(yscrollcommand=self.scrollbar.set)
        self.main_frame.bind("<Configure>", self.on_frame_configure)

        # Lier les événements de la molette de la souris
        self.canvas.bind_all("<MouseWheel>", self.on_mouse_wheel)

        # Création des différentes sections
        self.creer_section_boutons()
        self.creer_section_champs()
        self.creer_section_cases_a_cocher_radio()
        self.creer_formes()

        self.root.mainloop()

    def retour_action(self):
        self.graphique.fermer_fenetre(self.root)
        self.gestionnaire_etat_ecran.set_etat(EcranEtat.MENU)
        self.gestionnaire_etat_ecran.afficher_etat()

    def on_frame_configure(self, event):
        # Mettre à jour la région du scroll
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def on_mouse_wheel(self, event):
        # Défilement avec la molette de la souris
        self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def creer_section_boutons(self):
        # Cadre pour les boutons
        frame_boutons = tk.LabelFrame(self.main_frame, text="Boutons", padx=10, pady=10)
        frame_boutons.pack(side="left", fill="both", expand="yes", padx=20, pady=10)

        # Bouton 1 - Standard
        self.creer_bouton(frame_boutons, "Bouton 1", "Standard", {})

        # Bouton 2 - Coloré
        self.creer_bouton(frame_boutons, "Bouton 2", "bg='blue', fg='white'", {"bg": "blue", "fg": "white"})

        # Bouton 3 - 3D
        self.creer_bouton(frame_boutons, "Bouton 3", "relief=tk.RAISED, bd=5", {"relief": tk.RAISED, "bd": 5})

        # Bouton 4 - Police différente
        self.creer_bouton(frame_boutons, "Bouton 4", "font=('Helvetica', 14, 'bold')", {"font": ("Helvetica", 14, "bold")})

    def creer_bouton(self, parent, nom, tooltip_text, options):
        # Ajoute le nom du bouton comme texte, remplace si déjà défini
        options["text"] = nom

        bouton = tk.Button(parent, **options)
        bouton.pack(pady=5, padx=5)

        # Tooltip
        tooltip = tk.Label(self.root, text=tooltip_text, bg="yellow", bd=1, relief=tk.SOLID, padx=3, pady=1)
        tooltip.place_forget()

        def on_enter(event):
            tooltip.place(x=event.x_root - self.root.winfo_x(), y=event.y_root - self.root.winfo_y() - 25)

        def on_leave(event):
            tooltip.place_forget()

        bouton.bind("<Enter>", on_enter)
        bouton.bind("<Leave>", on_leave)

    def creer_section_champs(self):
        # Cadre pour les champs de texte à droite des boutons
        frame_champs = tk.LabelFrame(self.main_frame, text="Champs de Texte", padx=10, pady=10)
        frame_champs.pack(side="left", fill="both", expand="yes", padx=20, pady=10)

        # Champ 1 - Standard
        self.creer_champ(frame_champs, "Champ 1", "Standard", {})

        # Champ 2 - Coloré
        self.creer_champ(frame_champs, "Champ 2", "bg='lightyellow', bd=3", {"bg": "lightyellow", "bd": 3})

    def creer_champ(self, parent, nom, tooltip_text, options):
        champ = tk.Entry(parent, **options)
        champ.pack(pady=5, padx=5)
        champ.insert(0, nom)

        # Tooltip
        tooltip = tk.Label(self.root, text=tooltip_text, bg="yellow", bd=1, relief=tk.SOLID, padx=3, pady=1)
        tooltip.place_forget()

        def on_enter(event):
            tooltip.place(x=event.x_root - self.root.winfo_x(), y=event.y_root - self.root.winfo_y() - 25)

        def on_leave(event):
            tooltip.place_forget()

        champ.bind("<Enter>", on_enter)
        champ.bind("<Leave>", on_leave)

    def creer_section_cases_a_cocher_radio(self):
        # Cadre pour les cases à cocher et les formes géométriques
        frame_cases = tk.LabelFrame(self.main_frame, text="Cases à Cocher et radio", padx=10, pady=10)
        frame_cases.pack(side="left", expand="yes", padx=20, pady=10)

        # Cadre gauche pour les cases à cocher
        frame_cases = tk.Frame(frame_cases)
        frame_cases.pack(side="left", padx=5, pady=5)

        # Case à cocher
        case_var = tk.BooleanVar()
        case = tk.Checkbutton(frame_cases, text="Option 1", variable=case_var)
        case.pack(anchor="w")
        case_1 = tk.Checkbutton(frame_cases, text="Option 2", variable=case_var)
        case_1.pack(anchor="w")

        # Boutons radio
        radio_var = tk.StringVar()
        radio1 = tk.Radiobutton(frame_cases, text="Option A", variable=radio_var, value="A")
        radio2 = tk.Radiobutton(frame_cases, text="Option B", variable=radio_var, value="B")
        radio1.pack(anchor="w")
        radio2.pack(anchor="w")

    def creer_formes (self):

        frame_cases_formes = tk.LabelFrame(self.main_frame, text="Formes Géométriques", padx=10, pady=10)
        frame_cases_formes.pack(side="left", expand="yes", padx=20, pady=10)
        # Cadre droit pour les formes géométriques
        frame_formes = tk.Frame(frame_cases_formes)
        frame_formes.pack(side="right", padx=20, pady=5)

        canvas = tk.Canvas(frame_formes, width=200, height=100)
        canvas.pack()

        # Rectangle
        canvas.create_rectangle(10, 10, 100, 50, fill="red")
        # Cercle (oval)
        canvas.create_oval(120, 10, 180, 50, fill="blue")

    def afficher(self):
        # Assurer que l'interface est initialisée avant de l'afficher
        if self.root is None:
            self.initialiser_interface()
        self.graphique.ouvrir_fenetre(self.root)
