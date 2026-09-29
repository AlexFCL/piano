# Renderer déterministe — accords piano

Ce dossier produit les images d'accords à partir du template 711×254 du projet, sans redessin libre.

## Sources de vérité

Ordre obligatoire :
1. palette runtime : `../../data/music-theory/tonality-colors.json` ;
2. politique commune : `../../docs/chatgpt/RENDERERS_SOURCE_OF_TRUTH_V1.md` ;
3. explication fonctionnelle : `../../docs/chatgpt/PALETTE_TONALITES_ACCORDS_GAMMES_V1.md` ;
4. géométrie : `official_template.png` ;
5. logique de l'application : 17 graphies de tonique × 2 qualités × 3 positions = 102 combinaisons.

## Palette

La couleur dépend exclusivement de la tonique et du mode résolus depuis le JSON canonique. Les touches blanches et noires actives utilisent la **même couleur tonique/mode**.

Aucune valeur active ne doit être recopiée dans ce README ou définie en dur dans le renderer.

## Labels

Chaque touche active reçoit le nom théorique de la note en blanc. Les enharmonies et altérations théoriques sont conservées : Eb, Bb, F##, etc.

## Tests

```bash
python -m unittest -v test_renderer.py
```

La suite couvre les 102 combinaisons, la palette documentée, les trois positions de C majeur et plusieurs orthographes enharmoniques.
