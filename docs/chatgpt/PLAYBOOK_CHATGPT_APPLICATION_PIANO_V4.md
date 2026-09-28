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
- `second_page.html`
- `js/main.js`
- `js/second_page_script.js`
- `css/styles.css`
- `css/second_page_styles.css`

Attention : le comportement des accords n'est pas le même que celui des gammes.

### Gammes — comportement
Lire :
- `scales.html`
- `scale_training.html`
- `scale_library.html` si bibliothèque concernée
- `js/scales_main.js`
- `js/scales_script.js`
- `js/scale_library.js` si bibliothèque concernée
- `css/scales_styles.css`
- `css/scale_library.css` si bibliothèque concernée

Consulter Notion si l'intention fonctionnelle doit être arbitrée.

### Gammes — image

**Chemin canonique obligatoire :** `AlexFCL/piano` → `master` → `tools/piano_scale_renderer/`.

Lire/récupérer :
- `README.md`
- `SOURCE_IMAGES_GAMMES_PIANO_V1.7.md`
- `piano_scale_renderer.py`
- `scales.json`
- `official_template.png`
- `test_renderer.py`
- `golden/`

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
3. lire HEAD ;
4. lire les fichiers exacts ;
5. faire une modification minimale ;
6. vérifier les régressions visibles ;
7. commit ;
8. confirmer SHA et fichiers modifiés ;
9. mettre à jour V4 si architecture/contrat modifié.

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

- 4 PNG de gammes GitHub ne correspondent pas au renderer : D, E, Eb, F majeurs.
- Convention alignée : renderer/entraînement = Eb mineur naturel ; théorie = Eb éolien (notes Eb, F, Gb, Ab, Bb, Cb, Db).
- accueil data-driven : `data/categories.json` pilote les 5 cartes via `js/home.js` ; conserver la CI `category-consistency.yml` verte.
- le renversement des accords est affiché dans la consigne et doit rester synchronisé avec l'index d'image correspondant.
- `second_page_backup.html` et templates racine : ne pas supprimer par le nom seul.
- contrôle inter-sources automatisé actif via `tests/test_scale_consistency.py` + GitHub Actions ; pas de suite navigateur/E2E documentée.

## 6. Source de vérité courte

- **État actuel : GitHub**
- **Architecture/méthode : MASTER V4**
- **Conservation : MANIFEST V4**
- **Images : GitHub `tools/piano_scale_renderer/` (inclut V1.7 + renderer + template + tests)**
- **Intention gammes : Notion**
- **Historique : V1/V2/V3**
