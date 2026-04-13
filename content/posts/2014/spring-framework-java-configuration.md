---
_edit_last: "1"
author: admin
categories:
  - spring
date: "2014-06-16T05:07:42+00:00"
thumbnail: wp-content/uploads/2014/05/logo-spring-highres.png
featureImage: wp-content/uploads/2014/05/logo-spring-highres.png
featureImageAlt: "logo-spring-highres"
guid: http://javaetmoi.com/?p=1122
parent_post_id: null
post_id: "1122"
post_views_count: "18142"
summary: Dans ce billet, nous verrons comment **configurer en Java** le **contexte Spring** d’une application basée sur **Spring MVC**, **Spring Security**, **Spring Data JPA** et **Hibernate**, et cela sans utiliser la moindre ligne de XML.<br>Personnellement, je n’ai rien contre la **syntaxe XML** à laquelle j’étais habitué. D’autant la **verbosité** de la configuration avait considérablement diminué grâce à l’introduction des **namespaces XML** et des **annotations**. Avant d’utiliser la syntaxe Java sur une application d’entreprise, j’étais même sceptique quant aux gains qu’elle pouvait apporter. Aujourd’hui, je comprends mieux son intérêt et pourquoi les projets du portfolio Spring tels [Spring Integration 4.0](http://spring.io/blog/2014/04/30/spring-integration-4-0-released), [Spring Web Service 2.2](ttp://spring.io/blog/2014/05/22/spring-web-services-2-2-0-released) ou bien [Spring Security 3.2](http://spring.io/blog/2013/07/03/spring-security-java-config-preview-web-security) proposent dans leur dernière version un niveau de configuration Java iso-fonctionnel avec leur équivalent XML. Sans compter que le support de la configuration Java leur ouvre la porte d’une intégration plus poussée à [**Spring Boot**](http://projects.spring.io/spring-boot/), le nouveau fer de lance de Pivotal.<br>
tags:
  - hibernate
  - java
  - jpa
  - spring-framework
  - spring-mvc
  - spring-security
title: Configurez Spring en Java
url: /2014/06/spring-framework-java-configuration/

---
![logo-spring-highres](wp-content/uploads/2014/05/logo-spring-highres.png)

Dans ce billet, nous verrons comment **configurer en Java** le **contexte Spring** d’une application basée sur **Spring MVC**, **Spring Security**, **Spring Data JPA** et **Hibernate**, et cela sans utiliser la moindre ligne de XML.  
Personnellement, je n’ai rien contre la **syntaxe XML** à laquelle j’étais habitué. D’autant la **verbosité** de la configuration avait considérablement diminué grâce à l’introduction des **namespaces XML** et des **annotations**. Avant d’utiliser la syntaxe Java sur une application d’entreprise, j’étais même sceptique quant aux gains qu’elle pouvait apporter. Aujourd’hui, je comprends mieux son intérêt et pourquoi les projets du portfolio Spring tels [Spring Integration 4.0](http://spring.io/blog/2014/04/30/spring-integration-4-0-released), [Spring Web Service 2.2](ttp://spring.io/blog/2014/05/22/spring-web-services-2-2-0-released) ou bien [Spring Security 3.2](http://spring.io/blog/2013/07/03/spring-security-java-config-preview-web-security) proposent dans leur dernière version un niveau de configuration Java iso-fonctionnel avec leur équivalent XML. Sans compter que le support de la configuration Java leur ouvre la porte d’une intégration plus poussée à [**Spring Boot**](http://projects.spring.io/spring-boot/), le nouveau fer de lance de Pivotal.  

## Préambule

Avant de faire partie intégrante du framework Spring, la configuration Java était proposée aux développeurs Spring dans un projet externe : [Spring JavaConfig](http://docs.spring.io/spring-javaconfig/docs/1.0.0.M4/reference/html/). Depuis la version 3.0 du framework Spring, des fonctionnalités équivalentes ont été introduites au fil des versions. La version 4.0 voit l’aboutissement de ce travail.

Tous les extraits de code suivants sont issus d’une application web disponible sur Github : **[spring-javaconfig-sample](https://github.com/arey/spring-javaconfig-sample)**.  
Les dépendances maven requises sont déclarées dans le [pom.xml.](https://github.com/arey/spring-javaconfig-sample/blob/master/pom.xml) La toute dernière version des frameworks ont été exploitées :

- **Spring Framework 4.0**
- **Spring Data JPA 1.6**
- **Spring Security 3.2**
- **Hibernate 4.3**

Afin que cette application puisse être déployée dans un conteneur de Servlet 2.5, l’initialisation de la configuration Spring repose intégralement sur les déclarations réalisées en XML dans le web.xml. A cet effet, lors de la commande mvn clean install , un [serveur Jetty 6 compatible servlet 2.5](http://wiki.eclipse.org/Jetty/Starting/Jetty_Version_Comparison_Table) démarre puis arrête l’application.  
Dans un conteneur de Servlet 3.x, la déclaration du _DispatcherServlet_ pourrait être réalisée en Java via la classe [_AbstractAnnotationConfigDispatcherServletInitializer_](https://github.com/spring-projects/spring-framework/blob/master/spring-webmvc/src/main/java/org/springframework/web/servlet/support/AbstractAnnotationConfigDispatcherServletInitializer.java) introduite dans Spring 3.2.

Ce billet n’a pas pour vocation de se substituer au [manuel de référence du framework Spring](http://docs.spring.io/spring/docs/4.0.5.RELEASE/spring-framework-reference/htmlsingle/). Il ne vous montrera pas non plus l’équivalent XML de la configuration Java. Son objectif est de vous donner un exemple de configuration afin que vous puissiez monter rapidement une application utilisant la syntaxe Java.

## Contextes applicatifs Spring

L’application web donnée en exemple reprend l’architecture type d’une application Spring MVC dans laquelle un _[WebApplicationContext](https://github.com/spring-projects/spring-framework/blob/v4.0.5.RELEASE/spring-web/src/main/java/org/springframework/web/context/WebApplicationContext.java)_ parent (ou root) est chargé avec le listener _[ContextLoaderListener](https://github.com/spring-projects/spring-framework/blob/v4.0.5.RELEASE/spring-web/src/main/java/org/springframework/web/context/ContextLoaderListener.java)_ et un _WebApplicationContext_ enfant est chargé via la _[DispatcherServlet](https://docs.spring.io/spring-framework/docs/current/javadoc-api/org/springframework/web/servlet/DispatcherServlet.html)_.

Le **contexte parent** met à disposition les beans Spring de la **couche service métier** et de la **couche de persistance** ( **infrastructure comprise**). La **sécurité** est également définie au niveau du contexte parent car les services métiers peuvent être sécurisés ( _[@Secured](https://github.com/spring-projects/spring-security/blob/3.2.4.RELEASE/core/src/main/java/org/springframework/security/access/annotation/Secured.java)_). Chacune de ces couches étant configurée dans une classe qui lui est dédiée, la classe **_[MainConfig](https://github.com/arey/spring-javaconfig-sample/blob/master/src/main/java/com/javaetmoi/sample/config/MainConfig.java)_** a pour rôle de toutes les référencer :

```java
@Configuration
@Import(value = {
        DataSourceConfig.class,
        InfrastructureConfig.class,
        RepositoryConfig.class,
        ServiceConfig.class,
        SecurityConfig.class
} )
public class MainConfig {

```

L’ **annotation [_@Configuration_](https://github.com/spring-projects/spring-framework/blob/f29d6eb5f68bb3acc4100172e5d6bc8b985fd9fa/spring-context/src/main/java/org/springframework/context/annotation/Configuration.java) joue un rôle central**. Les classes où elle est apposée se substituent en effet aux traditionnels fichiers de configuration XML. Nous y retrouvons la **déclaration de beans Spring**, l’ **import** de fichiers ou de classes de configuration, la **détection automatique de beans** annotés par analyse de classpath ou bien encore l’ **activation de fonctionnalités** avancées et des annotations associées ( _@Transactional_, _@Cacheable_, _@Scheduled_, _@Async_ …)

Remarque : la déclaration de beans Spring peut se faire en dehors d’une classe de _@Configuration_. C’est ce qu’on appelle le **mode** **lite Beans**. Non recommandé, le manuel de référence de Spring explique quels en sont les limitations et les dangers.

La classe **_[MainConfig](https://github.com/arey/spring-javaconfig-sample/blob/master/src/main/java/com/javaetmoi/sample/config/MainConfig.java)_** est également annotée avec l’annotation [**_@Import_**](https://github.com/spring-projects/spring-framework/blob/f29d6eb5f68bb3acc4100172e5d6bc8b985fd9fa/spring-context/src/main/java/org/springframework/context/annotation/Import.java) permettant d’importer d’autres classes de configuration. Via l’annotation [**_@ImportResource_**](https://github.com/spring-projects/spring-framework/blob/f29d6eb5f68bb3acc4100172e5d6bc8b985fd9fa/spring-context/src/main/java/org/springframework/context/annotation/ImportResource.java), Spring offre la possibilité d’importer des fichiers de configuration XML. Très pratique lorsqu’on dépend de librairies tierces n’offrant qu’une configuration XML.

Pour Spring, les **classes annotées avec _@Configuration_** sont des **beans Spring**:

```sh
08:02:13.246 [main] DEBUG o.s.b.f.s.DefaultListableBeanFactory - Creating shared instance of singleton bean 'mainConfig'
08:02:13.246 [main] DEBUG o.s.b.f.s.DefaultListableBeanFactory - Creating instance of bean 'mainConfig'
```

Cette spécificité infère aux beans de configuration la possibilité d’utiliser l’ **injection de dépendance** via les annotations **_@Autowired_** et **_@Inject_**. Leur cycle de vie permet également d’utiliser les annotations **_@PostConstruct_** et **_@PreDestroy_**.  
La classe **_[MainConfig](https://github.com/arey/spring-javaconfig-sample/blob/master/src/main/java/com/javaetmoi/sample/config/MainConfig.java)_** exploite cette possibilité pour injecter l’ [**_Environment_**](https://github.com/spring-projects/spring-framework/blob/1204d2aef4afdefb4ba73c86565aab3f5b2a6931/spring-core/src/main/java/org/springframework/core/env/Environment.java) modélisant l’environnement d’exécution de l’application. Cette interface permet notamment d’accéder aux **profils Spring activés**. Lors de l’initialisation de la configuration spécifiée par **_[MainConfig](https://github.com/arey/spring-javaconfig-sample/blob/master/src/main/java/com/javaetmoi/sample/config/MainConfig.java)_**, la méthode _initApp()_ annotée avec _@PostConstruct_ génère une trace listant les profils actifs.

```java
    @Autowired
    private Environment         env;

    @PostConstruct
    public void initApp() {
        LOG.debug("Looking for Spring profiles...");
        if (env.getActiveProfiles().length == 0) {
            LOG.info("No Spring profile configured, running with default configuration.");
        } else {
            for (String profile : env.getActiveProfiles()) {
                LOG.info("Detected Spring profile: {}", profile);
            }
        }
    }

```

Le **contexte enfant** est quant à lui définie au travers d’une seule classe **_[WebMvcConfig](https://github.com/arey/spring-javaconfig-sample/blob/master/src/main/java/com/javaetmoi/sample/config/WebMvcConfig.java)_** que nous détaillerons par la suite. Cette hiérarchie de contexte permet aux beans de type _@Service_ déclarés dans le contexte parent d’être visibles par les beans de type _@Controller_, l’inverse n’étant pas vrai.

## Tester la configuration Spring

De par le fait qu’elle est **vérifiée à la compilation**, la configuration codée en Java permet d’éviter de facto les erreurs que l’on retrouvait couramment en XML : fautes de frappe, déplacement de classes, JAR non présent dans le classpath ...  
Ce premier garde-fou n’empêche pas d’autres erreurs. Par exemple, l’annotation [_@EnableCaching_](https://github.com/spring-projects/spring-framework/blob/05e96ee44817d40c7a60734bd4b8ec577d6e5194/spring-context/src/main/java/org/springframework/cache/annotation/EnableCaching.java) génère une exception lorsqu’aucun bean de type [_CacheManager_](https://github.com/spring-projects/spring-framework/blob/658f7f58dfd5299757a16aa16133b576555d2a75/spring-context/src/main/java/org/springframework/cache/CacheManager.java) n’a pas été déclaré :

```java
Caused by: java.lang.IllegalStateException: No bean of type CacheManager could be found. Register a CacheManager bean or remove the @EnableCaching annotation from your configuration.
```

Pour se prémunir de genre d’exceptions découvertes au démarrage de votre application, le **module Spring Test** propose tout un jeu d’annotations : **_@WebAppConfiguration_**, [**_@ContextConfiguration_**](https://github.com/spring-projects/spring-framework/blob/b308659cda79f39f117f59f2d083abdd83f654d5/spring-test/src/main/java/org/springframework/test/context/ContextConfiguration.java), [**_@ActiveProfiles_**](https://github.com/spring-projects/spring-framework/blob/b308659cda79f39f117f59f2d083abdd83f654d5/spring-test/src/main/java/org/springframework/test/context/ActiveProfiles.java) ou bien encore [**_@ContextHierarchy_**](https://github.com/spring-projects/spring-framework/blob/b308659cda79f39f117f59f2d083abdd83f654d5/spring-test/src/main/java/org/springframework/test/context/ContextHierarchy.java). Introduite avec la version 3.2.2 de Spring, cette dernière permet de reproduire une hiérarchie de contextes Spring et de tester ainsi le chargement de contextes en conditions réelles.  
La classe **_[SpringConfigTest](https://github.com/arey/spring-javaconfig-sample/blob/master/src/test/java/com/javaetmoi/sample/config/SpringConfigTest.java)_** donne un exemple de test d’intégration de configuration Spring :

```java
@RunWith(SpringJUnit4ClassRunner.class)
@WebAppConfiguration
@ContextHierarchy({
        @ContextConfiguration(classes = MainConfig.class),
        @ContextConfiguration(classes = WebMvcConfig.class) })
@ActiveProfiles("test")
public class SpringConfigTest {

    @Autowired
    private WebApplicationContext wac;

    @Test
    public void springConfiguration() {
        assertNotNull(wac);
    }
}

```

## DataSource

La couche de persistance reposant sur JPA, une **connexion à une base de données relationnelle** est nécessaire. Selon le contexte dans lequel s’exécute l’application, cette _DataSource_ peut être récupérée de 2 manières :

1. Par **lookup JNDI** lorsque l’application est déployée dans un serveur d’application JavaEE ou un conteneur web gérant ses propres ressources.
1. **Initialisée au démarrage de l’application** par création d’une base de données en mémoire. Utile pour les tests d’intégration ou pour faciliter le déploiement de l’application.

Déclaré dans le bean de configuration **_[DataSourceConfig](https://github.com/arey/spring-javaconfig-sample/blob/master/src/main/java/com/javaetmoi/sample/config/DataSourceConfig.java)_**, le **bean dataSource** sera par la suite injecté dans le bean de configuration _InfrastructureConfig_.

**L’instanciation, la configuration et l’initialisation d’un bean Spring** est réalisé dans une **méthode annotée par** [**_@Bean_**](https://github.com/spring-projects/spring-framework/blob/master/spring-context/src/main/java/org/springframework/context/annotation/Bean.java). Par défaut, le nom du bean Spring est déduit du nom de sa méthode. Voici un exemple de déclaration de beans :

```java
@Configuration
@PropertySource({ "classpath:com/javaetmoi/sample/config/datasource.properties" })
public class DataSourceConfig {

    @Autowired
    private Environment env;

    @Bean
    @Profile("javaee")
    public JndiObjectFactoryBean dataSource() throws IllegalArgumentException {
        JndiObjectFactoryBean dataSource = new JndiObjectFactoryBean();
        dataSource.setExpectedType(DataSource.class);
        dataSource.setJndiName(env.getProperty("jdbc.jndiDataSource"));
        return dataSource;
    }

    @Bean
    @Profile("test")
    public DataSource testDataSource() {
        return new EmbeddedDatabaseBuilder().setType(EmbeddedDatabaseType.H2).build();
    }
}

```

On retrouve une méthode de déclaration de _DataSource_ pour chacun des 2 contextes présentés ci-dessus. Chaque méthode et annotée avec un [_@Profile_](https://github.com/spring-projects/spring-framework/blob/master/spring-context/src/main/java/org/springframework/context/annotation/Profile.java) Spring différent : **javaee** et **test**.  
Le profile **javaee** est activé dans le **[web.xml](https://github.com/arey/spring-javaconfig-sample/blob/master/src/main/webapp/WEB-INF/web.xml)**:

```xhtml
<context-param>
  <param-name>spring.profiles.active</param-name>
  <param-value>javaee</param-value>
</context-param>
```

Le profile **test** est quant à lui activé par l’annotation **@ActiveProfiles("test")** apposée sur la classe de test _[SpringConfigTest](https://github.com/arey/spring-javaconfig-sample/blob/master/src/test/java/com/javaetmoi/sample/config/SpringConfigTest.java)_.  
La **méthode _dataSource()_** utilise la fabrique de beans _[JndiObjectFactoryBean](https://github.com/spring-projects/spring-framework/blob/e9a24da2253ea23a90f65d52f8dcf2ed3b15afc3/spring-context/src/main/java/org/springframework/jndi/JndiObjectFactoryBean.java)_ pour récupérer la _DataSource_ à partir de son nom JNDI.  
Le bean _Environment_ est de nouveau utilisé. Cette fois-ci, pour récupérer la valeur de la propriété _"jdbc.jndiDataSource"_ définie dans le fichier _datasource.properties_ chargée à l’aide de l’annotation [**_@PropertySource_**](https://github.com/spring-projects/spring-framework/blob/master/spring-context/src/main/java/org/springframework/context/annotation/PropertySource.java).

A noter que le type de retour de cette méthode est un _JndiObjectFactoryBean_. Pour retourner directement un _DataSource_, il aurait été nécessaire de se substituer au conteneur Spring en invoquant la méthode _afterPropertiesSet()_ de la fabrique de beans :

```java
dataSource.afterPropertiesSet();
return (DataSource) dataSource.getObject();
```

En effet, appelée pendant la phase d’initialisation du bean, _afterPropertiesSet()_ effectue le lookup JNDI. Sans cet appel, la dataSource serait _null_ :

```java
Caused by: org.springframework.beans.factory.BeanDefinitionStoreException: Factory method [public javax.persistence.EntityManagerFactory com.javaetmoi.sample.config.InfrastructureConfig.entityManagerFactoryBean()] threw exception; nested exception is java.lang.IllegalArgumentException: DataSource must not be null
```

## Couche de persistance

Déjà amorcée par la déclaration de la source de données, la mise en œuvre de la couche de persistance est complétée par 2 autres beans de configuration :

1. **_[InfrastructureConfig](https://github.com/arey/spring-javaconfig-sample/blob/master/src/main/java/com/javaetmoi/sample/config/InfrastructureConfig.java)_** : infrastructure JPA composée d’une **fabrique du gestionnaire d’entités JPA** et du **gestionnaire de transactions** associé
1. **_[RepositoryConfig](https://github.com/arey/spring-javaconfig-sample/blob/master/src/main/java/com/javaetmoi/sample/config/RepositoryConfig.java)_** : **activation de Spring Data JPA** et **détection des beans** de type [_Repository_](https://github.com/spring-projects/spring-data-commons/blob/cc576a73981d94f51511c80830aacd2afd744900/src/main/java/org/springframework/data/repository/Repository.java) (DAOs)

L’annotation [**_@EnableTransactionManagement_**](https://github.com/spring-projects/spring-framework/blob/1204d2aef4afdefb4ba73c86565aab3f5b2a6931/spring-tx/src/main/java/org/springframework/transaction/annotation/EnableTransactionManagement.java) portée par le **bean _[InfrastructureConfig](https://github.com/arey/spring-javaconfig-sample/blob/master/src/main/java/com/javaetmoi/sample/config/InfrastructureConfig.java)_** permet d’activer l’utilisation des annotations _[@Transactional](https://github.com/spring-projects/spring-framework/blob/1204d2aef4afdefb4ba73c86565aab3f5b2a6931/spring-tx/src/main/java/org/springframework/transaction/annotation/Transactional.java)_ chargées de délimiter les transactions base de données :

```java
@Configuration
@EnableTransactionManagement
@PropertySource({ "classpath:com/javaetmoi/sample/config/infrastructure.properties" })
public class InfrastructureConfig {

    @Autowired
    Environment        env;

    @Autowired
    private DataSource dataSource;

```

Récupérée par JNDI ou instanciée en mémoire, la _DataSource_ est injectée sur le même modèle que n’importe quel bean Spring.  
Viennent ensuite la déclaration des beans **_transactionManager_** et **_transactionTemplate_** :

```java
    @Bean
    public JpaTransactionManager transactionManager() {
        JpaTransactionManager jpaTransactionManager = new JpaTransactionManager();
        jpaTransactionManager.setEntityManagerFactory(entityManagerFactory());
        return jpaTransactionManager;
    }

    @Bean
    public TransactionTemplate transactionTemplate() {
        TransactionTemplate transactionTemplate = new TransactionTemplate();
        transactionTemplate.setTransactionManager(transactionManager());
        return transactionTemplate;
    }

```

Mettons de côté la méthode _entityManagerFactory()_ sur laquelle nous reviendrons plus loin. Cette configuration montre **comment mettre en relations 2 beans Spring** : le bean _transactionTemplate_ utilise en effet le bean _transactionManager_. En XML, cette mise en relation est habituellement réalisée à l’aide de la balise _ref_ et de l’identifiant du bean. En Java, l’ **injection d’un bean dans un autre** se fait en utilisant la méthode de déclaration du bean à injecter, en l’occurrence ici _transactionManager()_. **Ce qui ressemble à un appel de méthode est trompeur**. **En effet, Spring interprète ce type d’appel afin de gérer le cycle de vie des Beans**. Par exemple, lorsqu’un bean est de portée singleton, la méthode de création du bean n’est invoquée qu’une seule et unique fois même si le bean est injecté dans plusieurs beans. Techniquement, Spring instrumente les classes annotées avec _@Configuration_ au démarrage du contexte applicatif.

Le bean **_entityManagerFactory_** est déclaré de la façon suivante :

```java
Ex    @Bean
    public EntityManagerFactory entityManagerFactory() {
        LocalContainerEntityManagerFactoryBean em = new LocalContainerEntityManagerFactoryBean();
        em.setDataSource(dataSource);
        em.setPersistenceUnitName("javaconfigSamplePersistenceUnit");
        em.setPackagesToScan("com.javaetmoi.sample.domain");
        em.setJpaVendorAdapter(jpaVendorAdaper());
        em.setJpaPropertyMap(additionalProperties());
        em.afterPropertiesSet();
        return em.getObject();
    }

```

Il utilise le bean _dataSource_ injecté plus haut dans la classe de configuration. Derrière la méthode _jpaVendorAdaper()_ se cache un autre bean. Quant à _additionalProperties()_, il s’agit d’un vrai appel de méthode. De la même manière que pour la _DataSource_, l’appel aux méthodes _afterPropertiesSet()_ et _getObject()_ sont nécessaires pour retourner un bean de type _EntityManagerFactory._

Une **autre possibilité** aurait consisté à renvoyer un _LocalContainerEntityManagerFactoryBean_ puis à utiliser l’annotation _@Autowired_ sur la méthode _transactionManager_. Charge à Spring de demander à la fabrique de beans de lui retourner un _EntityManagerFactory_:

```java
@Bean
public LocalContainerEntityManagerFactoryBean entityManagerFactoryBean() {
        LocalContainerEntityManagerFactoryBean em = new LocalContainerEntityManagerFactoryBean();
    // …
    return em;
}

@Bean
@Autowired
public JpaTransactionManager transactionManager(EntityManagerFactory entityManagerFactory) {
    JpaTransactionManager jpaTransactionManager = new JpaTransactionManager();
    jpaTransactionManager.setEntityManagerFactory(entityManagerFactory);
    return jpaTransactionManager;
}
```

L’injection du bean _dataSource_ dans le _LocalContainerEntityManagerFactoryBean_ aurait pu être réalisée d’une autre manière. En effet, en tant que beans Spring, les beans de configuration peuvent être injectés dans d’autres bean de configuration. Ainsi, le bean _DataSourceConfig_ aurait pu être injecté dans _InfrastructureConfig_. Il devient alors possible d’appeler dataSourceConfig.dataSource()  pour récupérer la _dataSource_ :

```java
@Autowired
private DataSourceConfig dataSourceConfig;
…
@Bean
public EntityManagerFactory entityManagerFactory() {
    LocalContainerEntityManagerFactoryBean em = new LocalContainerEntityManagerFactoryBean();
    em.setDataSource(dataSourceConfig.dataSource());
    …
}
```

Bien que facilitant la navigation dans la configuration Spring, cette technique induit un **couplage fort** entre les 2 beans de configuration.  
Une fois l’infrastructure Hibernate / JPA mis en place, le bean de configuration **_[RepositoryConfig](https://github.com/arey/spring-javaconfig-sample/blob/master/src/main/java/com/javaetmoi/sample/config/RepositoryConfig.java)_** initie la couche d’accès aux données. Par commodité, son implémentation est réalisée à l’aide du projet **[Spring Data JPA](http://projects.spring.io/spring-data-jpa/)**. L’annotation **_[@EnableJpaRepositories](https://github.com/spring-projects/spring-data-jpa/blob/b99508fbf9e5f02aa35a1ff3c92b0c34d6bdedf4/src/main/java/org/springframework/data/jpa/repository/config/EnableJpaRepositories.java)_** active ce dernier : **toutes les interfaces contenues dans un package donné et étendant l’interface _[Repository](https://github.com/spring-projects/spring-data-commons/blob/cc576a73981d94f51511c80830aacd2afd744900/src/main/java/org/springframework/data/repository/Repository.java)_ de Spring Data sont détectées puis interprétées**. Par défaut, les requêtes JPA sont générées à partir du nom des méthodes exposées dans ces interfaces. Les implémentations personnalisées des _Repository_ sont recherchées à l’aide du suffixe _Impl_.

```java
@Configuration
@EnableJpaRepositories("com.javaetmoi.sample.repository")
public class RepositoryConfig { }

```

La couche de persistance est sans doute celle nécessitant le plus de configuration. A côté, la couche services métiers est particulièrement simple.

## Couche services

L’objectif premier de **_[ServiceConfig](https://github.com/arey/spring-javaconfig-sample/blob/master/src/main/java/com/javaetmoi/sample/config/ServiceConfig.java)_** consiste à **détecter tous les beans Spring annotés par l’annotation** **_[@Service](https://github.com/spring-projects/spring-framework/blob/v4.0.5.RELEASE/spring-context/src/main/java/org/springframework/stereotype/Service.java)_**. L’annotation **_[@ComponentScan](https://github.com/spring-projects/spring-framework/blob/v4.0.5.RELEASE/spring-context/src/main/java/org/springframework/context/annotation/ComponentScan.java)_** joue ce rôle en **analysant récursivement** le package Java dédié aux services métiers, dans notre exemple le package _com.javaetmoi.sample.service_ :

```java
@Configuration
@EnableAsync
@EnableScheduling
@EnableAspectJAutoProxy
@EnableCaching
@ComponentScan(basePackages = { "com.javaetmoi.sample.service" })
public class ServiceConfig implements AsyncConfigurer {

```

C’est dans cette couche que je vous propose d’activer des **fonctionnalités avancées** de Spring :

- **_[@EnableAsync](https://github.com/spring-projects/spring-framework/blob/v4.0.5.RELEASE/spring-context/src/main/java/org/springframework/scheduling/annotation/EnableAsync.java)_**: appel de méthode asynchrone via l’annotation _[@Async](https://github.com/spring-projects/spring-framework/blob/v4.0.5.RELEASE/spring-context/src/main/java/org/springframework/scheduling/annotation/Async.java)_
- **_[@EnableScheduling](https://github.com/spring-projects/spring-framework/blob/v4.0.5.RELEASE/spring-context/src/main/java/org/springframework/scheduling/annotation/EnableScheduling.java)_**: planification d’appel de méthode via l’annotation _[@Scheduled](https://github.com/spring-projects/spring-framework/blob/v4.0.5.RELEASE/spring-context/src/main/java/org/springframework/scheduling/annotation/Scheduled.java)_
- **_[@EnableAspectJAutoProxy](https://github.com/spring-projects/spring-framework/blob/v4.0.5.RELEASE/spring-context/src/main/java/org/springframework/context/annotation/EnableAspectJAutoProxy.java)_**: proxyfication de beans Spring ne possédant pas d’interface.
- **_[@EnableCaching](https://github.com/spring-projects/spring-framework/blob/v4.0.5.RELEASE/spring-context/src/main/java/org/springframework/cache/annotation/EnableCaching.java)_**: résultat de l’appel de méthode mis en cache avec _[@Cacheable](https://github.com/spring-projects/spring-framework/blob/v4.0.5.RELEASE/spring-context/src/main/java/org/springframework/cache/annotation/Cacheable.java)_, évincer avec _[@CacheEvict](https://github.com/spring-projects/spring-framework/blob/v4.0.5.RELEASE/spring-context/src/main/java/org/springframework/cache/annotation/CacheEvict.java)_ ou bien rafraichit avec _[@CachePut](https://github.com/spring-projects/spring-framework/blob/v4.0.5.RELEASE/spring-context/src/main/java/org/springframework/cache/annotation/CachePut.java)_. Si vous n’ pas encore [passés à Java 8](http://docs.oracle.com/javase/tutorial/java/annotations/repeating.html), l’annotation _[@Caching](https://github.com/spring-projects/spring-framework/blob/v4.0.5.RELEASE/spring-context/src/main/java/org/springframework/cache/annotation/Caching.java)_ permet d’utiliser plusieurs fois l’une des 3 annotations précédentes sur la même méthode.

Comme indiqué plus haut, l’annotation _@EnableCaching_ nécessite un _[CacheManager](https://github.com/spring-projects/spring-framework/blob/v4.0.5.RELEASE/spring-context/src/main/java/org/springframework/cache/CacheManager.java)_. La définition d’un bean _cacheManager_ et d’un _defaultCache_ sont donnés ici à titre indicatif :

```java
@Bean
    public CacheManager cacheManager() {
        SimpleCacheManager cacheManager = new SimpleCacheManager();
        List<Cache> caches = new ArrayList<Cache>();
        // to customize
        caches.add(defaultCache());
        cacheManager.setCaches(caches);
        return cacheManager;
    }

    @Bean
    public Cache defaultCache() {
        ConcurrentMapCacheFactoryBean cacheFactoryBean = new ConcurrentMapCacheFactoryBean();
        cacheFactoryBean.setName("default");
        cacheFactoryBean.afterPropertiesSet();
        return cacheFactoryBean.getObject();

    }

```

Afin de pouvoir personnaliser le pool de threads utilisé lors de traitements asynchrone, l’annotation _@EnableAsync_ encourage à définir son propre pool en implémentant l’interface **_[AsyncConfigurer](https://github.com/spring-projects/spring-framework/blob/v4.0.5.RELEASE/spring-context/src/main/java/org/springframework/scheduling/annotation/AsyncConfigurer.java)_** et sa méthode public Executor getAsyncExecutor()  :

```java
    @Override
    public Executor getAsyncExecutor() {
        log.debug("Creating Async Task Executor");
        ThreadPoolTaskExecutor executor = new ThreadPoolTaskExecutor();
        // to customize with your requirements
        executor.setCorePoolSize(5);
        executor.setMaxPoolSize(40);
        executor.setQueueCapacity(100);
        executor.setThreadNamePrefix("MyExecutor-");
        executor.initialize();
        return executor;
    }

```

Avant de passer à la configuration de la couche présentation, terminons l’initialisation du contexte racine par la mise en place de la sécurité.

## Sécurité

Reposant sur projet **[Spring Security](http://projects.spring.io/spring-security/)**, la configuration de la sécurité applicative est centralisée dans le fichier **_[SecurityConfig](https://github.com/arey/spring-javaconfig-sample/blob/blog/src/main/java/com/javaetmoi/sample/config/SecurityConfig.java)_**. L’annotation **_[@EnableWebMvcSecurity](https://github.com/spring-projects/spring-security/blob/3.2.4.RELEASE/config/src/main/java/org/springframework/security/config/annotation/web/servlet/configuration/EnableWebMvcSecurity.java)_** s’utilise de pair avec la classe abstraite **_[WebSecurityConfigurerAdapter](https://github.com/spring-projects/spring-security/blob/3.2.4.RELEASE/config/src/main/java/org/springframework/security/config/annotation/web/configuration/WebSecurityConfigurerAdapter.java)_**. Cette dernière permet d’activer la configuration par défaut de Spring Security. La redéfinition de certaines méthodes permet de personnaliser la configuration via les classes _AuthenticationManagerBuilder_ , _HttpSecurity_ et _WebSecurity_.

```java
@Configuration
@EnableWebMvcSecurity
public class SecurityConfig extends WebSecurityConfigurerAdapter {

```

Publié sur le blog de Spring, le billet [Spring Security Java Config Preview: Web Security](http://spring.io/blog/2013/07/03/spring-security-java-config-preview-web-security/) explique comment utiliser la syntaxe Java.  
Dans notre exemple, la déclaration du filtre _springSecurityFilterChain_ dans le _web.xml_ permet de rester compatible avec les conteneurs de Servlet 2.5.@

L’un des apports du fichier **_[SecurityConfig](https://github.com/arey/spring-javaconfig-sample/blob/blog/src/main/java/com/javaetmoi/sample/config/SecurityConfig.java)_** réside dans la mise à disposition du **bean authenticatedUserDetails**. Implémentant l’interface _[UserDetails](https://github.com/spring-projects/spring-security/blob/3.2.4.RELEASE/core/src/main/java/org/springframework/security/core/userdetails/UserDetails.java)_ de Spring Security, ce bean permet d’accéder aux données utilisateurs (ex : login, nom, habilitations) de l’utilisateur authentifié. De portée session (spécifiée avec l’annotation **_[@Scope](https://github.com/spring-projects/spring-framework/blob/v4.0.5.RELEASE/spring-context/src/main/java/org/springframework/context/annotation/Scope.java)_**), ce bean peut être injecté dans des beans de scopes différents, par exemple dans les contrôleurs ou les services métiers de portée singleton. Très pratique pour les logs et/ou les données de traçabilité.

```java
    @Bean
    @Scope(value = "session", proxyMode = ScopedProxyMode.TARGET_CLASS)
    public UserDetails authenticatedUserDetails() {
        SecurityContextHolder.getContext().getAuthentication();
        Authentication authentication = SecurityContextHolder.getContext().getAuthentication();
        if (authentication != null) {
            if (authentication instanceof UsernamePasswordAuthenticationToken) {
                return (UserDetails) authentication.getPrincipal();
            }
            if (authentication instanceof RememberMeAuthenticationToken) {
                return (UserDetails) authentication.getPrincipal();
            }
        }
       return null;
    }
```

Remarque : le système d’authentification sur lequel est branchée votre application peut renvoyer des données supplémentaires. Il est alors fréquent d’avoir à spécialiser la classe _[User](https://github.com/spring-projects/spring-security/blob/3.2.4.RELEASE/core/src/main/java/org/springframework/security/core/userdetails/User.java)_ implémentant _[UserDetails](https://github.com/spring-projects/spring-security/blob/3.2.4.RELEASE/core/src/main/java/org/springframework/security/core/userdetails/UserDetails.java)_. Si vous ne définissez pas d’interface sur votre classe _MyUser_, l’utilisation du **_ScopedProxyMode.TARGET\_CLASS_** est requise par Spring pour proxyfier votre classe.

## Couche présentation

La configuration Java de **[Spring MVC](http://docs.spring.io/spring/docs/4.0.5.RELEASE/spring-framework-reference/htmlsingle/#mvc)** ressemble à celle de Spring Security. L’annotation _[@EnableWebMvc](https://github.com/spring-projects/spring-framework/blob/v4.0.5.RELEASE/spring-webmvc/src/main/java/org/springframework/web/servlet/config/annotation/EnableWebMvc.java)_ s’utilise conjointement à la classe abstraite _[WebMvcConfigurerAdapter](https://github.com/spring-projects/spring-framework/blob/v4.0.5.RELEASE/spring-webmvc/src/main/java/org/springframework/web/servlet/config/annotation/WebMvcConfigurerAdapter.java)_. L’application bénéficie d’une configuration par défaut qu’il est possible de personnaliser par redéfinition de méthodes. La classe **_[WebMvcConfig](https://github.com/arey/spring-javaconfig-sample/blob/blog/src/main/java/com/javaetmoi/sample/config/WebMvcConfig.java)_** joue ce rôle :

```java
@Configuration
@EnableWebMvc
@ComponentScan(basePackages = { "com.javaetmoi.sample.web" })
public class WebMvcConfig extends WebMvcConfigurerAdapter {

    private static final int CACHE_PERIOD = 31556926; // one year

    @Autowired
    private RequestMappingHandlerAdapter requestMappingHandlerAdapter;

    @PostConstruct
    public void init() {
        requestMappingHandlerAdapter.setIgnoreDefaultModelOnRedirect(true);
    }

    @Bean
    public ViewResolver viewResolver() {
        // Example: the 'info' view logical name is mapped to the file '/WEB-INF/jsp/info.jsp'
        InternalResourceViewResolver bean = new InternalResourceViewResolver();
        bean.setViewClass(JstlView.class);
        bean.setPrefix("/WEB-INF/jsp/");
        bean.setSuffix(".jsp");
        return bean;
    }

    @Bean(name = "messageSource")
    public ReloadableResourceBundleMessageSource reloadableResourceBundleMessageSource() {
        ReloadableResourceBundleMessageSource messageSource = new ReloadableResourceBundleMessageSource();
        messageSource.setBasenames("classpath:com/javaetmoi/sample/web/messages");
        messageSource.setDefaultEncoding("UTF-8");
        return messageSource;
    }

    @Override
    public void addResourceHandlers(ResourceHandlerRegistry registry) {
        // Static ressources from both WEB-INF and webjars
        registry
            .addResourceHandler("/resources/**")
                .addResourceLocations("/resources/")
                .setCachePeriod(CACHE_PERIOD);
        registry
            .addResourceHandler("/webjars/**")
                .addResourceLocations("classpath:/META-INF/resources/webjars/")
                .setCachePeriod(CACHE_PERIOD);
    }

    @Override
    public void addViewControllers(ViewControllerRegistry registry) {
        registry.addViewController("/about"); // the about page did not required any controller
    }

    @Override
    public void configureDefaultServletHandling(DefaultServletHandlerConfigurer configurer) {
        // Serving static files using the Servlet container's default Servlet.
        configurer.enable();
    }

    @Override
    public void addFormatters(FormatterRegistry formatterRegistry) {
        // add your custom formatters
    }
}

```

En complément de la redéfinition de méthode, il est possible de configurer Spring MVC en paramétrant les beans créés automatiquement par l’annotation _@EnableWebMvc_ et la classe _[DelegatingWebMvcConfiguration](https://github.com/spring-projects/spring-framework/blob/v4.0.5.RELEASE/spring-webmvc/src/main/java/org/springframework/web/servlet/config/annotation/DelegatingWebMvcConfiguration.java)_ qu’elle référence.  
C’est précisément le cas du bean _RequestMappingHandlerAdapter_ qui est paramétré dans _init()_ appelée au chargement du contexte applicatif Spring.  
Pour les nouvelles applications Spring MVC, il est recommandé par Spring de forcer à _true_ le flag **_ignoreDefaultModelOnRedirect_**. Lors de redirection, l'utilisation de l'interface _[RedirectAttributes](https://github.com/spring-projects/spring-framework/blob/v4.0.5.RELEASE/spring-webmvc/src/main/java/org/springframework/web/servlet/mvc/support/RedirectAttributes.java)_ devient alors nécessaire pour spécifier quelle donnée doit être passée à la _[RedirectView](https://github.com/spring-projects/spring-framework/blob/v4.0.5.RELEASE/spring-webmvc/src/main/java/org/springframework/web/servlet/view/RedirectView.java)_.

La configuration donnée en exemple ne donne qu’un aperçu de l’éventail des possibilités de configuration offertes par Spring MVC : choix de la technologie de rendu (ici JSP), accès aux ressources statiques, définition du cache, internationalisation, déclaration des formateurs globaux ...

## Conclusion

En guise de conclusion, voici un tableau récapitulant les avantages et les inconvénients qu’a un développeur Java à passer sur une syntaxe full Java :

**Avantages****Inconvénients**

- Type safe : syntaxe vérifiée à la compilation
- Complétion dans l’IDE sans plugin
- Import Java mettant en évidence les dépendances non présentes
- Refactoring facilité de la configuration
- Ajout de code possible lors de la déclaration de beans (ex : logs)
- Accélère le chargement du contexte applicatif
- Traite la configuration comme du code
- Navigation dans la conf facilitée
- Mixité possible avec la configuration XML
- Plus besoin de connaitre les namespaces XML

- Nouvelle syntaxe à appréhender
- Subtilités à maîtriser : _afterPropertiesSet()_, appels de méthodes annotées avec _@Bean_ qui n’en sont pas

Références :

1. [Manuel de référence Spring Framework 4](http://docs.spring.io/spring/docs/4.0.5.RELEASE/spring-framework-reference/pdf/spring-framework-reference.pdf) (Pivotal)
1. [Spring Java Based Configuration](http://www.tutorialspoint.com/spring/spring_java_based_configuration.htm) (Tutorials Point)
1. [Spring Data, une autre façon d’accéder aux données](http://blog.soat.fr/2014/02/spring-data-une-autre-facon-dacceder-aux-donnees) (So@t)
1. [Spring Security Java Config Preview: Web Security](http://spring.io/blog/2013/07/03/spring-security-java-config-preview-web-security/) (Pivotal)
1. [Spring Java Config 101](http://java.dzone.com/articles/spring-java-config-101-0) (DZone)
1. [Spring Cache](http://blog.zenika.com/index.php?post/2014/06/03/spring-cache) (Zenika)
