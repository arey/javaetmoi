---
_edit_last: "1"
author: admin
categories:
  - spring
date: "2014-09-16T06:40:53+00:00"
thumbnail: /wp-content/uploads/2014/09/2014-09-input-spring-mvc-en-html5-logo.png
featureImage: /wp-content/uploads/2014/09/2014-09-input-spring-mvc-en-html5-logo.png
featureImageAlt: "Logo HTML 5"
guid: http://javaetmoi.com/?p=1199
parent_post_id: null
post_id: "1199"
post_views_count: "24640"
summary: |-
  [![Logo HTML 5](http://javaetmoi.com/wp-content/uploads/2014/09/2014-09-input-spring-mvc-en-html5-logo-150x150.png)](http://javaetmoi.com/wp-content/uploads/2014/09/2014-09-input-spring-mvc-en-html5-logo.png)

  Cet article explique comment **étendre Spring MVC pour générer le code HTML 5** **des champs de saisie** (input fields) à partir des **annotations Bean Validation** (JSR 330) apposées sur des Entités ou de simples DTO.

  Dans une application web **, valider les écrans de saisie côté client** permet de donner un retour rapide à l’utilisateur. Avant HTML 5, le développeur web était bien démuni pour implémenter ces contrôles de surface sur le Navigateur. Certes, HTML 4 permettait de spécifier la taille max des champs de saisie (balise _maxLength_) et leur caractère obligatoire ou non (balise _required_). Les autres contrôles effectués côté serveur étaient alors bien souvent recodés en JavaScript à l’aide de jQuery, de CSS et de quelques plugins.
  Aujourd’hui, HTML 5 se démocratise et le code JavaScript de validation devrait bientôt s’alléger drastiquement. En effet, cette spécification permet de standardiser la validation des champs de saisie côté client. Le développeur a désormais la possibilité de spécifier le type de champs (ex : nombre, date, URL …), des valeurs min et max ou bien encore un pattern de validation à l’aide d’une expression régulière.

  ![Logo HTML 5](/wp-content/uploads/2014/09/2014-09-input-spring-mvc-en-html5-logo.png)
tags:
  - bean-validation
  - hibernate
  - html-5
  - jsp
  - spring-mvc
  - tag
title: Validation HTML 5 avec Spring MVC et Bean Validation
url: /2014/09/validation-html-5-avec-spring-mvc-et-bean-validation/

---
[![Logo HTML 5](/wp-content/uploads/2014/09/2014-09-input-spring-mvc-en-html5-logo.png)](/wp-content/uploads/2014/09/2014-09-input-spring-mvc-en-html5-logo.png)

Cet article explique comment **étendre Spring MVC pour générer le code HTML 5** **des champs de saisie** (input fields) à partir des **annotations Bean Validation** (JSR 330) apposées sur des Entités ou de simples DTO.

Dans une application web **, valider les écrans de saisie côté client** permet de donner un retour rapide à l’utilisateur. Avant HTML 5, le développeur web était bien démuni pour implémenter ces contrôles de surface sur le Navigateur. Certes, HTML 4 permettait de spécifier la taille max des champs de saisie (balise _maxLength_) et leur caractère obligatoire ou non (balise _required_). Les autres contrôles effectués côté serveur étaient alors bien souvent recodés en JavaScript à l’aide de jQuery, de CSS et de quelques plugins.
Aujourd’hui, HTML 5 se démocratise et le code JavaScript de validation devrait bientôt s’alléger drastiquement. En effet, cette spécification permet de standardiser la validation des champs de saisie côté client. Le développeur a désormais la possibilité de spécifier le type de champs (ex : nombre, date, URL …), des valeurs min et max ou bien encore un pattern de validation à l’aide d’une expression régulière.

## Validation HTML 5

Dans l’exemple ci-dessous exploitant les capacités du HTML 5, **Google Chrome gère nativement la validation du formulaire et l’affichage du message d’erreur**.
Les icones sont obtenus à l’aide d’un style CSS utilisant les pseudo-classes _input:required:invalid_, _input:focus:invalid_ et input:required:valid.

[![2014-08-input-spring-mvc-en-html5-email-erreur](/wp-content/uploads/2014/09/2014-08-input-spring-mvc-en-html5-email-erreur1.png)](/wp-content/uploads/2014/09/2014-08-input-spring-mvc-en-html5-email-erreur1.png) Voici la représentation HTML de ce formulaire :

```xhtml
<form id="customer" action="/htmlvalidation" method="post">
	<div>
		<label>First Name</label>
		<input id="firstName" type="text" required="required" />
	</div>
	<div>
		<label>Last Name</label>
		<input id="lastName" type="text" required="required" />
	</div>
	<div>
		<label>Address</label>
		<input id="address" type="text" maxlength="20" />
	</div>
	<div>
		<label>City</label>
		<input id="city" type="text" required="required" />
	</div>
	<div>
		<label>Telephone</label>
		<input id="telephone"type="text" maxlength="10" />
	</div>
	<div>
		<label>Email</label>
		<input id="email" type="email" />
	</div>
	<div>
		<label>Website URL</label>
		<input id="website" type="url" />
	</div>
	<div>
		<label>Age</label>
		<input id="age" type="number" max="99" min="18" />
	</div>
	<div>
		<button type="submit">Add Customer</button>
	</div>
</form>
```

Dans la suite de cet article, **nous verrons comment Spring MVC peut générer ce code HTML 5.**

Attention toutefois, chaque navigateur implémente différemment cette norme.
Par exemple, sous Google Chrome 36, les champs de type _date_ sont particulièrement aboutis, avec masque de saisie et calendrier ; voir ci-dessous la représentation de la ligne HTML _Birthdate:_ <input type="date" name="birthdate"> . Par contre, ni Internet Explorer 11 ni Firefox 31 ne fournissent un tel confort de saisie.

[![Champs de saisie d'une date HTML 5 sous Google Chrome](/wp-content/uploads/2014/09/2014-09-input-spring-mvc-en-html5-date-sous-chrome.png)](/wp-content/uploads/2014/09/2014-09-input-spring-mvc-en-html5-date-sous-chrome.png)

## Bean Validation

Dans le monde Java, la [spécification Bean Validation](http://beanvalidation.org/) (JSR-303 et JSR-349) n’a plus à faire ses preuves. Elle s’est tout d’abord imposée au niveau de la couche de persistance. Ses annotations sont en effet utilisées par JPA pour générer la structure de la base de données et pour valider les données avant d’exécuter les ordres SQL d’insertion et de mise à jour. Bean Validation a ensuite fait son entrée au niveau de la couche de présentation : avec JSF 2 puis dans Spring MVC via l’annotation _@Valid_.
Enfin, Bean Validation peut également être utilisé en dehors de tout framework, par exemple pour valider les données en entrée d’un web service.

## Code HTML 5 généré

 **Spring MVC permet de binder bi-directionnellement un champ de saisie avec la propriété d’une classe**. Cette classe peut être aussi bien une **entité métier** qu’un simple **DTO**. En supposant que Bean Validation est utilisé pour valider les données de cette classe côté server, nous allons demander à Spring d’exploiter ces annotations lors de la génération des attributs HTML de la balise <input/> , et ceci via le tag JSP personnalisé <jem:input />  que nous allons développer.

Voici le code HTML 5 que nous aimerions que Spring MVC génère :
**Code Java****Page JSP****HTML 5 généré**@NotEmpty
String firstName;<jem:input path="firstName" /><input id="firstName" type="text" required="required" />@NotNull
String city;<jem:input path="city" /><input id="city" type="text" required="required" />@Size(max=40)
String address;<jem:input path="address" /><input id="address" type="text" maxlength="40" />@Size(max=40)
String address;<jem:input path="address" maxlength="20"/><input id="address" type="text" maxlength="20" />@Min(value = 18)   @Max(value=99)   Integer age;<jem:input path="age" /><input id="age" type="number" max="99" min="18" />@Email
String email;<jem:input path="email" /><input id="email" type="email" />@URL
String website;<jem:input path="website" /><input id="website" type="url" />Integer birthYear;<jem:input path="birthYear" /><input id="birthYear" type="number" />Remarques :

- Les attributs font parties de la classe _Customer_. Côté contrôleur web, une instance est ajoutée au modèle Spring MVC de la vue.
- Le préfixe <jem: permet de distinguer notre balise personnalisée avec la balise input de Spring MVC (<form:input />)
- Les tags <jem:input />  sont disposés dans le formulaire <form:form modelAttribute="customer">

Si besoin est, l’attribut maxlength peut être redéfini manuellement via le tag <jem:input /> .

## Mise en œuvre

L’implémentation du tag [**_Html5InputTag_**](https://github.com/arey/spring-mvc-toolkit/blob/spring-mvc-toolkit-reactor-0.1/spring-mvc-toolkit/src/main/java/com/javaetmoi/core/mvc/tag/Html5InputTag.java) interprétant les contraintes Bean Validation demande un peu moins de 200 lignes de code. Elle spécialise la classe [_org.springframework.web.servlet.tags.form.InputTag_](https://github.com/spring-projects/spring-framework/blob/v4.0.6.RELEASE/spring-webmvc/src/main/java/org/springframework/web/servlet/tags/form/InputTag.java) de Spring MVC.
Trois méthodes y sont redéfinies :

1. Avant d’appeler la méthode parent, la méthode **_writeTagContent_** analyse la propriété à binder à la recherche de contraintes matérialisées par des annotations Bean Validation. Le résultat est stocké dans une _Map_ et sera utilisé dans les 2 autres méthodes.
1. En complément des attributs _type_ et _value_, la méthode **_writeValue_** est chargée d’écrire les attributs _maxLength_, _min_, _max_ et _required_ à partir des contraintes portées par la propriété à binder.
1. Enfin, la méthode **_getType_** détermine la valeur de l’attribut _type_ en fonction du type de la propriété à binder (ex : Integer) ou des contraintes qu’elle porte.

Pour davantage de détails, voici le code source complet de la classe [**_Html5InputTag_**](https://github.com/arey/spring-mvc-toolkit/blob/spring-mvc-toolkit-reactor-0.1/spring-mvc-toolkit/src/main/java/com/javaetmoi/core/mvc/tag/Html5InputTag.java):

```java
Extrait de la classe Html5InputTag.java
```

Cette classe peut être reprise et adaptée en fonction de vos besoins.

## Tests unitaires

La classe [**_TestHtml5InputTag_**](https://github.com/arey/spring-mvc-toolkit/blob/spring-mvc-toolkit-reactor-0.1/spring-mvc-toolkit/src/test/java/com/javaetmoi/core/mvc/tag/TestHtml5InputTag.java) teste unitairement chacune des annotations Bean Validation supportés par le tag.
A titre d’exemple, voici la méthode testant le HTML généré à partir de l’annotation _@Size_ :

```java
Extrait de la classe TestHtml5InputTag.java
```

## Intégration manuelle du tag

Pour utiliser cette classe dans une application Spring MVC, il est nécessaire de déclarer le tag correspondant dans un fichier TLD qui sera analysé par le conteneur web à son démarrage. Ce descripteur doit se situer dans le répertoire _WEB-INF\\tld_ (pour un WAR) ou _META-INF\\tld_ (pour un JAR).

La description du tag reprend exactement celle du tag input de Spring MVC déclaré dans le descripteur [META\_INF/spring-form.tld](https://github.com/spring-projects/spring-framework/blob/v4.0.6.RELEASE/spring-webmvc/src/main/resources/META-INF/spring-form.tld) du module spring-webmvc. Seule l’implémentation change.

## Taglib prête à l’emploi

Pour faciliter l’intégration de ce tag, le [**projet open source spring-mvc-toolkit**](https://github.com/arey/spring-mvc-toolkit/tree/master/spring-mvc-toolkit) propose un [taglib](https://github.com/arey/spring-mvc-toolkit/blob/spring-mvc-toolkit-reactor-0.1/spring-mvc-toolkit/src/main/resources/META-INF/tld/javaetmoi-mvc.tld). L’URI du taglib est _/core/spring-mvc_

Afin de pouvoir l’utiliser sur une application existante, l’ajout de la dépendance maven suivante est nécessaire :

```xhtml
<dependency>
     <groupId>com.javaetmoi.core</groupId>
     <artifactId>spring-mvc-toolkit</artifactId>
     <version>0.1</version>
</dependency>
```

Lors d’un mvn clean install , le JAR sera téléchargé depuis [Maven Central](http://repo1.maven.org/maven2/com/javaetmoi/core/spring-mvc-toolkit/).

## Démo

Le [projet spring-mvc-toolkit](https://github.com/arey/spring-mvc-toolkit) vient avec une [**application démo**](https://github.com/arey/spring-mvc-toolkit/tree/master/spring-mvc-toolkit-demo) mettant en œuvre les différentes fonctionnalités offertes par le projet
La [**page htmlvalidation.jsp**](https://github.com/arey/spring-mvc-toolkit/blob/spring-mvc-toolkit-reactor-0.1/spring-mvc-toolkit-demo/src/main/webapp/WEB-INF/pages/htmlvalidation.jsp) montre comment utiliser le tag _Html5InputTag_. Remarquez qu’aucun code JavaScript n’est utilisé. Afin d’uniformiser le comportement sur l’ensemble des navigateurs, 2 styles CSS sont appliqués aux pseudo-classes _:valid_ et _:invalid_ pour afficher des icônes à droite du champ de saisie.

Dans le [pom.xml](https://github.com/arey/spring-mvc-toolkit/blob/spring-mvc-toolkit-reactor-0.1/spring-mvc-toolkit-demo/pom.xml) de cette application web de démo, le plugin Jetty pour maven est préconfiguré.

Voici la démarche à suivre pour tester la page :

1. Récupérer le code hébergé sur GitHub :
   git clone git://github.com/arey/spring-mvc-toolkit.git
1. Construire le projet avec maven :
   cd spring-mvc-tookit mvn clean install
1. Démarrer Jetty
   cd spring-mvc-toolkit-demomvn jetty:run-war
1. Accéder à la page de test du tag depuis votre Navigateur :
   [http://localhost:8080/htmlvalidation](http://localhost:8080/htmlvalidation)

## Conclusion

Cet article aura montré comment étendre les tags JSP de Spring MVC pour ajouter la validation côté client apportée par HTML 5. L’enrichissement du HTML généré par les tags se base sur les contraintes Bean Validation.

A ce jour, la classe [**_Html5InputTag_**](https://github.com/arey/spring-mvc-toolkit/blob/spring-mvc-toolkit-reactor-0.1/spring-mvc-toolkit/src/main/java/com/javaetmoi/core/mvc/tag/Html5InputTag.java) supporte 4 annotations Bean Validation ( _@Min, @Max_, _@NotNull_ et _@Size_) et 3 annotations spécifiques à Hibernate Validator ( _@Email_, _@NotEmpty_ et _@URL_).
Le support d’autres annotations pourraient être ajouté. L’annotation _@Pattern_ pourrait par exemple générer l’attribut _pattern_ qui accepte une expression régulière. La difficulté réside dans l’adaptation d’une regex Java en regex JavaScript, [ce qui a été fait dans le sens inverse par l’équipe GWT](https://gwt.googlesource.com/gwt/+/release/2.6/user/src/com/google/gwt/regexp/shared/RegExp.java).
Le support des groups Bean Validation pourrait également être ajouté.
Enfin, ce qui a ici été appliqué pour la classe _InputTag_ peut l’être à moindre échelle sur la classe _TextAreaTag_.

Références :

1. [HTML5 Form Validation Examples](http://www.the-art-of-web.com/html/html5-form-validation/)
1. [Formulaires HTML5 : placeholder, required, pattern et validation](http://www.alsacreations.com/tuto/lire/1391-formulaire-html5-placeholder-required-pattern.html)
1. [Classe RegExp.java de GWT](https://gwt.googlesource.com/gwt/+/release/2.6/user/src/com/google/gwt/regexp/shared/RegExp.java)
