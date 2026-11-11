---
_edit_last: "1"
author: Antoine Rey
categories:
  - retour-d'expérience
date: "2013-01-05T09:41:40+00:00"
toc: true
thumbnail: /logo/logo-jboss.svg
usePageBundles: true
guid: http://javaetmoi.com/?p=520
parent_post_id: null
post_id: "520"
post_views_count: "8990"
summary: |-
  Lors de la **migration** d’une application d’un **serveur d’application** vers un autre, il est fréquent d’être confronté à des problématiques de **conflits de librairies**. C’est par exemple le cas lorsqu’une application initialement déployée sur un Websphere Application Server 6.1  doit migrer sur **JBoss 5.1 EAP** (version commerciale de JBoss AS).
  Pour rappel, WAS 6.1 implémente J2EE 1.4 et s’exécute donc sur Java 5. Quant à JBoss 5.1 EAP, il implémente la norme Java EE 5, embarque donc de nombreuses implémentations des standards tels que JPA 1, JSF 1.2 et JAX-WS 1, et tourne sur Java 6.

  ![@Copyright JBoss - Classe chargée en priorité depuis lEAR](/2013/01/isoler-classloader-ear-jboss/JBoss-ClassLoading-Scoped-Java2ParentDelegationOff-300x202.png)
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
![Logo JBoss:right](/logo/logo-jboss.svg)Lors de la **migration** d’une application d’un **serveur d’application** vers un autre, il est fréquent d’être confronté à des problématiques de **conflits de librairies**. C’est par exemple le cas lorsqu’une application initialement déployée sur un Websphere Application Server 6.1  doit migrer sur **JBoss 5.1 EAP** (version commerciale de JBoss AS).
Pour rappel, WAS 6.1 implémente J2EE 1.4 et s’exécute donc sur Java 5. Quant à JBoss 5.1 EAP, il implémente la norme Java EE 5, embarque donc de nombreuses implémentations des standards tels que JPA 1, JSF 1.2 et JAX-WS 1, et tourne sur Java 6.<!--more-->

Pour illustration, prenons une application s’appuyant sur Hibernate 3.6 pour sa couche de persistance et JAXB 2.2 pour le marshalling lors d’appel de web services.  Ces 2 librairies sont embarquées dans le répertoire lib de son EAR et ne posent pas de problèmes particuliers à WAS 6.1.
Par contre, sur JBoss 5.1 EAP, c’est un tout autre problème. En effet,  son  implémentation JPA repose sur la version 3.3 d'Hibernate. Qui plus est, JAXB 2.1 a été intégrée dans Java 6.
Si vous tentez de déployer une telle application sur un JBoss installé avec la configuration par défaut, il y’a de fortes chances que vous tombiez sur l’une ou l’autre des exceptions suivantes : `ClassCastException`, `NoSuchMethodException`, `IllegalAccessErrors`, `VerifyError`.
A ce que j’ai compris en parcourant la documentation mais également déduis de mes tests, différents mécanismes permettent d’expliquer ces comportements :

1. Par défaut, lors du chargement d’une classe, le classloader de l’EAR va commencer par demander à son classloader parent (en l’occurrence celui de JBoss) de trouver la classe. Ainsi, c’est par exemple la classe Session d’Hibernate 3.3 qui sera chargée et non celle de la version 3.6 comme attendu. Il s’agit du comportement standard d’un classloader. Et c’est ce qu’on appelle communément le « j2se classloading compliance ». Sous WAS, cette stratégie de chargement peut être changée en paramétrant le classloader en `PARENT_LAST`.
1. Les classes chargées par d’autres applications déployées sur la même instance de JBoss peuvent être partagées par votre application. Par exemple, la console d’admin JBoss `admin-console.war` embarque sa propre version de Richfaces et de Seam et peut, malgré elle, vous en faire bénéficier.

## _Solutions étudiées_

Pour mener à bien la migration, plusieurs pistes ont été étudiées :

| N° | Solutions | Inconvénients | Avantages |
|----|-----------|---------------|-----------|
| 1 | Downgrader les versions des frameworks pour utiliser celles embarquées dans JBoss 5.1 | Important travail de refactoring pour combler les fonctionnalités manquantes.<br/>Bugs existants récupérés. | Respect de la norme Java EE 5.<br/>Support éditeur maximal. |
| 2 | Configurer sur mesure le répertoire d’installation de JBoss (ex : supprimer le support des EJB 3 et de JPA) | Mutualisation du répertoire d’installation rendue caduque.<br/>Main sur la production. | Un JBoss qui démarre plus vite.<br/>Pas d’impact sur le code. |
| 3 | Isoler le déploiement de l’application | Lire la documentation JBoss.<br/>Augmentation possible de la PermGen. | Risque nul.<br/>Simple configuration.<br/>Configuration embarquée dans l’EAR. |

## Configurer le classloader de l’application

![@Copyright JBoss - Classe chargée en priorité depuis l'EAR:right](JBoss-ClassLoading-Scoped-Java2ParentDelegationOff-300x202.png)

Pour mettre en œuvre la solution n°3 concernant à « scoper » l’application, il est nécessaire de configurer le chargement des classes de JBoss . Une description détaillée de son fonctionnement est disponible sur la page [JBossClassLoadingUseCases](https://community.jboss.org/wiki/JBossClassLoadingUseCases) du wiki de JBoss.
Dans notre cas, La configuration des classes loaders nécessaire est **deployment scoped** et `Java2ParentDelegation` **désactivé**. Cette configuration est représentée par la figure ci-contre.

Cette configuration présente les 2 avantages suivants :

1. Les JARs embarqués dans l'EAR priment sur celles fournies par JBoss 5.1 et le JRE.
1. Chaque application déployée sur le même serveur possède son propre UnifiedLoaderRepository (ULR). Le chargement des classes est isolé et n'interfère pas. Elles sont également isolées du chargement des applications tierces (ex: jmx-console et admin-console).

La configuration du fichier `jboss-app.xml` à déposer dans le répertoire META-INF de l’EAR est décrite sur la page [ClassLoadingConfiguration](https://community.jboss.org/wiki/ClassLoadingConfiguration) du wiki JBoss. En voici un exemple :

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE jboss-app PUBLIC
"-//JBoss//DTD Java EE Application 5.0//EN"
"http://www.jboss.org/j2ee/dtd/jboss-app_5_0.dtd">
<jboss-app>
  <loader-repository>com.javaetmoi:archive=monapplication-ear
      <loader-repository-config>java2ParentDelegation=false</loader-repository-config>
  </loader-repository>
</jboss-app>
```

## Configuration maven

Le plugin `maven-ear-plugin` permet de générer ce fichier `jboss-app.xml` :

```xml
<!-- Generation du classPath dans le Manifest de l'EAR, paramétrage du classloader -->
<!-- et recopie centralisée des JARs des WARs dans le répertoire lib -->
<plugin>
  <artifactId>maven-ear-plugin</artifactId>
  <configuration>
    <version>5</version>
    <defaultJavaBundleDir>lib/</defaultJavaBundleDir>
    <applicationXml>${project.build.directory}/application.xml</applicationXml>
    <archive>
      <manifest>
        <addClasspath>true</addClasspath>
      </manifest>
    </archive>
    <!-- Génère le fichier jboss-app.xml se trouvant dans le sous-répertoire META-INF de l'EAR -->
    <jboss>
      <version>5</version>
      <!-- Fait en sorte que que l'application ait son propre UnifiedLoaderRepository (ULR) -->
      <!-- Le déploiement de l'EAR est dit "scoped" -->
      <loader-repository>com.javaetmoi:archive=${project.artifactId}</loader-repository>
      <!-- Le flag Java2ParentDelegation est désactivé afin que les classes soient en priorité
         chargées à partir des libs de l'EAR -->
      <loader-repository-config>java2ParentDelegation=false</loader-repository-config>
    </jboss>
  </configuration>
</plugin>
```

## Conclusion

Scoper l’EAR déployé sur JBoss vous laisse la possibilité de choisir la version des frameworks que vous souhaitez et de ne pas vous le laisser imposer. Vous pourrez ainsi utiliser Hibernate comme implémentation de JPA 2 (en mode embarqué avec le support offert par Spring), Hibernate Validator 4 comme implémentation de la JSR 303 Bean Validation ou même SLF4J 1.6 et Logback 1.0.9 pour gérer vos traces.
A des fins de debug, tout client JMX permet de consulter les classes disponibles dans l’UnifiedLoaderRepository.
Enfin, pour un réglage plus fin du classloader, et bien que je n’ai pas eu besoin d‘y recourir, une [configuration avancée du jboss-classloading.xml](http://java.dzone.com/articles/jboss-microcontainer-classloading) est a priori possible.

Références :

1. JBossClassLoadingUseCases : [https://community.jboss.org/wiki/JBossClassLoadingUseCases](https://community.jboss.org/wiki/JBossClassLoadingUseCases)
1. ClassLoadingConfiguration : [https://community.jboss.org/wiki/ClassLoadingConfiguration](https://community.jboss.org/wiki/ClassLoadingConfiguration)
1. A Look Inside JBoss Microcontainer's ClassLoading Layer : [http://java.dzone.com/articles/jboss-microcontainer-classloading](http://java.dzone.com/articles/jboss-microcontainer-classloading)
1. Demystifying the JBoss5 jboss-classloading.xml file  : [http://phytodata.wordpress.com/2010/10/21/demystifying-the-jboss5-jboss-classloading-xml-file/](http://phytodata.wordpress.com/2010/10/21/demystifying-the-jboss5-jboss-classloading-xml-file/)
