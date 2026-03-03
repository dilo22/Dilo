from enums.ecran_etat_enum import EcranEtat


class GestionnaireEtatEcran:
    def __init__(self):
        self.etat: EcranEtat = EcranEtat.MAIN
        self.ecrans = {}

    def ajouter_ecran(self, etat, ecran):
        self.ecrans[etat] = ecran

    def get_etat(self):
        return self.etat

    def set_etat(self, etat: EcranEtat):
        self.etat = etat

    def afficher_etat(self):
        #print(self.ecrans)
        view = self.ecrans.get(self.get_etat())
        view.initialiser_interface()
        view.afficher()
