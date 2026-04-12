---
_edit_last: "1"
_wp_old_slug: utilisez-hibernate-4-3-sous-jboss-5-avec-spring-4
author: admin
categories:
  - orm
date: "2014-04-10T18:50:07+00:00"
thumbnail: wp-content/uploads/2014/04/logo-hibernate.png
featureImage: wp-content/uploads/2014/04/logo-hibernate.png
featureImageAlt: "logo-hibernate"
guid: http://javaetmoi.com/?p=1051
parent_post_id: null
post_id: "1051"
post_views_count: "5105"
summary: |-
  Dans mon [précédent billet](http://javaetmoi.com/2014/04/support-vfs2-jboss5-spring4/ "Support du VFS 2 de JBoss 5 dans Spring 4"), je vous expliquais comment réintroduire le support de VFS 2 abandonné dans **Spring Framework 4.0**. Et ceci, dans l’optique de pouvoir déployer mon application dans le serveur d’application **JBoss 5.1 EAP**.<br>Outre ce problème survenant lors de la détection de beans Spring dans le classpath, la montée de version de Spring 3.2 à Spring 4 a révélé un autre problème lié au format VFS de JBoss.  Cette fois-ci, c’est le framework **Hibernate 4.3** qui n’arrive pas à détecter les entités JPA du classpath.

  Certifié conforme à Java EE 5, JBoss 5.1 EAP utilise Hibernate 3.3 comme implémentation de JPA 1.  Dans mon cas, Hibernate 4.3 est utilisé en mode standalone et est donc directement embarqué dans les librairies de mon EAR. La configuration **JPA 2.1** est assurée par le support JPA offert par Spring, et plus particulièrement par la classe _[LocalContainerEntityManagerFactoryBean](https://github.com/spring-projects/spring-framework/blob/v4.0.3.RELEASE/spring-orm/src/main/java/org/springframework/orm/jpa/LocalContainerEntityManagerFactoryBean.java)_.<br>

  ![logo-hibernate](wp-content/uploads/2014/04/logo-hibernate.png)
tags:
  - bug
  - hibernate
  - jpa
  - spring-framework
title: Utilisez Hibernate 4.3 sous JBoss 5 avec Spring 4
url: /2014/04/hibernate4-sous-jboss5-avec-spring4/

---
{{< figure src="wp-content/uploads/2014/04/logo-hibernate.png" alt="logo-hibernate" caption="logo-hibernate" >}}

Dans mon [précédent billet](/2014/04/support-vfs2-jboss5-spring4/ "Support du VFS 2 de JBoss 5 dans Spring 4"), je vous expliquais comment réintroduire le support de VFS 2 abandonné dans **Spring Framework 4.0**. Et ceci, dans l’optique de pouvoir déployer mon application dans le serveur d’application **JBoss 5.1 EAP**.  
Outre ce problème survenant lors de la détection de beans Spring dans le classpath, la montée de version de Spring 3.2 à Spring 4 a révélé un autre problème lié au format VFS de JBoss.  Cette fois-ci, c’est le framework **Hibernate 4.3** qui n’arrive pas à détecter les entités JPA du classpath.

Certifié conforme à Java EE 5, JBoss 5.1 EAP utilise Hibernate 3.3 comme implémentation de JPA 1.  Dans mon cas, Hibernate 4.3 est utilisé en mode standalone et est donc directement embarqué dans les librairies de mon EAR. La configuration **JPA 2.1** est assurée par le support JPA offert par Spring, et plus particulièrement par la classe _[LocalContainerEntityManagerFactoryBean](https://github.com/spring-projects/spring-framework/blob/v4.0.3.RELEASE/spring-orm/src/main/java/org/springframework/orm/jpa/LocalContainerEntityManagerFactoryBean.java)_.  

## Problème rencontré

Au démarrage de l’application, Hibernate s’appuie sur l’interface _[Scanner](https://github.com/hibernate/hibernate-orm/blob/4.3.5.Final/hibernate-entitymanager/src/main/java/org/hibernate/jpa/boot/scan/spi/Scanner.java)_ pour détecter les classes, les packages et les ressources d’une Unité de Persistance JPA. L’implémentation _[StandardScanner](https://github.com/hibernate/hibernate-orm/blob/4.3.5.Final/hibernate-entitymanager/src/main/java/org/hibernate/jpa/boot/scan/internal/StandardScanner.java)_ délègue le parcours du WAR à la classe _[StandardArchiveDescriptorFactory](https://github.com/hibernate/hibernate-orm/blob/4.3.5.Final/hibernate-entitymanager/src/main/java/org/hibernate/jpa/boot/archive/internal/StandardArchiveDescriptorFactory.java)_. Ligne 72 de cette dernière, l’appel à la méthode file.exists() échoue sur le chemin « vfszip:/C:/jboss-eap-5.1/server/default/deploy/myapp-ear-1.0.0-SNAPSHOT.ear/myapp-war-1.0.0-SNAPSHOT.war/WEB-INF/classes/ ». Une _IllegalArgumentException_ est levée :

```java
21:51:24,472 INFO  [STDOUT] 21:51:24.472 |  INFO |  | Building JPA container EntityManagerFactory for persistence unit 'persistenceUnit'| org.springframework.orm.jpa.LocalContainerEntityManagerFactoryB ean.createNativeEntityManagerFactory(LocalContainerEntityManagerFactoryBean.java:332)
21:51:24,550 INFO  [STDOUT] 21:51:24.550 |  INFO |  | HHH000204: Processing PersistenceUnitInfo [ name: persistenceUnit ...]            | org.hibernate.jpa.internal.util.LogHelper.logPersistenceUnitInformation(LogHelper.java:46)
21:51:24,754 INFO  [STDOUT] 21:51:24.754 |  INFO |  | HHH000412: Hibernate Core {4.3.4.Final}                                           | org.hibernate.Version.logVersion(Version.java:54)
21:51:24,754 INFO  [STDOUT] 21:51:24.754 |  INFO |  | HHH000206: hibernate.properties not found                                         | org.hibernate.cfg.Environment.<clinit>(Environment.java:239)
21:51:24,769 INFO  [STDOUT] 21:51:24.754 |  INFO |  | HHH000021: Bytecode provider name : javassist                                     | org.hibernate.cfg.Environment.buildBytecodeProvider(Environment.java:346)
21:51:33,848 INFO  [STDOUT] 21:51:33.848 | ERROR |  | Context initialization failed                                                     | org.springframework.web.context.ContextLoader.initWebApplicationContext(ContextLoader.java:331)
org.springframework.beans.factory.BeanCreationException: Error creating bean with name 'entityManagerFactoryBean' defined in class com.javaetmoi.sample.config.InfrastructureConfig: Invocation of init method failed; nested exception is java.lang.IllegalArgumentException: File [/C:/jboss-eap-5.1/server/default/deploy/myapp-ear-1.0.0-SNAPSHOT.ear/myapp-war-1.0.0-SNAPSHOT.war/WEB-INF/classes/] referenced by given URL [vfszip:/C:/jboss-eap-5.1/server/default/deploy/myapp-ear-1.0.0-SNAPSHOT.ear/myapp-war-1.0.0-SNAPSHOT.war/WEB-INF/classes/] does not exist
        at org.springframework.beans.factory.support.AbstractAutowireCapableBeanFactory.initializeBean(AbstractAutowireCapableBeanFactory.java:1553) ~[spring-beans-4.0.2.RELEASE.jar:4.0.2.RELEASE]
        at org.springframework.beans.factory.support.AbstractAutowireCapableBeanFactory.doCreateBean(AbstractAutowireCapableBeanFactory.java:539) ~[spring-beans-4.0.2.RELEASE.jar:4.0.2.RELEASE]
        at org.springframework.beans.factory.support.AbstractAutowireCapableBeanFactory.createBean(AbstractAutowireCapableBeanFactory.java:475) ~[spring-beans-4.0.2.RELEASE.jar:4.0.2.RELEASE]
        at org.springframework.beans.factory.support.AbstractBeanFactory$1.getObject(AbstractBeanFactory.java:304) ~[spring-beans-4.0.2.RELEASE.jar:4.0.2.RELEASE]
        at org.springframework.beans.factory.support.DefaultSingletonBeanRegistry.getSingleton(DefaultSingletonBeanRegistry.java:228) ~[spring-beans-4.0.2.RELEASE.jar:4.0.2.RELEASE]
        at org.springframework.beans.factory.support.AbstractBeanFactory.doGetBean(AbstractBeanFactory.java:300) ~[spring-beans-4.0.2.RELEASE.jar:4.0.2.RELEASE]
        at org.springframework.beans.factory.support.AbstractBeanFactory.getBean(AbstractBeanFactory.java:195) ~[spring-beans-4.0.2.RELEASE.jar:4.0.2.RELEASE]
        at org.springframework.context.support.AbstractApplicationContext.getBean(AbstractApplicationContext.java:973) ~[spring-context-4.0.2.RELEASE.jar:4.0.2.RELEASE]
        at org.springframework.context.support.AbstractApplicationContext.finishBeanFactoryInitialization(AbstractApplicationContext.java:750) ~[spring-context-4.0.2.RELEASE.jar:4.0.2.RELEASE]
        at org.springframework.context.support.AbstractApplicationContext.refresh(AbstractApplicationContext.java:482) ~[spring-context-4.0.2.RELEASE.jar:4.0.2.RELEASE]
        at org.springframework.web.context.ContextLoader.configureAndRefreshWebApplicationContext(ContextLoader.java:403) ~[spring-web-4.0.2.RELEASE.jar:4.0.2.RELEASE]
        at org.springframework.web.context.ContextLoader.initWebApplicationContext(ContextLoader.java:306) ~[spring-web-4.0.2.RELEASE.jar:4.0.2.RELEASE] at org.springframework.web.context.ContextLoaderListener.contextInitialized(ContextLoaderListener.java:106) [spring-web-4.0.2.RELEASE.jar:4.0.2.RELEASE]
        at org.apache.catalina.core.StandardContext.listenerStart(StandardContext.java:3910) [jbossweb.jar!/:na]
        at org.apache.catalina.core.StandardContext.start(StandardContext.java:4389) [jbossweb.jar!/:na]
        at org.jboss.web.tomcat.service.deployers.TomcatDeployment.performDeployInternal(TomcatDeployment.java:321) [jboss-web-service.jar!/:5.1.1 (build: SVNTag=JBPAPP_5_1_1 date=201105171607)]
        ...
        at org.jboss.Main$1.run(Main.java:556) [run.jar:5.1.1 (build: SVNTag=JBPAPP_5_1_1 date=201105171607)]
        at java.lang.Thread.run(Thread.java:662) [na:1.6.0_26]
Caused by: java.lang.IllegalArgumentException: File [/C:/jboss-eap-5.1/server/default/deploy/myapp-ear-1.0.0-SNAPSHOT.ear/myapp-war-1.0.0-SNAPSHOT.war/WEB-INF/classes/] referenced by given URL [vfszip:/C:/jboss-eap-5.1/server/default/deploy/myapp-ear-1.0.0-SNAPSHOT.ear/myapp-war-1.0.0-SNAPSHOT.war/WEB-INF/classes/] does not exist at org.hibernate.jpa.boot.archive.internal.StandardArchiveDescriptorFactory.buildArchiveDescriptor(StandardArchiveDescriptorFactory.java:73) ~[hibernate-entitymanager-4.3.4.Final.jar:4.3.4.Final]
        at org.hibernate.jpa.boot.archive.internal.StandardArchiveDescriptorFactory.buildArchiveDescriptor(StandardArchiveDescriptorFactory.java:48) ~[hibernate-entitymanager-4.3.4.Final.jar:4.3.4.Final]
        at org.hibernate.jpa.boot.scan.spi.AbstractScannerImpl.buildArchiveDescriptor(AbstractScannerImpl.java:95) ~[hibernate-entitymanager-4.3.4.Final.jar:4.3.4.Final]
        at org.hibernate.jpa.boot.scan.spi.AbstractScannerImpl.scan(AbstractScannerImpl.java:70) ~[hibernate-entitymanager-4.3.4.Final.jar:4.3.4.Final]
        at org.hibernate.jpa.boot.internal.EntityManagerFactoryBuilderImpl.scan(EntityManagerFactoryBuilderImpl.java:723) ~[hibernate-entitymanager-4.3.4.Final.jar:4.3.4.Final]
        at org.hibernate.jpa.boot.internal.EntityManagerFactoryBuilderImpl.<init>(EntityManagerFactoryBuilderImpl.java:219) ~[hibernate-entitymanager-4.3.4.Finl.jar:4.3.4.Final]
        at org.hibernate.jpa.boot.internal.EntityManagerFactoryBuilderImpl.<init>(EntityManagerFactoryBuilderImpl.java:186) ~[hibernate-entitymanager-4.3.4.Final.jar:4.3.4.Final]
        at org.hibernate.jpa.boot.spi.Bootstrap.getEntityManagerFactoryBuilder(Bootstrap.java:45) ~[hibernate-entitymanager-4.3.4.Final.jar:4.3.4.Final]
        at org.hibernate.jpa.boot.spi.Bootstrap.getEntityManagerFactoryBuilder(Bootstrap.java:57) ~[hibernate-entitymanager-4.3.4.Final.jar:4.3.4.Final]
        at org.hibernate.jpa.HibernatePersistenceProvider.createContainerEntityManagerFactory(HibernatePersistenceProvider.java:150) ~[hibernate-entitymanager-4.3.4.Final.jar:4.3.4.Final]
        at org.springframework.orm.jpa.LocalContainerEntityManagerFactoryBean.createNativeEntityManagerFactory(LocalContainerEntityManagerFactoryBean.java:336)~[spring-orm-4.0.2.RELEASE.jar:4.0.2.RELEASE]
        at org.springframework.orm.jpa.AbstractEntityManagerFactoryBean.afterPropertiesSet(AbstractEntityManagerFactoryBean.java:318) ~[spring-orm-4.0.2.RELEASE.jar:4.0.2.RELEASE]
        at org.springframework.beans.factory.support.AbstractAutowireCapableBeanFactory.invokeInitMethods(AbstractAutowireCapableBeanFactory.java:1612) ~[spring-beans-4.0.2.RELEASE.jar:4.0.2.RELEASE]
        at org.springframework.beans.factory.support.AbstractAutowireCapableBeanFactory.initializeBean(AbstractAutowireCapableBeanFactory.java:1549) ~[spring-beans-4.0.2.RELEASE.jar:4.0.2.RELEASE]
        ... 82 common frames omitted
```

## Solution

Comme précisé en introduction, notre application utilise la fabrique de beans _[LocalContainerEntityManagerFactoryBean](https://github.com/spring-projects/spring-framework/blob/v4.0.3.RELEASE/spring-orm/src/main/java/org/springframework/orm/jpa/LocalContainerEntityManagerFactoryBean.java)_ pour créer l’ _[EntityManagerFactory](http://docs.oracle.com/javaee/6/api/javax/persistence/EntityManagerFactory.html)_ de JPA. Lors de la configuration de ce bean, la méthode _setPackagesToScan_ permet d’indiquer à Spring quel package Java il doit scanner au démarrage de l’application pour détecter les entités JPA. Spring utilise alors le même mécanisme d’auto-détection que pour les beans Spring et scanne tous les JAR du classpath.  
Dans l’exemple ci-desssous, le package _com.javaetmoi.demo.model_ ainsi que tous ses sous-packages sont scannés :

```java
@Bean
public LocalContainerEntityManagerFactoryBean entityManagerFactoryBean() {
    LocalContainerEntityManagerFactoryBean em = new LocalContainerEntityManagerFactoryBean();
    em.setDataSource(dataSource());
    em.setPackagesToScan("com.javaetmoi.persistencedemo.model");

    em.setJpaVendorAdapter(new HibernateJpaVendorAdapter(););
    em.setJpaProperties(additionalProperties());

    return em;
}
```

Le support JPA proposé par Spring fait que le fichier _pesistence.xml_ n’a plus de raison d’être. Et vous l’aurez compris, le scan d’Hibernate ait redondant à celui de Spring. Il peut donc être désactivé.

La classe **[NopScanner](https://gist.github.com/arey/10308277)** disponible sous forme de Gist permet de court-circuiter le scan d’Hibernate :

```java
No-operation Hibernate Scanner
```

Indiquer à Hibernate d’utiliser la classe [NopScanner](https://gist.github.com/arey/10308277) revient à déclarer la propriété Hibernate suivante :  
_hibernate.ejb.resource\_scanner=com.javaetmoi.core.persistence.hibernate.NopScanner_

En utilisant la syntaxe Java, cette propriété peut être ajoutée dans la méthode _additionalProperties()_ utilisée lors de la déclaration du bean _LocalContainerEntityManagerFactoryBean_ dans l’exemple précédent :

```java
 private Properties additionalProperties() {
    return new Properties() {
        {
            setProperty("hibernate.ejb.resource_scanner", "com.javaetmoi.core.persistence.hibernate.NopScanner");
            setProperty("hibernate.dialect",env.getProperty("hibernate.dialect"));
        }
    };
}
```

## Conclusion

La possibilité offerte par JPA de pouvoir être utilisée en dehors d’un conteneur Java EE ainsi que la souplesse du support JPA proposé par le framework Spring font qu’il est possible d’utiliser JPA 2.1 (introduit ans JEE 7) dans un serveur JEE 5.

Ayant utilisé cette approche dans ce billet, je vous donnerai prochainement un exemple complet de configuration Spring en Java d’une application basée sur Spring MVC et JPA. Restez connectés !!
