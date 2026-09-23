# APPLICATION PIANO â€” SOURCE MAÃTRE V4

**Projet :** Application piano  
**Statut :** source maÃ®tre consolidÃ©e  
**Date de consolidation :** 23/09/2026 â€” rÃ©vision aprÃ¨s publication du renderer dans GitHub  
**But :** permettre Ã  ChatGPT et au propriÃ©taire du projet de comprendre, modifier et maintenir le projet sans perdre de dÃ©pendance importante ni confondre les sources.

---

## 0. RÃ¨gles de sÃ©curitÃ© documentaire

Ces rÃ¨gles s'appliquent avant toute autre rÃ¨gle du projet.

1. **Ne jamais recommander la suppression d'un fichier ou d'une source sans en avoir inspectÃ© le contenu et les dÃ©pendances.**
2. **Ne jamais considÃ©rer â€œancienâ€, â€œV1â€, â€œV2â€, â€œbackupâ€, â€œzipâ€, â€œtemplateâ€ ou â€œarchiveâ€ comme synonyme de supprimable.**
3. Avant toute suppression ou retrait d'une source active :
   - identifier son rÃ´le ;
   - identifier ce qui en dÃ©pend ;
   - identifier son remplaÃ§ant exact ;
   - vÃ©rifier que le remplaÃ§ant couvre rÃ©ellement toutes ses fonctions ;
   - vÃ©rifier qu'une sauvegarde indÃ©pendante existe.
4. **En cas de doute : conserver.**
5. Une nouvelle documentation peut supersÃ©der une ancienne documentation, mais elle **ne remplace jamais automatiquement** un script, un asset, un template, un test ou un historique.
6. Toute opÃ©ration destructive doit Ãªtre prÃ©cÃ©dÃ©e d'un inventaire explicite `Ã©lÃ©ment â†’ rÃ´le â†’ dÃ©pendants â†’ remplaÃ§ant â†’ sauvegarde â†’ dÃ©cision`.

---

## 1. Source de vÃ©ritÃ© par domaine

Il n'existe pas une source unique pour tout. Utiliser la source adaptÃ©e au sujet.

| Domaine | Source prioritaire | RÃ¨gle |
|---|---|---|
| Ã‰tat actuel du site | GitHub `AlexFCL/piano`, branche `master` | Toujours relire avant une modification |
| Architecture globale | Ce document V4 | Sert de carte du projet |
| Routage rapide ChatGPT | `PLAYBOOK_CHATGPT_APPLICATION_PIANO_V4.md` | Ã€ lire en premier dans une future demande |
| DÃ©pendances / conservation | `MANIFEST_APPLICATION_PIANO_V4.md` | DÃ©cide ce qui doit Ãªtre conservÃ© |
| Images de gammes | GitHub `tools/piano_scale_renderer/` | **Source canonique exÃ©cutable** : doctrine + renderer + template + tests |
| SpÃ©cification fonctionnelle du gÃ©nÃ©rateur de gammes | Notion `SpÃ©cifications â€“ GÃ©nÃ©rateur de gammes piano` | Intention fonctionnelle ; le code GitHub prÃ©vaut pour l'Ã©tat rÃ©el |
| Anciennes dÃ©cisions/documentations | Archives V1/V2/V3 | Historique seulement |

---

## 2. IdentitÃ© et infrastructure

### 2.1 DÃ©pÃ´t canonique

- **GitHub :** `AlexFCL/piano`
- **Branche par dÃ©faut :** `master`
- **VisibilitÃ© :** publique
- **Stack :** HTML / CSS / JavaScript statique
- **Framework :** aucun framework applicatif observÃ©
- **GitHub Pages :** le dÃ©pÃ´t signale `has_pages: true`
- **Renderer canonique :** `tools/piano_scale_renderer/`
- **Documentation ChatGPT versionnÃ©e :** `docs/chatgpt/`
- **Pointeur de dÃ©marrage :** `CHATGPT_PROJECT_POINTER.md`

Le HEAD doit toujours Ãªtre revÃ©rifiÃ© avant une Ã©criture future ; ne jamais figer un SHA comme Ã©tat courant dans la documentation.

### 2.2 Ce projet n'est pas le projet Â« Les perms de l'Intervalle Â»

`AlexFCL/perms-basse` est un autre projet. Ne jamais importer automatiquement dans Application piano :

- la branche `main` ;
- Next.js ;
- Vercel ;
- Cloudflare R2 ;
- Auth0 ;
- les conventions de dÃ©ploiement de `perms-basse`.

### 2.3 HÃ©bergement

GitHub Pages est activÃ© au niveau du dÃ©pÃ´t. Le **mode exact de publication** (branche/dossier de source et URL de publication) n'a pas Ã©tÃ© vÃ©rifiÃ© via l'endpoint Pages pendant cette consolidation. Ne pas l'inventer.

---

## 3. Architecture actuelle du dÃ©pÃ´t

### 3.1 Vue d'ensemble vÃ©rifiÃ©e

Le dÃ©pÃ´t contient actuellement :

- 9 pages HTML ;
- 4 fichiers CSS ;
- 7 scripts JavaScript ;
- 5 fichiers JSON de donnÃ©es ;
- 102 images d'accords ;
- 24 images de gammes ;
- des assets/template historiques Ã  la racine.

### 3.2 Arborescence logique

```text
AlexFCL/piano (master)
â”œâ”€â”€ index.html
â”œâ”€â”€ chords.html
â”œâ”€â”€ second_page.html
â”œâ”€â”€ second_page_backup.html
â”œâ”€â”€ scales.html
â”œâ”€â”€ scale_training.html
â”œâ”€â”€ theory.html
â”œâ”€â”€ theory_quiz.html
â”œâ”€â”€ category.html
â”œâ”€â”€ Template.png
â”œâ”€â”€ Template.jpg
â”œâ”€â”€ Readme.txt
â”œâ”€â”€ CHATGPT_PROJECT_POINTER.md
â”œâ”€â”€ tools/
â”‚   â””â”€â”€ piano_scale_renderer/
â”‚       â”œâ”€â”€ README.md
â”‚       â”œâ”€â”€ SOURCE_IMAGES_GAMMES_PIANO_V1.7.md
â”‚       â”œâ”€â”€ piano_scale_renderer.py
â”‚       â”œâ”€â”€ requirements.txt
â”‚       â”œâ”€â”€ scales.json
â”‚       â”œâ”€â”€ official_template.png
â”‚       â”œâ”€â”€ test_renderer.py
â”‚       â””â”€â”€ golden/
â”‚           â”œâ”€â”€ C-majeur.png
â”‚           â””â”€â”€ E-majeur.png
â”œâ”€â”€ docs/
â”‚   â””â”€â”€ chatgpt/
â”‚       â”œâ”€â”€ APPLICATION_PIANO_MASTER_V4.md
â”‚       â”œâ”€â”€ MANIFEST_APPLICATION_PIANO_V4.md
â”‚       â”œâ”€â”€ PLAYBOOK_CHATGPT_APPLICATION_PIANO_V4.md
â”‚       â”œâ”€â”€ ETAT_CONNU_DETTE_TECHNIQUE_APPLICATION_PIANO_V4.md
â”‚       â””â”€â”€ INSTRUCTIONS_MISE_A_JOUR_APPLICATION_PIANO_V4.md
â”œâ”€â”€ css/
â”‚   â”œâ”€â”€ styles.css
â”‚   â”œâ”€â”€ second_page_styles.css
â”‚   â”œâ”€â”€ scales_styles.css
â”‚   â””â”€â”€ library_styles.css
â”œâ”€â”€ js/
â”‚   â”œâ”€â”€ main.js
â”‚   â”œâ”€â”€ second_page_script.js
â”‚   â”œâ”€â”€ scales_main.js
â”‚   â”œâ”€â”€ scales_script.js
â”‚   â”œâ”€â”€ theory_page.js
â”‚   â”œâ”€â”€ theory_quiz.js
â”‚   â””â”€â”€ category_page.js
â”œâ”€â”€ data/
â”‚   â”œâ”€â”€ categories.json
â”‚   â”œâ”€â”€ exercises/
â”‚   â”‚   â”œâ”€â”€ basse.json
â”‚   â”‚   â”œâ”€â”€ rythme.json
â”‚   â”‚   â””â”€â”€ theorie.json
â”‚   â””â”€â”€ music-theory/
â”‚       â””â”€â”€ scales.json
â””â”€â”€ images/
    â”œâ”€â”€ Chords/   # 102 JPG
    â””â”€â”€ Scales/   # 24 PNG
```

---

## 4. Parcours applicatifs

### 4.1 Accueil

**EntrÃ©e :** `index.html`

L'accueil affiche cinq cartes codÃ©es directement dans le HTML :

1. Accords
2. Gammes
3. ThÃ©orie musicale
4. Rythme
5. Basse

`data/categories.json` existe, mais **n'alimente pas actuellement la page d'accueil**.

### 4.2 Accords

Flux :

```text
chords.html
â†’ js/main.js
â†’ second_page.html?updateTime=X
â†’ js/second_page_script.js
â†’ images/Chords/*.jpg
```

Comportement observÃ© :

- `updateTime` doit Ãªtre â‰¥ 1 seconde ;
- une note est tirÃ©e parmi 17 graphies ;
- majeur/mineur est tirÃ© ;
- une position/fondamentale-renversement est tirÃ©e ;
- le nom de l'image est calculÃ© par index `note-type-position.jpg` ;
- 102 images correspondent Ã  `17 Ã— 2 Ã— 3` combinaisons ;
- un nouveau tirage est fait toutes les `updateTime` secondes.

**Point Ã  surveiller :** la troisiÃ¨me valeur (fondamentale / 1er / 2e renversement) influence l'image, mais n'est pas affichÃ©e dans le texte de la question dans le code actuel. L'intention fonctionnelle n'est pas dÃ©terminable Ã  partir du code seul. Ne pas modifier sans dÃ©cision explicite.

### 4.3 Gammes â€” entraÃ®nement visuel

Flux :

```text
scales.html
â†’ js/scales_main.js
â†’ scale_training.html?updateTime=X
â†’ js/scales_script.js
â†’ images/Scales/*.png
```

Comportement observÃ© :

1. `updateTime` doit Ãªtre â‰¥ 1 seconde ;
2. une gamme est tirÃ©e parmi 24 entrÃ©es ;
3. le nom est affichÃ© immÃ©diatement ;
4. l'image est cachÃ©e pendant `updateTime` ;
5. l'image est rÃ©vÃ©lÃ©e pendant 3 secondes ;
6. une nouvelle gamme est tirÃ©e ;
7. le mÃªme index n'est pas proposÃ© deux fois de suite ;
8. l'image est prÃ©chargÃ©e avant rÃ©vÃ©lation ;
9. si `updateTime` est absent/invalide dans l'URL, la valeur de repli est 5 s.

Pool : 12 majeures + 12 mineures naturelles.

### 4.4 ThÃ©orie musicale

Flux :

```text
theory.html
â†’ js/theory_page.js
â†’ data/exercises/theorie.json
â†’ theory_quiz.html?mode=...
â†’ js/theory_quiz.js
â†’ data/music-theory/scales.json
```

Deux modes :

- `scale-quiz` : reconstruire depuis la fondamentale ;
- `scale-from-any-note` : reconstruire en commenÃ§ant depuis une note quelsonque de la gamme.

Le dataset de thÃ©orie contient 48 dÃ©finitions :

- 12 ioniennes ;
- 12 Ã©oliennes ;
- 12 pentatoniques majeures ;
- 12 pentatoniques mineures.

### 4.5 Basse et rythme

Flux :

```text
index.html
â†’ category.html?category=basse|rythme
â†’ js/category_page.js
â†’ data/exercises/basse.json ou rythme.json
```

Les exercices sont actuellement des cartes de consignes JSON, sans moteur d'exercice spÃ©cialisÃ©.

---

## 5. Architecture CSS / design

Le projet a une identitÃ© visuelle cohÃ©rente autour de :

- rouge principal `#991F3D` ;
- rouge foncÃ© `#78152F` ;
- fonds rosÃ©s ;
- police web Inter via Google Fonts ;
- responsive par media queries ;
- rÃ©duction d'animation via `prefers-reduced-motion` sur les vues principales.

RÃ©partition :

- `css/styles.css` : accueil + paramÃ©trage accords ;
- `css/second_page_styles.css` : entraÃ®nement accords ;
- `css/scales_styles.css` : paramÃ©trage + entraÃ®nement gammes ;
- `css/library_styles.css` : thÃ©orie + catÃ©gories basse/rythme.

**DÃ©pendance externe observÃ©e :** Google Fonts pour Inter. Si le rÃ©seau bloque cette ressource, la pile systÃ¨me prend le relais.

---

## 6. DonnÃ©es et duplication

Les dÃ©finitions musicales sont rÃ©parties dans plusieurs sources qui n'ont pas le mÃªme rÃ´le.

### 6.1 `js/scales_script.js`

RÃ´le : mapping fonctionnel de l'entraÃ®nement visuel : libellÃ© â†’ PNG.

### 6.2 `data/music-theory/scales.json`

RÃ´le : questions/rÃ©ponses de thÃ©orie. Inclut ionien, Ã©olien et pentatoniques.

## 6.3 `tools/piano_scale_renderer/scales.json`

RÃ´le : vÃ©ritÃ© opÃ©rationnelle du renderer d'images, avec sÃ©paration slot physique â†’ libellÃ© thÃ©orique. **Toujours lire cette copie GitHub ; ne pas reconstruire les gammes de mÃ©moire.**

### 6.4 Notion

RÃ´le : spÃ©cification fonctionnelle du gÃ©nÃ©rateur de gammes.

**RÃ¨gle : ne jamais modifier une source par analogie avec une autre. Identifier d'abord le domaine.**

---

## 7. Images de gammes â€” systÃ¨me canonique

### 7.1 Doctrine

Les images finales de gammes ne doivent **jamais** Ãªtre crÃ©Ã©es par gÃ©nÃ©ration visuelle libre. Elles sont produites par compositing dÃ©terministe sur un template verrouillÃ©.

**Emplacement canonique :** `AlexFCL/piano`, branche `master`, dossier `tools/piano_scale_renderer/`.

Contenu canonique :

- `tools/piano_scale_renderer/SOURCE_IMAGES_GAMMES_PIANO_V1.7.md` ;
- `tools/piano_scale_renderer/piano_scale_renderer.py` ;
- `tools/piano_scale_renderer/scales.json` ;
- `tools/piano_scale_renderer/official_template.png` ;
- `tools/piano_scale_renderer/test_renderer.py` ;
- `tools/piano_scale_renderer/requirements.txt` ;
- `tools/piano_scale_renderer/golden/C-majeur.png` ;
- `tools/piano_scale_renderer/golden/E-majeur.png`.

Le ZIP `piano_corrector_v1(1).zip` devient un **backup historique**, pas la source principale. Une future conversation doit rÃ©cupÃ©rer le moteur depuis GitHub.

### 7.2 Template canonique

- dimensions : **365 Ã— 254 px** ;
- SHA-256 : `cbda5265b1be6893010e8da73e1b7ab0c25656984724687f2fd13f79f0fa41a9` ;
- `Template2(1).png` = `official_template.png` octet pour octet ;
- `Template(1).png` = 711 Ã— 254 : ne pas l'utiliser comme template du renderer de gammes.

### 7.3 Palette canonique

- blanc actif : rouge `#C53650` ;
- noir actif : orange `#F68C1F` ;
- texte : blanc ;
- structure : template original.

### 7.4 Pipeline

1. vÃ©rifier le hash du template ;
2. dÃ©tecter/verrouiller la gÃ©omÃ©trie ;
3. activer exactement 7 slots ;
4. remplir les touches blanches actives sur le masque complet ;
5. restaurer les touches noires du template ;
6. remplir les touches noires actives ;
7. valider les aplats avant texte ;
8. placer les labels avec Roboto Condensed Bold ;
9. valider le rendu final ;
10. Ã©crire le PNG ;
11. produire un rapport.

### 7.5 Tests

Commande :

```bash
cd tools/piano_scale_renderer
python -m unittest -v test_renderer.py
```

Ã©rification relancÃ©e le 23/09/2026 : **8/8 tests OK**.

Commande de gÃ©nÃ©ration complÃ¨te :

```bash
cd tools/piano_scale_renderer
python piano_scale_renderer.py --all
```

### 7.6 Police

Le renderer dÃ©pend de **Roboto Condensed Bold**, non incluse dans l'archive. La documentation doit indiquer la dÃ©pendance mais ne doit pas redistribuer de fichier de police depuis ChatGPT.

---

## 8. Ã‰tat de cohÃ©rence connu

### 8.1 PNG GitHub vs renderer

Comparaison par Git blob SHA : **20/24 images GitHub correspondent exactement aux sorties du renderer fourni**.

Divergences actuelles :

- `D-majeur.png` ;
- `E-majeur.png` ;
- `Eb-majeur.png` ;
- `F-majeur.png`.

Ne pas remplacer automatiquement ces quatre fichiers sans demande explicite. Mais ne jamais dire que les 24 assets sont synchronisÃ©s tant que cet Ã©cart existe.

### 8.2 `Eb mineur` vs `D# Ã©olien`

- entraÃ®nement visuel/renderer : **Eb mineur naturel** ;
- dataset thÃ©orie : **D# Ã©olien**.

Les deux reprÃ©sentent la mÃªme classe de hauteur mais une orthographe thÃ©orique diffÃ©rente. **Aucune harmonisation automatique.**

### 8.3 CatÃ©gories

`data/categories.json` existe mais l'accueil est hardcodÃ© dans `index.html`.

### 8.4 Fichiers legacy / rÃ´le non prouvÃ©

@Ã  conserver tant que leur rÃ´le n'est pas explicitement Ã©tabli :

- `second_page_backup.html` ;
- `Template.png` ;
- `Template.jpg` ;
- `Readme.txt` mÃªme s'il est vide ;
- anciens documents V1/V2/V3 hors contexte actif si archivÃ©s.

### 8.5 Tests applicatifs

Aucune suite de tests automatisÃ©s de l'application web n'a Ã©tÃ© observÃ©e dans le dÃ©pÃ´t actuel. Les tests automatisÃ©s existants concernent le renderer de gammes.

---

## 8.6 Bootstrap obligatoire pour une future conversation

Si une future conversation reÃ§oit une demande telle que Â» gÃ©nÃ©re une gamme Â», Â« corrige une image de gamme Â¹ ou Â« ajoute un PNG de gamme Â» :

1. ouvrir `CHATGPT_PROJECT_POINTER.md` si disponible ;
2. rÃ©soudre `AlexFCL/piano` / `master` ;
3. rÃ©cupÃ©rer **sans improvisation** `tools/piano_scale_renderer/` ;
4. exÃ©cuter les tests du renderer avant livraison ;
5. utiliser exclusivement la sortie du renderer ;
6. ne jamais utiliser `image_gen` ou un dessin manuel pour lâ€™asset final.

Cette rÃ¨gle prÃ©vaut sur tout souvenir de conversation.

---

## 9. PrioritÃ© en cas de contradiction

1. **Ã‰tat courant du code** â†’ GitHub live.
2. **RÃ¨gles de rendu des PNG** â†’ V1.7 + renderer/tests.
3. **Intention fonctionnelle** â†’ spÃ©cification Notion la plus rÃ©cente.
4. **Architecture / mÃ©thode de travail** â†’ V4.
5. **Historique** â†’ V1/V2/V3.

Une source plus rÃ©cente ne peut remplacer une source d'un autre type que si son péê\š[pê™HHÛİ]œ™H^XÚ][Y[‚‚‹KKB‚ˆÈÈLˆ›ØÙ\Üİ\ÈØ›YØ]Ú\™Hİ\ˆ\È]\™\È[X[™\Â‚ˆÈÈÈLŒH]Y\İ[Ûˆİ\ˆ	ğê]]XİY[‚‹H°ê\šYšY\ˆÚ]XˆÂ‹H°ê\Û™™H\Z\È\ÈšXÚY\œÈ°êY[ÈÂ‹H][\Ù\ˆÛÛ[YHØ\K\ÈÛÛ[YH™]]™HH	ğê]]]™K‚‚ˆÈÈÈLŒˆ[ÙYšXØ][ÛˆÚ]X‚‚ŒKˆ°ê\šYšY\ˆ[^ÓÜX[›ØÂŒ‹ˆ°ê\šYšY\ˆX\İ\˜ÂŒËˆ™[]™\ˆHPQÂˆ\™H\ÈšXÚY\œÈ^XİÈÂKˆ[ÙYšY\ˆ[š\]Y[Y[ÙH]ZH\İ°êXÙ\ÜØZ\™HÂ‹ˆ°ê\šYšY\ˆ\È[\XİÈÂËˆÜ°êY\ˆHÛÛ[Z]ÂˆÛÛ™š\›Y\ˆHÒHHÛÛ[Z]ÂKˆY]™H0è›İ\ˆHØİ[Y[][ÛˆÚH	Ø\˜Ú]Xİ\™HİHHÛÛ˜]Ú[™ÙK‚‚ˆÈÈÈLŒÈ›İ]™[H[XYÙHHØ[[YHÈÛÜœ™Xİ[Û‚‚ŒKˆ™H\È][\Ù\ˆH[Ù0êH	Ú[XYÙHÂŒ‹ˆ°êXİ\0ê\™\ˆÛÛËÜX[›×ÜØØ[WÜ™[™\™\‹Ø\Z\ÈÚ]XˆÂŒËˆ\™H‘PQQK›YHŒKÈ]°ê\šYšY\ˆH0êYš[š][Ûˆ[œÈØØ[\ËšœÛÛ˜Âˆğê[°ê\™\ˆÂKˆ[˜Ù\ˆ\È\İÈÂ‹ˆ\™H˜[Y][Û‹\™\ÜšœÛÛ˜ÂËˆÛÛ\\™\ˆ]HšXÚY\ˆÚ]XˆÚH™[\XÙ[Y[ÂˆÙ][[Y[[œİZ]H[\Ü\ˆ	Ø\ÜÙ]‚‚ˆÈÈÈLİ\™\ÜÚ[ÛˆÈ™]ŞXYÙB‚]˜[H\™H0ªÈİ\š[YH0®È‚‚ŒKˆ[œÜXİ\ˆÂŒ‹ˆÛ\ÜÙ\ˆÂŒËˆÚ\˜Ú\ˆ\È0ê\[™[ÈÂˆY[YšY\ˆ[ˆ™[\péØ[ÂKˆ˜Z\™Kİ˜[Y\ˆ[ˆ˜XÚİ\Â‹ˆ›ÙZ\™H[™H™XÛÛ[X[™][Ûˆ°ê]™\œÚX›HÂËˆš]š[0êYÚY\ˆTÒU‘T˜ÚHHØZ[ˆHİ\™\ÜÚ[Ûˆ\İ˜ZX›K‚‚‹KKB‚ˆÈÈLKˆZ\ÙH0è›İ\ˆHHØİ[Y[][Û‚‚“Y]™H0è›İ\ˆ]X[™	İ[ˆHÙ\È0ê[0ê[Y[ÈÚ[™ÙH‚‚‹HİXİ\™HH0ê\0íÂ‹HZ›İ]Üİ\™\ÜÚ[Ûˆ	İ[ˆÛXZ[™H›Û˜İ[Û›™[Â‹HÛİ\˜ÙHH°ê\š]0êHÂ‹H›Ü›X]Û›ÛXœ™H\È\ÜÙ]ÈÂ‹H›Û˜İ[Û›™[Y[\Èğê[°ê\˜]]\œÈÂ‹HÛÛ™[[ÛœÈHšXÚY\œÈÂ‹H™[™\™\‹İ[\]Kİ\İÈÂ‹H[ÙH	Ú0êX™\™Ù[Y[Â‹H0ê\[™[˜ÙH^\›™HÂ‹H0êXÚ\Ú[ÛˆH°ê\ÛİY™H[™H[˜ÛÚ0ê\™[˜ÙHØİ[Y[0êYK‚‚•[™HÚ[\H[ÙYšXØ][ÛˆÛÜÛpê]\]YHØØ[H‰Ú[\ÜÙH\È›Ü˜ğê[Y[H°êpêXÜš\™HØ]YˆÚH[HÚ[™ÙH[™H°êÛH°ê]][\ØX›K‚‚‹KKB‚ˆÈÈL‹ˆ°ê\İ[pêHH°êY°ê\™[˜ÙB‚ˆ
Š\XØ][ÛˆX[›ÈHÚ]Xˆ[^ÓÜX[›Øœ˜[˜ÚHX\İ\˜\XØ][Ûˆİ]\]YHSĞÔÔËÒ”ËŠŠ‚‚ˆ
Š“HÛÙHÚ]XˆÛ›™H	ğê]]°êY[ˆHÛ›™HHØ\H]Hpê]ÙKŠŠ‚‚ˆ
Š”™[™\™\ˆØ[›Ûš\]YH\ÈØ[[Y\Èˆ[^ÓÜX[›ØÈX\İ\˜ÈÛÛËÜX[›×ÜØØ[WÜ™[™\™\‹ØˆİZ›İ\œÈ8 &]][\Ù\ˆİ\ˆğê[°ê\™\ˆİHÛÜœšYÙ\ˆ[ˆ‘ÈÈ˜[XZ\ÈHğê[°ê\˜][Ûˆ8 &Z[XYÙHXœ™KŠŠ‚‚ˆ
Š“H’T\İÜš\]YH™\İH[ˆ˜XÚİ\H°êXİ\0ê\˜][Û‹XZ\ÈÚ]Xˆ\İ0ê\ÛÜ›XZ\ÈHÛİ\˜ÙHØ[›Ûš\]YHH[İ]\‹H[\]H]\È\İËŠŠ‚‚ˆ
Š]Xİ[™Hİ\™\ÜÚ[ÛˆØ[œÈ[™[Z\™K0ê\[™[˜Ù\Ë™[\péØ[]˜XÚİ\ŠŠ‚