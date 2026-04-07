---
_edit_last: "1"
author: admin
categories:
  - retour-d'expérience
date: "2015-08-27T05:20:24+00:00"
thumbnail: /wp-content/uploads/2015/08/clean_code_72_color.png
featureImage: /wp-content/uploads/2015/08/clean_code_72_color.png
featureImageAlt: "clean_code_logo"
guid: http://javaetmoi.com/?p=1435
parent_post_id: null
post_id: "1435"
post_views_count: "14858"
summary: |-
  [![clean_code_logo](http://javaetmoi.com/wp-content/uploads/2015/08/clean_code_72_color-150x150.png)](http://javaetmoi.com/wp-content/uploads/2015/08/clean_code_72_color.png) Réaliser des **revues de code e** st une activité que je pratique régulièrement sur les projets que j’encadre techniquement. De manière général, elles **se déroulent sur le poste du développeur**. Ce dernier me présente ses derniers changements, justifie ses choix et m’explique ses difficultés. En fonction de son expérience sur le projet, la périodicité des revues varie d’1 fois par jour à 2 fois par mois.
  Les améliorations à apporter sont réalisées en séance en pair programming ou bien consignées directement dans le code à l’aide d’un TODO. Je profite de ces moments privilégiés pour expliquer et/ou échanger autour des règles de coding et d’architecture logicielle.

  Dans le cadre de l’ **externalisation du développement** d’une application, les revues de code se pratiquent différemment. En effet, la livraison du code intervient souvent après un long effet tunnel. Dès le début des développements, les développeurs doivent connaître mes attentes. Ce billet a pour objectif de les formaliser de manière synthétique.
title: Check-list revue de code Java
url: /2015/08/check-list-revue-code-et-architecture-java/

---
[![clean_code_logo](/wp-content/uploads/2015/08/clean_code_72_color.png)](/wp-content/uploads/2015/08/clean_code_72_color.png) Réaliser des **revues de code e** st une activité que je pratique régulièrement sur les projets que j’encadre techniquement. De manière général, elles **se déroulent sur le poste du développeur**. Ce dernier me présente ses derniers changements, justifie ses choix et m’explique ses difficultés. En fonction de son expérience sur le projet, la périodicité des revues varie d’1 fois par jour à 2 fois par mois.
Les améliorations à apporter sont réalisées en séance en pair programming ou bien consignées directement dans le code à l’aide d’un TODO. Je profite de ces moments privilégiés pour expliquer et/ou échanger autour des règles de coding et d’architecture logicielle.

Dans le cadre de l’ **externalisation du développement** d’une application, les revues de code se pratiquent différemment. En effet, la livraison du code intervient souvent après un long effet tunnel. Dès le début des développements, les développeurs doivent connaître mes attentes. Ce billet a pour objectif de les formaliser de manière synthétique.

## Sonar, bien mais pas suffisant

Dans ces 2 types de revues, la **qualité du code** est mesurée automatiquement par l’outil **[SonarQube](http://www.sonarqube.org/)**. Des seuils sont fixés pour chaque métrique :  taux de couverture de tests, nombre de défauts ... Accessible en ligne et documenté, le profil SonarQube fait office de référence sur les règles à respecter : de la simple règle de formatage du code à la gestion des exceptions.

Pour autant, toutes les bonnes pratiques en termes de qualité du code et d’architecture ne peuvent pas être contrôlées par cet outil. Qui plus est, il est parfois possible de leurrer SonarQube. Par exemple, en utilisant des outils de génération automatique de tests unitaires (TU) ou en développement des TU sans assertions, on augmente artificiellement la couverture de code. **Une revue « manuelle » reste donc obligatoire**.

Les points qui sont surveillés lors de cette revue sont référencés dans une **check-list**. Ces points ont été répartis en 5 catégories :

1. Code Design
1. Architecture logicielle
1. Performance
1. Tests
1. Sécurité

Certains points sont spécifiques à l’architecture technique de l’application. Dans notre exemple, l’application web est décomposée en 3 couches et repose sur les technologies Spring MVC, CXF et JDBC.
Sans surprise, de nombreuses de règles sont tirées de l’ouvrage de référence des développeurs « [Clean Code](http://www.amazon.fr/Clean-Code-Handbook-Software-Craftsmanship/dp/0132350882)» d'Uncle Bobo. Les autres proviennent de bonnes pratiques, d’état de l’art et d’expériences.

## Code Design

**Rubrique****Description****Qualité**Respecter les règles du profil "Sonar way " de SonarQube**Lisibilité du code**Code élégant et facile à lire.
Les classes et les méthodes doivent être relativement petites (classes < 300 lignes et méthodes < 20).
Les conditions doivent être compréhensibles.
Homogénéité du code : règles de nommage, découpage en package ...
Pas de code mort ni de code commenté.
Noms appropriés (doit révéler l'intention, ne pas les tronquer ou le abréger)**Simplicité**Principe KISS. Pas d'over-design
Utilisation de Design Pattern justifiée
Dépendances vers d'autres classes minimales**Réutilisation**Framework open source à privilégier sur du code maison.
Code factorisé. Code dupliqué à éviter.
Utilisation appropriée de l'héritage et de la composition**Commentaires**La javadoc apporte une plus-value et doit aider à la maintenance de l'application. Interfaces, Classes, propriétés et méthodes publiques doivent comporter une Javadoc.
Les commentaires dans le code doivent se limiter à des explications (le pourquoi).**Configuration**Les variables susceptibles de changer d'un environnement à l'autre doivent être externalisées et variabilisées par environnement.
Le texte et les libellés des pages JSP sont externalisés dans des message bundles (.properties)

## Architecture logicielle

**Rubrique**Description**Gestion des transactions**Les transactions base de données sont gérées au niveau de la couche des services métier.**Configuration Spring**Privilégier les annotations Spring à la configuration XML (moins verbeux). La configuration XML ou Java est réservée aux beans d'infrastructure et à la configuration de l'architecture applicative.**Découplage**Utiliser l'inversion de dépendances (Spring IoC).
Utiliser des types abstraits ou des interfaces.
Eviter les appels de méthodes statiques.**Thread-safe**Les ressources partagées entre 2 requêtes HTTP doivent être synchronisées.
Attention aux beans Spring de portées singleton et prototype avec états.**Gestion des exceptions**Utiliser des exceptions vérifiées pour les erreurs fonctionnelles récupérables.
Utiliser les exceptions non vérifiées ( _RuntimeException_) pour les erreurs techniques non récupérables.
Lever des exceptions dès que nécessaire (au plus tôt). Programmation défensive, par assertions.
Traiter les exceptions au niveau le plus haut. Traiter les exceptions dans les niveaux intermédiaires que si nécessaire.**Frameworks**Utiliser les bibliothèques et frameworks référencés dans le catalogue des normes et standards l’EntrepriseL'ajout de dépendances tierces est soumise à dérogation et se devra d’être justifié.**Singleton**Ne pas utiliser le pattern Singleton.
Laisser Spring gérer le cycle de vie des objets (beans de portée singleton)**Logs applicatifs**Messages de logs pertinents et contextualisés.
L’encapsulation d’une exception apporte des informations complémentaires sur le contexte d’appel.
Login de l’utilisateur affiché systématiquement grâce au MDC de SLF4J.Ne pas logger 2x la même erreur.Seules les erreurs techniques sont loggés avec le ERROR.**Découpage en couches**Respect du découpage en 3 couches : Contrôleur => Services métiers => DAO/Repository.
Les services métiers et les DAO sont déclarés dans le contexte root.
Les contrôleurs Spring MVC sont quant à eux déclarés dans un contexte enfant.

## Performances

**Rubrique**Description**Web Service**Limiter le nombre d'appel de WS.Echouer rapidement (timeout faible).**Base de données**Maitriser le nombre de requêtes SQL exécutés par un DAO.
Utiliser des index.
Eviter les recherches de type like commençant par un %.Lorsque la pagination n’est pas utilisée, toujours limiter le nombre de résultats remontés par une requête.**Cache**L'utilisation du cache Hibernate ou d'un cache applicatif doit être motivée. Les gains doivent pouvoir être mesurés.
L'application doit fonctionner lorsque le cache est désactivé.**Mapping Objet-Objet**Les mappings entre DTO doivent être réalisés manuellement en Java.
L'utilisation de frameworks comme Dozer ou Orika est proscrite.

## Tests unitaires

**Rubrique**Description**Règles d’or**Aussi important que du code de production.
Permet de documenter le code.Utiliser des noms de méthode qui documentent le TU.Un scénario par méthode de test.**Périmètre**Tester les cas limites.
Tester les exceptions.
Tester les requêtes SQL.
Un test sans assertion ne vaut (presque) rien.**DAO / Repository**DbUnit (ou DbSetup) et une base de données embarquées peuvent être utilisée pour tester les DAO.

## Sécurité

**Rubrique**Description**SQL**Utiliser des _PreparedStatement_ avec JDBC.**Logs**Ne pas logger des données sensibles.**Web**Les applications web sont sécurisées avec Spring Security.
Valider systématiquement les données saisies par l'utilisateur.
Un utilisateur ne doit pas pouvoir escalader ses propres privilèges en forgeant sa propre requête HTTP.

## Conclusion

Cette check-list n’est sans doute pas exhaustive. Qui plus est, vous ne serez sans doute pas d’accord avec tous ces principes. **Libre à vous de la personnaliser** en fonction de vos contraintes techniques et de vos règles d’architecture. N’hésitez pas non plus à l **aisser vos commentaires** afin d’en débattre. En fonction de vos retours, je complèterai/amenderai ce billet.
