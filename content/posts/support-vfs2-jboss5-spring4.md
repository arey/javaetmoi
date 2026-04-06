---
_edit_last: "1"
author: admin
categories:
  - spring
date: "2014-04-01T04:50:09+00:00"
guid: http://javaetmoi.com/?p=1032
parent_post_id: null
post_id: "1032"
post_views_count: "13380"
summary: |-
  Ce billet solutionne un problème rencontré lors de la **montée de version du famework Spring**  de la version 3.2 à la **version** **4.0**. En effet, le déploiement d’une application sous **JBoss 5.1 EAP** échouait dès l’initialisation du contexte Spring. Plus précisément, une exception était levée lorsque Spring scanne le classpath à la recherche de beans Spring annotés par les annotations  @Repository, @Service, @Controller …{{ double-space-with-newline }}Comme le montre la pile d’appel complète ci-dessous, l’exception **java.lang.ClassNotFoundException: org.jboss.vfs.VFS** est encapsulée dans l’exception **java.lang.IllegalStateException: Could not detect JBoss VFS infrastructure**

  Ce problème ne m’était initialement pas apparu lors des développements sous Eclipse avec le plugin JBoss Tools pour WTP : Spring n’a aucun mai à trouver les beans d’un WAR ou d’un EAR explosé. Cette erreur s’est manifestée  lors du déploiement manuel de l’EAR dans le répertoire deploy de JBoss puis du démarrage du serveur par la commande run.bat.{{ double-space-with-newline }}
tags:
  - bug
  - jboss
  - spring-framework
title: Support du VFS 2 de JBoss 5 dans Spring 4
url: /2014/04/support-vfs2-jboss5-spring4/

---
{{< figure src="/wp-content/uploads/2014/04/logo-spring-framework.png" alt="logo-spring-framework" caption="logo-spring-framework" >}}

Ce billet solutionne un problème rencontré lors de la **montée de version du famework Spring**  de la version 3.2 à la **version** **4.0**. En effet, le déploiement d’une application sous **JBoss 5.1 EAP** échouait dès l’initialisation du contexte Spring. Plus précisément, une exception était levée lorsque Spring scanne le classpath à la recherche de beans Spring annotés par les annotations  @Repository, @Service, @Controller …  
Comme le montre la pile d’appel complète ci-dessous, l’exception **java.lang.ClassNotFoundException: org.jboss.vfs.VFS** est encapsulée dans l’exception **java.lang.IllegalStateException: Could not detect JBoss VFS infrastructure**

Ce problème ne m’était initialement pas apparu lors des développements sous Eclipse avec le plugin JBoss Tools pour WTP : Spring n’a aucun mai à trouver les beans d’un WAR ou d’un EAR explosé. Cette erreur s’est manifestée  lors du déploiement manuel de l’EAR dans le répertoire deploy de JBoss puis du démarrage du serveur par la commande run.bat.  

```java
14:01:54,811 INFO  [STDOUT] 14:01:54.811 | ERROR | Context initialization failed
	| org.springframework.web.context.ContextLoader.initWebApplicationContext(ContextLoader.java:336)
java.lang.ExceptionInInitializerError: null
        at org.springframework.core.io.support.PathMatchingResourcePatternResolver$VfsResourceMatchingDelegate.findMatchingResources(PathMatchingResourcePatternResolver.java:652) ~[spring-core-4.0.2.RELEASE.jar:4.0.2.RELEASE]
        at org.springframework.core.io.support.PathMatchingResourcePatternResolver.findPathMatchingResources(PathMatchingResourcePatternResolver.java:347) ~[spring-core-4.0.2.RELEASE.jar:4.0.2.RELEASE]
        at org.springframework.core.io.support.PathMatchingResourcePatternResolver.getResources(PathMatchingResourcePatternResolver.java:269) ~[spring-core-4.0.2.RELEASE.jar:4.0.2.RELEASE]
        at org.springframework.context.support.AbstractApplicationContext.getResources(AbstractApplicationContext.java:1170) ~[spring-context-4.0.2.RELEASE.jar:4.0.2.RELEASE]
        at org.springframework.context.annotation.ClassPathScanningCandidateComponentProvider.findCandidateComponents(ClassPathScanningCandidateComponentProvider.java:268) ~[spring-context-4.0.2.RELEASE.jar:4.0.2.RELEASE]
        at org.springframework.context.annotation.ClassPathBeanDefinitionScanner.doScan(ClassPathBeanDefinitionScanner.java:242) ~[spring-context-4.0.2.RELEASE.jar:4.0.2.RELEASE]
        at org.springframework.context.annotation.ComponentScanAnnotationParser.parse(ComponentScanAnnotationParser.java:134) ~[spring-context-4.0.2.RELEASE.jar:4.0.2.RELEASE]
        at org.springframework.context.annotation.ConfigurationClassParser.doProcessConfigurationClass(ConfigurationClassParser.java:236) ~[spring-context-4.0.2.RELEASE.jar:4.0.2.RELEASE]
        at org.springframework.context.annotation.ConfigurationClassParser.processConfigurationClass(ConfigurationClassParser.java:205) ~[spring-context-4.0.2.RELEASE.jar:4.0.2.RELEASE]
        at org.springframework.context.annotation.ConfigurationClassParser.processImports(ConfigurationClassParser.java:426) ~[spring-context-4.0.2.RELEASE.jar:4.0.2.RELEASE]
        at org.springframework.context.annotation.ConfigurationClassParser.doProcessConfigurationClass(ConfigurationClassParser.java:248) ~[spring-context-4.0.2.RELEASE.jar:4.0.2.RELEASE]
        at org.springframework.context.annotation.ConfigurationClassParser.processConfigurationClass(ConfigurationClassParser.java:205) ~[spring-context-4.0.2.RELEASE.jar:4.0.2.RELEASE]
        at org.springframework.context.annotation.ConfigurationClassParser.parse(ConfigurationClassParser.java:182) ~[spring-context-4.0.2.RELEASE.jar:4.0.2.RELEASE]
        at org.springframework.context.annotation.ConfigurationClassParser.parse(ConfigurationClassParser.java:152) ~[spring-context-4.0.2.RELEASE.jar:4.0.2.RELEASE]
        at org.springframework.context.annotation.ConfigurationClassPostProcessor.processConfigBeanDefinitions(ConfigurationClassPostProcessor.java:299) ~[spring-context-4.0.2.RELEASE.jar:4.0.2.RELEASE]
        at org.springframework.context.annotation.ConfigurationClassPostProcessor.postProcessBeanDefinitionRegistry(ConfigurationClassPostProcessor.java:243) ~[spring-context-4.0.2.RELEASE.jar:4.0.2.RELEASE]
        at org.springframework.context.support.PostProcessorRegistrationDelegate.invokeBeanDefinitionRegistryPostProcessors(PostProcessorRegistrationDelegate.java:254) ~[spring-context-4.0.2.RELEASE.jar:4.0.2.RELEASE]
        at org.springframework.context.support.PostProcessorRegistrationDelegate.invokeBeanFactoryPostProcessors(PostProcessorRegistrationDelegate.java:94) ~[spring-context-4.0.2.RELEASE.jar:4.0.2.RELEASE]
        at org.springframework.context.support.AbstractApplicationContext.invokeBeanFactoryPostProcessors(AbstractApplicationContext.java:609) ~[spring-context-4.0.2.RELEASE.jar:4.0.2.RELEASE]
        at org.springframework.context.support.AbstractApplicationContext.refresh(AbstractApplicationContext.java:464) ~[spring-context-4.0.2.RELEASE.jar:4.0.2.RELEASE]
        at org.springframework.web.context.ContextLoader.configureAndRefreshWebApplicationContext(ContextLoader.java:403) ~[spring-web-4.0.2.RELEASE.jar:4.0.2.RELEASE]
        at org.springframework.web.context.ContextLoader.initWebApplicationContext(ContextLoader.java:306) ~[spring-web-4.0.2.RELEASE.jar:4.0.2.RELEASE]
        at org.springframework.web.context.ContextLoaderListener.contextInitialized(ContextLoaderListener.java:106) [spring-web-4.0.2.RELEASE.jar:4.0.2.RELEASE]
				... X common frames omitted
        at java.lang.Thread.run(Thread.java:662) [na:1.6.0_26]
Caused by: java.lang.IllegalStateException: Could not detect JBoss VFS infrastructure
        at org.springframework.core.io.VfsUtils.<clinit>(VfsUtils.java:92) ~[spring-core-4.0.2.RELEASE.jar:4.0.2.RELEASE]
        ... 93 common frames omitted
Caused by: java.lang.ClassNotFoundException: org.jboss.vfs.VFS from BaseClassLoader@1269ac3{vfszip:/C:/dev/servers/jboss-eap-5.1/server/default/deploy/myapp-ear-1.0.0-SNAPSHOT.ear/}
        at org.jboss.classloader.spi.base.BaseClassLoader.loadClass(BaseClassLoader.java:477) ~[jboss-classloader.jar:2.0.9.GA]
        at java.lang.ClassLoader.loadClass(ClassLoader.java:247) ~[na:1.6.0_26]
        at org.springframework.core.io.VfsUtils.<clinit>(VfsUtils.java:69) ~[spring-core-4.0.2.RELEASE.jar:4.0.2.RELEASE]
        ... 93 common frames omitted
14:01:55,014 ERROR [StandardContext] Error listenerStart
```

## Diagnostic

Les versions communautaires JBoss AS 5 et commerciales JBoss 5 EAP s’appuient toutes les deux sur la version 2 du [Virtual File System](http://java.dzone.com/news/jboss-virtual-file-system).  Or, comme l’atteste le [commit de Juergen Hoeller](https://github.com/spring-projects/spring-framework/commit/ca194261a42a0a4f0c8bdc36f447e1029a7d2e3e) dans GitHub, le **support de VFS 2 a été volontairement retiré de Spring 4**.

Comme je m’y attendais, je ne suis pas le seul développeur à  regretter cet abandon. Le [forum de Spring](http://forum.spring.io/forum/spring-projects/container/744173-spring-4-doesn-t-support-vfs2) en donne une idée. Qui plus est, la documentation de Spring n’est pas tout à fait à jour à ce sujet. J’ai soumis la [pull request](https://github.com/spring-projects/spring-framework/pull/502) concernant la JavaDoc de la classe _VfsResource_.

## Réactivation de VFS2

Rétablir le support de VFS 2 dans Spring 4 n’a pas été très compliqué. J’ai tout simplement dupliqué le code de la classe **[VfsUtils](https://fisheye.springsource.org/browse/~br=3.2.x/spring-framework/spring-core/src/main/java/org/springframework/core/io/VfsUtils.java?hb=true) de Spring 3.2** dans la classe **[Vfs2Utils](https://github.com/arey/spring4-vfs2-support/blob/master/src/main/java/com/javaetmoi/core/spring/vfs/Vfs2Utils.java)**. Il a ensuite été nécessaire d’ [implémenter l’interface _ResourcePatternResolver_](http://docs.spring.io/spring/docs/3.2.8.RELEASE/javadoc-api/org/springframework/core/io/support/ResourcePatternResolver.html) et de câbler cette implémentation dans les classes responsables du chargement du contexte applicatif Spring (qui héritent de la classe _AbstractApplicationContext_).

Pour celles et ceux que cela intéresserait, j’ai publié ces quelques classes dans le projet **[spring4-vfs2-support](https://github.com/arey/spring4-vfs2-support/)** sous GitHub. Les 2 classes _[JBoss5XmlWebApplicationContext](https://github.com/arey/spring4-vfs2-support/blob/master/src/main/java/com/javaetmoi/core/spring/JBoss5XmlWebApplicationContext.java)_ et _[JBoss5AnnotationConfigWebApplicationContext](https://github.com/arey/spring4-vfs2-support/blob/master/src/main/java/com/javaetmoi/core/spring/JBoss5AnnotationConfigWebApplicationContext.java)_ en sont les points d’entrée.

## Utilisation

Pour utiliser Spring 4 avec JBoss 5, vous pouvez copier/coller le code du repo [spring4-vfs2-support](https://github.com/arey/spring4-vfs2-support/) ou bien tirer la dépendance maven suivante :

```xhtml
<dependency>
  <groupId>com.javaetmoi.core</groupId>
  <artifactId>javaetmoi-spring4-vfs2-support</artifactId>
  <version>1.1.0</version>
</dependency>
```

L’artefact javaetmoi-spring4-vfs2-support est publié sur un repository maven hébergé par CloudBees. Ce repo doit être référencé dans votre proxy Maven d’Entreprise (ex : Nexus) ou bien déclaré dans votre pom.xml au niveau de la balise <repositories> :

```xhtml
<repository>
  <id>javaetmoi-maven-release</id>
  <releases>
    <enabled>true</enabled>
  </releases>
  <name>Java et Moi Maven RELEASE Repository</name>
  <url>http://repository-javaetmoi.forge.cloudbees.com/release/</url>
</repository>
```

Une fois la configuration Maven terminée, il reste à indiquer à Spring quelle classe il doit utiliser pour charger sa configuration. Exemple de configuration du listener _ContextLoaderListener_ dans le _web.xml_ :

```xhtml
<context-param>
  <param-name>contextClass</param-name>
  <param-value> com.javaetmoi.core.spring.JBoss5XmlWebApplicationContext</param-value>
</context-param>
<listener>
    <listener-class>org.springframework.web.context.ContextLoaderListener</listener-class>
</listener>
```

## Conclusion

A l’exception de celles basées sur la spécification Servlet 3.0, vous pouvez souhaiter la bienvenues à toutes [les nouveautés de Spring 4](https://spring.io/blog/2013/12/12/announcing-spring-framework-4-0-ga-release).
