# SOURCE IMAGES GAMMES PIANO — V1.7

## Objet
Cette version **V1.7** documente la capitalisation issue de l’incident constaté sur certaines gammes (ex. D majeur, Eb majeur), **non pas comme un correctif local**, mais comme une **évolution générale de méthode** destinée à empêcher toute régression future sur **n’importe quelle gamme**.

L’objectif de cette V1.7 est donc :
- d’interdire toute méthode interprétative de rendu ;
- d’imposer un pipeline de production **déterministe** ;
- de formaliser des **invariants globaux** ;
- d’ajouter une procédure de **contrôle qualité générique** applicable à toutes les gammes ;
- d’éviter qu’un futur cas (ex. G majeur, Ab majeur, B majeur, etc.) reproduise le même type d’erreur sous une autre forme.

---

## 1. Constat capitalisé

### 1.1 Nature du problème observé
Les incidents observés n’étaient **pas** des erreurs théoriques de gamme.
Ils provenaient d’un **écart de méthode de rendu** :
- certaines touches blanches actives étaient correctement identifiées comme actives ;
- mais leur **remplissage rouge n’occupait pas toute la surface attendue de la touche** ;
- une zone blanche parasite restait visible dans la partie haute de la touche, autour des touches noires.

### 1.2 Pourquoi ce problème est grave
Le problème est grave car il peut se reproduire sur **n’importe quelle touche blanche active** et dans **n’importe quelle gamme** si le système s’autorise à :
- redessiner le clavier librement ;
- interpréter visuellement les formes ;
- ou reconstruire le rendu au lieu d’utiliser les masques officiels.

### 1.3 Leçon générale
La leçon à retenir n’est **pas** :
- « faire attention à D majeur » ;
- « faire attention à Eb majeur ».

La vraie leçon est :

> **Toute image de gamme doit être produite comme un rendu déterministe à partir du template officiel, jamais comme une génération visuelle interprétative.**

---

## 2. Changement de doctrine

### 2.1 Interdiction de la génération visuelle libre
Pour ce projet, le verbe « générer » une image de gamme signifie désormais exclusivement :

> **Produire un PNG final par application de règles, de masques et de compositing sur le template officiel.**

Cela exclut explicitement :
- tout redessin libre du clavier ;
- toute synthèse visuelle approximative ;
- toute reconstruction du clavier « à la main » ou par modèle d’image ;
- toute sortie dont la géométrie ou les aplats ne dérivent pas directement du template canonique.

### 2.2 Pipeline unique autorisé
Le pipeline autorisé est désormais le suivant :

1. Charger le **template officiel immuable**.
2. Déterminer la liste des **notes théoriques de la gamme**.
3. Convertir ces notes en **slots physiques du clavier**.
4. Déterminer le **libellé affiché** pour chaque slot actif.
5. Appliquer les **remplissages couleur par masque**.
6. Restaurer les éléments fixes du template (touches noires inactives, contours, structure).
7. Poser les **libellés** sur les touches actives.
8. Exécuter les **contrôles qualité automatiques**.
9. Exporter le PNG final uniquement si tous les contrôles passent.

Aucune autre méthode n’est acceptée.

---

## 3. Séparation obligatoire des concepts

Pour éviter les confusions de logique, le système doit maintenant traiter séparément **trois niveaux**.

### 3.1 Niveau A — structure physique du clavier
Une octave est composée des **slots fixes** suivants :
- C
- C#
- D
- D#
- E
- F
- F#
- G
- G#
- A
- A#
- B

Ces slots sont purement structurels.

### 3.2 Niveau B — notes actives de la gamme
La gamme détermine quelles notes sont actives.
Exemples :
- D majeur = D, E, F#, G, A, B, C#
- Eb majeur = Eb, F, G, Ab, Bb, C, D
- F majeur = F, G, A, Bb, C, D, E

### 3.3 Niveau C — libellé affiché
Le texte affiché dans l’image peut différer du nom structurel du slot.
Exemples :
- le slot **D#** peut afficher **Eb** ;
- le slot **G#** peut afficher **Ab** ;
- le slot **A#** peut afficher **Bb**.

### 3.4 Conséquence opérationnelle
Chaque touche active doit donc être décrite avec **au minimum** :
- un **slot physique** à colorer ;
- une **couleur** à appliquer ;
- un **libellé** à afficher.

Cette séparation est obligatoire et non négociable.

---

## 4. Invariants globaux de rendu

Les invariants suivants s’appliquent à **toutes les gammes**, sans exception.

### 4.1 Invariant de format
Le fichier final doit être strictement au format canonique :
- **365 × 254 px**

Tout autre format est non conforme.

### 4.2 Invariant de template
Le rendu final doit dériver du **template officiel immuable**.
La structure du clavier ne doit jamais être reconstruite librement.

### 4.3 Invariant de palette
Seules les couleurs officielles sont autorisées :
- rouge des touches blanches actives : `#C53650`
- orange des touches noires actives : `#F68C1F`
- blanc
- noir

Toute teinte parasite ou approximation colorimétrique est non conforme.

### 4.4 Invariant de remplissage des touches blanches actives
Pour **toute touche blanche active** :
- le rouge doit remplir **100 % du masque officiel de la touche blanche** ;
- cela inclut la partie haute de la touche, derrière les zones occupées visuellement par les touches noires ;
- les touches noires sont ensuite redessinées/restaurées par-dessus selon le template.

Aucune zone blanche parasite ne doit subsister dans une touche blanche active.

### 4.5 Invariant de remplissage des touches noires actives
Pour **toute touche noire active** :
- l’orange doit remplir **100 % du masque officiel de la touche noire** ;
- le remplissage doit être exact ;
- aucun décalage, tronquage ou approximation n’est toléré.

### 4.6 Invariant actif/inactif
Pour chaque image :
- toute touche attendue comme **active** doit être correctement colorée ;
- toute touche attendue comme **inactive** doit rester neutre.

### 4.7 Invariant label ↔ slot
Chaque libellé doit satisfaire simultanément :
- bon **texte** ;
- bonne **touche** ;
- bonne **position**.

### 4.8 Invariant d’intégrité de structure
Les éléments structurels du template doivent être conservés :
- contours ;
- géométrie ;
- séparations ;
- distribution exacte des touches noires.

---

## 5. Ordre de rendu obligatoire

L’ordre de rendu suivant est désormais imposé :

1. **Template de base**
2. **Remplissage complet des touches blanches actives**
3. **Restauration des touches noires inactives et de la structure**
4. **Remplissage des touches noires actives**
5. **Pose des libellés**
6. **Contrôle qualité**

### 5.1 Justification
Cet ordre empêche précisément le défaut où une touche blanche active serait remplie seulement sur sa partie basse.

### 5.2 Interdiction corrélée
Il est interdit de :
- peindre une touche blanche active uniquement sur sa zone visible sous les noires ;
- considérer qu’une touche blanche est « correcte » si seule sa partie basse est colorée ;
- produire un rendu qui ne suit pas cet ordre.

---

## 6. Contrôles qualité génériques avant livraison

Aucune image ne doit être livrée sans passer **tous** les contrôles suivants.

### 6.1 Contrôle structurel
Vérifier :
- dimensions exactes : 365 × 254 px ;
- utilisation du template canonique ;
- conservation de la géométrie.

### 6.2 Contrôle palette
Vérifier :
- présence exclusive des couleurs autorisées ;
- absence de teintes parasites.

### 6.3 Contrôle des touches actives
Vérifier :
- concordance entre la gamme demandée et la liste des slots actifs ;
- activation correcte de toutes les touches attendues.

### 6.4 Contrôle des touches inactives
Vérifier :
- absence de coloration sur les slots qui ne doivent pas être actifs.

### 6.5 Contrôle de remplissage des blanches actives
Pour chaque touche blanche active, vérifier que :
- le masque complet est coloré ;
- aucune zone blanche parasite n’apparaît dans la touche.

### 6.6 Contrôle de remplissage des noires actives
Pour chaque touche noire active, vérifier que :
- le masque complet est coloré en orange.

### 6.7 Contrôle des labels
Vérifier :
- nombre de libellés ;
- orthographe exacte ;
- association bon label / bon slot ;
- position correcte.

### 6.8 Contrôle final de conformité
Si un seul de ces contrôles échoue, le fichier est **rejeté** et ne doit pas être livré.

---

## 7. Procédure anti-régression globale

### 7.1 Principe
Un incident découvert sur une gamme doit désormais produire une **règle générale**, pas un patch local.

### 7.2 Obligation de capitalisation
À chaque incident détecté, il faut se demander :
- quelle propriété générale a été violée ?
- comment transformer cette propriété en invariant ?
- quel contrôle automatique permet d’empêcher toute réapparition du problème ?

### 7.3 Forme attendue des corrections
Les corrections acceptables sont :
- mise à jour d’un invariant global ;
- ajout d’un contrôle qualité générique ;
- amélioration du pipeline déterministe ;
- ajout d’une règle d’interdiction si nécessaire.

Les corrections **non** acceptables sont :
- « faire attention à ce cas précis » ;
- mémoriser une exception manuelle isolée ;
- corriger visuellement une image sans corriger la méthode.

---

## 8. Tests de régression à maintenir

Les cas qui ont révélé un défaut doivent rester présents dans les tests de régression, **mais ils ne doivent pas être les seuls**.

### 8.1 Jeux de tests minimaux
Le référentiel de test doit couvrir au minimum :
- une gamme avec seulement des blanches (ex. C majeur) ;
- une gamme mixte simples dièses (ex. D majeur) ;
- une gamme mixte avec bémols affichés sur slots dièses (ex. Eb majeur) ;
- une gamme avec un seul bémol (ex. F majeur) ;
- une gamme fortement altérée (ex. C# majeur ou F# majeur).

### 8.2 But du référentiel
Le but n’est pas de « tester les exemples connus » seulement, mais de vérifier que :
- les touches blanches actives sont toujours totalement remplies ;
- les slots et les labels restent correctement séparés ;
- le pipeline fonctionne pour différents profils de gamme.

---

## 9. Interdictions absolues

Sont désormais explicitement interdits :

1. **Redessiner le clavier** au lieu d’utiliser le template.
2. **Laisser un modèle d’image interpréter la géométrie**.
3. **Livrer une image hors format canonique**.
4. **Colorer partiellement une touche blanche active**.
5. **Fusionner la logique “slot physique” et la logique “libellé théorique”**.
6. **Corriger un cas isolé sans transformer la correction en règle générale**.

---

## 10. Règle opérationnelle finale

Pour ce projet, la règle de référence est désormais la suivante :

> **Toute image de gamme doit être construite par mapping explicite des notes vers des slots fixes, application de masques officiels, rendu déterministe, puis validation par invariants globaux.**

Et en formulation courte :

> **Pas de génération interprétative. Pas de patch local. Pipeline déterministe + contrôles globaux.**

---

## Statut de la V1.7
Cette V1.7 est une **mise à jour de doctrine**.
Elle complète les versions précédentes et formalise la méthode à suivre pour toutes les productions futures d’images de gammes piano du projet.
