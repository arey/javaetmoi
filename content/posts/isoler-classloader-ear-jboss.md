---
_edit_last: "1"
author: admin
categories:
  - retour-d'expérience
date: "2013-01-05T09:41:40+00:00"
thumbnail: /wp-content/uploads/2013/01/JBoss-ClassLoading-Scoped-Java2ParentDelegationOff-300x202.png
featureImage: /wp-content/uploads/2013/01/JBoss-ClassLoading-Scoped-Java2ParentDelegationOff-300x202.png
featureImageAlt: "@Copyright JBoss - Classe chargée en priorité depuis lEAR"
guid: http://javaetmoi.com/?p=520
parent_post_id: null
post_id: "520"
post_views_count: "8990"
summary: |-
  Lors de la **migration** d’une application d’un **serveur d’application** vers un autre, il est fréquent d’être confronté à des problématiques de **conflits de librairies**. C’est par exemple le cas lorsqu’une application initialement déployée sur un Websphere Application Server 6.1  doit migrer sur **JBoss 5.1 EAP** (version commerciale de JBoss AS).
  Pour rappel, WAS 6.1 implémente J2EE 1.4 et s’exécute donc sur Java 5. Quant à JBoss 5.1 EAP, il implémente la norme Java EE 5, embarque donc de nombreuses implémentations des standards tels que JPA 1, JSF 1.2 et JAX-WS 1, et tourne sur Java 6.
tags:
  - classloader
  - hibernate
  - javaee
  - jboss
  - jpa
  - maven
  - was
title: Isoler le classloader de son EAR sous JBoss
url: /2013/01/isoler-classloader-ear-jboss/

---
Lors de la **migration** d’une application d’un **serveur d’application** vers un autre, il est fréquent d’être confronté à des problématiques de **conflits de librairies**. C’est par exemple le cas lorsqu’une application initialement déployée sur un Websphere Application Server 6.1  doit migrer sur **JBoss 5.1 EAP** (version commerciale de JBoss AS).
Pour rappel, WAS 6.1 implémente J2EE 1.4 et s’exécute donc sur Java 5. Quant à JBoss 5.1 EAP, il implémente la norme Java EE 5, embarque donc de nombreuses implémentations des standards tels que JPA 1, JSF 1.2 et JAX-WS 1, et tourne sur Java 6.

Pour illustration, prenons une application s’appuyant sur Hibernate 3.6 pour sa couche de persistance et JAXB 2.2 pour le marshalling lors d’appel de web services.  Ces 2 librairies sont embarquées dans le répertoire lib de son EAR et ne posent pas de problèmes particuliers à WAS 6.1.
Par contre, sur JBoss 5.1 EAP, c’est un tout autre problème. En effet,  son  implémentation JPA repose sur la version 3.3 d'Hibernate. Qui plus est, JAXB 2.1 a été intégrée dans Java 6.
Si vous tentez de déployer une telle application sur un JBoss installé avec la configuration par défaut, il y’a de fortes chances que vous tombiez sur l’une ou l’autre des exceptions suivantes : _ClassCastException_, _NoSuchMethodException, IllegalAccessErrors_, _VerifyError._
A ce que j’ai compris en parcourant la documentation mais également déduis de mes tests, différents mécanismes permettent d’expliquer ces comportements :

1. Par défaut, lors du chargement d’une classe, le classloader de l’EAR va commencer par demander à son classloader parent (en l’occurrence celui de JBoss) de trouver la classe. Ainsi, c’est par exemple la classe Session d’Hibernate 3.3 qui sera chargée et non celle de la version 3.6 comme attendu. Il s’agit du comportement standard d’un classloader. Et c’est ce qu’on appelle communément le « j2se classloading compliance ». Sous WAS, cette stratégie de chargement peut être changée en paramétrant le classloader en PARENT\_LAST.
1. Les classes chargées par d’autres applications déployées sur la même instance de JBoss peuvent être partagées par votre application. Par exemple, la console d’admin JBoss admin-console.war embarque sa propre version de Richfaces et de Seam et peut, malgré elle, vous en faire bénéficier.

## _Solutions étudiées_

Pour mener à bien la migration, plusieurs pistes ont été étudiées :
**Solutions****Inconvénients****Avantages**1Downgrader les versions des frameworks pour utiliser celles embarquées dans JBoss 5.1Important travail de refactoring pour combler les fonctionnalités manquantes.
Bugs existants récupérés.Respect de la norme Java EE 5.
Support éditeur maximal.2Configurer sur mesure le répertoire d’installation de JBoss (ex : supprimer le support des EJB 3 et de JPA)Mutualisation du répertoire d’installation rendue caduque.
Main sur la production _._Un JBoss qui démarre plus vite.
Pas d’impact sur le code.3Isoler le déploiement de l’applicationLire la documentation JBoss.
Augmentation possible de la PermGen.Risque nul.
Simple configuration.
Configuration embarquée dans l’EAR.

## Configurer le classloader de l’application

{{< figure align="alignright" width=300 src="/wp-content/uploads/2013/01/JBoss-ClassLoading-Scoped-Java2ParentDelegationOff-300x202.png" alt="@Copyright JBoss - Classe chargée en priorité depuis l'EAR" caption="@Copyright JBoss - Classe chargée en priorité depuis l'EAR" >}}

Pour mettre en œuvre la solution n°3 concernant à « scoper » l’application, il est nécessaire de configurer le chargement des classes de JBoss . Une description détaillée de son fonctionnement est disponible sur la page [JBossClassLoadingUseCases](https://community.jboss.org/wiki/JBossClassLoadingUseCases) du wiki de JBoss.
Dans notre cas, La configuration des classes loaders nécessaire est **deployment scoped** et **Java2ParentDelegation** **désactivé**. Cette configuration est représentée par la figure ci-contre.

Cette configuration présente les 2 avantages suivants :

1. Les JARs embarqués dans l'EAR priment sur celles fournies par JBoss 5.1 et le JRE.
1. Chaque application déployée sur le même serveur possède son propre UnifiedLoaderRepository (ULR). Le chargement des classes est isolé et n'interfère pas. Elles sont également isolées du chargement des applications tierces (ex: jmx-console et admin-console).

La configuration du fichier **jboss-app.xml** à déposer dans le répertoire META-INF de l’EAR est décrite sur la page [ClassLoadingConfiguration](https://community.jboss.org/wiki/ClassLoadingConfiguration) du wiki JBoss. En voici un exemple :
Lors de la **migration** d’une application d’un **serveur d’application** vers un autre, il est fréquent d’être confronté à des problématiques de **conflits de librairies**. C’est par exemple le cas lorsqu’une application initialement déployée sur un Websphere Application Server 6.1  doit migrer sur **JBoss 5.1 EAP** (version commerciale de JBoss AS).
Pour rappel, WAS 6.1 implémente J2EE 1.4 et s’exécute donc sur Java 5. Quant à JBoss 5.1 EAP, il implémente la norme Java EE 5, embarque donc de nombreuses implémentations des standards tels que JPA 1, JSF 1.2 et JAX-WS 1, et tourne sur Java 6.<!--more-->

Pour illustration, prenons une application s’appuyant sur Hibernate 3.6 pour sa couche de persistance et JAXB 2.2 pour le marshalling lors d’appel de web services.  Ces 2 librairies sont embarquées dans le répertoire lib de son EAR et ne posent pas de problèmes particuliers à WAS 6.1.
Par contre, sur JBoss 5.1 EAP, c’est un tout autre problème. En effet,  son  implémentation JPA repose sur la version 3.3 d'Hibernate. Qui plus est, JAXB 2.1 a été intégrée dans Java 6.
Si vous tentez de déployer une telle application sur un JBoss installé avec la configuration par défaut, il y’a de fortes chances que vous tombiez sur l’une ou l’autre des exceptions suivantes : _ClassCastException_, _NoSuchMethodException, IllegalAccessErrors_, _VerifyError._
A ce que j’ai compris en parcourant la documentation mais également déduis de mes tests, différents mécanismes permettent d’expliquer ces comportements :

1. Par défaut, lors du chargement d’une classe, le classloader de l’EAR va commencer par demander à son classloader parent (en l’occurrence celui de JBoss) de trouver la classe. Ainsi, c’est par exemple la classe Session d’Hibernate 3.3 qui sera chargée et non celle de la version 3.6 comme attendu. Il s’agit du comportement standard d’un classloader. Et c’est ce qu’on appelle communément le « j2se classloading compliance ». Sous WAS, cette stratégie de chargement peut être changée en paramétrant le classloader en PARENT\_LAST.
1. Les classes chargées par d’autres applications déployées sur la même instance de JBoss peuvent être partagées par votre application. Par exemple, la console d’admin JBoss admin-console.war embarque sa propre version de Richfaces et de Seam et peut, malgré elle, vous en faire bénéficier.

## _Solutions étudiées_

Pour mener à bien la migration, plusieurs pistes ont été étudiées :
**Solutions****Inconvénients****Avantages**1Downgrader les versions des frameworks pour utiliser celles embarquées dans JBoss 5.1Important travail de refactoring pour combler les fonctionnalités manquantes.
Bugs existants récupérés.Respect de la norme Java EE 5.
Support éditeur maximal.2Configurer sur mesure le répertoire d’installation de JBoss (ex : supprimer le support des EJB 3 et de JPA)Mutualisation du répertoire d’installation rendue caduque.
Main sur la production _._Un JBoss qui démarre plus vite.
Pas d’impact sur le code.3Isoler le déploiement de l’applicationLire la documentation JBoss.
Augmentation possible de la PermGen.Risque nul.
Simple configuration.
Configuration embarquée dans l’EAR.

## Configurer le classloader de l’application

{{< figure align="alignright" width=300 src="/wp-content/uploads/2013/01/JBoss-ClassLoading-Scoped-Java2ParentDelegationOff-300x202.png" alt="@Copyright JBoss - Classe chargée en priorité depuis l'EAR" caption="@Copyright JBoss - Classe chargée en priorité depuis l'EAR" >}}

Pour mettre en œuvre la solution n°3 concernant à « scoper » l’application, il est nécessaire de configurer le chargement des classes de JBoss . Une description détaillée de son fonctionnement est disponible sur la page [JBossClassLoadingUseCases](https://community.jboss.org/wiki/JBossClassLoadingUseCases) du wiki de JBoss.
Dans notre cas, La configuration des classes loaders nécessaire est **deployment scoped** et **Java2ParentDelegation** **désactivé**. Cette configuration est représentée par la figure ci-contre.

Cette configuration présente les 2 avantages suivants :

1. Les JARs embarqués dans l'EAR priment sur celles fournies par JBoss 5.1 et le JRE.
1. Chaque application déployée sur le même serveur possède son propre UnifiedLoaderRepository (ULR). Le chargement des classes est isolé et n'interfère pas. Elles sont également isolées du chargement des applications tierces (ex: jmx-console et admin-console).

La configuration du fichier **jboss-app.xml** à déposer dans le répertoire META-INF de l’EAR est décrite sur la page [ClassLoadingConfiguration](https://community.jboss.org/wiki/ClassLoadingConfiguration) du wiki JBoss. En voici un exemple :
\[gist id="4451751"\]

## Configuration maven

Le plugin **maven-ear-plugin** permet de générer ce fichier jboss-app.xml :
\[gist id="4451788"\]

## Conclusion

Scoper l’EAR déployé sur JBoss vous laisse la possibilité de choisir la version des frameworks que vous souhaitez et de ne pas vous le laisser imposer. Vous pourrez ainsi utiliser Hibernate comme implémentation de JPA 2 (en mode embarqué avec le support offert par Spring), Hibernate Validator 4 comme implémentation de la JSR 303 Bean Validation ou même SLF4J 1.6 et Logback 1.0.9 pour gérer vos traces.
A des fins de debug, tout client JMX permet de consulter les classes disponibles dans l’UnifiedLoaderRepository.
Enfin, pour un réglage plus fin du classloader, et bien que je n’ai pas eu besoin d‘y recourir, une [configuration avancée du jboss-classloading.xml](http://java.dzone.com/articles/jboss-microcontainer-classloading) est a priori possible.

Références :

1. JBossClassLoadingUseCases : [https://community.jboss.org/wiki/JBossClassLoadingUseCases](https://community.jboss.org/wiki/JBossClassLoadingUseCases)
1. ClassLoadingConfiguration : [https://community.jboss.org/wiki/ClassLoadingConfiguration](https://community.jboss.org/wiki/ClassLoadingConfiguration)
1. A Look Inside JBoss Microcontainer's ClassLoading Layer : [http://java.dzone.com/articles/jboss-microcontainer-classloading](http://java.dzone.com/articles/jboss-microcontainer-classloading)
1. Demystifying the JBoss5 jboss-classloading.xml file  : [http://phytodata.wordpress.com/2010/10/21/demystifying-the-jboss5-jboss-classloading-xml-file/](http://phytodata.wordpress.com/2010/10/21/demystifying-the-jboss5-jboss-classloading-xml-file/)

## Configuration maven

Le plugin **maven-ear-plugin** permet de générer ce fichier jboss-app.xml :
Lors de la **migration** d’une application d’un **serveur d’application** vers un autre, il est fréquent d’être confronté à des problématiques de **conflits de librairies**. C’est par exemple le cas lorsqu’une application initialement déployée sur un Websphere Application Server 6.1  doit migrer sur **JBoss 5.1 EAP** (version commerciale de JBoss AS).
Pour rappel, WAS 6.1 implémente J2EE 1.4 et s’exécute donc sur Java 5. Quant à JBoss 5.1 EAP, il implémente la norme Java EE 5, embarque donc de nombreuses implémentations des standards tels que JPA 1, JSF 1.2 et JAX-WS 1, et tourne sur Java 6.<!--more-->

Pour illustration, prenons une application s’appuyant sur Hibernate 3.6 pour sa couche de persistance et JAXB 2.2 pour le marshalling lors d’appel de web services.  Ces 2 librairies sont embarquées dans le répertoire lib de son EAR et ne posent pas de problèmes particuliers à WAS 6.1.
Par contre, sur JBoss 5.1 EAP, c’est un tout autre problème. En effet,  son  implémentation JPA repose sur la version 3.3 d'Hibernate. Qui plus est, JAXB 2.1 a été intégrée dans Java 6.
Si vous tentez de déployer une telle application sur un JBoss installé avec la configuration par défaut, il y’a de fortes chances que vous tombiez sur l’une ou l’autre des exceptions suivantes : _ClassCastException_, _NoSuchMethodException, IllegalAccessErrors_, _VerifyError._
A ce que j’ai compris en parcourant la documentation mais également déduis de mes tests, différents mécanismes permettent d’expliquer ces comportements :

1. Par défaut, lors du chargement d’une classe, le classloader de l’EAR va commencer par demander à son classloader parent (en l’occurrence celui de JBoss) de trouver la classe. Ainsi, c’est par exemple la classe Session d’Hibernate 3.3 qui sera chargée et non celle de la version 3.6 comme attendu. Il s’agit du comportement standard d’un classloader. Et c’est ce qu’on appelle communément le « j2se classloading compliance ». Sous WAS, cette stratégie de chargement peut être changée en paramétrant le classloader en PARENT\_LAST.
1. Les classes chargées par d’autres applications déployées sur la même instance de JBoss peuvent être partagées par votre application. Par exemple, la console d’admin JBoss admin-console.war embarque sa propre version de Richfaces et de Seam et peut, malgré elle, vous en faire bénéficier.

## _Solutions étudiées_

Pour mener à bien la migration, plusieurs pistes ont été étudiées :
**Solutions****Inconvénients****Avantages**1Downgrader les versions des frameworks pour utiliser celles embarquées dans JBoss 5.1Important travail de refactoring pour combler les fonctionnalités manquantes.
Bugs existants récupérés.Respect de la norme Java EE 5.
Support éditeur maximal.2Configurer sur mesure le répertoire d’installation de JBoss (ex : supprimer le support des EJB 3 et de JPA)Mutualisation du répertoire d’installation rendue caduque.
Main sur la production _._Un JBoss qui démarre plus vite.
Pas d’impact sur le code.3Isoler le déploiement de l’applicationLire la documentation JBoss.
Augmentation possible de la PermGen.Risque nul.
Simple configuration.
Configuration embarquée dans l’EAR.

## Configurer le classloader de l’application

{{< figure align="alignright" width=300 src="/wp-content/uploads/2013/01/JBoss-ClassLoading-Scoped-Java2ParentDelegationOff-300x202.png" alt="@Copyright JBoss - Classe chargée en priorité depuis l'EAR" caption="@Copyright JBoss - Classe chargée en priorité depuis l'EAR" >}}

Pour mettre en œuvre la solution n°3 concernant à « scoper » l’application, il est nécessaire de configurer le chargement des classes de JBoss . Une description détaillée de son fonctionnement est disponible sur la page [JBossClassLoadingUseCases](https://community.jboss.org/wiki/JBossClassLoadingUseCases) du wiki de JBoss.
Dans notre cas, La configuration des classes loaders nécessaire est **deployment scoped** et **Java2ParentDelegation** **désactivé**. Cette configuration est représentée par la figure ci-contre.

Cette configuration présente les 2 avantages suivants :

1. Les JARs embarqués dans l'EAR priment sur celles fournies par JBoss 5.1 et le JRE.
1. Chaque application déployée sur le même serveur possède son propre UnifiedLoaderRepository (ULR). Le chargement des classes est isolé et n'interfère pas. Elles sont également isolées du chargement des applications tierces (ex: jmx-console et admin-console).

La configuration du fichier **jboss-app.xml** à déposer dans le répertoire META-INF de l’EAR est décrite sur la page [ClassLoadingConfiguration](https://community.jboss.org/wiki/ClassLoadingConfiguration) du wiki JBoss. En voici un exemple :
\[gist id="4451751"\]

## Configuration maven

Le plugin **maven-ear-plugin** permet de générer ce fichier jboss-app.xml :
\[gist id="4451788"\]

## Conclusion

Scoper l’EAR déployé sur JBoss vous laisse la possibilité de choisir la version des frameworks que vous souhaitez et de ne pas vous le laisser imposer. Vous pourrez ainsi utiliser Hibernate comme implémentation de JPA 2 (en mode embarqué avec le support offert par Spring), Hibernate Validator 4 comme implémentation de la JSR 303 Bean Validation ou même SLF4J 1.6 et Logback 1.0.9 pour gérer vos traces.
A des fins de debug, tout client JMX permet de consulter les classes disponibles dans l’UnifiedLoaderRepository.
Enfin, pour un réglage plus fin du classloader, et bien que je n’ai pas eu besoin d‘y recourir, une [configuration avancée du jboss-classloading.xml](http://java.dzone.com/articles/jboss-microcontainer-classloading) est a priori possible.

Références :

1. JBossClassLoadingUseCases : [https://community.jboss.org/wiki/JBossClassLoadingUseCases](https://community.jboss.org/wiki/JBossClassLoadingUseCases)
1. ClassLoadingConfiguration : [https://community.jboss.org/wiki/ClassLoadingConfiguration](https://community.jboss.org/wiki/ClassLoadingConfiguration)
1. A Look Inside JBoss Microcontainer's ClassLoading Layer : [http://java.dzone.com/articles/jboss-microcontainer-classloading](http://java.dzone.com/articles/jboss-microcontainer-classloading)
1. Demystifying the JBoss5 jboss-classloading.xml file  : [http://phytodata.wordpress.com/2010/10/21/demystifying-the-jboss5-jboss-classloading-xml-file/](http://phytodata.wordpress.com/2010/10/21/demystifying-the-jboss5-jboss-classloading-xml-file/)

## Conclusion

Scoper l’EAR déployé sur JBoss vous laisse la possibilité de choisir la version des frameworks que vous souhaitez et de ne pas vous le laisser imposer. Vous pourrez ainsi utiliser Hibernate comme implémentation de JPA 2 (en mode embarqué avec le support offert par Spring), Hibernate Validator 4 comme implémentation de la JSR 303 Bean Validation ou même SLF4J 1.6 et Logback 1.0.9 pour gérer vos traces.
A des fins de debug, tout client JMX permet de consulter les classes disponibles dans l’UnifiedLoaderRepository.
Enfin, pour un réglage plus fin du classloader, et bien que je n’ai pas eu besoin d‘y recourir, une [configuration avancée du jboss-classloading.xml](http://java.dzone.com/articles/jboss-microcontainer-classloading) est a priori possible.

Références :

1. JBossClassLoadingUseCases : [https://community.jboss.org/wiki/JBossClassLoadingUseCases](https://community.jboss.org/wiki/JBossClassLoadingUseCases)
1. ClassLoadingConfiguration : [https://community.jboss.org/wiki/ClassLoadingConfiguration](https://community.jboss.org/wiki/ClassLoadingConfiguration)
1. A Look Inside JBoss Microcontainer's ClassLoading Layer : [http://java.dzone.com/articles/jboss-microcontainer-classloading](http://java.dzone.com/articles/jboss-microcontainer-classloading)
1. Demystifying the JBoss5 jboss-classloading.xml file  : [http://phytodata.wordpress.com/2010/10/21/demystifying-the-jboss5-jboss-classloading-xml-file/](http://phytodata.wordpress.com/2010/10/21/demystifying-the-jboss5-jboss-classloading-xml-file/)
