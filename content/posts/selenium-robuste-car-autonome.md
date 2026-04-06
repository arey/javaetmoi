---
_edit_last: "1"
author: admin
categories:
  - test
date: "2013-06-22T13:29:03+00:00"
guid: http://javaetmoi.com/?p=707
parent_post_id: null
post_id: "707"
post_views_count: "5482"
summary: |-
  De nos jours, l’utilisation d’un serveur d’ **intégration continue** pour déployer son application puis exécuter ses **tests [Selenium](http://seleniumhq.org/)** s’est relativement démocratisée. Néanmoins, l’investissement réalisé pour l’écriture de ces tests peut rapidement être mis à mal par le coût associé à leur maintenance. En effet, les tests d’IHM sont de nature plus **instables** que de simples tests unitaires. Outre des problématiques de rendu et de transversalité des fonctionnalités testées, l’une des principales difficultés réside dans la **répétabilité des tests**. Les **données de test** y jouent pour beaucoup. Cette difficulté est décuplée lorsque votre application repose sur une **architecture SOA** dont les services SOAP, XML ou bien REST sont hébergés par des tiers : vous n’avez aucune maitrise sur les données de l’environnement testé, ni sur sa stabilité.
  Des tests qui échouent régulièrement à cause de données ayant été modifiées rendent laborieuse la détection de véritables **régressions**.
  Cet article propose une solution appliquée depuis 2 ans sur une application de taille modeste (35 000 LOC pour 20 écrans).
tags:
  - selenium
  - soa
  - spring-aop
  - test
title: Rendez autonomes vos Selenium
url: /2013/06/selenium-robuste-car-autonome/

---
De nos jours, l’utilisation d’un serveur d’ **intégration continue** pour déployer son application puis exécuter ses **tests [Selenium](http://seleniumhq.org/)** s’est relativement démocratisée. Néanmoins, l’investissement réalisé pour l’écriture de ces tests peut rapidement être mis à mal par le coût associé à leur maintenance. En effet, les tests d’IHM sont de nature plus **instables** que de simples tests unitaires. Outre des problématiques de rendu et de transversalité des fonctionnalités testées, l’une des principales difficultés réside dans la **répétabilité des tests**. Les **données de test** y jouent pour beaucoup. Cette difficulté est décuplée lorsque votre application repose sur une **architecture SOA** dont les services SOAP, XML ou bien REST sont hébergés par des tiers : vous n’avez aucune maitrise sur les données de l’environnement testé, ni sur sa stabilité.
Des tests qui échouent régulièrement à cause de données ayant été modifiées rendent laborieuse la détection de véritables **régressions**.
Cet article propose une solution appliquée depuis 2 ans sur une application de taille modeste (35 000 LOC pour 20 écrans). **Constitution d’un jeu de données**

La 1ière idée permettant de résoudre ce type de problématique consiste à essayer **d’échantillonner manuellement** des données de test satisfaisant les critères de chaque test Selenium. Par exemple, pour exécuter le scénario fonctionnel permettant d’effectuer un avenant, est dressée une liste de contrat en cours.
Mais que se passe-t-il lorsqu’un développeur ou qu’un autre test Selenium clôture l’un des contrats référencés ou qu’une recopie de la base de production supprime le contrat du système ? L’échantillonnage doit être recommencé.

Une solution plus avancée consiste à **échantillonner dynamiquement** les données de test. Pour se faire, les applications tierces doivent soit mettre à disposition des services spécifiques de recherche, soit donner accès à leur base de données. Les premiers demandent des coûts de développement et de maintenance, ce qui les rend difficilement envisageables. La seconde nécessite d’appréhendez le modèle des différents systèmes tiers ou qu’un membre de l’équipe apporte son aide dans l’élaboration des requêtes SQ L nécessaires à la récupération des échantillons. Moins coûteuse, cette solution n’est pas toujours bien vue. Qui plus est, tout changement ultérieur du schéma risque de faire échouer les tests.

## **L’indépendance est votre salut**

Pour rendre les **tests exécutables à l’infini** sans avoir à se préoccuper de l’état des partenaires (Back Offices, référentiels métiers, serveur SSO,  éditique, GED …),  la solution que nous avons mise en place consiste à bouchonner tous leurs appels. En pratique, nous nous sommes appuyés sur le composant Mock Switcher développé par [mon illustre prédécesseur](https://github.com/gdarmont). Ce composant permet d’ **enregistrer les réponses des partenaires** en fonction des paramètres d’appel. Sauvegardés au format XML ou JSON, ces réponses peuvent être retouchées pour les besoins du test.  Mais surtout, elles **simuleront les réponses** des partenaires lors de l’exécution des tests.
Techniquement, le Mock Switcher repose sur [**Spring AOP**](http://static.springsource.org/spring/docs/3.2.3.RELEASE/spring-framework-reference/html/aop.html "Aspect Oriented Programming with Spring") et [XStream](http://xstream.codehaus.org/ "XStream is a simple library to serialize objects to XML and back again.")/ [Jackson](http://jackson.codehaus.org/ "Jackson streaming JSON parser"). Il peut être assimilé à un système de cache applicatif persistant les données sur disque et utilisé à des fins de test.
Initialement, le Mock Switcher avait été développé pour bouchonner temporairement des partenaires indisponibles et ne pas bloquer ainsi les développeurs. Son usage a ici été quelque peu détourné.

Sur le même principe, s’affranchir des **éléments d’infrastructure** permet de gagner en stabilité et de s’assurer davantage de la répétabilité des tests. De nos jours, cette virtualisation est possible à l’aide de bases de données embarquées ([H2](http://www.h2database.com/), [HSQLDB](http://hsqldb.org/)), de providers JMS en mémoire ([ActiveMQ](http://activemq.apache.org/)) ou bien encore de bouchons de serveurs mails SMTP ([Dumbster](http://quintanasoft.com/dumbster/) ou [Wiser SubEtha SMTP](http://code.google.com/p/subethasmtp/wiki/Wiser)) …

**Avec ces 2 approches combinées, l’application peut s’exécuter en autonomie complète, déconnectée de tout réseau**.

En pratique, les tests sont exécutés par une commande maven qui construit l’application, la démarre avec un profil Spring standalone (utilisation de l’infrastructure de test et activation des mocks) puis exécute les tests Selenium.  La base de données embarquée est initiée avec des données du référentiel. Si besoin est, des modifications spécifiques au scénario de tests peuvent être effectuées avec le démarrage d’un test.
Le schéma suivant illustre l’application de ces différentes étapes :
[![Automatisation de l'exécition de tests Selenium autonomes](/wp-content/uploads/2013/06/deploiement-tests-selenium-autonomes.png)](/wp-content/uploads/2013/06/deploiement-tests-selenium-autonomes.png)

Cette typologie de test présente des avantages comme des inconvénients :
**Avantages****Inconvénients**

- Les mêmes tests peuvent être exécutés en parallèle (par des développeurs et/ou builds différents)
- Diminution des faux négatifs
- Exécution plus rapide des tests
- Feedback immédiat lors d’une migration technique (ex : montée de version de frameworks)
- Maitrise des jeux de données associés aux scénarios de tests

- Lorsqu’un test échoue, une vérification du jeu de données est nécessaire
- Maintenance des bouchons  XML / JSON
- Maintenance du script DDL et des jeux de données SQL
- Débogage nécessitant de démarrer l’application avec le profile standalone
- Adhérences non testées

## **Conclusion**

Plus rapide à exécuter que des tests réellement connectés, ces tests peuvent être déclenchés après chaque commit effectué par un développeur dans le gestionnaire de code source. Une pré-qualification de l’application est ainsi effectuée au plus tôt.

Complémentaire aux tests unitaires et aux tests d’intégration automatisés, **ces tests orientés IHM couvrent les principales couches de l’application** : de la page HTML au code Java des contrôleurs, des services métiers et de la couche de persistance, en passant par le code JavaScript et les appels Ajax. Seule la partie échange est émulée.
Pour combler ce vide, sur notre application, d’autres tests Selenium sans bouchon sont joués en complément par un build nocturne ; ils permettent de vérifier l’intégration de l’application avec ses partenaires et toutes ses adhérences. Pour ne pas retomber sur les problématiques de répétabilité évoquées en début d’article, ces tests essaient d’être le plus indépendants des données et couvrent ainsi d’autres fonctionnalités.
