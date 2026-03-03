# from regle import ReglesJeu
# from son import play_sound_background
# from parametres import Parametres, SoundSettings
from librairie.graphique_interface import GraphiqueInterface
from enums.ecran_etat_enum import EcranEtat
from ecran.ecran import Ecran
from ecran.gestionnaire_etat_ecran import GestionnaireEtatEcran


class EcranMain(Ecran):
    def __init__(self, graphic: GraphiqueInterface, view_manager_state: GestionnaireEtatEcran):
        # On l'initialise à None pour pouvoir rentrer dans la fonction initialiser
        super().__init__()
        self.fenetre_main = None
        self.gestionnaire_etat_ecran = view_manager_state
        self.graphique = graphic

    def initialiser_interface(self):
        self.fenetre_main = self.graphique.creer_fenetre("DILO", 800, 600, "images/icone.ico")

        # self.fenetre_menu = tk.Toplevel(self.application.fenetre_principale)
        # self.fenetre_menu.title("Menu Principal")

        # self.langues = {
        #     'fr': {
        #         'Lancer_Partie': "Lancer Partie",
        #         'Parametre': "Paramètre",
        #         'Règles': "Règles"
        #     },
        #     'en': {
        #         'Lancer_Partie': "Start Game",
        #         'Parametre': "Settings",
        #         'Règles': "Rules"
        #     }
        # }
        # # la langue par défaut
        # self.langue = 'fr'

        # self.fenetre_menu.geometry("800x600")
        # self.fenetre_menu.title("En Garde")
        self.root_frame = self.graphique.creer_frame(self.fenetre_main, bg="#0b9eb5")
        # self.root_frame = tk.Frame(self.fenetre_menu, bg="#eaba61")
        self.root_frame.pack(fill='both', expand=True)

        # self.fenetre_menu.iconbitmap("images/icone.ico")

        # Frame pour contenir l'image et le bouton image
        self.top_frame = self.graphique.creer_frame(self.root_frame)
        # self.top_frame = tk.Frame(self.root_frame, bg="#eaba61")
        self.top_frame.pack(side="top", pady=10)
        # self.fenetre_menu.minsize(650, 600)

        # Ajout de l'image dans le top_frame
        # self.logo_image = tk.PhotoImage(file="images/logo.png")

        self.image = self.graphique.creer_image("images/logo.png", width=650, height=150)

        # label = self.graphique.create_widget(self.top_frame, self.logo_image)
        # label.pack(fill="both", expand=True)

        self.logo_image = self.graphique.creer_widget(self.top_frame, image=self.image)
        # self.logo_label = self.graphique.create_widget(self.top_frame, image=self.logo_image, bg="#eaba61", width=650)
        self.logo_image.pack(fill="both", expand=True)
        # self.logo_image.pack(anchor="center", padx=5)

        # self.frame = self.graphique.create_frame(self.root_frame, bg="#eaba61")
        # self.frame = tk.Frame(self.root_frame, bg="#eaba61")
        # self.frame.pack(side="top", pady=10)

        # Autres boutons
        self.bouton_1 = self.graphique.creer_button(frame=self.root_frame, fonction=lambda: self.ouvrir_menu(),
                                                    bg="#FFFFFF", activebackground="#057e92", label="Menu",
                                                    font=("Verdana", 14), width=30, height=3)
        # self.bouton_1 = tk.Button(self.root_frame , text="Lancer Partie",cursor="hand2", command=self.ouvrir_niveau,
        #                           bg="#df7d10", font=("Verdana", 14), width=30, height=3, compound=tk.LEFT,
        #                           activebackground="#674424")
        self.bouton_1.pack(padx=40, pady=2, expand=True)

        self.bouton_2 = self.graphique.creer_button(frame=self.root_frame, fonction=lambda: self.ouvrir_parametres(),
                                                    bg="#FFFFFF", activebackground="#057e92", label="Paramètres",
                                                    font=("Verdana", 14), width=30, height=3)
        # self.bouton_2 = tk.Button(self.root_frame, text="Paramètres", cursor="hand2", command=self.ouvrir_parametres,
        #                           bg="#df7d10", font=("Verdana", 14), width=30, height=3,  compound=tk.LEFT,
        #                           activebackground="#674424")
        self.bouton_2.pack(padx=40, pady=2, expand=True)
        """
        self.bouton_3 = self.graphique.creer_button(frame=self.root_frame, fonction=lambda: self.ouvrir_regle(),
                                                    bg="#FFFFFF", activebackground="#057e92", label="Régles",
                                                    font=("Verdana", 14), width=30, height=3)
        # self.bouton_3 = tk.Button(self.root_frame, text="Régles", cursor="hand2", command=self.ouvrir_regle,
        #                           bg="#df7d10", font=("Verdana", 14), width=30, height=3, compound=tk.LEFT,
        #                           activebackground="#674424")
        self.bouton_3.pack(padx=40, pady=2, expand=True)
        """
        # Bouton pour quitter l'application

        self.bouton_4 = self.graphique.creer_button(frame=self.root_frame, fonction=exit, bg="#FFFFFF",
                                                    activebackground="#057e92", label="Sortir",
                                                    font=("Verdana", 14), width=30, height=3)
        # self.bouton_4 = tk.Button(self.root_frame, text="Quitter le jeu", cursor="hand2", command=exit,
        #                           bg="#df7d10", font=("Verdana", 14), width=30, height=3, compound=tk.LEFT,
        #                           activebackground="#674424")
        self.bouton_4.pack(padx=40, pady=2, expand=True)

        # self.update_interface()

    def ouvrir_menu(self):
        # self.view_niveau.open_fenetre()
        # On change d'state
        self.gestionnaire_etat_ecran.set_etat(EcranEtat.MENU)
        self.graphique.fermer_fenetre(self.fenetre_main)
        self.gestionnaire_etat_ecran.afficher_etat()

        # self.fenetre_menu.destroy()
        # self.destroy()  # Ferme la fenêtre Menu
        # self.niveau_window = self.application.afficher_selection_niveau()
        # Sois celui d'en haut sois celui du bas
        # self.niveau_window = Niveau(self.application)

    # J'ai rajouté le regles_windows.run pour le demarrage
    def ouvrir_regle(self):
        #     ReglesJeu(self.application.fenetre_principale)
        pass

    # def update_interface(self):
    #     # Obtenez les textes appropriés pour la langue actuelle (self.langue)
    #     texts = self.langues[self.langue]

    #     # Mettez à jour le texte des boutons dans le menu
    #     self.bouton_1.configure(text=texts['Lancer_Partie'])
    #     self.bouton_2.configure(text=texts['Parametre'])
    #     self.bouton_3.configure(text=texts['Règles'])

    def ouvrir_parametres(self):
        self.gestionnaire_etat_ecran.set_etat(EcranEtat.PARAMETRES)
        #self.graphique.fermer_fenetre(self.fenetre_main)
        self.gestionnaire_etat_ecran.afficher_etat()
        #     sound_settings = SoundSettings()
        #     parametres_window = Parametres(sound_settings)
        #     parametres_window.update_interface()
        

    def afficher(self):
        self.graphique.ouvrir_fenetre(self.fenetre_main)

# if __name__ == "__main__":
#     # audio_file_path = "son/music.mp3"
#     # play_sound_background(audio_file_path)
#     app = Menu()
#     app.mainloop()
