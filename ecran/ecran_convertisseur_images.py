import os
import threading
import tkinter as tk
from tkinter import ttk, filedialog, messagebox

from PIL import Image

from librairie.graphique_interface import GraphiqueInterface
from enums.ecran_etat_enum import EcranEtat
from ecran.ecran import Ecran
from ecran.gestionnaire_etat_ecran import GestionnaireEtatEcran


SUPPORTED_EXT = (".jpg", ".jpeg", ".png", ".bmp", ".tif", ".tiff")


def is_transparent(img: Image.Image) -> bool:
    if img.mode in ("RGBA", "LA"):
        return True
    return img.mode == "P" and "transparency" in img.info


class EcranConvertisseurImages(Ecran):
    def __init__(self, graphique: GraphiqueInterface, gestionnaire_etat_ecran: GestionnaireEtatEcran):
        self.graphique = graphique
        self.gestionnaire_etat_ecran = gestionnaire_etat_ecran

        self.fenetre = None
        self.files = []

        # Vars Tk
        self.output_dir = None
        self.quality = None
        self.method = None
        self.lossless = None
        self.keep_metadata = None

        # UI
        self.listbox = None
        self.out_label = None
        self.quality_scale = None
        self.quality_value = None
        self.method_combo = None
        self.convert_btn = None
        self.progress = None
        self.status = None
        self.log = None

        # Images
        self.retour_image = None
        self.retour_button = None

    def initialiser_interface(self):
        self.fenetre = self.graphique.creer_fenetre(
            "Convertisseur WebP (multi-fichiers)",
            720,
            520,
            "images/icone.ico"
        )

        # Variables Tk
        self.output_dir = tk.StringVar(master=self.fenetre, value="")
        self.quality = tk.IntVar(master=self.fenetre, value=82)
        self.method = tk.IntVar(master=self.fenetre, value=6)
        self.lossless = tk.BooleanVar(master=self.fenetre, value=False)
        self.keep_metadata = tk.BooleanVar(master=self.fenetre, value=False)

        pad = 10

        # --- Barre du haut ---
        top = ttk.Frame(self.fenetre)
        top.pack(fill="x", padx=pad, pady=(pad, 0))
        #print("fenetre =", self.fenetre, "master =", self.fenetre.master)
        # ✅ Comme ton app "devises" : on recrée l'image à chaque ouverture d'écran
        self.retour_image = self.graphique.creer_image("images/retour.png", width=30, height=30)

        retour_button = tk.Button(self.fenetre, image=self.retour_image, command=self.retour_action)
        #retour_button.grid(row=0, column=0, padx=10, pady=10, sticky="nw")

        """self.retour_button = tk.Button(
            top,
            image=self.retour_image,
            command=self.retour_action,
            cursor="hand2",
            borderwidth=0
        )
        self.retour_button.image = self.retour_image  # anti-GC"""
        retour_button.pack(side="left", padx=(0, 10))

        ttk.Button(top, text="Choisir images…", command=self.pick_files).pack(side="left")
        ttk.Button(top, text="Vider la liste", command=self.clear_files).pack(side="left", padx=(8, 0))

        # --- Zone centrale ---
        mid = ttk.Frame(self.fenetre)
        mid.pack(fill="both", expand=True, padx=pad, pady=pad)

        left = ttk.Frame(mid)
        left.pack(side="left", fill="both", expand=True)

        ttk.Label(left, text="Fichiers sélectionnés :").pack(anchor="w")
        self.listbox = tk.Listbox(left, selectmode=tk.EXTENDED)
        self.listbox.pack(fill="both", expand=True, pady=(6, 0))

        right = ttk.Frame(mid, width=260)
        right.pack(side="right", fill="y")
        right.pack_propagate(False)

        # --- Sortie ---
        out_frame = ttk.LabelFrame(right, text="Sortie")
        out_frame.pack(fill="x", pady=(0, 10))

        ttk.Button(out_frame, text="Choisir dossier…", command=self.pick_output_dir).pack(fill="x", padx=8, pady=8)
        self.out_label = ttk.Label(out_frame, text="(pas choisi)", wraplength=230)
        self.out_label.pack(fill="x", padx=8, pady=(0, 8))

        # --- Qualité / Compression ---
        opt_frame = ttk.LabelFrame(right, text="Qualité / Compression")
        opt_frame.pack(fill="x", pady=(0, 10))

        ttk.Label(opt_frame, text="Qualité (photos) :").pack(anchor="w", padx=8, pady=(8, 0))

        # Créer le scale SANS callback d'abord
        self.quality_scale = ttk.Scale(opt_frame, from_=50, to=95, orient="horizontal")
        self.quality_scale.pack(fill="x", padx=8, pady=(4, 0))

        # Label avant activation callback
        self.quality_value = ttk.Label(opt_frame, text=str(self.quality.get()))
        self.quality_value.pack(anchor="e", padx=8, pady=(0, 8))

        # Activation callback après création
        self.quality_scale.configure(command=self._on_quality_change)
        self.quality_scale.set(self.quality.get())

        ttk.Label(opt_frame, text="Méthode (0 = rapide, 6 = mieux) :").pack(anchor="w", padx=8)
        self.method_combo = ttk.Combobox(opt_frame, values=[0, 1, 2, 3, 4, 5, 6], state="readonly")
        self.method_combo.set(str(self.method.get()))
        self.method_combo.pack(fill="x", padx=8, pady=(4, 8))

        # --- Options ---
        misc_frame = ttk.LabelFrame(right, text="Options")
        misc_frame.pack(fill="x", pady=(0, 10))

        ttk.Checkbutton(
            misc_frame,
            text="Lossless (logos/captures)",
            variable=self.lossless,
            command=self._toggle_lossless_ui
        ).pack(anchor="w", padx=8, pady=(8, 4))

        ttk.Checkbutton(
            misc_frame,
            text="Garder métadonnées (limité)",
            variable=self.keep_metadata
        ).pack(anchor="w", padx=8, pady=(0, 8))

        # --- Bas ---
        bottom = ttk.Frame(self.fenetre)
        bottom.pack(fill="x", padx=pad, pady=(0, pad))

        self.convert_btn = ttk.Button(bottom, text="Convertir en WebP", command=self.start_convert)
        self.convert_btn.pack(side="left")

        self.progress = ttk.Progressbar(bottom, length=320, mode="determinate")
        self.progress.pack(side="left", padx=(10, 0))

        self.status = ttk.Label(bottom, text="Prêt.")
        self.status.pack(side="right")

        # --- Log ---
        log_frame = ttk.LabelFrame(self.fenetre, text="Log")
        log_frame.pack(fill="both", expand=False, padx=pad, pady=(0, pad))

        self.log = tk.Text(log_frame, height=7, wrap="word")
        self.log.pack(fill="both", expand=True, padx=8, pady=8)
        self.log.configure(state="disabled")

    def afficher(self):
        self.graphique.ouvrir_fenetre(self.fenetre)

    # ✅ IMPORTANT: on affiche le menu puis on ferme l’ancienne fenêtre
    def retour_action(self):
        self.graphique.fermer_fenetre(self.fenetre)
        self.gestionnaire_etat_ecran.set_etat(EcranEtat.MENU)  # Ou l'état approprié pour revenir à l'écran précédent
        self.gestionnaire_etat_ecran.afficher_etat()
        #old = self.fenetre
        #self.gestionnaire_etat_ecran.set_etat(EcranEtat.MENU)
        #self.gestionnaire_etat_ecran.afficher_etat()
        #self.graphique.fermer_fenetre(old)

    def _safe_ui(self, fn):
        if self.fenetre is None:
            return
        self.fenetre.after(0, fn)

    def _log(self, msg: str):
        self.log.configure(state="normal")
        self.log.insert("end", msg + "\n")
        self.log.see("end")
        self.log.configure(state="disabled")

    def _on_quality_change(self, v):
        v = int(float(v))
        self.quality.set(v)
        if self.quality_value is not None:
            self.quality_value.config(text=str(v))

    def _toggle_lossless_ui(self):
        if self.lossless.get():
            self.status.config(text="Lossless activé (idéal logos/captures).")
        else:
            self.status.config(text="Prêt.")

    def pick_files(self):
        files = filedialog.askopenfilenames(
            title="Choisir des images",
            filetypes=[
                ("Images", "*.jpg *.jpeg *.png *.bmp *.tif *.tiff"),
                ("Tous les fichiers", "*.*"),
            ],
        )
        if not files:
            return

        valid = [f for f in files if f.lower().endswith(SUPPORTED_EXT)]
        if not valid:
            messagebox.showwarning("Aucun fichier valide", "Aucune image supportée n'a été sélectionnée.")
            return

        self.files = list(valid)
        self.refresh_listbox()
        self.status.config(text=f"{len(self.files)} fichier(s) prêt(s).")
        self._log(f"Ajouté: {len(self.files)} fichier(s).")

    def clear_files(self):
        self.files = []
        self.refresh_listbox()
        self.progress["value"] = 0
        self.status.config(text="Prêt.")
        self._log("Liste vidée.")

    def refresh_listbox(self):
        self.listbox.delete(0, "end")
        for f in self.files:
            self.listbox.insert("end", f)

    def pick_output_dir(self):
        d = filedialog.askdirectory(title="Choisir le dossier de sortie")
        if not d:
            return
        self.output_dir.set(d)
        self.out_label.config(text=d)
        self._log(f"Dossier de sortie: {d}")

    def start_convert(self):
        if not self.files:
            messagebox.showinfo("Info", "Choisis d'abord des images.")
            return
        if not self.output_dir.get():
            messagebox.showinfo("Info", "Choisis un dossier de sortie.")
            return

        self.convert_btn.config(state="disabled")
        self.progress["value"] = 0
        self.progress["maximum"] = len(self.files)
        self.status.config(text="Conversion…")

        threading.Thread(target=self._convert_worker, daemon=True).start()

    def _convert_worker(self):
        out_dir = self.output_dir.get()
        q = int(self.quality.get())
        method = int(self.method_combo.get())
        lossless = bool(self.lossless.get())

        ok = 0
        fail = 0

        for idx, in_path in enumerate(self.files, start=1):
            base = os.path.splitext(os.path.basename(in_path))[0]
            out_path = os.path.join(out_dir, base + ".webp")

            try:
                img = Image.open(in_path)

                if is_transparent(img):
                    img = img.convert("RGBA")
                else:
                    img = img.convert("RGB")

                save_kwargs = {"format": "WEBP", "method": method}
                if lossless:
                    save_kwargs["lossless"] = True
                else:
                    save_kwargs["quality"] = q

                if self.keep_metadata.get():
                    icc = img.info.get("icc_profile")
                    if icc:
                        save_kwargs["icc_profile"] = icc

                img.save(out_path, **save_kwargs)
                ok += 1
                self._safe_ui(lambda p=in_path, o=out_path:
                              self._log(f"OK  : {os.path.basename(p)} -> {os.path.basename(o)}"))
            except Exception as e:
                fail += 1
                self._safe_ui(lambda p=in_path, err=str(e):
                              self._log(f"ERR : {os.path.basename(p)} ({err})"))

            self._safe_ui(lambda v=idx: self.progress.config(value=v))

        def done():
            self.convert_btn.config(state="normal")
            if fail == 0:
                self.status.config(text=f"Terminé ({ok}/{ok + fail})")
                messagebox.showinfo("Terminé", f"Conversion terminée.\nOK: {ok}\nErreurs: {fail}")
            else:
                self.status.config(text=f"Terminé (OK {ok}, erreurs {fail})")
                messagebox.showwarning("Terminé", f"Conversion terminée.\nOK: {ok}\nErreurs: {fail}\nRegarde le log.")

        self._safe_ui(done)