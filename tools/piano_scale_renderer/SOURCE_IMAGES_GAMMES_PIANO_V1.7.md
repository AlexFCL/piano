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

> **V��ƭy