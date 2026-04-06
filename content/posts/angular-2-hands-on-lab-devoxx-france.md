---
_edit_last: "1"
author: admin
categories:
  - conférence
date: "2016-04-30T15:04:09+00:00"
guid: http://javaetmoi.com/?p=1560
parent_post_id: null
post_id: "1560"
post_views_count: "8952"
summary: |-
  Lors de l’édition 2013 de Devoxx France, [je découvrais la simplicité de coder une application full JavaScript avec Angular JS](http://javaetmoi.com/2013/04/angularjs-devoxx-france-2013/). Lors de l’édition 2014, [je recodais from scratch sa fonctionnalité phare de binding directionnel](http://javaetmoi.com/2014/04/lab-angularjs-from-scratch-devoxx-france-2014/). Deux ans ont passé. Depuis son annonce, la version 2 d’Angular déchaine les passions au sein de la communauté front. Animé par Wassim Chegham , Emmanuel Demey et Cyril Balit, le [**Hand’s On Lab sur Angular 2**](http://cfp.devoxx.fr/2016/talk/ROC-7855/Angular_2_hands_on) fut pour moi l’occasion de découvrir les nouveautés, mais surtout, de découvrir si ce nouveau cru est aussi séduisant que le premier.

  Ce billet s’adresse à celles et ceux qui n’ont pas pu assister à ce Lab et qui **ont envie de découvrir** [**Angular 2**](https://angular.io/). Il s’appuie sur les ressources mises à disposition par les speakers.
  En7 étapes, vous développerez une application de Quizz avec la beta 11 d’Angular 2.

  ![2016-04-20_Hands-on-lab-Angular2_Devoxx_France_2016](http://javaetmoi.com/wp-content/uploads/2016/04/2016-04-20_Hands-on-lab-Angular2_Devoxx_France_2016-1024x576.jpg)

  ##
tags:
  - angular2
  - devoxx
  - typescript
title: Lab Angular 2 à Devoxx France 2016
url: /2016/04/angular-2-hands-on-lab-devoxx-france/

---
Lors de l’édition 2013 de Devoxx France, [je découvrais la simplicité de coder une application full JavaScript avec Angular JS](/2013/04/angularjs-devoxx-france-2013/). Lors de l’édition 2014, [je recodais from scratch sa fonctionnalité phare de binding directionnel](/2014/04/lab-angularjs-from-scratch-devoxx-france-2014/). Deux ans ont passé. Depuis son annonce, la version 2 d’Angular déchaine les passions au sein de la communauté front. Animé par Wassim Chegham , Emmanuel Demey et Cyril Balit, le [**Hand’s On Lab sur Angular 2**](http://cfp.devoxx.fr/2016/talk/ROC-7855/Angular_2_hands_on) fut pour moi l’occasion de découvrir les nouveautés, mais surtout, de découvrir si ce nouveau cru est aussi séduisant que le premier.

Ce billet s’adresse à celles et ceux qui n’ont pas pu assister à ce Lab et qui **ont envie de découvrir** [**Angular 2**](https://angular.io/). Il s’appuie sur les ressources mises à disposition par les speakers.
En7 étapes, vous développerez une application de Quizz avec la beta 11 d’Angular 2.

![2016-04-20_Hands-on-lab-Angular2_Devoxx_France_2016](/wp-content/uploads/2016/04/2016-04-20_Hands-on-lab-Angular2_Devoxx_France_2016.jpg)

##  Installation du post de dév

Le repository GitHub [**angular2-codelab**](https://github.com/manekinekko/angular2-codelab) met à disposition l’application finale sur le master ainsi que 2 branches par étape (step) :

1. Une branche de départ (ex : step1)
1. Une branche mettant à disposition la correction de l’étape (ex : step1-solution)

Point d’attention : le contenu de la branche step2 ne correspond pas à celui de la branche step1-solution. Lors du passage à l’étape suivante, un checkout de la branche correspondante sera donc nécessaire.

Le fichier [README.md](https://github.com/manekinekko/angular2-codelab/blob/master/README.md) donne les instructions pour :

1. Forker puis récupérer le repo
1. Construire l’application (modules JavaScript téléchargés via npm)
1. Démarrer l’application via la commande _ng serve_

La commande **_ng_** fait appel au client en ligne de commande fournit par Angular 2. Ce dernier remplace des outils de build comme gulp et permet également de générer les composants. A termes, il est prévu qu’il soit capable de packager l’application et de la déployer sur le serveur.

Pour IDE, un simple éditeur de texte peut suffire. Proposant complétion et compilation, l’utilisation de Visual Studio, Atom ou d’IntelliJ IDEA est toutefois préférable.
Le serveur web démarré par _ng_ supporte le live reload : à chaque changement de code, la page est rafraichie.

Bien que [les slides](http://slides.com/wassimchegham/getting-started-with-angular-2#/) montrent à quoi ressemble l’application finale, je vous conseille de faire un checkout du master et de naviguer sur [http://localhost:4200/](http://localhost:4200/). Vous aurez ainsi une idée plus précise de l’objectif à atteindre lors de la partie pratique.

## Un mot sur TypeScript

Avant de commencer à jouer avec Angular 2, il est nécessaire de s’arrêter sur un détail d’importance. Bien qu’étant un framework front, le langage first d’Angular 2 n’est pas JavaScript/ECMAScript mais [**TypeScript**](https://www.typescriptlang.org/). Inventé par Microsoft, TypeScript est un sur-ensemble de ES5, ES2015 (ES6), ES2016 (ES7) et ceux à venir. Dans le navigateur ou via un outil de build, TypeScript est transpilé en JavaScript.
Angular 2 n’impose pas l’utilisation de TypeScript. On peut utiliser ES5, ES6 et même Dart. Mais l’utilisation de TypeScript simplifie l’utilisation d’Angular2. A minima, Wassim conseille d’utiliser ES6. Pour faire tourner du ES6 sur les navigateurs ne le supportant pas, il est nécessaire de passer par un transpileur comme **Babel**.
Utiliser TypeScript pour vos développements Angular 2 n’impose pas de rester sur ce dernier. Repasser à du full JavaScript restera possible.

Ce lab est codé en TypeScript. Une connaissance minimale de ce dernier ou, à défaut, d’ES6 est recommandé. J’ai toutefois pu m’en sortir sans : baladez-vous dans le code source du step1 pour apprendre la syntaxe des imports, la définition d’une classe, l’usage des annotations …

Si vous vous posez la question, les fichiers suffixés par **_.d.ts_** et présents dans le workspace du Lab permettent d’utiliser des librairies tierces JavaScript depuis TypeScript (ex : Jasmine et Selenium).

## Les apports d’Angular 2

Angular 2 est [présenté comme une plateforme de développement](http://slides.com/wassimchegham/getting-started-with-angular-2#/7/4) (et non un framework). Il couvre bien plus de [fonctionnalités](http://slides.com/wassimchegham/getting-started-with-angular-2#/8/5) qu’Angular 1 (NG1).

Chose intéressante : on peut faire tourner une application Angular 2 côté serveur avec Node.
Comme React, Angular 2 peut fonctionner sans DOM (avec le shadow DOM), ce qui ouvre son utilisation aux applications natives.

**Step 1 – Les composants**

Cette première étape va vous permettre de créer **votre premier composant** et d’initier l’application web.

Une application Angular 2 est un [arbre de composants](http://slides.com/wassimchegham/getting-started-with-angular-2#/9/11) (au sens Web Components), là où Angular 1 était un arbre cyclique (dirty checking).
Il s’agit du concept principal d’Angular 2. Un composant Angular 2 combine directive, contrôleur et scope d’Angular 1.

L’application Quizz est constituée des 7 composants suivants :

1. **![](/wp-content/uploads/2016/04/lab-docker1.png)Ng2CodelabApp**: une application Angular 2 est elle même un composant. C’est le composant parent de tous les autres composants.
1. **Toolbar**: barre de navigation située en haut de l’écran
1. **Home**: page d’accueil affichant une liste de thèmes (TypeScript, ECMAScript 6, Angular 2 et React). Le détail de chaque thème est géré par le composant ThemeCard.
1. **ThemeCard**: affiche le nom du thème, une image, son descriptif et propose un bouton permettant de commencer le quizz associé.
1. **Technology**: page affichant une question (composant QuestionCard) et permettant de naviguer vers les questions précédentes / suivantes.
1. **QuestionCard**: affiche la question et reçoit les réponses de l’utilisateur
1. **Summary**: page listant les résultats des questions d’un quizz

Ces composants sont tous localisés dans le répertoire _src/app/components_ de votre projet. Chaque composant dispose d’un répertoire dédié.
Techniquement, un composant est une classe JavaScript décorée avec l’annotation **@Component** et explicitement exportée (mot clé **export** d’ES6).

Un composant peut disposer d’une **vue**. Cette dernière est déclarée en tant que propriété **_template_** ou **_templateUrl_** du @Component. L’attribut **_templateUrl_** référence un template HTML externe (comme sous Angular 1) et **_template_** permet d’utiliser les backquotes TS pour déclarer un template inline.

Au travers de la propriété **_selector_** de @Component, un composant peut également être associé à une balise HTML, et même plus largement à un **selector CSS 3**.

Pour démarrer une application Bootstrap, il faut appeler la fonction **_bootstrap_** en lui passant la classe du composant parent, en l’occurrence _Ng2CodelabApp_.

Les informations précédentes devraient vous aider à **implémenter le step-1** en suivant les instructions données dans le fichier [STEPS.md](https://github.com/manekinekko/angular2-codelab/blob/master/STEPS.md). A vous de jouer.
Avant de commencer le step-2, voici quelques explications sur la solution.

Dans le fichier _ng2-codelab.js_, la déclaration du **selector**: **'app'**, permet à Angular 2 de reconnaître la balise < **_app>_** que vous avez ajoutée dans le fichier [index.html](https://github.com/manekinekko/angular2-codelab/blob/master/src/index.html):

```xhtml
<app>
  <div class="mdl-grid">
    <div class="mdl-cell mdl-cell--12-col">
      <div class="mdl-spinner mdl-js-spinner is-active"></div>
    </div>
  </div>
</app>
```

Toujours dans le _index.html_, on indique à Angular 2 quel fichier JS utiliser pour bootstraper l’application via l’appel à _System.import("app.js")._ Le fichier app.js est la version transpilée de app.ts.

```js
<script>
System.config({
  packages: {
    app: {
      format: 'register',
      defaultExtension: 'js'
    }
  }
});

System.import('app.js').then(null, console.error.bind(console));
</script>
```

Dans le jargon d’Angular 2, le composant Ng2CodelabApp initié dans cette étape s’appelle un **« dumb » component**.

Enfin, dans [app.js](https://github.com/manekinekko/angular2-codelab/blob/step-1-solution/src/app.ts), la classe _Ng2CodelabApp_ exportée précédemment est importée :
import { Ng2CodelabApp } from './app/ng2-codelab';

A la fin de cette étape, la page d’accueil n’affiche qu’un simple sablier.
![lab2-angular2-devoxxfr2016](/wp-content/uploads/2016/04/lab2-angular2-devoxxfr2016.png)

## Step 2 – Templates et cycle de vie

Dans le step 1, les fichiers HTML manipulés ne comportaient aucune syntaxe particulière à Angular. Le step 2 vise à utiliser quelques notations syntaxiques propres à Angular 2 et qui vont sont présentées dans [le slide Template Syntaxe](http://slides.com/wassimchegham/getting-started-with-angular-2#/8/16) et dont voici quelques explications.
Syntaxe raccourcie d’Angular 2 :

- Double accolade **{{**: affiche une propriété du composant (même syntaxe qu’Angular 1)
- Crochet **\[\]**: **binding unidirectionnel** d’une propriété du DOM (ex : classList), d’une propriété d’une classe, d’une classe CSS, d’un style CSS, d’un attribut du DOM
- Parenthèse **()**: binding sur un événement du navigateur (ex : _(click)_) ou d’un événement custom, et même de futurs évènements HTML (en Angular 1 la liste des évènements était hard-codée)
- Crochet + parenthèse **\[()\]**: binding bidirectionnel. Contrairement à Angular 1, le binding bidirectionnel n’est plus la norme dans Angular 2.
- Etoile **\***: directives qui viennent modifier le DOM.

Au premier abord, cette nouvelle syntaxe peut dérouter. Les speakers ne s’en cachent pas. Mais à l’usage, ils nous ont assuré qu’elle permettait de gagner en lisibilité.

**Les composants ont un cycle de vie**. Angular 2 permet aux développeurs d’interagir à l’aide de fonction callback : _[ngOnInit, ngDoCheck, ngOnChanges …](http://slides.com/wassimchegham/getting-started-with-angular-2#/8/18)_  Ces fonctions sont à déclarer dans les composants. Angular 2 les appellera au moment approprié. Détail de 3 fonctions sur les 8 disponibles :

- **ngOnInit**: déclenchée lorsque la directive a été compilée, que les meta-données sont chargées et que la directive démarre
- **ngOnChanges(records)**: écoute les changements d’état réalisés par un composant parent
- **ngAfterViewInit**: appelée lorsque la vue a été chargée

**Chaque composant gère son état**. C’est l’une des raisons qui fait qu’Angular 2 est plus performant que son prédécesseur.

En pratique, le **Parent** passe une information à son **Enfant** (propriété **_@Input_**). C’est l’Enfant qui met à jour son état. L’Enfant peut communiquer avec son Parent via l’event binding (propriété **_@Output_**). [Le slide State Managment](http://slides.com/wassimchegham/getting-started-with-angular-2#/8/21) schématise ce comportement. Des ressemblances existent avec l’ [architecture Flux](https://facebook.github.io/react/blog/2014/05/06/flux.html).

Dans le [slide d’exemple](http://slides.com/wassimchegham/getting-started-with-angular-2#/8/22), le composant _ThemeCard_ implémente l’interface _AfterViewInit_. Facultative, l’utilisation de cette interface TypeScript permet à l’IDE de mettre en garde le développeur si il omet d’implémenter la fonction _ngAfterViewInit()_.

La convention de nommage suivante est à respecter pour le double data-binding :

```js
@Input() <propertyName>
@Output() <propertyName>Change
```

La partie théorie s’arrête ici. En pratique, le step 2 vous demande de créer le nouveau composant **ThemeCard** puis de l’utiliser dans le composant Home.
En entrée, ThemeCard acceptera un paramètre de type **_ITechnology_**. Le template de ThemeCard affichera le _titre_, la _description_ et le _logo_ de cette technologie.
Le composant Home sera responsable de charger la liste des technologies à afficher. Elle s’appuiera sur le **_TechnologiesStore_** mis à votre disposition. Les notions de module et d’injection de dépendances seront abordés par la suite. Pour le moment, contentez vous d’ajouter la propriété _themeCards_ et le constructeur suivant à la classe Home :

```js
private themeCards: any[];

constructor(technologiesStore: TechnologiesStore){
    technologiesStore.fetch().then((themes) => this.themeCards = themes);
}
```

Remarque : pour utiliser le _TechnologiesStore_, il faut le déclarer en tant que **_providers_** au niveau de l’annotation _@Component_.
Munis de ces informations, **vous pouvez commencer le [step 2](https://github.com/manekinekko/angular2-codelab/blob/master/STEPS.md#step-2-home-and-theme-card-components)**.
Avant de passer au step 3, arrêtons-nous un moment sur la solution.

Le template de Home est intéressant :

```xhtml
<theme-card
    *ngFor="#card of themeCards"
    [theme]="card"
    class="mdl-cell mdl-cell--6-col"
></theme-card>
```

Il boucle sur la collection de _themeCards_ chargée par le constructeur du composant Home. La syntaxe dièse **_#card_** permet de référencer le _this_ du composant.

Le template _theme-card.html_ référence quant à lui les propriétés du composant :

```xhtml
<h2 class="mdl-card__title-text">{{ theme.title }}</h2>
…
<img [src]="theme.logo" alt="" width="200" height="200">
<p>{{ theme.description }}</p>
```

## Step 3 – Le routage

Cette étape a pour objectif de vous faire prendre en main le component **angular2/router**. Bien que s’agissant d’un module externe à Angular 2, il s’agit du module officiel de gestion de la **navigation**.
Ce qu’il est important de comprendre, c’est que **chaque composant peut être routable**. Dans Angular 2, **les routes se font entre composants et non entre vues**. Bien qu’il existe des règles globales à l’application, chaque composant gère ses propres règles de routage.

Le [slide Component Router](http://slides.com/wassimchegham/getting-started-with-angular-2#/8/25) illustre la configuration des routes et leur utilisation dans un template inline.
Utilisé dans le template, l’attribut **\[routerLink\]** crée un lien hypertexte vers un autre composant.
L’élément **<router-outlet>** équivaut au ng-view d’Angular 1.
L’annotation **@RouteConfig** permet de déclarer les routes. La syntaxe des points de suspensions du path (ex : '/details/ **…'**) permet de déléguer le routage à un autre composant.
Dans le constructeur d’un composant, il est possible de récupérer le paramètre d’URL via la classe **RouteParams**.

Le [slide Bootstraping the Router](http://slides.com/wassimchegham/getting-started-with-angular-2#/8/26) illustre l’initialisation du routeur qui a lieu dans le fichier principal (app.ts).
3 composants sont à importer :

1. **ROUTER\_PROVIDERS**: permet de récupérer les services du routeur
1. **PathLocationStragegy** ou **HashLocationStrategie**: type de navigation, par hash ou URL
1. **LocationStrategy**: permet de spécifier la stratégie de navigation à utiliser dans l’application

D’après les speakers, l’ambition de ce module router est d’arriver au même niveau que [UI Router](https://github.com/angular-ui/ui-router) avec des routes imbriquées (routes abstraites). Il est d'ailleurs dors et déjà [utilisable dans Angular 1](https://docs.angularjs.org/guide/component-router).
L’objectif du [**step3**](https://github.com/manekinekko/angular2-codelab/blob/master/STEPS.md#step-3-setting-up-the-router-and-question-component) est d’initier le composant QuestionCard puis de mettre en place la navigation entre le Home, ThemeCard et QuestionCard. A vous de jouer.

Dans la solution, 2 routes sont déclarées au niveau du composant parent Ng2CodelabApp :

1. une route principale **_/_** gérée par le composant Home et configurée pour être la route par défaut,
1. et une route **_/question_** gérée par le composant QuestionCard.

```js
@Component({
  selector: 'app',
  templateUrl: 'app/ng2codelab.html',
  directives : [Home, ROUTER_DIRECTIVES]
})
@RouteConfig([
    {
      path: '/',
      component: Home,
      name: 'Home',
      useAsDefault: true
  },
 {
  path: '/question',
    component: QuestionCard,
    name: 'QuestionCard'
 }
])
export class Ng2CodelabApp {
```

Dans le template _theme-card.html_, la directive **\[routerLink\]** génère le lien hypertexte _/question_.

```xhtml
<a [routerLink]="[ '/QuestionCard' ]" class="mdl-button mdl-button--colored mdl-js-button mdl-js-ripple-effect">
  Start test
</a>
```

Un clic sur le lien déclenche le routage vers le composant QuestionCard. Dans le DOM, la balise _<home>_ est remplacée par _<question-card>._

## Step 4 – Les providers

Entraperçu dans l’étape 2 lors de l’utilisation du _TechnologiesStore_, le **provider** est le thème central de cette 4ième étape.
Un provider est chargé de mettre une classe JavaScript à disposition d’un composant. Typiquement, un composant va avoir besoin d’un service qui interagit avec le backend pour récupérer / mettre à jour des données.
La mise en relation est basée sur l’ **injection de dépendance**(IoC). Pour rappel, Angular 1 est le premier framework front à avoir utilisé l’IoC. Son implémentation était assez rudimentaire. Angular 2 améliore ce premier coup d’essai en donnant davantage la main aux développeurs. Ainsi, un composant enfant pourra, par exemple, redéfinir les providers de son parent.

Angular 2 propose 2 types de providers :

1. [**Local**](http://slides.com/wassimchegham/getting-started-with-angular-2#/8/29) : permet d’utiliser un provider dans un composant. En ES6, il est nécessaire d’utiliser l’annotation @Inject
1. [**Global**](http://slides.com/wassimchegham/getting-started-with-angular-2#/8/30): injection à la racine de l’application. Mises-en garde : comme en Angular 1, tout provider est un singleton.

La fonction **provide()** d’angular-core permet de configurer les providers. [Le slide Providers Configuration](http://slides.com/wassimchegham/getting-started-with-angular-2#/8/32)  montre 3 syntaxes différentes.

Le [**step-4**](https://github.com/manekinekko/angular2-codelab/blob/master/STEPS.md#step-4-technology-component) consiste à afficher les questions d’une technologie, à maintenir les choix de l’utilisateur et à naviguer entre les questions.
Pour vous y aider, le service **QuestionStore** est mis à votre disposition :

```js
@Injectable()
export class QuestionsStore {

 private questions: IQuestion[];

 constructor(questions: IQuestion[] = QUESTIONS){
  this.questions = questions.map( (question: IQuestion) => new Question(question));
 }…
}
```

Ce service est injecté dans le composant **Technology** qui vous ait également fournit.

Une fois le step-4 réalisé, le composant QuestionCard est relativement concis :

```js
@Component({
  selector: 'question-card',
  encapsulation: ViewEncapsulation.None,
  templateUrl: './app/components/question-card/question-card.html',
  directives: [ROUTER_DIRECTIVES]
})
export class QuestionCard implements AfterViewInit {

 @Input() question: IQuestion;
 @Output() checked: EventEmitter<IChoice>;

 constructor() {
  this.checked = new EventEmitter();
 }

 onCheckedChange($event, choice: IChoice) {
  this.checked.emit(choice);
 }
}
```

La question à afficher lui est passée en paramètre @Input.
Et à chaque fois que l’utilisateur sélectionne / désélectionne une réponse, l’événement **_checked_** est envoyé au composant parent, à savoir Technology.
Le template de ce dernier binde l’événement sur la fonction toggle :

```js
template: `
  <question-card (checked)="toggle($event)"[question]="currentQuestion" class="mdl-cell mdl-cell--4-col" ></question-card> private toggle(choice: IChoice) {
  this.questions[this.currentQuestionId].toggle(choice);
}
```

## Step 5 – Smart components

Aucun slide « Break time » ne précède l’étape n°5. Cette dernière ne requière pas de nouvelles notions. Par contre, vous allez mettre en œuvre un autre type de composant : le **« smart » component** **Summary**. Les smarts components n’échangent pas seulement des données avec leur composant parent, mais lisent / écrivent des données via des services.
Dans cette étape, vous allez accéder au service **QuestionStore** depuis le composant **Summary**. Le QuestionStore sera mis à disposition par un _Provider_ de type _Factory_.

A vous d’implémenter le [**step-5**](https://github.com/manekinekko/angular2-codelab/blob/master/STEPS.md#step-5-summary-component).

La solution ne comporte pas de difficultés particulières. Le QuestionStore est injecté par constructeur. Et les questions sont récupérées en asynchrone via une promesse.

```js
@Component({
 providers: [
  new Provider(QuestionsStore, {
   useFactory: () => new QuestionsStore(SessionStore.read())
  })
 ],
 selector: 'summary',
 template: `
  <div>
   <div class="mdl-cell mdl-cell--9-col-desktop mdl-cell--6-col-tablet mdl-cell--4-col-phone">
    <div class="mdl-card__supporting-text">
     <h4>Your score is {{ score }}/{{ total }}</h4>
    </div>
   </div>
  </div>
  <question-card [question]="question" *ngFor="#question of questions"></question-card>
 `,
 directives: [QuestionCard],
 encapsulation: ViewEncapsulation.None
})
export class Summary implements OnInit{

private questions: IQuestion[];
private score: number;
private total: number;
private questionsStore: IQuestionsStore;

constructor(questionsStore: QuestionsStore) {
 this.questionsStore = questionsStore;
 this.questionsStore
  .fetch()
  .then( (questions) => this.questions = questions );
}
…
}

```

## Step 6 – Les pipes

Les filtres d’Angular 1 ont été renommées en **pipes**. Le concept et la syntaxe restent inchangés. Leur fonctionnement s’inspire des pipes Linux. Ils s’utilisent dans les templates pour transformer ou formater une donnée. Un pipe peut accepter des paramètres.
Angular 2 vient avec un certains nombres de [built-ins pipes](http://slides.com/wassimchegham/getting-started-with-angular-2#/8/37): DatePipe, UpperCase …
L’étape 6 consiste à créer son propre Pipe. Le slide [Custom Pipes](http://slides.com/wassimchegham/getting-started-with-angular-2#/8/36) montre comment utiliser l’annotation **@Pipe** pour déclarer un Pipe. Appuyez-vous sur cette exemple pour implémenter le [**step-6**](https://github.com/manekinekko/angular2-codelab/blob/master/STEPS.md#step-6-add-a-pipe).

Comme vous pouvez le constater, l’implémentation du **MarkPipe** est concise :

```js
import { Pipe } from 'angular2/core';
import { IChoice } from '../../services/question-store/question-store';

@Pipe({
 name: 'mark'
})
export class  MarkPipe {
 transform(choice: IChoice) {
  return choice.isCorrect() ? '✔' : '✘';
 }
}
```

Voici comment ce pipe est utilisé dans le template du composant QuestionCard :

```xhtml
<span *ngIf="preview" class="answer" >{{ choice | mark }}</span>
```

## Step 7 – Les directives

Cette dernière étape du Lab vous montre comment créer votre propre **Directive**. Le concept de directive structurelle n’a pas changé depuis Angular 1 : une directive permet d’attacher des comportements à des éléments customs du DOM. Un exemple sera bien plus parlant : [MyHighlightDirective](http://slides.com/wassimchegham/getting-started-with-angular-2#/8/41). L’usage de l’interface **Renderer** à la place d’un accès direct au DOM permet de rendre l’application portable (ex : rendu côté serveur).

Je vous laisse implémenter le [**step-7**](https://github.com/manekinekko/angular2-codelab/blob/master/STEPS.md#step-7-add-a-directive).
Et voici un extrait de la solution :

```js
import { Directive, ElementRef, Renderer, Input, AfterViewInit } from 'angular2/core';

@Directive({
  selector: '[status]'
})
export class StatusDirective implements AfterViewInit {

  @Input('status') status: boolean;

  constructor(
    private el: ElementRef,
    private renderer: Renderer
  ) {}

  ngAfterViewInit() {
    let color = this.status ? 'green' : 'red';
    this.renderer.setElementStyle(this.el.nativeElement, 'color', color);
  }
}
```

# Conclusion

Ce Lab vous aura permis de construire pas à pas une application de quizz tout en découvrant les fonctionnalités phares d’Angular 2.

Personnellement, j’ai trouvé le niveau de ce Lab élevé. Pour se débloquer, il est fréquent d’aller regarder la correction. Et le nombre de lignes de code à produire pour chaque étape est relativement conséquent. Le fait de ne connaître ni TypeScript ni ES6 aura été une difficulté supplémentaire.
La prise en main d’Angular 2 m’a demandé un investissement bien plus important que pour Angular 1. L’approche par composants n’est pas habituelle lorsqu’on a l’habitude de raisonner sur des pages. De mon point de vue, il est nécessaire de bien maîtriser ce framework avant de pouvoir l’utiliser efficacement.

Reste à savoir si Angular 2 réussira à s’imposer face à des frameworks plus légers tels ReactJS ? J’ai ouïe dire lors de Devoxx France que les Evangélistes Google le considéraient comme déjà mort … S’agit-il d’un troll ? Seul l’avenir nous le dira !
