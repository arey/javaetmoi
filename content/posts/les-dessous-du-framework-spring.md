---
_edit_last: "1"
author: admin
categories:
  - spring
date: "2015-12-07T17:50:46+00:00"
guid: http://javaetmoi.com/?p=1493
parent_post_id: null
post_id: "1493"
post_views_count: "3384"
summary: |-
  Chaque jour, de nombreux développeurs utilisent le **framework Spring** pour **l’injection de dépendances** et la **gestion des transactions**. Majeures, ces 2 fonctionnalités ne nécessitent pas un gros effort d’apprentissage. Pour autant, leurs mises en œuvre par le framework est complexe. Par curiosité intellectuelle, mais également afin d’éviter certains pièges et de profiter pleinement des capacités de Spring, il est intéressant de comprendre les **mécanismes internes du framework** qu’on utilise au quotidien : **cycle de vie** d’un bean, **proxy**, **intercepteur**, **post-processeur**, **fabrique** de beans, **hiérarchie de contextes**, **portée** …
  Les slides de cette présentation ont pour objectif de vous les introduire.

  **[Les dessous du framework spring](//fr.slideshare.net/AntoineRey/les-dessous-du-framework-spring "Les dessous du framework spring")** par **[Antoine Rey](//www.slideshare.net/AntoineRey)**
tags:
  - spring-framework
title: Les dessous du Framework Spring
url: /2015/12/les-dessous-du-framework-spring/

---
Chaque jour, de nombreux développeurs utilisent le **framework Spring** pour **l’injection de dépendances** et la **gestion des transactions**. Majeures, ces 2 fonctionnalités ne nécessitent pas un gros effort d’apprentissage. Pour autant, leurs mises en œuvre par le framework est complexe. Par curiosité intellectuelle, mais également afin d’éviter certains pièges et de profiter pleinement des capacités de Spring, il est intéressant de comprendre les **mécanismes internes du framework** qu’on utilise au quotidien : **cycle de vie** d’un bean, **proxy**, **intercepteur**, **post-processeur**, **fabrique** de beans, **hiérarchie de contextes**, **portée** …
Les slides de cette présentation ont pour objectif de vous les introduire.

**[Les dessous du framework spring](//fr.slideshare.net/AntoineRey/les-dessous-du-framework-spring "Les dessous du framework spring")** par **[Antoine Rey](//www.slideshare.net/AntoineRey)**

Sujets abordés :

- Post-processeurs et fabriques de beans Spring
- Intercepteur transactionnel et pièges de l’annotation @Transactional
- Lever des ambiguïtés lors de l’injection de beans
- Injection de beans de portées différentes
- Hiérarchie de contextes Spring
- Créer sa propre annotation
- Architecture pluggable
- Accès au contexte Spring
