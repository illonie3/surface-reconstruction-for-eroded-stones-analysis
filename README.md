# Reconstruction 3D par Stéréophotométrie

Ce projet permet de reconstruire numériquement en 3D la surface d'un objet (comme des échantillons de calcaire) à partir d'une série de photographies en 2D. 

## 💡 Principe du code (Photometric Stereo)

Le programme repose sur le principe de la **stéréophotométrie**. L'idée est de prendre plusieurs photos d'un même objet avec une caméra fixe (vue du dessus), mais en modifiant l'angle d'incidence de la lumière pour chaque prise de vue. 

1. **Extraction des normales :** En analysant les variations d'ombres et de luminosité sur les 5 images, l'algorithme calcule le vecteur normal (l'orientation) de chaque pixel de la surface.
2. **Intégration de la surface :** Le script utilise les mathématiques (différences finies et transformée en cosinus discrète via la méthode de Simchony) pour "intégrer" ces normales et calculer l'altitude ($Z$) de chaque point.
3. **Restitution 3D :** La matrice d'altitudes obtenue est convertie en un modèle 3D interactif visualisable directement dans le navigateur.

## 🛠 Prérequis et Configuration (Ubuntu / Linux)

Pour faire fonctionner ce programme sur une machine Ubuntu, vous devez installer Python 3 et les bibliothèques scientifiques requises.

1. **Mettre à jour le système et installer pip (gestionnaire de paquets Python) :**
   ```bash
   sudo apt update
   sudo apt install python3 python3-pip
   ```

2. **Installer les dépendances du projet :**
   Placez-vous dans le dossier racine du projet et exécutez :
   ```bash
   pip3 install -r requirements.txt
   ```
   *(Assurez-vous que votre fichier `requirements.txt` contient bien : `numpy`, `matplotlib`, `Pillow`, `scipy`, `pandas`, `plotly` et `opencv-python`)*.

## 📁 Préparation des dossiers et nommage des photos

Le nommage des photos est **strict**. Pour que le calcul mathématique de la matrice d'éclairage ($S$) fonctionne, l'algorithme lit l'angle d'azimut de la source lumineuse directement dans le nom du fichier. 

*   Créez un dossier par échantillon (par exemple `echantillon_A/`).
*   Placez-y exactement **5 photos** (prises par le haut).
*   L'angle d'élévation de la lampe doit être d'environ **26°**.
*   **Nommage :** Les fichiers doivent être nommés avec l'angle de la source lumineuse en degrés, suivi de l'extension (ex: `.jpg`). 

**Exemple de structure de dossier valide :**
```text
echantillon_A/
├── 0.jpg      (lumière à 0°)
├── 72.jpg     (lumière à 72°)
├── 144.jpg    (lumière à 144°)
├── 216.jpg    (lumière à 216°)
└── 288.jpg    (lumière à 288°)
```

## 🚀 Utilisation (Invite de commande)

### Étape 1 : Recadrage et Normalisation
L'algorithme requiert que les images soient parfaitement alignées et normalisées en luminosité. 
Ouvrez un terminal Python ou exécutez la fonction `recadrer_normaliser('echantillon_A/')`. 
*   **Interaction :** Une fenêtre va s'ouvrir pour chaque image. Vous devez **cliquer** avec votre souris sur un point de repère commun (une infractuosité, une marque) sur chaque photo pour que le programme recadre automatiquement la pile d'images. Si les images sont déjà parfaitement fixes et identiques, vous pouvez fermer directement les fenêtres.

### Étape 2 : Lancement du traitement
Exécutez ensuite la fonction `traitement('echantillon_A/')`.

### (Astuce) Lancement direct depuis le terminal Linux
Si vous souhaitez lancer le programme entier d'un seul coup via une ligne de commande comme à l'époque (`python3 reconstruction_v3.py echantillon_A/`), ajoutez ces lignes tout à la fin de votre fichier `reconstruction_v3.py` :

```python
if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        dossier_cible = sys.argv[1]
        # Assurez-vous que le nom du dossier finit par un "/"
        if not dossier_cible.endswith('/'):
            dossier_cible += '/'
        print(f"Lancement du recadrage pour le dossier : {dossier_cible}")
        recadrer_normaliser(dossier_cible)
        print("Lancement de la reconstruction 3D...")
        traitement(dossier_cible)
    else:
        print("Veuillez indiquer le dossier à traiter. Exemple : python3 reconstruction_v3.py data/")
```

## 📊 Ce que retourne le code (Sorties)

Une fois le traitement terminé, le programme génère les éléments suivants dans le dossier analysé :
1. **`reconstruction.html` :** Le résultat final. Un fichier HTML contenant un graphique 3D interactif (généré avec Plotly) de la surface reconstituée. Vous pouvez l'ouvrir avec n'importe quel navigateur web (Chrome, Firefox...) pour zoomer et faire tourner votre échantillon.
2. **Une image `.jpg` :** Une sauvegarde de la carte de profondeur (nommée d'après l'écart-type des altitudes calculées).
3. **Des fenêtres Matplotlib :** Pendant l'exécution, le programme affiche temporairement l'image de l'albédo (la texture 2D sans les ombres) et l'histogramme des profondeurs calculées.