from librairie.graphique_interface import GraphiqueInterface
from enums.ecran_etat_enum import EcranEtat
from ecran.ecran import Ecran
from ecran.gestionnaire_etat_ecran import GestionnaireEtatEcran

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import threading

from faster_whisper import WhisperModel
from PIL import Image, ImageTk


class EcranAudioText(Ecran):
    def __init__(self, graphique: GraphiqueInterface, gestionnaire_etat_ecran: GestionnaireEtatEcran):
        self.graphique = graphique
        self.gestionnaire_etat_ecran = gestionnaire_etat_ecran

        self.fenetre = None

        # UI
        self.path_label = None
        self.lang_var = None
        self.lang_combo = None
        self.btn_transcribe = None
        self.text = None
        self.status_var = None

        # Data
        self.audio_path = None

        # Whisper
        self.model = None
        self.model_lock = threading.Lock()

        # Image retour (Tk image)
        self.retour_image = None

    def initialiser_interface(self):
        self.fenetre = self.graphique.creer_fenetre(
            "Audio → Texte (Whisper local)",
            700,
            520,
            "images/icone.ico"
        )

        top = ttk.Frame(self.fenetre, padding=10)
        top.pack(fill="x")

        # ✅ Création image retour avec master = cette fenêtre (corrige pyimage.. doesn't exist)
        pil_img = Image.open("images/retour.png").resize((30, 30))
        self.retour_image = ImageTk.PhotoImage(pil_img, master=self.fenetre)

        retour_button = tk.Button(top, image=self.retour_image, command=self.retour_action, cursor="hand2")
        retour_button.image = self.retour_image  # garde une référence
        retour_button.pack(side="left", padx=(0, 10))

        ttk.Button(top, text="Choisir un fichier audio", command=self.pick_audio).pack(side="left")
        self.path_label = ttk.Label(top, text="Aucun fichier")
        self.path_label.pack(side="left", padx=10)

        opts = ttk.Frame(self.fenetre, padding=(10, 0, 10, 10))
        opts.pack(fill="x")

        ttk.Label(opts, text="Langue :").pack(side="left")
        self.lang_var = tk.StringVar(value="auto")
        self.lang_combo = ttk.Combobox(
            opts,
            textvariable=self.lang_var,
            values=["auto", "fr", "en", "es", "de", "it"],
            width=8,
            state="readonly",
        )
        self.lang_combo.pack(side="left", padx=6)

        self.btn_transcribe = ttk.Button(opts, text="Transcrire", command=self.transcribe, state="disabled")
        self.btn_transcribe.pack(side="left", padx=6)

        ttk.Button(opts, text="Effacer", command=self.clear).pack(side="right", padx=6)
        ttk.Button(opts, text="Sauvegarder le texte", command=self.save_text).pack(side="right")

        mid = ttk.Frame(self.fenetre, padding=10)
        mid.pack(fill="both", expand=True)

        self.status_var = tk.StringVar(value="Prêt.")
        ttk.Label(mid, textvariable=self.status_var).pack(anchor="w")

        self.text = tk.Text(mid, wrap="word")
        self.text.pack(fill="both", expand=True, pady=(6, 0))

    def retour_action(self):
        self.graphique.fermer_fenetre(self.fenetre)
        self.gestionnaire_etat_ecran.set_etat(EcranEtat.MENU)
        self.gestionnaire_etat_ecran.afficher_etat()

    def afficher(self):
        self.graphique.ouvrir_fenetre(self.fenetre)

    def pick_audio(self):
        path = filedialog.askopenfilename(
            title="Choisir un audio",
            filetypes=[
                ("Audio", "*.wav *.mp3 *.m4a *.aac *.flac *.ogg *.opus *.webm"),
                ("Tous les fichiers", "*.*"),
            ],
        )
        if not path:
            return

        self.audio_path = path
        self.path_label.config(text=path)
        self.btn_transcribe.config(state="normal")
        self.status_var.set("Fichier chargé. Prêt à transcrire.")

    def clear(self):
        self.audio_path = None
        if self.path_label is not None:
            self.path_label.config(text="Aucun fichier")
        if self.text is not None:
            self.text.delete("1.0", "end")
        if self.btn_transcribe is not None:
            self.btn_transcribe.config(state="disabled")
        if self.status_var is not None:
            self.status_var.set("Prêt.")

    def save_text(self):
        content = self.text.get("1.0", "end").strip()
        if not content:
            messagebox.showinfo("Rien à sauvegarder", "Il n’y a pas de texte.")
            return

        path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Texte", "*.txt")],
            title="Enregistrer la transcription",
            initialfile="transcription.txt",
        )
        if not path:
            return

        try:
            with open(path, "w", encoding="utf-8") as f:
                f.write(content)
            messagebox.showinfo("OK", f"Texte enregistré :\n{path}")
        except Exception as e:
            messagebox.showerror("Erreur", f"Impossible d’enregistrer.\n\nDétail : {e}")

    def _ensure_model_loaded(self):
        with self.model_lock:
            if self.model is None:
                self.model = WhisperModel("small", device="cpu", compute_type="int8")

    def transcribe(self):
        if not self.audio_path:
            messagebox.showwarning("Aucun fichier", "Choisis un fichier audio d’abord.")
            return

        self.btn_transcribe.config(state="disabled")
        self.status_var.set("Transcription en cours…")
        self.fenetre.update_idletasks()

        threading.Thread(target=self._transcribe_worker, daemon=True).start()

    def _transcribe_worker(self):
        try:
            self._ensure_model_loaded()

            language = self.lang_var.get()
            if language == "auto":
                language = None

            segments, info = self.model.transcribe(
                self.audio_path,
                language=language,
                vad_filter=True,
            )

            out = []
            for seg in segments:
                txt = (seg.text or "").strip()
                if txt:
                    out.append(txt)
            result = "\n".join(out).strip()

            detected = getattr(info, "language", "?")
            self.fenetre.after(0, lambda: self._transcribe_done(result, detected))

        except Exception as e:
            self.fenetre.after(0, lambda: self._transcribe_error(e))

    def _transcribe_done(self, result: str, detected_language: str):
        self.text.delete("1.0", "end")
        self.text.insert("1.0", result if result else "(Aucun texte détecté)")
        self.status_var.set(f"Terminé. Langue détectée: {detected_language}")
        self.btn_transcribe.config(state="normal" if self.audio_path else "disabled")

    def _transcribe_error(self, e: Exception):
        self.status_var.set("Erreur.")
        self.btn_transcribe.config(state="normal" if self.audio_path else "disabled")
        messagebox.showerror("Erreur", f"Impossible de transcrire.\n\nDétail : {e}")