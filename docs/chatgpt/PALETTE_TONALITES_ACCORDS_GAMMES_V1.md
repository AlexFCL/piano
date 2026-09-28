# PALETTE TONALITÉS — ACCORDS ET GAMMES — V1

**Projet :** Application piano  
**Statut :** référence canonique pour la couleur associée à une tonique et à son mode  
**Périmètre :** éléments d’interface représentant un accord ou une gamme

## 1. Règle fonctionnelle

La couleur d’un accord ou d’une gamme dépend de deux informations :

1. sa **tonique** ;
2. son **mode**.

Règle d’application :

- si l’accord ou la gamme est **majeur(e)**, utiliser la colonne **Majeur** de la tonique ;
- si l’accord ou la gamme est **mineur(e)**, utiliser la colonne **Mineur** de la tonique ;
- la colonne **Base** conserve la couleur d’identité de la tonique pour un usage neutre, un état sans mode ou un besoin futur ;
- les graphies enharmoniques indiquées sur une même ligne utilisent exactement la même famille de couleurs : Do# / Réb, Ré# / Mib, Fa# / Solb, Sol# / Lab, La# / Sib.

La couleur **Base** ne doit donc pas remplacer les variantes Majeur/Mineur lorsqu’un mode est connu.

## 2. Table canonique

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
| **Si** | `#8F244D` | `#731E3E` | `#CC6F8F` |

## 3. Exemples d’application

- **Do majeur** → `#B51B1B`
- **Do mineur** → `#EB8080`
- **Mib majeur** → `#5E1F99`
- **Mib mineur** → `#B883E3`
- **Fa# majeur** → `#1976D2`
- **Solb mineur** → `#7EC3F9`

## 4. Portée dans l’application

Cette palette est **transversale aux accords et aux gammes**. Elle sert à colorer les éléments d’interface associés au nom ou à l’identité harmonique d’un accord/d’une gamme.

Pour les gammes, le périmètre actuel de l’application comprend 12 majeures et 12 mineures naturelles. La règle « Mineur » reste la règle par défaut pour toute future famille explicitement mineure, sauf décision fonctionnelle ultérieure contraire.

## 5. Ne pas confondre avec la palette du renderer piano

Cette palette **ne remplace pas** la palette technique du renderer des PNG de gammes.

Le renderer conserve sa propre convention pour les touches du clavier :

- touche blanche active : `#C53650` ;
- touche noire active : `#F68C1F` ;
- texte : blanc ;
- structure : template original.

Les deux systèmes répondent à des fonctions différentes :

- **palette tonalité/mode** = identité visuelle de l’accord ou de la gamme dans l’interface ;
- **palette renderer** = remplissage des touches actives dans les images pédagogiques.

## 6. Règle d’implémentation future

Lors d’une future implémentation, éviter de recopier ces couleurs manuellement dans plusieurs scripts/pages. Préférer une **source de données unique** contenant, pour chaque tonique, les trois valeurs `base`, `major` et `minor`, puis faire consommer cette source par les interfaces concernées.

Cette documentation est la source fonctionnelle de référence tant que cette palette n’a pas été déplacée vers une source runtime unique explicitement documentée.
