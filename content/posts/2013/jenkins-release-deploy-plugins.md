---
_edit_last: "1"
author: admin
categories:
  - maven
date: "2013-07-16T16:37:26+00:00"
thumbnail: wp-content/uploads/2013/07/jenkins-build-history.png
featureImage: wp-content/uploads/2013/07/jenkins-build-history.png
featureImageAlt: "jenkins-build-history"
guid: http://javaetmoi.com/?p=721
parent_post_id: null
post_id: "721"
post_views_count: "9806"
summary: |-
  [![jenkins-build-history](http://javaetmoi.com/wp-content/uploads/2013/07/jenkins-build-history-300x220.png)](http://javaetmoi.com/wp-content/uploads/2013/07/jenkins-build-history.png) A Devoxx France, lorsqu’Axel Fontaine vante les mérites du **Continuous Delivery** et que Ludovic Cinquin affirme que **Facebook est mis en production 2 fois par jour**, avouez que cela a de quoi vous laisser rêveur ? En attendant de travailler un jour dans des structures ayant compris que des **livraisons fréquentes** et **automatisées** permettent de gagner en fiabilité, en agilité et de développer leur business, vous n’avez d’autres choix que de vous approprier les processus établis où vous intervenez et de les améliorer à votre niveau.

  Dans les grands comptes où je suis intervenu, la mouvance **Devops** prônant de tels processus n’avait pas encore percé. Quelques **outils** sont bien mis en place. Mais pour autant, **MOE** et **exploitation** sont 2 **équipes** bien **distinctes**. L’exploitation peut elle-même être scindée en 2 : production et intégration (hors-prod). C’est précisément dans ce contexte que s’inscrit  cet article. Il montre comment utiliser un **serveur d’intégration continue** pour releaser puis **déployer une application** sur les environnements autorisés.

  ![jenkins-build-history](wp-content/uploads/2013/07/jenkins-build-history.png)
tags:
  - devops
  - jenkins
  - maven
  - plugin
title: Orchestrez vos déploiements avec Jenkins
url: /2013/07/jenkins-release-deploy-plugins/

---
[![jenkins-build-history](wp-content/uploads/2013/07/jenkins-build-history.png)](wp-content/uploads/2013/07/jenkins-build-history.png) A Devoxx France, lorsqu’Axel Fontaine vante les mérites du **Continuous Delivery** et que Ludovic Cinquin affirme que **Facebook est mis en production 2 fois par jour**, avouez que cela a de quoi vous laisser rêveur ? En attendant de travailler un jour dans des structures ayant compris que des **livraisons fréquentes** et **automatisées** permettent de gagner en fiabilité, en agilité et de développer leur business, vous n’avez d’autres choix que de vous approprier les processus établis où vous intervenez et de les améliorer à votre niveau.

Dans les grands comptes où je suis intervenu, la mouvance **Devops** prônant de tels processus n’avait pas encore percé. Quelques **outils** sont bien mis en place. Mais pour autant, **MOE** et **exploitation** sont 2 **équipes** bien **distinctes**. L’exploitation peut elle-même être scindée en 2 : production et intégration (hors-prod). C’est précisément dans ce contexte que s’inscrit  cet article. Il montre comment utiliser un **serveur d’intégration continue** pour releaser puis **déployer une application** sur les environnements autorisés.

## CONTEXTE DE MISE EN ŒUVRE

Prenons un exemple concret qui servira de trame à ce billet. Supposons que l’exploitation met à disposition de la MOE des **scripts shell** permettant de livrer leur application sur le serveur d’intégration et de préparer un package qui sera utilisé lors des livraisons sur les environnements suivants.
Le **package de livraison** comprend :

1. Le ou les **binaires de l’application** : **EAR**, WAR ou même JAR pour les batchs
1. La **configuration applicative par environnement**

Ces fichiers constituent les livrables. On pourrait imaginer y ajouter des scripts SQL de mise à jour du schéma de la base et/ou des données.

Les scripts shell permettent de copier les  binaires et la configuration sur le serveur d’application, de redémarrer le serveur d’application puis de contrôler l’état de l’application une fois celle-ci démarrée. Au format XML ou .properties, les fichiers de configuration sont déposés dans le **classpath** du serveur afin d’être accessibles par l’application.

Dans notre exemple, la MOE a la main mise sur l’environnement d’intégration. Elle peut y déployer  son application à volonté. A tout moment (ex : à la fin d’une itération ou d’un sprint), elle peut décider de créer le package qui permettra à la MOA de recetter l’application. Une fois déposé dans le SAS de recette, le package de livraison est déployé sur l’environnement de recette, et cela automatiquement 2 fois par jour. Leur installation en pré-production et en production est réalisée à la demande de la MOE par les équipes d’intégration puis de production.

Au quotidien, les développeurs Java utilisent [Jenkins](http://jenkins-ci.org/) comme plateforme d’intégration continue. Ils l’utilisent pour récupérer le code depuis SVN, le compiler, exécuter les tests unitaires, lancer l’analyse qualimétrique ou bien encore dérouler les tests fonctionnels. Est configuré un job Jenkins de build par branche de l’application.

Les livraisons en intégration sont réalisées manuellement par commandes SFTP et SSH. Les binaires sont récupérés du repository maven d’Entreprise [Nexus](http://www.sonatype.org/nexus/). Au préalable, le [plugin release pour maven](http://maven.apache.org/maven-release/maven-release-plugin/) leur aura permis de construire les livrables et de le publier dans Nexus via la commande suivante :
_mvn perform:prepare perform:release_

Voyons à présent comment Jenkins va permettre d’améliorer ce process et de fluidifier les livraisons.

## RELEASE DEPUIS JENKINS

Afin de garantir le périmètre d’une **version d’un livrable** et la répétabilité de sa construction, le **processus de release** est encouragé dès lors qu’un livrable est susceptible de pouvoir être déployé jusqu’en production. Ce processus vérifie entre autre que l’application ne dépend que d’artefacts immuables, dont la version est figée. Simple mais fastidieuse, gourmande en ressources matérielles, cette action peut être facilitée par le [plugin M2 Release](https://wiki.jenkins-ci.org/display/JENKINS/M2+Release+Plugin) de Jenkins.

Son installation ne pose aucune difficulté. Un compte générique permettant d’accéder au SCM  de l’entreprise peut y être configuré afin que tous les projets puissent par la suite en bénéficier. Le plugin maven release utilise ce compte pour récupérer le code source, commiter des changements de version dans les pom.xml et créer un tag.

Pour qu’un plan de build puisse être releasé depuis Jenkins, la case **Maven release build** doit être cochée :
![jenkins-maven-release-build-config](wp-content/uploads/2013/07/jenkins-maven-release-build-config.png)

Au besoin, les commandes maven peuvent être complétées avec un goal ou un **profil maven** particulier, pour par exemple publier les **sources** et la **javadoc** dans le repo maven d’entreprise ou bien encore exécuter des **tests d’intégration** en complément des tests unitaires.

A la suite d’un build, Jenkins offre la possibilité d’ **archiver les artefacts construits** et qui se trouvent encore dans son espace de travail. Cette fonctionnalité est particulièrement utile lors d’une release. Les **livrables** peuvent ainsi être **archivés** et rattachés au build pour un usage ultérieur :

![jenkins-archiver-artefacts](wp-content/uploads/2013/07/jenkins-archiver-artefacts.png)

Le pattern de sélection des fichiers à archiver est basé sur la **syntaxe ant** (ex : \*\*/\*.ear pour archiver tous les fichiers EAR du workspace). Dans l’exemple précédent, l’EAR de l’application web, l’archive zip contenant les binaires du batch de l’application ainsi que tous les fichiers de configuration (.xml, .properties …) sont archivés à chaque fin de build.

Une fois configuré, le processus de release se fait à la demande sur **simple clic**. Cette action peut être réalisée par le chef de projet ou le responsable de l’intégration, une fois que ce dernier a vérifié que toutes les fiches Jira de la version à releaser sont clôturées et que le code est commité dans SVN.

Voici la **procédure** à suivre pour **déclencher manuellement la release** :

1. Sélectionner le build Jenkins correspondant à la branche de la version de l’application à releaser (exemple : MyBank-2.0.x ou MyBank-trunk)
1. Cliquer sur le **menu Peform Maven Release**
   **![jenkins-maven-release-build-launch](wp-content/uploads/2013/07/jenkins-maven-release-build-launch.png)**
1. Renseigner le formulaire de release en suivant les **règles de versionning** définies sur votre application
   ![jenkins-release-build](wp-content/uploads/2013/07/jenkins-release-build.png)
1. Cliquer sur le **bouton Schedule Maven Release Build**
1. Le plugin release de maven prend la main et effectue les tâches suivantes :
   1. Création du tag de la release dans SVN
   1. Déploiement dans Nexus les artefacts construits (EAR)
   1. Commits SVN mettant à jour la version des pom.xml
1. En cas de succès, dans l’historique des builds, l’icône ![jenkins-icon-package](wp-content/uploads/2013/07/jenkins-icon-package-1.png)    doit apparaître à côté du build releasé. La version de la release (ex : 3.0.5) est accessible en tant qu’info-bulle :
   ![jenkins-package-version](wp-content/uploads/2013/07/jenkins-package-version.png)
1. Une sélection du build permet de consulter les livrables archivés
   ![jenkins-artefacts](wp-content/uploads/2013/07/jenkins-artefacts.jpg)
1. Cette version être prête à être déployée sur un serveur d’application

## DÉPLOIEMENT DES BUILDS PAR PROMOTION

Ainsi, la version de l’application web releasée précédemment est désormais prête à être **déployée** sur l’ **environnement d’intégration** pour des tests plus poussés côté MOE. Une fois le procès-verbal (PV) d’intégration validé, cette version pourra être ensuite déployée sur l’environnement de **recette** afin que la MOA lance sa campagne de tests d’acceptation. Le PV de recette signé, cette même version sera prête à être **livrée en production**. Ce workflow décrit le scénario le plus optimiste dans lequel la première version de l’application ne contient aucune anomalie. En pratique, plusieurs allers retours avec l’équipe de développement auront très certainement lieu, ce qui entraînera plusieurs cycles de release et de re-livraison de l’application.
Voici un scénario déjà plus réaliste :

1. _Fin des développements de la V2 de l’application_ _à_ _release version 2.0.0_ _à_ _déploiement en intégration_ _à_ _bugs remontés par la MOE_
1. _Corrections_ _à_ _Release version 2.0.1_ _à_ _déploiement en intégration_ _à_ _PV d’intégration_ _à_ _déploiement en recette_ _à_ _bugs remontés par la MOA_
1. _Corrections_ _à_ _Release version 2.0.2_ _à_ _déploiement en intégration_ _à_ _déploiement en recette_ _à_ _PV de recette fonctionnelle_ _à_ _déploiement en pré-production_ _à_ _PV de recette technique_ _à_ _déploiement en production_

La promotion d’une version de l’application vers un environnement en amont de la chaîne porte un nom : la **promotion de builds**. Et au même titre que la gestion des release, le serveur d’intégration continue Jenkins permet de la piloter. Pour se faire, l’installation du [plugin Promoted Builds](https://wiki.jenkins-ci.org/display/JENKINS/Promoted+Builds+Plugin) est pré-requise. Le build de l’application doit ensuite être configuré en sélectionnant autant de fois la case **_Promote builds when_** que de promotions seront possibles. Dans notre exemple, la promotion vers l’environnement d’intégration sera appelée « Deploy Integration » et la promotion vers l’environnement de recette sera nommée « Deploy UAT ».
![jenkins-promotion-integration-criteria](wp-content/uploads/2013/07/jenkins-promotion-integration-criteria.png)

Afin de pouvoir les différencier visuellement, une icône de couleur différente peut être associée à chacune des promotions (exemple : ![jenkins-icon-star-gold](wp-content/uploads/2013/07/jenkins-icon-star-gold-1.png) pour l’intégration et ![jenkins-icon-star-green](wp-content/uploads/2013/07/jenkins-icon-star-green-1.png) pour la recette). Jenkins est paramétré pour que la promotion soit activée manuellement par l’utilisateur. Une alternative aurait par exemple pu consister à promouvoir automatiquement en intégration la version d’une application suite au succès de ses build nocturnes des tests (ex : [Fitness](http://fitnesse.org/), [Selenium](http://docs.seleniumhq.org/)).

Lorsqu’un build est promu, des actions peuvent être déclenchées séquentiellement. Plusieurs actions sont mises à disposition nativement par Jenkins. Des plugins permettent de les enrichir. Voici quelques exemples d’actions possibles :

- Exécuter une ligne de commande batch Windows ou Linux
- Envoyer une notification par mail ou par XMPP
- Créer une fiche Jira
- Lancer une commande maven
- Copier des artefacts sur un serveur via SSH
- Supprimer le workspace Jenkins courant

Dans notre contexte, la **copie par SSH des artefacts** sur le serveur de déploiement de l’entreprise nous intéresse particulièrement. Apportée par le [plugin Publish Over SSH](https://wiki.jenkins-ci.org/display/JENKINS/Publish+Over+SSH+Plugin), cette action permet en complément d’exécuter une série de commandes sur le serveur distant une fois les artefacts copiés.
La figure suivante illustre la configuration de la recopie d’un EAR dans un répertoire dédié du serveur de déploiement puis l’exécution de 3 commandes permettant d’installer l’EAR, d’arrêter le serveur d’application puis de le redémarrer.
![jenkins-promotion-integration-action](wp-content/uploads/2013/07/jenkins-promotion-integration-action.png)

En amont de cette action, le transfert de la configuration peut être configuré de la même manière.
Dans la configuration proposée, l’EAR et les fichiers de configuration sont récupérés depuis l’archive des artefacts du build promu. Une alternative consisterait à récupérer le numéro de version de la release puis à utiliser l’ [API REST du serveur Nexus](https://repository.sonatype.org/nexus-core-documentation-plugin/core/docs/index.html) et la commande _wget_ pour récupérer le livrable dont les _groupId_, _artefactId_ et _packaging_ sont connus. Cette configuration pourrait s’appuyer sur le plugin [Jenkins Remote SSH](https://wiki.jenkins-ci.org/display/JENKINS/SSH+plugin).

Une fois configuré, il est possible de **promouvoir un build** et de **déployer l’application sur l’environnement de son choix**, qu’il s’agisse du build d’une version SNAPSHOT ou d’une RELEASE. D’après l’historique des builds ci-dessous, le build #2451 correspond à une  version releasée de l’application qui a été déployée en intégration. Le build #2455 correspond à une version releasée qui a été déployée en intégration et en recette.

![jenkins-build-history](wp-content/uploads/2013/07/jenkins-build-history-1.png)
Particulièrement souple, la promotion de build permet de livrer sur le même environnement des versions d’applications hébergées sur des branches différentes (trunk/master vs branche de maintenance). Elle permet également de livrer en un clic une version précédente pour, par exemple, vérifier si l’anomalie constatée est ou non une régression.

## CONCLUSION

Cet article nous aura permis de découvrir une utilisation moins courante d’un serveur d’intégration continue. Ne se limitant plus à l’étape de développements et de tests, **Jenkins permet de gérer le cycle de vie des releases d’une application ainsi que leur déploiement**.

Les possibilités offertes par Jenkins sont variées. Dans un autre contexte, il pourrait tout à fait être envisagé de substituer la promotion manuelle par une **promotion automatiquement** déclenchée par un autre build ou par un commit dans votre SCM (Git, SVN). Nous aurions très bien pu également découper notre build monolithique en plusieurs builds spécialisés : job de build, job de packaging, job de tests et job de déploiement. Cette **chaîne de builds** est rendue possible par la [configuration d’un pipeline de jobs](http://jenkins-le-guide-complet.batmat.cloudbees.net/html/sect-build-pipelines.html).

Enfin, le déploiement sur le serveur d’applications fut assuré ici par de simples scripts shell pilotant les scripts natifs du serveur d’application. Lorsque l’entreprise dispose d’un outil dédié à cette tâche tel [Serena Release Manager](http://www.serena.com/index.php/fr/products/serena-release-manager/benefits/), l’utilisation du plugin Jenkins [Serena Deploy](https://wiki.jenkins-ci.org/display/JENKINS/Serena+Deploy+Plugin) permet de pousser l’EAR et la configuration dans le repository SRA. Sur le même principe, tout fournisseur de PAAS dispose généralement d’un plugin Jenkins permettant de déployer une application  dans le Cloud ([CloudBees](https://wiki.jenkins-ci.org/display/JENKINS/Cloudbees+Deployer+Plugin), [OpenShift](https://github.com/openshift/jenkins-cloud-plugin), [Heroku](https://github.com/heroku/heroku-jenkins-plugin), [Cloud Foundry](http://blog.cloudfoundry.com/2011/09/22/rapid-cloud-foundry-deployments-with-maven/)…).
