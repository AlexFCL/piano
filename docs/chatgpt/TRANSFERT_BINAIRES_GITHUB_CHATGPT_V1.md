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

La méthode Git object est acceptable uniquement si la charge utile reste raisonnable et peut être transmise intégralement.

Procédure obligatoire dans ChatGPT :
1. vérifier la taille réelle du fichier local ;
2. encoder **un seul fichier binaire par appel** en base64 ;
3. appeler `create_blob(encoding="base64")` pour ce seul fichier ;
4. noter immédiatement le SHA du blob ;
5. répéter fichier par fichier ; ne jamais regrouper plusieurs gros base64 dans le même appel ;
6. une fois tous les blobs créés, créer **un seul tree** contenant l'ensemble des chemins ;
7. créer **un seul commit** ;
8. revérifier le HEAD juste avant `update_ref` ;
9. déplacer `master` uniquement en fast-forward ;
10. relire plusieurs fichiers créés et vérifier leurs blob SHA.

Retour d'expérience validé le 28/09/2026 : des PNG d'environ 4–5 Ko passent correctement avec cette granularité. Le regroupement de plusieurs base64 dans un seul appel est à éviter même si la somme paraît petite.

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
