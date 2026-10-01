# RENDERERS — SOURCES DE VÉRITÉ — V1

**Projet :** Application piano  
**Statut :** CANONIQUE — première lecture obligatoire pour toute tâche de rendu d'images  
**Périmètre :** accords, gammes, pentatoniques et tout futur renderer pédagogique

## 1. Hiérarchie de priorité

Pour toute question de couleur ou toute génération/correction d'asset, appliquer cet ordre sans exception :

1. **Source runtime absolue :** `data/music-theory/tonality-colors.json`
2. **Routage et priorité des renderers :** le présent document
3. **Explication fonctionnelle de la palette :** `docs/chatgpt/PALETTE_TONALITES_ACCORDS_GAMMES_V1.md`
4. **Politique du renderer concerné :** `tools/<renderer>/RENDERER_POLICY.md`
5. **README, tests et définitions du renderer concerné**
6. **Documents historiques, snapshots, archives ZIP et anciens échanges** : informatifs uniquement

En cas de contradiction, la source située plus haut dans cette liste l'emporte.

Si `data/music-theory/tonality-colors.json` est absent, illisible ou inaccessible, **ne pas générer d'image et ne substituer aucune couleur**. Récupérer d'abord l'état courant de `AlexFCL/piano`, branche `master`.

## 2. Règle colorimétrique commune

- Toute couleur active est résolue exclusivement depuis `tonality-colors.json`.
- **Règle par défaut** : toutes les touches actives d'un même accord ou d'une même gamme utilisent la même couleur tonique/mode, quelle que soit leur nature physique.
- **Exception documentée maj7 (01/10/2026)** : fondamentale = variante `base` de la tonique ; tierce, quinte et septième = variante `minor` de la tierce majeure, conformément à `PALETTE_TONALITES_ACCORDS_GAMMES_V1.md`.
- Toute autre exception multicolore doit être explicitement spécifiée avant implémentation ; ne jamais l'inférer.
- Les renderers ne doivent définir aucune couleur active statique dépendant du type de touche.
- Les libellés restent blancs.
- Une valeur recopiée dans un README, un test, un snapshot ou un ancien document ne devient jamais une source runtime.

## 3. Renderers couverts

### Accords
- dossier : `tools/piano_chord_renderer/`
- code : `piano_chord_renderer.py`
- politique : `RENDERER_POLICY.md`

### Gammes et pentatoniques
- dossier : `tools/piano_scale_renderer/`
- code commun : `piano_scale_renderer.py`
- définitions : `scales.json` et `pentatonic_scales.json`
- politique : `RENDERER_POLICY.md`

Les pentatoniques ne disposent pas d'un moteur colorimétrique séparé : elles héritent obligatoirement de la même source runtime et du même moteur que les autres gammes.

## 4. Procédure obligatoire avant génération

1. Vérifier le dépôt `AlexFCL/piano` et la branche `master`.
2. Lire `CHATGPT_PROJECT_POINTER.md`.
3. Charger **en premier** `data/music-theory/tonality-colors.json`.
4. Lire le présent document.
5. Lire la politique, le README, le code et les tests du renderer concerné.
6. Exécuter les tests du renderer.
7. Générer les assets uniquement avec le renderer canonique.
8. Vérifier que la couleur réellement utilisée correspond à la paire tonique/mode du JSON.
9. Livrer uniquement les sorties validées.

## 5. Règle pour les tests

Les tests font partie du système de vérité et ne doivent pas devenir une seconde palette.

- Toute valeur attendue de couleur doit être résolue depuis `data/music-theory/tonality-colors.json`.
- Il est interdit de figer une valeur hexadécimale de couleur active dans un test de renderer.
- Chaque renderer doit vérifier que toutes ses sorties utilisent exactement la variante `major` ou `minor` du JSON canonique pour la tonique concernée.
- Une évolution volontaire de `tonality-colors.json` doit donc se propager automatiquement aux tests sans nécessiter de recopier les couleurs.

## 6. Règle anti-régression

Une archive, un ZIP, un snapshot `golden/`, une pièce jointe de projet ou un ancien document peut être utile pour l'historique ou la géométrie, mais **ne doit jamais remplacer la palette runtime courante**.

Toute évolution future de palette se fait d'abord dans `data/music-theory/tonality-colors.json`. Les renderers doivent consommer ce fichier, pas recopier ses valeurs.
