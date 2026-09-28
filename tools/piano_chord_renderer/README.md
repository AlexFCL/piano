# Renderer déterministe — accords piano

Ce dossier produit les images d'accords à partir du template 711×254 du projet, sans redessin libre.

## Sources de vérité

- géométrie : `official_template.png` ;
- palette tonique/mode : `../../data/music-theory/tonality-colors.json` ;
- logique de l'application : 17 graphies de tonique × 2 qualités × 3 positions = 102 combinaisons.

## Palette

La couleur dépend de la tonique et du mode. Par exemple :

- C majeur → `#B51B1B` ;
- C mineur → `#EB8080`.

Les touches blanches et noires actives utilisent la **même couleur tonique/mode**. Ce renderer n'utilise aucune couleur dépendant du type physique de touche : seule la paire tonique/mode détermine la couleur.

## Labels

Chaque touche active reçoit le nom théorique de la note en blanc. Les enharmonies et altérations théoriques sont conservées : Eb, Bb, F##, etc.

## Tests

```bash
python -m unittest -v test_renderer.py
```

La suite couvre les 102 combinaisons, la palette documentée, les trois positions de C majeur et plusieurs orthographes enharmoniques.
