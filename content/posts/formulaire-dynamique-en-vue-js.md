---
_edit_last: "1"
author: admin
categories:
  - retour-d'expérience
date: "2017-05-18T16:15:36+00:00"
guid: http://javaetmoi.com/?p=1726
parent_post_id: null
post_id: "1726"
post_views_count: "24928"
summary: |-
  Dans ce billet, nous allons mettre en pratique l’initiation à Vue.js reçue le mois dernier. Je vous propose de **coder un pseudo Google Form** avec l’aide de [**Vue.js**](https://vuejs.org/), de **Bootsrap** et du framework de validation [**VeeValidate**](http://vee-validate.logaretm.com/).
  Le **formulaire HTML** est généré automatiquement à partir d’un **paramétrage JSON** récupéré par une API REST. Nous n’aborderons pas ici la partie serveur.
  Un utilisateur peut sauvegarder son formulaire à l’état de brouillon afin de poursuivre ultérieurement sa saisie. Le formulaire à afficher peut donc être pré-saisi.
  La **validation** est **dynamique**: elle se fait au fur et à mesure de la saisie du formulaire.
  Voici un exemple de formulaire :

  [![](http://javaetmoi.com/wp-content/uploads/2017/05/2017-05-Formulaire-dynamique-en-Vue.js-1024x694.png)](http://javaetmoi.com/wp-content/uploads/2017/05/2017-05-Formulaire-dynamique-en-Vue.js.png)
tags:
  - javascript
  - vue.js
title: Formulaire dynamique en Vue.Js
url: /2017/05/formulaire-dynamique-en-vue-js/

---
Dans ce billet, nous allons mettre en pratique l’initiation à Vue.js reçue le mois dernier. Je vous propose de **coder un pseudo Google Form** avec l’aide de [**Vue.js**](https://vuejs.org/), de **Bootsrap** et du framework de validation [**VeeValidate**](http://vee-validate.logaretm.com/).
Le **formulaire HTML** est généré automatiquement à partir d’un **paramétrage JSON** récupéré par une API REST. Nous n’aborderons pas ici la partie serveur.
Un utilisateur peut sauvegarder son formulaire à l’état de brouillon afin de poursuivre ultérieurement sa saisie. Le formulaire à afficher peut donc être pré-saisi.
La **validation** est **dynamique**: elle se fait au fur et à mesure de la saisie du formulaire.
Voici un exemple de formulaire :

[![](/wp-content/uploads/2017/05/2017-05-Formulaire-dynamique-en-Vue.js.png)](/wp-content/uploads/2017/05/2017-05-Formulaire-dynamique-en-Vue.js.png)

## Démo live

Avant de passer aux explications, mettons en action ce formulaire. HTML, code JavaScript et rendu graphique sont accessibles dans [ce snippet JSFiddle](https://jsfiddle.net/Elryk/dz3m4mpv/) codé avec Vue 2.2, VeeValidate 2.0 et Bootstrap 3.3 :

## Le modèle objet du formulaire

Vue.js implémentant le **pattern MVC**, intéressons-nous au **modèle objet** sous-jacent à notre formulaire :

- Un **formulaire** est composé d’une **liste de questions**.
- Chaque **question** comporte un **libellé** suivi d’un **champ de saisi**.
- Le champ de saisi peut différer en fonction du type question : zone de saisie sur une ligne, radio bouton, liste déroulante, zone de texte multi-lignes …

Le paramétrage du formulaire (et son état courant) est décrit sous forme d’un tableau de questions en notation littérale JavaScript :

```js
var formParameters =
    [ { id: 1, label: 'First Name', type: 'input', answer: 'Antoine' },
      { id: 2, label: 'Last Name', type: 'input' },
      { id: 3, label: 'Email', type: 'input'},
      { id: 4, label: 'Job', type: 'select', options: ['...', 'Developer', 'Ops', 'Project Manager'], answer: 'Developer' },
      { id: 5, label: 'Gender', type: 'radio', options: ['Male', 'Female'], answer: 'Male'},
      { id: 6, label: 'Address', type: 'textarea', placeholder: 'Your zip code and city'}
    ];
```

En pratique, le paramétrage du formulaire sera récupéré par API REST au chargement de la page. Afin de rendre autonome notre exemple, il y est hard-codé.
Voici à quoi ressemble le point d’entrée de notre application Vue.js :

```js
var app = new Vue({
        el: '#dynform',
        data: {
            questions: []
        },
        created: function () {
            // Dynamic Form could be load from a REST API
            this.questions.push(formParameters);
        }
    });
```

Le tableau de questions (notre modèle) est stocké dans l’objet data de l’instance Vue.

## Arbre de composants

Orienté composants, **Vue.js permet de structurer la génération du formulaire à l’aide de plusieurs composants**.
Le composant générique _<form-question>_ est responsable d’afficher le libellé de la question puis de sélectionner le sous-composant approprié pour la zone de saisie. Exemple : un _<form-radio>_ lorsque la question est de type radio. Il gère également l’affichage du caractère wildcard \* lorsque la question est obligatoire.

## La page HTML

La majorité du code HTML est localisé dans les templates Vue.js des sous-composants. Le code HTML de la page du formulaire est réduit à un simple _<form>_ générant autant de balises _<form-question>_ que de questions paramétrées dans le modèle du formulaire :

```xhtml
<form id="dynform" class="panel-body form-horizontal" v-on:submit.prevent="displayForm">
    <div class="row">
        <div class="col-md-12 ">
            <form-question v-for="question in questions" :question="question"
                           :key="question.id"></form-question>
        </div>
    </div>
    <button type="submit" class="btn btn-primary">Submit</button>
</form>
```

La soumission du formulaire déclenche la fonction _displayForm_ dont nous verrons l’implémentation par la suite.

## Le composant <form-question>

Le **composant _<form-question>_** accepte en paramètre l’une des questions de notre formulaire.
Conditionnel, **son template est généré dynamiquement en JavaScript** par concaténation de String. Ne pouvant utiliser la propriété _template_, il est initialisé dans la **fonction _created_** au travers de la propriété **_this.$options.template_**.

```js
Vue.component('form-question', {
    props: ['question'],
    created: function () {
        this.$options.template = '<div class="form-group"> ' +
            '<label :for="question.id" class="col-sm-3 col-lg-2 control-label">' +
            '{{question.label}}';
        if (this.question.required || ((this.question.validate !== undefined) && this.question.validate.match("required"))) {
            this.$options.template += '<em>*</em>'
        }
        this.$options.template += '</label>' +
            '<div class="col-sm-9 col-lg-10">';
        switch (this.question.type) {
            case 'input'  :
                this.$options.template += '<form-input :question="question"></form-input>';
                break;
            case 'select' :
                this.$options.template += '<form-select :question="question"></form-select>';
                break;
            ...
        }
        this.$options.template +=
            '</div>' +
            '</div>';
    }
});
```

Le switch case permet de sélectionner le sous-composant Vue à afficher : _<form-input>_, _<form-select>_, _<form-radio>_ et _<form-textarea>_. Chacun d’eux accepte un seul paramètre : la question courante à afficher.

## Form Input

Au travers du _<form-input>_, regardons de plus près à quoi ressemble un **sous-composant**. Voici une version dénudée de validation :

```js
Vue.component('form-input', {
    props: ['question'],
    template: '<div class="form-group">' +
    '<input :name="question.label" :id="question.id" type="text" class="form-control"' +
    '       v-model="question.answer"  :placeholder="question.placeholder"/>' +
    '</div>'
});
```

Les attributs _id_, _name_ et _placeholder_ sont attribués par **binding** en utilisant la syntaxe raccourcie de _v-bind:name="question.label"_.
La valeur du champs de saisie référence le modèle question.answer.

Les autres sous-composants sont conçus sur le même modèle.

## Validation du formulaire

La validation du formulaire est implémentée à l’aide de la librairie [VeeValidate](http://vee-validate.logaretm.com/).
Chaque question du modèle se voit ajouter un **attribut _validate_** spécifiant les **contraintes de validation** à l’aide de la syntaxe VeeValidate.
Exemple sur le nom de famille qui est requis, ne doit comporter que des caractères alphabétiques et au minimum 2 caractères :

```js
{id: 2, label: 'Last Name', type: 'input', validate: "required|alpha|min:2"}
```

Le template de chaque sous-composant est agrémenté avec un **attribut _v-validate_** bindé sur le modèle _validate_. En cas d’erreur de validation, le message d’erreur est affiché dans un _<span>_ et la classe CSS _has-error_ de Bootstrap et ajouté au _<div>_ englobant de type _form-group_.
Complétons ainsi notre exemple du sous-composant _<form-input>_:

```js
Vue.component('form-input', {
    props: ['question'],
    template: '<div class="form-group" :class="{\'input\': true, \'has-error\': errors.has(question.label) }">' +
    '<input type="text" v-validate="question.validate" :id="question.id" :name="question.label"'+
    'class="form-control" v-model="question.answer":placeholder="question.placeholder"/>' +
    '    <span v-show="errors.has(question.label)" class="help-block">{{ errors.first(question.label) }}</span>' +
    '</div>'
});
```

## Factorisation du template de gestion des erreurs

La gestion des **erreurs de validation** est identique sur chaque sous-composant.
Le _<div class="form-group">_ se voit ajouter la classe CSS Boostrap **_has-error_** lorsque VeeValidate détecte une ou plusieurs erreurs.
Le **_<span>_** affiche le 1er **message d’erreur** détecté.
Ayant toutes 2 besoins d’accéder à la propriété _errors_ locale au sous-composant, ces balises HTML ne peuvent être remontées dans le composant _<form-question>_.
Pour éviter la duplication de code HTML dans les template, il est néanmoins possible de factoriser le code dans une fonction _questionTemplate_ :

```js
function questionTemplate(customField) {
    return '<div class="form-group" :class="{\'input\': true, \'has-error\': errors.has(question.label) }">' +
        customField +
        '<span v-show="errors.has(question.label)" class="help-block">{{ errors.first(question.label) }}</span>' +
        '</div>'
}

Vue.component('form-input', {
    props: ['question'],
    template: questionTemplate('<input v-validate="question.validate" :name="question.label" :id="question.id" type="text" class="form-control" v-model="question.answer" :placeholder="question.placeholder"/>')
});
```

A noter que cette factorisation n’a pas été mise en œuvre dans le snippet JSFiddle.

## Validation globale

Avant de soumettre au serveur le formulaire, une validation globale est réalisée côté client.
En cas de succès, le snippet affiche au format JSON les données à transmettre. En cas d’erreur, il affiche leur nombre et les messages d’erreur à côté de chaque champ en erreur.

La validation d’un formulaire composé de plusieurs sous-composants n’est pas native avec VeeValidate, preuve en est l’issue [Can't validate form with multiple child components](https://github.com/logaretm/vee-validate/issues/56). Plutôt que de passer par un composant faisant office de bus de messages, j’ai choisi d’utiliser l’ [API de validation](http://vee-validate.logaretm.com/api.html).
L’instance _$validator_ de l’application Vue est recyclée. Les contraintes de validation de chaque champ lui sont rattachées (méthode _attach_). L’objet _data_ référence les données du formulaire à valider. Cet objet est passé à la méthode de validation _validateAll_ qui accepte 2 fonctions de callback :

1. En cas de succès (méthode _then_), un tableau contenant les données à soumettre au serveur est construit puis, dans le cadre de la démo, affiché simplement dans une popup.
1. Lorsqu’un ou plusieurs champs sont invalides (méthode _catch_), un artifice consistant à itérer sur l’ensemble des sous-composants et à déclencher leur validation individuelle permet d’afficher le message d’erreur local et d’activer le style CSS approprié. Le nombre de champs invalide est affiché dans une popup.

```js
methods: {
    displayForm: function(event) {
        var $this = this;
        var $validator = this.$validator;
        var data = {};
        this.questions.forEach(function(question) {
            if (question.validate !== undefined) {
                $validator.attach(question.label, question.validate);
                data[question.label] = question.answer;
            }
        });
        var $questions = this.questions;
        $validator.validateAll(data).then(function() {
            var form = [];
            $questions.forEach(function(question) {
                form.push({
                    id: question.id,
                    label: question.label,
                    answer: question.answer
                });
            });
            alert("Valid form: "+JSON.stringify(form));
        }).catch(function(error) {
            $this.$children.forEach(function(child) {
                child.$children.forEach(function(child) {
                    child.$validator.validateAll().then(function() {}).catch(function() {});

                });
            });
            alert("Invalid form. Error count:  " + $validator.getErrors().count());
        })
    }
}
```

## Conclusion

En une **centaine de lignes de code JavaScript**, nous disposons d’une application web capable d’afficher n’importe quel **formulaire décrit en JSON**.
Pour l’instant limité, le nombre de champs de saisie ne demande qu’à être étendu : sélection multiple, date avec calendrier, upload de fichiers …

Pour des questions de sécurité et d’intégrité des données, la **validation** effectuée côté client devra être redondée **côté serveur**.
