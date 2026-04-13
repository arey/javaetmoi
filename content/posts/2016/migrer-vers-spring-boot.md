---
_edit_last: "1"
author: admin
categories:
  - spring
date: "2016-08-29T16:05:29+00:00"
toc: true
thumbnail: wp-content/uploads/2016/07/screenshot-petclinic.jpg
featureImage: wp-content/uploads/2016/07/screenshot-petclinic.jpg
featureImageAlt: "screenshot-petclinic"
guid: http://javaetmoi.com/?p=1623
parent_post_id: null
post_id: "1623"
post_views_count: "14586"
summary: |-
  Cela fait un an que je contribue activement à la maintenance de l’application **Spring Petclinic**. Développée initialement par les créateurs du framework Spring, Juergen Hoeller et Rob Harrop, cette application démo a évolué au fur et à mesure des montées de version du framework.  Elle est passée d’une approche full XML, à une approche mixte annotations + XML. Une branche est également disponible pour la configuration Java.
  Récemment, nous avons mis à disposition une branche basée sur **Spring Boot 1.4.0**. L’objectif de ce billet est de vous expliquer quels ont été les impacts d’une telle migration.

  ![screenshot-petclinic](wp-content/uploads/2016/07/screenshot-petclinic.jpg)
tags:
  - spring-boot
title: Migrer vers Spring Boot
url: /2016/08/migrer-vers-spring-boot/

---
Cela fait un an que je contribue activement à la maintenance de l’application **Spring Petclinic**. Développée initialement par les créateurs du framework Spring, Juergen Hoeller et Rob Harrop, cette application démo a évolué au fur et à mesure des montées de version du framework.  Elle est passée d’une approche full XML, à une approche mixte annotations + XML. Une branche est également disponible pour la configuration Java.
Récemment, nous avons mis à disposition une branche basée sur **Spring Boot 1.4.0**. L’objectif de ce billet est de vous expliquer quels ont été les impacts d’une telle migration.

![screenshot-petclinic](wp-content/uploads/2016/07/screenshot-petclinic.jpg)

## Stack technique existante

Techniquement, la [branche master](https://github.com/spring-projects/spring-petclinic/) à partir de laquelle a été créée la [**branche springboot**](https://github.com/spring-projects/spring-petclinic/tree/springboot) est relativement à jour. Elle s’appuie sur le BOM 2.0.7 de la plateforme Spring.IO.
Spring MVC 4.2, JSP, Dandelion, jQuery 2 et Bootstrap 3.3 sont utilisés pour la couche de présentation.
La couche de persistance propose 3 implémentations différentes : Spring Data JPA 1.9, JPA/Hibernate 4.3 et JDBC. Un profile Spring permet de choisir quelle implémentation utiliser au démarrage de l’application.

Le build est principalement construit autour de Maven. Bower est utilisé pour télécharger les frameworks JavaScript / CSS. Les feuilles de styles sont écrites en LESS. Un plugin maven les convertit en CSS.

L’application est compatible Java 7 et 8. Sur mon poste de dév, je la déploie sur Tomcat 7, et Tomcat 8.. A noter que sous Jetty, les pages JSP ne s’affichent pas suite à un [bug de Dandelion](https://github.com/dandelion/dandelion/issues/113).

## Cible

Le but de la migration est de conserver l’application iso-fonctionnelle et de garder dans la mesure du possible les mêmes frameworks. Par contre, nous avons fait le choix de ne retenir qu’une seule des 3 implémentations de la couche de persistance, à savoir Spring Data JPA. Garder les 3 technologies aurait complexifié inutilement la configuration Spring.

Afin de coller davantage à l’esprit Spring Boot, nous sommes revenus aux webjars et avons délaissé l’usage de Bower. Ce billet n’abordera pas ce changement.

Non pris en compte par Spring Data JPA, l’aspect [_CallMonitoringAspect_](https://github.com/spring-projects/spring-petclinic/blob/482eeb1c217789b5d772f5c15c3ab7aa89caf279/src/main/java/org/springframework/samples/petclinic/util/CallMonitoringAspect.java) n’a pas été conservé.

## Configuration Maven

La migration vers Spring Boot a simplifié le [**pom.xml**](https://github.com/spring-projects/spring-petclinic/blob/springboot/pom.xml) qui est passé de 461 à 357 lignes XML.
Voici les changements apportés :

1. Ajout d’un POM Parent : org.springframework.boot:spring-boot-starter-parent
1. Suppression du Bill Of Materials io.spring.platform:platform-bom
1. Remplacement des dépendances de frameworks par les « Spring Boot Starter » équivalents : spring-boot-starter-actuator, spring-boot-starter-cache, spring-boot-starter-data-jpa, spring-boot-starter-test et spring-boot-starter-web
1. Déclaration du plugin Maven spring-boot-maven-plugin
1. Suppression de la déclaration des plugins maven-war-plugin, maven-assembly-plugin et tomcat7-maven-plugin

## Configuration Spring

L’automatisation de la configuration Spring est mise en avant par les concepteurs de Spring Boot. Nous nous attendions donc à obtenir une configuration la plus minimaliste possible.
Le passage à Spring Boot nous a contraint à délaisser le web.xml au profit de l’interface _ServletContainerInitializer_ introduite par l’API Servlet 3.0.

La configuration Spring Boot est écrite en Java : 76 lignes de code Java sont venues remplacer 248 lignes de configuration Spring XML et 99 lignes du web.xml.

Voici le détail des changements :

1. Création d’une classe principale [**_PetClinicApplication_**](https://github.com/spring-projects/spring-petclinic/blob/springboot/src/main/java/org/springframework/samples/petclinic/PetClinicApplication.java) implémentant la classe abstraite _SpringBootServletInitializer_ et annotée avec l’annotation @SpringBootApplication
1. Centralisation de la configuration de la servlet et des filtres Dandelion dans la classe de configuration [_DandelionConfig_](https://github.com/spring-projects/spring-petclinic/blob/springboot/src/main/java/org/springframework/samples/petclinic/config/DandelionConfig.java)
1. Introduction de la classe de configuration [_CacheConfig_](https://github.com/spring-projects/spring-petclinic/blob/springboot/src/main/java/org/springframework/samples/petclinic/config/CacheConfig.java) permettant de n’activer ehcache qu’en production
1. Suppression du web.xml
1. Suppression de 5 fichiers de configuration Spring

## Paramétrage

Initialement répartie dans différents fichiers, le paramétrage applicatif a été centralisé dans le fichier [**application.properties**](https://github.com/spring-projects/spring-petclinic/blob/springboot/src/main/resources/application.properties).
Les fichiers data-access.properties et logback.xml ont été supprimés.
Par convention, le fichier de configuration ehcache.xml a été déplacé à la racine du classpath.

## Simplification des tests

Au niveau des dépendances, le starter **spring-boot-starter-test** tire tous les frameworks de tests utilisés par Petclinic :  **JUnit**, **Spring Test**, **AssertJ**, **Mockito**, Json Path et Hamcrest.
Un peu comme Unitils en son temps, Spring Boot facilite l’utilisation conjointe de ces différents frameworks. Et la version 1.4.0 de Spring Boot améliore encore leur intégration.

Ainsi, l’annotation `@MockBean` permet de créer un mock avec Mockito, de l’enregistrer au sein du contexte applicatif Spring et de l’injecter dans votre classe de tests unitaires. Nul besoin désormais de faire appel explicitement à la méthode _Mockito::mock()._

En fonction de la couche applicative à laquelle la classe testée appartient, la configuration Spring du test associé peut être auto-détectée. Ainsi, pour la couche web Spring MVC, l’annotation `@WebMvcTest` détecte tous les beans annotés avec @Controller, @ControllerAdvice et @JsonComponent puis configure l’instance de MockMvc. La classe de test _[OwnerControllerTests](https://github.com/spring-projects/spring-petclinic/blob/springboot/src/test/java/org/springframework/samples/petclinic/web/OwnerControllerTests.java)_ la montre en action.

## Autres changements

D’autres changements mineurs ont été nécessaires :

- Le contrôleur Spring MVC [_WelcomeController_](https://github.com/spring-projects/spring-petclinic/blob/springboot/src/main/java/org/springframework/samples/petclinic/web/WelcomeController.java) a été ajouté. Il a pour rôle d’afficher la page d’accueil de l’application.
- Le [_PetTypeFormatter_](https://github.com/spring-projects/spring-petclinic/blob/springboot/src/main/java/org/springframework/samples/petclinic/web/PetTypeFormatter.java) s’est vu transformé en bean Spring (ajout de l’annotation @Component).
- Le fichier [**txt**](https://github.com/spring-projects/spring-petclinic/blob/springboot/src/main/resources/banner.txt) a été ajouté afin de personnaliser le logo Ascii-art affiché lors du démarrage de l’application
- Suite à un problème avec Dandelion, les inclusions de JSP ont été remplacées par des tags JSP.

## Conclusion

Le portage vers Spring Boot n’aura demandé que quelques heures de développement. Au final, la configuration Spring est simplifiée à l’extrême. Et mis à part la configuration Maven, Petclinic ne contient a plus une seule ligne de XML.
En bonus, l’application s’est automatiquement vu enrichie d’une API de management accessible à la fois en REST et en JMX.
Petclinic est packagé sous forme de war auto-exécutable. Une limitation du support des pages JSP par Spring Boot fait qu’il n’est pas (encore ?) possible de le jarjariser.
