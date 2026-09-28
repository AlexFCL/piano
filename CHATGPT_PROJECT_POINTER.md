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
1. lire d'abord `docs/chatgpt/PALETTE_TONALITES_ACCORDS_GAMMES_V1.md`;
2. utiliser `data/music-theory/tonality-colors.json` comme source runtime des couleurs ;
3. lire `tools/piano_scale_renderer/README.md` et `tools/piano_scale_renderer/RENDERER_POLICY.md`;
4. récupérer le renderer, le template, les définitions et les tests depuis ce dossier ;
5. exécuter les tests ;
6. exécuter `piano_scale_renderer.py` ;
7. utiliser uniquement la sortie validée.

Règle verrouillée : toutes les touches actives d'une même gamme utilisent la même couleur tonique/mode. Une ancienne règle de couleur dépendant du type physique de touche est obsolète et ne doit jamais être réintroduite.

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
- Générateur aléatoire / page unique d’exercice : `scale_training.html`
- Ancienne page `scales.html` : route de compatibilité qui redirige vers `scale_training.html`
- Images validées : `images/Scales/`
- Logique d’entraînement : `js/scales_script.js`
- Logique d’affichage de la bibliothèque : `js/scale_library.js`
- Style d’entraînement : `css/scales_styles.css`
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

## Générateur d'accords — architecture actuelle
- Page unique de l'exercice : `chords.html`
- Logique runtime : `js/chords_script.js`
- Style dédié : `css/chords_styles.css`
- Assets : `images/Chords/<tonique>-<majeur|mineur>-<fond|1er|2eme>.png`
- `second_page.html` est conservée uniquement comme route de compatibilité et redirige vers `chords.html`.

Comportement fonctionnel :
1. l'entrée Accords depuis l'accueil ouvre directement la page d'exercice `chords.html`, sans page de réglage intermédiaire ;
2. l'utilisateur peut modifier le temps de réponse directement sur cette page ;
3. les filtres `Majeur` / `Mineur` sont multi-sélectionnables, avec au moins une option active ;
4. les filtres `Fondamental` / `1er renversement` / `2e renversement` sont multi-sélectionnables, avec au moins une option active ;
5. une modification de filtre ou de durée s'applique au tirage suivant et ne coupe pas le tour en cours ;
6. la consigne affiche l'accord et le renversement sur une seule ligne, par exemple `Eb, 2e renversement` ou `G#, fondamental`; pour un mineur, le mode reste explicite, par exemple `Eb mineur, 2e renversement` ;
7. chaque tour affiche d'abord la consigne seule pendant le délai choisi ;
8. l'image-réponse est ensuite affichée pendant 3 secondes ;
9. un nouveau tirage est lancé automatiquement en évitant, lorsque plusieurs choix sont disponibles, de répéter immédiatement exactement le même accord.



### Générateur aléatoire de gammes — comportement
1. le lien `Entraînement aléatoire` de la bibliothèque ouvre directement `scale_training.html`, sans page de réglage intermédiaire ;
2. le temps de réponse est modifiable directement sur la page d’exercice ;
3. les boutons `Majeur` et `Mineur` sont multi-sélectionnables, avec au moins un type actif ;
4. une modification de type ou de durée s’applique au tirage suivant et ne coupe pas le tour en cours ;
5. le pool majeur contient les 12 gammes majeures et le pool mineur les 12 gammes mineures naturelles ;
6. chaque tour affiche d’abord le nom de la gamme pendant le délai choisi ;
7. l’image-réponse est ensuite affichée pendant 3 secondes ;
8. lorsque plusieurs gammes sont disponibles, le générateur évite de répéter immédiatement la même gamme.
