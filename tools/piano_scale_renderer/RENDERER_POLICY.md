# Politique canonique — rendu des gammes piano

Ce dossier contient le renderer déterministe officiel des images de gammes du projet Application piano.

## Hiérarchie des sources

1. `data/music-theory/tonality-colors.json` — autorité runtime absolue des couleurs.
2. `docs/chatgpt/RENDERERS_SOURCE_OF_TRUTH_V1.md` — ordre de priorité commun à tous les renderers.
3. `docs/chatgpt/PALETTE_TONALITES_ACCORDS_GAMMES_V1.md` — explication fonctionnelle.
4. Le présent fichier — politique spécifique aux gammes et pentatoniques.

En cas de contradiction, la source située plus haut l'emporte. Si le JSON n'est pas accessible, ne pas générer d'asset et ne substituer aucune couleur.

## Règle absolue
Pour toute génération, correction ou remplacement d'une image de gamme, utiliser exclusivement :
`tools/piano_scale_renderer/`

Ne jamais produire l'asset final par génération d'image libre, redessin manuel, approximation visuelle ou reconstruction du clavier.

## Pipeline obligatoire
1. Charger `official_template.png`.
2. Lire la définition de gamme dans `scales.json`.
3. Mapper notes théoriques → slots physiques → libellés affichés.
4. Résoudre la couleur de la gamme depuis `data/music-theory/tonality-colors.json` selon sa tonique et son mode.
5. Remplir toutes les touches actives avec cette même couleur.
6. Restaurer les éléments structurels du template.
7. Poser les libellés.
8. Exécuter les validations.
9. Exporter uniquement si tous les contrôles passent.

## Invariants
- Format : 365 × 254 px.
- Template officiel verrouillé par SHA-256 dans le renderer.
- 7 slots actifs par gamme.
- Séparer slot physique et libellé théorique : un slot D# peut afficher Eb.
- Toute régression découverte doit devenir un test générique, pas un patch local.
- La couleur d'une gamme vient uniquement de la paire tonique/mode.
- Une touche active blanche et une touche active noire utilisent la même couleur de gamme.
- La référence fonctionnelle est `docs/chatgpt/PALETTE_TONALITES_ACCORDS_GAMMES_V1.md` et la source runtime est `data/music-theory/tonality-colors.json`.
- Aucun snapshot binaire historique n'est conservé comme référence colorimétrique. Toute future référence doit être générée par le renderer courant et validée contre `tonality-colors.json`.

## Procédure future ChatGPT
Pour une demande du type « génère/corrige telle gamme » :
1. récupérer ce dossier depuis GitHub `AlexFCL/piano`, branche `master`;
2. lancer `python -m unittest -v test_renderer.py`;
3. lancer `python piano_scale_renderer.py "<nom de gamme>"`;
4. contrôler le rapport de validation;
5. livrer le PNG;
6. si demandé, mettre à jour `images/Scales/` dans un commit séparé ou explicitement documenté.

Le ZIP historique du correcteur n'est qu'un backup. GitHub est la source canonique exécutable.

## Tests et palette

Les tests de ce renderer doivent résoudre leurs couleurs attendues depuis `data/music-theory/tonality-colors.json`. Aucune valeur hexadécimale de couleur active ne doit être figée dans les tests. La politique commune `docs/chatgpt/RENDERERS_SOURCE_OF_TRUTH_V1.md` s'applique intégralement.
