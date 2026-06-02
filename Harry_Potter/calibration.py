import cv2
import numpy as np

from utils import fenetre_ouverte, touche_quitter


def rien(valeur):
    return None


def lancer_calibration(index_camera=0):
    video = cv2.VideoCapture(index_camera)
    if not video.isOpened():
        print("Camera introuvable.")
        return

    nom_fenetre = "Calibration HSV"
    cv2.namedWindow(nom_fenetre)

    cv2.createTrackbar("H bas", nom_fenetre, 100, 179, rien)
    cv2.createTrackbar("S bas", nom_fenetre, 150, 255, rien)
    cv2.createTrackbar("V bas", nom_fenetre, 50, 255, rien)
    cv2.createTrackbar("H haut", nom_fenetre, 130, 179, rien)
    cv2.createTrackbar("S haut", nom_fenetre, 255, 255, rien)
    cv2.createTrackbar("V haut", nom_fenetre, 255, 255, rien)

    while True:
        ret, frame = video.read()
        if not ret:
            break

        frame_hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        h_bas = cv2.getTrackbarPos("H bas", nom_fenetre)
        s_bas = cv2.getTrackbarPos("S bas", nom_fenetre)
        v_bas = cv2.getTrackbarPos("V bas", nom_fenetre)
        h_haut = cv2.getTrackbarPos("H haut", nom_fenetre)
        s_haut = cv2.getTrackbarPos("S haut", nom_fenetre)
        v_haut = cv2.getTrackbarPos("V haut", nom_fenetre)

        seuil_bas = np.array([h_bas, s_bas, v_bas])
        seuil_haut = np.array([h_haut, s_haut, v_haut])

        masque = cv2.inRange(frame_hsv, seuil_bas, seuil_haut)
        resultat = cv2.bitwise_and(frame, frame, mask=masque)

        cv2.imshow(nom_fenetre, resultat)
        cv2.imshow("Masque", masque)

        touche = cv2.waitKey(1) & 0xFF
        if touche == ord("s"):
            print(f"Seuil bas: {seuil_bas.tolist()}")
            print(f"Seuil haut: {seuil_haut.tolist()}")
        if touche_quitter(touche):
            break
        if not (fenetre_ouverte(nom_fenetre) and fenetre_ouverte("Masque")):
            break

    video.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    lancer_calibration()
