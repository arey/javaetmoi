---
_edit_last: "1"
author: admin
categories:
  - retour-d'expérience
date: "2016-06-10T05:32:14+00:00"
guid: http://javaetmoi.com/?p=1615
parent_post_id: null
post_id: "1615"
post_views_count: "4617"
tags:
  - java
title: Les Streams Java 8 par l'exemple
url: /2016/06/les-streams-java-8-par-lexemple/

---
Bien que **Java 8** soit sorti il y’a 2 ans, tous les développeurs n’ont pas eu encore la chance de pouvoir utiliser, en entreprise, tous les concepts issus de la **programmation fonctionnelle** et qui ont été introduits dans cette version majeure : expressions lambda, interfaces fonctionnelles, méthodes par défaut, Optional, références de méthode, Streams …
Pourtant, Java 8 est à nos portes : des projets de migration de serveur d’application se terminent, les socles d’entreprise se mettent à jour, des frameworks exploitent ces nouveautés (ex : JUnit 5) ... Et on va enfin pouvoir exploiter à bon escient toutes ces nouvelles fonctionnalités. Mais avant cela, une mise à niveau est indispensable. Et c’est dans cet objectif que j’ai récemment initié mes collègues aux **Streams**.
A partir d’un jeux de données réduit (une liste de 3 clients), **j’ai implémenté quelques règles de gestion à la fois en Java 7 avec des boucles et en Java 8 avec des Streams**, histoire de leur montrer la différence.

\[slideshare id=62288571&doc=13-14-lesstreamsjava8-160523061803\]
