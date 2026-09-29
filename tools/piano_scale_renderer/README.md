# Correcteur / renderer déterministe — gammes piano

Ce dossier remplace la génération d'images libre par un **renderer déterministe**.

## Principe

Le programme ne redessine jamais un clavier. Il :

1. charge `official_template.png` (365×254 px) ;
2. détecte et verrouille sa géométrie canonique ;
3. lit la couleur de la gamme dans `../../data/music-theory/tonality-colors.json` à partir de sa **tonique** et de son **mode** ;
4. remplit toutes les touches actives, blanches ou noires, avec cette **même couleur tonique/mode** ;
5. restaure les éléments structurels du template ;
6. valide les aplats **avant** de poser le texte ;
7. place les libellés avec Roboto Condensed Bold ;
8. rejette l'image si une validation échoue.

Aucun modèle d'image n'est utilisé pour les assets finaux.

## Familles prises en charge

Un **seul moteur de rendu** est utilisé pour toutes les familles afin d'éviter les divergences de géométrie, de palette et de validation.

- `scales.json` : 12 gammes majeures + 12 gammes mineures naturelles, **7 notes actives** ;
- `pentatonic_scales.json` : 12 pentatoniques majeures + 12 pentatoniques mineures, **5 notes actives**.

Le nombre de notes attendu est déterminé par la famille de la gamme. Les pentatoniques ne possèdent pas de renderer séparé.

## Palette canonique

Ordre obligatoire :
1. `../../data/music-theory/tonality-colors.json` — autorité runtime absolue ;
2. `../../docs/chatgpt/RENDERERS_SOURCE_OF_TRUTH_V1.md` — hiérarchie commune à tous les renderers ;
3. `../../docs/chatgpt/PALETTE_TONALITES_ACCORDS_GAMMES_V1.md` — explication fonctionnelle.

- une gamme majeure utilise la variante `major` de sa tonique ;
- une gamme mineure utilise la variante `minor` de sa tonique ;
- toutes les touches actives utilisent la même couleur, indépendamment du fait qu'elles soient blanches ou noires ;
- les libellés restent blancs ;
- aucune couleur active statique dépendant du type physique de touche ne doit être utilisée ;
- si le JSON canonique est inaccessible, aucune image ne doit être générée et aucune couleur ne doit être substituée.

## Séparation fondamentale

`scales.json` sépare explicitement :

- **slot physique** du clavier : `C#`, `D#`, etc. ;
- **libellé théorique affiché** : `Db`, `Eb`, etc.

Exemple Db majeur :

```json
{
  "C": "C",
  "C#": "Db",
  "D#": "Eb",
  "F": "F",
  "F#": "Gb",
  "G#": "Ab",
  "A#": "Bb"
}
```

Ainsi `Eb` ne peut pas « glisser » vers une autre touche : son slot physique est `D#`.

## Utilisation

```bash
python piano_scale_renderer.py "Db majeur"
python piano_scale_renderer.py "D majeur"
python piano_scale_renderer.py "Eb majeur"
python piano_scale_renderer.py --all

# Pentatoniques
python piano_scale_renderer.py --scales pentatonic_scales.json "C pentatonique majeure"
python piano_scale_renderer.py --scales pentatonic_scales.json "Eb pentatonique mineure"
python piano_scale_renderer.py --scales pentatonic_scales.json --all
```

Les PNG sont écrits dans `output/`. Un `validation-report.json` est créé à chaque exécution.

## Tests anti-régression

```bash
python -m unittest -v test_renderer.py
python -m unittest -v test_pentatonic_renderer.py
```

Les tests couvrent notamment :

- D et E de D majeur remplis jusqu'en haut ;
- D de Eb majeur rempli jusqu'en haut ;
- mapping Db majeur verrouillé : `Db→C#`, `Eb→D#`, `Gb→F#`, `Ab→G#`, `Bb→A#` ;
- touches blanches inactives de Db majeur restant blanches ;
- 24 gammes classiques ayant exactement 7 slots actifs ;
- 24 pentatoniques ayant exactement 5 slots actifs ;
- même palette tonique/mode pour les gammes classiques et pentatoniques ;
- correspondances enharmoniques des pentatoniques verrouillées par tests.

## Dépendance

- Python 3
- Pillow
- Roboto Condensed Bold installée sur la machine (non incluse dans ce dossier)

## Verrouillage supplémentaire

Le renderer vérifie aussi le **SHA-256 exact du template officiel** avant toute génération. Si le template est remplacé ou modifié, la génération s'arrête.

Les anciens fichiers du dossier `golden/` sont des snapshots historiques. Ils ne constituent plus une référence colorimétrique tant qu'ils n'ont pas été régénérés depuis la palette tonique/mode actuelle.
