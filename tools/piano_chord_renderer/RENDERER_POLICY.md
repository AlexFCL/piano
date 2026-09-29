# Politique canonique — rendu des accords piano

## Hiérarchie des sources

1. `data/music-theory/tonality-colors.json` — autorité runtime absolue des couleurs.
2. `docs/chatgpt/RENDERERS_SOURCE_OF_TRUTH_V1.md` — ordre de priorité commun à tous les renderers.
3. `docs/chatgpt/PALETTE_TONALITES_ACCORDS_GAMMES_V1.md` — explication fonctionnelle.
4. Le présent fichier — politique spécifique au renderer d'accords.

En cas de contradiction, la source située plus haut l'emporte. Si le JSON n'est pas accessible, ne pas générer d'asset et ne substituer aucune couleur.

## Règle absolue

Toute image d'accord doit dériver du template officiel 711×254, par compositing déterministe.

## Pipeline

1. vérifier le SHA-256 du template ;
2. lire la palette tonique/mode dans `data/music-theory/tonality-colors.json` ;
3. calculer les trois notes théoriques de l'accord ;
4. appliquer le renversement demandé ;
5. mapper les notes vers les slots physiques du clavier ;
6. remplir toutes les touches actives avec la couleur de la tonique + du mode ;
7. restaurer la structure des touches noires depuis le template ;
8. poser les libellés théoriques en blanc ;
9. valider puis exporter.

## Invariants

- format : 711×254 ;
- exactement trois notes actives ;
- couleur issue de la table tonique/mode canonique ;
- même couleur sur les touches blanches et noires actives ;
- libellé théorique distinct du slot physique ;
- aucune génération visuelle libre ;
- aucune couleur ne doit être dérivée du fait qu'une touche soit blanche ou noire.
