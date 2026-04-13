---
_edit_last: "1"
author: admin
categories:
  - conférence
date: "2017-04-09T18:16:16+00:00"
toc: true
thumbnail: wp-content/uploads/2017/04/vuejs-emmanuel.png
featureImage: wp-content/uploads/2017/04/vuejs-emmanuel.png
guid: http://javaetmoi.com/?p=1677
parent_post_id: null
post_id: "1677"
post_views_count: "6444"
summary: |-
  Au cours des précédentes éditions de Devoxx France, je me suis familiarisé avec les frameworks JavaScript du moment : [AngularJS](http://javaetmoi.com/2013/04/angularjs-devoxx-france-2013/) en 2013 puis [Angular 2](http://javaetmoi.com/2016/04/angular-2-hands-on-lab-devoxx-france/) et [ReactJS](wp-content/uploads/2016/05/Devoxx_France-2016-Let_s_React.pdf) en 2016. Cette année, ce fut au tour d’un nouveau venu, à savoir **Vue.js**. Je l’ai testé au travers du [Hands-on Lab](http://cfp.devoxx.fr/2017/talk/USM-5688/Apres_Angular_et_React,_voici_..._VueJS) animé par Emmanuel Demey et Aurélien Loyer. Si vous n’avez pas eu la chance d’y participer, cet article a pour humble **objectif de vous aider à réaliser ce Lab par vous-même**, tel un **tutoriel**. Il complète le code disponible sur le [dépôt GitHub du Lab](https://github.com/Gillespie59/devoxx-vuejs/) ainsi que [les slides consultables en ligne](http://slides.com/emmanueldemey-1/deck-13). Vous pouvez également l’utiliser pour étudier à quoi ressemble une application Vue.js et découvrir ses principaux concepts.

  ![](wp-content/uploads/2017/04/vuejs-emmanuel.png)Emmanuel et Aurélien sont consultants web chez Zenika Lille. Familiarisés avec Angular, ils ont découvert VueJS au travers d’un projet personnel.
  VueJS nous est présenté comme une librairie (et non un framework) dédiée à la création d’interfaces web HTML. Il se veut **simple** et efficace, idéal pour créer rapidement une application web. Ses concepts principaux sont les **Vues**(il ne s’appelle pas Vue.js pour rien), les **Directives**, les **Composants** et le **Binding**. Tels les Web Components, Vue.js utilise le **Shadow DOM** pour scoper le style CSS des composants.
  Après cette courte introduction, place au CodeLab.

  ![Codez le lab Vue.js de Devoxx France 2017](wp-content/uploads/2017/04/vuejs-emmanuel.png)
tags:
  - devoxx
  - javascript
  - vue.js
title: Codez le lab Vue.js de Devoxx France 2017
url: /2017/04/codez-lab-vue-js-devoxx-france-2017/

---
Au cours des précédentes éditions de Devoxx France, je me suis familiarisé avec les frameworks JavaScript du moment : [AngularJS](/2013/04/angularjs-devoxx-france-2013/) en 2013 puis [Angular 2](/2016/04/angular-2-hands-on-lab-devoxx-france/) et [ReactJS](wp-content/uploads/2016/05/Devoxx_France-2016-Let_s_React.pdf) en 2016. Cette année, ce fut au tour d’un nouveau venu, à savoir **Vue.js**. Je l’ai testé au travers du [Hands-on Lab](http://cfp.devoxx.fr/2017/talk/USM-5688/Apres_Angular_et_React,_voici_..._VueJS) animé par Emmanuel Demey et Aurélien Loyer. Si vous n’avez pas eu la chance d’y participer, cet article a pour humble **objectif de vous aider à réaliser ce Lab par vous-même**, tel un **tutoriel**. Il complète le code disponible sur le [dépôt GitHub du Lab](https://github.com/Gillespie59/devoxx-vuejs/) ainsi que [les slides consultables en ligne](http://slides.com/emmanueldemey-1/deck-13). Vous pouvez également l’utiliser pour étudier à quoi ressemble une application Vue.js et découvrir ses principaux concepts.

![](wp-content/uploads/2017/04/vuejs-emmanuel.png)Emmanuel et Aurélien sont consultants web chez Zenika Lille. Familiarisés avec Angular, ils ont découvert VueJS au travers d’un projet personnel.
VueJS nous est présenté comme une librairie (et non un framework) dédiée à la création d’interfaces web HTML. Il se veut **simple** et efficace, idéal pour créer rapidement une application web. Ses concepts principaux sont les **Vues**(il ne s’appelle pas Vue.js pour rien), les **Directives**, les **Composants** et le **Binding**. Tels les Web Components, Vue.js utilise le **Shadow DOM** pour scoper le style CSS des composants.
Après cette courte introduction, place au CodeLab.

## L’application Zenika Ecommerce

Au cours de ce CodelLab, vous allez développer une petite application de e-commerce dédiée à la vente de bières (nos speakers ne sont pas Lillois pour rien).
![](wp-content/uploads/2017/04/screenshot-zenika-ecommerce.png)

La page est décomposée en 2 parties :

1. **un** **menu** supérieur permettant d’accéder au panier et donnant quelques informations sur le contenu de ce dernier,
1. **une liste de bières** en stock que vous pouvez acheter.

Le template HTML et les ressources statiques de cette page nous sont fournies dans la [branche step0](https://github.com/Gillespie59/devoxx-vuejs/tree/step0). L’objectif du Lab sera de les dynamiser en les intégrant dans des composants Vue.js.
Les données (à savoir les bières) seront tout d’abord hard-codées à la main dans le JS avant d’être récupérées d’un serveur Node.JS via une API REST.

Ce Lab est développé en ECMAScript 6 (alias JavaScript 2015). L’utilisation de la syntaxe raccourcie de déclaration de méthodes est encouragée.

## Pré-requis

Les **instructions** des différents exercices du Lab sont données dans le fichier [**index.md**](https://github.com/Gillespie59/devoxx-vuejs/blob/master/docs/index.md). Chaque exercice est reconnaissable au pattern PW _<Numéro>_ (pour Project Work ?).

Avant de commencer à implémenter un exercice, vous devrez tout d’abord vous référer à la partie théorique [**des slides**](http://slides.com/emmanueldemey-1/deck-13).
Avant d’aller plus loin, les pré-requis suivants sont nécessaires :

- Un client Git
- Un Node.JS 7 ou +
- Votre IDE favori
- L’ [extension Chrome Vue-devtools (facultatif)](https://github.com/vuejs/vue-devtools)

L’installation du cli Vue et le boostrap de l’application feront partis de l’exercice PW1.

## PW0 – Ressources mises à dispositions

Cette étape se résume à cloner le repo [https://github.com/Gillespie59/devoxx-vuejs](https://github.com/Gillespie59/devoxx-vuejs) et à checkouter la branche step0.

Voici les fichiers / répertoires qui vous intéresseront :

- **docs/index.md**: instructions permettant de réaliser le Lab
- **server/**: serveur Express / Node.JS utilisé à partir de l’exercice 4 pour exposer la liste de bières sous forme d’API REST. A noter que le fichier server/beers.json sera utilisé dès l’étape 2 pour hard-codé sous forme d’objet JavaScript le tableau de bières à afficher.
- **static/**: ressources statiques (CSS, fonts et images)
- **html**: template statique HTML de la page d’accueil utilisé dès l’étape 2.
- html : non utilisé lors du lab par faute de temps, ce template permet d’initier la page affichant le panier utilisateur (PW7)

## PW1 – Application blanche Vue.JS

Avant de créer votre première application, un peu de théorie est nécessaire pour vous familiariser avec les **principaux concepts de Vue.js**. Pour se faire, parcourez les 5 slides suivants :

- **Interpolation** [2-3](http://slides.com/emmanueldemey-1/deck-13#/2/3)
- **Bindings** [2-4](http://slides.com/emmanueldemey-1/deck-13#/2/4) et [2-5](http://slides.com/emmanueldemey-1/deck-13#/2/5)
- **Events Handlers** [2-6](http://slides.com/emmanueldemey-1/deck-13#/2/6) et [2-7](http://slides.com/emmanueldemey-1/deck-13#/2/7)

Lors de la conception du binding de Vue.js, son concepteur n’a pas souhaité utiliser le **préfixe data**\- afin d’être conforme au W3C. Son point de vue est que le code généré par Vue.js est lui conforme W3C.

Pour créer une application Vue.JS, à l’instar de ember-cli et angular-cli, on peut utiliser l’interface en ligne de commande (command-line interface) **vue-cli**. L’utilitaire vue-cli propose **différents types de squelette** : du plus basique à celui basé sur webpack. Dans le Lab, nous utiliserons le **squelette webpack**.

A la fin du PW1, la d’accueil du template Vue.js doit s’ouvrir dans votre navigateur :
![](wp-content/uploads/2017/04/screenshot-template-vue.png)

Le **code source** de l’application que vous allez compléter au cours du Lab se trouve dans le répertoire **src/**.
Le fichier **main.js** est le point d’entrée de l’application. On y retrouve la déclaration de la **vue racine** de l’application :

```js
new Vue({
   el: '#app',
   template: '<App/>',
   components: { App }
 })
```

L’objet **Vue** est l’ **objet principal** de la librairie **.** Son constructeur prend en paramètre un objet JS dont les propriétés sont normalisées. Ici, notre vue racine en définie 3 :

- **el**: associe la vue avec un élément du DOM ayant l’identifiant app
- **template**: l’élément du DOM sera remplacé par le code HTML du template, ici une balise personnalisée <App/>
- **components**: composants Vue.js nécessaires au rendu de la vue. Ici, le composant App est référencé. C’est lui qui va être chargé d’interpréter la balise <App/>

Dans le fichier **index.html**, nous retrouvons le <div> portant l’identifiant "app" et qui sera donc associé à la vue racine :

```xhtml
<body>
  <div id="app"></div>
</body>
```

Particulièrement simple, cette vue racine ne comporte ni données ni gestionnaire d’évènements.

Le code source du composant App est localisé dans le fichier src/App.vue. **L’approche composant de Vue.js s’inspire très fortement du standard Web Components** dont Polymer est une implémentation. L’objectif d’un composant est d’ **encapsuler du code**(HTML + JS + CSS) afin de pouvoir le **réutiliser**. Un composant est associé à une balise HMTL. Ici, à la balise <App/>. Vous l’aurez remarqué, c’est le nom du fichier .vue qui détermine le nom de la balise HTML associée.
Un composant peut être déclaré par programmation via la méthode Vue.component() ou bien décrit dans un fichier dédié portant l’ **extension .vue**. Le fichier App.vue est scindé en 3 parties :

1. **<template>**: code HTML templatisé à l’aide de la syntaxe Mustache.
1. **<scripts>**: code JavaScript du composant : nom, données, comportement, méthode callback appelée lors des différentes étapes du cycle de vie du composant …
1. **<style>**: style CSS global ou spécifique au composant. Pour un style spécifique, il faut ajouter l’attribut **scoped**. Le navigateur utilise alors le Shadow DOM.

Des **loaders Webpack** sont chargés de transformer le contenu des fichiers .vue en JavaScript.
Dans la suite du Lab, vous aurez à personnaliser le fichier App.vue.

## PW2 – Dynamiser la page à l’aide d’un composant

Cet exercice est sans nul doute le plus difficile du Lab. Vous allez en effet devoir manipuler pour la 1ière fois les principales notions de Vue.js : les composants, le binding et le templating.
Avant de commencer l’énoncé, veuillez prendre connaissance des slides théoriques sur les composants :

- **Global Components** [3-1](http://slides.com/emmanueldemey-1/deck-13#/3/1) à [3-6](http://slides.com/emmanueldemey-1/deck-13#/3/6)
- **Local component** [3-7](http://slides.com/emmanueldemey-1/deck-13#/3/7)
- **Fichiers .vue** [3-7](http://slides.com/emmanueldemey-1/deck-13#/3/7) et [3-8](http://slides.com/emmanueldemey-1/deck-13#/3/8)

Le **mécanisme de communication entre composants** est similaire à celui d’Angular 2 : le composant parent passe des propriétés à ses composant enfants. Les enfants émettent des évènements à leur parent.

**Solution**
Commencer par créer 2 fichiers Menu.vue et Beer.vue dans le sous-répertoire components.
Les 2 composants Beer et Menu sont référencés dans la vue racine App.vue :

```js
<script>
import Menu from './components/Menu'
import Beer from './components/Beer'

export default {
  name: 'app',
  components: {
    "v-menu": Menu,
    "v-beer": Beer
  },
```

La balise <menu> étant déjà réservée par HTML 5, nous suffixons les balises avec v-. Ainsi, la balise HTML associée au composant Menu est <v-menu>.

Le composant Menu encapsule le tag <nav> du fichier home.html récupéré lors du PW0 :

```xhtml
<template>
  <nav class="navbar navbar-inverse navbar-fixed-top" role="navigation">
    <div class="container">
      <div class="navbar-header">
        <a class="navbar-brand" href="/">Zenika Ecommerce</a>
      </div>
      <div class="navbar-collapse" id="bs-example-navbar-collapse-1">
        <ul class="nav navbar-nav">
          <li>
            <a href="#/basket.html">Accéder à votre panier {{bieres.length}} articles</a>
          </li>
        </ul>
      </div>
    </div>
  </nav>
</template>

<script>
export default {
  name: 'menu',
  props: ['bieres']
}
</script>

<style lang="css">
</style>
```

Pour afficher dynamiquement le nombre de bières ajoutées au panier, on déclare une propriété _bieres_. Un tableau de bières peut ensuite être passé en paramètre d’entrée du tag <v-menu>  dans le fichier App.vue :

```xhtml
<template>
  <div id="app">
    <v-menu :bieres="panier"></v-menu>
```

Ici on utilise la syntaxe raccourcie :bieres équivalente à v-bind:bieres. Le _panier_ passé en paramètre référence l’attribut panier du modèle (attribut data) du composant App. Au démarrage de l’application, le panier du client est vide :

```js
export default {
  name: 'app'
  ...
  data () {
   return {
     panier: []
     }
  }
}
```

Le composant Beer est responsable d’afficher le détail d’un article/item (dans notre cas une bière) et permet à l’utilisateur de l’ajouter à son panier. Sa déclaration se rapproche de celle du composant Menu.
Son template est créé à partir du div « thumbnail » récupéré du fichier home.html.
Le composant Beer accepte la propriété _item_ (qui n’est autre que la bière à afficher). Un item possède 5 propriétés : label, price, image, description et note. Ces propriétés sont affichés dans le template par la syntaxe {{item. _<propriété>_}}

```xhtml
<template lang="html">
  <div class="thumbnail">
    <img :src="item.image" alt="">
    <div class="caption">
      <h4 class="pull-right">{{item.price}} €</h4>
      <h4><a href="#">{{item.label}}</a>
      </h4>
      <p>{{item.description}}</p>
    </div>
    <div class="ratings">
      <button @click="ajouter" type="button" class="pull-right btn btn-primary" aria-label="Ajoutez au Panier">Ajouter</button>
      <p>
        <span class="glyphicon glyphicon-star"></span>
        <span class="glyphicon glyphicon-star"></span>
        <span class="glyphicon glyphicon-star"></span>
        <span class="glyphicon glyphicon-star"></span>
        <span class="glyphicon glyphicon-star-empty"></span>
      </p>
    </div>
  </div>
</template>

<script>
export default {
  name: 'produit',
  props: ['item'],
  methods: {
    ajouter () {
      this.$emit('ajout', this.item)
    }
  }
}
</script>

<style lang="css">
</style>
```

La balise <img>  référence l’URL de l’image représentant la bière passée en item :

```xhtml
<img :src="item.image" alt="">
```

La propriété HTML _src_ n’est pas directement utilisée. Vue.JS l’interdit. La **syntaxe :src** permet de ne valoriser l’attribut HTML _src_ que lorsque la donnée sera disponible. En effet, la donnée peut provenir d’une API REST et pendant quelques ms ou secondes la donnée peut être undefined. On retrouve la même problématique en Angular.

Outre l’affichage dynamique des propriété d’un item, le composant Beer permet d’ajouter la bière au panier. Lorsque l’utilisateur clique sur le bouton « Ajouter », on fait appel à la méthode ajouter() du composant :

```xhtml
<button @click="ajouter" type="button" >Ajouter</button>
```

Est utilisé ici une syntaxe raccourcie de v-on:click="ajouter" .
La méthode ajouter émet un événement au composant parent App :

```js
ajouter () {
  this.$emit('ajout', this.item)
}
```

 _‘ajout’_ correspond au nom de l’événement et _this.item_ à la donnée associée à l’événement, ici la bière à ajouter au panier. Dans le composant parent App, il est désormais possible de s’abonner à l’événement ‘ajout’. Nous y reviendrons.
A noter que le mot clé _this_ correspondant à l’instance de la Vue.

Dans le composant App, le tag <v-beer>  peut désormais être utilisé pour afficher chacune des bières. Dans un 1er temps, le tableau de bières est hard-codé sous forme d’un tableau d’objets JavaScript déclaré en tant que propriété _produits_ du composant App :

```js
data () {
  return {
    panier: [],
    produits: [
      {
        'label': 'Queue de Charrue',
        'price': '3.70',
        'image': '/static/images/queuedecharrue.jpg',
        'description': 'La Queue de Charrue est une famille de bières brassées pour la Brasserie Vanuxeem. La plus connue et typique est la Queue de Charrue brune. Son nom ...',
        'note': 4
      },
      ...
    ]
  }
```

Le tableau de _produits_ est construit par copier/coller du fichier beers.json.

Dans le template du composant App, n’ayant pas encore appris comment itérer sur un tableau, le tag <v-beer>  est répété 4 fois :
<div class="col-sm-4 col-lg-4 col-md-4">

```xhtml
<div class="col-sm-4 col-lg-4 col-md-4">
    <v-beer v-on:ajout="ajoutPanier" :item="produits[0]"></v-beer>
</div>
<div class="col-sm-4 col-lg-4 col-md-4">
    <v-beer v-on:ajout="ajoutPanier" :item="produits[1]"></v-beer>
</div>
…
```

Chaque bière est référencée par son index dans le tableau _produits_. Elles sont passées en paramètres du composant Beer par la propriété _item_.

La directive _v-on_ positionne le handler _ajoutPanier_ sur l’écoute de l’événement _ajout_ émis par le composant Beer.
L’implémentation de la méthode _ajouterPanier_ ne pose aucune difficulté :

```js
methods: {
 ajoutPanier: function (biere) {
   this.panier.push(biere)
 }
},
```

Lorsqu’une bière est ajoutée au panier, le modèle _panier_ de la vue est modifié. A l’écran, le nombre d’articles du panier est automatiquement rafraichi.

Bravo, vous venez de terminer l’étape PW2.

## PW3 – Utilisation des directives

Beaucoup plus simple et court que le précédent, ce 3ième exercice consiste à mettre en œuvre 3 directives proposées par Vue.js.
Commencez par prendre connaissance des slides [4-1](http://slides.com/emmanueldemey-1/deck-13#/4/1) à [4-3](http://slides.com/emmanueldemey-1/deck-13#/4/3) puis suivez l’ [énoncé](https://github.com/Gillespie59/devoxx-vuejs/blob/master/docs/index.md#pw3---les-directives).

**Solution**

La **directive v-for** permet d’itérer sur la liste des bières afin d'afficher autant de composants Beer.vue qu'il y a d'éléments dans le tableau :

```xhtml
<div v-for="beer in produits" class="col-sm-4 col-lg-4 col-md-4">
  <v-beer v-on:ajout="ajoutPanier" :item="beer"></v-beer>
</div>
```

Contrairement à Angular 2, Vue.js offre la possibilité d’utiliser directement les directives sur le tag <v-beer>  (et non pas seulement sur le <div> englobant) :

```xhtml
<v-beer v-for="beer in produits" v-on:ajout="ajoutPanier" :item="beer>
```

Dans le tableau de Beer, l’ajout d’une propriété _stock_ initialisée à 5 pour tous les éléments se fait sans difficulté :

```js
{
  'label': 'Queue de Charrue',
  'price': '3.70',
  'image': '/static/images/queuedecharrue.jpg',
  'description': '...'
  'note': 4,
  'stock': 5
},
```

Lorsqu’une bière est ajoutée au panier, on décrémente son stock :

```js
ajouter () {
  this.item.stock--;
  this.$emit('ajout', this.item)
}
```

En utilisant la **directive v-if**, nous pouvons désormais n’afficher à l’utilisateur que les bières en stock :

```xhtml
<v-beer v-for="beer in produits" v-if="beer.stock > 0" v-on:ajout="ajoutPanier" v-bind:item="beer"></v-beer>
```

Pour changer la couleur de fond d'un produit lorsque son stock atteint 1, on commence par déclarer la classe CSS _last_ dans la section <style> de App.vue :

```css
<style lang="css">
.last {
    background-color: rgba(255, 0, 0, 0.4)
}
</style>
```

Sur le div possédant la classe thumbnail, en utilisant la directive v-bind:class , nous pouvons ensuite ajouter la classe _last_ lorsque le stock de bière est de 1 :

```xhtml
<div class="thumbnail" :class="{ last: item.stock == 1 }">
```

Une seconde solution consiste à utiliser les **computed values**. Une computed value s’utilise comme une propriété mais se définit comme une méthode. Son résultat est mis en cache par Vue.js. Nous déclarons la computed value _thumbnailClass_ dans App.vue :

```js
export default {
  name: 'produit',
  props: ['item'],
  computed: {
    thumbnailClass() {
      return this.item.stock === 1 ? 'thumbnail last' : 'thumbnail';
    }
  },
...

```

Son utilisation dans le template HTML se fait par binding :

```xhtml
<div :class="thumbnailClass">
```

Les computed values peuvent également être utilisées pour afficher le coût total du panier dans Menu.vue. Le total est calculé à partir du prix de chaque bière :

```js
<script>
export default {
  name: 'menu',
  props: ['bieres'],
  computed: {
    total: function () {
      let total = 0
      this.bieres.map((biere) => {
        total += parseFloat(biere.price)
      })
      return Math.round(total * 100) / 100
    }
  }
}
</script>
```

La computed value _total_ est ensuite utilisée dans le template comme s’il s’agissait d’une propriété :

```xhtml
<a href="#/basket.html">Accéder à votre panier ({{bieres.length}} articles - {{total}} €)</a>
```

Pour afficher une mention différente lorsque le panier est vide, on utilise de nouveau la **directive** **v-if** :

```xhtml
<a v-if="bieres.length > 0" href="#/basket.html">Accéder à votre panier ({{bieres.length}} articles - {{total}} €)</a>
<a v-if="bieres.length === 0" href="#/basket.html">Accéder à votre panier (vide)</a>
```

## PW4 – Les filtres

Les slides [5-2](http://slides.com/emmanueldemey-1/deck-13#/5/2) et [5-3](http://slides.com/emmanueldemey-1/deck-13#/5/3) expliquent comment créer un filtre global à toute l’application et un filtre local au composant.
Lors du Lab, nous n’avons pas eu le temps de coder cet exercice. Je vous décrirai donc uniquement comment créer et utiliser le premier **filtre uppercase** demandé.

Commencez par créer le fichier src/filters/uppercase.js :

```js
import Vue from 'vue'

Vue.filter('uppercase', function (value) {
  if (!value) return ''
  value = value.toString()
  return value.toUpperCase()
})
```

Importez ce fichier dans main.js :

```js
import './filters/uppercase'
```

Puis, avec la même syntaxe qu’Angular, utilisez le filtre dans Beer.vue :

```xhtml
<h4><a href="#">{{ item.label | uppercase }}</a>
```

## PW5 – Les Ressources

 [Cet exercice](https://github.com/Gillespie59/devoxx-vuejs/blob/master/docs/index.md#pw5---les-ressources) propose d’ **utiliser une API REST** pour récupérer la liste des bières à afficher. Le **module vue-resource** présenté dans les slides [6-1](http://slides.com/emmanueldemey-1/deck-13#/6/1) à [6-9](http://slides.com/emmanueldemey-1/deck-13#/6/9) va vous y aider.
Comme vous le verrai, l’API de **$http** ressemble beaucoup à celle de AngularJS. Les méthodes get, head, delete, post retournent une promesse. Elles acceptent 2 callback : l’une en cas de succès et l’autre en cas d’erreur.

Les intercepteurs permettent de transformer une requête http, par exemple pour ajouter des headers HTTP.

Pour résoudre cet exercice, il vous sera utile de savoir qu’un composant possède un **cycle de vie** et qu’on peut brancher du code à chaque étape. Comme son nom d’L’étape `created()` permet d’exécuter du code initialisant les données du composant.

**Solution**

Commencez par démarrer le serveur REST avec Node.JS puis testez son API depuis le navigateur.
Extrait de la réponse observée lors d’un GET sur [http://localhost:1337/api/v1/beers](http://localhost:1337/api/v1/beers)  :

```js
[
  {
    "label": "Queue de Charrue",
    "description": "La Queue de Charrue est une famille de bières brassées pour la Brasserie Vanuxeem. La plus connue et typique est la Queue de Charrue brune. Son nom ...",
    "image": "/static/images/queuedecharrue.jpg",
    "price": 3.7,
    "stock": 2
  },
…
```

Installez le module vue-resource via la commande npm :

```sh
npm install vue-resource --save
```

Dans le fichier main.js, importez le module vue-resource :

```js
import VueResource from 'vue-resource';

Vue.use(VueResource);
```

Dans App.vue, implémentez la méthode `getProduits()` faisant appel à l’API REST. Cette méthode est appelée pendant le cycle de vie du composant, une fois celui-ci créé :

```js
created() {
   this.getProduits();
},
methods: {
   getProduits() {
   this.$http.get('http://localhost:1337/api/v1/beers')
           .then(response => { this.produits = response.body; });
 },
```

On initialise à vide le tableau de bières précédemment hard-codé :

```js
produits: []
```

## Conclusion

Les plus motivés pourront poursuivre les exercices PW6, PW7 et PW8 du Lab. Vous y apprendrez comment configurer un **routeur**, **valider des formulaires** et **gérer de manière centralisée l’état d’une application**. Les différentes branches Git permettent d’avoir accès aux corrections.

Vue.js se veut simple. Ce Lab nous l’aura confirmé. Reprenant de nombreux concepts de ses pairs, il ne dépaysera pas les développeurs front.
Vue.js se veut également léger. C’est le cas si l’on se restreint à son noyau. Néanmoins, dès que l’on développe une application web un peu conséquente, on doit y ajouter des modules tiers : vue-resource, vee-validate, vuex … L’avantage de Vue.js est d’être flexible et de nous laisser choisir ces différentes briques. Il se veut beaucoup moins structurant qu’un Angular.

Pour terminer, un grand merci à Aurélien et Emmanuel pour cette découverte. Et à l’an prochain pour ne nouveau framework JS du moment !!

Resources :

- [Dépôt GitHub du Hands-On Lab](https://github.com/Gillespie59/devoxx-vuejs/)
- [Slides accompagnants le Hands-on Lab](http://slides.com/emmanueldemey-1/deck-13)
- [Site web officiel de Vue.js](https://vuejs.org/)
- [Tutoriel très complet et en français sur Vue.js](http://laravel.sillo.org/vue-js/)
