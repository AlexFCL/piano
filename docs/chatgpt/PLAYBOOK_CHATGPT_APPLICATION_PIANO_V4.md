# PLAYBOOK CHATGPT — APPLICATION PIANO V4

**But :** répondre vite sans sacrifier la fiabilité.  
**Principe :** lire peu, mais lire la bonne source.

## 1. Démarrage de toute future demande

Si le contexte est incomplet, lire d’abord `AlexFCL/piano/CHATGPT_PROJECT_POINTER.md`.

1. Identifier le domaine : accueil/UI, accords, gammes fonctionnelles, images de gammes, théorie, basse/rythme, infrastructure/documentation.
2. Si la demande concerne l'état courant ou une modification : **vérifier GitHub live**.
3. Si la demande concerne les PNG de gammes : **ouvrir GitHub `tools/piano_scale_renderer/` ; c’est le renderer canonique.**
4. Ne jamais extrapoler l'architecture d'un autre projet.
5. Ne jamais recommander une suppression sans le protocole de sécurité.

### Politique de mutation GitHub

Pour toute tâche multi-fichiers, travailler en lecture seule jusqu'à ce que le lot soit prêt. Ne pas pousser chaque fichier séparément.

Procédure :
1. relever le HEAD de `master` ;
2. lire/préparer toutes les modifications ;
3. si l'utilisateur a demandé un contrôle avant publication, attendre son « GO push » ;
4. créer un arbre Git contenant toutes les modifications ;
5. créer **un seul commit** ;
6. revérifier que le HEAD de `master` n'a pas changé ;
7. déplacer `master` une seule fois ;
8. vérifier les workflows déclenchés.

Éviter `update_file` répété sur `master` : chaque appel crée un commit et peut relancer GitHub Pages.

## 2. Routage par domaine

### UI / accueil / CSS
Pour l'accueil, lire :
- `index.html`
- `js/home.js`
- `data/categories.json`
- `css/styles.css`

Les 5 cartes d'accueil sont pilotées par `data/categories.json`. Ne pas les recopier en dur dans `index.html`.

Contrôle :
`python -m unittest -v tests/test_categories.py`

CI :
`.github/workflows/category-consistency.yml`

### Accords
Lire :
- `chords.html`
- `js/chords_script.js`
- `css/chords_styles.css`
- `second_page.html` uniquement si la route de compatibilité est concernée

Attention : le comportement des accords n'est pas le même que celui des gammes.
Pour produire/corriger une image d'accord, lire d'abord `data/music-theory/tonality-colors.json` puis `docs/chatgpt/RENDERERS_SOURCE_OF_TRUTH_V1.md`, et utiliser `tools/piano_chord_renderer/`.

### Palette accords + gammes

Ordre de lecture obligatoire pour toute production d'image :
1. `data/music-theory/tonality-colors.json` — **source runtime absolue, à lire en premier** ;
2. `docs/chatgpt/RENDERERS_SOURCE_OF_TRUTH_V1.md` — hiérarchie commune à tous les renderers ;
3. `docs/chatgpt/PALETTE_TONALITES_ACCORDS_GAMMES_V1.md` — explication fonctionnelle ;
4. politique/README/tests du renderer concerné.

Si le JSON n'est pas accessible, arrêter la génération : ne jamais substituer une couleur depuis la mémoire, un ZIP, un snapshot ou un ancien document.

- Tonique = famille chromatique.
- Majeur = variante `major`.
- Mineur = variante `minor`.
- `base` = couleur neutre conservée pour les usages sans mode / futurs.
- Source runtime : `data/music-theory/tonality-colors.json`.
- Les renderers pédagogiques doivent consommer cette palette : même couleur tonique/mode pour toutes les touches actives, blanches ou noires.
- Toute documentation ou implémentation qui réintroduit une couleur fixe dépendant du type physique de touche est obsolète.

### Gammes — comportement
Lire :
- `scale_training.html`
- `js/scales_script.js`
- `css/scales_styles.css`
- `scale_library.html` + `js/scale_library.js` + `css/scale_library.css` si la bibliothèque est concernée
- `scales.html` uniquement comme route de compatibilité

Consulter Notion si l'intention fonctionnelle doit être arbitrée.

### Gammes — image

**Chemin canonique obligatoire :** `AlexFCL/piano` → `master` → `tools/piano_scale_renderer/`.

Lire/récupérer dans cet ordre :
- `data/music-theory/tonality-colors.json`
- `docs/chatgpt/RENDERERS_SOURCE_OF_TRUTH_V1.md`
- `docs/chatgpt/PALETTE_TONALITES_ACCORDS_GAMMES_V1.md`
- `README.md`
- `SOURCE_IMAGES_GAMMES_PIANO_V1.8.md`
- `piano_scale_renderer.py`
- `scales.json`
- `official_template.png`
- `test_renderer.py`
- `golden/` uniquement comme historique, jamais comme source colorimétrique

Procédure obligatoire : récupérer depuis GitHub → exécuter les tests → générer avec le script → lire la validation → comparer si remplacement → livrer/importer.

**Ne pas chercher une autre méthode. Ne pas redessiner le clavier. Ne pas utiliser de génération d’image libre pour l’asset final.**

### Gammes — cohérence inter-sources

Test :
`tests/test_scale_consistency.py`

Commande locale :

```bash
python -m unittest -v tests/test_scale_consistency.py
```

La CI correspondante est `.github/workflows/scale-consistency.yml`. Elle doit rester verte lorsque le renderer, l'entraînement, la bibliothèque, la théorie ou les PNG de gammes sont modifiés.

### Théorie
Lire :
- `theory.html`
- `theory_quiz.html`
- `js/theory_page.js`
- `js/theory_quiz.js`
- `data/exercises/theorie.json`
- `data/music-theory/scales.json`

### Basse / rythme
Lire :
- `data/categories.json`
- `category.html`
- `js/category_page.js`
- JSON d'exercices indiqué par `exerciseFile`
- `css/library_styles.css` si UI concernée

## 3. Procédure GitHub avant mutation

1. repository = `AlexFCL/piano` ;
2. branche = `master` ;
3. relever le HEAD une fois ;
4. lire les fichiers exacts et préparer le lot sans mutation ;
5. vérifier les impacts et les tests à exécuter ;
6. si un accord de publication est prévu, attendre le « GO push » ;
7. créer tous les blobs puis **un seul tree + un seul commit** ;
8. revérifier le HEAD juste avant `update_ref` ;
9. publier sans force uniquement si le HEAD est inchangé ;
10. confirmer le SHA et les workflows réellement déclenchés.

Ne pas faire une série de `update_file` sur `master` pour une même tâche.

## 4. Suppression / nettoyage

Avant de proposer de retirer quoi que ce soit :

- ouvrir le fichier/archive ;
- inventorier son contenu ;
- chercher les dépendances ;
- identifier le remplaçant ;
- vérifier le backup ;
- préférer `ARCHIVER` à `SUPPRIMER` si le bénéfice est faible.

**En cas de doute : conserver.**

## 5. Alertes mémorisées

- Ne pas utiliser les anciennes comparaisons blob/golden pour conclure sur la conformité des PNG de gammes ; la conformité actuelle doit être vérifiée contre la palette tonique/mode et le renderer courant.
- Convention alignée : renderer/entraînement = Eb mineur naturel ; théorie = Eb éolien (notes Eb, F, Gb, Ab, Bb, Cb, Db).
- accueil data-driven : `data/categories.json` pilote les 5 cartes via `js/home.js` ; conserver la CI `category-consistency.yml` verte.
- le renversement des accords est affiché dans la consigne et doit rester synchronisé avec l'index d'image correspondant.
- `second_page_backup.html` et templates racine : ne pas supprimer par le nom seul.
- contrôle inter-sources automatisé actif via `tests/test_scale_consistency.py` + GitHub Actions ; pas de suite navigateur/E2E documentée.

## 6. Source de vérité courte

- **État actuel : GitHub**
- **Architecture/méthode : MASTER V4**
- **Conservation : MANIFEST V4**
- **Images : GitHub `tools/piano_scale_renderer/` (inclut V1.8 + renderer + template + tests)**
- **Intention gammes : Notion**
- **Historique : V1/V2/V3**
