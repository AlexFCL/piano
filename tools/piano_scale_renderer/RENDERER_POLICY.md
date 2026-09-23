# Politique canonique — rendu des gammes piano

Ce dossier contient le renderer déterministe officiel des images de gammes du projet Application piano.

## Règle absolue
Pour toute génération, correction ou remplacement d'une image de gamme, utiliser exclusivement :
`tools/piano_scale_renderer/`

Ne jamais produire l'asset final par génération d'image libre, redessin manuel, approximation visuelle ou reconstruction du clavier.

## Pipeline obligatoire
1. Charger `official_template.png`.
2. Lire la définition de gamme dans `scales.json`.
3. Mapper notes théoriques → slots physiques → libellés affichés.
4. Remplir les touches blanches actives en `#C53650`.
5. Restaurer les touches noires depuis le template.
6. Remplir les touches noires actives en `#F68C1F`.
7. Poser les libellés.
8. Exécuter les validations.
9. Exporter uniquement si tous les contrôles passent.

## Invariants
- Format : 365 × 254 px.
- Template officiel verrouillé par SHA-256 dans le renderer.
- 7 slots actifs par gamme.
- Séparer slot physique et libellé théorique : un slot D# peut afficher Eb.
- Toute régression découverte doit devenir un test générique, pas un patch local.
- Les golden images C majeur et E majeur doivent rester pixel-identiques.

## Procédure future ChatGPT
Pour une demande du type « génère/corrige telle gamme » :
1. récupérer ce dossier depuis GitHub `AlexFCL/piano`, branche `master`;
2. lancer `python -m unittest -v test_renderer.py`;
3. lancer `python piano_scale_renderer.py "<nom de gamme>"`;
4. contrôler le rapport de validation;
5. livrer le PNG;
6. si demandé, mettre à jour `images/Scales/` dans un commit séparé ou explicitement documenté.

Le ZIP historique du correcteur n'est qu'un backup. GitHub est la source canonique exécutable.
