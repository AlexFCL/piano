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
Lire seulement les HTML/CSS concernés dans GitHub.

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
- `js/scales_main.js`
- `js/scales_script.js`
- `css/scales_styles.css`

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
- `category.html`
- `js/category_page.js`
- JSON de la catégorie
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
- Renderer/entraînement : Eb mineur naturel ; théorie : D# éolien.
- `data/categories.json` n'alimente pas l'accueil.
- le renversement des accords influence l'image mais n'est pas affiché dans le texte actuel.
- `second_page_backup.html` et templates racine : ne pas supprimer par le nom seul.
- aucune suite de tests web automatisés observée ; les tests solides concernent le renderer.

## 6. Source de vérité courte

- **État actuel : GitHub**
- **Architecture/méthode : MASTER V4**
- **Conservation : MANIFEST V4**
- **Images : GitHub `tools/piano_scale_renderer/` (inclut V1.7 + renderer + template + tests)**
- **Intention gammes : Notion**
- **Historique : V1/V2/V3**
