# APPLICATION PIANO — POINTEUR DE BOOTSTRAP CHATGPT

Ce fichier doit permettre à une future conversation de retrouver immédiatement les sources utiles sans dépendre de la mémoire d'une ancienne conversation.

## Identité
- Projet : Application piano
- Dépôt : `AlexFCL/piano`
- Branche canonique : `master`
- Stack : HTML / CSS / JavaScript statique
- État réel du code : GitHub

## Première lecture
1. `docs/chatgpt/PLAYBOOK_CHATGPT_APPLICATION_PIANO_V4.md`
2. `docs/chatgpt/APPLICATION_PIANO_MASTER_V4.md` si davantage de contexte est nécessaire
3. `docs/chatgpt/MANIFEST_APPLICATION_PIANO_V4.md` avant toute suppression, archivage ou nettoyage

## Renderer canonique des images de gammes
Chemin obligatoire :
`tools/piano_scale_renderer/`

Pour toute génération, correction ou remplacement d'un PNG de gamme :
1. lire `tools/piano_scale_renderer/README.md`;
2. lire `tools/piano_scale_renderer/RENDERER_POLICY.md`;
3. récupérer le renderer, le template, les définitions et les tests depuis ce dossier;
4. exécuter les tests;
5. exécuter `piano_scale_renderer.py`;
6. utiliser uniquement la sortie validée.

Ne jamais improviser une image de gamme avec un générateur visuel libre ou un redessin approximatif.

## Sources fonctionnelles
- Application live : GitHub
- Intentions / spécifications fonctionnelles des gammes : Notion, page « Spécifications – Générateur de gammes piano »
- Renderer des PNG de gammes : GitHub `tools/piano_scale_renderer/`

## Règle de conservation
Ne jamais conseiller la suppression d'une source, d'un script, d'un asset, d'un template, d'un test ou d'une archive sans avoir vérifié son contenu, ses dépendances, son remplaçant et l'existence d'un backup. En cas de doute : conserver.
