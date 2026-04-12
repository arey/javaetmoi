---
_edit_last: "1"
author: admin
categories:
  - retour-d'expérience
  - spring
date: "2021-11-06T16:53:05+00:00"
thumbnail: wp-content/uploads/2021/11/oauth2%5Flogo.png
featureImage: wp-content/uploads/2021/11/oauth2%5Flogo.png
guid: https://javaetmoi.com/?p=2138
parent_post_id: null
post_id: "2138"
post_views_count: "26940"
summary: "## Contexte\n\n \n\nDe nos jours, il est courant de devoir **consommer** une **API REST sécurisée** à l’aide du standard **OAuth 2.0** ou de sa surcouche **OpenID Connect** (OIDC). <br>Schématiquement, le consommateur génère un **jeton (token)** opaque ou JWT en appelant un serveur d’autorisation (Authorization server) puis, à chaque appel d’API REST, le transmet en tant que bearer via l’ **en-tête HTTP** **Authorization**. Ce token a souvent une **durée de vie** transmise par le serveur d’autorisation via la propriété **expires\\_in**.\n\nOAuth 2.0 propose quatre cinématiques (flows), la plus commune étant l’Authorization Code Flow. Lorsque l’API REST est appelée depuis une application web, il est courant de voir utiliser le Client Credentials Flow ou le **[Resource](https://www.oreilly.com/library/view/getting-started-with/9781449317843/ch04.html)** **[Owner Password Credentials Flow](https://www.oreilly.com/library/view/getting-started-with/9781449317843/ch04.html)**.\n\nRécemment, j’ai été amené à **consommer l’API REST du** **CRM Salesforce** **depuis une application Spring Boot**. Cette API était sécurisée avec le Resource Owner password Credentials Flow. Salesforce joue à la fois le rôle de l’Authorization Server et du Resource Owner. Le client (l’application Spring Boot) transmet ses **credentials** (login et mot de passe) à l’Authorization Server pour obtenir un **Access Token**. <br>Cet article a pour objectif de vous présenter la **configuration Spring Security** mise en œuvre pour appeler cette API. Les extraits de code proviennent du repository GitHub [**arey/spring-security-oauth2-salesforce-sample**](https://github.com/arey/spring-security-oauth2-salesforce-sample)."
tags:
  - oauth-2.0
  - salesforce
  - spring-security
title: Configuration Spring Security d’un client de l’API REST Salesforce sécurisée avec OAuth 2.0
url: /2021/11/configuration-spring-security-dun-client-de-lapi-rest-salesforce-securisee-avec-oauth-2-0/

---
## Contexte

{{< figure src="wp-content/uploads/2021/11/oauth2%5Flogo.png" alt="" caption="" >}}

De nos jours, il est courant de devoir **consommer** une **API REST sécurisée** à l’aide du standard **OAuth 2.0** ou de sa surcouche **OpenID Connect** (OIDC).   
Schématiquement, le consommateur génère un **jeton (token)** opaque ou JWT en appelant un serveur d’autorisation (Authorization server) puis, à chaque appel d’API REST, le transmet en tant que bearer via l’ **en-tête HTTP** **Authorization**. Ce token a souvent une **durée de vie** transmise par le serveur d’autorisation via la propriété **expires\_in**.

OAuth 2.0 propose quatre cinématiques (flows), la plus commune étant l’Authorization Code Flow. Lorsque l’API REST est appelée depuis une application web, il est courant de voir utiliser le Client Credentials Flow ou le **[Resource](https://www.oreilly.com/library/view/getting-started-with/9781449317843/ch04.html)** **[Owner Password Credentials Flow](https://www.oreilly.com/library/view/getting-started-with/9781449317843/ch04.html)**.

Récemment, j’ai été amené à **consommer l’API REST du** **CRM Salesforce** **depuis une application Spring Boot**. Cette API était sécurisée avec le Resource Owner password Credentials Flow. Salesforce joue à la fois le rôle de l’Authorization Server et du Resource Owner. Le client (l’application Spring Boot) transmet ses **credentials** (login et mot de passe) à l’Authorization Server pour obtenir un **Access Token**.   
Cet article a pour objectif de vous présenter la **configuration Spring Security** mise en œuvre pour appeler cette API. Les extraits de code proviennent du repository GitHub [**arey/spring-security-oauth2-salesforce-sample**](https://github.com/arey/spring-security-oauth2-salesforce-sample).

## Stack technique

L’appel d’une API sécurisée avec OAuth 2.0 depuis une application Java reposant sur Spring Boot peut être implémenté de plusieurs façons : une authentification maison à l’aide d’un bon vieux Apache HttpClient ou de Spring RestTemplate, l’utilisation d’une librairie tierce (ex : [MITREid](https://github.com/mitreid-connect/OpenID-Connect-Java-Spring-Server/tree/master/openid-connect-client) ou [Nimbus](https://connect2id.com/products/nimbus-oauth-openid-connect-sdk)) ou bien encore de **Spring Security**. L’utilisation de Spring Security s’est tout naturellement imposée car elle s’intègre parfaitement à la stack technique existante et était déjà utilisée dans l’application pour sécuriser ses propres API.

[Depuis sa version 5, Spring Security permet d’intégrer des services sécurisés avec OAuth 2](https://spring.io/blog/2018/03/06/using-spring-security-5-to-integrate-with-oauth-2-secured-services-such-as-facebook-and-github).0\. Il n’est plus nécessaire d’utiliser le projet [Spring Security OAuth](https://spring.io/projects/spring-security-oauth) qui a été déprécié.   
Le module [**spring-security-oauth2-client**](https://docs.spring.io/spring-security/site/docs/current/reference/html5/#spring-security-oauth2-client) contient le code client supportant OAuth 2.0 et OIDC. Son package racine est _org.springframework.security.oauth2.client_.   
Spring Boot vient avec un starter facilitant l’intégration de ce module : **spring-boot-starter-oauth2-client**.

En résumé, cet exemple s’appuie sur **Spring Boot 2.5** et **Spring Security 5.5**.

## Dépendances Maven

Pour appeler une API REST sécurisée avec OAuth 2.0, [la documentation de référence de Spring Security encourage l’utilisation de Spring **WebClient**](https://docs.spring.io/spring-security/site/docs/5.2.1.RELEASE/reference/htmlsingle/#oauth2client) provenant du **module spring-webflux**. De nombreux exemples trouvés sur le Net vont dans ce sens. L’usage de RestTemplate passe sous silence. D’après Stackoverflow, moyennant la création de l’intercepteur [OAuthClientCredentialsRestTemplateInterceptor](https://stackoverflow.com/questions/58982286/spring-security-5-replacement-for-oauth2resttemplate), pour celles et ceux qui préfèrent, il semble néanmoins possible de continuer à utiliser RestTemplate.   
Sur une application Spring MVC (non réactive) qui utilise WebClient avec des appels bloquants, voici les modules Spring Boot à déclarer dans le [pom.xml](https://github.com/arey/spring-security-oauth2-salesforce-sample/blob/main/pom.xml) de Maven :

```xml
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-web</artifactId>
</dependency>
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-webflux</artifactId>
</dependency>
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-security</artifactId>
</dependency>
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-oauth2-client</artifactId>
</dependency>
```

Remarque : le token Salesforce étant opaque, nul besoin d’ajouter la dépendance _spring-security-oauth2-jose_.

## Configuration Spring Boot

Dans le fichier de configuration Spring Boot **[application.yml](https://github.com/arey/spring-security-oauth2-salesforce-sample/blob/main/src/main/resources/application.yml)**, on déclare un client nommé salesforce et un provider du même nom (rappelez-vous, Salesforce joue le rôle d’Authorization Server et du Resource Owner). L’ **authorization-grant-type** est de type **password** (se référer à la classe [AuthorizationGrantType](https://github.com/spring-projects/spring-security/blob/5.5.3/oauth2/oauth2-core/src/main/java/org/springframework/security/oauth2/core/AuthorizationGrantType.java) pour une liste exhaustive des constantes) et le **client-authentification-method** est valorisé avec **client\_secret\_post** (se référer à la classe [ClientAuthenticationMethod](https://github.com/spring-projects/spring-security/blob/5.5.3/oauth2/oauth2-core/src/main/java/org/springframework/security/oauth2/core/ClientAuthenticationMethod.java)).

```yaml
# Configuration of the Salesforce CRM
myapp:
  salesforce:
    host: https://${SALESFORCE_SUBDOMAIN}.salesforce.com
    # Change vXX.X version if required
    base-path: ${myapp.salesforce.host}/services/data/v53.0
    # Replace the your-resource-path placeholder by your own resource path
    resource-path: /sobjects/${SALESFORCE_RESOURCE_PATH}/{id}

spring:
  security:
    oauth2:
      client:
        registration:
          salesforce:
            provider: salesforce
            client-authentication-method: client_secret_post
            authorization-grant-type: password
            client-id: ${CLIENT_ID}
            client-secret: ${CLIENT_SECRET}
            username: ${USERNAME}
            password: ${PASSWORD}
        provider:
          salesforce:
            token-uri: ${myapp.salesforce.host}/services/oauth2/token
```

Les variables en majuscule peuvent être changées / hardcodées à votre guise ou bien passées sous forme de variables d’environnements. Elles dépendent pour la plupart de l’environnement dans lequel l’application est déployée.

La classe [OAuth2ClientProperties](https://github.com/spring-projects/spring-boot/blob/v2.5.6/spring-boot-project/spring-boot-autoconfigure/src/main/java/org/springframework/boot/autoconfigure/security/oauth2/client/OAuth2ClientProperties.java) charge tous les clients définis dans le fichier application.yml ou application.properties. Les clients doivent être préfixés par le préfixe : **_spring.security.oauth2.client_**.

La cinématique [Resource Owner Password](https://www.oreilly.com/library/view/getting-started-with/9781449317843/ch04.html) n’est pas (encore ?) pleinement supporté par Spring Boot 2.5 dans la mesure où les propriétés **_username_** et **_password_** ne sont pas directement mappées dans la classe [OAuth2ClientProperties](https://github.com/spring-projects/spring-boot/blob/v2.5.6/spring-boot-project/spring-boot-autoconfigure/src/main/java/org/springframework/boot/autoconfigure/security/oauth2/client/OAuth2ClientProperties.java) de Spring Boot. Dans notre exemple, on réutilise le préfixe _spring.security.oauth2.client_ pour les déclarer au même niveau que le _client-id_ et le _client-secret_.

## Déclaration du bean salesforceWebClient

La classe de configuration Spring **[OAuth2ClientConfig](https://github.com/arey/spring-security-oauth2-salesforce-sample/blob/main/src/main/java/com/javametmoi/sample/salesforce/OAuth2ClientConfig.java)** déclare le bean **salesforceWebClient** de type WebClient. Si besoin, d’autres clients pourraient y être ajoutés.   
Le filtre [ServletOAuth2AuthorizedClientExchangeFilterFunction](https://github.com/spring-projects/spring-security/blob/5.5.3/oauth2/oauth2-client/src/main/java/org/springframework/security/oauth2/client/web/reactive/function/client/ServletOAuth2AuthorizedClientExchangeFilterFunction.java) est utilisé lors de la construction de WebClient via le WebClient.Builder.

Le bean **authorizedClientManager** construit un [OAuth2AuthorizedClientProvider](https://github.com/spring-projects/spring-security/blob/5.5.3/oauth2/oauth2-client/src/main/java/org/springframework/security/oauth2/client/OAuth2AuthorizedClientProvider.java) supportant le **grant\_type=password**. Une spécificité consiste à tester le nom du client (ici _salesforce_) pour ajouter dynamiquement _username_ et password au contexte d’autorisation [OAuth2AuthorizationContext](https://github.com/spring-projects/spring-security/blob/5.5.3/oauth2/oauth2-client/src/main/java/org/springframework/security/oauth2/client/OAuth2AuthorizationContext.java).

```java
@Configuration
public class OAuth2ClientConfig {

    private static final String SALESFORCE_CLIENT_NAME = "salesforce";

    private static final String CLIENT_PROPERTY_KEY = "spring.security.oauth2.client.registration.";

    @Autowired
    private Environment env;

    @Bean
    public OAuth2AuthorizedClientManager authorizedClientManager(
            ClientRegistrationRepository clientRegistrationRepository,
            OAuth2AuthorizedClientService authorizedClientService) {
        OAuth2AuthorizedClientProvider authorizedClientProvider =
                OAuth2AuthorizedClientProviderBuilder.builder()
                        .password()
                        .build();

        // Using AuthorizedClientServiceOAuth2AuthorizedClientManager instead of the DefaultOAuth2AuthorizedClientManager
        // to support asynchrone execution through the @Async annotation
        AuthorizedClientServiceOAuth2AuthorizedClientManager authorizedClientManager =
                new AuthorizedClientServiceOAuth2AuthorizedClientManager(
                        clientRegistrationRepository, authorizedClientService);
        authorizedClientManager.setAuthorizedClientProvider(authorizedClientProvider);
        authorizedClientManager.setContextAttributesMapper(oAuth2AuthorizeRequest -> {
                    if (SALESFORCE_CLIENT_NAME.equals(oAuth2AuthorizeRequest.getClientRegistrationId())) {
                        HashMap<String, Object> map = new HashMap<>();
                        map.put(OAuth2AuthorizationContext.USERNAME_ATTRIBUTE_NAME, getProperty(SALESFORCE_CLIENT_NAME, "username"));
                        map.put(OAuth2AuthorizationContext.PASSWORD_ATTRIBUTE_NAME, getProperty(SALESFORCE_CLIENT_NAME, "password"));
                        return map;
                    }
                    return null;
                }
        );

        return authorizedClientManager;
    }

    @Bean
    public WebClient salesforceWebClient(OAuth2AuthorizedClientManager authorizedClientManager) {
        // May use a ServerAuth2AuthorizedClientExchangeFilterFunction in a reactive stack
        ServletOAuth2AuthorizedClientExchangeFilterFunction oauth2Client =
                new ServletOAuth2AuthorizedClientExchangeFilterFunction(authorizedClientManager);
        oauth2Client.setDefaultClientRegistrationId(SALESFORCE_CLIENT_NAME);
        return WebClient.builder()
                .baseUrl(env.getProperty("myapp.salesforce.base-path"))
                .apply(oauth2Client.oauth2Configuration())
                .build();
    }

    private String getProperty(String client, String property) {
        return env.getProperty(CLIENT_PROPERTY_KEY + client + "." + property);
    }
}
```

## Utilisation du bean salesforceWebClient

Une fois configuré, le bean salesforceWebClient peut être utilisé comme tout WebClient, sans se soucier du mécanisme d’authentification.   
Exemple :

```java
@Component
public class SalesforceClient {

    private static final Logger LOG = LoggerFactory.getLogger(SalesforceClient.class);

    @Autowired
    private WebClient salesforceWebClient;

    @Value("${myapp.salesforce.resource-path}")
    private String resourcePath;

    public String upsertResource(String resourceId, String jsonRequest) {
        Mono<String> response = salesforceWebClient
                .patch()
                .uri(uriBuilder -> uriBuilder
                        .path(resourcePath)
                        .build(resourceId))
                .contentType(MediaType.APPLICATION_JSON)
                .bodyValue(jsonRequest)
                .retrieve()
                .onStatus(HttpStatus::isError, errorResponse -> {
                    logErrorBody(errorResponse);
                    return Mono.error(new RuntimeException(String.format("Salesforce request on error status=%s, headers=%s",
                            errorResponse.statusCode(), errorResponse.headers().asHttpHeaders())));
                })
                .bodyToMono(String.class);

        return response.block();
    }

    public static void logErrorBody(ClientResponse response) {
        if (LOG.isErrorEnabled()) {
            response.bodyToMono(String.class)
                    .publishOn(Schedulers.boundedElastic())
                    .subscribe(body -> LOG.error("Body of the #Salesforce error response: {}", body));
        }
    }
}
```

Lors de l’appel à _response.block()_, la méthode _ServletOAuth2AuthorizedClientExchangeFilterFunction::filter_ est appelée. Lors du premier appel, elle délègue l’authentification OAuth 2.0 à la classe [DefaultPasswordTokenResponseClient](https://github.com/spring-projects/spring-security/blob/5.5.3/oauth2/oauth2-client/src/main/java/org/springframework/security/oauth2/client/endpoint/DefaultPasswordTokenResponseClient.java). En coulisse, un _RestTemplate_ est utilisé pour réaliser l’appel POST HTTP et récupérer l’access token :

```http
POST https://<your_subdomain>.salesforce.com/services/oauth2/token?
grant_type=password
&username=...
&password=...
&client_id=…
&client_secret=…

```

Le **test d’intégration** [**SalesforceClientIntegrationTest**](https://github.com/arey/spring-security-oauth2-salesforce-sample/blob/main/src/test/java/com/javametmoi/sample/salesforce/SalesforceClientIntegrationTest.java) permet de vérifier que tout fonctionne.

## Pour aller plus loin

Dans cet article, au travers d’exemples de code extraits du repo GitHub [spring-security-oauth2-salesforce-sample](https://github.com/arey/spring-security-oauth2-salesforce-sample), nous avons vu comment implémenter la cinématique OAuth 2.0 Resource Owner Password Credentials dans une application Spring Boot 2.5 avec Spring Security 5.5.

Cette implémentation n’est pas parfaite dans le sens où Salesforce ne renvoie malheureusement pas l’en-tête `expires_in` recommandée par la [RFC-6749](https://datatracker.ietf.org/doc/html/rfc6749#section-5.1) et précisant la durée de validation de l’access token (en général de 2h, mais sans garantie). En son absence, la méthode `getExpiresAt()` de la classe [OAuth2AccessTokenResponse](https://github.com/spring-projects/spring-security/blob/main/oauth2/oauth2-core/src/main/java/org/springframework/security/oauth2/core/endpoint/OAuth2AccessTokenResponse.java) de Spring Security le calcule en ajoutant une seconde au timestamp `issued_at`. Vous l’aurez compris, l’authentification OAuth 2.0 se fera presque à chaque requête. Dans mon cas métier, ce n’était pas trop préoccupant car les appels Salesforce étaient peu fréquents et en asynchrone. Je vous laisse réfléchir à ce qu’il en est pour vous ? Selon le [site d’Xkit](https://xkit.co/post/when-do-salesforce-access-tokens-expire), il semblerait que Salesforce expose une [**API OAuth 2.0 d’introspection**](https://help.salesforce.com/s/articleView?id=sf.remoteaccess_oidc_token_introspection_endpoint.htm&type=5) permettant de connaître l’état du jeton et donc sa validité. Resterait à trouver comment brancher cet appel dans Spring Security.

**Ressources** :

- [OAuth 2 Resource Owner Password Credentials Flow](https:/guide-api-rest.marmicode.fr/securite-des-apis-rest/oauth-2/oauth-2-authorization-code-flow) (Marmicode)
- [Getting Started with OAuth 2.0 by Ryan Boyd - Chapter 4. Resource Owner Password Flow](https://www.oreilly.com/library/view/getting-started-with/9781449317843/ch04.html) (Oreilly library)
- [Using Spring Security 5 to integrate with OAuth 2-secured services such as Facebook and GitHub](https://spring.io/blog/2018/03/06/using-spring-security-5-to-integrate-with-oauth-2-secured-services-such-as-facebook-and-github) (Spring Blog)
- [Spring Security OAuth 5.2 Migration Sample](https://github.com/jgrandja/spring-security-oauth-5-2-migrate) (GitHub)
- [Spring Security 5 Replacement for OAuth2RestTemplate](https://stackoverflow.com/questions/58982286/spring-security-5-replacement-for-oauth2resttemplate) (StackOverflow)
- [Spring Security OAuth 2.0 client configuration for Salesforce](https://github.com/arey/spring-security-oauth2-salesforce-sample) (GitHub)
- [OAuth 2.0 Username-Password Flow for Special Scenarios](https://help.salesforce.com/s/articleView?id=sf.remoteaccess_oauth_username_password_flow.htm&type=5)(Salesforce documentation)
- [REST API Developer Guide](https://developer.salesforce.com/docs/atlas.en-us.api_rest.meta/api_rest/intro_rest.htm) (Salesforce documentation)
- [When do Salesforce access tokens expire?](https://xkit.co/post/when-do-salesforce-access-tokens-expire) (Xkit)
