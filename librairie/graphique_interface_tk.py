import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from librairie.graphique_interface import GraphiqueInterface


class GraphiqueInterfaceTk(GraphiqueInterface):
    def __init__(self):
        super().__init__()
        self.root = None
        self._mainloop_running = False

    def creer_fenetre(self, titre: str, longueur: int, largeur: int, chemin_logo: str):
        """
        Crée une fenêtre d'écran.
        - 1 seul Tk() global (root caché)
        - chaque écran = Toplevel(root)
        """
        if self.root is None:
            self.root = tk.Tk()
            self.root.withdraw()  # root caché, sert de base pour PhotoImage sans master

        fenetre = tk.Toplevel(self.root)
        fenetre.title(titre)
        fenetre.geometry(f"{longueur}x{largeur}")
        fenetre.iconbitmap(chemin_logo)

        # Fermeture propre (croix)
        def on_close():
            try:
                fenetre.destroy()
            except tk.TclError:
                return

            # Si plus aucune fenêtre Toplevel, on quitte tout
            if self.root is not None:
                restants = [
                    w for w in self.root.winfo_children()
                    if isinstance(w, tk.Toplevel) and w.winfo_exists()
                ]
                if not restants:
                    try:
                        self.root.quit()
                        self.root.destroy()
                    except tk.TclError:
                        pass
                    self.root = None
                    self._mainloop_running = False

        fenetre.protocol("WM_DELETE_WINDOW", on_close)

        return fenetre

    def creer_frame(self, fenetre, bg: str = None, width: int = None, height: int = None):
        return tk.Frame(fenetre, bg=bg, width=width, height=height)

    def fermer_fenetre(self, fenetre):
        """
        Détruit la fenêtre (Toplevel).
        Si c’est la dernière, quitte l’app.
        """
        if fenetre is None:
            return
        try:
            fenetre.destroy()
        except tk.TclError:
            return

        # Si plus de fenêtres, quitter
        if self.root is not None:
            restants = [
                w for w in self.root.winfo_children()
                if isinstance(w, tk.Toplevel) and w.winfo_exists()
            ]
            if not restants:
                try:
                    self.root.quit()
                    self.root.destroy()
                except tk.TclError:
                    pass
                self.root = None
                self._mainloop_running = False

    def ouvrir_fenetre(self, fenetre):
        """
        Lance la boucle Tk UNE seule fois.
        (fenetre est ignorée, car on pilote via root)
        """
        if self.root is None:
            # fallback (cas anormal)
            fenetre.mainloop()
            return

        if not self._mainloop_running:
            self._mainloop_running = True
            self.root.mainloop()

    def creer_button(self, frame, fonction, bg: str = None, activebackground: str = None, label=None,
                     image=None, font=None, width=None, height=None):
        return tk.Button(
            frame,
            width=width,
            height=height,
            text=label,
            cursor="hand2",
            image=image,
            command=fonction,
            bg=bg,
            activebackground=activebackground,
            font=font
        )

    def creer_progress_bar(self, frame, orient: str = None, length: str = None, mode: str = None):
        return ttk.Progressbar(frame, orient=orient, length=length, mode=mode)

    def creer_widget(self, frame, image=None, text: str = None, bg: str = None, font: str = None,
                     width: int = None, height: int = None, fg: str = None, relief: str = None,
                     padx: int = None, pady: int = None):
        if image is not None:
            label = tk.Label(
                frame, image=image, bg=bg, font=font, width=width, height=height,
                fg=fg, relief=relief, padx=padx, pady=pady
            )
            label.image = image  # anti-GC
            return label

        if text is not None:
            return tk.Label(
                frame, text=text, bg=bg, font=font, width=width, height=height,
                fg=fg, relief=relief, padx=padx, pady=pady
            )

        return None

    # ✅ INCHANGÉ (comme tu veux)
    def creer_image(self, chemin_image: str, width: int = None, height: int = None):
        original_image = Image.open(chemin_image)
        resized_image = original_image.resize((width, height))
        image = ImageTk.PhotoImage(resized_image)
        return image

    def creer_canvas(self, fenetre, bg: str = None, width: int = None, height: int = None):
        return tk.Canvas(fenetre, bg=bg, width=width, height=height)

    def creer_sous_fentre(self, fenetre):
        return tk.Toplevel(fenetre)

    def creer_carre(self, frame, chemin_image: str, label: str, fonction):
        image = self.creer_image(chemin_image, width=100, height=100)
        bouton = self.creer_button(frame, fonction=fonction, image=image, label=label)
        bouton.image = image  # IMPORTANT anti-GC
        return bouton

    def creer_label(self, frame, image=None, text: str = None, bg: str = None, font: str = None,
                    width: int = None, height: int = None, fg: str = None, relief: str = None,
                    padx: int = None, pady: int = None, bd: int = None, anchor: str = None):
        label = tk.Label(
            frame, image=image, text=text, bg=bg, font=font,
            width=width, height=height, fg=fg, relief=relief,
            padx=padx, pady=pady, bd=bd, anchor=anchor
        )
        if image is not None:
            label.image = image
        return label