\
# APPLICATION PIANO — SOURCE MAÎTRE V4

**Projet :** Application piano  
**Statut :** source maître consolidée  
**Date de consolidation :** 23/09/2026  
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
| Images de gammes | `SOURCE_IMAGES_GAMMES_PIANO_V1.7.md` + `piano_corrector_v1.zip` | Doctrine + outil exécutable |
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
- **HEAD vérifié lors de cette consolidation :** `265115ed7c480aa2057bb703e6e6503ca9f3f4df`
- **Dernier commit observé :** `Match image exercise cards to theory quiz` du 22/09/2026

Le HEAD doit toujours être revérifié avant une écriture future.

### 2.2 Ce projet n'est pas le projet « Les perms de l'Intervalle »

`AlexFCL/perms-basse` est un autre projet. Ne jamais importer automatiquement dans Application piano :

- la branche `main` ;
- Next.js ;
- Vercel ;
- Cloudflare R2 ;
- Auth0 ;
- les conventions de déploiement de `perms-basse`.

### 2.3 Hébergement

GitHub Pages est activé au niveau du dépôt. Le **mode exact de publication** (branche/dossier de source et URL de publication) n'a pas été vérifié via l'endpoint Pages pendant cette consolidation. Ne pas l'inventer.

---

## 3. Architecture actuelle du dépôt

### 3.1 Vue d'ensemble vérifiée

Le dépôt contient actuellement :

- 9 pages HTML ;
- 4 fichiers CSS ;
- 7 scripts JavaScript ;
- 5 fichiers JSON de données ;
- 102 images d'accords ;
- 24 images de gammes ;
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
├── theory.html
├── theory_quiz.html
├── category.html
├── Template.png
├── Template.jpg
├── Readme.txt
├── css/
│   ├── styles.css
│   ├── second_page_styles.css
│   ├── scales_styles.css
│   └── library_styles.css
├── js/
│   ├── main.js
│   ├── second_page_script.js
│   ├── scales_main.js
│   ├── scales_script.js
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
│       └── scales.json
└── images/
    ├── Chords/   # 102 JPG
    └── Scales/   # 24 PNG
```

---

## 4. Parcours applicatifs

### 4.1 Accueil

**Entrée :** `index.html`

L'accueil affiche cinq cartes codées directement dans le HTML :

1. Accords
2. Gammes
3. Théorie musicale
4. Rythme
5. Basse

`data/categories.json` existe, mais **n'alimente pas actuellement la page d'accueil**.

### 4.2 Accords

Flux :

```text
chords.html
→ js/main.js
→ second_page.html?updateTime=X
→ js/second_page_script.js
→ images/Chords/*.jpg
```

Comportement observé :

- `updateTime` doit être ≥ 1 seconde ;
- une note est tirée parmi 17 graphies ;
- majeur/mineur est tiré ;
- une position/fondamentale-renversement est tirée ;
- le nom de l'image est calculé par index `note-type-position.jpg` ;
- 102 images correspondent à `17 × 2 × 3` combinaisons ;
- un nouveau tirage est fait toutes les `updateTime` secondes.

**Point à surveiller :** la troisième valeur (fondamentale / 1er / 2e renversement) influence l'image, mais n'est pas affichée dans le texte de la question dans le code actuel. L'intention fonctionnelle n'est pas déterminable à partir du code seul. Ne pas modifier sans décision explicite.

### 4.3 Gammes — entraînement visuel

Flux :

```text
scales.html
→ js/scales_main.js
→ scale_training.html?updateTime=X
→ js/scales_script.js
→ images/Scales/*.png
```

Comportement observé :

1. `updateTime` doit être ≥ 1 seconde ;
2. une gamme est tirée parmi 24 entrées ;
3. le nom est affiché immédiatement ;
4. l'image est cachée pendant `updateTime` ;
5. l'image est révélée pendant 3 secondes ;
6. une nouvelle gamme est tirée ;
7. le même index n'est pas proposé deux fois de suite ;
8. l'image est préchargée avant révélation ;
9. si `updateTime` est absent/invalide dans l'URL, la valeur de repli est 5 s.

Pool : 12 majeures + 12 mineures naturelles.

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
→ category.html?category=basse|rythme
→ js/category_page.js
→ data/exercises/basse.json ou rythme.json
```

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
- `css/library_styles.css` : théorie + catégories basse/rythme.

**Dépendance externe observée :** Google Fonts pour Inter. Si le réseau bloque cette ressource, la pile système prend le relais.

---

## 6. Données et duplication

Les définitions musicales sont réparties dans plusieurs sources qui n'ont pas le même rôle.

### 6.1 `js/scales_script.js`

Rôle : mapping fonctionnel de l'entraînement visuel : libellé → PNG.

### 6.2 `data/music-theory/scales.json`

Rôle : questions/réponses de théorie. Inclut ionien, éolien et pentatoniques.

### 6.3 `piano_corrector/scales.json`

Rôle : vérité opérationnelle du renderer d'images, avec séparation slot physique → libellé théorique.

### 6.4 Notion

Rôle : spécification fonctionnelle du générateur de gammes.

**Règle : ne jamais modifier une source par analogie avec une autre. Identifier d'abord le domaine.**

---

## 7. Images de gammes — système canonique

### 7.1 Doctrine

Les images finales de gammes ne doivent **jamais** être créées par génération visuelle libre. Elles sont produites par compositing déterministe sur un template verrouillé.

Sources :

- `SOURCE_IMAGES_GAMMES_PIANO_V1.7.md` ;
- `piano_corrector_v1.zip` ;
- `piano_scale_renderer.py` ;
- `scales.json` ;
- `official_template.png` ;
- `test_renderer.py` ;
- golden images C majeur et E majeur.

### 7.2 Template canonique

- dimensions : **365 × 254 px** ;
- SHA-256 : `cbda5265b1be6893010e8da73e1b7ab0c25656984724687f2fd13f79f0fa41a9` ;
- `Template2(1).png` = `official_template.png` octet pour octet ;
- `Template(1).png` = 711 × 254 : ne pas l'utiliser comme template du renderer de gammes.

### 7.3 Palette canonique

- blanc actif : rouge `#C53650` ;
- noir actif : orange `#F68C1F` ;
- texte : blanc ;
- structure : template original.

### 7.4 Pipeline

1. vérifier le hash du template ;
2. détecter/verrouiller la géométrie ;
3. activer exactement 7 slots ;
4. remplir les touches blanches actives sur le masque complet ;
5. restaurer les touches noires du template ;
6. remplir les touches noires actives ;
7. valider les aplats avant texte ;
8. placer les labels avec Roboto Condensed Bold ;
9. valider le rendu final ;
10. écrire le PNG ;
11. produire un rapport.

### 7.5 Tests

Commande :

```bash
python -m unittest -v test_renderer.py
```

Vérification relancée le 23/09/2026 : **8/8 tests OK**.

Commande de génération complète :

```bash
python piano_scale_renderer.py --all
```

### 7.6 Police

Le renderer dépend de **Roboto Condensed Bold**, non incluse dans l'archive. La documentation doit indiquer la dépendance mais ne doit pas redistribuer de fichier de police depuis ChatGPT.

---

## 8. État de cohérence connu

### 8.1 PNG GitHub vs renderer

Comparaison par Git blob SHA : **20/24 images GitHub correspondent exactement aux sorties du renderer fourni**.

Divergences actuelles :

- `D-majeur.png` ;
- `E-majeur.png` ;
- `Eb-majeur.png` ;
- `F-majeur.png`.

Ne pas remplacer automatiquement ces quatre fichiers sans demande explicite. Mais ne jamais dire que les 24 assets sont synchronisés tant que cet écart existe.

### 8.2 `Eb mineur` vs `D# éolien`

- entraînement visuel/renderer : **Eb mineur naturel** ;
- dataset théorie : **D# éolien**.

Les deux représentent la même classe de hauteur mais une orthographe théorique différente. **Aucune harmonisation automatique.**

### 8.3 Catégories

`data/categories.json` existe mais l'accueil est hardcodé dans `index.html`.

### 8.4 Fichiers legacy / rôle non prouvé

À conserver tant que leur rôle n'est pas explicitement établi :

- `second_page_backup.html` ;
- `Template.png` ;
- `Template.jpg` ;
- `Readme.txt` même s'il est vide ;
- anciens documents V1/V2/V3 hors contexte actif si archivés.

### 8.5 Tests applicatifs

Aucune suite de tests automatisés de l'application web n'a été observée dans le dépôt actuel. Les tests automatisés existants concernent le renderer de gammes.

---

## 9. Priorité en cas de contradiction

1. **État courant du code** → GitHub live.
2. **Règles de rendu des PNG** → V1.7 + renderer/tests.
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

1. vérifier `AlexFCL/piano` ;
2. vérifier `master` ;
3. relever le HEAD ;
4. lire les fichiers exacts ;
5. modifier uniquement ce qui est nécessaire ;
6. vérifier les impacts ;
7. créer le commit ;
8. confirmer le SHA du commit ;
9. mettre à jour la documentation si l'architecture ou le contrat change.

### 10.3 Nouvelle image de gamme / correction

1. ne pas utiliser de modèle d'image ;
2. ouvrir le correcteur ;
3. vérifier la définition dans `scales.json` ;
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

> **Les images de gammes dépendent de V1.7 + `piano_corrector_v1.zip` + template canonique 365×254. Le ZIP est une dépendance opérationnelle, pas une archive jetable.**

> **Aucune suppression sans inventaire, dépendances, remplaçant et backup.**