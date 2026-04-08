---
_edit_last: "1"
_wp_old_slug: benchmark-framework-javas-mapping-objet
author: admin
categories:
  - retour-d'expérience
date: "2015-09-16T05:20:37+00:00"
thumbnail: /wp-content/uploads/2015/09/logo-java-performance.png
featureImage: /wp-content/uploads/2015/09/logo-java-performance.png
featureImageAlt: "logo-java-performance"
guid: http://javaetmoi.com/?p=1442
parent_post_id: null
post_id: "1442"
post_views_count: "22999"
summary: |-
  [![logo-java-performance](http://javaetmoi.com/wp-content/uploads/2015/09/logo-java-performance.png)](http://javaetmoi.com/wp-content/uploads/2015/09/logo-java-performance.png) Ce billet a pour origine un commentaire posté dans [mon précédent billet](http://javaetmoi.com/2015/08/check-list-revue-code-et-architecture-java/) et dans lequel Laurent demandait un **retour d’expérience** sur l’utilisation de **frameworks Java de mapping objet vers objet** tels [Dozer](https://github.com/DozerMapper/dozer) ou [ModelMapper](http://modelmapper.org/).

  Dans l’architecture d’une **applicative n-tiers**, une couche de mapping objet / objet peut intervenir à plusieurs niveaux :

  1. En entrée ou en sortie d’un web service SOAP afin de convertir en objet métier les DTO générés à partir du WSDL, ou inversement.
  2. Entre la couche de présentation et la couche de services métiers lorsque la première expose des DTO et la seconde travaille avec des objets métiers.
  3. Entre la couche de services métiers et la couche d’accès aux données afin de mapper les entités persistances en objets métiers.

  Dans le premier exemple, le développeur n’a guère le choix. Dans les 2 autres, il s’agit d’un choix d’architecture.
  L’introduction d’une couche de mapping n’est pas un choix à prendre à la légère : ayant pour objectif de découpler les couches, elle complexifie l’application et peut détériorer ses performances. Le choix d’en introduire une et d’utiliser un framework pour faciliter sa mise en œuvre n’est pas non plus évident.

  Ce billet est découpé en 2 parties :

  1. Une première dressant les **avantages** et les **inconvénients** d’utiliser **Dozer** par rapport à une **approche manuelle**,
  2. et une seconde présentant les résultats d’un **micro-benchmark** comparant plusieurs frameworks : **Dozer**, **Orika**, **Selma**, **MapStruct** et **ModelMapper**.
tags:
  - benchmark
  - dozer
  - mapstruct
  - modelmapper
  - orika
  - selma
title: Benchmark de frameworks de mapping objet
url: /2015/09/benchmark-frameworks-java-mapping-objet/

---
[![logo-java-performance](/wp-content/uploads/2015/09/logo-java-performance.png)](/wp-content/uploads/2015/09/logo-java-performance.png) Ce billet a pour origine un commentaire posté dans [mon précédent billet](/2015/08/check-list-revue-code-et-architecture-java/) et dans lequel Laurent demandait un **retour d’expérience** sur l’utilisation de **frameworks Java de mapping objet vers objet** tels [Dozer](https://github.com/DozerMapper/dozer) ou [ModelMapper](http://modelmapper.org/).

Dans l’architecture d’une **applicative n-tiers**, une couche de mapping objet / objet peut intervenir à plusieurs niveaux :

1. En entrée ou en sortie d’un web service SOAP afin de convertir en objet métier les DTO générés à partir du WSDL, ou inversement.
1. Entre la couche de présentation et la couche de services métiers lorsque la première expose des DTO et la seconde travaille avec des objets métiers.
1. Entre la couche de services métiers et la couche d’accès aux données afin de mapper les entités persistances en objets métiers.

Dans le premier exemple, le développeur n’a guère le choix. Dans les 2 autres, il s’agit d’un choix d’architecture.
L’introduction d’une couche de mapping n’est pas un choix à prendre à la légère : ayant pour objectif de découpler les couches, elle complexifie l’application et peut détériorer ses performances. Le choix d’en introduire une et d’utiliser un framework pour faciliter sa mise en œuvre n’est pas non plus évident.

Ce billet est découpé en 2 parties :

1. Une première dressant les **avantages** et les **inconvénients** d’utiliser **Dozer** par rapport à une **approche manuelle**,
1. et une seconde présentant les résultats d’un **micro-benchmark** comparant plusieurs frameworks : **Dozer**, **Orika**, **Selma**, **MapStruct** et **ModelMapper**.

## Tableau comparatif Dozer vs mapping manuel en Java

Extrait d’un **retour d’expérience**, le tableau ci-dessous dresse les avantages et les inconvénients de Dozer par rapport à une approche manuelle. A vous de pondérer chaque avantage / inconvénient en fonction de vos exigences.
| | **Dozer** | **Java** |
|---|---|---|
| **Avantages** | - Lisibilité du XML pour mapper les champs : profondeur du chemin de la propriété, découplage entre la correspondance source/destination et la règle de transformation, conversion implicite en fonction des types source et destination<br>- Réutilisation du code : transformations réutilisables<br>- Structure le développement de mappings<br>- Le mapping sert à la fois pour créer un nouvel objet et compléter un objet existant<br>- Mapping bi-directionnel offert | - Simplicité<br>- Pile d’appel claire lors du debug<br>- Type safe |
| **Inconvénients** | - Faibles performances<br>- Mapping non compilé : pas de complétion dans l’IDE, refactoring nécessitant des recherches dans le XML<br>- Utilisation de converter pour gérer les cas compliqués (et ne pas faire appel à du code Java après le mapping Dozer).<br>- Apprentissage du framework et des bonnes pratiques | - Verbosité du code Java pour les tests de nullité et le code d’instanciation |

En fonction de votre expertise, ce tableau pourrait être adapter avec d’autres frameworks.

Quel que soit l’approche choisie (framework ou code manuel), seuls des **tests unitaires** permettront de valider le mapping. Ne pouvant être automatisés, ces tests s’avèrent malheureusement longs et fastidieux.

## Micro-benchmark

Ne trouvant aucun comparatif récent sur les performances des frameworks de mapping, j’ai créé sur GitHub le projet [java-object-mapper-benchmark](http://github.com/arey/java-object-mapper-benchmark). Ce dernier utilise **[JMH](http://openjdk.java.net/projects/code-tools/jmh/)** (Java Microbenchmarking Harness) pour réaliser un micro-benchmark entre Dozer, Selma, ModelMapper, Orika, MapStruct et un mapping écrit manuellement.

Le diagramme ci-dessous présente résultats obtenus avec la configuration suivante :

- OS: MacOSX
- CPU: Core i7 2.8GHz 6MB cache × 4 cores
- RAM: 16GB
- JVM: Oracle 1.8.0\_25 64 bits

[![](/wp-content/uploads/2015/09/2015-09-mapping-objet-objet2.png)](/wp-content/uploads/2015/09/2015-09-mapping-objet-objet2.png)

Comme on pouvait s’y attendre, les performances du code écrit à la main sont les meilleures.
Selma et MapStruct se rapprochent le plus des performances d’un code écrit manuellement. Ce résultat s’explique par le fait qu’ils génèrent le code source à l’aide de l’ **Annotation Processor** introduit par Java 6 (JSR-269).
Basés sur l’ **introspection** de code, Dozer et ModelMapper sont peu performants.
Entre ces 2 catégories, on retrouve Orika qui utilise au runtime l’API **Java Compiler** pour générer le code du mapping.

Pour exécuter vous même le benchmark, Maven, un JDK et 3 lignes de commandes suffisent :

```sh
git clone git://github.com/arey/java-object-mapper-benchmark.git
mvn clean install
java -jar target/benchmarks.jar
```

## Conclusion

En 2015, l’utilisation d’un framework de mapping objet / objet basé sur la génération de code plutôt que sur l’introspection semble préférable. Non seulement les performances sont bien meilleures, mais le couplage avec le framework est faible puisqu’il est possible de le supprimer et de conserver dans votre SCM le code généré. **Selma** et **MapStruct** sont les 2 gagnants du benchmark.

Encore une fois, avant de partir sur une telle approche, prenez un temps de réflexion. Des entités métiers annotées avec Bean Validation et traversant l’ensemble des couches restent l’architecture la plus simple à mettre en œuvre. Je suis déjà intervenu sur une application où une couche de mapping avait été mise en œuvre dès le départ pour des raisons de découplage, puis retirée au fur et à mesure car sa plus value était trop faible.

Références :

- [Dozer vs Orika vs Manual (2013)](http://blog.sokolenko.me/2013/05/dozer-vs-orika-vs-manual.html)
- [Java Bean Mapper Performance Tests](http://www.christianschenk.org/blog/java-bean-mapper-performance-tests/) (2007)
- [Selma, le mapping Java à la compilation](http://blog.xebia.fr/2014/04/24/selma-le-mapping-java-a-la-compilation/) (2014)
- [Using JMH for Java Microbenchmarking](http://nitschinger.at/Using-JMH-for-Java-Microbenchmarking) (2013)
