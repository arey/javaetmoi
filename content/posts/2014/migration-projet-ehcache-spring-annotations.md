---
_edit_last: "1"
author: admin
categories:
  - spring
date: "2014-12-01T05:53:51+00:00"
thumbnail: wp-content/uploads/2014/05/logo-spring-highres.png
featureImage: wp-content/uploads/2014/05/logo-spring-highres.png
featureImageAlt: "logo-spring-highres"
guid: http://javaetmoi.com/?p=1273
parent_post_id: null
post_id: "1273"
post_views_count: "5308"
summary: |-
  EhCache est sans nul doute le framework open source de gestion de cache applicatif le plus populaire parmi les développeurs Java. Polyvalent, **EhCache** peut être mis en œuvre dans les différentes couches d’une application web :

  - [![logo-spring-highres](http://javaetmoi.com/wp-content/uploads/2014/05/logo-spring-highres-300x225.png)](http://javaetmoi.com/wp-content/uploads/2014/05/logo-spring-highres.png) Persistance : utilisé comme cache de niveau 2 de JPA / Hibernate pour stocker des entités et le résultat des requêtes en base.
  - Service métier : mise en cache du résultat d’un service métier ou d’un appel de web service
  - Présentation : cache de pages ou de fragments de page HTML

  Habitués à gérer la sécurité et les transactions de manière déclarative à l’aide d’annotations, le projet open source [ehcache-spring-annotations](https://code.google.com/p/ehcache-spring-annotations/) a fait le bonheur des développeurs Spring en 2010 en introduisant l’ **annotation @Cacheable**
  Hébergé sur Google Code, ce projet n’est aujourd’hui plus maintenu. Il ne supporte pas Spring 4.x. Rattrapant son retard, la version 3.1 du framework Spring a été enrichi de sa propre annotation @Cacheable. Comme à son habitude, Spring permet de s’abstraire de la solution de cache sous-jacente (ex : ConcurrentMap, EhCache, Guava …) en proposant une API générique. Les débuts de cette API ont été difficiles (cf. SPR-10237 à laquelle j’ai participé). Aujourd’hui mature, implémentant la JSR-107 JCache, il n’y a aucune raison pour ne pas migrer dessus.
  Relativement court **, ce billet explique pas à pas comment migrer de ehcache-spring-annotations vers le support de cache du framework Spring**.

  ![logo-spring-highres](wp-content/uploads/2014/05/logo-spring-highres.png)
tags:
  - ehcache
  - spring-framework
title: Désendettement du projet ehcache-spring-annotations
url: /2014/12/migration-projet-ehcache-spring-annotations/

---
EhCache est sans nul doute le framework open source de gestion de cache applicatif le plus populaire parmi les développeurs Java. Polyvalent, **EhCache** peut être mis en œuvre dans les différentes couches d’une application web :

- [![logo-spring-highres](wp-content/uploads/2014/05/logo-spring-highres.png)](wp-content/uploads/2014/05/logo-spring-highres.png) Persistance : utilisé comme cache de niveau 2 de JPA / Hibernate pour stocker des entités et le résultat des requêtes en base.
- Service métier : mise en cache du résultat d’un service métier ou d’un appel de web service
- Présentation : cache de pages ou de fragments de page HTML

Habitués à gérer la sécurité et les transactions de manière déclarative à l’aide d’annotations, le projet open source [ehcache-spring-annotations](https://code.google.com/p/ehcache-spring-annotations/) a fait le bonheur des développeurs Spring en 2010 en introduisant l’ **annotation @Cacheable**
Hébergé sur Google Code, ce projet n’est aujourd’hui plus maintenu. Il ne supporte pas Spring 4.x. Rattrapant son retard, la version 3.1 du framework Spring a été enrichi de sa propre annotation @Cacheable. Comme à son habitude, Spring permet de s’abstraire de la solution de cache sous-jacente (ex : ConcurrentMap, EhCache, Guava …) en proposant une API générique. Les débuts de cette API ont été difficiles (cf. SPR-10237 à laquelle j’ai participé). Aujourd’hui mature, implémentant la JSR-107 JCache, il n’y a aucune raison pour ne pas migrer dessus.
Relativement court **, ce billet explique pas à pas comment migrer de ehcache-spring-annotations vers le support de cache du framework Spring**.

## Erreur rencontrée

L’utilisation de la directive _<ehcache:annotation-driven />_ avec Spring 4.1 fait échouer le chargement du contexte Spring :

```java
2014-11-27 20:01:04,948  ERROR org.springframework.web.context.ContextLoader [319] - Context initialization failed org.springframework.beans.factory.BeanDefinitionStoreException: Unexpected exception parsing XML document from class path resource [com/javaetmoi/demo/services/applicationContext-cache.xml]; nested exception is java.lang.IllegalArgumentException: 'beanName' must not be empty
```

## Migration

Ce paragraphe dresse les étapes à suivre pour de désendetter du projet [_ehcache-spring-annotations_](http://code.google.com/p/ehcache-spring-annotations/) et utiliser le support offert par les versions 3.1 et supérieures du framework Spring.

### Dépendances

Dans le pom.xml , supprimer la dépendance vers ehcache-spring-annotations :

```xhtml
<dependency>
      <groupId>com.googlecode.ehcache-spring-annotations</groupId>
      <artifactId>ehcache-spring-annotations</artifactId>
      <version>1.2.0</version>
</dependency>
```

Si vous ne l’utilisez pas encore, ajouter la dépendance suivante. Elle contient la fabrique _EhCacheManagerFactoryBean_ que nous utiliserons par la suite.

```xhtml
<dependency>
      <groupId>org.springframework</groupId>
      <artifactId> spring-context-support </artifactId>
   <version>4.1.2.RELEASE </version>
</dependency>
```

Si nécessaire, mettez également à jour votre version d’EhCache. En effet, Spring 4.1 requière EhCache 2.5 ou supérieur.

### Configuration Spring

Plusieurs changements sont à réaliser dans le fichier de configuration XML où est déclaré le cache applicatif.

1\. Commencer par remplacer le **namespace XML** **ehcache** :

Source :

```xhtml
xmlns:ehcache="http://ehcache-spring-annotations.googlecode.com/svn/schema/ehcache-spring"
```

Cible :

```xhtml
xmlns:cache="http://www.springframework.org/schema/cache"
```

2\. Changer ensuite le **xsi:schemaLocation** du namespace

Source :

```xhtml
http://ehcache-spring-annotations.googlecode.com/svn/schema/ehcache-spring http://ehcache-spring-annotations.googlecode.com/svn/schema/ehcache-spring/ehcache-spring-1.0.xsd
```

Cible :

```xhtml
http://www.springframework.org/schema/cache http://www.springframework.org/schema/cache/spring-cache-4.1.xsd
```

3\. Modifier l’activation des annotations

Source : <ehcache:annotation-driven />Cible : <cache:annotation-driven/>

Si vous utilisez la configuration Java, vous pouvez utiliser à la place l’annotation @EnableCaching.
Par défaut, _cacheManager_ est le nom du bean gestionnaire de cache associé aux annotations.

1. Ajouter le bean _cacheManager_ référençant la fabrique de gestionnaire de cache :

```xhtml
<bean id="cacheManager"
    class="org.springframework.cache.ehcache.EhCacheCacheManager">
    <property name="cacheManager" ref="ehcacheManagerFactory"/>
</bean>
```

La déclaration de fabrique _ehcacheManagerFactory_ ne bouge pas :

```xhtml
<bean id="ehcacheManagerFactory" class="org.springframework.cache.ehcache.EhCacheManagerFactoryBean">
    <property name="configLocation" value="classpath:com/javaetmoi/demo/services/ ehcache.xml"/>
    <property name="shared" value="true"/>
</bean>
```

### Refactoring Java

La dernière étape consiste à refactorer les classes Java utilisant les annotations du projet ehcache-spring-annotations :

1. Modifier le package de l'annotation _@Cacheable_ de _com.googlecode.ehcache.annotations_ pàar _org.springframework.cache.annotation_. L'attribut _cacheName_ de la précédente annotation devient _value_. L’annotation standardisée _javax.cache.annotation.CacheResult_ peut également être employée
1. Remplacer l'annotation _@com.googlecode.ehcache.annotations.TriggersRemove_ par _@org.springframework.cache.annotation.CacheEvict_. L'attribut _cacheName_ devient _value_. Et l'attribut _removeAll_ devient _allEntries_. L’annotation standardisée _javax.cache.annotation.CacheRemove_ peut également être employée

## Conclusion

La migration ne pose aucune difficulté technique. L’équivalence des annotations nécessite de consulter la documentation des 2 projets.
Une fois configuré, vous pourrez alors changer de solution de cache sans toucher au code Java. A vous le cache distribué et élastique de GemFire !

Références :

- [Chapitre Cache Abstraction du manuel de reference du framework Spring](http://docs.spring.io/spring/docs/current/spring-framework-reference/htmlsingle/#cache)
- [Comparaison Spring Cache vs ehcache-spring-annotations](http://labs.excilys.com/2011/03/04/cache-de-methode-spring-cache-vs-ehcache-spring-annotations/)
- [Tutorial Spring Cache](http://spring.io/blog/2011/02/23/spring-3-1-m1-cache-abstraction)
