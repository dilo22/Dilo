import tkinter as tk
from tkinter import messagebox
from librairie.graphique_interface import GraphiqueInterface
from enums.ecran_etat_enum import EcranEtat
from ecran.ecran import Ecran
from ecran.gestionnaire_etat_ecran import GestionnaireEtatEcran
import random

class EcranJeuSerpent(Ecran):
    def __init__(self, graphique: GraphiqueInterface, gestionnaire_etat_ecran: GestionnaireEtatEcran):
        super().__init__()
        self.graphique = graphique
        self.gestionnaire_etat_ecran = gestionnaire_etat_ecran
        self.fenetre_jeu = None
        self.canvas = None
        self.snake = []
        self.food = None
        self.direction = "Right"
        self.running = True
        self.speed = 100  # Vitesse du serpent

    def initialiser_interface(self):
        # Création de la fenêtre principale
        self.fenetre_jeu = self.graphique.creer_fenetre("Jeu de Serpent", 600, 500, "images/icone.ico")

        # Ajouter un bouton pour revenir en arrière
        self.retour_image = self.graphique.creer_image("images/retour.png", width=30, height=30)
        retour_button = tk.Button(self.fenetre_jeu, image=self.retour_image, command=self.retour_action, bg="#e0e0e0", bd=0)
        retour_button.grid(row=0, column=0, padx=10, pady=10, sticky="nw")

        # Création du canvas pour le jeu
        self.canvas = tk.Canvas(self.fenetre_jeu, width=400, height=400, bg="black")
        self.canvas.grid(row=1, column=0, padx=10, pady=10)

        self.initialiser_jeu()

        # Bind les touches pour changer la direction du serpent
        self.fenetre_jeu.bind("<Up>", lambda event: self.change_direction("Up"))
        self.fenetre_jeu.bind("<Down>", lambda event: self.change_direction("Down"))
        self.fenetre_jeu.bind("<Left>", lambda event: self.change_direction("Left"))
        self.fenetre_jeu.bind("<Right>", lambda event: self.change_direction("Right"))

    def initialiser_jeu(self):
        self.snake = [(20, 20)]
        self.direction = "Right"
        self.create_food()
        self.update_game()

    def update_game(self):
        if not self.running:
            return

        # Déplacer le serpent
        head_x, head_y = self.snake[0]
        if self.direction == "Up":
            head_y -= 20
        elif self.direction == "Down":
            head_y += 20
        elif self.direction == "Left":
            head_x -= 20
        elif self.direction == "Right":
            head_x += 20
        
        new_head = (head_x, head_y)
        self.snake = [new_head] + self.snake[:-1]

        # Vérifier les collisions
        if self.check_collision():
            self.game_over()
            return

        # Vérifier si le serpent mange la nourriture
        if self.snake[0] == self.food:
            self.snake.append(self.snake[-1])
            self.create_food()

        self.draw_game()
        self.fenetre_jeu.after(self.speed, self.update_game)

    def draw_game(self):
        self.canvas.delete("all")
        # Dessiner le serpent
        for segment in self.snake:
            self.canvas.create_rectangle(segment[0], segment[1], segment[0] + 20, segment[1] + 20, fill="green")

        # Dessiner la nourriture
        self.canvas.create_rectangle(self.food[0], self.food[1], self.food[0] + 20, self.food[1] + 20, fill="red")

    def create_food(self):
        self.food = (random.randint(0, 19) * 20, random.randint(0, 19) * 20)

    def change_direction(self, new_direction):
        if (new_direction == "Up" and self.direction != "Down") or \
           (new_direction == "Down" and self.direction != "Up") or \
           (new_direction == "Left" and self.direction != "Right") or \
           (new_direction == "Right" and self.direction != "Left"):
            self.direction = new_direction

    def check_collision(self):
        head_x, head_y = self.snake[0]
        # Vérifier les collisions avec les murs
        if head_x < 0 or head_x >= 400 or head_y < 0 or head_y >= 400:
            return True
        # Vérifier les collisions avec le corps du serpent
        if self.snake[0] in self.snake[1:]:
            return True
        return False

    def game_over(self):
        self.running = False
        messagebox.showinfo("Game Over", "Game Over! Cliquez sur OK pour retourner au menu.")
        self.retour_action()

    def retour_action(self):
        self.graphique.fermer_fenetre(self.fenetre_jeu)
        self.gestionnaire_etat_ecran.set_etat(EcranEtat.MENU)  # Retour à l'écran menu ou autre état approprié
        self.gestionnaire_etat_ecran.afficher_etat()

    def afficher(self):
        self.graphique.ouvrir_fenetre(self.fenetre_jeu)
