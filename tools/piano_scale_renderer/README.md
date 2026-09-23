# Correcteur / renderer déterministe — gammes piano

Ce dossier remplace la génération d'images libre par un **renderer déterministe**.

## Principe

Le programme ne redessine jamais un clavier. Il :

1. charge `official_template.png` (365×254 px) ;
2. détecte et verrouille sa géométrie canonique ;
3. remplit les **masques fixes** des touches blanches actives en `#C53650` ;
4. restaure les touches noires depuis le template original ;
5. remplit l'intérieur des touches noires actives en `#F68C1F` ;
6. valide les aplats **avant** de poser le texte ;
7. place les libellés avec Roboto Condensed Bold ;
8. rejette l'image si une validation échoue.

Aucun modèle d'image n'est utilisé pour les assets finaux.

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
```

Les PNG sont écrits dans `output/`. Un `validation-report.json` est créé à chaque exécution.

## Tests anti-régression

```bash
python -m unittest -v test_renderer.py
```

Les tests couvrent notamment :

- D et E de D majeur remplis jusqu'en haut ;
- D de Eb majeur rempli jusqu'en haut ;
- mapping Db majeur verrouillé : `Db→C#`, `Eb→D#`, `Gb→F#`, `Ab→G#`, `Bb→A#` ;
- touches blanches inactives de Db majeur restant blanches ;
- 24 gammes ayant exactement 7 slots actifs.

## Dépendance

- Python 3
- Pillow
- Roboto Condensed Bold installée sur la machine (non incluse dans ce dossier)

## Verrouillage supplémentaire

Le renderer vérifie aussi le **SHA-256 exact du template officiel** avant toute génération. Si le template est remplacé ou modifié, la génération s'arrête.

Deux images approuvées (`golden/C-majeur.png` et `golden/E-majeur.png`) servent de références de non-régression : le renderer doit les reproduire **pixel pour pixel**.
