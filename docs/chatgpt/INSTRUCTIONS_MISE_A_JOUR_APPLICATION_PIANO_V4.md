# INSTRUCTIONS PRÉCISES — MISE À JOUR DU PROJET CHATGPT

## Objectif

Mettre en place la documentation V4 **sans supprimer aucune source importante**.

## Étape 1 — conserver le backup hors de ChatGPT

Télécharger et conserver localement :

- `BACKUP_APPLICATION_PIANO_2026-09-23.zip`

Idéalement, faire une seconde copie sur un autre emplacement (cloud personnel, disque externe, etc.).

## Étape 2 — ajouter les trois nouvelles sources V4 au projet ChatGPT « Application piano »

Ajouter :

1. `APPLICATION_PIANO_MASTER_V4.md`
2. `MANIFEST_APPLICATION_PIANO_V4.md`
3. `PLAYBOOK_CHATGPT_APPLICATION_PIANO_V4.md`

## Étape 3 — renderer versionné dans GitHub

Le renderer canonique est :

`AlexFCL/piano` → `master` → `tools/piano_scale_renderer/`

Le dossier contient la V1.7, le script, `scales.json`, le template, les tests et les golden images.

Le ZIP `piano_corrector_v1(1).zip` est une **sauvegarde historique**. Une future conversation ne doit plus en dépendre pour travailler.

## Étape 4 — ne rien supprimer pour le moment

Laisser en place les anciennes V1/V2/V3 pendant la transition. Une nouvelle version documentaire ne remplace jamais automatiquement un script, un asset, un template, un test ou un historique.

## Étape 5 — test de récupération

Ouvrir une nouvelle conversation dans le projet « Application piano » et demander :

> « Donne-moi la hiérarchie des sources de vérité du projet, le dépôt/branche, et explique comment tu génères une image de gamme sans génération libre. »

La réponse correcte doit notamment identifier :

- `AlexFCL/piano` / `master` ;
- MASTER V4 / MANIFEST V4 / PLAYBOOK V4 ;
- `tools/piano_scale_renderer/` comme **source canonique exécutable** ;
- `SOURCE_IMAGES_GAMMES_PIANO_V1.7.md` dans ce dossier pour la doctrine ;
- le template 365×254 verrouillé ;
- le ZIP historique uniquement comme backup.

Si ce test échoue, **ne retirer aucune ancienne source**.

## Étape 6 — nettoyage éventuel, uniquement après test

Optionnel. Si tu veux réduire les contradictions dans le contexte actif :

- conserver le backup ZIP local ;
- regrouper les anciennes V1/V2/V3 dans une archive historique ;
- retirer seulement leurs copies individuelles du projet ChatGPT après vérification.

Ne rien supprimer est une option valide.

## Étape 7 — vérifier le pointeur GitHub

Le dépôt doit contenir :

- `CHATGPT_PROJECT_POINTER.md` à la racine ;
- `docs/chatgpt/` avec les documents V4 ;
- `tools/piano_scale_renderer/` avec le moteur.

Dans une future conversation, si ChatGPT hésite sur la méthode de génération, la réponse correcte est **d’ouvrir ce pointeur et le dossier GitHub**, pas de reconstruire la méthode de mémoire.

## Étape 8 — Notion

La page `Spécifications – Générateur de gammes piano` reste une référence fonctionnelle. GitHub reste la source de vérité de l’état réel. Sa mise à jour de statut est recommandée mais distincte de la publication du renderer.

## Quand mettre la V4 à jour ensuite ?

Mettre à jour MASTER/MANIFEST/PLAYBOOK quand :

- une page ou un domaine est ajouté/supprimé ;
- une source de vérité change ;
- le renderer change ;
- le template ou son hash change ;
- les conventions de noms changent ;
- le comportement fonctionnel des générateurs change ;
- le mode de déploiement change ;
- une incohérence connue est résolue.

Pour une simple retouche CSS locale, mettre à jour la V4 seulement si elle introduit une nouvelle convention générale.