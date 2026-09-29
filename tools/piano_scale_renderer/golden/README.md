# Golden — répertoire volontairement sans snapshot binaire

Les anciens snapshots binaires ont été retirés pour qu'aucun asset historique ne puisse être pris par erreur comme référence colorimétrique.

Pour toute non-régression de rendu :
- source runtime des couleurs : `../../../data/music-theory/tonality-colors.json` ;
- hiérarchie commune : `../../../docs/chatgpt/RENDERERS_SOURCE_OF_TRUTH_V1.md` ;
- renderer courant : `../piano_scale_renderer.py` ;
- tests courants : `../test_renderer.py` et `../test_pentatonic_renderer.py`.

Si des snapshots binaires sont réintroduits un jour, ils doivent être générés par le renderer courant et validés contre la palette runtime du même commit.
