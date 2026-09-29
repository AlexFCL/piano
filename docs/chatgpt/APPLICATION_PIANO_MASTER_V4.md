# APPLICATION PIANO — SOURCE MAÎTRE V4

**Projet :** Application piano  
**Statut :** source maître consolidée  
**Date de consolidation :** 29/09/2026 — audit global architecture, documentation et cadence GitHub/CI  
**But :** permettre à ChatGPT et au propriétaire du projet de comprendre, modifier et maintenir le projet sans perdre de dépendance importante ni confondre les sources.

---

## 0. Règles de sécurité documentaire

Ces règles s'appliquent avant toute autre règle du projet.

1. **Ne jamais recommander la suppression d'un fichier ou d'une source sans en avoir inspecté le contenu et les dépendances.**
2. **Ne jamais considérer “ancien”, “V1”, “V2”, “backup”, “zip”, “template” ou “archive” comme synonyme de supprimable.**
3. Avant toute suppression ou retrait d'une source active :
   - identifier son rôle ;
   - identifier ce qui en dépend ;
   - identifier son remplaçant exact ;
   - vérifier que le remplaçant couvre réellement toutes ses fonctions ;
   - vérifier qu'une sauvegarde indépendante existe.
4. **En cas de doute : conserver.**
5. Une nouvelle documentation peut superséder une ancienne documentation, mais elle **ne remplace jamais automatiquement** un script, un asset, un template, un test ou un historique.
6. Toute opération destructive doit être précédée d'un inventaire explicite `élément → rôle → dépendants → remplaçant → sauvegarde → décision`.

---

## 1. Source de vérité par domaine

Il n'existe pas une source unique pour tout. Utiliser la source adaptée au sujet.

| Domaine | Source prioritaire | Règle |
|---|---|---|
| État actuel du site | GitHub `AlexFCL/piano`, branche `master` | Toujours relire avant une modification |
| Architecture globale | Ce document V4 | Sert de carte du projet |
| Routage rapide ChatGPT | `PLAYBOOK_CHATGPT_APPLICATION_PIANO_V4.md` | À lire en premier dans une future demande |
| Dépendances / conservation | `MANIFEST_APPLICATION_PIANO_V4.md` | Décide ce qui doit être conservé |
| Images de gammes | GitHub `tools/piano_scale_renderer/` + `data/music-theory/tonality-colors.json` | Renderer déterministe ; la couleur doit provenir exclusivement de la paire tonique/mode |
| Images d'accords | GitHub `tools/piano_chord_renderer/` | **Source canonique exécutable** : renderer + template + tests |
| Palette tonique/mode | `data/music-theory/tonality-colors.json` | **Source runtime absolue** des couleurs Base/Majeur/Mineur ; à lire avant toute génération |
| Politique commune des renderers | `docs/chatgpt/RENDERERS_SOURCE_OF_TRUTH_V1.md` | Hiérarchie obligatoire pour tous les renderers ; interdit toute substitution si le JSON n'est pas lu |
| Hiérarchie des renderers | `docs/chatgpt/RENDERERS_SOURCE_OF_TRUTH_V1.md` | Règle de priorité commune : JSON runtime d'abord, puis politique commune, puis documentation spécifique |
| Spécification fonctionnelle du générateur de gammes | Notion `Spécifications – Générateur de gammes piano` | Intention fonctionnelle ; le code GitHub prévaut pour l'état réel |
| Anciennes décisions/documentations | Archives V1/V2/V3 | Historique seulement |

---

## 2. Identité et infrastructure

### 2.1 Dépôt canonique

- **GitHub :** `AlexFCL/piano`
- **Branche par défaut :** `master`
- **Visibilité :** publique
- **Stack :** HTML / CSS / JavaScript statique
- **Framework :** aucun framework applicatif observé
- **GitHub Pages :** le dépôt signale `has_pages: true`
- **Renderer accords canonique :** `tools/piano_chord_renderer/`
- **Renderer gammes canonique :** `tools/piano_scale_renderer/`
- **Palette runtime tonique/mode :** `data/music-theory/tonality-colors.json`
- **Documentation ChatGPT versionnée :** `docs/chatgpt/`
- **Pointeur de démarrage :** `CHATGPT_PROJECT_POINTER.md`

Le HEAD doit toujours être revérifié avant une écriture future ; ne jamais figer un SHA comme état courant dans la documentation.

### 2.2 Ce projet n'est pas le projet « Les perms de l'Intervalle »

`AlexFCL/perms-basse` est un autre projet. Ne jamais importer automatiquement dans Application piano :

- la branche `main` ;
- Next.js ;
- Vercel ;
- Cloudflare R2 ;
- Auth0 ;
- les conventions de déploiement de `perms-basse`.

### 2.3 Hébergement

GitHub Pages est actif. Le comportement observé le 29/09/2026 est qu'un push sur `master` déclenche un `pages build and deployment`. Une rafale de petits commits provoque donc une rafale de builds, souvent annulés par les commits suivants. Le **mode exact de source de publication** (branche/dossier configuré côté Pages) n'est pas documenté ici.

---

## 3. Architecture actuelle du dépôt

### 3.1 Vue d'ensemble vérifiée

Le dépôt contient actuellement :

- 10 pages HTML ;
- 6 fichiers CSS ;
- 10 scripts JavaScript ;
- 8 fichiers JSON de données ;
- 102 images d'accords ;
- 48 images de gammes (24 classiques + 24 pentatoniques) ;
- des assets/template historiques à la racine.

### 3.2 Arborescence logique

```text
AlexFCL/piano (master)
├── index.html
├── chords.html
├── second_page.html
├── second_page_backup.html
├── scales.html
├── scale_training.html
├── scale_library.html
├── theory.html
├── theory_quiz.html
├── category.html
├── Template.png
├── Template.jpg
├── Readme.txt
├── CHATGPT_PROJECT_POINTER.md
├── .github/
│   └── workflows/
│       ├── scale-consistency.yml
│       ├── category-consistency.yml
│       ├── renderer-palette-source.yml
│       └── chord-assets.yml
├── tests/
│   ├── test_scale_consistency.py
│   ├── test_categories.py
│   └── test_renderer_palette_source.py
├── tools/
│   ├── piano_scale_renderer/
│       ├── README.md
│       ├── SOURCE_IMAGES_GAMMES_PIANO_V1.8.md
│       ├── piano_scale_renderer.py
│       ├── requirements.txt
│       ├── scales.json
│       ├── official_template.png
│       ├── test_renderer.py
│       └── golden/
│           ├── C-majeur.png
│           └── E-majeur.png
│   └── piano_chord_renderer/
│       ├── README.md
│       ├── RENDERER_POLICY.md
│       ├── piano_chord_renderer.py
│       ├── official_template.png
│       ├── test_renderer.py
│       └── requirements.txt
├── docs/
│   └── chatgpt/
│       ├── APPLICATION_PIANO_MASTER_V4.md
│       ├── MANIFEST_APPLICATION_PIANO_V4.md
│       ├── PLAYBOOK_CHATGPT_APPLICATION_PIANO_V4.md
│       ├── ETAT_CONNU_DETTE_TECHNIQUE_APPLICATION_PIANO_V4.md
│       └── INSTRUCTIONS_MISE_A_JOUR_APPLICATION_PIANO_V4.md
├── css/
│   ├── styles.css
│   ├── chords_styles.css
│   ├── second_page_styles.css
│   ├── scales_styles.css
│   ├── scale_library.css
│   └── library_styles.css
├── js/
│   ├── home.js
│   ├── chords_script.js
│   ├── main.js
│   ├── second_page_script.js
│   ├── scales_main.js
│   ├── scales_script.js
│   ├── scale_library.js
│   ├── theory_page.js
│   ├── theory_quiz.js
│   └── category_page.js
├── data/
│   ├── categories.json
│   ├── exercises/
│   │   ├── basse.json
│   │   ├── rythme.json
│   │   └── theorie.json
│   └── music-theory/
│       ├── scales.json
│       └── tonality-colors.json
└── images/
    ├── Chords/   # 102 PNG
    └── Scales/   # 48 PNG : 24 classiques + 24 pentatoniques
```

---

## 4. Parcours applicatifs

### 4.1 Accueil

Flux :

```text
index.html
→ js/home.js
→ data/categories.json
→ route propre à chaque catégorie
```

`data/categories.json` est la source des métadonnées des cinq cartes d'accueil : identifiant, titre, description, icône et route.

Ordre actuel :

1. Accords
2. Gammes
3. Théorie musicale
4. Rythme
5. Basse

`index.html` ne duplique plus ces métadonnées : `js/home.js` construit les cartes à partir du JSON. Les catégories génériques Rythme et Basse utilisent en plus le champ `exerciseFile` pour pointer vers leur fichier d'exercices.

### 4.2 Accords

Flux runtime actuel :

```text
index.html
→ data/categories.json
→ chords.html
→ js/chords_script.js
→ images/Chords/<tonique>-<majeur|mineur>-<fond|1er|2eme>.png
```

`second_page.html` est conservée comme route de compatibilité, mais la page d'exercice courante est `chords.html`.

Comportement actuel :
- temps de réponse réglable directement sur la page, minimum 1 s ;
- filtres Majeur/Mineur multi-sélectionnables avec au moins une option active ;
- filtres Fondamental/1er/2e renversement multi-sélectionnables avec au moins une option active ;
- changement de filtre ou de durée appliqué au tour suivant ;
- consigne = accord + position ;
- réponse affichée pendant 3 s ;
- répétition immédiate évitée lorsqu'il existe plusieurs choix.

Renderer canonique : `tools/piano_chord_renderer/`. Palette runtime : `data/music-theory/tonality-colors.json`.

### 4.3 Gammes — entraînement visuel

Deux parcours sont distincts :

```text
index.html
→ scale_library.html
→ js/scale_library.js
→ images/Scales/*.png
```

et :

```text
scale_library.html
→ scale_training.html
→ js/scales_script.js
→ images/Scales/*.png
```

`scales.html` reste une route de compatibilité qui redirige vers `scale_training.html`.

L'entraînement propose actuellement 12 majeures + 12 mineures naturelles, avec temps de réponse réglable (minimum 1 s), filtres Majeur/Mineur, réponse affichée 3 s et évitement de la répétition immédiate.

Le dépôt contient aussi 24 PNG pentatoniques produits par le renderer. Leur présence dans `images/Scales/` ne signifie pas que l'onglet Pentatoniques de la bibliothèque est déjà activé.

### 4.3.1 Palette transversale tonique / mode — accords + gammes

Référence fonctionnelle : `docs/chatgpt/PALETTE_TONALITES_ACCORDS_GAMMES_V1.md`.  
Source runtime canonique : `data/music-theory/tonality-colors.json`.

Règle : la **tonique** choisit la famille de couleur ; le **mode** choisit la variante. Un accord ou une gamme majeur(e) utilise la couleur **Majeur** correspondante, un accord ou une gamme mineur(e) utilise la couleur **Mineur** correspondante. La couleur **Base** est conservée comme identité neutre / réserve pour les usages futurs.

Les renderers d'accords et de gammes doivent consommer cette source et appliquer une couleur unique tonique/mode à toutes les touches actives, blanches ou noires. Aucune couleur fixe ne doit être choisie selon le type physique de touche. La hiérarchie commune est définie dans `docs/chatgpt/RENDERERS_SOURCE_OF_TRUTH_V1.md`; les tests de renderer doivent également dériver leurs couleurs attendues du JSON et ne pas figer de valeur hexadécimale active.

### 4.4 Théorie musicale

Flux :

```text
theory.html
→ js/theory_page.js
→ data/exercises/theorie.json
→ theory_quiz.html?mode=...
→ js/theory_quiz.js
→ data/music-theory/scales.json
```

Deux modes :

- `scale-quiz` : reconstruire depuis la fondamentale ;
- `scale-from-any-note` : reconstruire en commençant depuis une note quelconque de la gamme.

Le dataset de théorie contient 48 définitions :

- 12 ioniennes ;
- 12 éoliennes ;
- 12 pentatoniques majeures ;
- 12 pentatoniques mineures.

### 4.5 Basse et rythme

Flux :

```text
index.html
→ js/home.js
→ data/categories.json
→ category.html?category=basse|rythme
→ js/category_page.js
→ data/categories.json
→ exerciseFile
→ data/exercises/basse.json ou rythme.json
```

`js/category_page.js` ne recopie plus les titres/descriptions de Basse et Rythme : il relit la même entrée de `data/categories.json` que l'accueil.

Les exercices sont actuellement des cartes de consignes JSON, sans moteur d'exercice spécialisé.

---

## 5. Architecture CSS / design

Le projet a une identité visuelle cohérente autour de :

- rouge principal `#991F3D` ;
- rouge foncé `#78152F` ;
- fonds rosés ;
- police web Inter via Google Fonts ;
- responsive par media queries ;
- réduction d'animation via `prefers-reduced-motion` sur les vues principales.

Répartition :

- `css/styles.css` : accueil + paramétrage accords ;
- `css/second_page_styles.css` : entraînement accords ;
- `css/scales_styles.css` : paramétrage + entraînement gammes ;
- `css/scale_library.css` : bibliothèque visuelle des gammes ;
- `css/library_styles.css` : théorie + catégories basse/rythme.

**Dépendance externe observée :** Google Fonts pour Inter. Si le réseau bloque cette ressource, la pile système prend le relais.

---

## 6. Données et duplication

Les définitions musicales sont réparties dans plusieurs sources qui n'ont pas le même rôle.

### 6.1 `js/scales_script.js`

Rôle : mapping fonctionnel de l'entraînement visuel : libellé → PNG.

### 6.2 `js/scale_library.js`

Rôle : mapping d'affichage de la bibliothèque visuelle : libellé français → PNG.

### 6.3 `data/music-theory/scales.json`

Rôle : questions/réponses de théorie. Inclut ionien, éolien et pentatoniques.

### 6.4 `tools/piano_scale_renderer/scales.json`

Rôle : vérité opérationnelle du renderer d'images, avec séparation slot physique → libellé théorique. **Toujours lire cette copie GitHub ; ne pas reconstruire les gammes de mémoire.**

### 6.5 Notion

Rôle : spécification fonctionnelle du générateur de gammes.

### 6.6 Contrôle automatique de cohérence

`tests/test_scale_consistency.py` contrôle automatiquement la zone de recouvrement entre :

- `tools/piano_scale_renderer/scales.json` ;
- `js/scales_script.js` ;
- `js/scale_library.js` ;
- `data/music-theory/scales.json` ;
- les PNG attendus dans `images/Scales/`.

Le test vérifie notamment les 12 majeures + 12 mineures naturelles, l'unicité des mappings, les noms de fichiers, les libellés de la bibliothèque et la concordance des orthographes ioniennes/éoliennes avec le renderer.

La CI `.github/workflows/scale-consistency.yml` exécute ce test sur `master` et sur les pull requests quand l'une de ces sources change. Notion reste hors CI car il s'agit d'une spécification fonctionnelle externe, pas d'une source runtime.

**Règle : ne jamais modifier une source par analogie avec une autre. Identifier d'abord le domaine.**

---

## 7. Images de gammes — système canonique

### 7.1 Doctrine

Les images finales de gammes ne doivent **jamais** être créées par génération visuelle libre. Elles sont produites par compositing déterministe sur un template verrouillé.

**Emplacement canonique :** `AlexFCL/piano`, branche `master`, dossier `tools/piano_scale_renderer/`.

Contenu canonique :

- `tools/piano_scale_renderer/SOURCE_IMAGES_GAMMES_PIANO_V1.8.md` ;
- `tools/piano_scale_renderer/piano_scale_renderer.py` ;
- `tools/piano_scale_renderer/scales.json` ;
- `tools/piano_scale_renderer/official_template.png` ;
- `tools/piano_scale_renderer/test_renderer.py` ;
- `tools/piano_scale_renderer/requirements.txt` ;
- `data/music-theory/tonality-colors.json` ;
- `docs/chatgpt/PALETTE_TONALITES_ACCORDS_GAMMES_V1.md`.

Le dossier `golden/` contient des snapshots historiques et n'est pas une source colorimétrique canonique tant qu'il n'a pas été régénéré avec la palette actuelle.

Le ZIP `piano_corrector_v1(1).zip` devient un **backup historique**, pas la source principale. Une future conversation doit récupérer le moteur depuis GitHub.

### 7.2 Template canonique

- dimensions : **365 × 254 px** ;
- SHA-256 : `cbda5265b1be6893010e8da73e1b7ab0c25656984724687f2fd13f79f0fa41a9` ;
- `Template2(1).png` = `official_template.png` octet pour octet ;
- `Template(1).png` = 711 × 254 : ne pas l'utiliser comme template du renderer de gammes.

### 7.3 Palette du renderer de gammes

Le renderer de gammes consomme la palette tonique/mode canonique structurée dans `data/music-theory/tonality-colors.json`.

Règle verrouillée :
- la tonique choisit la famille ;
- un mode majeur utilise la variante `major` ;
- un mode mineur utilise la variante `minor` ;
- toutes les touches actives d'une même gamme utilisent la même couleur, qu'elles soient blanches ou noires ;
- les libellés restent blancs ;
- aucune couleur fixe ne doit dépendre du type physique de touche.

Référence fonctionnelle : `docs/chatgpt/PALETTE_TONALITES_ACCORDS_GAMMES_V1.md`.

### 7.4 Pipeline

1. vérifier le hash du template ;
2. détecter/verrouiller la géométrie ;
3. lire la définition de gamme et activer exactement 7 slots pour les gammes classiques ;
4. résoudre la couleur tonique/mode depuis `data/music-theory/tonality-colors.json` ;
5. remplir toutes les touches actives avec cette même couleur ;
6. restaurer les éléments structurels du template ;
7. valider les aplats avant texte ;
8. placer les labels avec Roboto Condensed Bold ;
9. valider le rendu final ;
10. écrire le PNG ;
11. produire un rapport.

### 7.5 Tests

Commande :

```bash
cd tools/piano_scale_renderer
python -m unittest -v test_renderer.py
```

Le nombre exact de tests ne doit pas être figé dans cette documentation. Exécuter la suite actuelle et vérifier qu'elle passe avant toute livraison.

Commande de génération complète :

```bash
cd tools/piano_scale_renderer
python piano_scale_renderer.py --all
```

### 7.6 Police

Le renderer dépend de **Roboto Condensed Bold**, non incluse dans l'archive. La documentation doit indiquer la dépendance mais ne doit pas redistribuer de fichier de police depuis ChatGPT.

---

## 8. État de cohérence connu

### 8.1 PNG GitHub vs renderer

Les anciennes comparaisons par blob SHA contre le renderer historique ou les snapshots `golden/` ne constituent plus une preuve de conformité colorimétrique depuis l'adoption de la palette tonique/mode.

Avant d'affirmer que les assets de `images/Scales/` sont synchronisés, il faut les régénérer avec le renderer courant, vérifier la palette tonique/mode, puis comparer explicitement les sorties attendues aux PNG live.

### 8.2 Convention enharmonique mineure — résolue

Décision du 28/09/2026 :

- entraînement visuel/renderer : **Eb mineur naturel** ;
- dataset théorie, mode éolien : **Eb éolien** ;
- notes attendues dans le quiz : **Eb, F, Gb, Ab, Bb, Cb, Db**.

La précédente entrée **D# éolien** a été remplacée afin d'aligner le quiz de théorie avec la convention pédagogique déjà utilisée par le renderer et l'entraînement visuel. Cette décision concerne l'éolien ; elle ne renomme pas automatiquement les autres familles de gammes enharmoniques.

### 8.3 Accords / renversement — résolu

Décision du 28/09/2026 : le renversement/fondamentale tiré est affiché dans la consigne. Les assets canoniques d'accords utilisent désormais un nommage descriptif PNG (`C-majeur-fond.png`, `C-mineur-1er.png`, etc.) généré par `tools/piano_chord_renderer/`. Les anciens JPG indexés peuvent rester comme legacy tant qu'aucun nettoyage explicite n'est décidé.

### 8.4 Catégories — résolu

Décision du 28/09/2026 :

- `data/categories.json` contient les métadonnées des 5 cartes d'accueil ;
- `js/home.js` génère l'accueil depuis ce fichier ;
- `js/category_page.js` réutilise ces métadonnées pour Basse et Rythme ;
- `tests/test_categories.py` vérifie l'ordre, les champs obligatoires, les routes et les fichiers d'exercices ;
- `.github/workflows/category-consistency.yml` exécute ce contrôle automatiquement.

La duplication des titres/descriptions/routes entre `index.html` et le JSON a donc été supprimée.

### 8.5 Fichiers legacy / rôle non prouvé

À conserver tant que leur rôle n'est pas explicitement établi :

- `second_page_backup.html` ;
- `Template.png` ;
- `Template.jpg` ;
- `Readme.txt` même s'il est vide ;
- anciens documents V1/V2/V3 hors contexte actif si archivés.

### 8.6 Tests applicatifs

Cinq ensembles de contrôles automatisés existent désormais :

- renderer de gammes : tests dédiés au rendu déterministe, à la géométrie et à la palette tonique/mode ;
- renderer d'accords : tests couvrant les 102 combinaisons, la palette tonique/mode, les trois positions de Do majeur et les orthographes enharmoniques ;
- cohérence applicative des gammes : 5 tests dans `tests/test_scale_consistency.py`, exécutés par GitHub Actions ;
- cohérence des catégories : tests dans `tests/test_categories.py`, exécutés par GitHub Actions ;
- politique de source de palette : `tests/test_renderer_palette_source.py`, exécuté par `.github/workflows/renderer-palette-source.yml`.

Ces contrôles ne remplacent pas une recette navigateur : aucune suite E2E/UI automatisée n'est actuellement documentée.

---

## 8.7 Bootstrap obligatoire pour une future conversation

Si une future conversation reçoit une demande telle que « génère une gamme », « corrige une image de gamme » ou « ajoute un PNG de gamme » :

1. ouvrir `CHATGPT_PROJECT_POINTER.md` si disponible ;
2. résoudre `AlexFCL/piano` / `master` ;
3. récupérer **sans improvisation** `tools/piano_scale_renderer/` ;
4. exécuter les tests du renderer avant livraison ;
5. utiliser exclusivement la sortie du renderer ;
6. ne jamais utiliser `image_gen` ou un dessin manuel pour l’asset final.

Cette règle prévaut sur tout souvenir de conversation.

---

## 9. Priorité en cas de contradiction

1. **État courant du code** → GitHub live.
2. **Règles de rendu des PNG** → palette `docs/chatgpt/PALETTE_TONALITES_ACCORDS_GAMMES_V1.md` + source runtime `data/music-theory/tonality-colors.json` + renderer/tests.
3. **Intention fonctionnelle** → spécification Notion la plus récente.
4. **Architecture / méthode de travail** → V4.
5. **Historique** → V1/V2/V3.

Une source plus récente ne peut remplacer une source d'un autre type que si son périmètre le couvre explicitement.

---

## 10. Processus obligatoire pour les futures demandes

### 10.1 Question sur l'état actuel

- vérifier GitHub ;
- répondre depuis les fichiers réels ;
- utiliser V4 comme carte, pas comme preuve de l'état live.

### 10.2 Modification GitHub

1. vérifier `AlexFCL/piano` / `master` et relever le HEAD ;
2. travailler en lecture seule pendant l'audit et la préparation ;
3. préparer toutes les modifications du lot avant publication ;
4. si l'utilisateur souhaite contrôler la publication, attendre son « GO push » ;
5. créer les blobs et un arbre Git unique ;
6. créer **un seul commit** pour la tâche ;
7. revérifier que le HEAD de `master` est toujours celui relevé au départ ;
8. déplacer `master` une seule fois, sans force ;
9. vérifier les workflows réellement déclenchés ;
10. mettre à jour la documentation si l'architecture ou le contrat change.

Éviter une série de `update_file` sur `master` : chaque commit intermédiaire peut déclencher GitHub Pages et les CI.

### 10.3 Nouvelle image de gamme / correction

1. ne pas utiliser de modèle d'image ;
2. récupérer `tools/piano_scale_renderer/` depuis GitHub ;
3. lire d'abord `data/music-theory/tonality-colors.json`, puis `RENDERERS_SOURCE_OF_TRUTH_V1.md`, `README.md`, la V1.8 et vérifier la définition dans `scales.json` ;
4. générer ;
5. lancer les tests ;
6. lire `validation-report.json` ;
7. comparer au fichier GitHub si remplacement ;
8. seulement ensuite importer l'asset.

### 10.4 Suppression / nettoyage

Avant de dire « supprime » :

1. inspecter ;
2. classer ;
3. chercher les dépendants ;
4. identifier un remplaçant ;
5. faire/valider un backup ;
6. produire une recommandation réversible ;
7. privilégier `ARCHIVER` si le gain de suppression est faible.

---

## 11. Mise à jour de la documentation

Mettre à jour V4 quand l'un de ces éléments change :

- structure du dépôt ;
- ajout/suppression d'un domaine fonctionnel ;
- source de vérité ;
- format/nombre des assets ;
- fonctionnement des générateurs ;
- conventions de fichiers ;
- renderer/template/tests ;
- mode d'hébergement ;
- dépendance externe ;
- décision de résoudre une incohérence documentée.

Une simple modification cosmétique locale n'impose pas forcément de réécrire V4, sauf si elle change une règle réutilisable.

---

## 12. Résumé de référence

> **Application piano = GitHub `AlexFCL/piano`, branche `master`, application statique HTML/CSS/JS.**

> **Le code GitHub donne l'état réel. La V4 donne la carte et la méthode.**

> **Renderer canonique des gammes : `AlexFCL/piano` / `master` / `tools/piano_scale_renderer/`. Toujours l’utiliser pour générer ou corriger un PNG ; jamais de génération d’image libre.**

> **Le ZIP historique reste un backup de récupération, mais GitHub est désormais la source canonique du moteur, du template et des tests.**

> **Aucune suppression sans inventaire, dépendances, remplaçant et backup.**
