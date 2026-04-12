---
_edit_last: "1"
author: admin
categories:
  - spring
date: "2014-10-14T04:53:33+00:00"
thumbnail: wp-content/uploads/2014/05/logo-spring-highres.png
featureImage: wp-content/uploads/2014/05/logo-spring-highres.png
featureImageAlt: "logo-spring-highres"
guid: http://javaetmoi.com/?p=1216
parent_post_id: null
post_id: "1216"
post_views_count: "17022"
summary: '[![logo-spring-highres](http://javaetmoi.com/wp-content/uploads/2014/05/logo-spring-highres-300x225.png)](http://javaetmoi.com/wp-content/uploads/2014/05/logo-spring-highres.png) Le développement d’applications web requière une vigilance toute particulière quant à l’utilisation de la **session web**. Spring MVC offre les mécanismes permettant aux développeurs de ne plus manipuler directement l’objet **_HttpSession_** mis à disposition par le conteneur web. Les 2 annotations **_@Scope("session")_** et **_@SessionAttributes_** en font parties. Dans ce billet, je vous expliquerai **le fonctionnement de l’annotation _@SessionAttributes_** qu’il est essentiel de maitriser avant d’utiliser. Nous verrons qu’elle fonctionne de pair avec l’annotation **_@ModelAttribute_** et qu’elle permet de simuler une **portée conversation**. Nous commencerons cet article par rappeler ce qu’est **un modèle** et nous le terminerons en **testant** **unitairement** du code qui utilise _@SessionAttributes_.'
tags:
  - mvc
  - spring-mvc
  - test
title: Démystifier l’annotation @SessionAttributes de Spring MVC
url: /2014/10/annotation-sessionattributes-modelattribute-spring-mvc/

---
[![logo-spring-highres](wp-content/uploads/2014/05/logo-spring-highres.png)](wp-content/uploads/2014/05/logo-spring-highres.png) Le développement d’applications web requière une vigilance toute particulière quant à l’utilisation de la **session web**. Spring MVC offre les mécanismes permettant aux développeurs de ne plus manipuler directement l’objet **_HttpSession_** mis à disposition par le conteneur web. Les 2 annotations **_@Scope("session")_** et **_@SessionAttributes_** en font parties. Dans ce billet, je vous expliquerai **le fonctionnement de l’annotation _@SessionAttributes_** qu’il est essentiel de maitriser avant d’utiliser. Nous verrons qu’elle fonctionne de pair avec l’annotation **_@ModelAttribute_** et qu’elle permet de simuler une **portée conversation**. Nous commencerons cet article par rappeler ce qu’est **un modèle** et nous le terminerons en **testant** **unitairement** du code qui utilise _@SessionAttributes_.

## Le modèle de Spring MVC

Comme son nom l’indique, Spring MVC est un framework de présentation basé sur le pattern **M** odel **V** iew **C** ontroller. Un modèle est mis à disposition de la vue par le contrôleur, par exemple pour alimenter les listes déroulantes lors du rendu de la page HTML. Un modèle peut également être soumis au contrôleur par la vue (post de formulaire) ; on parle alors de **« command object »**. La conversion de données (ou binding) entre des chaînes de caractères du protocole HTTP et la représentation Java du modèle est assuré par les [_Converter_](https://github.com/spring-projects/spring-framework/blob/v4.1.1.RELEASE/spring-core/src/main/java/org/springframework/core/convert/converter/Converter.java) et les [_Formatter_](https://github.com/spring-projects/spring-framework/blob/v4.1.1.RELEASE/spring-context/src/main/java/org/springframework/format/Formatter.java) configurés au démarrage du contexte Spring ou via l’annotation [_@InitBinder_](https://github.com/spring-projects/spring-framework/blob/v4.1.1.RELEASE/spring-web/src/main/java/org/springframework/web/bind/annotation/InitBinder.java) pour du sur-mesure. Un **binding bi-directionnel** est mis en œuvre sur un modèle utilisé conjointement pour le rendu de la page et la soumission de données (ex : formulaire d’édition).
Spring MVC représente le modèle comme un ensemble de clé-valeur (tableau associatif). La clé est une chaine de caractère. La valeur peut-être de n’importe quel type. La classe [**_ModelMap_**](https://github.com/spring-projects/spring-framework/blob/v4.1.1.RELEASE/spring-context/src/main/java/org/springframework/ui/ModelMap.java) implémente cette représentation. Elle étend la classe _java.util.LinkedHashMap_.

Dans les contrôleurs Spring MVC, il est possible de manipuler l’interface **_Model_** pour ajouter manuellement des données au modèle soit directement, soit par l’utilisation de la classe _ModelAndView_. Voici un exemple tiré du manuel de référence de Spring Framework :

```java
@ModelAttribute
public void populateModel(@RequestParam String number, Model model) {
        model.addAttribute(accountManager.findAccount(number));
}
```

Pour implémentation de l’interface [_Model_](https://github.com/spring-projects/spring-framework/blob/v4.1.1.RELEASE/spring-context/src/main/java/org/springframework/ui/Model.java), Spring MVC utilise la classe [_BindingAwareModelMap_](https://github.com/spring-projects/spring-framework/blob/v4.1.1.RELEASE/spring-context/src/main/java/org/springframework/validation/support/BindingAwareModelMap.java) qui étend indirectement [_ModelMap_](https://github.com/spring-projects/spring-framework/blob/v4.1.1.RELEASE/spring-context/src/main/java/org/springframework/ui/ModelMap.java).
Dans cet exemple, l’instance renvoyée par l’appel à la méthode _findAccount_ est de type _Account_. La clé est calculée par convention de nommage via la classe [_org.springframework.core.Conventions_](https://github.com/spring-projects/spring-framework/blob/v4.1.1.RELEASE/spring-core/src/main/java/org/springframework/core/Conventions.java). Il est bien entendu possible d’utiliser la méthode model.addAttribute("account", accountManager.findAccount(number));  pour spécifier une clé.

L’enrichissement du modèle peut également être réalisé sans manipulation de l’interface _Model_ :

```java
@ModelAttribute
public Account addAccount(@RequestParam String number) {
        return accountManager.findAccount(number);
}
```

Sur mes applications, je privilégie cette seconde syntaxe qui est moins verbeuse et permet de découper le code en autant de méthodes que d’objets à ajouter dans le modèle.

D’un point de vue technique, les 2 exemples présentés ci-dessus sont équivalents. Concentrons-nous à présent sur le rôle de L’annotation _@ModelAttribute_.

## Annotation @ModelAttribute sur les méthodes

 **Le comportement de l’annotation** [**_@ModelAttribute_**](https://github.com/spring-projects/spring-framework/blob/v4.1.1.RELEASE/spring-web/src/main/java/org/springframework/web/bind/annotation/ModelAttribute.java) **diffère en fonction de là où elle est apposée** :

1. sur les méthodes des contrôleurs
1. sur les paramètres des méthodes des contrôleurs.

Dans les exemples précédents, l’annotation _@ModelAttribute_ annote une méthode d’un contrôleur. Elle indique à Spring MVC que la méthode est responsable de préparer le modèle. A noter que plusieurs méthodes d’un même contrôleur peuvent être annotés avec _@ModelAttribute_. **Spring MVC appelle toutes les méthodes _@ModelAttribute_ avant d’appeler la méthode _@RequestMapping_** (également appelé handler) chargée de traiter la requête HTTP en appelant les services métiers.

**Les données ajoutées au modèle dans les méthodes _@ModelAttributes_ sont ensuite accessibles à la méthode _@RequestMapping_.**

Dans le second exemple, la méthode _addAccount_ renvoie un _Account_ sans manipuler l’interface Model. **Spring MVC sait implicitement que l’objet retourné par une méthode _@ModelAttribute_ doit être ajouté au modèle.** Pour la clé, il utilise les mêmes conventions de nommage que la méthode addAttribute(Object attributeValue) . Il est possible de spécifier la clé en utilisant la syntaxe @ModelAttribute("account") .

Une fois l’appel à la méthode _@RequestMapping_ réalisé, et avant le rendu de la vue, Spring MVC doit mettre à disposition de la vue le modèle.
Par défaut, Spring MVC utilise les attributs de la requête. Tout se joue dans la méthode _exposeModelAsRequestAttributes_ de la classe [_AbstractView_](https://github.com/spring-projects/spring-framework/blob/v4.1.1.RELEASE/spring-webmvc/src/main/java/org/springframework/web/servlet/view/AbstractView.java). Les objets du modèle sont ajoutés aux attributs de la requête comme on pourrait le faire en manipulant l’API Servlet :
request.setAttribute(modelName, modelValue);

Lorsque le mode debug est activée, la trace suivante est généré dans les logs :

```sh
18:42:41.702 [qtp20079748-21] DEBUG o.s.web.servlet.view.JstlView - Added model object 'account' of type [com.javaetmoi.core.mvc.demo.model.Account] to request in view with name 'accountdetail'
```

Ici, la vue est une JSP utilisant les tags JSTL.

Dans le corps de la page JSP, il est alors possible d’utiliser une Expression Language (EL) évaluant les propriétés du modèle :
<c:out value="${account.number}" />

Attention aux performances

L’annotation _@ModelAttribute_ peut causer des problèmes de performance si l’on ne maîtrise pas son cycle d’appel dans les contrôleurs de Spring MVC.

En effet, l'appel systématique aux méthodes _@ModelAttribute_ à chaque rafraichissement de page peut détériorer les performances d’une application lorsqu’un appel à un ou plusieurs web services et/ou DAO est nécessaire pour construire le modèle.

**L'utilisation de l'annotation _@SessionAttributes_ ou d'un cache applicatif permet d'enrayer ce type de déconvenue**.

## L’annotation @SessionAttributes

Les handlers des contrôleurs Spring MVC (annotés avec _@RequestMapping)_ acceptent en paramètre de nombreux types de paramètres ; les interfaces _HttpSession_ et _HttpServletRequest_ en font partie. Un développeur peut donc directement manipuler _HttpSession_ pour ajouter en session des données du modèle qu’ils voudraient voir conserver sur plusieurs requêtes HTTP.

Afin de simplifier le code d’accès à la session web, et toujours dans l’idée d’éviter de manipuler directement la session, **Spring MVC propose l’annotation** [**_@SessionAttributes_**](https://github.com/spring-projects/spring-framework/blob/v4.1.1.RELEASE/spring-web/src/main/java/org/springframework/web/bind/annotation/SessionAttributes.java). Cette annotation se déclare au niveau de la classe de type _@Controller_. Ses 2 propriétés value et _type_ permettent de lister respectivement le nom des modèles (le nom des clés) et/ou le type de modèle à sauvegarder de manière transparente dans la session HTTP.

**Avant le rendu de la vue, Spring MVC copie par référence les attributs du modèle référencés par _@SessionAttributes_ dans la session**. Les attributs du modèle seront alors à la fois disponible en tant qu’attribut de la requête ( _HttpServletRequest_) et de la session ( _HttpSession_).
Pour persister les données du modèle en session, Spring MVC utilise l’abstraction [_SessionAttributeStore_](https://github.com/spring-projects/spring-framework/blob/v4.1.1.RELEASE/spring-web/src/main/java/org/springframework/web/bind/support/SessionAttributeStore.java). L’implémentation par défaut repose sur la session HTTP. Mais on pourrait très bien imaginer une implémentation utilisant un cache de données distribué (type [Redis](http://redis.io/) ou [GemFire](http://www.vmware.com/products/vfabric-gemfire/overview)) ou une base NoSQL. Gains escomptés de cette approche :

- Affinité de session plus nécessaire
- Tolérance aux pannes renforcées
- Livraisons sans interruption de service

Cette ouverture sera peut-être prochainement exploitée par le [**nouveau projet spring-session**](https://github.com/spring-projects/spring-session).

Une autre facilité apportée par l’annotation _@SessionAttributes_ est d’ **éviter au développeur de tester si un objet existe déjà en session avant de l’instancier/ou de le récupérer puis de l’ajouter à la session**.
En effet, avant d’invoquer la méthode _@RequestMapping_ cible, Spring MVC commence par initialiser le modèle du contrôleur (méthode _RequestMappingHandlerAdapter#invokeHandleMethod_). Dans un premier temps, il **restaure les attributs du modèle qui sont en session**(méthode _ModelFactory# initModel_). Dans un second temps, il itère sur les méthodes annotées par _@ModelAttributes_(méthode _ModelFactory#invokeModelAttributeMethods_). **Avant d’appeler chaque méthode _@ModelAttributes_, il vérifie si l’attribut retourné n’existe pas déjà dans le modèle** (et donc préalablement en session).

Le diagramme d’activités ci-dessous illustre le mécanisme complet :

[![2014-09-spring-mvc-sessionattributes-diagram](wp-content/uploads/2014/10/2014-09-spring-mvc-sessionattributes-diagram1.png)](wp-content/uploads/2014/10/2014-09-spring-mvc-sessionattributes-diagram1.png)

## Libérer la mémoire

A présent que nous avons vu comment ajouter des données en session, apprenons à les retirer, et ceci toujours sans manipuler l’interface _HttpSession_. Pour se faire, Spring MVC met à disposition [l’ **interface _SessionStatus_**](https://github.com/spring-projects/spring-framework/blob/v4.1.1.RELEASE/spring-web/src/main/java/org/springframework/web/bind/support/SessionStatus.java).
**La méthode _setComplete()_ permet de supprimer de la session tous les attributs référencés par l’annotation _@ModelAttributes_ du contrôleur où elle est appelée.**

Comme le montre l’exemple de code tiré du [projet spring-mvc-toolkit](https://github.com/arey/spring-mvc-toolkit), Spring MVC sait passer au handler une instance de _SessionStatus_ :

```java
@RequestMapping("/endsession")
public String endSessionHandlingMethod(SessionStatus status){
        status.setComplete();
        return "sessionsattributepage";
}
```

Lorsqu’un attribut a été retiré de la session (" _myBean1_" dans l’exemple ci-dessous) et que l’on cherche à initier le modèle à partir des données en session _@SessionAttributes("myBean1")_, Spring MVC lève une _HttpSessionRequiredException_ :

```sh
org.springframework.web.HttpSessionRequiredException: Expected session attribute 'myBean1'
	at org.springframework.web.method.annotation.ModelFactory.initModel(ModelFactory.java:103)
	at org.springframework.web.servlet.mvc.method.annotation.RequestMappingHandlerAdapter.invokeHandleMethod(RequestMappingHandlerAdapter.java:726)
```

## Démonstration

Les explications données dans ce blog s’appuient sur des tests réalisés dans la [branche SessionAttributes](https://github.com/arey/spring-mvc-toolkit/tree/SessionAttributes) du projet [spring-mvc-toolkit](https://github.com/arey/spring-mvc-toolkit). Reprenant l’idée présentée dans le billet [Understanding Spring MVC Model and SessionAttributes](http://www.intertech.com/Blog/understanding-spring-mvc-model-and-session-attributes/), les 2 contrôleurs [_MyController_](https://github.com/arey/spring-mvc-toolkit/blob/SessionAttributes/spring-mvc-toolkit-demo/src/main/java/com/javaetmoi/core/mvc/demo/controller/MyController.java) et [_OtherController_](https://github.com/arey/spring-mvc-toolkit/blob/SessionAttributes/spring-mvc-toolkit-demo/src/main/java/com/javaetmoi/core/mvc/demo/controller/OtherController.java) tracent l’appel de méthodes et affichent le contenu du modèle, de la requête et de la session. La page [_sessionsattributepage.jsp_](https://github.com/arey/spring-mvc-toolkit/blob/SessionAttributes/spring-mvc-toolkit-demo/src/main/webapp/WEB-INF/pages/sessionsattributepage.jsp) affiche quant à elle le contenu de la requête et de la session.

Extrait de la classe [_MyController_](https://github.com/arey/spring-mvc-toolkit/blob/SessionAttributes/spring-mvc-toolkit-demo/src/main/java/com/javaetmoi/core/mvc/demo/controller/MyController.java):

```java
Extrait de la classe MyController.java
```

Extrait de la classe [_OtherController_](https://github.com/arey/spring-mvc-toolkit/blob/SessionAttributes/spring-mvc-toolkit-demo/src/main/java/com/javaetmoi/core/mvc/demo/controller/OtherController.java):

```java
Extrait de la classe OtherController.java
```

Voici les étapes à suivre pour exécuter l’application démo. Les prérequis sont d’avoir installé sur son post Git, Java 6 ou + et maven 3 ou + :

1. git clone git://github.com/arey/spring-mvc-toolkit.git
1. git checkout SessionAttributes
1. mvn clean install
1. cd spring-mvc-toolkit-demo
1. mvn jetty:run-war
1. Naviguer sur [http://localhost:8080/dosomething](http://localhost:8080/dosomething)

Nous allons décrire à présent les traces affichées et le contenu des pages observé lors de la navigation sur les liens.

### Appel à dosomething

Traces observées lors de l’appel à [http://localhost:8080/dosomething](http://localhost:8080/dosomething) :

```default
Inside of addMyBean1ToSessionScope
Inside of addMyBean2ToRequestScope
Inside of addMyOtherBeanAToSessionScope
Inside of addMyOtherBeanBToSessionScope
Inside of dosomething handler method
--- Model data ---
myBean1 -- MyBean [name=My Bean 1]
myBean2 -- MyBean [name=My Bean 2]
myOtherBeanA -- MyOtherBean [name=My Other Bean A]
myOtherBeanB -- MyOtherBean [name=My Other Bean B]
=== Request data ===
*** Session data ***
```

Page affichée dans le navigateur :

[![2014-09-spring-mvc-sessionattributes-screenshot1](wp-content/uploads/2014/10/2014-09-spring-mvc-sessionattributes-screenshot1.jpg)](wp-content/uploads/2014/10/2014-09-spring-mvc-sessionattributes-screenshot1.jpg) Analyse :

- Les 4 méthodes annotées par _@ModelAttribute_ sont appelées avant la méthode _@RequestMapping_.
- Les beans créés par chacune de ces méthodes sont disponibles dans le modèle dès l’appel à la méthode _@RequestMapping_.
- Lors de l’appel à la méthode _@RequestMapping_, la requête et la session HTTP ne contiennent encore aucun attribut.
- Lors du rendu de la page, les 4 beans sont présents au niveau de la requête. Par contre, seul les 3 beans référencés par _l’annotation @SessionAttributes( value="myBean1", types={MyOtherBean.class} )_ sont présents en session.

### Premier appel à other

Traces observées lors du clic sur le lien "/other" :

```default
Inside of addMyBean3ToSessionScope
Inside of other handler method
MyBean [name=My Bean 1]
--- Model data ---
myBean3 -- MyBean [name=My Bean 3]
myBean1 -- MyBean [name=My Bean 1]
=== Request data ===
*** Session data ***
myOtherBeanA -- MyOtherBean [name=My Other Bean A]
myOtherBeanB -- MyOtherBean [name=My Other Bean B]
myBean1 -- MyBean [name=My Bean 1]
```

Page affichée dans le navigateur :

[![2014-09-spring-mvc-sessionattributes-screenshot2](wp-content/uploads/2014/10/2014-09-spring-mvc-sessionattributes-screenshot2.jpg)](wp-content/uploads/2014/10/2014-09-spring-mvc-sessionattributes-screenshot2.jpg) Analyse :

- Lors de l’appel à la méthode _@RequestMapping_:

  - les 2 beans référencés par l’annotation @SessionAttributes({"myBean1", "myBean3"}) sont disponibles dans le modèle,
  - les beans _myOtherBeanA_ et _myOtherBeanB_ sont présents en session mais pas recopiées dans le modèle
- Lors du rendu de la page JSP : Le bean _myBean3_ créé par le contrôleur est ajouté à la session qui compte désormais 4 beans

### Appel à endsession

Trace observée lors du clic sur le lien "/endession" :

```default
Inside of addMyBean2ToRequestScope
--- Model data ---
myOtherBeanA -- MyOtherBean [name=My Other Bean A]
myOtherBeanB -- MyOtherBean [name=My Other Bean B]
myBean1 -- MyBean [name=My Bean 1]
myBean2 -- MyBean [name=My Bean 2]
=== Request data ===
*** Session data ***
myOtherBeanA -- MyOtherBean [name=My Other Bean A]
myOtherBeanB -- MyOtherBean [name=My Other Bean B]
myBean1 -- MyBean [name=My Bean 1]
myBean3 -- MyBean [name=My Bean 3]
```

Page affichée dans le navigateur :

[![2014-09-spring-mvc-sessionattributes-screenshot3](wp-content/uploads/2014/10/2014-09-spring-mvc-sessionattributes-screenshot3.jpg)](wp-content/uploads/2014/10/2014-09-spring-mvc-sessionattributes-screenshot3.jpg) Analyse :

- L’URL /endession est mappée sur le contrôleur _MyController_ déjà utilisé lors du 1er accès à l’URL /dosomething
- Seule l’une des 4 méthodes annotées avec _@ModelAttribute_ est appelée : _addMyBean2ToRequestScope_. Les 3 autres méthodes ne sont pas appelées car les beans qu’elles créent sont déjà présent en session.
- L’appel à la méthode _setComplete();_ ne retire pas instantanément les beans de la session mais joue le rôle de marqueur.
- Les beans référencés par _MyController_ sont supprimés de la session avant le rendu de la page JSP. Bien que supprimés de la session, ils sont disponibles dans le scope request.

### Second appel à other

 [![2014-09-spring-mvc-sessionattributes-screenshot4](wp-content/uploads/2014/10/2014-09-spring-mvc-sessionattributes-screenshot4.jpg)](wp-content/uploads/2014/10/2014-09-spring-mvc-sessionattributes-screenshot4.jpg)

Injecté dans le handler, le bean myBean1 n'est plus disponible en session.
public String otherHandlingMethod(Model model, HttpServletRequest request, HttpSession session, @ModelAttribute("myBean1") MyBean myBean) {

## Tests unitaires

La mise au point de tests unitaires ou de tests d’intégration mettant en jeu ou plusieurs contrôleurs annotés avec _@SessionAttributes_ nécessite un travail supplémentaire.
En effet, lorsque le handler d’un contrôleur s’appuie sur une donnée qui devrait être présente en session, il est nécessaire d’utiliser la méthode **_sessionAttr_** pour passer au contrôleur la donnée attendue.
Par ailleurs, entre 2 appels de handler, Spring Test ne conserve pas les données sauvegardées en session. Lors du 2ième appel, il est donc sorte nécessaire de réinjecter la donnée créée lors du premier appel. La classe [**_MvcResult_**](https://github.com/spring-projects/spring-framework/blob/v4.1.1.RELEASE/spring-test/src/main/java/org/springframework/test/web/servlet/MvcResult.java) permet d’accéder au résultat du 1er appel.
Le test unitaire [_SessionAttributesTest_](https://github.com/arey/spring-mvc-toolkit/blob/SessionAttributes/spring-mvc-toolkit-demo/src/test/java/com/javaetmoi/core/mvc/demo/controller/SessionAttributesTest.java) monte un exemple d’utilisation :

```java
Extrait de la classe SessionAttributesTest.java
```

## Conclusion

Introduite depuis Spring 2.5, l’ **annotation _@SessionAttributes_** n’a pas d’équivalent dans d’autres frameworks MVC. Je pense par exemple à Struts. Son utilisation demande de comprendre son fonctionnement et la « magie » qu’on peut lui prêter. J’espère que cet article vous aura permis de démystifier ces mécanismes. La prochaine fois que vous l’utiliserez, je vous invite à vous référer au diagramme présenté au milieu de ce billet. N’hésitez pas non plus à cloner le projet [spring-mvc-toolkit](https://github.com/arey/spring-mvc-toolkit) et à jouer avec la branche _SessionAttributes_.

Références :

1. [Manuel de référence du framework Spring MVC](http://docs.spring.io/spring/docs/current/spring-framework-reference/htmlsingle/#mvc)
1. [Understanding Spring MVC Model and SessionAttributes](http://www.intertech.com/Blog/understanding-spring-mvc-model-and-session-attributes/)
1. [Projet Spring Session](https://github.com/spring-projects/spring-session)
1. [Power of Spring's @ModelAttribute and @SessionAttributes](http://vmustafayev4en.blogspot.fr/2012/10/power-of-springs-modelattribute-and.html)
1. [Spring MVC - Session Attributes handling](http://vard-lokkur.blogspot.fr/2011/01/spring-mvc-session-attributes-handling.html)
