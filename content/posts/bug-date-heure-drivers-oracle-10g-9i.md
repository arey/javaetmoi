---
_edit_last: "1"
author: admin
categories:
  - retour-d'expérience
date: "2013-01-19T18:14:11+00:00"
guid: http://javaetmoi.com/?p=564
parent_post_id: null
post_id: "564"
post_views_count: "6392"
summary: |-
  Récemment, je suis tombé sur un **bug** lié à l’utilisation d’une **version de driver** **JDBC pour Oracle** plus récente que la version de la base Oracle attaquée en SQL via JDBC.

  # Les symptômes

  Dans notre contexte applicatif, la date et l’heure des données lues en base sont utilisées pour détecter des conflits de version, d’une manière similaire au versioning Hibernate. Concrètement, cela nous permet d’éviter qu’une donnée traitée par batch quotidien écrase une donnée plus fraiche provenant d’un système tiers. Ce mécanisme permet notamment d’exécuter un batch sans interruption de service de l’application web associée. Le bug que je vais vous décrire nous a été révélé tardivement. Sous certaines conditions,  nous avons en effet constaté que le batch ne rattrapait jamais des données. C’est **comme si l’heure n’était jamais prise en compte** **dans le code Java**.
tags:
  - bug
  - jdbc
  - oracle
title: 'Oracle : dis-moi quelle heure est-il ?'
url: /2013/01/bug-date-heure-drivers-oracle-10g-9i/

---
Récemment, je suis tombé sur un **bug** lié à l’utilisation d’une **version de driver** **JDBC pour Oracle** plus récente que la version de la base Oracle attaquée en SQL via JDBC.

# Les symptômes

Dans notre contexte applicatif, la date et l’heure des données lues en base sont utilisées pour détecter des conflits de version, d’une manière similaire au versioning Hibernate. Concrètement, cela nous permet d’éviter qu’une donnée traitée par batch quotidien écrase une donnée plus fraiche provenant d’un système tiers. Ce mécanisme permet notamment d’exécuter un batch sans interruption de service de l’application web associée. Le bug que je vais vous décrire nous a été révélé tardivement. Sous certaines conditions,  nous avons en effet constaté que le batch ne rattrapait jamais des données. C’est **comme si l’heure n’était jamais prise en compte** **dans le code Java**.

# Lecture de la colonne DATE

Dans la base de données Oracle 9i interrogées, date et heure des données sont stockées dans une colonne de type DATE. Aucun doute sur un éventuel problème d’insertion des données, Toad nous confirme que l’heure est bel et bien présente. L’hypothèse d’un problème de lecture de l’heure a été confirmée en debuggant le batch, et plus particulièrement le code Java chargé de parcourir le _ResultSet_ ramenée par une requête SQL. Voici le résultat des différents tests effectués :

```java
String type = resultSet.getMetaData().getColumnTypeName(1);  // "DATE"
Object res = resultSet.getObject("lastupdate");      // 2013-01-18
res = resultSet.getDate("lastupdate");               // 2013-01-18
res = resultSet.getTimestamp("lastupdate");          // 2013-01-18 19:35:20.0
```

La norme SQL précise que le type temporel DATE ne contient pas d’informations sur l’heure. La classe _java.sql.Date_ nous le rappelle. Le type temporel TIMESTAMP matérialisé par la classe _java.sql.Timestamp_ permet quant à lui de stocker date, heure et nanosecondes. En forçant l’appel à la méthode _getTimestanp()_, on obtient le résultat escompté. L’heure stockée en base est bien remontée lors de l’exécution de la requête. Je me serais donc attendu à ce que les meta-données JDBC soit de type TIMESTAMP à la place de DATE et que la méthode getObject() utilisée dans le code applicatif manipule des _java.sql.Timestamp_.

# Le driver JDBC en cause

Sur le site d’Oracle, la FAQ « [What is going on with DATE and TIMESTAMP?](http://www.oracle.com/technetwork/database/enterprise-edition/jdbc-faq-090281.html#08_01) »  décrit précisément le problème rencontré et donne plusieurs pistes pour le résoudre. Pour résumer, jusqu’à la version 9.2 d’Oracle, cette dernière ne distinguait pas les types temporels SQL DATE et TIMESTAMP. Le type DATE Oracle combinait à la fois dates et heures. Jusque-là, le driver JDBC Oracle associé le type DATE à un _java.sql.Timestamp_. L’implémentation du type SQL TIMESTAMP est arrivée avec la version 9.2 de la base Oracle. Pour se conformer à la norme SQL, Oracle préconisa de migrer les colonnes de type DATE contenant des heures dans une colonne de type TIMESTAMP. Logiquement, le driver JDBC de la 9.2 associait désormais le type DATE dans un _java.sql.Date_ et le type TIMESTAMP dans un _java.sql.Timestamp_. C’était oublier les bases antérieures à la version 9.2 ou celles qui n’avaient pas suivi les préconisations par difficultés techniques ou coûts. Ce changement de comportement du driver a perduré jusqu’à sa version 10.2. Oracle fit marche arrière avec la version 11.1 de son driver JDBC.  Les types SQL DATE furent de nouveau associés à la classe _java.sql.Timestamp_. Notre code applicatif utilisait la version 10.2.0.3 du driver Oracle. La base de données Oracle interrogée est quant à elle une 9.2.0.8.0. Elle pourrait donc théoriquement utiliser le type TIMESTAMP ; mais ce n’est pas le cas.

## Corrections possibles

Plusieurs solutions permettent de contourner ce problème :

1. Migrer le schéma pour **utiliser le type TIMESTAMP** à la place d’une DATE. Dans notre contexte, la base ne nous appartenant pas, cette solution ne peut s’appliquer.
1. Utiliser la méthode **_defineColumnType_** de la classe _OracleStatement_ afin de **redéfinir en _Timestamp_** les colonnes de type DATE. De par la verbosité du code et l’adhérence à la classe _OracleStatement_ du driver Oracle, cette solution fut mise de côté. En outre, nos tests étant basés sur la base de données embarquée H2, cette solution nous imposerait de supporter les 2 bases de données.
1. **Forcer l’appel à la méthode _getTimestamp_** du _ResultSet_ à la place d’un _getObject_. Sans doute la solution la moins risquée. Les impacts sont identifiés et maitrisés. Côté code, le code générique faisant massivement appel à la méthode _getObject_ devrait être retouché pour tester par le biais des méta-données JDBC si la colonne lue est de type DATE.
1. Utiliser le mode de compatibilité Oracle 8 en passant à true la propriété **_oracle.jdbc.V8Compatible_** de la connexion JDBC. Ne maitrisant pas les effets de bord et ce mode de compatibilité n’étant plus supporté à partir de la version 11 du driver Oracle, cette solution a été écartée.
1. Utiliser la **version 11 du driver JDBC Oracle** corrigeant le problème. C’est la solution qui a été retenue. Une migration vers Oracle 11 des bases de données de l’entreprise étant prévue à moyen termes, cette solution parait la plus pérenne, d’autant que nos tests n’ont pas décelé d’autres changements induits par cette montée de version de driver.

## Version du driver JDBC

Jusqu’à ce problème, je n’avais jamais prêté attention à la version du driver JDBC pour Oracle utilisée chez mon client. En effet, son choix est aux mains de l’équipe d’exploitation qui assure leur installation et leurs montées de version sur les serveurs d’applications. Le socle applicatif de l’entreprise est naturellement basé sur la même version. Par ailleurs, les driver Oracle sont unifiés. A savoir qu’un driver sait communiquer avec des bases de données de versions inférieures, voir même supérieure : «  [Which JDBC drivers support which versions of Oracle Database?](http://www.oracle.com/technetwork/database/enterprise-edition/jdbc-faq-090281.html#02_02) »

# Conclusion

En conclusion, comme je vous l’ai montré, une montée de version de drivers JDBC n’est pas anodine, surtout avec Oracle. Tout comme la montée de version d’un framework, une analyse d’impacts doit être menée à partir des [notes de livraisons](http://www.oracle.com/technetwork/database/features/jdbc/index-091264.html "Oracle JDBC Driver Downloads page").
Par ailleurs, nos tests unitaires sur une base embarquée n’ont pas pu déceler ce problème.  Moralité, même avec un taux de couverture maximum, des tests d’intégration ne sont jamais à exclure.
Seul petit réconfort : les ingénieurs Java de chez Oracle sont tombés sur le même bug. Preuve en est, l’exécution d’une requête SQL depuis l'outil Oracle SQL Developer installé sur mon poste de dév et qui ne renvoie pas l'heure des dates.
