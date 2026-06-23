SPRITES — mode d'emploi
=======================

Dépose simplement tes PNG ici, le jeu les charge tout seul.
Tant qu'un fichier est absent ou invalide, le jeu garde les voitures
vectorielles (repli automatique) — donc rien ne casse si tu n'as encore rien.

Fichiers attendus (par défaut) :
  sprites/mustang.png   -> voiture de la map "Coastal Test"
  sprites/f1.png        -> voiture des circuits F1

La config se règle en haut du <script> de index.html, objet SPRITES :

  mustang: { src:"sprites/mustang.png", frames:1, facing:"up", dw:20, dh:36 }


DEUX MODES
----------

1) SPRITE UNIQUE (le plus simple — ex. packs Kenney CC0)
   - Une seule image, vue de dessus, fond TRANSPARENT (PNG).
   - Le jeu la fait pivoter en temps réel selon le cap.
   - Règle "facing" selon l'orientation du nez dans TON image :
       "up"  (nez vers le haut)   <- défaut
       "right", "down", "left"
   - frames:1

2) SPRITE SHEET ROTATION (le look "3D" — pré-rendu Blender)
   - Plusieurs cellules, une par angle, sur une grille.
   - Le jeu NE pivote PAS : il choisit la bonne cellule selon le cap.
   - Config exemple (36 angles sur une grille 6x6) :
       f1: { src:"sprites/f1.png", frames:36, cols:6, rows:6, dir:1, base:0, dw:24, dh:40 }
     * frames = nombre total de cellules
     * cols/rows = grille
     * dir  = sens de rotation des frames (+1 ou -1) — inverse si ça tourne à l'envers
     * base = angle (radians) de la frame n°0 — ajuste si l'orientation est décalée
   - Astuce rendu : caméra orthographique vue de dessus inclinée ~30°,
     une lumière "soleil" + ombre douce, fond transparent, 36 ou 72 frames.


RÉGLAGES COMMUNS
----------------
   dw / dh = taille d'affichage en unités monde (largeur / longueur).
             Garde le ratio de ton image pour éviter la déformation.
             (CAR_SCALE dans le CONFIG s'applique en plus, globalement.)


OÙ TROUVER DES ASSETS (licences claires)
----------------------------------------
   - Kenney.nl            : packs Racing / Top-Down, CC0 (gratuit, commercial OK)
   - Quaternius / Poly Pizza / Sketchfab (filtre licence) : modèles 3D à pré-rendre
   - itch.io / OpenGameArt : sprites top-down (vérifier la licence par asset)

   ⚠ Évite les vraies marques (Ford Mustang) et livrées F1 officielles si tu
     comptes publier : logos/designs protégés. Pour un usage perso, pas de souci.
