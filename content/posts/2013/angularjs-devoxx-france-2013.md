---
_edit_last: "1"
author: admin
categories:
  - conférence
date: "2013-04-02T16:44:53+00:00"
toc: true
thumbnail: wp-content/uploads/2013/04/devoxxfr-2013-angularjs.jpg
featureImage: wp-content/uploads/2013/04/devoxxfr-2013-angularjs.jpg
featureImageAlt: "Université AngularJS ou le futur du développement Web à devoxxx France 2013"
guid: http://javaetmoi.com/?p=667
parent_post_id: null
post_id: "667"
post_views_count: "20933"
summary: |-
  [![Université AngularJS ou le futur du développement Web à devoxxx France 2013](wp-content/uploads/2013/04/devoxxfr-2013-angularjs.jpg)](wp-content/uploads/2013/04/devoxxfr-2013-angularjs.jpg)

  A deux semaines de sa première formation en entreprise sur **AngularJS**, répétition générale pour Thierry Chatel devant 200 développeurs avides d’en apprendre un peu plus sur le dernier né des frameworks JavaScript de **Google**. Développeur Java / Swing chez IBM au début des années 2000, Thierry s’est ensuite dirigé vers du conseil en architecture avant de découvrir AngularJS durant l’été 2011. Depuis, il y consacre beaucoup d’énergie et anime notamment le site [FrAngular.com](http://www.frangular.com/), premier blog francophone dédié à ce framework.
  Assez parlé de sa personne, lui-même n’en serait que trop gêné.

  Comme de nombreux développeurs venus assister à cette conférence, j’étais curieux de découvrir à mon tour le framework qui avait fait autant parlé de lui lors de Devoxx World 2012. Et autant vous l’annoncer dès maintenant : je n’ai pas été déçu.

  D’une durée de 3h, cette Université intitulée **[AngularJS, ou le futur du développement Web](http://www.devoxx.com/display/FR13/AngularJS%2C+ou+le+futur+du+developpement+Web)** s’est décomposée en une première partie théorique suivie d’une seconde plus pratique basée sur différents types d’applications : [Last Tweets](http://jsfiddle.net/tchatel/4FNeB/), [directive Google Maps](http://plnkr.co/edit/gn1jVW?p=preview) et [Game Store](https://github.com/tchatel/angular-gamestore). Live coding et démos furent au rendez-vous.
  Pour la petite anecdote, [les slides de la présentation](http://tchatel.github.com/slides-angularjs/) sont écrits avec la syntaxe Markdown et sont interprétés par l’outil [Angular Showoff](https://github.com/tchatel/angular-showoff) reposant, vous l’aurez deviné, sur Angular. L’intérêt majeur est qu’ils peuvent embarquer du code Angular, pratique pour les démos in-slides telles que :

  ```xhtml
  Your name:
  Hello {{me}}!
  ```

  ![Université AngularJS ou le futur du développement Web à devoxxx France 2013](wp-content/uploads/2013/04/devoxxfr-2013-angularjs.jpg)
tags:
  - angularjs
  - devoxx
  - javascript
title: AngularJS à Devoxx France 2013
url: /2013/04/angularjs-devoxx-france-2013/

---
[![Université AngularJS ou le futur du développement Web à devoxxx France 2013](wp-content/uploads/2013/04/devoxxfr-2013-angularjs.jpg)](wp-content/uploads/2013/04/devoxxfr-2013-angularjs.jpg)

A deux semaines de sa première formation en entreprise sur **AngularJS**, répétition générale pour Thierry Chatel devant 200 développeurs avides d’en apprendre un peu plus sur le dernier né des frameworks JavaScript de **Google**. Développeur Java / Swing chez IBM au début des années 2000, Thierry s’est ensuite dirigé vers du conseil en architecture avant de découvrir AngularJS durant l’été 2011. Depuis, il y consacre beaucoup d’énergie et anime notamment le site [FrAngular.com](http://www.frangular.com/), premier blog francophone dédié à ce framework.
Assez parlé de sa personne, lui-même n’en serait que trop gêné.

Comme de nombreux développeurs venus assister à cette conférence, j’étais curieux de découvrir à mon tour le framework qui avait fait autant parlé de lui lors de Devoxx World 2012. Et autant vous l’annoncer dès maintenant : je n’ai pas été déçu.

D’une durée de 3h, cette Université intitulée **[AngularJS, ou le futur du développement Web](http://www.devoxx.com/display/FR13/AngularJS%2C+ou+le+futur+du+developpement+Web)** s’est décomposée en une première partie théorique suivie d’une seconde plus pratique basée sur différents types d’applications : [Last Tweets](http://jsfiddle.net/tchatel/4FNeB/), [directive Google Maps](http://plnkr.co/edit/gn1jVW?p=preview) et [Game Store](https://github.com/tchatel/angular-gamestore). Live coding et démos furent au rendez-vous.
Pour la petite anecdote, [les slides de la présentation](http://tchatel.github.com/slides-angularjs/) sont écrits avec la syntaxe Markdown et sont interprétés par l’outil [Angular Showoff](https://github.com/tchatel/angular-showoff) reposant, vous l’aurez deviné, sur Angular. L’intérêt majeur est qu’ils peuvent embarquer du code Angular, pratique pour les démos in-slides telles que :

```xhtml
Your name:
Hello {{me}}!
```

## La fonctionnalité clé

La fonctionnalité phare que recherchait notre speaker dans un framework JavaScript était le **data** **binding bi-directionnel** entre le modèle et les vues. C’est donc ce qu’il a particulièrement apprécié dans Angular et mis en avant dès le début de sa présentation.
Par data binding bi-directionnel, on entend qu’une mise à jour du modèle JavaScript soit répercutée sur l’IHM et, inversement, qu’une interaction de l’utilisateur (ex : saisie dans un champ texte) soit aussitôt reflétée dans le modèle. C’est le comportement que l’on retrouve typiquement côté serveur avec des technologies telles JSF entre la vue xhtml et les beans managés.
La majorité de ses concurrents JavaScript n’assurent le binding que dans un seul sens : des données du modèle vers la vue HTML. En général, l’opération inverse doit être implémentée manuellement en JavaScript en s’abonnement aux évènements du DOM, par exemple à l’aide de JQuery.
Angular permet de gérer nativement ce binding qui, jusque-là, faisait défaut au HTML. Concrètement, cela se traduit par drastiquement **moins de code JavaScript de manipulation du** **DOM** et, implicitement, une compréhension du code et une maintenance facilitée. Je confirme que, dans les applications présentées lors de ce show, nous n’avons pas vu une ligne de ce type de code.
Autre aspect en faveur d’Angular : le modèle JavaScript ainsi que les différents services JS écrits par le développeur ne requièrent aucune adhérence avec Angular. On retrouve le côté POJO de Java et des beans Spring. C’est ce qui donne son petit côté magique au framework.

## Le mécanisme

Le mécanisme sous-jacent au data binding est introduit par Thierry au travers du slogan d’Angular **« HTML enhanced for webapps »**. En effet, le parti pris d’AngularJS est d’étendre le HTML, de l’enrichir avec des **directives** Angular, à savoir des tags et des attributs supplémentaires ainsi que des expressions entre {{double accolades}}. La page HTML fait elle-même office de Template.
Au démarrage de l’application, lors d’une phase de compilation, le framework parcourt le DOM à la recherche de ces balises puis instrumente le code HTML afin d’assurer le binding.  A partir de ce point, modèles et vues sont synchronisés en continue.
La force d’Angular réside dans le fait qu’il n’est nul besoin d’utiliser JavaScript pour déclarer un template. C’est la page HTML qui est étendue pour jouer ce rôle.

Sous le capot d’Angular, la détection des changements côtés vue s’appuie sur des évènements du DOM (ex : onclick, onkeyup) ou extérieurs (ex : timeout, réponse Ajax).
Par contre, les modifications du modèle sont détectées par un mécanisme bien spécifique : le **dirty checking**. A ce que j’en ai compris, il permet de surveiller tout objet JavaScript, de détecter qu’une valeur a changé puis d’exécuter du code JS. J’entrevoie une similitude avec le fonctionnement d’Hibernate qui surveille les changements opérés sur les objets attachés à sa session, ceci pour les refléter en base de données.

Le dirty checking s’appuie sur des **watches**, des listeners à l’écoute des changements. Lors de la compilation du template, Angular positionne automatiquement des watches sur les expressions et les tags HTML bindés avec un modèle. Pour des problématiques de performance, Thierry nous alerte sur le fait que l’expression surveillée ne doit pas être trop couteuse à évaluer.
Pour les objets « non managés » par Angular (issus par exemple d’API tierces), le développeur peut déclarer des watches de manière impérative.  Cette possibilité a été illustrée lors du développement d’une directive Angular utilisant l’API Google Maps. Le but était de surveiller le déplacement du centre de la carte via la souris de l’utilisateur et, le cas échéants, de mettre à jour les 2 champs de saisie correspondant à la latitude et la longitude, champs par ailleurs modifiables au clavier.

Syntaxe utilisée pour ajouter un watcher :

```js
scope.$watches('center', function () { map.setCenter(scope.center); }, true);
```

L’objet center possédant 2 propriétés, le paramètre booléen _true_ précise à Angular qu’il doit surveiller l’objet en profondeur.

Pour terminer sur ce sujet, notre orateur nous laisse rêveur en nous annonçant que ce mécanisme de dirty-checking est à l’étude au sein du W3C sous le nom de Object.observe() et que certaines versions avant-gardistes de navigateurs telles Chrome Canari ou Chronium l’implémentent déjà nativement, multipliant ainsi par 20 les performances actuelles du dirty-checking d’Angular.

## Les autres concepts

Bien entendu, la force d’Angular ne se limite pas au seul data binding bi-directionnel. Le framework met à disposition de nombreux concepts bien connus des développeurs Java :

- **MVC** : le pattern Modèle Vue Contrôleur fait partie intégrante d’Angular. Le HTML enrichi représente la vue. Des actions positionnées sur la vue permettent de faire appel à des contrôleurs JavaScript. Ces derniers exécutent le code applicatif puis mettent les données à disposition de la vue par l’intermédiaire d’un **contexte**. Thierry nous explique que les contrôleurs peuvent fonctionner sans la vue, ce qui est intéressant pour les tests. Une mauvaise pratique est donc de manipuler le DOM dans le contrôleur. Il nous rappelle aussi que le pattern MVC permet d’avoir plusieurs vues pour les mêmes contrôleurs / données ; une vue pouvant ainsi être dédiée aux appareils mobiles.
- **Injection de dépendance** : les amateurs de Spring, de Guice ou de CDI retrouveront avec plaisir ce pattern dans Angular. Lors de l’appel d’une méthode d’un contrôleur, Angular lui injecte en paramètre les services dont il a besoin. Ces services peuvent être fournis par Angular (ex : $http pour des appels REST) ou par le développer qui les aura préalablement configurés à l’aide d’un provider. Pour les curieux, Thierry rentre dans le détail de l’implémentation en expliquant qu’Angular se base sur la signature des méthodes pour déterminer le service à injecter. Le nom des paramètres est interprété comme le nom du service à injecter. Cette approche pose problème lorsque le code JS est minifié. Il devient alors nécessaire de déclarer explicitement le nom des services à injecter en passant par un tableau de chaînes de caractères.
- **Service** : tout objet JS peut être mis à disposition du reste de l’application  en tant que service. Outre le fait de pouvoir mutualiser du code faisant, par exemple, appel à des services REST du backend, les services permettent de conserver des données entre 2 contrôleurs. Thierry prend l’exemple d’un panier d’achat issu de l’application [Game Store](https://github.com/tchatel/angular-gamestore).
- **Navigation**: la navigation entre les différentes vues s’appuie sur le mécanisme de **routes** bien connu des développeurs PlayFramework. Boutons précédents, suivants et marque-pages sont gérés nativement.
- **Scope**: en Java, que ce soit en JSF ou avec Spring, les beans ont une portée (un scope). Dans Angular, cette notion prend un autre sens. Il faut le voir comme un contexte d’exécution qui peut être propre à une directive Angular. Les scopes sont utilisés lors de l’évaluation des  {{ expressions }}. Lorsque l’objet référencé n’est pas présent dans le contexte courant, Angular va le chercher dans le contexte englobant, et ainsi de suite, en remontant la hiérarchie dans le DOM. Cela me fait penser aux EL de l’API Servlet qui utilisent dans l’ordre les portées page, request, session et application.
- **Filtre**: dans Angular, les filtres ne sont pas à rapprocher des filtres JavaEE ou Spring Security, mais aux pipes Unix. Thierry a utilisé un filtre pour parser le texte d’un tweet et y ajouter une balise <a> lorsqu’une URL est détectée. Angular semble disposer d’un ensemble de filtres prêts à l’emploi.

## Les tests

Lors de cette présentation, l’outillage concernant les tests n’a pas été oublié.
Pour les tests fonctionnels, [Karma](http://karma-runner.github.com/) (ex-Testacular) permet d’exécuter des tests dans les navigateurs connectés à l’outil. Une démo a été réalisée sous nos yeux avec Chrome, Firefox, IE et depuis un Smartphone. Karma présente l’avantage d’utiliser le moteur JavaScript des différents navigateurs connectés.
Tel [infinitest](http://infinitest.github.com/), Karma relance les tests à chaque sauvegarde du code.
Créé par Vojta Jína, développeur principal d’Angular, Karma connait le fonctionnement d’AngularJS. Cela lui permet de résoudre de manière transparente le problème des requêtes Ajax souvent rencontré dans les tests Selenium.

Du point de vue des tests unitaires, Angular permet de tester des contrôleurs et des services JS nécessitant de faire appel à un serveur. Pour se faire, Angular fourni le mock object _\_$httpBackend\__ qui permet de simuler un appel au serveur et de retourner le jeu de données nécessaire au test (ex : au format JSON).

Enfin, dans le cadre d’un débogage, le [plugin Batarang pour Chrome](https://chrome.google.com/webstore/detail/angularjs-batarang/ighdmehidhipcmcojjgiloacoafjmpfk) facilite l’inspection du DOM et des scopes.

## La cible

D’après notre speaker, Angular cible avant tout les applications de gestion qui font habituellement recourt à de multiples champs de saisie.
Dédié aux applications mono-pages (SPA), il ne le recommande pas pour les sites web, d’autant plus qu’ils ne seraient pas indexables dans Google. Un paradoxe.
A noter qu’Angular est un framework qui s’utilise uniquement côté client, à savoir dans le navigateur, et qui n’a donc aucun sens à être embarqué côté serveur (ex : dans Node.JS).

Encore jeune, très peu d’applications visibles sur le Net reposent sur Angular. Thierry nous cite tout de même quelques exemples :

- le nouveau manager d’OVH,
- le site de Google « Doubleclick for publisher » dédié aux professionnels de la publicité,
- et le site Youtube de la PS3.

## Les limites

Thierry nous parle de la limite des 2000 watches. Limite que l’on peut facilement dépasser si l’on n’y prête pas attention et que l’on dispose d’une machine puissante. Ce seuil est d’autant plus valable sur les mobiles. Une astuce consiste à ne surveiller que les données visibles par l’utilisateur et à désactiver les watches sur les expressions qui ne varieront jamais.

Le framework Angular ne dispose pas de composants UI. Il permet de réutiliser des composants JQuery UI, mais un adaptateur est nécessaire. Des librairies externes telles qu’ [AngularUI](http://angular-ui.github.com/) ou [AngularStrap](http://mgcrea.github.com/angular-strap/) commencent à voir le jour.

Par ailleurs, en tant que framework, Angular est particulièrement structurant. Simple librairie, JQuery l’est beaucoup moins. Une application basée sur Angular doit donc adhérer complètement à sa philosophie ; il n’est pas intéressant de n’utiliser que certaines briques. A noter tout de même qu’il est possible de n’utiliser Angular que sur une partie de son application web et de le positionner, par exemple, que sur un simple div.

Lors de la série des questions/réponses, un développeur de l’assistance fait remarquer qu’Angular demande une syntaxe spécifique pour fonctionner sous IE 7. Son fonctionnement sur d’anciens navigateurs semble donc nécessiter quelques adaptations.
Lors de cette session, certaines fonctionnalités indispensables à toute IHM n’ont pas été abordées. C’est par exemple le cas de la validation des données saisies dans les formulaires.

## Conclusion

Malgré sa jeunesse, AngularJS semble chambouler le foisonnant écosystème des frameworks JavaScript (Backbone.js, Knockout, Ember.js). Certains le voient déjà comme l’inspirateur d’ HTML 6. Avec DART, GWT et Angular, Google possède plusieurs poulains. Reste à savoir lequel sera le plus endurant ?

Pour ma part, outre l’omniprésent JQuery, je n’avais encore jamais pris le temps d’étudier l’un de ces frameworks JavaScript qui détrônent progressivement les technologies côté serveur.
Cette université m’aura conforté dans mon choix de regarder de plus près ce que propose AngularJS.
D’après Thierry, apprendre correctement le JavaScript est un pré-requis. L’apprécier en est un second. Avant d’aborder les [tutoriaux sur Angular](http://docs.angularjs.org/tutorial), je vais donc commencer pas ressortir le livre [JavaScript, gardez le meilleur](http://www.amazon.fr/JavaScript-Gardez-meilleur-Crockford-Douglas/dp/2744023280) de Douglas Crockford.

Références :

- Les slides de l’Université sur AngularJS à Devoxx France 2013 : [http://tchatel.github.com/slides-angularjs/](http://tchatel.github.com/slides-angularjs/)
- Blog francophone sur le framework AngularJS : [http://www.frangular.com/](http://www.frangular.com/)
- Tutorial du site d’AngularJS : [http://docs.angularjs.org/tutorial](http://docs.angularjs.org/tutorial)
- Concepts du framework du site officiel : [http://docs.angularjs.org/guide/concepts](http://docs.angularjs.org/guide/concepts)
- Séries de courtes vidéos réalisées par John Lindquist : [http://egghead.io/](http://egghead.io/)
- Application Last Tweets de Thierry Chatel : [http://jsfiddle.net/tchatel/4FNeB/](http://jsfiddle.net/tchatel/4FNeB/)
- Exemple de directive Google Maps de Thierry Chatel : [http://plnkr.co/edit/gn1jVW?p=preview](http://plnkr.co/edit/gn1jVW?p=preview)
- Application Game Store de Thierry Chatel : [https://github.com/tchatel/angular-gamestore](https://github.com/tchatel/angular-gamestore)
- Outil Angular Showoff utilisé pour la réalisation des slides : [https://github.com/tchatel/angular-showoff](https://github.com/tchatel/angular-showoff)
- Communauté Google+ Angular JS France : [https://plus.google.com/communities/109984348857296908402](https://plus.google.com/communities/109984348857296908402)
