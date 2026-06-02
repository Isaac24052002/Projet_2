import argparse
import os
import cv2
import numpy as np

from background_capture import capturer_fond
from utils import (
    construire_masque_cape,
    fenetre_ouverte,
    fusionner_images,
    touche_quitter,
)


def analyser_arguments():
    parser = argparse.ArgumentParser(
        description="Effet de cape d'invisibilite par soustraction de fond."
    )
    parser.add_argument("--camera", type=int, default=0, help="Index de la camera.")
    parser.add_argument("--largeur", type=int, default=640, help="Largeur de capture.")
    parser.add_argument("--hauteur", type=int, default=480, help="Hauteur de capture.")
    parser.add_argument(
        "--images-fond", type=int, default=30, help="Nombre d'images pour le fond."
    )
    parser.add_argument(
        "--delai-fond",
        type=int,
        default=3,
        help="Delai avant capture du fond (secondes).",
    )
    parser.add_argument("--h-bas", type=int, default=100, help="Seuil bas H.")
    parser.add_argument("--s-bas", type=int, default=150, help="Seuil bas S.")
    parser.add_argument("--v-bas", type=int, default=50, help="Seuil bas V.")
    parser.add_argument("--h-haut", type=int, default=130, help="Seuil haut H.")
    parser.add_argument("--s-haut", type=int, default=255, help="Seuil haut S.")
    parser.add_argument("--v-haut", type=int, default=255, help="Seuil haut V.")
    parser.add_argument(
        "--taille-noyau", type=int, default=5, help="Taille du noyau morphologique."
    )
    parser.add_argument(
        "--iterations-dilatation", type=int, default=1, help="Iterations de dilatation."
    )
    parser.add_argument(
        "--iterations-fermeture",
        type=int,
        default=1,
        help="Iterations de fermeture (remplit les trous).",
    )
    parser.add_argument(
        "--flou-masque", type=int, default=3, help="Taille du flou gaussien du masque."
    )
    parser.add_argument(
        "--masque-doux",
        action="store_true",
        help="Adoucir le masque pour un fondu plus naturel.",
    )
    parser.add_argument(
        "--afficher-masque", action="store_true", help="Afficher le masque binaire."
    )
    parser.add_argument(
        "--enregistrer", action="store_true", help="Enregistrer la video de sortie."
    )
    parser.add_argument(
        "--sortie",
        type=str,
        default="output/demo.mp4",
        help="Chemin de la video de sortie.",
    )
    parser.add_argument("--fps", type=int, default=20, help="FPS pour la video de sortie.")
    return parser.parse_args()


def ouvrir_camera(index_camera, largeur, hauteur):
    video = cv2.VideoCapture(index_camera)
    if not video.isOpened():
        return None
    video.set(cv2.CAP_PROP_FRAME_WIDTH, largeur)
    video.set(cv2.CAP_PROP_FRAME_HEIGHT, hauteur)
    return video


def preparer_enregistrement(chemin_sortie, fps, largeur, hauteur):
    dossier = os.path.dirname(chemin_sortie)
    if dossier:
        os.makedirs(dossier, exist_ok=True)
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    ecrivain = cv2.VideoWriter(chemin_sortie, fourcc, fps, (largeur, hauteur))
    if not ecrivain.isOpened():
        print("Impossible d'ouvrir le fichier video de sortie.")
        return None
    return ecrivain


def lancer():
    arguments = analyser_arguments()
    video = ouvrir_camera(arguments.camera, arguments.largeur, arguments.hauteur)
    if video is None:
        print("Camera introuvable.")
        return

    fond_reference = capturer_fond(
        video,
        nombre_images=arguments.images_fond,
        delai_compte_a_rebours=arguments.delai_fond,
    )
    if fond_reference is None:
        print("Echec de capture du fond.")
        video.release()
        return

    hauteur, largeur = fond_reference.shape[:2]
    ecrivain = None
    if arguments.enregistrer:
        ecrivain = preparer_enregistrement(arguments.sortie, arguments.fps, largeur, hauteur)

    seuil_bas = np.array([arguments.h_bas, arguments.s_bas, arguments.v_bas])
    seuil_haut = np.array([arguments.h_haut, arguments.s_haut, arguments.v_haut])

    while True:
        ret, frame = video.read()
        if not ret:
            break

        frame_hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        masque_cape = construire_masque_cape(
            frame_hsv,
            seuil_bas,
            seuil_haut,
            taille_noyau=arguments.taille_noyau,
            iterations_dilatation=arguments.iterations_dilatation,
            iterations_fermeture=arguments.iterations_fermeture,
            flou_gaussien=arguments.flou_masque,
            masque_doux=arguments.masque_doux,
        )

        resultat = fusionner_images(frame, fond_reference, masque_cape)

        cv2.imshow("Invisibilite", resultat)
        if arguments.afficher_masque:
            cv2.imshow("Masque", masque_cape)

        if ecrivain is not None:
            ecrivain.write(resultat)

        touche = cv2.waitKey(1) & 0xFF
        if touche_quitter(touche):
            break
        if not fenetre_ouverte("Invisibilite"):
            break
        if arguments.afficher_masque and not fenetre_ouverte("Masque"):
            break

    video.release()
    if ecrivain is not None:
        ecrivain.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    lancer()
