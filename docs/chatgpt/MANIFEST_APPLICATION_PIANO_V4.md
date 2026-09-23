# MANIFEST APPLICATION PIANO — V4

**Objet :** savoir exactement quoi conserver, où chercher et ce qui peut ou non être considéré comme remplaçable.  
**Date :** 23/09/2026.

## Légende de statut

- **CANONIQUE** : source de vérité sur son périmètre.
- **DÉPENDANCE OPÉRATIONNELLE** : nécessaire pour reproduire/maintenir une fonction ; ne pas supprimer.
- **RÉFÉRENCE** : utile pour comprendre une intention ou une décision.
- **LIVE** : doit être relu car évolue.
- **HISTORIQUE** : ne pas utiliser comme état courant, mais conserver en archive.
- **NON DÉTERMINÉ** : rôle incomplet ; conserver par défaut.
- **BACKUP** : sauvegarde de récupération ; garder indépendamment du contexte actif.

## 1. Sources actives recommandées dans le projet ChatGPT

| Élément | Statut | Rôle | Action |
|---|---|---|---|
| `APPLICATION_PIANO_MASTER_V4.md` | CANONIQUE | Architecture + règles globales | Déposer / garder |
| `MANIFEST_APPLICATION_PIANO_V4.md` | CANONIQUE | Conservation + dépendances | Déposer / garder |
| `PLAYBOOK_CHATGPT_APPLICATION_PIANO_V4.md` | CANONIQUE | Routage rapide | Déposer / garder |
| `SOURCE_IMAGES_GAMMES_PIANO_V1.7.md` | RÉFÉRENCE LOCALE | Copie de la doctrine ; la copie GitHub du renderer est canonique | Garder pendant la transition |
| `piano_corrector_v1.zip` | BACKUP | Snapshot historique du renderer | Garder hors GitHub comme récupération |

Les trois V4 constituent le **socle actif ChatGPT**. Le renderer n’est plus dépendant d’une pièce jointe : il est versionné dans GitHub. Les anciennes documentations peuvent rester présentes ; si elles sont retirées du contexte actif un jour, elles doivent auparavant être sauvegardées hors du projet.

## 2. Sources externes / live

| Source | Statut | Rôle | Règle |
|---|---|---|---|
| GitHub `AlexFCL/piano` / `master` | LIVE + CANONIQUE | État courant de l'application | Relire avant toute mutation ou réponse “actuelle” |
| GitHub `tools/piano_scale_renderer/` | CANONIQUE + DÉPENDANCE OPÉRATIONNELLE | Renderer, template, définitions, tests et doctrine des PNG | **Toujours utiliser pour produire/corriger une gamme** |
| GitHub `docs/chatgpt/` | CANONIQUE | Copie durable des documents V4 | Utiliser si les pièces jointes ChatGPT sont absentes |
| GitHub `CHATGPT_PROJECT_POINTER.md` | CANONIQUE | Pointeur minimal de bootstrap | Lire en premier si le contexte projet est incomplet |
| Notion `Spécifications – Générateur de gammes piano` | RÉFÉRENCE | Intention fonctionnelle détaillée | Consulter si comportement fonctionnel concerné |

## 3. Fichiers fournis / sauvegardés

| Élément | SHA-256 vérifié | Statut | Décision |
|---|---|---|---|
| `piano_corrector_v1(1).zip` | `e2df9057692f550ff936c9f2d2a45d231476cfcde1ede9fe4c233d69a38f9cfd` | BACKUP | Conserver comme snapshot historique ; le moteur canonique est maintenant dans GitHub |
| `SOURCE_IMAGES_GAMMES_PIANO_V1.7.md` | `4b6590ffac2992405862aafff4b9f5d67acc4f055acf323b669283d8d70485c3` | CANONIQUE | Garder |
| `Template2(1).png` | `cbda5265b1be6893010e8da73e1b7ab0c25656984724687f2fd13f79f0fa41a9` | CANONIQUE POUR RENDERER | Garder ou conserver via `official_template.png` du correcteur |
| `Template(1).png` | `4f395f36d61d0eb9e350db97081a24fc45a8fd3cf8dbd714a0e5bd94aba8f422` | NON DÉTERMINÉ / LEGACY | Conserver |
| `BACKUP_APPLICATION_PIANO_2026-09-23.zip` | `843c29ceeaa12111ac952e4f6dc8068bf081928d38ef72c1f695e5760371863a` | BACKUP | Conserver hors du contexte actif si possible |

## 4. Contenu indispensable du renderer canonique

Le dossier GitHub `tools/piano_scale_renderer/` doit contenir au minimum :

- `piano_scale_renderer.py` ;
- `scales.json` ;
- `official_template.png` ;
- `test_renderer.py` ;
- `requirements.txt` ;
- `golden/C-majeur.png` ;
- `golden/E-majeur.png` ;
- la capacité à générer les 24 sorties ;
- la capacité à régénérer `validation-report.json`.

`output/`, `last-run.log`, `test-results.txt` et `__pycache__/` ne sont pas canoniques et ne doivent pas être versionnés.

Si le renderer change, les tests doivent passer avant toute mise à jour des assets ou de la documentation.

## 5. Documentation historique

Éléments connus :

- `SOURCE_PROJET_APPLICATION_PIANO(1)(1).md` ;
- `SOURCE_PROJET_APPLICATION_PIANO_V2(1).md` ;
- `SOURCE_PROJET_APPLICATION_PIANO_V3_CONSOLIDEE.md` ;
- `PLAYBOOK_CHATGPT_APPLICATION_PIANO_V3.md`.

Statut : **HISTORIQUE**.

Ils ne décrivent plus complètement l'état courant, mais ils peuvent contenir la chronologie des décisions. Ils peuvent être regroupés dans une archive après sauvegarde, pas supprimés par défaut.

## 6. Fichiers live GitHub à ne pas interpréter comme jetables

- `second_page_backup.html` : nom “backup” mais rôle non validé → conserver.
- `Template.png` / `Template.jpg` : assets legacy à la racine → conserver tant que le rôle n'est pas clarifié.
- `Readme.txt` : vide actuellement → faible valeur, mais aucune suppression recommandée sans raison.

## 7. Règle de remplacement

Un élément A n'est considéré comme remplacé par B que si :

1. B contient toutes les fonctions utiles de A ;
2. les dépendants de A peuvent fonctionner avec B ;
3. les tests pertinents passent ;
4. une sauvegarde indépendante de A existe ;
5. la documentation a été mise à jour ;
6. la décision de retrait est explicite.

Sans ces six conditions : **A reste à conserver**.
