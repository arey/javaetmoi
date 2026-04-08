---
_edit_last: "1"
author: admin
categories:
  - spring
date: "2015-02-02T07:16:08+00:00"
guid: http://javaetmoi.com/?p=1304
parent_post_id: null
post_id: "1304"
post_views_count: "577640"
summary: |-
  Pour créer vos IHM web en Java, vous n’avez que l’embarras du choix : Vaadin, JSF, GWT, Spring MVC, Tapestry …

  Pour accéder aux données, à chacun ses préférences : Hibernate, JPA 2, iBatis, Spring JDBC, Spring Data …

  En matière de web services, il n’y a qu’à choisir : CXF, JAX-WS, JAX-RS, Spring WS, Restlet …

  Mais pour écrire vos traitements par lot ? java.io ? Soyons fou : commons-io. Pas très sexy …
  la JSR-352 Java Batch de JEE 7 ? Optez pour l’original.

  Alors franchissez le pas et venez découvrir Spring Batch au cours d’un workshop basé sur un cas d’utilisation concret.
tags:
  - spring-batch
title: Etudes de cas Spring Batch
url: /2015/02/worskshop-etudes-de-cas-spring-batch/

---
Pour créer vos IHM web en Java, vous n’avez que l’embarras du choix : Vaadin, JSF, GWT, Spring MVC, Tapestry …

Pour accéder aux données, à chacun ses préférences : Hibernate, JPA 2, iBatis, Spring JDBC, Spring Data …

En matière de web services, il n’y a qu’à choisir : CXF, JAX-WS, JAX-RS, Spring WS, Restlet …

Mais pour écrire vos traitements par lot ? java.io ? Soyons fou : commons-io. Pas très sexy …
la JSR-352 Java Batch de JEE 7 ? Optez pour l’original.

Alors franchissez le pas et venez découvrir Spring Batch au cours d’un workshop basé sur un cas d’utilisation concret.

Sommaire de la présentation :

1. **Introduction**
1. **Présentation de l’étude de cas**
   1. Périmètre fonctionnel
   1. Origine du projet de migration
   1. Objectifs du projet
1. **Mise en œuvre**
   1. Décomposition du batch en une seule étape
   1. Vocable Spring Batch
   1. Diagramme de séquence de traitement d’un chunk
   1. Configuration d'un Job et d’un Step
   1. Reader Hibernate
   1. Quelques implémentations de reader disponibles
   1. Déclaration et implémentation d’un Item Processor
   1. Configuration des writers
   1. Quelques implémentations de Writers disponibles
   1. Extrait du diagramme de dépendance des beans Spring
   1. Gestion des transactions
   1. Gestion des erreurs
   1. Exécution du batch
1. **Démo**
1. **Pour aller plus loin**
1. **Conclusion**
   1. Retours sur la migration vers Spring Batch
   1. Spring Batch en 3 mots
