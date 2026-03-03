
class GraphiqueInterface:
    def __init__(self) -> None:
        pass

    def creer_fenetre(self, titre: str, longueur: int, largeur: int, chemin_logo: str) -> any:
        # On crée une exception si on n'a pas implementé la fonction creer_fenetre
        raise Exception("fonction creer_fenetre n'est pas implementé")

    def creer_frame(self, fenetre, bg: str = None, width: int = None, height: int = None) -> any:
        # On crée une exception si on n'a pas implementé la fonction creer_frame
        raise Exception("fonction creer_fenetre n'est pas implementé")

    def creer_button(self, frame, fonction, bg: str = None, activebackground: str = None, label: str = None,
                     image: str = None, font=None, width: int = None, height: int = None):
        # On crée une exception si on n'a pas implementé la fonction creer_button
        raise Exception("fonction creer_button n'est pas implementé")

    def fermer_fenetre(self, fenetre) -> None:
        # On crée une exception si on n'a pas implementé la fonction fermer_fenetre
        raise Exception("fonction fermer n'est pas implementé")

    def ouvrir_fenetre(self, fenetre):
        # On crée une exception si on n'a pas implementé la fonction ouvrir_fenetre
        raise Exception("fonction ouvrir_fenetre n'est pas implementé")

    def creer_progress_bar(self, frame, orient: str = None, length: int = None, mode: str = None):
        # On crée une exception si on n'a pas implementé la fonction creer_progress_bar
        raise Exception("fonction creer_progress_bar n'est pas implementé")

    def creer_widget(self, frame, image: str = None, text: str = None, bg: str = None, font: str = None,
                     width: int = None, height: int = None, fg: str = None, relief: str = None,
                     padx: int = None, pady: int = None):
        # On crée une exception si on n'a pas implementé la fonction creer_widget
        raise Exception("fonction creer_widget n'est pas implementé ! ! !")

    def creer_image(self, chemin_image: str, width: int = None, height: int = None):
        # On crée une exception si on n'a pas implementé la fonction creer_image
        raise Exception("fonction creer_image n'est pas implementé ! ! !")

    def creer_canvas(self, fenetre, bg: str = None, width: int = None, height: int = None):
        # On crée une exception si on n'a pas implementé la fonction creer_canvas
        raise Exception("fonction creer_canvas n'est pas implementé ! ! ! ")

    def creer_sous_fentre(self, fenetre):
        # On crée une exception si on n'a pas implementé la fonction creer_sous_fenetre
        raise Exception("fonction creer_sous_fentre n'est pas implementé ! ! ! ")
    def creer_carre(self, frame, chemin_image: str, label: str, fonction):
        # On crée une exception si on n'a pas implementé la fonction creer_carre
        raise Exception("fonction creer_carre n'est pas implementé ! ! ! ")
    def creer_label(self, frame, image=None, text: str = None, bg: str = None, font: str = None,
                    width: int = None, height: int = None, fg: str = None, relief: str = None,
                    padx: int = None, pady: int = None, bd: int = None, anchor: str = None):
        # On crée une exception si on n'a pas implementé la fonction creer_label
        raise Exception("fonction creer_label n'est pas implementé ! ! ! ")
