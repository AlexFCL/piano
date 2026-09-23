# ÉTAT CONNU / DETTE TECHNIQUE — APPLICATION PIANO V4

**Mise à jour :** le renderer de gammes est désormais destiné à être versionné dans `tools/piano_scale_renderer/` ; le ZIP devient un backup historique.
Ce document ne donne pas un ordre de correction. Il sépare ce qui est observé de ce qui est à décider.

## OBSERVÉ — PNG de gammes

20/24 fichiers `images/Scales/` correspondent au renderer fourni.

Non identiques :
- `D-majeur.png`
- `E-majeur.png`
- `Eb-majeur.png`
- `F-majeur.png`

**Décision requise avant action :** faut-il remplacer les quatre assets GitHub par les sorties canoniques actuelles ?

## OBSERVÉ — nomenclature mineure

- entraînement/renderer : `Eb mineur naturel`
- théorie : `D#` éolien

**Décision requise :** conserver les deux orthographes selon le contexte ou harmoniser explicitement.

## OBSERVÉ — accords / renversement

Dans `js/second_page_script.js`, le renversement/fondamentale est tiré et sélectionne l'image, mais le texte affiché ne contient pas cette troisième valeur.

**NON DÉTERMINABLE :** bug ou comportement voulu.

## OBSERVÉ — catégories

`data/categories.json` existe mais l'accueil est écrit directement dans `index.html`.

Risque : double maintenance.

## OBSERVÉ — duplication des gammes

Définitions présentes dans :
- renderer `scales.json`
- `js/scales_script.js`
- théorie `data/music-theory/scales.json`
- Notion

Risque : divergence silencieuse.

## OBSERVÉ — tests

- renderer : 8 tests automatisés, actuellement OK ;
- application web : aucune suite automatisée observée.

## OBSERVÉ — fichiers legacy

- `second_page_backup.html`
- `Template.png`
- `Template.jpg`
- `Readme.txt`

Rôle exact non documenté pour tous. Conserver par défaut.

## OBSERVÉ — dépendance Google Fonts

Les CSS chargent Inter depuis Google Fonts. Fallback système présent.

## OBSERVÉ — GitHub Pages

`has_pages: true`. Configuration exacte de la source de publication non vérifiée dans cette consolidation.
