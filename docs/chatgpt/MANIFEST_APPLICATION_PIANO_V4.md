# MANIFEST — APPLICATION PIANO V4

Ce manifeste répond à : « Qu'est-ce qui doit rester disponible pour maintenir le projet sans perte de capacité ? »

## CANONIQUE — NE PAS SUPPRIMER
### Dépôt applicatif
- `AlexFCL/piano`
- branche `master`

### Bootstrap ChatGPT
- `/CHATGPT_PROJECT_POINTER.md`

### Documentation de routage
- `docs/chatgpt/PLAYBOOK_CHATGPT_APPLICATION_PIANO_V4.md`
- `docs/chatgpt/APPLICATION_PIANO_MASTER_V4.md`
- `docs/chatgpt/MANIFEST_APPLICATION_PIANO_V4.md`

### Renderer des images de gammes — DÉPENDANCE OPÉRATIONNELLE
- dossier `tools/piano_scale_renderer/`
- `piano_scale_renderer.py`
- `requirements.txt`
- `scales.json`
- `official_template.png`
- `test_renderer.py`
- `golden/`
- `README.md`
- `RENDERER_POLICY.md`

Sans ce dossier, le projet perd sa méthode déterministe de production des PNG de gammes.

## ASSETS RUNTIME
- `images/Chords/`
- `images/Scales/`

Ne jamais considérer ces dossiers comme reconstruisibles sans avoir vérifié la chaîne de production correspondante.

## RÉFÉRENCE FONCTIONNELLE
- Notion : « Spécifications – Générateur de gammes piano »

## HISTORIQUE / BACKUPS
Les anciennes versions documentaires, ZIP, templates historiques et snapshots restent à conserver tant qu'une analyse explicite n'a pas établi qu'ils sont redondants et sauvegardés.

## Protocole obligatoire avant suppression
Pour chaque élément :
1. ouvrir / inspecter;
2. décrire son rôle;
3. identifier ses dépendants;
4. identifier un remplaçant réel;
5. vérifier un backup;
6. seulement ensuite décider ARCHIVER ou SUPPRIMER.

Si un point n'est pas démontré : CONSERVER.
