import cv2
import numpy as np


def touche_quitter(touche):
    return touche in (ord("q"), ord("Q"), 27)


def fenetre_ouverte(nom_fenetre):
    try:
        return cv2.getWindowProperty(nom_fenetre, cv2.WND_PROP_VISIBLE) >= 1
    except cv2.error:
        return False


def construire_masque_cape(
    frame_hsv,
    seuil_bas,
    seuil_haut,
    taille_noyau=5,
    iterations_dilatation=1,
    iterations_fermeture=1,
    flou_gaussien=3,
    masque_doux=False,
):
    masque = cv2.inRange(frame_hsv, seuil_bas, seuil_haut)
    noyau = np.ones((taille_noyau, taille_noyau), np.uint8)
    masque = cv2.morphologyEx(masque, cv2.MORPH_OPEN, noyau)
    if iterations_fermeture > 0:
        masque = cv2.morphologyEx(
            masque, cv2.MORPH_CLOSE, noyau, iterations=iterations_fermeture
        )
    if iterations_dilatation > 0:
        masque = cv2.morphologyEx(
            masque, cv2.MORPH_DILATE, noyau, iterations=iterations_dilatation
        )
    if flou_gaussien and flou_gaussien > 0:
        if flou_gaussien % 2 == 0:
            flou_gaussien += 1
        masque = cv2.GaussianBlur(masque, (flou_gaussien, flou_gaussien), 0)
        if not masque_doux:
            _, masque = cv2.threshold(masque, 127, 255, cv2.THRESH_BINARY)
    return masque


def fusionner_images(frame_bgr, fond_bgr, masque_cape):
    if masque_cape.ndim == 3:
        masque_cape = cv2.cvtColor(masque_cape, cv2.COLOR_BGR2GRAY)
    alpha = masque_cape.astype(np.float32) / 255.0
    alpha = cv2.merge([alpha, alpha, alpha])
    frame_f = frame_bgr.astype(np.float32)
    fond_f = fond_bgr.astype(np.float32)
    resultat = (fond_f * alpha) + (frame_f * (1.0 - alpha))
    return np.clip(resultat, 0, 255).astype(np.uint8)
