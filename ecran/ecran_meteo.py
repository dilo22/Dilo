import os
import threading
import tkinter as tk
from tkinter import ttk, messagebox
from io import BytesIO
from dotenv import load_dotenv
import requests
from PIL import Image, ImageTk

from librairie.graphique_interface import GraphiqueInterface
from enums.ecran_etat_enum import EcranEtat
from ecran.ecran import Ecran
from ecran.gestionnaire_etat_ecran import GestionnaireEtatEcran


# ==============================
# CONFIG (PAS DE CLÉ EN DUR)
# ==============================
# Mets ta clé dans une variable d'environnement OPENWEATHER_API_KEY
# Exemple PowerShell (session) :
#   $env:OPENWEATHER_API_KEY="ta_cle"
load_dotenv()
OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")
UNITS = "metric"  # "metric" = °C, "imperial" = °F
LANG = "fr"


class EcranMeteo(Ecran):
    def __init__(self, graphique: GraphiqueInterface, gestionnaire_etat_ecran: GestionnaireEtatEcran):
        self.graphique = graphique
        self.gestionnaire_etat_ecran = gestionnaire_etat_ecran

        self.fenetre = None

        # Tk vars
        self.city_var = None

        # UI
        self.icon_label = None
        self.city_label = None
        self.desc_label = None
        self.temp_label = None
        self.feels_label = None
        self.hum_label = None
        self.wind_label = None
        self.press_label = None
        self.status = None

        # Images
        self.retour_image = None
        self.icon_img = None  # anti-GC

    def initialiser_interface(self):
        self.fenetre = self.graphique.creer_fenetre("Météo", 520, 360, "images/icone.ico")
        self.city_var = tk.StringVar(master=self.fenetre, value="Paris")

        pad = 12

        top = ttk.Frame(self.fenetre)
        top.pack(fill="x", padx=pad, pady=(pad, 6))

        # Bouton retour
        self.retour_image = self.graphique.creer_image("images/retour.png", width=30, height=30)
        retour_btn = tk.Button(
            top,
            image=self.retour_image,
            command=self.retour_action,
            cursor="hand2",
            borderwidth=0,
            highlightthickness=0
        )
        retour_btn.image = self.retour_image  # anti-GC
        retour_btn.pack(side="left", padx=(0, 10))

        ttk.Label(top, text="Ville :").pack(side="left")

        entry = ttk.Entry(top, textvariable=self.city_var, width=26)
        entry.pack(side="left", padx=(8, 8))
        entry.bind("<Return>", lambda _e: self.fetch_weather_async())

        ttk.Button(top, text="Rechercher", command=self.fetch_weather_async).pack(side="left")

        ttk.Separator(self.fenetre).pack(fill="x", padx=pad, pady=6)

        body = ttk.Frame(self.fenetre)
        body.pack(fill="both", expand=True, padx=pad, pady=6)

        left = ttk.Frame(body, width=140)
        left.pack(side="left", fill="y")
        left.pack_propagate(False)

        right = ttk.Frame(body)
        right.pack(side="left", fill="both", expand=True, padx=(12, 0))

        self.icon_label = ttk.Label(left)
        self.icon_label.pack(pady=(10, 8))

        self.city_label = ttk.Label(right, text="Entrez une ville puis Rechercher.", font=("Segoe UI", 12, "bold"))
        self.city_label.pack(anchor="w", pady=(8, 6))

        self.desc_label = ttk.Label(right, text="")
        self.desc_label.pack(anchor="w", pady=(0, 10))

        self.temp_label = ttk.Label(right, text="Température : -")
        self.temp_label.pack(anchor="w", pady=2)

        self.feels_label = ttk.Label(right, text="Ressenti : -")
        self.feels_label.pack(anchor="w", pady=2)

        self.hum_label = ttk.Label(right, text="Humidité : -")
        self.hum_label.pack(anchor="w", pady=2)

        self.press_label = ttk.Label(right, text="Pression : -")
        self.press_label.pack(anchor="w", pady=2)

        self.wind_label = ttk.Label(right, text="Vent : -")
        self.wind_label.pack(anchor="w", pady=2)

        bottom = ttk.Frame(self.fenetre)
        bottom.pack(fill="x", padx=pad, pady=(0, pad))

        self.status = ttk.Label(bottom, text="Prêt.")
        self.status.pack(side="left")

    def afficher(self):
        self.graphique.ouvrir_fenetre(self.fenetre)

    # ✅ Pattern propre : afficher menu puis fermer la fenêtre météo
    def retour_action(self):
        old = self.fenetre
        self.gestionnaire_etat_ecran.set_etat(EcranEtat.MENU)
        self.gestionnaire_etat_ecran.afficher_etat()
        self.graphique.fermer_fenetre(old)

    def _safe_ui(self, fn):
        if self.fenetre is None:
            return
        self.fenetre.after(0, fn)

    def fetch_weather_async(self):
        city = self.city_var.get().strip()
        if not city:
            messagebox.showinfo("Info", "Entre une ville.")
            return

        if not OPENWEATHER_API_KEY:
            messagebox.showwarning(
                "Clé API manquante",
                "Définis la variable d'environnement OPENWEATHER_API_KEY.\n"
                "Exemple PowerShell:\n"
                '$env:OPENWEATHER_API_KEY="ta_cle"'
            )
            return

        self.status.config(text="Chargement…")
        threading.Thread(target=self._worker_fetch, args=(city,), daemon=True).start()

    def _worker_fetch(self, city: str):
        try:
            data = self._call_weather_api(city)
            self._safe_ui(lambda d=data: self._render(d))
            self._safe_ui(lambda: self.status.config(text="OK."))
        except Exception as e:
            self._safe_ui(lambda: self.status.config(text="Erreur."))
            self._safe_ui(lambda err=str(e): messagebox.showerror("Erreur", err))

    def _call_weather_api(self, city: str) -> dict:
        url = "https://api.openweathermap.org/data/2.5/weather"
        params = {"q": city, "appid": OPENWEATHER_API_KEY, "units": UNITS, "lang": LANG}
        r = requests.get(url, params=params, timeout=12)

        if r.status_code == 401:
            raise Exception("Clé API invalide (401).")
        if r.status_code == 404:
            raise Exception("Ville introuvable (404).")
        if r.status_code != 200:
            raise Exception(f"Erreur API ({r.status_code}) : {r.text}")

        return r.json()

    def _render(self, data: dict):
        name = data.get("name", "?")
        country = data.get("sys", {}).get("country", "")
        weather = (data.get("weather") or [{}])[0]
        main = data.get("main", {})
        wind = data.get("wind", {})

        desc = (weather.get("description") or "").capitalize()
        icon = weather.get("icon") or ""

        temp = main.get("temp")
        feels = main.get("feels_like")
        hum = main.get("humidity")
        press = main.get("pressure")
        wind_speed = wind.get("speed")

        unit_temp = "°C" if UNITS == "metric" else "°F"
        unit_wind = "m/s" if UNITS == "metric" else "mph"

        self.city_label.config(text=f"{name} ({country})" if country else name)
        self.desc_label.config(text=desc)

        self.temp_label.config(text=f"Température : {temp}{unit_temp}" if temp is not None else "Température : -")
        self.feels_label.config(text=f"Ressenti : {feels}{unit_temp}" if feels is not None else "Ressenti : -")
        self.hum_label.config(text=f"Humidité : {hum}%" if hum is not None else "Humidité : -")
        self.press_label.config(text=f"Pression : {press} hPa" if press is not None else "Pression : -")
        self.wind_label.config(text=f"Vent : {wind_speed} {unit_wind}" if wind_speed is not None else "Vent : -")

        self._load_icon(icon)

    def _load_icon(self, icon_code: str):
        if not icon_code:
            self.icon_label.config(image="")
            self.icon_img = None
            return

        icon_url = f"https://openweathermap.org/img/wn/{icon_code}@2x.png"
        r = requests.get(icon_url, timeout=12)
        r.raise_for_status()

        img = Image.open(BytesIO(r.content)).convert("RGBA").resize((110, 110))
        self.icon_img = ImageTk.PhotoImage(img)  # anti-GC
        self.icon_label.config(image=self.icon_img)