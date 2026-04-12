---
_edit_last: "1"
author: admin
categories:
  - retour-d'expérience
date: "2013-03-19T19:48:16+00:00"
thumbnail: wp-content/uploads/2013/03/2013-03-promotion-continue-avec-git-svn.png
featureImage: wp-content/uploads/2013/03/2013-03-promotion-continue-avec-git-svn.png
featureImageAlt: "Workflow de promotion en continue du trunk vers la branche"
guid: http://javaetmoi.com/?p=626
parent_post_id: null
post_id: "626"
post_views_count: "18324"
summary: |-
  Dans le cadre d’un important **chantier** de **migration technique** d’une **application**, j’ai eu l’occasion de pratiquer ce que j’appellerais la **promotion de code en continue**.

  Pour resituer le contexte, ce chantier dura plus de 6 mois. Entre le début et la fin de la migration, l’application a été livrée plusieurs fois en production, embarquant à chaque fois de nombreuses évolutions fonctionnelles. Nous avons donc dû nous organiser pour migrer l’application sans pénaliser l’avancement du reste de l’équipe.
  Les changements techniques étant bien trop transverses à l’application, la stratégie de [Feature Toggle](http://martinfowler.com/bliki/FeatureToggle.html) ne pouvait s’appliquer. Nous nous sommes donc dirigés vers une technique assimilable au [Feature Branch](http://martinfowler.com/bliki/FeatureBranch.html) ; notre migration technique n’étant rien d’autre qu’une feature comme une autre.  Logiquement, une branche dédiée à la migration a été créée.

  Notre stratégie fut de **merger régulièrement dans cette branche le code issu de la branche de développement**. Une fois la migration terminée, la branche de migration a été à son tour mergée dans la branche de développement.

  ![Workflow de promotion en continue du trunk vers la branche](wp-content/uploads/2013/03/2013-03-promotion-continue-avec-git-svn.png)
tags:
  - git
  - svn
title: Promotion de code en continue avec git-svn
url: /2013/03/promotion-code-continue-merge-git-svn/

---
Dans le cadre d’un important **chantier** de **migration technique** d’une **application**, j’ai eu l’occasion de pratiquer ce que j’appellerais la **promotion de code en continue**.

Pour resituer le contexte, ce chantier dura plus de 6 mois. Entre le début et la fin de la migration, l’application a été livrée plusieurs fois en production, embarquant à chaque fois de nombreuses évolutions fonctionnelles. Nous avons donc dû nous organiser pour migrer l’application sans pénaliser l’avancement du reste de l’équipe.
Les changements techniques étant bien trop transverses à l’application, la stratégie de [Feature Toggle](http://martinfowler.com/bliki/FeatureToggle.html) ne pouvait s’appliquer. Nous nous sommes donc dirigés vers une technique assimilable au [Feature Branch](http://martinfowler.com/bliki/FeatureBranch.html) ; notre migration technique n’étant rien d’autre qu’une feature comme une autre.  Logiquement, une branche dédiée à la migration a été créée.

Notre stratégie fut de **merger régulièrement dans cette branche le code issu de la branche de développement**. Une fois la migration terminée, la branche de migration a été à son tour mergée dans la branche de développement.

[![Workflow de promotion en continue du trunk vers la branche](wp-content/uploads/2013/03/2013-03-promotion-continue-avec-git-svn.png)](wp-content/uploads/2013/03/2013-03-promotion-continue-avec-git-svn.png)

## Git svn à la rescousse

Comme c’est encore le cas dans de nombreuses entreprises, SVN est l’unique outil de versioning proposé dans l’usine de développement. La plateforme d’intégration continue s’appuie dessus et, installés sur une infrastructure de production, les repos SVN présentent l’intérêt d’être archivés quotidiennement.
C’est là que la **[passerelle git-svn](http://git-scm.com/book/fr/Git-et-les-autres-syst%C3%A8mes-Git-et-Subversion)** intervient en mettant à la portée des utilisateurs SVN la **puissance** et la **facilité des merges  apportées par Git**. Git-svn permet en effet de maintenir à jour la branche svn avec le trunk.
Cette facilité a un prix : une vigilance accrue et une grande **rigueur** lors des **opérations en ligne de commande**. En effet, une erreur d’inattention et vous pouvez vous retrouver à commiter le code de la branche de migration sur le trunk SVN. C’est pourquoi, au cours de la migration, le mode opératoire  présenté ci-dessus a été scrupuleusement suivi.

## Mode opératoire

Les instructions suivantes permettent de récupérer dans la branche de migration SVN, les développements commités sur le trunk SVN.
L’exemple illustrant ces instructions concerne une application Java.  Maven est l’outil de build utilisé pour compiler, exécuter les tests unitaires et vérifier ainsi l’état du merge.
Les 2 branches Git manipulées sont associées aux branches SVN suivantes :

1. master (git) => trunk (svn)
1. local-feature-migration (branche locale git)=> feature-migration (branche distance svn)

Depuis la précédente opération de merge, nous partons du principe que des commits ont pu ou non avoir eu lieu dans le trunk.  De la même manière, des modifications ont pu ou non avoir été commitées et poussées dans la branche de migration.

Avant de commencer, s’assurer que toutes les modifications sont commitées dans le repo SVN et l’intégration continue est au vert, à la fois sur le trunk et la branche.

Enfin, cette opération de merge est à réaliser de préférence depuis le même repo git local. Ce dernier possède  l’historique des merges réalisés précédemment. Il faut en effet garder à l’esprit que, une fois commité dans SVN, le commit ancêtre entre le trunk et la branche est perdu. Même avec git-svn, un autre développeur ne pourrait le récupérer.

**1. Faire pointer le master au niveau du trunk**

```sh
git checkout master
git svn rebase
```

 **2\. Effectuer un checkout de la branche locale (et non distante)**

```sh
git checkout local-feature-migration
```

Avec le pont git-svn, les merges ne fonctionnent que dans un sens. Il faut donc veiller à se placer sur la branche sur laquelle on veut créer le commit de merge.

**3\. Merger le master vers la branche locale**

```sh
git merge --no-ff master
```

Remarque : l'option _--no-ff_ (no fast-forward) est très importante : elle force git à créer un commit dit de "merge". Lorsque la branche ou le master n'ont pas bougé, cela évite que la référence HEAD de la branche _local-feature-migration_ soit déplacée pour pointer sur le dernier commit de la branche master. En résumé, cela permet de conserver 2 branches distinctes, comme dans SVN. La conséquence désastreuse de cet oubli est qu'un _svn dcommit_ de la branche _local-feature-migration_ serait pourrait être réalisé sur le _trunk_.

**4\. Régler les éventuels conflits**

```sh
git mergetool
git rebase --continue
```

Utiliser son outil de merge préféré, par exemple kdiff3 ou TortoiseMerge.

**5\. Exécuter le build maven**

```sh
mvn clean install
```

Permet de s’assurer que le code compile et que les tests unitaires passent.

**6\. Commiter dans SVN**

```sh
git svn dcommit
```

Sous peine de corrompre votre repo git, attention à ne pas effectuer de _git svn rebase_ entre le _merge_ et le _svn dcommit_.

Clonage d’un repo SVN existant, création d’une branche Git et liaison avec une branche SVN distante sont expliqués dans la [documentation de git-svn](http://git-scm.com/book/fr/Git-et-les-autres-syst%C3%A8mes-Git-et-Subversion).

## Bénéfices

Voici une liste non exhaustive des bénéfices apportés par cette méthode de travail :

1. Le report des commits au fil de l'eau permet de régler au plus tôt d'éventuels problèmes de merge. L’effet tunnel est évité. Les conflits sont résolus plus rapidement car les modifications sont encore toutes fraiches dans la tête des développeurs (du trunk comme de la branche).
1. Cette stratégie permet de déployer en dual-run les 2 versions de l'application, sans perte de fonctionnalités puisqu’elles sont iso-fonctionnelles (à la migration technique prêt). La comparaison de comportements et les bascules en sont facilitées.

## Conclusion

Après quelques essais, la fréquence retenue pour réaliser ces opérations de merge fut d’une fois par semaine.
Au final, ce n’est pas une application, mais dix qui ont été migrées à l’aide de cette stratégie. Au total, 2 millions de ligne de code ont ainsi été promues.
Bien entendu, ce procédé peut être appliqué avec d’autres technologies que maven et Java.
