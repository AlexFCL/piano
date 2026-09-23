# PLAYBOOK CHATGPT — APPLICATION PIANO V4

But : répondre vite en allant directement à la bonne source.

## Démarrage
Si le contexte est incomplet, lire d'abord `/CHATGPT_PROJECT_POINTER.md`.

Toujours vérifier GitHub live avant une affirmation sur l'état actuel ou avant une mutation.

## Routage
### Accueil / UI
Lire les HTML/CSS concernés dans GitHub.

### Accords
Lire :
- `chords.html`
- `second_page.html`
- `js/main.js`
- `js/second_page_script.js`
- CSS associés

Ne pas extrapoler le comportement des gammes aux accords.

### Gammes — comportement
Lire :
- `scales.html`
- `scale_training.html`
- `js/scales_main.js`
- `js/scales_script.js`
- `css/scales_styles.css`
Consulter Notion si l'intention fonctionnelle doit être arbitrée.

### Gammes — images
SOURCE CANONIQUE :
`AlexFCL/piano` → `master` → `tools/piano_scale_renderer/`

Lire :
- `README.md`
- `RENDERER_POLICY.md`
- `piano_scale_renderer.py`
- `scales.json`
- `official_template.png`
- `test_renderer.py`
- `golden/`

Procédure obligatoire :
GitHub → récupération du dossier → tests → renderer → validation → PNG.

Ne jamais générer librement l'asset final.

### Théorie
Lire :
- `theory.html`
- `theory_quiz.html`
- `js/theory_page.js`
- `js/theory_quiz.js`
- `data/exercises/theorie.json`
- `data/music-theory/scales.json`

### Basse / rythme
Lire `category.html`, `js/category_page.js` et le JSON de catégorie concerné.

## Mutation GitHub
1. vérifier repo `AlexFCL/piano`;
2. vérifier branche `master`;
3. lire HEAD;
4. lire les fichiers exacts;
5. faire le changement minimal;
6. vérifier les régressions;
7. commit;
8. confirmer SHA et fichiers modifiés.

## Suppression
Avant toute recommandation de suppression : inspecter le contenu, rechercher les dépendances, identifier le remplaçant, vérifier le backup. Si une preuve manque : CONSERVER.

## Alertes connues
- Les jeux de données « gammes » existent à plusieurs endroits et ne doivent pas être fusionnés silencieusement.
- L'entraînement image utilise Eb mineur naturel tandis que la théorie comporte D# éolien : ne pas réconcilier sans décision explicite.
- Des PNG live peuvent diverger du renderer ; vérifier avant de les remplacer.
