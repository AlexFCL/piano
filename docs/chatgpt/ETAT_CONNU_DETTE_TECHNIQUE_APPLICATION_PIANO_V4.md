# ÉTAT CONNU / DETTE TECHNIQUE — APPLICATION PIANO V4

**Mise à jour :** le renderer de gammes est désormais destiné à être versionné dans `tools/piano_scale_renderer/` ; le ZIP devient un backup historique.
Ce document ne donne pas un ordre de correction. Il sépare ce qui est observé de ce qui est à décider.

## HISTORIQUE — ancienne comparaison des PNG de gammes

L'ancien constat « 20/24 fichiers correspondent au renderer fourni » provenait d'un renderer/snapshot antérieur et **ne doit plus être utilisé pour juger la conformité actuelle**.

État structurel vérifié au 29/09/2026 :
- `images/Scales/` contient 48 PNG ;
- 24 correspondent aux gammes classiques (12 majeures + 12 mineures naturelles) ;
- 24 correspondent aux pentatoniques ;
- la présence des pentatoniques dans les assets ne signifie pas qu'elles sont déjà exposées dans la bibliothèque UI.

Pour contrôler la conformité colorimétrique, il faut régénérer avec le renderer courant et `data/music-theory/tonality-colors.json`, puis comparer les sorties aux assets live.

## RÉSOLU — nomenclature mineure

Décision du 28/09/2026 :

- entraînement/renderer : `Eb mineur naturel`
- théorie : `Eb` éolien
- notes attendues : `Eb, F, Gb, Ab, Bb, Cb, Db`

L'ancienne entrée `D#` éolien du dataset de théorie a été remplacée. L'incohérence est considérée comme résolue pour le mode éolien.

## RÉSOLU — accords / renversement

Décision du 28/09/2026 :

- le renversement/fondamentale reste tiré parmi 3 positions ;
- il sélectionne toujours l'image correspondante ;
- il est désormais affiché dans la consigne sous le nom de l'accord ;
- libellés : `fond.`, `1er (tonique haut)`, `2ème (tierce haut)`.

Les 102 fichiers `images/Chords/*.png` couvrent toujours exactement les combinaisons `17 × 2 × 3`.

## RÉSOLU — catégories

Décision du 28/09/2026 :

- les 5 cartes de l'accueil sont décrites dans `data/categories.json` ;
- `js/home.js` génère les cartes depuis cette source ;
- `js/category_page.js` réutilise la même source pour les métadonnées Basse/Rythme ;
- `tests/test_categories.py` + `.github/workflows/category-consistency.yml` contrôlent la structure, l'ordre, les routes et les fichiers d'exercices.

Le risque de double maintenance des métadonnées d'accueil est considéré comme résolu.

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

Les contrôles automatisés couvrent actuellement :
- renderer de gammes et pentatoniques ;
- renderer d'accords ;
- cohérence des sources de gammes ;
- cohérence des catégories ;
- politique commune de source de palette des renderers.

Les nombres exacts de méthodes de test ne sont pas figés ici : ils évoluent avec les suites. Aucune suite navigateur / E2E complète n'est documentée.

## OBSERVÉ — fichiers legacy

- `second_page_backup.html`
- `Template.png`
- `Template.jpg`
- `Readme.txt`

Rôle exact non documenté pour tous. Conserver par défaut.

## OBSERVÉ — dépendance Google Fonts

Les CSS chargent Inter depuis Google Fonts. Fallback système présent.

## MITIGÉ — GitHub Pages / bruit de CI

GitHub Pages est actif et un push sur `master` déclenche un `pages build and deployment`.

Incident observé le 29/09/2026 : 17 commits en quelques minutes ont déclenché 17 builds Pages, dont la plupart ont été annulés par des commits plus récents, ainsi que plusieurs workflows supplémentaires.

Mesures retenues :
- préparer les changements en lecture seule ;
- regrouper une tâche multi-fichiers dans un seul commit ;
- déplacer `master` une seule fois ;
- ajouter `concurrency` aux workflows maison pour annuler un run obsolète ;
- restreindre le workflow lourd de génération des accords aux vrais inputs susceptibles de modifier les PNG ;
- ne pas déclencher les workflows uniquement parce que leur propre fichier YAML a été édité sur `master`.

Le mode exact de source GitHub Pages reste distinct de ce constat ; ce qui est vérifié ici est le comportement effectif des builds lors des pushs sur `master`.
