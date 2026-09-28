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

## RÉSOLU — nomenclature mineure

Décision du 28/09/2026 :

- entraînement/renderer : `Eb mineur naturel`
- théorie : `Eb` éolien
- notes attendues : `Eb, F, Gb, Ab, Bb, Cb, Db`

L'ancienne entrée `D#` éolien du dataset de théorie a été remplacée. L'incohérence est considérée comme résolue pour le mode éolien.

## OBSERVÉ — accords / renversement

Dans `js/second_page_script.js`, le renversement/fondamentale est tiré et sélectionne l'image, mais le texte affiché ne contient pas cette troisième valeur.

**NON DÉTERMINABLE :** bug ou comportement voulu.

## OBSERVÉ — catégories

`data/categories.json` existe mais l'accueil est écrit directement dans `index.html`.

Risque : double maintenance.

## MITIGÉ — duplication des gammes

Définitions / mappings présents dans :
- renderer `tools/piano_scale_renderer/scales.json`
- entraînement `js/scales_script.js`
- bibliothèque `js/scale_library.js`
- théorie `data/music-theory/scales.json`
- Notion

Le risque de divergence runtime est désormais couvert par `tests/test_scale_consistency.py` et la CI `.github/workflows/scale-consistency.yml`. Le test vérifie les 24 gammes visuelles, leurs mappings vers les PNG et la concordance des orthographes ioniennes/éoliennes avec le renderer.

Notion reste volontairement hors de cette CI : c'est une spécification fonctionnelle externe et sa cohérence documentaire reste à vérifier lors d'un changement de contrat.

## OBSERVÉ — tests

- renderer : 8 tests automatisés ;
- cohérence des sources de gammes : 5 tests automatisés, exécutés par GitHub Actions ;
- navigateur / E2E : aucune suite automatisée documentée.

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
