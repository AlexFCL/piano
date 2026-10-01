# PALETTE TONALITÉS — ACCORDS ET GAMMES — V1

**Projet :** Application piano  
**Statut :** référence fonctionnelle canonique  
**Source de données runtime :** `data/music-theory/tonality-colors.json`  
**Périmètre :** accords, gammes et renderers pédagogiques utilisant l'identité tonique/mode

## 0. Autorité et priorité

La **source runtime absolue** des couleurs est `data/music-theory/tonality-colors.json`.

Le présent document explique la règle fonctionnelle, mais ne doit jamais être utilisé comme copie autonome de la palette. En cas d'écart entre ce document et le JSON, **le JSON l'emporte**.

Avant toute tâche sur un renderer, lire aussi `docs/chatgpt/RENDERERS_SOURCE_OF_TRUTH_V1.md`. Si le JSON n'est pas accessible, aucune couleur ne doit être substituée ou déduite.

## 1. Règle fonctionnelle

La couleur dépend de la **tonique** et du **mode** :

- majeur → colonne **Majeur** ;
- mineur → colonne **Mineur** ;
- **Base** → identité neutre de la tonique pour un usage sans mode ou futur ;
- les graphies enharmoniques d'une même ligne partagent la même famille.

## 2. Table de lecture documentaire (non autoritaire)

| Tonique | Base | Majeur | Mineur |
|---|---|---|---|
| **Do** | `#D62828` | `#B51B1B` | `#EB8080` |
| **Do# / Réb** | `#00A6A6` | `#008F8F` | `#66CCCC` |
| **Ré** | `#E6A700` | `#C48F00` | `#F1CC66` |
| **Ré# / Mib** | `#7B2CBF` | `#5E1F99` | `#B883E3` |
| **Mi** | `#2E9B45` | `#228037` | `#7CC88B` |
| **Fa** | `#8B5A2B` | `#6F4622` | `#C9A27E` |
| **Fa# / Solb** | `#2196F3` | `#1976D2` | `#7EC3F9` |
| **Sol** | `#F26B21` | `#D35415` | `#F8A67E` |
| **Sol# / Lab** | `#26428B` | `#1D3370` | `#6F8FD6` |
| **La** | `#E83E8C` | `#C72D74` | `#F19BC2` |
| **La# / Sib** | `#86B817` | `#6E9612` | `#B8DB67` |
| **Si** | `#8E244D` | `#731E3E` | `#CC6F8F` |

## 3. Exemples

- **Do majeur** → `#B51B1B`
- **Do mineur** → `#EB8080`
- **Mib majeur** → `#5E1F99`
- **Mib mineur** → `#B883E3`
- **Fa# majeur** → `#1976D2`
- **Solb mineur** → `#7EC3F9`

## 4. Source unique

Ne pas recopier ces couleurs dans les scripts, renderers ou tests. La table structurée dans
`data/music-theory/tonality-colors.json` est la seule source runtime à consommer.

La table ci-dessus est un miroir documentaire lisible. Si elle diverge du JSON, elle est considérée obsolète et le JSON l'emporte.

Tous les renderers actuels et futurs doivent suivre `docs/chatgpt/RENDERERS_SOURCE_OF_TRUTH_V1.md` et lire directement cette source. Les tests doivent eux aussi résoudre les valeurs attendues depuis le JSON, sans figer de valeur hexadécimale de couleur active.

## 5. Règle de rendu

Lorsqu'un renderer adopte cette palette, toutes les touches actives d'un même accord ou d'une même gamme utilisent la **même couleur tonique/mode**, quelle que soit la nature blanche ou noire de la touche. Les libellés de notes restent blancs.


## 6. Extension mnémotechnique — accords maj7

**Décision fonctionnelle du 01/10/2026.**

Pour un accord **maj7 en position fondamentale**, les quatre notes sont :
`fondamentale – tierce majeure – quinte juste – septième majeure`.

Règle visuelle spécifique :
- la **fondamentale** utilise la variante `base` de sa tonique dans `data/music-theory/tonality-colors.json` ;
- les **trois autres notes** utilisent ensemble la variante `minor` de la **tierce majeure**, car ces trois notes forment le triade mineur construit sur cette tierce.

Exemple :
- `Cmaj7 = C E G B` ;
- `C` → `base` de C ;
- `E G B` → `minor` de E, car `E G B = E mineur`.

Cette règle est une **exception mnémotechnique explicitement documentée** à la règle historique « une couleur unique par accord ». Elle ne modifie pas rétroactivement les PNG de triades majeures/mineures existants.

Les deux couleurs doivent toujours être résolues depuis le JSON canonique ; aucune valeur hexadécimale ne doit être figée dans un nouveau renderer.

Le rendu reste déterministe, dérivé du template officiel 711×254, avec placement au plus près du centre permis par les deux octaves du template.

La règle visuelle des **accords min7** n'est pas encore spécifiée dans cette version : ne pas l'inventer.
