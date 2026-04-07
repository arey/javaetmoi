---
_edit_last: "1"
author: admin
categories:
  - retour-d'expérience
date: "2013-08-01T18:13:55+00:00"
thumbnail: /wp-content/uploads/2013/07/git-logo.png
featureImage: /wp-content/uploads/2013/07/git-logo.png
featureImageAlt: "Logo du SCM GIT"
guid: http://javaetmoi.com/?p=735
parent_post_id: null
post_id: "735"
post_views_count: "21056"
summary: '[![Logo du SCM GIT](http://javaetmoi.com/wp-content/uploads/2013/07/git-logo-300x125.png)](http://javaetmoi.com/wp-content/uploads/2013/07/git-logo.png) Dans le cycle de vie d’une application, il arrive parfois qu’ **une branche prenne le pas sur une autre  branche** et qu’il soit nécessaire d’écraser la seconde par la première. Prenons l’exemple d’une application où, par convention, le master (ou le trunk sous SVN) est considéré comme la branche de développement (axée vers le futur) et que l’utilisation du système de branches soit habituellement consacrée aux branches de maintenance. Dans certaines circonstances (ex : nouveaux développements à commencer pour la version N+2, migration technique à réaliser …), une branche peut prendre le dessus du master. Afin de retrouver la convention d’origine, une **recopie de la branche sur le master** va, à termes, être nécessaire. Que ce soit avec Git ou git-svn, nous allons voir comment **[Git](http://git-scm.com/)** peut nous y aider en **quelques lignes de commande**.'
tags:
  - git
title: Ecraser une branche par une autre avec Git
url: /2013/08/ecraser-une-branche-par-une-autre-avec-git/

---
[![Logo du SCM GIT](/wp-content/uploads/2013/07/git-logo.png)](/wp-content/uploads/2013/07/git-logo.png) Dans le cycle de vie d’une application, il arrive parfois qu’ **une branche prenne le pas sur une autre  branche** et qu’il soit nécessaire d’écraser la seconde par la première. Prenons l’exemple d’une application où, par convention, le master (ou le trunk sous SVN) est considéré comme la branche de développement (axée vers le futur) et que l’utilisation du système de branches soit habituellement consacrée aux branches de maintenance. Dans certaines circonstances (ex : nouveaux développements à commencer pour la version N+2, migration technique à réaliser …), une branche peut prendre le dessus du master. Afin de retrouver la convention d’origine, une **recopie de la branche sur le master** va, à termes, être nécessaire. Que ce soit avec Git ou git-svn, nous allons voir comment **[Git](http://git-scm.com/)** peut nous y aider en **quelques lignes de commande**.

## Mise en scène

L’ **historique de commits** ci-dessous illustre les explications qui suivront :
[![Historique des commits réalisés avec Git](/wp-content/uploads/2013/07/2013-08-ecraser-branche-avec-git-svn-1.png)](/wp-content/uploads/2013/07/2013-08-ecraser-branche-avec-git-svn-1.png)

Cet historique des commits commence par la branche _master_ sur laquelle les fonctionnalités A et B ont été commitées. La branche _maBranche_ est alors créée à partir du commit de la fonctionnalité B. Un premier merge no fast-forward est créé pour récupérer la fonctionnalité E de _master_ dans _maBranche_ : le commit de merge « _Merge branch ‘master’ into maBranche_ » est créé.

A partir de là, les nouvelles fonctionnalités F, G et H sont développées sur _maBranche_. Ne pouvant attendre la fin des développements de la fonctionnalité G qui résoudrait proprement le problème rencontré par les utilisateurs, est créé sur le _master_ un contournement permettant d’y palier temporairement. Ce _Hotfix_ est déployé en production. N’ayant aucun intérêt dans les prochaines versions de l’application, **ce _Hotfix_ ne doit être en aucun cas mergé sur _maBranche_**. Une fois les développements de la fonctionnalité H terminés et déployés en production, l’équipe décide de faire revenir sur le _master_ les développements de _maBranche_.
Les **2 derniers commits** de l’historique mettent en œuvre cette opération.

## Commandes

Voici les 4 lignes de commandes à exécuter pour réaliser cet écrasement de branche :

1. Se placer sur la branche à conserver
   **git checkout maBranche**
1. Demander une fusion avec la **stratégie** **_ours_** (attention, ceci est différent d'un merge avec stratégie _recursive_ et l’ _option ours_) qui va uniquement conserver le contenu de la branche actuelle. En effet, l'option **_-s ours_** indique à Git de fusionner la branche source dans la branche cible mais sans aucunement modifier la branche cible. Cette stratégie est habituellement utilisée pour ne pas reporter un commit d’une branche de maintenance sur le master.
   **git merge -s ours master -m "Merge avec stratégie ours"**
1. Repasser sur la branche master
   **git checkout master**
1. Demander une fusion de la branche _maBranche_ vers le _master_ tout en conservant 2 branches distinctes (un _fast-forward_ aurait été réalisé puisque que le dernier commit n’est autre que notre fusion de la commande n°2).
   **git merge --no-ff maBranche**

Sortie console sur notre exemple de la commande Git n°4 :
[![Log du git merge --no-ff maBranche](/wp-content/uploads/2013/07/2013-08-ecraser-branche-avec-git-svn-2.png)](/wp-content/uploads/2013/07/2013-08-ecraser-branche-avec-git-svn-2.png)

Comme attendu, le fichier _Hotfix.txt_ ayant été ajouté lors du commit _Hotfix_ est supprimé du _master_. Si, dans un autre exemple, le commit _Hotfix_ avait modifié une ligne du fichier _FeatureE.txt_, un _revert_ de cette modification aurait alors été effectué.

## Conclusion

Cet article explique comment **Git permet d’écraser le contenu de la branche A par une branche B** lorsque la branche B a pris le pas sur la branche A et qu’aucune des modifications présente dans le branche A n'a besoin d'être conservée (tout a été préalablement fusionné, reporté par [cherry-pick](http://think-like-a-git.net/sections/rebase-from-the-ground-up/cherry-picking-explained.html), copié à la main ou volontairement ignoré car à ne pas reporter).
Cerise sur le gâteau : ces opérations sont **applicables entre 2 branches SVN** par le biais du [bridge git-svn](http://git-scm.com/book/fr/Git-et-les-autres-syst%C3%A8mes-Git-et-Subversion).
