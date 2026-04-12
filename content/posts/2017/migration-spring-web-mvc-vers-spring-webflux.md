---
_edit_last: "1"
_thumbnail_id: "1795"
_wp_old_slug: migration-spring-mvc-vers-spring-webflux
_xmlsf_image_featured:
  caption: ""
  loc: https://javaetmoi.com/wp-content/uploads/2017/12/spring-webflux.png
  title: spring-webflux
author: admin
categories:
  - spring
featureImage: /wp-content/uploads/2017/12/spring-webflux.png
featureImageAlt: spring-webflux
date: "2017-12-07T17:26:12+00:00"
thumbnail: /wp-content/uploads/2017/12/spring-webflux.png
guid: http://javaetmoi.com/?p=1794
parent_post_id: null
post_id: "1794"
post_views_count: "11049"
summary: |-
  [![](http://javaetmoi.com/wp-content/uploads/2017/12/spring-webflux.png)](http://javaetmoi.com/wp-content/uploads/2017/12/spring-webflux.png)[**Spring WebFlux**](https://docs.spring.io/spring-framework/docs/5.0.1.RELEASE/spring-framework-reference/web-reactive.html#spring-webflux) est une **fonctionnalit** **é majeure** de **Spring Framework 5**. Disposant de son propre module Maven (spring-weblux), ce **nouveau framework web** se positionne comme une **alternative** **à Spring Web MVC.** Ce dernier a été conçu par-dessus l’API Servlet. Spring WebFlux l’a été pour les **applications r** **éactives**, avec I/O non bloquantes, asynchrones, **à faible latence**, basées sur des serveurs comme Netty, Undertow ou compatibles Servlets 3.1 et +.
  Spring WebFlux s’éloigne du modèle d’un thread par requête HTTP et se base désormais sur le projet [**Reactor**](https://projectreactor.io/) pour orchestrer le traitement des requêtes.
  Conçu avant tout pour exposer des **API REST** attaquant des bases NoSQL non bloquantes dans des architecture micro-services, Spring WebFlux peut être utilisé sur des applications web dont les **IHM** sont rendues côté serveur (ex : avec Thymeleaf ou Freemarker).

  J’ai récemment migré vers Spring WebFlux la [version Kotlin et Spring Boot de l’application démo Spring Petclinic](http://github.com/spring-petclinic/spring-petclinic-kotlin). Dans ce court billet, je voulais vous lister les adaptations mises en œuvre dans le [commit 279b2e7](https://github.com/spring-petclinic/spring-petclinic-kotlin/commit/279b2e7c58906d9a765e7229043c7d563f016b1c).

  ![spring-webflux](/wp-content/uploads/2017/12/spring-webflux.png)
tags:
  - spring-mvc
  - spring-webflux
title: Migration Spring MVC vers Spring WebFlux
url: /2017/12/migration-spring-web-mvc-vers-spring-webflux/

---
[![](/wp-content/uploads/2017/12/spring-webflux.png)](/wp-content/uploads/2017/12/spring-webflux.png)[**Spring WebFlux**](https://docs.spring.io/spring-framework/docs/5.0.1.RELEASE/spring-framework-reference/web-reactive.html#spring-webflux) est une **fonctionnalit** **é majeure** de **Spring Framework 5**. Disposant de son propre module Maven (spring-weblux), ce **nouveau framework web** se positionne comme une **alternative** **à Spring Web MVC.** Ce dernier a été conçu par-dessus l’API Servlet. Spring WebFlux l’a été pour les **applications r** **éactives**, avec I/O non bloquantes, asynchrones, **à faible latence**, basées sur des serveurs comme Netty, Undertow ou compatibles Servlets 3.1 et +.
Spring WebFlux s’éloigne du modèle d’un thread par requête HTTP et se base désormais sur le projet [**Reactor**](https://projectreactor.io/) pour orchestrer le traitement des requêtes.
Conçu avant tout pour exposer des **API REST** attaquant des bases NoSQL non bloquantes dans des architecture micro-services, Spring WebFlux peut être utilisé sur des applications web dont les **IHM** sont rendues côté serveur (ex : avec Thymeleaf ou Freemarker).

J’ai récemment migré vers Spring WebFlux la [version Kotlin et Spring Boot de l’application démo Spring Petclinic](http://github.com/spring-petclinic/spring-petclinic-kotlin). Dans ce court billet, je voulais vous lister les adaptations mises en œuvre dans le [commit 279b2e7](https://github.com/spring-petclinic/spring-petclinic-kotlin/commit/279b2e7c58906d9a765e7229043c7d563f016b1c).

## Changement de dépendances

Le **build Gradle** a été modifié en 2 points :

1. Le starter Spring Boot spring-boot-starter-web est remplacé par **spring-boot-starter-webflux**
1. La dépendance vers **Expression Language** (org.glassfish:javax.el) a été ajoutée pour les **tests** qui requièrent le support Bean Validation offert par Spring (classe LocalValidatorFactoryBean).

Après résolution des dépendances, le changement le plus notable est que le JAR **spring-webmvc a été remplacé par spring-weblux**.
Spring Web MVC s’appuie sur l’API Servlet. Pour preuve, toutes les classes de ce module appartiennent au package _org.springframework.web.servlet_. On y retrouvait par exemples les classes **DispatcherServlet** et ModelAndView. Spring WebFlux ne les utilise plus.

## Une migration quasi-transparente

Spring WebFlux réutilisent les classes et annotations bien connues des développeurs Spring MVC : `@Controller`, `@RequestMapping`, @ModelAttribute, Model ou bien encore @InitBinder.
La migration vers Spring WebFlux du code de production est donc relativement simple.

Les contrôleurs doivent être ajustés afin de ne plus utiliser les classes du module spring-webmvc. Ces changements sont identifiés dès la phase de compilation.
Dans l’exemple ci-dessous, la classe `ModelAndView` a été remplacée par la classe `Model`:

Utilisation de ModelAndView avec Spring Web MVC :

```java
@GetMapping("/owners/{ownerId}")
 fun showOwner(@PathVariable("ownerId") ownerId: Int): ModelAndView {
    val mav = ModelAndView("owners/ownerDetails")
    mav.addObject(this.owners.findById(ownerId))
    return mav
}

```

Code migré vers Spring WebFlux en utilisant la classe Model :

```java
@GetMapping("/owners/{ownerId}")
fun showOwner(@PathVariable("ownerId") ownerId: Int, model: Model): String {
    model.addAttribute(this.owners.findById(ownerId))
    return "owners/ownerDetails"
}
```

Au cours de la migration, des incompatibilités ont été détectées au runtime et lors de l’exécution des tests unitaires.
Ce fut notamment le cas de la classe `ModelMap` qui provoquait une erreur lors de la résolution des paramètres :

_java.lang.IllegalStateException: Failed to invoke handler method with resolved arguments: \[0\]\[type=java.lang.Integer\]\[value=1\],\[1\]\[type=org.springframework.validation.support.BindingAwareConcurrentModel\]\[value={owner=org.springframework.samples.petclinic.owner.Owner@373c0f9b, types=\[bird, cat, dog, hamster, lizard, snake\]}\] on public java.lang.String org.springframework.samples.petclinic.owner.PetController.initUpdateForm(int,org.springframework.ui.ModelMap)_ _at org.springframework.web.reactive.result.method.InvocableHandlerMethod.lambda$invoke$0(InvocableHandlerMethod.java:160) ~\[spring-webflux-5.0.1.RELEASE.jar:5.0.1.RELEASE\]_ _at reactor.core.publisher.MonoFlatMap$FlatMapMain.onNext(MonoFlatMap.java:118) \[reactor-core-3.1.1.RELEASE.jar:3.1.1.RELEASE\]_

Pour corriger ce problème, la classe `ModelMap` a été remplacée par `Model` dans les handlers de requêtes.

Utilisation de ModelMap avec Spring Web MVC :

```java
@GetMapping(value = "/pets/{petId}/edit")
 fun initUpdateForm(@PathVariable petId: Int, model: ModelMap): String {
     val pet = pets.findById(petId)
    model.put("pet", pet)
     return VIEWS_PETS_CREATE_OR_UPDATE_FORM
}

```

Remplacée par la classe Model avec Spring WebFlux :

```java
@GetMapping(value = "/pets/{petId}/edit")
fun initUpdateForm(@PathVariable petId: Int, model: Model): String {
    val pet = pets.findById(petId)
    model.addAttribute("pet", pet)
    return VIEWS_PETS_CREATE_OR_UPDATE_FORM
}
```

## Refactoring des tests unitaires

La migration a demandé davantage d’effort pour les tests unitaires de la couche web. Il a en effet été nécessaire de complètement les refactorer.

Spring WebFlux ne permet plus de tester en boîte blanche les contrôleurs. **La classe MockMvc n’existe plus**. Et il est désormais impossible de vérifier l’état du model ou le nom de la vue rendue par le contrôleur.

Pour tester les contrôleurs, Spring WebFlux propose d’utiliser la classe `WebTestClient`, le pendant de la classe [WebClient](http://www.baeldung.com/spring-5-webclient) pour les tests. WebTestClient a été pensé avant tout pour tester les retours au format JSON. Tester du HTML est moins simple. Il est nécessaire d’évaluer les templates Thymeleaf, ce qui présente néanmoins l’avantage de les tester. Lorsque l’on souhaite effectuer des assertions XPath, il est nécessaire de normaliser le HTML au format XHTML (fermer les balises).

Si l’on prend exemple sur la classe de test [OwnerControllerTest](https://github.com/spring-petclinic/spring-petclinic-kotlin/blob/d52b733dc1eabded1677622879a380b6a7b2ab3d/src/test/kotlin/org/springframework/samples/petclinic/owner/OwnerControllerTest.kt), son en-tête a dû être modifiée en 3 points :

1. L’annotation @WebMvcTest est remplacée par `@WebFluxTest`
1. La classe de configuration `ThymeleafAutoConfiguration` a été ajoutée
1. Injecté, le bean `WebTestClient` remplace MockMvc

En-tête d’une classe de test d’un contrôleur Spring Web MVC :

```java
@RunWith(SpringRunner::class)
 @WebMvcTest(OwnerController::class)
 class OwnerControllerTest {

    @Autowired
    lateinit private var mockMvc: MockMvc

```

En-tête d’une classe de test migrée à Spring WebFlux :

```java
@RunWith(SpringRunner::class)
@WebFluxTest(OwnerController::class)
@Import(ThymeleafAutoConfiguration::class)
class OwnerControllerTest {

      @Autowired
    lateinit private var client: WebTestClient;

```

Attardons-nous à présent sur l’une des méthodes de test. Par exemple, celle qui teste la soumission d’un formulaire invalide.
Avec Spring Web MVC, les assertions s’appuient sur les méthodes `attributeHasErrors` et `attributeHasFieldErrors` de l’objet renvoyait par la méthode model() :

```java
@Test
fun testProcessCreationFormHasErrors() {
    mockMvc.perform(post("/owners/new")
        .param("firstName", "Joe")
        .param("lastName", "Bloggs")
        .param("city", "London")
    )
        .andExpect(status().isOk)
    .andExpect(model().attributeHasErrors("owner"))
    .andExpect(model().attributeHasFieldErrors("owner", "address"))
    .andExpect(model().attributeHasFieldErrors("owner", "telephone"))
    .andExpect(view().name("owners/createOrUpdateOwnerForm"))
}
```

Avec Spring WebFlux, on **analyse le contenu du HTML généré**. Les assertions sont ici moins précises car les messages d’erreur ne sont pas reliés au champs de saisie :

```java
@Test
fun testProcessCreationFormHasErrors() {
    val formData = LinkedMultiValueMap<String, String>(3)
    formData.put("firstName", Arrays.asList("Joe"))
    formData.put("lastName", Arrays.asList("Bloggs"))
    formData.put("city", Arrays.asList("London"))
    val res = client.post().uri("/owners/new")
            .header("Accept-Language", "en-US")
            .body(BodyInserters.fromFormData(formData))
            .exchange()
            .expectStatus().isOk
            .expectBody(String::class.java).returnResult()

    Assertions.assertThat(res.responseBody).contains("numeric value out of bounds (&lt;10 digits&gt;.&lt;0 digits&gt; expected")
    Assertions.assertThat(res.responseBody).contains("must not be empty")
}
```

Lors de la migration du test [CrashControllerTest](https://github.com/spring-petclinic/spring-petclinic-kotlin/blob/d52b733dc1eabded1677622879a380b6a7b2ab3d/src/test/kotlin/org/springframework/samples/petclinic/system/CrashControllerTest.kt) chargé de vérifier que la levée d’une exception technique renvoie sur une page d’erreur générique, après avoir importé la classe de configuration **ErrorWebFluxAutoConfiguration**, le **template error.html** n’était pas retrouvé. Un palliatif (temporaire ?) a été de le **renommer en 5xx.html**.

## Démarrage

Une fois que le code compile et que les TU sont au vert, il reste à démarrer l’application.
Dans les logs, on note un changement d’importance :

```default
Netty started on port(s): 8080
```

Ce n’est plus Jetty, mais Netty qui apparaît dans les logs de démarrage. Netty étant le serveur par défaut choisi par Pivotal dans Spring Boot pour faire exécuter les applications Spring WebFlux.

## Pour aller plus loin

Lorsqu’une application reactive utilise Spring WebFlux, 2 modèles de programmation sont proposés pour configurer la couche web :

1. Utiliser les **annotations de Spring MVC**. Choix qui a été fait pour [spring-petclinic-kotlin](https://github.com/spring-petclinic/spring-petclinic-kotlin/) car le plus transparent lors d’une migration.
1. Utiliser la programmation fonctionnelle via les [**Functional Endpoints**](https://docs.spring.io/spring-framework/docs/5.0.1.RELEASE/spring-framework-reference/web-reactive.html#webflux-fn) pour déclarer les routes et les handlers de requêtes HTTP. Spring Framework 5 vient avec une nouvelle fonctionnalité : le [Kotlin routing DSL](https://docs.spring.io/spring-framework/docs/5.0.0.RELEASE/spring-framework-reference/kotlin.html#webflux-functional-dsl). L’utilisation de ce DSL pourrait avoir du sens sur [spring-petclinic-kotlin](https://github.com/spring-petclinic/spring-petclinic-kotlin/), au moins pour la partie REST. Peut-être la prochaine évolution ?

## Post-scriptum

Comme précisé par Sébastien Deleuze dans la [Pull Request #9](https://github.com/spring-petclinic/spring-petclinic-kotlin/pull/9), utiliser Spring WebFlux avec JPA peut entrainer des problèmes de scalabilité. En effet, JPA est une API bloquante. Un rollback vers Spring MVC a été réalisé.
Une migration complète vers WebFlux passerait donc par une migration vers une base NoSQL supportant les appels non bloquants. L'UI devrait également être retravaillée pour profiter du streaming des données. Fonctionnellement, Petclinic n'en a pas réellement besoin et ne se prête donc pas bien au use case d'utilisation de WebFlux.

 Références :

- [Spring WebFlux](https://docs.spring.io/spring-framework/docs/5.0.1.RELEASE/spring-framework-reference/web-reactive.html#spring-webflux) (manuel de référence de Spring Framework)
- [Projet Reactor](https://projectreactor.io/) (site web oficiel)
- [Commit GitHub](https://github.com/spring-petclinic/spring-petclinic-kotlin/commit/dc1eabded1677622879a380b6a7b2ab3d) montrant les différences entre l’utilisation de Spring MVC et Spring WebFlux
- [Spring 5 WebClient](http://www.baeldung.com/spring-5-webclient) (Baeldung blog)
- [WebFlux Fonctionnal DSL](https://docs.spring.io/spring-framework/docs/5.0.0.RELEASE/spring-framework-reference/kotlin.html#webflux-functional-dsl) (manuel de référence de Spring Framework)
