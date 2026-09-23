# APPLICATION PIANO — RÉFÉRENTIEL MAÎTRE V4

## 1. Identité
Application web statique d'entraînement musical.
- Dépôt : `AlexFCL/piano`
- Branche canonique : `master`
- Stack : HTML / CSS / JavaScript
- GitHub est la source de vérité pour l'état réel du code.

Ce projet est distinct du projet `AlexFCL/perms-basse`.

## 2. Architecture applicative
### Accueil
`index.html` expose les entrées principales : accords, gammes, théorie musicale, rythme et basse.

### Accords
Flux principal :
`chords.html` → `js/main.js` → `second_page.html` → `js/second_page_script.js`

Les images d'accords vivent dans `images/Chords/`.

### Gammes
Flux principal :
`scales.html` → `js/scales_main.js` → `scale_training.html` → `js/scales_script.js`

Contrat fonctionnel actuel : nom de gamme → délai utilisateur → image-réponse 3 s → gamme suivante, sans rechargement complet.

Les images utilisées par l'application vivent dans `images/Scales/`.

### Théorie
`theory.html`, `theory_quiz.html`, `js/theory_page.js`, `js/theory_quiz.js`, `data/music-theory/scales.json`.

### Basse / rythme
`category.html`, `js/category_page.js`, JSON sous `data/exercises/`.

## 3. Renderer canonique des gammes
Le code de production des PNG est désormais versionné dans :
`tools/piano_scale_renderer/`

Ce dossier est une dépendance opérationnelle du projet, pas une archive.

Il contient :
- `piano_scale_renderer.py`
- `requirements.txt`
- `scales.json`
- `official_template.png`
- `test_renderer.py`
- `golden/C-majeur.png`
- `golden/E-majeur.png`
- `README.md`
- `RENDERER_POLICY.md`

Règle : toute future génération/correction d'image de gamme doit partir de ce dossier GitHub. Aucun rendu visuel libre ne doit produire l'asset final.

## 4. Source de vérité par sujet
- État live : GitHub.
- Architecture globale / routage : ce référentiel + Playbook.
- Conservation / suppression : Manifest.
- Spécification fonctionnelle du générateur de gammes : Notion.
- PNG de gammes : renderer GitHub + ses tests.
- Historique : anciennes versions documentaires et backups, à conserver tant qu'une suppression n'est pas explicitement validée.

## 5. Règles de maintenance
Avant modification : vérifier HEAD et lire les fichiers actuels.
Après modification : valider le comportement, confirmer le commit et mettre à jour la documentation si l'architecture ou un contrat change.

Avant suppression : inventaire, dépendances, remplaçant, backup. En cas de doute, conserver.

## 6. Dette / divergences à ne pas masquer
- Des définitions de gammes sont dupliquées entre renderer, script d'entraînement et données de théorie.
- Eb mineur naturel et D# éolien ne sont pas la même convention documentaire dans les jeux actuels.
- Un audit précédent a identifié des divergences entre certains PNG live et la sortie du renderer. Recontrôler l'état GitHub au moment d'une correction.
- `data/categories.json` ne constitue pas nécessairement le registre de l'accueil : vérifier le code live.
- Les fichiers legacy ne sont pas supprimables sur leur seul nom.

## 7. Règle anti-perte
Une nouvelle version documentaire ne remplace jamais automatiquement un script, un template, un asset, un test ou un backup. Toute suppression doit être prouvée sûre.
