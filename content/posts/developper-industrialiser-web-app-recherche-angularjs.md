---
_edit_last: "1"
author: admin
categories:
  - retour-d'expérience
date: "2014-02-09T19:13:56+00:00"
guid: http://javaetmoi.com/?p=898
parent_post_id: null
post_id: "898"
post_views_count: "18884"
summary: |-
  Au travers du billet [Elastifiez la base MusicBrainz sur OpenShift](https://github.com/angular/angular-seed/blob/master/README.md), je vous ai expliqué comment indexer dans **Elasticsearch** et avec **Spring Batch** l’encyclopédie musicale **MusicBrainz.** L’index avait ensuite été déployé sur le Cloud **OpenShift** de RedHat.{{ double-space-with-newline }}Une application HTML 5 était mise à disposition pour consulter les albums de musique ainsi indexés. Pour m’y aider, [Lucian Precup](https://twitter.com/lucianprecup) m’avait autorisé à adapter l’application qu’il avait mise au point pour l’atelier [Construisons un moteur de recherche](http://agenda2013.scrumday.fr/event/149)  de la conférence Scrum Day 2013.{{ double-space-with-newline }}Afin d’approfondir mes connaissances de l’ **écosystème JavaScript,** je me suis amusé à recoder cette **application front-end** en partant de zéro. Ce fut l’occasion d’adopter les meilleures pratiques en vigueur : framework JavaScript MV\*, outils de builds, tests,  qualité du code, packaging …{{ double-space-with-newline }}Au travers de ce article, je vous présenterai comment :

  1. Mettre en place un projet Anguler à l’aise d’ **Angular Seed**, **Node.js** et **Bower**
  2. Développer en full **AngularJS** et **Angular UI Bootstrap**
  3. Utiliser le framework **elasticsearch-js**
  4. **Internationaliser** une application Angular
  5. Tester unitairement et fonctionnellement une application JS avec **Jasmine** et **Karma**
  6. Analyser du code source JavaScript avec **jshint**
  7. Packager avec **Grunt** le livrable à déployer
  8. Utiliser l’ **usine de développement** JavaScript disponible sur le Cloud : Travis CI, Coversall.io et David

  Le code source de l’application est bien entendu [disponible sur GitHub](https://github.com/arey/angular-musicbrainz) et [testable en ligne](http://angular-musicbrainz.javaetmoi.com/).
tags:
  - angularjs
  - bootstrap
  - bower
  - elasticsearch
  - grunt
  - jasmine
  - javascript
  - jshint
  - karma
  - nodejs
  - npm
  - test
  - travis
title: Développer et industrialiser une web app avec AngularJS
url: /2014/02/developper-industrialiser-web-app-recherche-angularjs/

---
Au travers du billet [Elastifiez la base MusicBrainz sur OpenShift](https://github.com/angular/angular-seed/blob/master/README.md), je vous ai expliqué comment indexer dans **Elasticsearch** et avec **Spring Batch** l’encyclopédie musicale **MusicBrainz.** L’index avait ensuite été déployé sur le Cloud **OpenShift** de RedHat.  
Une application HTML 5 était mise à disposition pour consulter les albums de musique ainsi indexés. Pour m’y aider, [Lucian Precup](https://twitter.com/lucianprecup) m’avait autorisé à adapter l’application qu’il avait mise au point pour l’atelier [Construisons un moteur de recherche](http://agenda2013.scrumday.fr/event/149)  de la conférence Scrum Day 2013.  
Afin d’approfondir mes connaissances de l’ **écosystème JavaScript,** je me suis amusé à recoder cette **application front-end** en partant de zéro. Ce fut l’occasion d’adopter les meilleures pratiques en vigueur : framework JavaScript MV\*, outils de builds, tests,  qualité du code, packaging …  
Au travers de ce article, je vous présenterai comment :

1. Mettre en place un projet Anguler à l’aise d’ **Angular Seed**, **Node.js** et **Bower**
1. Développer en full **AngularJS** et **Angular UI Bootstrap**
1. Utiliser le framework **elasticsearch-js**
1. **Internationaliser** une application Angular
1. Tester unitairement et fonctionnellement une application JS avec **Jasmine** et **Karma**
1. Analyser du code source JavaScript avec **jshint**
1. Packager avec **Grunt** le livrable à déployer
1. Utiliser l’ **usine de développement** JavaScript disponible sur le Cloud : Travis CI, Coversall.io et David

Le code source de l’application est bien entendu [disponible sur GitHub](https://github.com/arey/angular-musicbrainz) et [testable en ligne](http://angular-musicbrainz.javaetmoi.com/).

{{< figure src="/wp-content/uploads/2014/02/angular-musicbrainz-screenshot.png" alt="Angular MusicBrainz web app screenshot" caption="Angular MusicBrainz web app screenshot" >}}

## Démarrer un projet avec Angular Seed

Hébergé sur GitHub et maintenu par les auteurs d’Angular, le projet [**angular-seed**](https://github.com/angular/angular-seed) permet de démarrer  rapidement une application Angular. Outre le **squelette applicatif**, ce projet propose :

- des **exemples de tests** unitaires et de tests dits end-to-end,
- des **scripts** .sh ou .bat permettant d’ **exécuter** ces différents types de **tests**
- un **script** JS permettant de **démarrer un serveur web** sous NodeJS

Le [README.MD](https://github.com/angular/angular-seed/blob/master/README.md) explique de manière approfondie l’organisation du projet et la nature de chaque fichier.  
Une fois ce repository cloné sous GitHub ou bien dézippé en local, il est possible de le personnaliser à sa guise.

Une alternative à angular-seed serait d’utiliser [Yo](https://github.com/yeoman/yo) pour générer le squelette de l’application, sur un principe similaire aux archetypes maven.

## Exécuter l’application

L’application blanche fournie dans Angular Seed étant une application full HTML, il n’est pas nécessaire de la déployer dans un serveur d’application JEE ou un conteneur web. **Un  simple serveur web** comme Apache ou Nginx est nécessaire.  
Les utilisateurs de **Firefox** pourront même se passer de serveur web et ouvrir directement le fichier _app/index.html_ à partir de leur disque.  
Chrome n’ayant pas cette faculté (les requêtes Ajax chargées de récupérer un fichier sur disque sont bloquées), vous pouvez utiliser le serveur web installé sur votre poste de développement.

En guise de serveur web, vous pourrez utiliser le script _scripts\\web-server.js_ pour en démarrer un en full JavaScript. Le seul pré-requis est l’ [**installation de NodeJS**](http://nodejs.org/) qui intègre le moteur JavaScript V8 de Google. A noter que NodeJS et son gestionnaire de paquets [**npm**](https://npmjs.org/) seront nécessaires dans la suite de cet article pour installer les outils, construire l’application, monter de version les dépendances ou bien encore exécuter les tests.

Une fois NodeJS installé et ajouté au PATH du système, exécuter la commande suivante pour démarrer le serveur:

```batch
D:\Dev\angular-musicbrainz>node scripts\web-server.js
Http Server running at http://localhost:8000/
```

Saisir l’URL [http://localhost:8000/app/index.html](http://localhost:8000/app/index.html) dans le navigateur de votre choix. Les requêtes HTTP apparaissent sur la console :

```batch
GET /app/index.html Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.63 Safari/537.36
GET /app/lib/bootstrap/dist/css/bootstrap.css Mozilla/5.0d (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.63 Safari/537.36
GET /app/lib/bootstrap/dist/css/bootstrap-theme.css Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.63 Safari/53
GET /app/lib/angular-resource/angular-resource.js Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.63 Safari/537.
…
```

## Structuration du projet

La structure des répertoires du projet reprend celle d’Angular Seed.  Le tableau ci-dessous liste les librairies tierces utilisées par l’application.

**Répertoires / fichiers****Description****app/**Code source et ressources de l’application**css/**Feuilles de styles CSS**i18n/**Fichiers JSON de traduction de l’application**img/**Images et icône**index.html**Page principale de la Single Page Application**js/**Fichiers JavaScript spécifiques à l’application**app.js**Déclaration des modules et démarrage de l’application**controllers.js**Contrôleurs Angular spécifiques à l’application**directives.js**Directives Angular spécifiques à l’application**filters.js**Filtres / formateurs Angular spécifiques à l’application**routes.js**Configuration des routes**services.js**Services spécifiques à l’application**lib/**Librairies tierces déclarées dans bower.json**angular/**Module principal d’Angular**angular-i18n/**Fichiers de traductions fournis par Angular**angular-mocks/**Mocks permettant de bouchonner des services Angular**angular-resource/**Accès REST aux ressources serveur**angular-route/**Routage des vues en fonction de l’URL**angular-sanitize/**Filtres standards**angular-scenario/**DSL des scénarios de tests end-to-end**angular-ui-boostrap-bower/**Widgets Angular basés sur Bootstrap**bootstrap/**Mise en page et charte graphique**elasticsearch-js/**Client JavaScript pour Elasticsearch**jquery/**Manipulation de DOM**partials/**Template HTML des vues de l’application**directives/**Template HTML des directives de l’application**conf/**Configuration Karma des tests unitaires et e2e**dist/**Répertoire de destination du livrable de production**node\_modules/**Modules NodeJS utilisées par Grunt**scripts/**Scripts shell, JS et batch permettant de lancer les tests et de démarrer un serveur web**test/**Code source des tests**e2e/**Tests end-to-end**unit/**Tests unitaires

## Automatisation avec Grunt

**[Grunt](http://gruntjs.com/)** peut être comparé au [Gradle](http://www.gradle.org/) du monde JavaScript. Il permet d’exécuter des tâches sous NodeJS et est particulièrement utile pour automatiser certaines tâches de développement. Son installation nécessite une seule commande :  
npm install -g grunt-cli

Le gestionnaire **npm** permet ensuite de télécharger et d’installer les modules NodeJS nécessaires au fonctionnement du script Grunt. Commande à exécuter à la racine du répertoire, au même niveau que le fichier [package.json](https://github.com/arey/angular-musicbrainz/blob/master/package.json "package.json") :  
npm install

Le sous-répertoire _node\_modules_ est alimenté par les modules déclarés dans le fichier [package.json](https://github.com/arey/angular-musicbrainz/blob/v1.0/package.json).

Angular Seed ne configurant pas Grunt, je me suis inspiré de [différents exemples](http://gruntjs.com/sample-gruntfile) pour mettre au point le [script Gruntfile.js](https://github.com/arey/angular-musicbrainz/blob/v1.0/package.json).

Voici quelques commandes utiles :

- **grunt test**: lance successivement les tests unitaires et les tests end-to-end
- **grunt server**: démarre un serveur web, ouvre la page dans l’application et, à l’instar de JRebel, recharge à chaud le code modifié depuis votre IDE.
- **grunt jshint**: vérifie que la qualité du code de production JavaScript
- **grunt build**: construit le livrable à installer sur le serveur web. Les fichiers générés sont mis à disposition dans le sous-répertoire _dist_.
- **grunt karma:coverage**: génère le taux de couverture des tests unitaires. Au format HTML, le rapport est accessible depuis le sous-répertoire _coverage\\PhantomJS 1.9.2 (Windows 7)\\lcov-report_

Pendant le développement de l’application web, à des fins de débogage, le code JavaScript est non minifié et séparé dans plusieurs fichiers, de même pour les feuilles de style CSS.  
Sur un principe similaire à ce que propose [Jawr](https://jawr.java.net/) dans le monde Java, l’étape de build va permettre d’obtenir un livrable le plus léger possible. Voici les opérations effectuées :

1. Le code JavaScript et les feuilles de styles CSS sont concaténées puis minifiés. Exemple de directive à placer dans le code HTML :  

   ```default
   Directive build:js sur la page index.html
   ```



1. Les images bitmaps et vectorielles sont réduites.
1. Les pages HTML référençant ces ressources statiques sont mises à jour en conséquences.

## Dépendances Bower

Comme vu au paragraphe précédent, les modules nécessaires au fonctionnement de l’infrastructure de build basé sur Grunt sont récupérés à l’aide de npm et du fichier package.json.

Les librairies nécessaires au développement de l’application (Angular, Bootstrap) et de ses tests sont gérées par un second système de dépendances, à savoir [**Bower**](http://bower.io/). Cet outil permet de rechercher des librairies via la commande  **_bower search <nom-librairie>_**. L’instruction **_bower install <nom- librairie> –save(-dev)_** permet de la télécharger et de la référencer dans le fichier **[bower.json](https://github.com/arey/angular-musicbrainz/blob/v1.0/bower.json)**. Les librairies sont installées dans le répertoire _app/lib_ configuré dans le fichier [.bowerrc](https://github.com/arey/angular-musicbrainz/blob/v1.0/.bowerrc).

S'appuyant sur le fichier [bower.json](https://github.com/arey/angular-musicbrainz/blob/master/bower.json "bower.json"), la commande **_bower install_** permet de récupérer toutes les dépendances utilisées par l’application. Elle permet également de mettre à jour les dépendances lors d’une montée de version.

En théorie, il n’est pas nécessaire d’archiver ces dépendances dans le gestionnaire de code source (ici GitHub). En pratique, c’est utile de pouvoir exécuter l’application sans avoir à installer ni NodeJS ni Bower.

## Architecture applicative

En avril 2013, je découvrais Angular à Devoxx France. Je vous en [présentais ici même les mécanismes et les fonctionnalités clés](/2013/04/angularjs-devoxx-france-2013/). Après m’être auto-formé et avoir animé un workshop sur ce framework, j’étais impatient de le mettre en œuvre sur un projet personnel (en attendant un futur projet pro). Et autant vous l’annoncer dès à présent, je n’ai pas été déçu : j’ai pris un réel plaisir à développer le front end de mon application de recherche angular-musicbrainz.

D’un point de vue de l’architecture applicative, cette single page application est composée de **3 fichiers HTML** principaux :

1. [index.html](https://github.com/arey/angular-musicbrainz/blob/v1.0/app/index.html) : bootstrape l’application en initiant le gabarit HTML (essentiellement le menu) et en téléchargeant les fichiers JavaScript, HTML et CSS nécessaires à son fonctionnement
1. [partials\\search.html](https://github.com/arey/angular-musicbrainz/blob/v1.0/app/partials/search.html) : vue de recherche et de restitution des résultats. C’est l’implémentation de cette vue que nous allons présenter dans la suite de se billet.
1. [partials\\info.html](https://github.com/arey/angular-musicbrainz/blob/v1.0/app/partials/info.html) : vue référençant quelques URLs utiles.

Le code JavaScript de l’application est découpé techniquement. A une couche technique (contrôleurs, services, filtres et directives) correspond un fichier JavaScript et un module Angular.  
Simple,  cette organisation est pratique pour de petites applications. Sur des applications plus conséquences, [un découpage fonctionnel est à privilégier](https://medium.com/opinionated-angularjs/9f01b594bf06s).

### Services

L’application repose sur 4 **services** implémentés dans le fichier [services.js](https://github.com/arey/angular-musicbrainz/blob/v1.0/app/js/services.js):

**Nom du service****Fonctionnalités****es**Crée et configure un client Elasticsearch. S’appuie sur la fabrique mise à disposition par la librairie [elasticsearch-js](http://www.elasticsearch.org/guide/en/elasticsearch/client/javascript-api/current/index.html).**searchService**Code métier regroupant les requêtes JSON de recherche Elasticsearch. 2 méthodes sont disponibles : l’une pour la recherche full text et l’autre pour l’auto-complétion.**userLanguage**Permet d’accéder à la locale de l’utilisateur.**translation**Récupère le fichier de traduction de l’application.

### Filtres

Les templates HTML reposent sur 5 **filtres** personnalisés

**Nom du filtre****Utilisation****Rendu****interpolate**{ 'v%VERSION%' \| interpolate }V1.0**joinBy**{{hit.\_source.tags \| joinBy:' - '}}pop - rock - blues**reverse**ng-repeat="rating in facets.rating.entries \| reverse"[![angular-musicbrainz-rating](/wp-content/uploads/2014/02/angular-musicbrainz-rating.png)](/wp-content/uploads/2014/02/angular-musicbrainz-rating.png)**artistTypeLabel**{{type.term \| artistTypeLabel}}Artiste (fr) ou Artist (en)**yearFormat**{{range \| yearFormat}}Avant 1970 (fr)

Pour les détails d’implémentation, se référer au code source [filters.js](https://github.com/arey/angular-musicbrainz/blob/v1.0/app/js/filters.js) et aux tests unitaires qui les documentent [filterSpecs.js.](https://github.com/arey/angular-musicbrainz/blob/v1.0/test/unit/filtersSpec.js)

### Directives

2 **widgets graphiques** ont été réalisés à l’aide de **directives**:

**Directive****Utilisation****Rendu****Cover**<cover album-id="hit.\_source.id"> </cover>[![angular-musicbrainz-cover](/wp-content/uploads/2014/02/angular-musicbrainz-cover.png)](/wp-content/uploads/2014/02/angular-musicbrainz-cover.png)**Rank**<rank score="hit.\_source.rating.score"> </rank>[![angular-musicbrainz-rank](/wp-content/uploads/2014/02/angular-musicbrainz-rank1.png)](/wp-content/uploads/2014/02/angular-musicbrainz-rank1.png)

A noter que la [directive rating d’Angular Bootsrap](http://angular-ui.github.io/bootstrap/#/rating) offre une alternative à la directive rank. Cette dernière reprend la CSS de [MusicBrainz](http://musicbrainz.org/artist/a3cb23fc-acd3-4ce0-8f36-1e5aa6a18432/ratings) permettant d’ajuster le dégradé des étoiles au pixel près.

Afin de rendre le code des directives plus lisible et maintenable, les templates HTML de ces 2 directives ont été externalisés dans des fichiers html dédiés.  
Exemple [rating.xml](https://github.com/arey/angular-musicbrainz/blob/v1.0/app/partials/directives/rating.html) :

```markup
<span class="inline-rating">
  <span class="star-rating small-star">
     <span style="width:{{score+ceil}}%;" class="current-rating">{{score}}</span>
  </span>
</span>
```

La configuration des tests unitaires Karma a dû être ajustée en conséquences :

```java
// generate js files from html templates to expose them during testing.
   preprocessors : {
        'app/partials/directives/**/*.html': ['ng-html2js']
    },

```

### Contrôleurs

A  chaque vue de l’application, correspond un **contrôleur**. Le fichier [controller.js](https://github.com/arey/angular-musicbrainz/blob/v1.0/app/partials/directives/rating.html) en défini donc deux : _SearchCtrl_ et _InfoCtrl_.  
Trivial, le contrôleur _InfoCtrl_ met à disposition dans le scope de le **vue _info_** les 2 URLs affichées et formatées  à l’aide de la directive Angular [ngLinky](http://docs.angularjs.org/api/ngSanitize.filter:linky)

Contrôleur :

```js
$scope.demoUrl = 'http://angular-musicbrainz.javaetmoi.com/';
```

Template :

```xhtml
<li>Online Demo: <span ng-bind-html="demoUrl | linky"/></li>
```

Le **contrôleur _SearchCtrl_** embarque toute la logique applicative de l’application. Il offre à la fois des **fonctions** réagissant aux actions utilisateurs et les **données** utilisées par Angular lors du rendu de la **vue _search_**. En voici les principales :

**Propriété****Type****Description****fullTextSearch**fonctionExécute une recherche full text lors du clic sur le bouton « Recherche MusicBrainz».**autocomplete**fonctionExécute une requête d’auto-complétion à chaque frappe de l’utilisateur dans le zone de recherche.**selectPage**FonctionPermet à l’utilisateur de sélectionner une plage de résultats. Exécute une recherche Elasticsearch sur la plage indiquée.**searchResp**DonnéeRésultats Elasticsearch d’une recherche fulltext.**pageSize**DonnéeNombre de résultats à afficher à l’écran.**currentPage**DonnéePlage de résultats actuellement affichée.**pageSizes**DonnéeTailles de plages que l’utilisateur peut choisir.

### Routes

Par rapport au template angular-seed, la **configuration des routes** a été externalisée dans un fichier dédié [routes.js](https://github.com/arey/angular-musicbrainz/blob/v1.0/app/js/routes.js).

### **Application  
**

Le 6ième et dernier module Angular correspond  **au module applicatif** **_musicAlbumApp_** déclaré dans le fichier [app.js](https://github.com/arey/angular-musicbrainz/blob/v1.0/app/js/app.js). Outre la déclaration des **modules Angular** nécessaires au fonctionnement de l'application, ce module est chargé de déterminer la langue dans laquelle l'interface doit s'afficher puis charger les données adéquates. Nous y reviendrons dans la suite de cet article.

## Utilisation d’elasticsearch-js

Pour interroger le cluster Elasticsearch depuis le navigateur, j’ai étudié 3 possibilités : le [service natif $http](http://docs.angularjs.org/api/ng.$http) d’Angular, la librairie [elastic.js](http://www.fullscale.co/elasticjs/) et la librairie **[elasticsearch-js](https://github.com/elasticsearch/elasticsearch-js)**. Sortie en décembre 2013 et [mise en avant par Elasticsearch.org](http://www.elasticsearch.org/blog/client-for-node-js-and-the-browser/), j’ai choisi d’utiliser cette dernière. Via la création de [tickets GitHub](https://github.com/elasticsearch/elasticsearch-js/issues/created_by/arey), j’ai eu la chance de pouvoir  contribuer à l’amélioration de cette jeune librairie déjà très mature.

Le **module esFactory** permet de déclarer en quelques lignes un client JavaScript Elasticsearch. Voici les paramètres renseignés :

```java
angular.module('musicAlbumApp.services', ['ngResource'])
    .value('version', '1.0')
    // elasticsearch.angular.js creates an elasticsearch
    // module, which provides an esFactory
    .service('es', ['esFactory', function (esFactory) {
        return esFactory({
            hosts: [
                // you may use localhost:9200 with a local Elasticsearch cluster
                'es.javaetmoi.com:80'
            ],
            log: 'trace',
            sniffOnStart: false
        });
    }])
```

J’ai volontairement désactivé la fonctionnalité de **sniffOnStart**. En effet, j’ai configuré le reverse proxy Nginx pour ne laisser passer que les requêtes de _\_search_. Les requêtes HTTP de type HEAD envoyées par le client pour déterminer la disponibilité des différents nœuds du cluster étaient donc rejetées.

L’appel au service de recherche Elasticsearch est également très simple. Dans l’attribut _body_ de la fonction _[search](http://www.elasticsearch.org/guide/en/elasticsearch/client/javascript-api/current/api-reference-1-0.html#api-search-1-0)_ proposée par l’API, est utilisé le formalisme standard de déclaration des requêtes au format JSON. En complément, les attributs _index_ et _type_ permettent respectivement d’indiquer sur quel index Elasticsearch et sur quel type de document lancer la recherche. Voici un exemple d’appel :

_Extrait méthode fullTextSearch_

```java
.factory('searchService', ['es', function (es) {
        return {
            'fullTextSearch': function (from, size, text) {
                return es.search({
                    index: 'musicalbum',
                    type: 'album',
                    body: {
                        'from': from,
                        'size': size,
                        'query': {
                            'bool': {
                                'must': [
                                    {
                                        'fuzzy_like_this': {
                                            'fields': [
                                                'name',
                                                'artist.name',
                                                'year.string'
                                            ],
                                            'like_text': text,
                                            'min_similarity': 0.7,
                                            'prefix_length': 1
                                        }
                                    }
                                ]
                            }
                        },
                        'facets': {
                            'artist_type': {
                                'terms': {
                                    'field': 'artist.type_id'
                                }
                            },
                            'album_rating': {
                                'histogram': {
                                    'key_field': 'rating.score',
                                    'interval': 21
                                }
                            },
                            'album_year': {
                                'range': {
                                    'field': 'year',
                                    'ranges': [
                                        { 'to': 1970},
                                        {  'from': 1970, 'to': 1980},
                                        {  'from': 1980, 'to': 1990},
                                        {  'from': 1990, 'to': 2000},
                                        {  'from': 2000, 'to': 2010},
                                        {  'from': 2010 }
                                    ]
                                }
                            }
                        }
                    }
                });
            },
```

La fonction _[search](http://www.elasticsearch.org/guide/en/elasticsearch/client/javascript-api/current/api-reference-1-0.html#api-search-1-0)_ renvoie une promesse de réponse. Pour récupérer la réponse retournée par Elasticsearch, la méthode _then_ peut être utilisée :

```js
searchService.fullTextSearch(from, $scope.pageSize.count, text).then(
                function (resp) {
                    $scope.searchResp = resp;
                    $scope.totalItems = resp.hits.total;
searchService.fullTextSearch(from, $scope.pageSize.count, text).then(
    function (resp) {
        $scope.searchResp = resp;
        $scope.totalItems = resp.hits.total;
    }
);
```

## Localisation

Le **[service $locale](http://docs.angularjs.org/guide/i18n)** d’Angular permet de formater les nombres et les dates en fonction des préférences linguistiques de l’utilisateur. Il existe autant de fichiers JavaScript que de combinaisons langue / pays (exemples : _angular-locale\_fr-fr.js_, _angular-locale\_en-us.js_).

Pour charger le fichier adéquat, l’application doit détecter le langage défini par l’utilisateur dans son Navigateur. A première vue, les variables du DOM _window.navigator.userLanguage_ et _window.navigator.language_ auraient dû apporter cette information. Il en aurait été trop simple. L’article [Detecting a Browser’s Language in Javascript](http://blog.dansingerman.com/post/909213798/detecting-a-browsers-language-in-javascript) explique précisément pourquoi.  
Le header HTPP **_Accept-Language_** ne peut être lue que côté serveur web. Or, l’application était jusque-là full JavaScript. Convertir la page _index.html_ en une page PHP ou JSP aurait été simple. Néanmoins, j’ai préféré m’affranchir de toute installation côté serveur. J’ai donc utilisé le service [http://ajaxhttpheaders.appspot.com](http://ajaxhttpheaders.appspot.com) mis à disposition sur Google App Engine et dont voici un exemple d’utilisation :

```js
$http.jsonp('http://ajaxhttpheaders.appspot.com?callback=JSON_CALLBACK').
success(function (data) {
    var acceptLang = data['Accept-Language'];
    langRange = userLanguage.getFirstLanguageRange(acceptLang);
    language = userLanguage.getLanguage(langRange);
    if (sessionStorage) {
        sessionStorage.setItem('userLanguageRange', langRange);
    }
}).
finally(function () {
    loadI18nResources();
});
```

Une fois la langue de l’utilisateur connue, la fonction [$.getScript](http://api.jquery.com/jquery.getscript/) de JQuery permet de charger dynamiquement le fichier JavaScript Angular correspondant.  
Afin d’éviter des appels intempestifs au service [http://ajaxhttpheaders.appspot.com](http://ajaxhttpheaders.appspot.com), la langue est conservée dans le **sessionStorage** du navigateur.  
Dans un souci d’internationalisation, l’application angular-musicbrainz a été traduite en 2 langues : le français et l’anglais. Les libellés affichés à l’écran dépendent donc des préférences utilisateurs. Le système mis en œuvre s’inspire de ce que proposent les articles [Creating multilingual support using AngularJS](http://www.novanet.no/blog/hallstein-brotan/dates/2013/10/creating-multilingual-support-using-angularjs/) et [Traduction des libellés dans les vues AngularJS](http://www.frangular.com/2012/12/traduction-des-libelles-dans-les-vues-angularjs.html). Un **objet translation** contenant la traduction de tous les libellés d’une langue est chargé à partir d’un fichier JSON puis ai mis dans le scope parent ($rootScope). Cet objet peut être accédé à la fois dans les templates HTML que côté JavaScript :

```default
<label id="search-input-label" class="col-sm-3 control-label" ng-bind="translation.SEARCH_LABEL">Searching a music album</label>
```

```js
$scope.pageSizes = [
            {count: 5, label: '5 ' + $scope.translation.SEARCH_PAGE_RESULT},

```

## Widgets graphiques

Le projet [UI Bootstrap](http://angular-ui.github.io/bootstrap/) propose une douzaine de directives Angular basées sur [Boostrap](http://getbootstrap.com/) : sélection de date avec calendrier, accordéon, onglets, barres de progression, fenêtre popup, collapse, carrousel d’images …

Notre web app de recherche utilise 3 de ses directives:

DirectiveVisuelExemple d’utilisation dans les templates HTML**typeahead**[![angular-musicbrainz-typeahead](/wp-content/uploads/2014/02/angular-musicbrainz-typeahead.png)](/wp-content/uploads/2014/02/angular-musicbrainz-typeahead.png)

```xhtml
<input type="text"
class="form-control"
ng-model="searchText"
typeahead="album for album
in autocomplete($viewValue)
| filter:$viewValue" />
```

**pagination**[![angular-musicbrainz-pagination](/wp-content/uploads/2014/02/angular-musicbrainz-pagination.png)](/wp-content/uploads/2014/02/angular-musicbrainz-pagination.png)

```xhtml
<pagination total-items="totalItems"
page="currentPage"
max-size="maxSize"
num-pages="numPages"
items-per-page="pageSize.count"
on-select-page="selectPage(page)">
</pagination>
```

**pager**[![angular-musicbrainz-pager](/wp-content/uploads/2014/02/angular-musicbrainz-pager.png)](/wp-content/uploads/2014/02/angular-musicbrainz-pager.png)

```xhtml
<pager total-items="totalItems"
page="currentPage"
on-select-page="selectPage(page)">
</pager>
```

Comme le montre les exemples ci-dessus, les directives UI Boostrap permettent d’étendre le HTML, soit par de nouveaux tags (ex: <pagination/> , soit par des attributs enrichissants des tags standards (ex : typeahead sur <input/> ).

## Tests unitaires

Avec son **découpage** en modules, la possibilité de créer des **mocks** et l’indépendance du code JavaScript au regard du DOM, Angular permet de tester unitairement chaque contrôleur, service, filtre, route et directive. Qui plus est, l’application blanche [angular-seed](https://github.com/angular/angular-seed)  vient avec toute l’infrastructure de tests : spécifications **[Jasmine](http://pivotal.github.io/jasmine/)** à compléter, configuration **[Karma](http://karma-runner.github.io/)**, scripts batch et shell permettant d’exécuter les tests. Autant dire, le développeur n’a aucune excuse pour ne pas **tester unitairement** son application.  
L’application angular-musicbrainz comptabilise **36 tests unitaires**, couvrant ainsi **65%** du code source. Avant de pouvoir exécuter les tests unitaires, il est nécessaire d’installer les quatre modules Karma suivants :

npm install -g karma karma-junit-reporter karma-ng-html2js-preprocessor karma-coverage

Les tests unitaires peuvent être exécutés de 2 manières :

1. Par la commande grunt : grunt karma
1. Ou par un script : scripts\\test.bat

Karma exécute les tests puis se met en attente de changements. En effet, tel [infinitest](http://infinitest.github.com/), Karma relance les tests à chaque modification du code source ou des tests. Cela s’avère très pratique pour lever au plus tôt toute régression ou bien travailler en TDD.

Autre aspect de Karma : il permet de faire tourner les tests simultanément dans un ou plusieurs navigateurs. Dans le fichier de configuration [karma.conf.js](https://github.com/arey/angular-musicbrainz/blob/v1.0/config/karma.conf.js), **Google Chrome** et le navigateur headless **[PhantomJS](http://phantomjs.org/)** ont été retenus.

Une fois la structuration d’un cas de test prise en main (mots clés _describe_, _beforeEach_ et _it_), l’écriture du code de tests est plus ou moins simple. La difficulté principale vient de la lourdeur de la configuration nécessaire à mettre en place pour bouchonner les adhérences. Voici par exemple comment tester la fonction _fullTextSearch_ du contrôleur _SearchCtrl_ :

```javascript
it('fullTextSearch should put the searchResp variable into the scope', function () {

            expect(scope.searchResp).toBeUndefined();
            expect(scope.isAvailableResults()).toBeFalsy();
            expect(scope.isAtLeastOneResult()).toBeFalsy();

            scope.fullTextSearch('U2', 1);
it('fullTextSearch should put the searchResp variable into the scope', function () {

    expect(scope.searchResp).toBeUndefined();
    expect(scope.isAvailableResults()).toBeFalsy();
    expect(scope.isAtLeastOneResult()).toBeFalsy();

    scope.fullTextSearch('U2', 1);

    // scope.$digest() will fire watchers on current scope,
    // in short will run the callback function in the controller that will call anotherService.doSomething
    scope.$digest();

    expect(scope.searchResp).toBeDefined();
    expect(scope.totalItems).toBeDefined();
    expect(scope.isAvailableResults()).toBeTruthy();
    expect(scope.isAtLeastOneResult()).toBeTruthy();
});

```

Le contrôleur _SearchCtrl_  s’appuie sur le service _searchService_ dont la fonction _fullTextSearch_ a dû être bouchonnée. Au final, le développeur écrit plus de code de test que de code testé.  
Espérons que le duo Karma / Jasmine gagnera en maturité avec le temps. En Java, l’utilisation des annotations [_@Mock_](http://docs.mockito.googlecode.com/hg/latest/org/mockito/Mockito.html#mock_annotation) et [_@InjectInto_](http://www.unitils.org/apidocs/org/unitils/inject/annotation/InjectInto.html) permet en effet de réduire drastiquement ce type code.

Non des moindre, le dernier point à connaître lors de l’écriture des tests concerne les assertions. Venant avec un nombre de [matchers clés en mains](https://github.com/pivotal/jasmine/wiki/Matchers), Jasmine permet d’écrire ses propres matchers.

## Tests end-to-end

A l’instar de ce que propose [Selenium](http://docs.seleniumhq.org/) dans le monde Java, Karma permet d’écrire et d’exécuter des scénarios fonctionnels. Un prérequis à leur exécution est que l’application web doit être démarrée.

Là encore, l’application blanche [angular-seed](https://github.com/angular/angular-seed)  vient avec toute l’infrastructure de tests e2e nécessaire. Comme prérequis, le module [karma-ng-scenario](https://github.com/karma-runner/karma-ng-scenario) doit être installé via npm :

npm install -g karma-ng-scenario

Les tests e2e peuvent être exécutés en ligne de commande: scripts\\e2e-test.bat

Pour l’écriture des scénarios de tests, le module [angular-scenario](http://docs.angularjs.org/guide/dev_guide.e2e-testing) fournit un DSL permettant de sélectionner des éléments du DOM et de simuler des évènements utilisateurs. A noter que le [framework Protactor](https://github.com/angular/protractor) doit remplacer à termes ce module.  
Comme le montre l’extrait de code ci-dessous, le code reste lisible :

```javascript
describe('search', function () {

    beforeEach(function () {
        browser().navigateTo('#/search');
    });

    it('should render search when user navigates to /search', function () {
        expect(element('#search-input-label').text()).
        toContain('music');
    });

    it('U2 album search', function () {
        input('searchText').enter('U2');
        element(':button').click();
        expect(element('#result-number').text()).
        toContain('22');

    });

});
```

Créé par l’un des développeurs d’Angular, Karma a l’avantage de connaître le fonctionnement interne d’Angular. Cette faculté lui permet de résoudre les problèmes de requêtes Ajax souvent rencontrés dans les tests Selenium. Adieux les tempos ou autre  [_waitForElement_](http://agilesoftwaretesting.com/selenium-wait-for-ajax-the-right-way/).

{{< figure src="/wp-content/uploads/2014/02/angular-musicbrainz-e2e.png" alt="angular-musicbrainz-e2e" caption="angular-musicbrainz-e2e" >}}

Exécution des tests end-to-end dans Chrome :  

## Contrôle qualité avec JSHint

Fork actif de [jslint](http://www.jslint.com/), **[JSHint](http://www.jshint.com/)** s’apparente au Checkstyle du monde Java. Cet outil Open Source effectue plusieurs types de vérifications sur les fichiers JavaScript :

- Conventions de nommage
- Règles de formatage
- Bonnes pratiques permettant d’éviter de potentiels bugs

Le fichier de configuration [.jshintrc](https://github.com/arey/angular-musicbrainz/blob/master/.jshintrc) permet d’activer chacune [des dizaines de règles](https://gist.github.com/haschek/2595796) proposées par JSHint. Activée sur notre projet, la règle **_curly_** vérifie par exemple s’il ne manque pas des accolades dans les boucles et les conditions.

La vérification des fichiers JavaScript peut ensuite se faire, soit en ligne de commande :

```sh
D:\Dev\angular-musicbrainz>grunt jshint
Running "jshint:all" (jshint) task
Linting app/js/services.js ...ERROR
[L140:C17] W116: Expected '{' and instead saw 'return'.
return undefined;
```

Soit directement depuis IntelliJ IDEA après configuration :

{{< figure src="/wp-content/uploads/2014/02/angular-musicbrainz-jshint.png" alt="angular-musicbrainz-jshint" caption="angular-musicbrainz-jshint" >}}

{{< figure src="/wp-content/uploads/2014/02/angular-musicbrainz-jshint2.png" alt="angular-musicbrainz-jshint2" caption="angular-musicbrainz-jshint2" >}}

JSHint a toute sa place sur un projet de grande taille sur lesquels de nombreux développeurs travaillent puis se relaieront pour sa maintenance. Sur de plus modestes applications comme angular-musicbainz , il a le mérite de former et de mettre en garde des développeurs JavaScript Junior.

## Usine de dév JavaScript

Dans le billet [Ma petite usine logicielle](/2012/12/ma-petite-usine-logicielle-github-cloudbees/), je vous expliquais comment utiliser [CloudBees](http://www.cloudbees.com/) et GitHub pour industrialiser vos projets Java. Vous l’aviez compris, l’intégration continue et l’automatisation des tâches me tiennent à cœur. J’ai donc naturellement regardé ce qui existait dans le monde JavaScript. Ce dernier n’est pas en reste. Voici ce que j’ai mis en place sur angular-musicbrainz.

Déjà mis en place sur mes projets Java avec Maven, **[Travis CI](https://travis-ci.org/)** est une plateforme d’intégration continue mise à disposition gratuitement pour les projets Open Source. Cette plateforme présente l’avantage de supporter NodeJS et peut donc intégrer des applications JavaScript.

La configuration du build Travis se trouve dans le fichier [.travis.yml](https://github.com/arey/angular-musicbrainz/blob/master/.travis.yml):

```yaml
language: node_js
node_js:
  - 0.10

before_script:
  - npm install -g grunt-cli

script:
  - grunt karma:ci

after_success:
  - grunt coverage
```

On demande à Travis d’installer le client Grunt avant d’exécuter les tests unitaires et de publier la couverture de code. A chaque commit dans le repo GitHub, le build est lancé. La sortie console s’affiche en temps réel :

{{< figure src="/wp-content/uploads/2014/02/angular-musicbrainz-travis.png" alt="angular-musicbrainz-travis" caption="angular-musicbrainz-travis" >}}


En cas d’échec du build, vous pouvez être notifiés par email , IRC, webhook ...

Outre la génération d’un rapport de couverture de code testé, la commande grunt coverage  envoie ce rapport au service **[Coveralls](https://coveralls.io/)**. Ce dernier historise le taux de couverture et offre une IHM permettant de naviguer parmi les fichiers analysés.

L’ [historique des builds du projet angular-musicbrainz](https://coveralls.io/r/arey/angular-musicbrainz) est accessible en ligne :

{{< figure src="/wp-content/uploads/2014/02/angular-musicbrainz-coveralls1.png" alt="angular-musicbrainz-coveralls1" caption="angular-musicbrainz-coveralls1" >}}


Le [taux de couverture du build n°494581](https://coveralls.io/builds/494581) est également consultable en ligne :

{{< figure src="/wp-content/uploads/2014/02/angular-musicbrainz-coveralls1.png" alt="angular-musicbrainz-coveralls1" caption="angular-musicbrainz-coveralls1" >}}


Autre service en ligne intéressant : pouvoir vérifier rapidement que les dépendances d’une application sont à jour. C’est ce que propose **[David](https://www.david-dm.org/)**. Voici visuellement la synthèse proposée par David pour les [dépendances de dev d’angular-musicbainz](https://david-dm.org/arey/angular-musicbrainz#info=devDependencies) :

{{< figure src="/wp-content/uploads/2014/02/angular-musicbrainz-david.png" alt="angular-musicbrainz-david" caption="angular-musicbrainz-david" >}}

A noter qu’un service similaire pour les dépendances utilisées par Bower serait intéressant.

Chacun de ces services propose un **badge** dynamique. Pratique, ces badges peuvent être affichés dans le README.MD :

## [![angular-musicbrainz-build-status](/wp-content/uploads/2014/02/angular-musicbrainz-build-status.png)](/wp-content/uploads/2014/02/angular-musicbrainz-build-status.png)  
Conclusion

Ce long billet m’aura permis de vous faire découvrir les différentes facettes du monde JavaScript dont j’ai fait connaissance tout au long du développement de cette petite application web de recherche.  
**L’utilisation d’Angular est plaisante et me réconcilie avec le développement** **JavaScript** que je ne trouvais jusque-là pas assez industrialisé. Diminuant le nombre de lignes de code JavaScript au profit du HTML, ce framework permet de structurer proprement le code JavaScript. Ceux qui ont connus des applications où chaque page comporte des centaines de lignes jQuery non organisées apprécieront sans aucun doute.

En quelques années, je constate avec plaisir que l’écosystème JavaScript a rattrapé son retard sur celui de Java : intégration continue, outils de builds, tests unitaires, tests fonctionnels, qualimétrie,  gestion des dépendances, MVC, data-binding, POJO, templating, injection de dépendances, modularisation, nombre grandissant de frameworks, moteur d’exécution optimisé, support IDE … Chapeau bas.
