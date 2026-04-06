---
_edit_last: "1"
_mobile_page_template: Modèle par défaut
_monsterinsights_sitenote_active: ""
_monsterinsights_skip_tracking: ""
_wp_page_template: default
author: admin
date: "2012-12-27T15:37:09+00:00"
footnotes: ""
guid: http://javaetmoi.com/?page_id=500
parent_post_id: null
post_id: "500"
post_views_count: "142"
title: Spring
url: /spring/

---
Développant des applications basées sur le framework Spring depuis 2006 et ayant à mon actif 2 certifications Spring, cette page recense les articles les plus pertinents postés sur ce blog.

## Certifications Spring

1. [Core Spring 3.0 Certification Mock Exam](/2012/02/core-spring-3-0-certification-mock-exam/ "Core Spring 3.0 Certification Mock Exam") : examen blanc de 50 questions, en ligne ou au format PDF, permettant de préparer la Certification Core Spring 3.0.
1. [Enterprise Spring Integration Certification Mock Exam](/2012/10/enterprise-spring-integration-certification-mock-exam/ "Enterprise Spring Integration Certification Mock Exam") : examen blanc permettant de préparer la certification Enterprise Integration with Spring (EIwS 1.x). Au programme, 25 questions réparties sur les thématiques Web Services, REST, Remoting, JMS, Transaction, Spring Batch et Spring Integration.
1. [Certified Spring Enterprise Integration Specialist Study Notes](/2012/09/certified-spring-enterprise-integration-specialist-study-notes/ "Certified Spring Enterprise Integration Specialist Study Notes"): guide de révision permettant de préparer la certification Spring Enterprise Integration Specialist. Les sujets couverts sont Spring Batch, Spring Integration, Spring Remoting, Spring WS, Srping REST, Spring JMS et les transactions XA.

## Spring Batch

1. [Parallélisation de traitements batchs](/2012/12/parallelisation-de-traitements-batchs-spring-batch/ "Parallélisation de traitements batchs") : partant de l’expérience acquise sur un batch indexant des données dans le moteur de recherche Elasticsearch , cet article explique pas à pas comment mettre en œuvre 2 des techniques de parallélisationset de partitionnement proposées nativement par Spring Batch.

1. [Spring Batch s’auto-nettoie](/2012/06/sprint-batch-sauto-nettoie/ "Spring Batch s’auto-nettoie") : tasklet permettant de nettoyer l'historique Spring Batch.
1. [Indexation Elasticsearch avec Spring Batch](/2013/11/musicbrainz-elasticsearch-angularjs-openshift/ "Elastifiez la base MusicBrainz sur OpenShift") : l’indexation de la base de données musicale MusicBrainz illustre l’utilisation de tasklets de suppression, de création et de configuration d’un index Elasticsearch. Reader JDBC, processor et writer Elasticsearch sont également mis à l’épreuve dans une tasklet de type chunk.
1. [Etude de cas Spring Batch](/2015/02/worskshop-etudes-de-cas-spring-batch/): support de présentation d'un retour d'expérience sur la migration d'un batch existant vers Spring Batch.

## Spring Boot

1. [Introduction à Spring Boot](/2016/10/introduction-a-spring-boot/) : slides présentant les grands principes de Spring Boot., démystifiant le fonctionnement de l’auto-configuration puis montrant comment Spring Boot permet de simplifier encore davantage les tests.
1. [Migrer vers Spring Boot](/2016/08/migrer-vers-spring-boot/) : présente les différentes étapes qui ont été nécessaires pour migrer l'application démo Spring Petclinic de Spring Framework vers Spring Boot.
1. [Migration Spring MVC vers Spring WebFlux](/2017/12/migration-spring-web-mvc-vers-spring-webflux/) : étude de cas de la migration d'une application démo basée sur Spring Boot 2
1. [Générateur de squelette d’application basé sur Spring Initializr](/2022/07/generateur-de-squelette-dapplication-base-sur-spring-initializr/) : explique comment créer une version spécialisée de Spring Initializr en prenant pour exemple la configuration du openapi-generator-maven-plugin

## Spring MVC

1. [Validation HTML 5 avec Spring MVC et Bean Validation](/2014/09/validation-html-5-avec-spring-mvc-et-bean-validation/ "Validation HTML 5 avec Spring MVC et Bean Validation") : explique comment étendre le tag JSP _InputTag_ de Spring MVC pour lui faire générer du code HTML 5 de validation de formulaires côté navigateur à partir des contraintes Bean Validation (JSR 330)
1. [Démystifier l’annotation @SessionAttributes de Spring MVC](/2014/10/annotation-sessionattributes-modelattribute-spring-mvc/ "Démystifier l’annotation @SessionAttributes de Spring MVC") : couplée à l'annotation _@ModelAttribute_, _@SessionAttributes_ permet de simuler une portée conversation. Définition d'un modèle, tests unitaires et libération de la mémoire sont expliqués.

## Spring Cloud

1. [Architecture Microservices avec Spring Cloud](/2018/10/architecture-microservices-avec-spring-cloud/) : découvrez comment bâtir une architecture microservices avec Spring Cloud, Netflix OSS, Zipkin et Docker.
1. [Désendettement de Spring Cloud Netflix](/2019/11/desendettement-de-spring-cloud-netflix/) : retour d'expérience sur le désendettement de Spring Cloud Netflix : migration de Zuul 1 vers Spring Cloud Gateway, de Ribbon vers Spring Cloud Loadbalancer et de Hystrix vers Spring Cloud Circuit Breaker / Resilience4j.

## Spring Framework

1. [Configuration de Spring en Java](/2014/06/spring-framework-java-configuration/ "Configurez Spring en Java") : explique comment configurer le contexte applicatif d'une application Spring avec le langage Java, sans  XML. Les annotations @Configuration, @Bean, @Import, @ComponentScan, @Scope et @EnableXXX y sont décrites. Une application démo et un test unitaire basés sur Spring MVC, Spring Security, Spring Data JPA et Hibernate illustre l'article.
1. [Architecture d'un moteur d'indexation](/2013/02/architecture-middle-indexation-elasticsearch/ "Architecture d’un middle d’indexation") : décrit l’architecture mise en œuvre pour indexer des données dans Elasticsearch met à l’épreuve Spring AOP pour intercepter les mises à jour des données et Spring Integration pour les indexer en temps réel.

1. [DbSetup, une alternative à DbUnit](/2013/09/dbsetup-spring-test-vs-dbunit/ "DbSetup, une alternative à DbUnit") : présente quelles sont les facilités qu'offre le framework DbSetup pour alimenter une base de données et montre comment l'intégrer avec Spring Test, notamment en utilisant le rollback pattern.
1. [Support du VFS 2 de JBoss 5 dans Spring 4](/2014/04/support-vfs2-jboss5-spring4/ "Support du VFS 2 de JBoss 5 dans Spring 4") : présentation du projet [spring4-vfs2-suppor](https://github.com/arey/spring4-vfs2-support/) t permettant de déployer une application basée sur Spring Framework 4.0 dans un JBoss AS 5 ou un JBoss 5.x EAP.

1. [Modern Entreprise Java  Architecture with Spring 4.1](/2015/04/18-prises-de-notes-a-devoxx-france-2015/) : prise de note de la conférence donnée par Juergen Hoeler lors de Devoxx France 2015 sur l'état de l'art des applications basées sur Spring et les nouveautés de Spring Framework 4.0 et 4.1.
1. [Désendettement du projet ehcache-spring-annotations](/2014/12/migration-projet-ehcache-spring-annotations/) : guide de migration du projet ehcache-spring-annotations vers le support de cache du framework Spring.
1. [L'offre Spring et les bases](/2014/11/workshop-spring-1-offre-spring-et-bases/) : support de présentation d'un workshop zoomant sur la richesse du [portfolio Spring](http://spring.io/projects) et introduisant aux fondamentaux de Spring Framework.

## Spring Petclinic

1. [Découvrez les forks de Spring Petclinic :](/2016/12/les-forks-de-spring-petclinic/) cet article commence par présenter techniquement l'application démo Spring Petclinic puis dresse un panorama des forks regroupés dans l'organisation GitHub Spring Petclinic : React, AngularJS, Microservices avec Spring Boot, plain old Spring Framework ...
1. [Image Docker pour Spring Boot Petclinic](/2016/11/image-docker-pour-spring-boot-petclinic/): explique comment construire une image Docker de Spring Petclinic à l'aide du plugin pour Maven docker-maven-plugin développé par l’équipe de Spotify.
1. [Découvrir Kotlin en migrant une webapp Spring Boot](/2017/09/migrez-application-java-spring-boot-vers-kotlin/) : guide de migration de l'application démo Spring Petclinic de Java vers Kotlin.
1. [Intégrer un Chatbot dans une webapp Java avec LangChain4j](/2024/11/integrer-un-chatbot-dans-une-webapp-java-avec-langchain4j/) : guide d'intégration étape par étape d'un assistant virtuel dans une application de gestion Java à l'aide du framework LangChain4j, de son starter Spring Boot et des LLM OpenAI et Azure OpenAI.
