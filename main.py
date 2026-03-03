from librairie.graphique_interface_tk import GraphiqueInterfaceTk
from ecran.ecran_menu import EcranMenu
from ecran.ecran_main import EcranMain
from ecran.ecran_calculatrice import EcranCalculatrice 
from ecran.ecran_convertisseur_devises import EcranConvertisseurDevises
from ecran.ecran_jeu_serpent import EcranJeuSerpent
from ecran.ecran_caisse import EcranCaisse
from ecran.ecran_liste_couleurs import EcranListeCouleurs 
from ecran.gestionnaire_etat_ecran import GestionnaireEtatEcran
from enums.ecran_etat_enum import EcranEtat
from ecran.ecran_matrice_couleurs import EcranMatriceCouleurs
from ecran.ecran_scales import EcranSelecteurCouleur
from ecran.ecran_horloge import EcranHorloge
from ecran.ecran_mdp import EcranMotDePasse
from ecran.ecran_qrcode import EcranQRCode
from ecran.ecran_youtube import EcranYoutube
from ecran.ecran_dj import EcranDJ
from ecran.ecran_dessin import EcranDessin
from ecran.ecran_meteo import EcranMeteo
from ecran.ecran_aide import EcranAide
from ecran.ecran_parametres import EcranParametre
from ecran.ecran_audio_text import EcranAudioText
from ecran.ecran_convertisseur_images import EcranConvertisseurImages


if __name__ == "__main__":
    # Initialisation de l'interface graphique
    graphique = GraphiqueInterfaceTk()

    # Initialisation du gestionnaire d'états d'écran
    gestionnaire_etat_ecran = GestionnaireEtatEcran()

    # Création et ajout des différents écrans au gestionnaire d'états d'écran
    main = EcranMain(graphique, gestionnaire_etat_ecran)
    gestionnaire_etat_ecran.ajouter_ecran(EcranEtat.MAIN, main)

    menu = EcranMenu(graphique, gestionnaire_etat_ecran)
    gestionnaire_etat_ecran.ajouter_ecran(EcranEtat.MENU, menu)

    calculatrice = EcranCalculatrice(graphique, gestionnaire_etat_ecran)
    gestionnaire_etat_ecran.ajouter_ecran(EcranEtat.CALCULATRICE, calculatrice)

    convertisseur = EcranConvertisseurDevises(graphique, gestionnaire_etat_ecran)
    gestionnaire_etat_ecran.ajouter_ecran(EcranEtat.DEVISES, convertisseur)

    jeu_serpent = EcranJeuSerpent(graphique, gestionnaire_etat_ecran)
    gestionnaire_etat_ecran.ajouter_ecran(EcranEtat.JEU_SERPENT, jeu_serpent)
    
    caisse = EcranCaisse(graphique, gestionnaire_etat_ecran)
    gestionnaire_etat_ecran.ajouter_ecran(EcranEtat.CAISSE, caisse)

    liste_couleurs = EcranListeCouleurs(graphique, gestionnaire_etat_ecran)
    gestionnaire_etat_ecran.ajouter_ecran(EcranEtat.LISTE_COULEURS, liste_couleurs)

    matrice_couleurs = EcranMatriceCouleurs(graphique, gestionnaire_etat_ecran)
    gestionnaire_etat_ecran.ajouter_ecran(EcranEtat.MATRICE_COULEURS, matrice_couleurs)

    scales = EcranSelecteurCouleur(graphique, gestionnaire_etat_ecran)
    gestionnaire_etat_ecran.ajouter_ecran(EcranEtat.SCALES, scales)

    horloge = EcranHorloge(graphique, gestionnaire_etat_ecran)
    gestionnaire_etat_ecran.ajouter_ecran(EcranEtat.HORLOGE, horloge)

    mdp = EcranMotDePasse(graphique, gestionnaire_etat_ecran)
    gestionnaire_etat_ecran.ajouter_ecran(EcranEtat.MDP, mdp)

    qrcode = EcranQRCode(graphique, gestionnaire_etat_ecran)
    gestionnaire_etat_ecran.ajouter_ecran(EcranEtat.QRCODE, qrcode)

    youtube = EcranYoutube(graphique, gestionnaire_etat_ecran)
    gestionnaire_etat_ecran.ajouter_ecran(EcranEtat.YOUTUBE, youtube)

    dj = EcranDJ(graphique, gestionnaire_etat_ecran)
    gestionnaire_etat_ecran.ajouter_ecran(EcranEtat.DJ, dj)

    dessin = EcranDessin(graphique, gestionnaire_etat_ecran)
    gestionnaire_etat_ecran.ajouter_ecran(EcranEtat.DESSIN, dessin)

    audiotext = EcranAudioText(graphique, gestionnaire_etat_ecran)
    gestionnaire_etat_ecran.ajouter_ecran(EcranEtat.AUDIOTEXT, audiotext)

    convertisseurimages = EcranConvertisseurImages(graphique, gestionnaire_etat_ecran)
    gestionnaire_etat_ecran.ajouter_ecran(EcranEtat.CONVERTISSEUR_IMAGES, convertisseurimages)

    meteo = EcranMeteo(graphique, gestionnaire_etat_ecran)
    gestionnaire_etat_ecran.ajouter_ecran(EcranEtat.METEO, meteo)

    aide = EcranAide(graphique, gestionnaire_etat_ecran)
    gestionnaire_etat_ecran.ajouter_ecran(EcranEtat.AIDE, aide)

    parametres = EcranParametre(graphique, gestionnaire_etat_ecran)
    gestionnaire_etat_ecran.ajouter_ecran(EcranEtat.PARAMETRES, parametres)

    # Affichage de l'état actuel du gestionnaire d'états d'écran
    gestionnaire_etat_ecran.afficher_etat()
