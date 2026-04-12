---
_edit_last: "1"
author: admin
categories:
  - maven
date: "2016-09-06T15:58:15+00:00"
thumbnail: wp-content/uploads/2016/09/merge1.png
featureImage: wp-content/uploads/2016/09/merge1.png
featureImageAlt: "merge1"
guid: http://javaetmoi.com/?p=1630
parent_post_id: null
post_id: "1630"
post_views_count: "10012"
summary: |-
  L’utilisation conjointe de **Maven** pour réaliser des release et de **git-flow** peut s’avérer laborieuse.
  En effet, lorsque vous travaillez avec des branches (quel que soit le SCM), une bonne pratique veut que chaque branche possède son propre numéro de version. Afin d’éviter des collisions de nommage, cette pratique devient indispensable lorsque vous utilisez un serveur d’intégration continue pour publier les artefacts construits dans un repo Maven.
  Une fois une branche crée à partir d’une autre, chaque branche vit sa vie. Des releases Maven peuvent être réalisées de part et d’autre. Là où cela devient tendu, c’est lorsque vous devez reporter les commits d’une branche vers une autre. **Des conflits de merge sur le numéro de version Maven apparaissent alors inévitablement**. Lorsque votre application multi-modules comporte 15 pom.xml, c’est 15 conflits qu’il va falloir gérer manuellement. Il est effectivement risqué de conserver aveuglément la version du pom.xml local ou distant, car d’autres changements (et vrais conflits) peuvent se produire dans d’autres sections du pom.xml.

  Comme cas d’études, prenons l’exemple du repo Git helloworld :![merge1](http://javaetmoi.com/wp-content/uploads/2016/09/merge1.png)

  ![merge1](wp-content/uploads/2016/09/merge1.png)
tags:
  - git
  - maven
title: Faire cohabiter merge Git et release Maven
url: /2016/09/merge-git-et-release-maven/

---
L’utilisation conjointe de **Maven** pour réaliser des release et de **git-flow** peut s’avérer laborieuse.
En effet, lorsque vous travaillez avec des branches (quel que soit le SCM), une bonne pratique veut que chaque branche possède son propre numéro de version. Afin d’éviter des collisions de nommage, cette pratique devient indispensable lorsque vous utilisez un serveur d’intégration continue pour publier les artefacts construits dans un repo Maven.
Une fois une branche crée à partir d’une autre, chaque branche vit sa vie. Des releases Maven peuvent être réalisées de part et d’autre. Là où cela devient tendu, c’est lorsque vous devez reporter les commits d’une branche vers une autre. **Des conflits de merge sur le numéro de version Maven apparaissent alors inévitablement**. Lorsque votre application multi-modules comporte 15 pom.xml, c’est 15 conflits qu’il va falloir gérer manuellement. Il est effectivement risqué de conserver aveuglément la version du pom.xml local ou distant, car d’autres changements (et vrais conflits) peuvent se produire dans d’autres sections du pom.xml.

Comme cas d’études, prenons l’exemple du repo Git helloworld :![merge1](wp-content/uploads/2016/09/merge1.png)

Une application HelloWorld construite avec Maven a été releasée avec Maven en version 1.0.0 sur la branche **develop**. La prochaine version renseignée sur develop est 1.1.0-SNAPSHOT.
Une branche de maintenance **release/1.0.x** a ensuite été créée à partir du tag pointant sur le commit _« \[maven-release-plugin\] prepare release helloworld-1.0.0 »._ Une faute d’orthographe a été corrigée. Afin de la livrer en production rapidement, une version 1.0.1 a été réalisée avec Maven.
Cette correction doit désormais être reportée sur la branche develop. Entre temps, 2 commits ont été réalisés sur celle-ci, dont l’un touchant au pom.xml.
**Quelle solution adopter pour effectuer ce report ?**

Une première solution consiste à utiliser un **cherry-pick** du commit _« Fix spelling »._ Pour rappel, cherry-pick permet de reporter commit par commit les différences entre branche. Le risque est d’oublier un commit. Et cette solution peut devenir laborieuse si beaucoup de commits séparent les 2 branches.

Une seconde solution consiste à **merger** la branche release/1.0.x dans la branche develop.
Apparaît alors le conflit sur le numéro de version du pom.xml évoqué en introduction :

```sh
git merge release/1.0.x
Auto-merging src/main/java/com/compagny/HelloWorld.java
Auto-merging pom.xml
CONFLICT (content): Merge conflict in pom.xml
Automatic merge failed; fix conflicts and then commit the result.

git diff
diff --cc pom.xml
index b43c671,01257f6..0000000
--- a/pom.xml
+++ b/pom.xml
@@@ -6,9 -6,9 +6,13 @@@

      <groupId>com.mycompagny</groupId>
      <artifactId>helloworld</artifactId>
++<<<<<<< HEAD
 +    <version>1.1.0-SNAPSHOT</version>
++=======
+     <version>1.0.2-SNAPSHOT</version>
++>>>>>>> release/1.0.x

 -    <description>Hello World application</description>
 +    <description>Git merge demonstration</description>
```

Le conflit doit être résolu manuellement : la version 1.1.0-SNAPSHOT de la branche develop est à conserver.

Une solution permettant d’éviter de résoudre ce genre de conflits consiste à **utiliser un script que va utiliser Git pour merger 2 fichiers pom.xml**. C’est précisément l’objectif du driver de merge [**mergepom.py**](https://github.com/ralfth/pom-merge-driver/blob/master/mergepom.py) écrit en **Python** et que vous pouvez récupérer sur le repo GitHub [**pom-merge-driver**](https://github.com/ralfth/pom-merge-driver).
L’utilisation de ce script sous **Linux** et **Mac** est décrite dans le [README.md](https://github.com/ralfth/pom-merge-driver/blob/master/README.md).
Sur **Windows**, il est nécessaire de faire quelques adaptations :

- [Télécharger et installer Python (la version portable est suffisante)](https://www.python.org/downloads/)
- Dans le script mergepom.py, supprimer la ligne d’en-tête #! /usr/bin/env python
- Dans le fichier .gitconfig, ajouter le chemin vers python.exe :

```sh
[merge "pommerge"]
        name = A custom merge driver for Maven's pom.xml
        driver = '/C/dev/python/python.exe' C:/dev/git/mergepom.py %O %A %B
```

Afin de laisser la liberté aux autres développeurs d’utiliser ce script ou non, j’ai ajouté le fichier **attributes** dans le répertoire **.git/info** de mon repo local :

```default
pom.xml merge=pommerge
```

Remarque : alternativement, on peut également ajouter cette  ligne dans le fichier .gitattributes situé dans le répertoire racine du repo Git. Tous les développeurs de l'application en profitent alors.

On relance la commande de merge. Cette fois-ci, le script détecte un conflit sur le numéro de version du pom.xml et décide de garder celui de la branche courante, à savoir 1.1.0-SNAPHSOT :

```sh
git merge release/1.0.x
Merging pom version 1.0.2-SNAPSHOT into develop. Keeping version 1.1.0-SNAPSHOT
Auto-merging src/main/java/com/compagny/HelloWorld.java
Auto-merging pom.xml
Merge made by the 'recursive' strategy.
 pom.xml                                    | 2 +-
 src/main/java/com/compagny/HelloWorld.java | 2 +-
 2 files changed, 2 insertions(+), 2 deletions(-)
```

![merge2](wp-content/uploads/2016/09/merge2.png)

Le script Python respecte le workflow git-flow. De ce fait, les merge dans le master des branches de release et de hotfix conservent le numéro de version de ces dernières.

Comme moi, j’espère que l’existence de ce driver de merge Git vous simplifiera vos merges. Ne prenant en compte que les fichiers pom.xml encodé en UTF-8, j’ai fait une [demande d’évolution](https://github.com/ralfth/pom-merge-driver/issues/2). En attendant, vous pouvez changer l’encodage en dur dans le script ou bien, encore mieux, soumettre une pull request.

Enfin, sachez que d'autres drivers de merge Git existent. [pomutils](https://github.com/cecom/pomutils) est écrit en Java. Si vous en avez testé, n'hésitez pas à laisser un feedback.
