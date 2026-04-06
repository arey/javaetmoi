---
_edit_last: "1"
author: admin
categories:
  - spring
date: "2016-12-21T16:20:08+00:00"
guid: http://javaetmoi.com/?p=1657
parent_post_id: null
post_id: "1657"
post_views_count: "12651"
summary: |-
  L’ [**application démo Spring Petclinic**](https://github.com/spring-projects/spring-petclinic) a été conçue pour montrer comment le framework Spring peut être utilisé pour développer une **application web** secondée par une base de données relationnelle. En somme, rien de révolutionnaire. Mais c’est ce qui fait tout son intérêt : présenter une **architecture logicielle** respectant **l’état de l’art** d’une application conçue avec **Spring**.

  Avec plus de 2000 forks sur GitHub, la communauté a créé de nombreux forks de Spring Petclinic : **Angular**, **React**, **REST**, **Spring Cloud** … Afin de fédérer cet engouement, l’ [**organisation GitHub Spring Petclinic**](https://github.com/spring-petclinic) a été créé sur GitHub en novembre 2016. La version de référence de Spring Petclinic reste sur [https://github.com/spring-projects/spring-petclinic](https://github.com/spring-projects/spring-petclinic). Les branches et les forks ont basculé sur [https://github.com/spring-petclinic](https://github.com/spring-petclinic).

  Ce billet a pour objectif de vous présenter cette récente initiative puis de vous présenter les **différents forks** d’ores et déjà disponible dans l’organisation Spring Petclinic. Mais avant cela, remontons le temps.
tags:
  - angularjs
  - devtools
  - microservices
  - react
  - rest
  - spring-boot
  - spring-cloud
  - spring-framework
title: Découvrez les forks de Spring Petclinic
url: /2016/12/les-forks-de-spring-petclinic/

---
L’ [**application démo Spring Petclinic**](https://github.com/spring-projects/spring-petclinic) a été conçue pour montrer comment le framework Spring peut être utilisé pour développer une **application web** secondée par une base de données relationnelle. En somme, rien de révolutionnaire. Mais c’est ce qui fait tout son intérêt : présenter une **architecture logicielle** respectant **l’état de l’art** d’une application conçue avec **Spring**.

Avec plus de 2000 forks sur GitHub, la communauté a créé de nombreux forks de Spring Petclinic : **Angular**, **React**, **REST**, **Spring Cloud** … Afin de fédérer cet engouement, l’ [**organisation GitHub Spring Petclinic**](https://github.com/spring-petclinic) a été créé sur GitHub en novembre 2016. La version de référence de Spring Petclinic reste sur [https://github.com/spring-projects/spring-petclinic](https://github.com/spring-projects/spring-petclinic). Les branches et les forks ont basculé sur [https://github.com/spring-petclinic](https://github.com/spring-petclinic).

Ce billet a pour objectif de vous présenter cette récente initiative puis de vous présenter les **différents forks** d’ores et déjà disponible dans l’organisation Spring Petclinic. Mais avant cela, remontons le temps.

# Les origines

D’après une [vieille documentation encore en ligne](http://docs.spring.io/docs/petclinic.html), Spring Petclinic a été initialement développé par Ken Krebs en **2003**. A cette époque, la version 1.0 de Spring Framework n’était pas encore releasée ([il a fallu attendre mars 2004](https://en.wikipedia.org/wiki/Spring_Framework)). La Javadoc @author démontre que le co-fondateur du framework Spring, Juergen Hoeller en personne, a activement contribué à Petclinic.
Les années passèrent. L’application bénéficia des montées de version du framework Spring.
En 2007, Spring Petclinic était distribué avec **Spring Framework 2.5** en tant qu’ **application d’exemple**.
Ensuite, pendant 5 ans, l’application n’a plus évolué.

En 2013, Michael Isvy, ex-responsable formation Spring chez Pivotal, Keith Donald et Costin Leau ont fait revivre l’application en la déplaçant sur GitHub et en la migrant vers Spring 3.

A partir de juin 2015, j’ai eu l’honneur de reprendre la coordination technique du projet. Mes contributions principales auront été de proposer une configuration full Java, une version Spring Boot et de migrer l’IHM vers le thème Bootstrap 3 de Pivotal.

Le mois dernier, j’ai passé la main à Dave Syer, qui n’est autre que le papa de Spring Batch, Spring Cloud et de Spring Boot.

# L’application Petclinic de référence

Reprenant les rennes, Dave Syer a tout de suite mis sa griffe sur le repo [spring-projects/spring-petclinic](https://github.com/spring-projects/spring-petclinic/) :

1. **La version Spring Boot est désormais celle de référence**. La version Spring Framework est « archivée » dans un fork présenté plus loin.
1. **Java 8** minimum
1. La couche présentation en JSP est réécrite en **Thymeleaf**. Le WAR auto-exécutable devient un **JAR**.
1. L’ **architecture** applicative est **modernisée**. La Pull Request [#200](https://github.com/spring-projects/spring-petclinic/pull/200) « Modularize and migrate to aggregate-oriented domain » présente les changements. La couche service est retirée. Les _Controllers_ dialoguent directement directement avec la couche _Repository_ qui assure désormais la gestion des transactions. L’organisation des packages passe d’un découpage technique (model, repository, service et web) à un découpage métier (owner, vet, visit).

Ce dernier **changement d’architecture** est le fait le plus marquant. Quelle rupture avec 15 ans de découpage Contrôleur -> Service -> DAO. Afin d’éviter des dépendances circulaires entre packages Java, la conception objet est en quelque sorte dénormalisée. La classe [Visit](https://github.com/spring-projects/spring-petclinic/blob/master/src/main/java/org/springframework/samples/petclinic/visit/Visit.java) ne référence plus la classe Pet, mais seulement son identifiant.

Maintenue par l’équipe **Pivotal**, cette **version « canonique » de Spring Petclinic** est celle à partir desquels les forks pourront être créés. Notons enfin que c’est la version **Spring Boot** qui est mise en avant. Cela implique qu’une nouvelle application Spring doit donc partir dans la majorité des cas sur du Spring Boot.

# Spring Framework Petclinic

L’application [spring-petclinic/spring-framework-petclinic](https://github.com/spring-petclinic/spring-framework-petclinic)  a pour objectif de maintenir une version de Spring Petclinic sans Spring Boot, à l’ancienne, avec de la **configuration Spring**, de bonnes vielles pages **JSP** et une **architecture 3-tiers**.

Comparée à son aînée, cette version présente de nombreux points d’intérêts :

1. La **configuration Spring** en **XML** (branche master) ou en full **Java** (branch [javaconfig](https://github.com/spring-petclinic/spring-framework-petclinic/tree/javaconfig)) de l’ensemble des couches d’une application web : présentation (Spring MVC, ressources statiques, dépendances JavaScript récupérées avec webjar), service (cache et transaction) et persistance.
1. 3 implémentations de la couche de persistance : **Spring JDBC**, **Hibernate** et **Spring Data JPA**. Le choix se fait au démarrage de l’application web par l’usage d’un profile Spring.
1. Des templates de pages et des composants graphiques avec **JSP**.
1. L’usage de l’ **AOP** avec l’aspect [CallMonitoringAspect](https://github.com/spring-petclinic/spring-framework-petclinic/blob/master/src/main/java/org/springframework/samples/petclinic/util/CallMonitoringAspect.java)
1. Un support de **PostreSQL** en plus de MySQL et HSQLDB.

Le fichier [README.MD](https://github.com/spring-petclinic/spring-framework-petclinic/blob/master/readme.md) donne les points d’entrée vers les fichiers  de configurer et les classes Java les plus intéressantes.

# Spring Petclinic AngularJS

Le fork [spring-petclinic/spring-petclinic-angular1](https://github.com/spring-petclinic/spring-petclinic-angular1) a été créé à partir de la branche angular de l’application de référence, juste avant que celle-ci ne soit supprimée.
[Liu Dapeng](https://www.verydapeng.com/), Michael Isvy et moi-même en sont les principaux contributeurs.

L’intérêt principal de ce fork est de disposer d’un **front-end full JavaScript**. Le code **Angular JS 1.5** dialogue avec le backend à l’aide d’une **API REST** propulsée par Spring MVC.
L’intérêt secondaire est de prouver que les mondes JavaScript et Java peuvent parfaitement cohabiter. Le téléchargement et l’exécution des outils front-end **gulp**, **bower**, **npm** et **node** sont pilotés par Maven à l’aide du [frontend-maven-plugin](https://github.com/eirslett/frontend-maven-plugin).

L’application est décomposée en **2 modules Maven**, un client front-end et une partie serveur Spring Boot :

1. **spring-petclinic-client**: ressources statiques (fichiers JavaScript Angular, images, fonts, css) packagées sous forme d’un webjar
1. **spring-petclinic-server**: API REST de Spring Petclinic et la page index.html (template Thymeleaf) permettant de référencer les ressources statiques du webjar

Côté **serveur**, afin d’exposer une API REST au front-end Angular, les contrôleurs Spring MVC ont été convertis en @RestController, renommés pour les besoins de l'API REST et simplifiés car une partie de la logique est désormais traitée dans le navigateur (ex : [OwnerResource.java](https://github.com/spring-petclinic/spring-petclinic-angular1/blob/master/spring-petclinic-server/src/main/java/org/springframework/samples/petclinic/web/OwnerResource.java)).

La partie **front** n’a rien à voir avec l’originale en JSP / Java. Elle bascule complètement dans le monde JavaScript (à l’exception d’un peu de Maven).
Le [spring-petclinic-client/pom.xml](https://github.com/spring-petclinic/spring-petclinic-angular1/blob/master/spring-petclinic-client/pom.xml) est configuré pour installer Node JS et NPM, récupérer les librairies tierces JS avec bower (cf. bower.json) puis lancer la phase de build avec Gulp (cf. gulpfile.js). Le répertoire target/dist construit par Gulp et les librairies JS sont enfin packagés par Maven sous forme de webjar. A noter que Gulp est configuré pour générer des CSS à partir des fichiers LESS de Petclinic et à minifier JS et CSS.
Le code AngularJS est centralisé dans le répertoire [spring-petclinic-client/src/scripts/.](https://github.com/spring-petclinic/spring-petclinic-angular1/tree/master/spring-petclinic-client/src/scripts) L’application Angular est bootstrapée dans le fichier [app.js](https://github.com/spring-petclinic/spring-petclinic-angular1/blob/master/spring-petclinic-client/src/scripts/app.js). Le module externe ui-router est chargé de la navigation entre vues. L’organisation de chaque vue se fait sur le même modèle. Voici en exemple celle listant les vétérinaires :

1. [vet-list.component.js](https://github.com/spring-petclinic/spring-petclinic-angular1/blob/master/spring-petclinic-client/src/scripts/vet-list/vet-list.component.js): déclaration du composant vetList, du template vet-list.template.html et du contrôleur VetListController
1. [vet-list.controller.js](https://github.com/spring-petclinic/spring-petclinic-angular1/blob/master/spring-petclinic-client/src/scripts/vet-list/vet-list.controller.js): définition du contrôleur VetListController chargé de faire un appel REST pour récupérer l’objet JSON représentant la liste des vétérinaires.
1. [vet-list.js](https://github.com/spring-petclinic/spring-petclinic-angular1/blob/master/spring-petclinic-client/src/scripts/vet-list/vet-list.js): configuration ui-router faisant le lien entre l’URL /vets et le template vet-list
1. [vet-list.template.js](https://github.com/spring-petclinic/spring-petclinic-angular1/blob/master/spring-petclinic-client/src/scripts/vet-list/vet-list.template.html): template HTML comportant des directives Angular

Spring Petclinic AngularJS montre également l’usage des **DevTools**. [Introduits dans Spring Boot 1.3](https://spring.io/blog/2015/06/17/devtools-in-spring-boot-1-3), ils peuvent remplacer l’usage d’outils comme JRebel ou Spring Loaded.
Le module **spring-boot-devtools** a été configuré de manière à ce que :

- la recompilation d’une classe Java déclenche le rechargement du contexte applicatif Spring (qui dure à peine 2 secondes sur mon macbook)
- une modification de ressources statiques déclenche un rafraichissement de la page dans le navigateur (le plugin [LiveReload](http://livereload.com/) doit préalablement être installé)

Cette configuration n’est active que pendant la phase de développement. Elle est localisée dans le fichier [application-dev.properties](https://github.com/spring-petclinic/spring-petclinic-angular1/blob/master/spring-petclinic-server/src/main/resources/application-dev.properties) qui n’est chargé par Spring Boot que lorsque le **profile Spring dev** est actif. Dans votre IDE, ajouter l’option ci-dessous au démarrage de la JVM : -Dspring.profiles.active=dev

# Spring Petclinic ReactJS

Le projet [spring-petclinic/spring-petclinic-reactjs](https://github.com/spring-petclinic/spring-petclinic-reactjs) est le 2nd portage de l’application Spring Petclinic vers un **front-end full JavaScript** de type **SPA** (Single Page Application), en l’occurrence basé ici sur [ReactJS](https://facebook.github.io/react/) (un framework MVC JavaScript développé par Facebook) et [TypeScript](https://www.typescriptlang.org/) (un sur-ensemble de ES6 développé par Microsoft).
Ce fork a été développé par [Nils Hartmann](http://nilshartmann.net/), co-auteur d’un [livre en allemand sur React](https://reactbuch.de/) et pro Spring Boot. Nils est parti de la version Spring Boot de Spring Petclinic. Pour designer l’API REST, il a récupéré certaines classes de la version AngularJS.

Comparé au fork AngularJS, front-end et backend disposent de leur propre serveur : l’un tournant sur **Node.JS** et l’autre sous **Spring Boot**.

La partie **front-end** est localisée dans le sous-répertoire [client](https://github.com/spring-petclinic/spring-petclinic-reactjs/tree/master/client). Outre le code TypeScript (TS) et les ressources statiques, on retrouve la configuration d’un certain nombres d’outils JavaScript :

- **NPM** tire les dépendances
- **Webpack** permet de modulariser le code JavaScript
- Pendant le développement, **Babel** transpile à chaud le code TS en JS
- **TSlint** est utilisé pour vérifier la qualité du code TS
- Téléchargement de définitions TS avec **Typings**

Chaque page de l’application web a été décomposée en composants et sous-composants React. A titre d’exemple, la page [OwnersPage.tsx](https://github.com/spring-petclinic/spring-petclinic-reactjs/blob/e5b7f58edf72764aa2f87e2b98cf6c9c1dea4b65/client/src/components/owners/OwnersPage.tsx) affichant le détail d’un propriétaire est découpée en 2 composants : [OwnerInformation.tsx](https://github.com/spring-petclinic/spring-petclinic-reactjs/blob/master/client/src/components/owners/OwnerInformation.tsx) et [PetsTable.tsx](https://github.com/spring-petclinic/spring-petclinic-reactjs/blob/master/client/src/components/owners/PetsTable.tsx). La majeure partie du code applicatif se retrouve ainsi dans le répertoire [client/src/components](https://github.com/spring-petclinic/spring-petclinic-reactjs/tree/master/client/src/components) dédié aux composants.

La partie **serveur** se rapproche de celle d’AngularJS. Seule différence majeure : les **données** envoyées par le client sont **validées**. Se référer aux classes [InvalidRequestException](https://github.com/spring-petclinic/spring-petclinic-reactjs/blob/master/src/main/java/org/springframework/samples/petclinic/web/api/InvalidRequestException.java), [ApiExceptionHandler](https://github.com/spring-petclinic/spring-petclinic-reactjs/blob/master/src/main/java/org/springframework/samples/petclinic/web/api/ApiExceptionHandler.java), [ErrorResource](https://github.com/spring-petclinic/spring-petclinic-reactjs/blob/master/src/main/java/org/springframework/samples/petclinic/web/api/ErrorResource.java) et [FieldErrorResource](https://github.com/spring-petclinic/spring-petclinic-reactjs/blob/master/src/main/java/org/springframework/samples/petclinic/web/api/FieldErrorResource.java). Bien conçue, cette couche de validation pourra être reportée sur la version AngularJS (cf. [issue 7](https://github.com/spring-petclinic/spring-petclinic-angular1/issues/7)).

# Spring Petclinic Microservices

Fondée par Maciej Szarliński, la version **microservices** de Spring Petclinic est mon coup de cœur du moment : [spring-petclinic/spring-petclinic-microservices](https://github.com/spring-petclinic/spring-petclinic-microservices). Un grand nombre de modules de la stack **Spring Cloud** y sont mis en œuvre.

Ce fork de la version AngularJS de Spring Petclinic a été décomposée en **3 micro-services** fonctionnels: **customers**, **vets** et **visits**. Autonomes, ces micro-services ne communiquent pas ensemble. Au démarrage, ils vont chercher leur configuration auprès du **serveur de config** (module [spring-petclinic-config-server](https://github.com/spring-petclinic/spring-petclinic-microservices/tree/master/spring-petclinic-config-server)). Par défaut, le serveur de config récupère la configuration depuis le repo GitHub [spring-petclinic-microservices-config](https://github.com/spring-petclinic/spring-petclinic-microservices-config/). Il est possible d’utiliser un repo Git local : -Dspring.profiles.active=local -DGIT\_REPO=/projects/spring-petclinic-microservices-config

Les 3 micro-services vont s’enregistrer auprès de l’ **annuaire de Service**(module [spring-petclinic-discovery-server](https://github.com/spring-petclinic/spring-petclinic-microservices/tree/master/spring-petclinic-discovery-server)) basé sur **Eureka**. Ils peuvent ainsi être accédés à partir de leur nom de service (ex : [http://customers-service/owners/{ownerId})](http://customers-service/owners/%7BownerId%7D)). Leur nom est paramétré dans le fichier [bootstrap.yml](https://github.com/spring-petclinic/spring-petclinic-microservices/blob/master/spring-petclinic-customers-service/src/main/resources/bootstrap.yml), au côté de l’URL du serveur de config.

Le front-end Angular n’attaque pas directement les 3 micro-services. Il passe par une **API Gateway** dont le mécanisme de routage est assuré par **Zuul** (module [spring-petclinic-api-gateway](https://github.com/spring-petclinic/spring-petclinic-microservices/tree/master/spring-petclinic-api-gateway)). Cette gateway n’est pas réduite à un simple passe-plat. Elle s’occupe de :

1. **Agréger** les réponses renvoyées par plusieurs micro-services avant de les retourner au client (se référer à la classe [ApiGatewayController](https://github.com/spring-petclinic/spring-petclinic-microservices/blob/ae7a717c153f67b1b844fb9d1be5da750063fd37/spring-petclinic-api-gateway/src/main/java/org/springframework/samples/petclinic/api/boundary/web/ApiGatewayController.java))
1. **Load-balancer** les requêtes entre plusieurs instances du même micro-services (annotation _@LoadBalanced_ dans la classe [ApiGatewayApplication](https://github.com/spring-petclinic/spring-petclinic-microservices/blob/master/spring-petclinic-api-gateway/src/main/java/org/springframework/samples/petclinic/api/ApiGatewayApplication.java)).

Afin de pouvoir suivre les requêtes HTTP entre plusieurs microservices, un mécanisme de **traces distribuées** a été mis en œuvre avec **Spring Cloud Sleuth**. L’interface graphique du serveur **Zipkin** permet de les consulter.

Enfin, avec pour objectif de simplifier le démarrage de l’ensemble de ces applications (3 microservices + 4 composants d’infra), un fichier **docker-compose.yml** [sera bientôt mis à disposition](https://github.com/spring-petclinic/spring-petclinic-microservices/pull/28).

# Tableau de synthèse

Le tableau ci-dessous dresse une liste des différentes versions de Spring Petclinic présentant à mes yeux un intérêt majeur :
**Appellation****Description****[Spring Petclinic](https://github.com/spring-petclinic)**Version de référence de Spring Petclinic.
Implémentée avec Spring Boot et Thymeleaf.**[Spring Framework Petclinic](https://github.com/spring-petclinic/spring-framework-petclinic)**Configuration XML et Java de Spring Framework.
Front-end implémenté en JSP.
3 technologies de persistance : JDBC, JPA et Spring Data JPA.[**Spring Petclinic AngularJS**](https://github.com/spring-petclinic/spring-petclinic-angular1)Front-end Angular 1 embarqué dans un webjar.
Usage de DevTools.**[Spring Petclinic ReactJS](https://github.com/spring-petclinic/spring-petclinic-reactjs)**Front-end ReactJS délivré par un serveur NodeJS et attaquant l’API REST du back-end implémenté en Spring Boot.[**Spring Petclinic Microservices**](spring-petclinic-microservices)Version distribuée de Spring Petclinic implémentée à l’aide de Spring Cloud : serveur Spring Config, annuaire de services avec Eureka, gestion des logs avec Zipkin et Sleuth, API Gateway avec Zuul, Docker compose …

# Conclusion

Dans cet article, j’ai commencé par retracer l’historique de l’application de référence Spring Petclinic qui a fêté son 13ième anniversaire et qui comptabilise plus de 2000 forks. Parmi ces forks, une poignée a intégré la nouvelle **organisation Spring Petclinic**. On y retrouve des versions front-end basées sur AngularJS et ReactJS, une version distribuée avec des micro-services et du Spring Cloud, une version plus legacy n’utilisant pas Spring Boot mais de la configuration XML ou Java (au choix).

L’organisation Spring Petclinic demande à s’élargir, soit en proposant un nouveau fork (ex : sur [Angular 2](https://github.com/spring-petclinic/spring-petclinic-angular1/issues/6)) soit en contribuant à ceux existants. Toute personne intéressée peut en faire la demande via l’issue [Spring Petclinic Organization](https://github.com/spring-projects/spring-petclinic/issues/203). Alors : à vos claviers !!

Resources :

- [Spring Petclinic community](https://github.com/spring-petclinic) (organisation GitHub)
- [DevTools in Spring Boot 1.3](https://spring.io/blog/2015/06/17/devtools-in-spring-boot-1-3) par Phill Webb (Pivotal)
- [Distributed Tracing with Spring Cloud Sleuth and Spring Cloud Zipkin](https://spring.io/blog/2016/02/15/distributed-tracing-with-spring-cloud-sleuth-and-spring-cloud-zipkin) par Josh Long (Pivotal)
- [Spring Boot 1.3 pour le web](https://www.youtube.com/watch?v=sR8PyhJa-Zw) par Biran Clozel et Stéphane Nicoll (Pivotal)
