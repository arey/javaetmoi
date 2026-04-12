---
_edit_last: "1"
author: admin
categories:
  - conférence
date: "2012-04-20T20:17:10+00:00"
thumbnail: wp-content/uploads/2012/04/2012-04-18-11.56.37.jpg
featureImage: wp-content/uploads/2012/04/2012-04-18-11.56.37.jpg
featureImageAlt: "Hands-on-Lab Le Président est ... de Devoxx France 2012"
guid: http://javaetmoi.com/?p=148
parent_post_id: null
post_id: "148"
post_views_count: "10911"
summary: |-
  Au cours de la première matinée de **Devoxx France**, j’ai pu assister à un **Lands-on-Lab** permettant de **s’initier au SDK** et à la plateforme **Google App Engine**.

  Nommé « [Le Président est …](http://www.devoxx.com/pages/viewpage.action?pageId=6128177)» \[1\], ce code labs fut co-animé par [Didier Girard](http://www.devoxx.com/display/FR12/Didier+Girard) (SFEIR), [Ludovic Champenois](http://www.devoxx.com/display/FR12/Ludovic+Champenois) (Google), [Martin Görner](http://www.devoxx.com/display/FR12/Martin+Gorner) (Google) et [Patrice de Saint Steban](https://twitter.com/#!/patoudss) (SFEIR). Il consistait à développer en 3h un site web visant à annoncer au soir du 6 mai 2012 le nom du nouveau Président. Une seule contrainte : accueillir un trafic potentiel de 50 millions d’utilisateurs et pouvoir tenir **un pic  de charge de 2 millions d’utilisateurs** aux alentours de 20h. En guise d’exemple, une [application démo](http://electionfr2012.appspot.com/) \[2\] était déjà disponible en ligne.

  D’actualités et évoquant des chiffres qui exciteraient tout architecte, ce code labs fut la parfaite occasion de m’initier à Google App Engine. Au cours de ce billet, je vous relaterai ce que j’y ai appris et vous donnerai accès au code source que vous pourrez à votre tour déployer sur le PaaS de Google.

  ![Hands-on-Lab Le Président est ... de Devoxx France 2012](wp-content/uploads/2012/04/2012-04-18-11.56.37.jpg)
tags:
  - app-engine
  - bigtable
  - cloud
  - devoxx
  - google
  - html-5
  - java
  - nosql
  - objectify
  - paas
title: Initiation à Google App Engine
url: /2012/04/devoxx-initiation-google-app-engine/

---
Au cours de la première matinée de **Devoxx France**, j’ai pu assister à un **Lands-on-Lab** permettant de **s’initier au SDK** et à la plateforme **Google App Engine**.

Nommé « [Le Président est …](http://www.devoxx.com/pages/viewpage.action?pageId=6128177)» \[1\], ce code labs fut co-animé par [Didier Girard](http://www.devoxx.com/display/FR12/Didier+Girard) (SFEIR), [Ludovic Champenois](http://www.devoxx.com/display/FR12/Ludovic+Champenois) (Google), [Martin Görner](http://www.devoxx.com/display/FR12/Martin+Gorner) (Google) et [Patrice de Saint Steban](https://twitter.com/#!/patoudss) (SFEIR). Il consistait à développer en 3h un site web visant à annoncer au soir du 6 mai 2012 le nom du nouveau Président. Une seule contrainte : accueillir un trafic potentiel de 50 millions d’utilisateurs et pouvoir tenir **un pic  de charge de 2 millions d’utilisateurs** aux alentours de 20h. En guise d’exemple, une [application démo](http://electionfr2012.appspot.com/) \[2\] était déjà disponible en ligne.

D’actualités et évoquant des chiffres qui exciteraient tout architecte, ce code labs fut la parfaite occasion de m’initier à Google App Engine. Au cours de ce billet, je vous relaterai ce que j’y ai appris et vous donnerai accès au code source que vous pourrez à votre tour déployer sur le PaaS de Google.

[![Hands-on-Lab "Le Président est ..." de Devoxx France 2012](wp-content/uploads/2012/04/2012-04-18-11.56.37.jpg)](wp-content/uploads/2012/04/2012-04-18-11.56.37.jpg)**Présentation de Google App**

App Engine est un serveur d’application pensé pour le Cloud. Visant historiquement les applications Python, il adresse aujourd’hui les applications Java.

Le SDK d’App Engine permet de développer une application, la tester puis la déployer dans le Cloud. Il propose également une console d’administration minimaliste.

Bon à savoir : le déploiement se fait au travers du protocole HTTP. Il peut donc passer les proxys et firewalls des entreprises.

La partie dite RUN donne accès à de nombreux services : base NoSQL (la fameuse BigTable qui a inspiré HBase), base MySQL, authentification (SSO de Google), CRON, task queue, chanel, images, mail (envoi et réception !!), MemCache, XMPP, URLFetch, BlobStore et bientôt FullText Search (annoncé lors de dernier Google IO).
Les speakers insistent sur le **service URLFetch** qui permet d’utiliser l’infrastructure Google pour récupérer des pages HTTP. Crawler le web est le métier de base de Google. Avec ses systèmes de cache et de résolution de noms de domaine, c’est donc sans doute la stack la plus optimisée au monde.

**Focus sur le DataSore**

Le DataStore c’est quoi ? C’est la solution NoSQL de Google basée sur BigTable. On peut la voir comme une **grosse HashMap** dans laquelle on stocke des documents dans n’importe quel format: XML, JSON, String, CSV … Charge est au développeur de gérer le marshalling  des données lors de leur persistance.
Chaque document possède un identifiant et peut avoir plusieurs index. Les index sont utilisés pour effectuer des recherches ; ils sont typés et peuvent être multi-valués.
Comme dans le monde relationnel, la création d’un index a un coût. C’est pourquoi Google les facture.

Le DataStore est optimisé pour être le plus performant en lecture. Il assure la réplication des données, leur accès simultanés et la montée en charge.

Point d’attention, les clauses where sont limitées à un seul ordre de comparaison. Ceci amène quelques sophistications : système de classification par intervalle, coordonnées géographiques passées de 2D en 1D.
Le DataStore peut être manipulée à l’aide d’une API Java, simple à prendre en main mais basique. Le projet [Objectify](http://code.google.com/p/objectify-appengine/) \[3\] permet d’apporter une sur-couche ORM utilisant les annotations JPA.
**Architecture d’AppEngine**

Les applications hébergées sur Google App Engine sont hébergées dans les mêmes Data Centers et les mêmes serveurs physiques que les applications Google comme Google Search, Google Mail, Google Docs … Les applications déployées sur AppEngine profitent donc de l’infrastructure de Google réputée fiable, robuste et hautement scalable.

A l’origine, l’architecture d’AppEngine était basée sur une **architecture dite « système 2000 »** : sessions utilisateurs en RAM avec des sticky load balancer. De nombreux problèmes en découlaient : arrêt des serveurs, mémoire insuffisante, lenteur du load balancing, problème de scalabilité.

L’architecture actuelle résout ces problèmes : instances stateless, état dans un MemCache et persistance dans un DataStore. Comme sur Amazon EC2,les **load balancers** deGoogle sont configurés le plus simplement possible en **round robin**, ce qui les rend **10x plus performant que les sticky sessions.** **Déroulement des Travaux Pratiques**

Les participants au code labs étaient tenus de venir avec un ordinateur portable équipé des **prérequis** suivants :

- JDK 6
- Eclipse Indigo 3.7 en version JEE (la version de base fonctionne mais il faudra par exemple oublier la coloration syntaxique des JSP)
- Google Plugin for Eclipse 3.7 et Google App Engine Java SDK 1.6.4 disponibles depuis le [référentiel de plugins Google pour Ecplise](http://dl.google.com/eclipse/plugin/3.7) \[4\]
- Un compte Gmail

Evidemment, les organisateurs avaient paré à tout aléa : une clé USB contenant tous ces outils était à notre disposition. En complément, y figuraient les [slides des travaux](http://code.google.com/p/devoxx-france-appengine/source/browse/#svn%2Ftrunk%2FLePresidentEst%20presentation) **pratiques**\[5\]. Oh surprise : au **format html 5,** les slides ont été réalisés avec le projet open source [Google HTML5 slides template](http://code.google.com/p/html5slides/) \[6\]. Impressionnant, mais pas encore tout à fait au point : navigation nécessitant de mixer clavier et souris, bug d’affichage, nécessite Google Chrome pour aller au-delà du premier slide, bug de rendu avec les cartes graphiques des VAIO Sony  …

Bien pensés, les TP permettent de nous initier pas à pas à l’utilisation du SDK et aux différents services du Cloud de Google :

1. Création puis configuration d’un **projet Eclipse** pour AppEnfine
1. Mise au point en **JSP** d’un formulaire de soumission de commentaires
1. **Exécution en local** de l’application
1. **Déploiement** sur l’infrastructure Google AppEngine
1. Utilisation du **UserService** d’AppEngine pour authentifier les utilisateurs à partir de leur compte Gmail
1. Persistance des commentaires dans le **DataStore** en utilisant l’API Java
1. Migration de la couche de persistance vers **Objectify**
1. Optimisation du rendu de la page avec les commentaires mis en cache grâce au service **MemCache**
1. Création d’une servlet dont l’appel est planifié par le **service CRON**

Dans le cadre du code labs, je me suis arrêté là. [Mon premier site](http://lepresidentantoine.appspot.com/) \[7\] Google AppEngine était en ligne. Bien entendu, pour les plus rapides, il était possible d’aller encore plus loin : compteur partagé, gestion d’index, upload de fichiers, réception et lecture d’un mail.

Pendant la phase de développement, suite à ce que je pensais être une anomalie, j’ai appris que lorsqu’une donnée est persistée dans BigTable, vous n’êtes pas certains de la retrouver immédiatement après lorsque vous requêter en lecture BigTable. En effet, il existe un **temps de propagation**. J’avoue que c’est assez déroutant, surtout lorsqu’on a pour référence le monde du relationnel où les données commitées en base sont immédiatement disponibles aux autres clients. Qui plus est, ce phénomène peut être accentué par une mauvaise utilisation du cache.
Chose néanmoins rassurante : pas besoin de déployer sur AppEngine pour s’en apercevoir, ce comportement est observable depuis Eclipse.

Avant de déployer son application, il est possible de spécifier sa version dans le fichier appengine-web.xml. Jusqu’à **10 versions** d’une même application peuvent être accessibles **en ligne simultanément**. Pratique pour les mises en production et les éventuels retours arrière. Seule chose à garder en tête : toutes les versions partagent les mêmes données.

**Conclusion**

En quelques heures, j’ai pu mettre en ligne un site fonctionnel écrit en Java. Bien qu’ayant déjà expérimenté le déploiement d’applications sur d’autres plateformes (CloudBees et Heroku pour ne pas les citer), cela reste toujours impressionnant. Grâce au Cloud, le **déploiement d’applications Java** devient d’une **facilité déconcertante**, chose impossible il y’a encore quelques années. Sans pouvoir réaliser avec le monde PHP, il y’a désormais de **nombreux hébergeurs Java** et une concurrence accrue. Ces derniers fournissent pour la plupart un environnement gratuit en dessous d’une certaine charge.

Cet enthousiasme est malheureusement modéré par le **lock-in** observé sur AppEngine. En effet, plus on utilise de services AppEngine, plus l’application devient dépendante de la plateforme Cloud de Google.

Références :

1. Présentation du code labs « Le Président est … » : [http://www.devoxx.com/pages/viewpage.action?pageId=6128177](http://www.devoxx.com/pages/viewpage.action?pageId=6128177)
1. Application d’exemple pour le code labs de Devoxx : [http://electionfr2012.appspot.com/](http://electionfr2012.appspot.com/)
1. Site d’Objetify AppEngine : [http://code.google.com/p/objectify-appengine/](http://code.google.com/p/objectify-appengine/)
1. Référentiel des plugins Eclipse 3.7 de Google : [http://dl.google.com/eclipse/plugin/3.7](http://dl.google.com/eclipse/plugin/3.7)
1. Code source de l’application exemple et de la présentation : [http://code.google.com/p/devoxx-france-appengine/source/browse/](http://code.google.com/p/devoxx-france-appengine/source/browse/)
1. Projet Google HTML5 slides template : [http://code.google.com/p/html5slides/](http://code.google.com/p/html5slides/)
1. Mon premier site Google AppEngine : [http://lepresidentantoine.appspot.com/](http://lepresidentantoine.appspot.com/)
