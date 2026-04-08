---
author: admin
categories:
  - retour-d'expérience
  - spring
date: "2019-11-28T08:37:31+00:00"
thumbnail: /wp-content/uploads/2019/11/spring-cloud-netflix.png
featureImage: /wp-content/uploads/2019/11/spring-cloud-netflix.png
guid: https://javaetmoi.com/?p=2045
parent_post_id: null
post_id: "2045"
post_views_count: "22746"
summary: |-
  [![](https://javaetmoi.com/wp-content/uploads/2019/11/spring-cloud-netflix.png)](https://javaetmoi.com/wp-content/uploads/2019/11/spring-cloud-netflix.png)Le projet  [Spring Cloud Netflix](https://spring.io/projects/spring-cloud-netflix) facilite l’intégration de différents projets de la suite [Netflix OSS](https://netflix.github.io/) dans des applications Spring Boot / Spring Cloud : Eureka, Zuul 1, Ribbon, Hystrix, Archaius, Feign. Jusqu’en 2018, le projet [Spring Petclinic Microservices](https://github.com/spring-petclinic/spring-petclinic-microservices) dont j’assure la maintenance utilisait ces 4 premiers projets.

  Or, certains des projets historiques de Netflix OSS ne sont plus activement développés. Ils sont rentrés en mode maintenance. C’est notamment le cas d’ [Hystrix](https://github.com/Netflix/Hystrix#hystrix-status), de Zuul 1 et de Ribbon. En décembre 2018, lors de l’annonce de la [sortie de Spring Cloud Greenwich RC1](https://spring.io/blog/2018/12/12/spring-cloud-greenwich-rc1-available-now), Pivotal recommande de migrer vers des projets tiers et de nouveaux modules Spring Cloud :

  **Anciennement****Solutions cibles** Hystrix [Resilience4j](https://github.com/resilience4j/resilience4j)Hystrix Dashboard / Turbine [Micrometer](https://micrometer.io/) \+ Monitoring System  Ribbon [Spring Cloud Loadbalancer](https://cloud.spring.io/spring-cloud-static/spring-cloud-commons/2.2.0.RC2/reference/html/#spring-cloud-loadbalancer) Zuul 1 [Spring Cloud Gateway](https://cloud.spring.io/spring-cloud-static/spring-cloud-gateway/2.2.0.RC2/reference/html/) Archaius 1 Spring Boot external config + Spring Cloud Config

  Dans le cadre de Spring Petclinic Microservices, seul Eureka est épargné et continue de jouer son rôle d’annuaire de service. Un désendettement vers **Resilience4j**, **Micrometer**, **Spring Cloud Loadbalancer** et **Spring Cloud Gateway** s’est naturellement imposé (issue [#117](https://github.com/spring-petclinic/spring-petclinic-microservices/issues/117)).

  Cet article retrace les différentes étapes de
  migration. J’espère qu’il vous sera utile si vous avez le même chemin à
  parcourir.

  ![Désendettement de Spring Cloud Netflix](/wp-content/uploads/2019/11/spring-cloud-netflix.png)
tags:
  - hystrix
  - resilience4j
  - ribbon
  - spring-cloud
  - zuul
title: Désendettement de Spring Cloud Netflix
url: /2019/11/desendettement-de-spring-cloud-netflix/

---
[![](/wp-content/uploads/2019/11/spring-cloud-netflix.png)](/wp-content/uploads/2019/11/spring-cloud-netflix.png)Le projet  [Spring Cloud Netflix](https://spring.io/projects/spring-cloud-netflix) facilite l’intégration de différents projets de la suite [Netflix OSS](https://netflix.github.io/) dans des applications Spring Boot / Spring Cloud : Eureka, Zuul 1, Ribbon, Hystrix, Archaius, Feign. Jusqu’en 2018, le projet [Spring Petclinic Microservices](https://github.com/spring-petclinic/spring-petclinic-microservices) dont j’assure la maintenance utilisait ces 4 premiers projets.

Or, certains des projets historiques de Netflix OSS ne sont plus activement développés. Ils sont rentrés en mode maintenance. C’est notamment le cas d’ [Hystrix](https://github.com/Netflix/Hystrix#hystrix-status), de Zuul 1 et de Ribbon. En décembre 2018, lors de l’annonce de la [sortie de Spring Cloud Greenwich RC1](https://spring.io/blog/2018/12/12/spring-cloud-greenwich-rc1-available-now), Pivotal recommande de migrer vers des projets tiers et de nouveaux modules Spring Cloud :

**Anciennement****Solutions cibles** Hystrix [Resilience4j](https://github.com/resilience4j/resilience4j)Hystrix Dashboard / Turbine [Micrometer](https://micrometer.io/) \+ Monitoring System  Ribbon [Spring Cloud Loadbalancer](https://cloud.spring.io/spring-cloud-static/spring-cloud-commons/2.2.0.RC2/reference/html/#spring-cloud-loadbalancer) Zuul 1 [Spring Cloud Gateway](https://cloud.spring.io/spring-cloud-static/spring-cloud-gateway/2.2.0.RC2/reference/html/) Archaius 1 Spring Boot external config + Spring Cloud Config

Dans le cadre de Spring Petclinic Microservices, seul Eureka est épargné et continue de jouer son rôle d’annuaire de service. Un désendettement vers **Resilience4j**, **Micrometer**, **Spring Cloud Loadbalancer** et **Spring Cloud Gateway** s’est naturellement imposé (issue [#117](https://github.com/spring-petclinic/spring-petclinic-microservices/issues/117)).

Cet article retrace les différentes étapes de
migration. J’espère qu’il vous sera utile si vous avez le même chemin à
parcourir.

## Zuul 1 vers Spring Cloud Gateway

Comme le souligne l’article [Rate\
Limiting In Spring Cloud Gateway With Redis](https://piotrminkowski.wordpress.com/2019/11/15/rate-limiting-in-spring-cloud-gateway-with-redis/), avec
2028 étoiles (au 22/11/2019), **Spring**
**Cloud Gateway** est le 2ième projet le plus populaire de la galaxy [Spring Cloud](https://github.com/spring-cloud) derrière
Spring Cloud Netflix. Il a été conçu pour succéder au proxy Zuul et fait office
d’API Gateway pour les architectures microservices. Bâti autour d’une
architecture réactive, [Spring\
Cloud Gateway requière l’utilisation de Spring WebFlux, de Netty et du projet\
Reactor](https://cloud.spring.io/spring-cloud-static/spring-cloud-gateway/2.2.0.RC2/reference/html/).

La migration de Spring Petclinic Microservices
de Zuul 1 vers [Spring Cloud Gateway](https://spring.io/projects/spring-cloud-gateway) s’est
concrétisée par la [Pull\
Request #125](https://github.com/spring-petclinic/spring-petclinic-microservices/pull/125).

1. Dans le pom.xml du module spring-petclinic-api-gateway, la
   première étape a consisté à changer de starter : de spring-cloud-starter-netflix-zuul
   vers **spring-cloud-starter-gateway**

- La seconde étape a nécessité de migrer de Spring Web vers **Spring Webflux**. Étape extrêmement simple puisqu’elle consiste à supprimer le starter _spring-boot-starter-web_ du _pom.xml_. La dépendance vers Spring Webflux est tirée transitivement par _spring-cloud-starter-gateway_
- L’annotation **@EnableZuulProxy** a été **retirée** de la classe principale
- Suite à la migration vers Spring Webflux, la page d’accueil _/static/index.html_ n’était plus mappée vers /   
 Une solution de contournement a nécessité de déclarer un Router. Se référer à l’ [issue Spring Boot #9785](https://github.com/spring-projects/spring-boot/issues/9785)
- Enfin, les **règles** **de** **routage Zuul** déclarées dans le fichier application.yml ont dû être **transposées** vers Spring Cloud Gateway

Configuration de depart Zuul :

```yaml
zuul:
  prefix: /api
  ignoredServices: '*'
  routes:
    vets-service: /vet/**
    visits-service: /visit/**
    customers-service: /customer/**
    api-gateway: /gateway/**
```

Configuration Spring Cloud Gateway :

```yaml
spring:
  cloud:
    gateway:
      routes:
        - id: vets-service
          uri: lb://vets-service
          predicates:
            - Path=/api/vet/**
          filters:
            - StripPrefix=2
        - id: visits-service
          uri: lb://visits-service
          predicates:
            - Path=/api/visit/**
          filters:
            - StripPrefix=2
        - id: customers-service
          uri: lb://customers-service
          predicates:
            - Path=/api/customer/**
          filters:
            - StripPrefix=2
```

Le filtre **SripPrefix** accepte pour paramètre le nombre de parties du chemin à retirer de la requête HTTP avant d’être redirigée vers le microservice cible.  
Exemple : lorsqu’une requête arrive sur la gateway avec l’URL [http://localhost::8080/api/customer/owners](http://localhost::8080/api/customer/owners), la requête _/owners_ est transmise au microservice _customers-service_ (sans le /api/customer).

A noter que la route _/api/gateway_ servie par le contrôleur Rest [ApiGatewayController](https://github.com/spring-petclinic/spring-petclinic-microservices/blob/master/spring-petclinic-api-gateway/src/main/java/org/springframework/samples/petclinic/api/boundary/web/ApiGatewayController.java) n’a plus besoin d’être déclarée.

## Ribbon vers Spring Cloud Reactive LoadBalancer

**[Spring Cloud LoadBalancer](https://cloud.spring.io/spring-cloud-static/spring-cloud-commons/2.2.0.RC2/reference/html/#spring-cloud-loadbalancer)** a été [incubé](https://github.com/spring-cloud-incubator/spring-cloud-loadbalancer) avant d'avoir été intégré au projet **Spring Cloud Commons**. Il abstrait l’utilisation d’un répartiteur de charge (load-balancer) côté client et fonctionne avec Spring RestTemplate, Spring WebClient et Spring WebFlux WebCient. Sous le capot, Spring Cloud LoadBalancer s’appuie sur Ribbon lorsque ce dernier est détecté dans le classpath et n’est pas désactivé. Dans le cas contraire, il **dispose de sa propre implémentation de répartiteur de charge**.

Lors de la montée de version vers **Spring Cloud Hoxton**, un **avertissement**
au **démarrage** de l’application **invite à ne plus utiliser** **Ribbon** pour orchestrer la répartition
des appels, car Spring Cloud Ribbon est désormais en mode maintenance :

``2019-11-13 18:32:41.670  WARN [api-gateway,,,] 79015 --- [  restartedMain] BockingLoadBalancerClientRibbonWarnLogger : You already have RibbonLoadBalancerClient on your classpath. It will be used by default. As Spring Cloud Ribbon is in maintenance mode. We recommend switching to BlockingLoadBalancerClient instead. In order to use it, set the value of `spring.cloud.loadbalancer.ribbon.enabled` to `false` or remove spring-cloud-starter-netflix-ribbon from your project.``

L’utilisation du répartiteur de charge natif à Spring
Cloud LoadBalancer a demandé l’ **exclusion** de plusieurs **dépendances**
liées à **Ribbon** :

- spring-cloud-starter-netflix-ribbon
- spring-cloud-netflix-ribbon
- ribbon-eureka

```xml
<dependency>
     <groupId>org.springframework.cloud</groupId>
     <artifactId>spring-cloud-starter-netflix-eureka-client</artifactId>
     <exclusions>
         <exclusion>
             <groupId>org.springframework.cloud</groupId>
             <artifactId>spring-cloud-starter-netflix-ribbon</artifactId>
         </exclusion>
         <exclusion>
             <groupId>org.springframework.cloud</groupId>
             <artifactId>spring-cloud-netflix-ribbon</artifactId>
         </exclusion>
         <exclusion>
             <groupId>com.netflix.ribbon</groupId>
             <artifactId>ribbon-eureka</artifactId>
         </exclusion>
     </exclusions>
 </dependency>
```

```xml
<dependency>
    <groupId>org.springframework.cloud</groupId>
    <artifactId>spring-cloud-starter-netflix-hystrix</artifactId>
    <exclusions>
        <exclusion>
            <groupId>org.springframework.cloud</groupId>
            <artifactId>spring-cloud-netflix-ribbon</artifactId>
        </exclusion>
    </exclusions>
</dependency>
```

L’ajout du starter **spring-cloud-starter-loadbalancer** n’a pas été nécessaire car ce dernier est tiré transitivement par le starter spring-cloud-starter-netflix-eureka-client.

Dans mon cas, l’utilisation du BlockingLoadBalancerClient n’était
pas possible car Spring Cloud Gateway nécessite d’utiliser
des APIs non bloquantes. Preuve
en stacktrace :

```text
java.lang.IllegalStateException: block()/blockFirst()/blockLast() are blocking, which is not supported in thread reactor-http-nio-2
	|_ checkpoint ⇢ HTTP GET "/api/gateway/owners/6"[ExceptionHandlingWebHandler]
Stack trace:
		at reactor.core.publisher.BlockingSingleSubscriber.blockingGet(BlockingSingleSubscriber.java:77)
		at reactor.core.publisher.Mono.block(Mono.java:1663)
		at org.springframework.cloud.loadbalancer.blocking.client.BlockingLoadBalancerClient.choose(BlockingLoadBalancerClient.java:86)
		at org.springframework.cloud.loadbalancer.blocking.client.BlockingLoadBalancerClient.execute(BlockingLoadBalancerClient.java:51)
		at org.springframework.cloud.client.loadbalancer.LoadBalancerInterceptor.intercept(LoadBalancerInterceptor.java:58)
		at org.springframework.http.client.InterceptingClientHttpRequest$InterceptingRequestExecution.execute(InterceptingClientHttpRequest.java:93)
		at brave.spring.web.TracingClientHttpRequestInterceptor.intercept(TracingClientHttpRequestInterceptor.java:51)
		at org.springframework.cloud.sleuth.instrument.web.client.LazyTracingClientHttpRequestInterceptor.intercept(TraceWebClientAutoConfiguration.java:308)
		at org.springframework.http.client.InterceptingClientHttpRequest$InterceptingRequestExecution.execute(InterceptingClientHttpRequest.java:93)
		at org.springframework.http.client.InterceptingClientHttpRequest.executeInternal(InterceptingClientHttpRequest.java:77)
		at org.springframework.http.client.AbstractBufferingClientHttpRequest.executeInternal(AbstractBufferingClientHttpRequest.java:48)
		at org.springframework.http.client.AbstractClientHttpRequest.execute(AbstractClientHttpRequest.java:53)
		at org.springframework.web.client.RestTemplate.doExecute(RestTemplate.java:742)
		at org.springframework.web.client.RestTemplate.execute(RestTemplate.java:677)
		at org.springframework.web.client.RestTemplate.getForObject(RestTemplate.java:318)
		at org.springframework.samples.petclinic.api.application.CustomersServiceClient.getOwner(CustomersServiceClient.java:33)
```

L’utilisation du RestTemplate pour appeler puis agréger le résultat de 2 microservices n’était plus possible (à noter que le client Zipkin l’utilise encore, mais en asynchrone dans un thread différent de ceux gérés par Reactor). J’ai donc été contraint de migrer vers la version **réactive** de **WebClient**.

## Du Spring RestTemplate au Spring WebFlux WebClient

A l’instar du RestTemplate, **WebClient** peut être automatiquement configuré pour utiliser un
LoadBalancerClient via l’utilisation de l’annotation **@LoadBalanced** :

```java
@Bean
@LoadBalanced
public WebClient.Builder loadBalancedWebClientBuilder() {
    return WebClient.builder();
}
```

Le _@RestController_ [ApiGatewayController](https://github.com/spring-petclinic/spring-petclinic-microservices/blob/master/spring-petclinic-api-gateway/src/main/java/org/springframework/samples/petclinic/api/boundary/web/ApiGatewayController.java) exposant l’API REST _/owners/{ownerId}_ change de signature : il renvoie désormais un **_Mono_** _<OwnerDetails>_ à la place d’un _OwnerDetails_.

L’utilisation du _WebClient.Builder_ déclaré plus haut nécessite un peu d’entrainement lorsqu’il s’agit de chaîner les appels distants et d’enrichir une première réponse avec une seconde.  
Voici un exemple d’appel simplifié :

```java
@Autowired
private WebClient.Builder webClientBuilder;

@GetMapping(value = "owners/{ownerId}")
public Mono<OwnerDetails> getOwnerDetails(final @PathVariable int ownerId) {
    return webClientBuilder.build().get()
        .uri("http://customers-service/owners/{ownerId}", ownerId)
        .retrieve()
        .bodyToMono(OwnerDetails.class)
        .flatMap(owner ->
            webClientBuilder.build()
                .get()
                .uri("http://visits-service/ pets/visits?petId={petId}", joinIds(owner.getPetIds()))
                .retrieve()
                .bodyToMono(Visits.class)
                .map(addVisitsToOwner(owner))
        );
}

private String joinIds(List<Integer> petIds) {
    return petIds.stream().map(Object::toString).collect(joining(","));
}

private Function<Visits, OwnerDetails> addVisitsToOwner(OwnerDetails owner) {
    return visits -> {
        owner.getPets()
            .forEach(pet -> pet.getVisits()
                .addAll(visits.getItems().stream()
                    .filter(v -> v.getPetId() == pet.getId())
                    .collect(Collectors.toList()))
            );
        return owner;
    };
}
```

Migrer de RestTemplate à WebClient, c’est bien. Mais mettre à jour les tests unitaires, c'est mieux. La classe [MockRestServiceServer](https://docs.spring.io/spring-framework/docs/current/javadoc-api/org/springframework/test/web/client/MockRestServiceServer.html) utilisée jusque-là n’a pas d’équivalent pour WebClient. [La documentation du framework Spring invite à utiliser OkHttp MockWebServer](https://docs.spring.io/spring-framework/docs/current/spring-framework-reference/web-reactive.html#webflux-client-testing). Si cela vous intéresse, vous pouvez regarder sa mise en œuvre dans la classe de test [VisitsServiceClientIntegrationTest](https://github.com/spring-petclinic/spring-petclinic-microservices/blob/master/spring-petclinic-api-gateway/src/test/java/org/springframework/samples/petclinic/api/application/VisitsServiceClientIntegrationTest.java).

## De Netflix Hystrix à Spring Cloud Circuit Breaker et Resilience 4J

A l’instar de Spring Cloud LoadBalancer, **Spring Cloud Circuit Breaker** fait
partie du projet **Spring Cloud Commons**.
Initié suite à la retraite d’Hystrix, Spring Cloud Circuit Breaker permet de **s’abstraire de l’implémentation d’un coupe**
**circuit**. Il supporte 4 implémentations : Hystrix, Resilience4J,
Sentinel et Spring Retry.

**Resilience4J** est l’implémentation préconisée par Spring et c’est elle que j’ai donc mise en œuvre. Mais basculer sur une autre librairie est censée ne nécessiter qu’un peu de configuration.

La migration vers Spring Cloud Circuit Breaker commence par
de la configuration Maven :

1. Ajouter 2 dépendances Maven :

   1. org.springframework.cloud:spring-cloud-starter-circuitbreaker-reactor-resilience4j

   1. io.github.resilience4j:resilience4j-micrometer (cette dépendance permet de remonter des métriques dans Prometheus)
1. Exclure spring-cloud-netflix-hystrix de l’artefact spring-cloud-starter-netflix-eureka-client
1. Suppression de la dépedance org.springframework.cloud:spring-cloud-starter-netflix-hystrix

L’annotation EnableCircuitBreaker n’est pas nécessaire pour
Resilience4j. Elle a été supprimée de la classe principale.

La déclaration du **bean** **defaultCustomizer** permet de spécifier la configuration par défaut de l’ensemble des circuit breaker Resilience4j utilisés dans l’application :

```java
/**
  * Default Resilience4j circuit breaker configuration
  */
 @Bean
 public Customizer<ReactiveResilience4JCircuitBreakerFactory> defaultCustomizer() {
     return factory -> factory.configureDefault(id -> new Resilience4JConfigBuilder(id)
         .circuitBreakerConfig(CircuitBreakerConfig.ofDefaults())
         .timeLimiterConfig(TimeLimiterConfig.custom().timeoutDuration(Duration.ofSeconds(4)).build())
         .build());
 }
```

En déclarant d’autres beans Spring, il est possible de configurer
spécifiquement certains circuit breaker par leur ID.

L’utilisation d’un circuit breaker passe par l’utilisation de la fabrique **ReactiveCircuitBreakerFactory** créée par Spring Boot. La classe [ApiGatewayController](https://github.com/spring-petclinic/spring-petclinic-microservices/blob/master/spring-petclinic-api-gateway/src/main/java/org/springframework/samples/petclinic/api/boundary/web/ApiGatewayController.java) a été adaptée : le _Mono<Visits>_ renvoyé par le service _getVisitsForPets_ subit une opération de transformation. C’est le **ReactiveCircuitBreaker** _getOwnerDetails_ qui est maintenant chargé d’exécuter la suite du flux et de gérer les exceptions applicatives ou le timeout, et de router alors sur une méthode de contournement ( **fallback method**). Dans notre cas, lorsque le service des visites est inaccessible ou trop lent, on considère que l’animal de compagnie n’a pas eu de visite.

```java
private final ReactiveCircuitBreakerFactory cbFactory;@GetMapping(value = "owners/{ownerId}")
 public Mono<OwnerDetails> getOwnerDetails(final @PathVariable int ownerId) {
     return customersServiceClient.getOwner(ownerId)
         .flatMap(owner ->
             visitsServiceClient.getVisitsForPets(owner.getPetIds())
                 .transform(it -> {
                     ReactiveCircuitBreaker cb = cbFactory.create("getOwnerDetails");
                     return cb.run(it, throwable -> emptyVisitsForPets());
                 })
                 .map(addVisitsToOwner(owner))
         );
 }
```

```java
private Mono<Visits> emptyVisitsForPets() {
    return Mono.just(new Visits());
}
```

Le test unitaire [ApiGatewayControllerTest](https://github.com/spring-petclinic/spring-petclinic-microservices/blob/master/spring-petclinic-api-gateway/src/test/java/org/springframework/samples/petclinic/api/boundary/web/ApiGatewayControllerTest.java)
s’assure que le coupe circuit est opérationnel :

```java
@ExtendWith(SpringExtension.class)
@WebFluxTest(controllers = ApiGatewayController.class)
@Import(ReactiveResilience4JAutoConfiguration.class)
class ApiGatewayControllerTest {

    @MockBean
    private CustomersServiceClient customersServiceClient;

    @MockBean
    private VisitsServiceClient visitsServiceClient;

    @Autowired
    private WebTestClient client;

    /**
     * Test Resilience4j fallback method
     */
    @Test
    void getOwnerDetails_withServiceError() {
        OwnerDetails owner = new OwnerDetails();
        PetDetails cat = new PetDetails();
        cat.setId(20);
        cat.setName("Garfield");
        owner.getPets().add(cat);
        Mockito
            .when(customersServiceClient.getOwner(1))
            .thenReturn(Mono.just(owner));

        Mockito
            .when(visitsServiceClient.getVisitsForPets(Collections.singletonList(cat.getId())))
            .thenReturn(Mono.error(new ConnectException("Simulate error")));

        client.get()
            .uri("/api/gateway/owners/1")
            .exchange()
            .expectStatus().isOk()
            .expectBody()
            .jsonPath("$.pets[0].name").isEqualTo("Garfield")
            .jsonPath("$.pets[0].visits").isEmpty();
    }

}
```

Suite à cette migration, le microservice exposant le Dashboard Hystrix a tout bonnement été supprimé. L’intégration de Micrometer / Prometheus / Grafana avait déjà été réalisée et expliquée dans un précédent billet : [Dashboard Grafana dockerizé](/2019/03/dashboard-grafana-docker/). Il restera à modifier le tableau de bord Grafana pour afficher les métriques remontées par Resilience4j.

## Conclusion

Commencée sous Greenwich, le désendettement de Zuul, Ribbon et Hystrix a été achevé dans [Spring Petclinic Microservices](https://github.com/spring-petclinic/spring-petclinic-microservices) un an plus tard suite à la sortie de Spring Cloud Hoxton RC2. Fonctionnellement, rien n’a changé pour l’utilisateur. Mais techniquement, nous nous appuyons désormais sur une stack à jour et, je l’espère, promis à un bel avenir. Le code source de l’application est disponible pour tous les développeurs désirant s’inspirer d’une **mise en œuvre concrète de Spring Cloud Gateway, Spring Cloud Loadbalancer et Spring Cloud Circuit Breaker**.

Références :

- [Spring\
  Cloud Gateway - Reference manual](https://cloud.spring.io/spring-cloud-static/spring-cloud-gateway/2.2.0.RC2/reference/html/) (Pivotal)
- [Spring\
  Cloud Gateway – Configuring a simple route](https://dzone.com/articles/spring-cloud-gateway-configuring-a-simple-route) (DZone)
- [Spring\
  Cloud LoadBalancer – Reference manual](https://cloud.spring.io/spring-cloud-static/spring-cloud-commons/2.2.0.RC2/reference/html/#spring-cloud-loadbalancer) (Pivotal)
- [Spring\
  Cloud Circuit Breaker – Reference manual](https://cloud.spring.io/spring-cloud-static/spring-cloud-commons/2.2.0.RC2/reference/html/#spring-cloud-circuit-breaker) (Pivotal)
- [Introducing\
  Spring Cloud Circuit Breaker](https://spring.io/blog/2019/04/16/introducing-spring-cloud-circuit-breaker) (Pivotal)
