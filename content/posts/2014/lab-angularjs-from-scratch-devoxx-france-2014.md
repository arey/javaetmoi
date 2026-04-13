---
_edit_last: "1"
author: admin
categories:
  - conférence
date: "2014-04-19T08:41:24+00:00"
toc: true
thumbnail: wp-content/uploads/2014/04/2014-04-comprendre-AngularJS-en-le-recodant-photo.jpg
featureImage: wp-content/uploads/2014/04/2014-04-comprendre-AngularJS-en-le-recodant-photo.jpg
featureImageAlt: "angular-from-scratch-devoxx-france-2014"
guid: http://javaetmoi.com/?p=1068
parent_post_id: null
post_id: "1068"
post_views_count: "11069"
summary: |-
  Lors de Devoxx France 2013, je découvrais AngularJS lors de l’Université sur AngularJS animée par Thierry Chatel. Enthousiasmé par ce framework, je vous faisais ici même [une restitution de cette Université](http://javaetmoi.com/2013/04/angularjs-devoxx-france-2013/). Depuis un an, j’ai poursuivi mon initiation en codant un [front-end pour Elasticsearch avec Angular](http://javaetmoi.com/2014/02/developper-industrialiser-web-app-recherche-angularjs/). Lorsque j’ai découvert que [Matthieu Lux](http://swiip.github.io/) et [Olivier Huber](https://twitter.com/@olivierhuber) proposaient le [**Hand’s-on-Lab** **« Angular JS from scratch : comprendre Angular en le refaisant de zéro »**](http://cfp.devoxx.fr/devoxxfr2014/talk/FWA-551/AngularJS%20from%20scratch%20:%20comprendre%20Angular%20en%20le%20re-faisant%20de%20z%C3%A9ro) à [Devoxx France 2014](http://www.devoxx.fr/), j’y ai vu l’occasion ou jamais d’approfondir mes connaissances et de découvrir les mécanismes se cachant derrière la magie d’Angular.

  [![angular-from-scratch-devoxx-france-2014](wp-content/uploads/2014/04/2014-04-comprendre-AngularJS-en-le-recodant-photo.jpg)](wp-content/uploads/2014/04/2014-04-comprendre-AngularJS-en-le-recodant-photo.jpg)

  Ce workshop a eu un beau succès : une salle comble 10 minutes avant son début et [une place sur le podium des meilleures sessions de la matinée](https://twitter.com/Swiip/status/456721029897781248/photo/1).
  Pour coder les différents exercices sans avoir à se tourner régulièrement vers les solutions, de solides connaissances en JavaScript étaient nécessaires : héritage par prototype, constructeur, portée du this, couteau suisse underscore (each, clone, isEqual) …
  Par ailleurs, pour apprécier la démarche, une connaissance minimaliste d’Angular me paraissait également indispensable.
  Durant les 3 heures du Lab, nous avons pu implémenter 11 des 12 étapes prévues initialement (la dernière étant en bonus). Timing parfaitement respecté. Si vous n’avez pas eu la chance d’assister à cette présentation et si vous disposez de 3 heures devant vous, je vous conseille de tenter de le réaliser chez vous.
  Les slides du workshop, le code source de départ, les solutions et les tests unitaires sous Jasmine sont disponibles dans le repo Github [angular-from-scratch](https://github.com/zenika/angular-from-scratch) de Zenika.

  ![angular-from-scratch-devoxx-france-2014](wp-content/uploads/2014/04/2014-04-comprendre-AngularJS-en-le-recodant-photo.jpg)
tags:
  - angularjs
  - devoxx
title: Comprendre AngularJS en le recodant à Devoxx France 2014
url: /2014/04/lab-angularjs-from-scratch-devoxx-france-2014/

---
Lors de Devoxx France 2013, je découvrais AngularJS lors de l’Université sur AngularJS animée par Thierry Chatel. Enthousiasmé par ce framework, je vous faisais ici même [une restitution de cette Université](/2013/04/angularjs-devoxx-france-2013/). Depuis un an, j’ai poursuivi mon initiation en codant un [front-end pour Elasticsearch avec Angular](/2014/02/developper-industrialiser-web-app-recherche-angularjs/). Lorsque j’ai découvert que [Matthieu Lux](http://swiip.github.io/) et [Olivier Huber](https://twitter.com/@olivierhuber) proposaient le [**Hand’s-on-Lab** **« Angular JS from scratch : comprendre Angular en le refaisant de zéro »**](http://cfp.devoxx.fr/devoxxfr2014/talk/FWA-551/AngularJS%20from%20scratch%20:%20comprendre%20Angular%20en%20le%20re-faisant%20de%20z%C3%A9ro) à [Devoxx France 2014](http://www.devoxx.fr/), j’y ai vu l’occasion ou jamais d’approfondir mes connaissances et de découvrir les mécanismes se cachant derrière la magie d’Angular.

[![angular-from-scratch-devoxx-france-2014](wp-content/uploads/2014/04/2014-04-comprendre-AngularJS-en-le-recodant-photo.jpg)](wp-content/uploads/2014/04/2014-04-comprendre-AngularJS-en-le-recodant-photo.jpg)

Ce workshop a eu un beau succès : une salle comble 10 minutes avant son début et [une place sur le podium des meilleures sessions de la matinée](https://twitter.com/Swiip/status/456721029897781248/photo/1).
Pour coder les différents exercices sans avoir à se tourner régulièrement vers les solutions, de solides connaissances en JavaScript étaient nécessaires : héritage par prototype, constructeur, portée du this, couteau suisse underscore (each, clone, isEqual) …
Par ailleurs, pour apprécier la démarche, une connaissance minimaliste d’Angular me paraissait également indispensable.
Durant les 3 heures du Lab, nous avons pu implémenter 11 des 12 étapes prévues initialement (la dernière étant en bonus). Timing parfaitement respecté. Si vous n’avez pas eu la chance d’assister à cette présentation et si vous disposez de 3 heures devant vous, je vous conseille de tenter de le réaliser chez vous.
Les slides du workshop, le code source de départ, les solutions et les tests unitaires sous Jasmine sont disponibles dans le repo Github [angular-from-scratch](https://github.com/zenika/angular-from-scratch) de Zenika.

L’objectif de ce billet est de vous accompagner dans la réalisation du Lab. Je me focaliserai sur les mécanismes qui permettent de recoder [le traditionnel « Hello Word » d’Angular](http://igorminar.github.io/ng-slides/angular-intro/#16). Vous y trouverez donc une version édulcorée du code du Lab. Garde-fous contre les boucles infinies et comparaisons par valeur n’y seront pas abordés.
Afin de mieux comprendre où s’inscrivent les différentes étapes qui permettent de réimplémenter Angular, je m’appuierai régulièrement sur le schéma présenté par Olivier au début du Lab :

[![angular-from-scratch-devoxx-france-2014-schema](wp-content/uploads/2014/04/2014-04-comprendre-AngularJS-en-le-recodant-digest.png)](wp-content/uploads/2014/04/2014-04-comprendre-AngularJS-en-le-recodant-digest.png)

Le code complet de ce billet est [disponible dans jsfiddle](http://jsfiddle.net/Elryk/gkk4m/) et également sous forme de [gist](https://gist.github.com/arey/11011876).
Afin de pouvoir plus facilement se référer au code source d’Angular, le nom des méthodes et des objets utilisés dans ce Lab reprend volontairement ceux d’Angular.

## Etape 1 : le $scope

Connu de tout développeur Angular, le **scope** est l’objet central du framework. Il permet de mettre à disposition des vues et des contrôleurs le modèle de données de l’application. Contrairement à d’autres frameworks comme Backbone, vous pouvez y placer des objets JavaScript standard (POJSO).
La particularité du scope est de pouvoir être observé. A l’instar du pattern Observer, des watchers peuvent s’enregistrer et être à l’écoute de tout changement sur le modèle, dans sa globalité ou sur une partie donnée. Les watchers sont tout simplement matérialisés par un tableau JavaScript :

```js
function Scope() {
    this.$$watchers = [];
}
```

En général, Angular instancie pour vous le scope des différentes vues composant une page.
Pour les besoins du Lab, nous l’instancions manuellement :

```js
var scope = new Scope();
```

Nous y définissons un objet labs comportant 2 propriétés :

```js
scope.labs = {
    titre: "AngularJS from scratch",
    date: new Date()
}
```

La page HTML référence le titre  objet de l’objet labs :

```xhtml
<h1 class="page-header" ng-bind="labs.titre">AngularJS from scratch</h1>
<input type="text" ng-model="labs.titre"/>
```

Nous reviendrons sur les directives _ng-bind_ et _ng-model_ lors des étapes 10 et 11.

## Etape 2 : Scope.$watch

Comme vu dans l’étape précédente, le scope contient un tableau de watchers. Le but de cette étape est d’implémenter une **fonction $watch** permettant d’ajouter un watcher dans le tableau _$$watchers_ du scope. Quiconque le souhaite pourra alors surveiller une donnée du scope.

```js
Scope.prototype.$watch = function (watcherFn, listenerFn) {
    var watcher = {
        watcherFn: watcherFn,
        listenerFn: listenerFn,
        last: undefined
    };
    this.$$watchers.push(watcher);
}
```

La fonction _$watch_ est ajoutée dans le prototype du _Scope_. Toute instance de _Scope_ hérite ainsi de cette fonction. La ligne this.$$watchers.push(watcher);  ne pose aucune difficulté.

Un watcher est caractérisé par 3 éléments :

1. une fonction _watcherFn_ indiquant quelle donnée du modèle l’appelant souhaite observer,
1. une fonction de rappel _listenerFn_ appelée lorsqu’un changement sera détecté
1. une variable interne _last_ permettant de sauvegarder la précédente valeur du modèle et de réaliser le dirty checking.

Voici un exemple d’appel à la fonction _$watch_ :

```js
scope.$watch(function (scope) {
    return scope.labs.titre;
}, function (newValue, oldValue, scope) {
    console.log("La titre a changé de", oldValue, "à", newValue);
});
```

En pratique, un développeur Angular fait rarement appel explicitement à cette méthode.

## Etape 3 et 5 : Scope.$digest et digest loop

La **fonction _$digest_** est au cœur d’Angular. Sur le schéma ci-dessus, elle représente la **digest loop**. Comme son nom l’indique, son algorithme principal consiste à boucler sur le tableau de watchers jusqu’à ce que tous les évènements aient été traités. Par évènement, on entend un changement dans le modèle.
Voici un exemple d’implémentation :

```js
Scope.prototype.$digest = function () {
    var dirty;
    do {
        dirty = false;
        _.each(this.$$watchers, function (watcher) {
            var newValue = watcher.watcherFn(this);
            if (watcher.last !== newValue) {
                watcher.listenerFn(newValue, watcher.last, this);
                watcher.last = newValue;
                dirty = true;
            }
        }.bind(this));
    } while (dirty);
}
```

Quelques explications peuvent être nécessaires à la compréhension de ce code :

- L’itération sur le tableau _$$watchers_ est réalisée par la méthode each d’Underscore
- La méthode _watcherFn_ accepte comme argument le scope à observer. Ici, un _this_ est passé en paramètre. Sans l’utilisation du _bind(this)_, ce serait le _this_ de l’inner fonction qui aurait été  passé à _watcherFn_ et non le scope sur lequel la méthode _$digest_ est appelée. _bind(this)_ est une technique native JavaScript que je ne connaissais pas. Elle permet de forcer le _this_. Une technique plus repandue est l’utilisation d’un _var self=this;_ avant la déclaration de l’inner fonction. Underscore aurait également pu être utilisé pour gérer cette problématique récurrente en JavaScript.
- Lorsqu’un changement est détecté, la fonction de rappel _listenerFn_ est appelée avec la nouvelle valeur, l’ancienne valeur et le scope.

A chaque fois qu’un _$digest_ est appelé, la fonction _watcherFn_ de tous les watchers est appelée. Cela a un coût. Et c’est pourquoi les auteurs d’Angular encouragent à garder cette fonction la plus légère possible. Appels réseaux et algorithmes complexes y sont à proscrire.

Lors du Lab, nous avons ajouté 3 améliorations :

1. Un premier garde-fou permettant d’éviter un appel infini en levant une erreur après 10 itérations
1. Un second garde-fou permettant d’éviter des appels récursifs à la méthode $digest (étape 7).
1. La possibilité d’effectuer des comparaisons par valeur et non pas uniquement par référence. La comparaison de tableaux ou de grappes d’objets devient alors possible (étape 6).

## Etape 4 : Scope.$apply

La **fonction _$apply_** exécute une expression passée en argument puis lance quoi qu’il arrive un _$digest_ :

```js
Scope.prototype.$apply = function (exprFn) {
    try {
        exprFn();
    } finally {
        this.$digest();
    }
}
```

Cette méthode est appelée en interne par Angular lorsqu’il a besoin de binder une donnée, par exemple lors de l’utilisation de la directive _ng-bind_ dans les templates. Tous les composants Angular y font appels.

En dehors d’un contexte Angular, cette méthode doit explicitement être  appelée par le développeur. C’est typiquement le cas depuis une callback jQuery.
L’étape 5 ayant été traitée en même temps que l’étape 3 et les étapes 6 et 7 étant facultatives pour l’objectif fixé initialement, nous enchaînons directement à l’étape 8.

## Etape 8 : place aux directives

Dans le fragment HTML présenté au début du billet, 2 directives viennent enrichir le HTML sous forme d’attributs : _ng-model_ et _ng-bind_. Dans Angular, une directive n’est rien d’autre qu’une fonction ou un objet ayant des propriétés bien définies. Pour les besoins du Lab, nous resterons sur le cas simple : la fonction. L’ **objet $$directives** doit permettre d’enregistrer les fonctions associées à ces directives. Pour rappel, un objet JavaScript peut être utilisé de la même manière qu’un tableau associatif (une Map en Java) : à partir de la clé (chaine _‘ng-bind’_) on récupère la valeur (fonction _ng-bind_).
La fonction **$directive** permet quant à elle d’ajouter une directive et de lire une directive depuis l’objet _$$directives_.

```js
var $$directives = {};
var $directive = function (name, directiveFn) {
    if (directiveFn) {
        $$directives[name] = directiveFn;
    }
    return $$directives[name];
}
```

La fonction _$directive_ fait à la fois getter et setter pour les _$$directives_. L’implémentation utilise une technique répandue en JavaScript : lorsque seul le nom d’une directive est passé en paramètre, la fonction agit comme un getter. Lorsque le nom et le code d’une directive sont passés en paramètre, la fonction enregistre la fonction avant de la retourner.

A noter que les développeurs Angular ne manipulent jamais directement ces 2 objets. Ils sont utilisés par le moteur d’injection de dépendance d’Angular.

## Etape 9 : $compile le DOM

Cette étape consiste à écrire la **fonction $compile** chargée de parcourir récursivement les éléments du DOM. Les attributs de chaque élément sont également parcourus. Lorsqu’un attribut correspond au nom d’une directive, la fonction implémentant la directive est exécutée.
Le code est compréhensif :

```js
var $compile = function(element, scope) {
    _.each(element.children, function (child) {
       $compile(child, scope);
    });
    _.each(element.attributes, function(attribute) {
        var directiveFn = $directive(attribute.name);
        if (directiveFn) {
            directiveFn(scope, element, element.attributes);
        }
    });
}
```

Deux remarques à propos du code :

1. Contrairement à ce que l’on pouvait s’attendre, tous les attributs de l’élément sur lequel est apposée la directive sont passés en paramètre de la fonction _directiveFn_.
1. La récursion sur les éléments enfants est lancée avant le parcours des attributs de l’élément. Angular offre le choix avec les propriétés _prelink_ et _postlink_. De manière générale, _postlink_ est à privilégier.

Pour demander à notre framework maison de parcourir l’intégralité du DOM, une unique ligne de code est nécessaire :

```js
$compile(document.body, scope);
```

A présent que le framework sait découvrir des directives dans le DOM et appeler la fonction correspondante, il est temps d’implémenter une première directive.

## Etape 10 : ng-bind

La **directive ng-bind** se met à l’écoute sur la donnée pointée par la valeur de l’attribut _ng-bind_. Lors d’un changement de valeur, l’élément du DOM (dans notre exemple _<h1>_) est modifié avec la nouvelle valeur.

```js
$directive('ng-bind', function (scope, element, attributes) {
    scope.$watch(function(scope) {
        return eval('scope.' + attributes['ng-bind'].value);    // 'scope. labs.titre'
    }, function(newValue) {
        element.innerHTML = newValue;
    });
});
```

Bien que controversée, l’utilisation de la fonction _eval_ simplifie ici le code. Au cours du Lab, Matthieu nous a donné son équivalent fonctionnel. Basé sur les fonctions _split_ et _reduce_, le code devient illisible pour les développeurs ne pratiquant pas ce paradigme.

## Etape 11 : ng-model

 **ng-model** est une directive gérant le data-binding bidirectionnel. Appliquée à la balise _<input/>_, elle permet d’y afficher le contenu du modèle même lorsque celui-ci change et de mettre à jour le modèle lorsque l’utilisateur saisit des données dans le champ de saisie.
S’agissant d’une version ++ de la directive _ng-bind_, le début de leur implémentation correspondant au premier sens de binding se ressemble :

```js
$directive('ng-model', function(scope, element, attributes) {
    scope.$watch(function() {
        return eval('scope.' + attributes['ng-model'].value);
    }, function(newValue) {
        element.value = newValue;
    });
    element.addEventListener('keyup', function() {
        scope.$apply(function() {
            eval('scope.' + attributes['ng-model'].value + ' = \"' + element.value + '\"');
        });
    });
});
```

La directive _ng-model_ ajoute un listener d’évènements JavaScript. Lorsque l’évènement _'keyup'_ survient, le modèle est mis à jour à l’intérieur de la fonction _$apply_. Cette dernière déclenche la digest loop qui notifie la balise _ng-bind_. C’est par ce mécanisme que lorsque l’utilisateur saisi du texte dans l’input, le titre _<h1>_ est mis à jour en conséquence.
La fonction _eval_ est là encore utilisée. Angular n’y fait pas appel car il possède son propre parseur.

## Hello World

Une fois ces 2 directives enregistrées, un changement du titre du labs met simultanément à jour le titre _<h1>_ et le champs de saisie _<input>_ :

```js
scope.$apply(function () {
    scope.labs.titre = "Hello World";
})
```

 [![angular-hello-world](wp-content/uploads/2014/04/2014-04-comprendre-AngularJS-en-le-recodant-hello-world.png)](http://jsfiddle.net/Elryk/gkk4m/)

## Conclusion

 [92 lignes de JavaScript](http://jsfiddle.net/Elryk/gkk4m/) auront été nécessaires pour ré-implémenter une version minimaliste du cœur d’AngularJS. Vous pouvez tester : le code fonctionne sous IE 11, Firefox 28 et Chrome 34. Underscore aura permis de gagner en clarté ainsi que quelques lignes de code.
N’ayant que quelques dizaines d’heures d’Angular à mon actif, j’espère que ce que je vous aurais restitué sera exempt d’erreurs. Dans le cas contraire, je compte sur les speakers et vous pour me rectifier.
