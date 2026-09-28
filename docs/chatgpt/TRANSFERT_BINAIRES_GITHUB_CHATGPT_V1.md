# TRANSFERT DE FICHIERS BINAIRES GITHUB ↔ CHATGPT — V1

**Projet :** Application piano  
**Statut :** procédure opérationnelle ChatGPT  
**Périmètre :** PNG, JPG, ZIP et autres fichiers binaires du dépôt `AlexFCL/piano`

## 1. Problème récurrent

Le connecteur GitHub utilisé par ChatGPT sait manipuler directement les fichiers texte, mais il ne dispose pas d'une action prenant un chemin local `/mnt/data/...` pour téléverser un fichier binaire tel quel.

Pour un binaire, l'API Git sous-jacente exige généralement :
1. lire les octets du fichier local ;
2. les encoder en base64 ;
3. créer un blob Git ;
4. ajouter le blob à un tree ;
5. créer le commit ;
6. déplacer la branche.

Le passage d'un gros base64 entre l'environnement local de ChatGPT et le connecteur GitHub est fragile : taille de charge utile, troncature et limites de sérialisation peuvent faire échouer l'opération.

## 2. Règle obligatoire

### GitHub → ChatGPT / environnement local

- Pour du texte : utiliser les actions GitHub de lecture de fichier.
- Pour un binaire : récupérer d'abord son SHA puis utiliser l'action blob adaptée si elle renvoie le contenu binaire/base64 exploitable.
- Ne jamais interpréter un aperçu textuel ou un SHA seul comme si le fichier binaire avait réellement été rapatrié.

### ChatGPT / environnement local → GitHub

- Pour du texte : utiliser les actions GitHub `create_file` / `update_file`.
- Pour un binaire : **ne pas utiliser `create_file` / `update_file`**, réservées au texte.
- Ne pas tenter par défaut de pousser un gros PNG/ZIP en injectant son base64 entier dans un unique appel de connecteur.
- Si aucune action GitHub n'accepte directement le fichier local ou un contenu binaire de taille sûre, considérer le transfert binaire comme **non fiable dans ce mode de chat** et ne pas prétendre qu'il a été effectué.

## 3. Méthode autorisée si le binaire est petit

La méthode Git object est acceptable uniquement si la charge utile reste raisonnable et peut être transmise intégralement :

1. encoder le fichier en base64 ;
2. `create_blob(encoding="base64")` ;
3. `create_tree` avec le blob ;
4. `create_commit` ;
5. revérifier le HEAD ;
6. `update_ref` en fast-forward ;
7. relire le fichier ou son blob pour vérifier le SHA.

Pour une série de fichiers, créer de préférence **un seul tree et un seul commit**.

## 4. Cas où il faut s'arrêter

S'arrêter avant mutation si :
- le base64 est volumineux ;
- le connecteur tronque ou refuse la charge ;
- le fichier local ne peut pas être fourni directement à l'action GitHub ;
- l'outil ne permet pas de vérifier l'identité binaire après écriture.

Dans ce cas, annoncer précisément la limite au lieu de répéter la même tentative.

## 5. Pourquoi cette règle existe

Les échecs répétés de transfert de PNG dans le dossier `images/Scales/` ne venaient pas de GitHub ni du dépôt : ils venaient du pont entre le stockage local ChatGPT et les actions GitHub, qui est excellent pour le texte mais pas conçu comme un téléverseur de fichiers binaires locaux.

Cette distinction doit être vérifiée avant toute demande du type :
- « envoie ces images sur GitHub » ;
- « récupère ce ZIP depuis GitHub » ;
- « remplace ces PNG en prod ».
