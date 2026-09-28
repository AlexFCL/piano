# APPLICATION PIANO — POINTEUR DE BOOTSTRAP CHATGPT

Ce fichier doit permettre à une future conversation de retrouver immédiatement les sources utiles sans dépendre de la mémoire d'une ancienne conversation.

## Identité
- Projet : Application piano
- Dépôt : `AlexFCL/piano`
- Branche canonique : `master`
- Stack : HTML / CSS / JavaScript statique
- État réel du code : GitHub

## Première lecture
1. `docs/chatgpt/PLAYBOOK_CHATGPT_APPLICATION_PIANO_V4.md`
2. `docs/chatgpt/APPLICATION_PIANO_MASTER_V4.md` si davantage de contexte est nécessaire
3. `docs/chatgpt/MANIFEST_APPLICATION_PIANO_V4.md` avant toute suppression, archivage ou nettoyage

## Renderer canonique des images de gammes
Chemin obligatoire :
`tools/piano_scale_renderer/`

Pour toute génération, correction ou remplacement d'un PNG de gamme :
1. lire `tools/piano_scale_renderer/README.md`;
2. lire `tools/piano_scale_renderer/RENDERER_POLICY.md`;
3. récupérer le renderer, le template, les définitions et les tests depuis ce dossier;
4. exécuter les tests;
5. exécuter `piano_scale_renderer.py`;
6. utiliser uniquement la sortie validée.

Ne jamais improviser une image de gamme avec un générateur visuel libre ou un redessin approximatif.

## Palette tonique / mode — accords et gammes
Référence canonique :
`docs/chatgpt/PALETTE_TONALITES_ACCORDS_GAMMES_V1.md`

Règle courte : tonique = famille de couleur ; majeur = variante majeure ; mineur = variante mineure ; base = variante neutre/réserve future. La source runtime structurée est `data/music-theory/tonality-colors.json`.

## Renderer canonique des images d'accords
Chemin : `tools/piano_chord_renderer/`.
Il utilise le template 711×254 et `data/music-theory/tonality-colors.json`. Les touches actives, blanches ou noires, reçoivent la même couleur tonique/mode et les notes sont libellées en blanc. Les assets runtime sont dans `images/Chords/` avec le nommage `<tonique>-<majeur|mineur>-<fond|1er|2eme>.png`.

## Sources fonctionnelles
- Application live : GitHub
- Intentions / spécifications fonctionnelles des gammes : Notion, page « Spécifications – Générateur de gammes piano »
- Renderer des PNG de gammes : GitHub `tools/piano_scale_renderer/`

## Règle de conservation
Ne jamais conseiller la suppression d'une source, d'un script, d'un asset, d'un template, d'un test ou d'une archive sans avoir vérifié son contenu, ses dépendances, son remplaçant et l'existence d'un backup. En cas de doute : conserver.


## Pages gammes
- Bibliothèque visuelle / point d’entrée depuis l’accueil : `scale_library.html`
- Générateur aléatoire / réglage du temps : `scales.html`
- Exercice en cours : `scale_training.html`
- Images validées : `images/Scales/`
- Logique d’affichage de la bibliothèque : `js/scale_library.js`
- Style de la bibliothèque : `css/scale_library.css`

La bibliothèque affiche actuellement 12 gammes majeures et 12 gammes mineures naturelles. Les familles futures (ex. pentatoniques) doivent s’ajouter comme nouveaux types sans remplacer les PNG canoniques existants.


## Contrôle automatique de cohérence des gammes
- Test : `tests/test_scale_consistency.py`
- CI : `.github/workflows/scale-consistency.yml`
- Commande locale : `python -m unittest -v tests/test_scale_consistency.py`
- Sources contrôlées : renderer `scales.json`, entraînement `js/scales_script.js`, bibliothèque `js/scale_library.js`, théorie `data/music-theory/scales.json` et existence des PNG référencés.

Ce contrôle empêche une divergence silencieuse entre les sources qui décrivent les 24 gammes visuelles. Notion reste une spécification fonctionnelle et n'est pas une source runtime testée par cette CI.


## Accueil et catégories
- Métadonnées des 5 cartes d'accueil : `data/categories.json`
- Rendu de l'accueil : `js/home.js`
- Pages génériques Basse/Rythme : `category.html` + `js/category_page.js`
- Test : `tests/test_categories.py`
- CI : `.github/workflows/category-consistency.yml`

Ne pas recopier manuellement dans `index.html` les titres, descriptions, icônes ou routes des catégories : l'accueil est rendu depuis `data/categories.json`.
