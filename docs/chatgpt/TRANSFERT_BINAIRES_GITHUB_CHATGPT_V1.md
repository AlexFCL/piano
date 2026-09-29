# TRANSFERT DE FICHIERS BINAIRES GITHUB ↔ CHATGPT — V2

**Projet :** Application piano  
**Statut :** procédure opérationnelle ChatGPT  
**Périmètre :** PNG, JPG, ZIP et autres fichiers binaires du dépôt `AlexFCL/piano`

## 1. Cause racine des échecs répétés

Le problème n'est pas GitHub et ce n'est pas non plus le format PNG.

Le problème vient de l'architecture des outils utilisés par ChatGPT :

- l'environnement local / container peut lire et écrire les fichiers de `/mnt/data` ;
- le connecteur GitHub authentifié peut lire et écrire dans GitHub ;
- **ces deux environnements ne partagent pas directement leur système de fichiers** ;
- l'action GitHub `create_blob` accepte une chaîne de caractères (`utf-8` ou `base64`), **pas un chemin local ni une référence de fichier du container** ;
- réciproquement, les lectures GitHub de fichiers binaires ne déposent pas automatiquement les octets dans `/mnt/data`.

Il n'existe donc pas, dans ce mode de chat, de canal natif du type :

`/mnt/data/image.png` → GitHub

ou :

GitHub → `/mnt/data/image.png`

sans étape intermédiaire.

## 2. Pourquoi le relais base64 plante

Pour envoyer un binaire local vers GitHub, il faudrait :

1. lire le fichier dans le container ;
2. l'encoder en base64 ;
3. faire sortir cette chaîne du container ;
4. la faire transiter par le contexte / les arguments d'outil ;
5. la réinjecter dans le connecteur GitHub ;
6. appeler `create_blob(encoding="base64")`.

Ce relais est intrinsèquement fragile :

- le base64 grossit les données d'environ 33 % ;
- les sorties d'outils et le contexte ont des limites de taille ;
- une chaîne longue peut être tronquée avant d'arriver au connecteur ;
- un lot de plusieurs images multiplie très vite la taille transportée ;
- même si un petit fichier peut parfois passer, cela ne constitue pas un chemin de transfert fiable.

**Conclusion : le modèle ne doit pas utiliser son propre contexte comme bus de transport binaire.**

## 3. Pourquoi le problème existe aussi dans l'autre sens

Pour rapatrier un fichier GitHub dans le container :

- le connecteur GitHub peut récupérer le contenu ou le blob ;
- mais il ne peut pas écrire directement dans `/mnt/data` ;
- le container peut écrire le fichier ;
- mais il ne peut pas consommer directement le résultat interne du connecteur GitHub sans que les données transitent à nouveau par le contexte.

Le même problème de pont apparaît donc dans les deux sens.

## 4. Chemins fiables

### GitHub → environnement local

Pour un dépôt **public** comme `AlexFCL/piano`, préférer un téléchargement HTTP direct du fichier brut depuis GitHub vers le container. Cette voie contourne le connecteur pour le transport des octets et évite le relais base64 par le contexte.

Le connecteur GitHub reste utile pour :
- vérifier le dépôt, la branche et le SHA ;
- trouver le chemin exact ;
- contrôler l'état Git.

Pour un dépôt privé, n'utiliser un transfert binaire que si l'outil retourne une vraie référence de fichier téléchargeable / matérialisable. Sinon, ne pas prétendre que le fichier a été rapatrié localement.

### Environnement local → GitHub

Avec les actions GitHub actuellement disponibles dans ce chat, il n'existe **pas de primitive native fiable** acceptant directement :
- un chemin `/mnt/data/...` ;
- un fichier local ;
- ou une référence de fichier du container.

`create_blob` n'accepte qu'une chaîne. Par conséquent, l'upload direct d'un lot de PNG depuis `/mnt/data` vers GitHub n'est pas considéré comme fiable par défaut.

## 5. Ce qu'il ne faut plus faire

- Ne pas annoncer « j'envoie les images » avant d'avoir confirmé qu'un vrai canal binaire direct existe.
- Ne pas encoder 24 PNG puis tenter de transporter leur base64 via les sorties d'outils.
- Ne pas considérer qu'un SHA GitHub signifie que le fichier existe aussi localement.
- Ne pas considérer qu'un fichier présent dans `/mnt/data` peut être lu automatiquement par le connecteur GitHub.
- Ne pas répéter une tentative identique après un échec de sérialisation/troncature.
- Ne pas qualifier une méthode de « validée » parce qu'un petit fichier isolé a éventuellement réussi une fois.

## 6. Procédure obligatoire avant toute demande binaire

Avant de commencer :

1. identifier le sens du transfert ;
2. identifier dans quel environnement se trouvent réellement les octets ;
3. vérifier si l'outil de destination accepte **un fichier/référence de fichier**, et pas seulement une chaîne ;
4. choisir un canal qui transporte réellement les octets sans passer par le contexte du modèle ;
5. si ce canal n'existe pas, le dire immédiatement avant mutation.

## 7. Application au projet piano

Pour les PNG de gammes :

- génération locale : container / `/mnt/data` ;
- état Git : connecteur GitHub ;
- téléchargement depuis GitHub public vers le container : HTTP brut possible ;
- upload des PNG locaux vers GitHub : **pas de pont binaire natif exposé par les actions GitHub actuelles**.

C'est cette séparation d'environnements — et non GitHub — qui explique les échecs récurrents observés lors des uploads/rapatriements d'images.
