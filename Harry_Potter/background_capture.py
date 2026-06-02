import cv2
import numpy as np

from utils import fenetre_ouverte, touche_quitter


def afficher_message(image, texte, couleur=(0, 255, 0)):
    cv2.putText(
        image,
        texte,
        (20, 40),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.8,
        couleur,
        2,
        cv2.LINE_AA,
    )


def capturer_fond(
    video, nombre_images=30, delai_compte_a_rebours=3, nom_fenetre="Capture du fond"
):
    if delai_compte_a_rebours > 0:
        for seconde in range(delai_compte_a_rebours, 0, -1):
            ret, frame = video.read()
            if not ret:
                continue
            image_affichee = frame.copy()
            afficher_message(image_affichee, f"Capture du fond dans {seconde}...")
            cv2.imshow(nom_fenetre, image_affichee)
            touche = cv2.waitKey(1000) & 0xFF
            if touche_quitter(touche) or not fenetre_ouverte(nom_fenetre):
                cv2.destroyWindow(nom_fenetre)
                return None

    images = []
    for _ in range(nombre_images):
        ret, frame = video.read()
        if not ret:
            continue
        images.append(frame.astype(np.float32))
        cv2.imshow(nom_fenetre, frame)
        touche = cv2.waitKey(1) & 0xFF
        if touche_quitter(touche) or not fenetre_ouverte(nom_fenetre):
            cv2.destroyWindow(nom_fenetre)
            return None

    if not images:
        cv2.destroyWindow(nom_fenetre)
        return None

    fond_moyen = np.mean(images, axis=0).astype(np.uint8)
    cv2.destroyWindow(nom_fenetre)
    return fond_moyen
