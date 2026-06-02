# Projet Cape d'Invisibilite (OpenCV)

Effet d'invisibilite en temps reel avec une cape bleu roi.
Le masquage se fait en HSV puis le fond capture est reintegre.

## Installation

python -m pip install -r requirements.txt

## Lancer le programme

python main.py

Touches:
- q : quitter

Options utiles:
- --afficher-masque
- --enregistrer
- --sortie output/demo.mp4
- --iterations-fermeture 1
- --masque-doux
- --flou-masque 7

## Calibration HSV

python calibration.py

Ajustez les trackbars puis appuyez sur s pour afficher les seuils.

## Conseils

- Laissez le champ vide pendant la capture du fond.
- Evitez les objets bleu roi dans le decor.
- Ajustez les seuils HSV selon la lumiere.
