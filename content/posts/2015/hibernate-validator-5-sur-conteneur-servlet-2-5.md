---
_edit_last: "1"
author: admin
categories:
  - retour-d'expérience
date: "2015-10-01T05:17:30+00:00"
thumbnail: /wp-content/uploads/2015/09/hibernate-validator-logo.png
featureImage: /wp-content/uploads/2015/09/hibernate-validator-logo.png
featureImageAlt: "hibernate-validator-logo"
guid: http://javaetmoi.com/?p=1462
parent_post_id: null
post_id: "1462"
post_views_count: "4654"
summary: |-
  Implémentation de référence de [Bean Validation 1.1](http://beanvalidation.org/), [Hibernate Validator 5.x requière une implémentation d'Unified Expression Language respectant la JSR-341](http://docs.jboss.org/hibernate/validator/5.1/reference/en-US/html/validator-gettingstarted.html#validator-gettingstarted-uel) (correspond aux [**EL 2.2**](https://jcp.org/en/jsr/detail?id=341)).
  EL 2.2 étant apparue avec Java EE 6, il n’est donc pas possible d’utiliser Hibernate Validator 5 dans un serveur d’application Java EE 5 et un conteneur de servlets 2.5. C’est pourquoi [Hibernate Validator 5 ne fonctionne pas avec Tomcat 6](http://hibernate.org/validator/faq/#does-hibernate-validator-5-x-work-with-tomcat-6).

  [![hibernate-validator-logo](http://javaetmoi.com/wp-content/uploads/2015/09/hibernate-validator-logo.png)](http://javaetmoi.com/wp-content/uploads/2015/09/hibernate-validator-logo.png)

  Essayer et vous tomberez au runtime sur l’exception suivante :
  NoSuchMethodError: javax.el.ExpressionFactory.newInstance()Ljavax/el/ExpressionFactory)

  ![hibernate-validator-logo](/wp-content/uploads/2015/09/hibernate-validator-logo.png)
tags:
  - el
  - hibernate-validator
title: Hibernate Validator 5 sur un conteneur de Servlet 2.5
url: /2015/10/hibernate-validator-5-sur-conteneur-servlet-2-5/

---
Implémentation de référence de [Bean Validation 1.1](http://beanvalidation.org/), [Hibernate Validator 5.x requière une implémentation d'Unified Expression Language respectant la JSR-341](http://docs.jboss.org/hibernate/validator/5.1/reference/en-US/html/validator-gettingstarted.html#validator-gettingstarted-uel) (correspond aux [**EL 2.2**](https://jcp.org/en/jsr/detail?id=341)).
EL 2.2 étant apparue avec Java EE 6, il n’est donc pas possible d’utiliser Hibernate Validator 5 dans un serveur d’application Java EE 5 et un conteneur de servlets 2.5. C’est pourquoi [Hibernate Validator 5 ne fonctionne pas avec Tomcat 6](http://hibernate.org/validator/faq/#does-hibernate-validator-5-x-work-with-tomcat-6).

[![hibernate-validator-logo](/wp-content/uploads/2015/09/hibernate-validator-logo.png)](/wp-content/uploads/2015/09/hibernate-validator-logo.png)

Essayer et vous tomberez au runtime sur l’exception suivante :
NoSuchMethodError: javax.el.ExpressionFactory.newInstance()Ljavax/el/ExpressionFactory)

Comme indiqué dans la documentation, embarquer EL 2.2 dans votre WAR ne résout pas le problème et génère ce type d’erreur au runtime :

```java
java.lang.LinkageError: loader constraint violation: when resolving interface method "javax.servlet.jsp.JspApplicationContext.getExpressionFactory()Ljavax/el/ExpressionFactory;" the class loader (instance of org/apache/jasper/servlet/JasperLoader) of the current class, org/apache/jsp/index_jsp, and the class loader (instance of org/apache/catalina/loader/StandardClassLoader) for resolved class, javax/servlet/jsp/JspApplicationContext, have different Class objects for the type javax/el/ExpressionFactory used in the signature
```

Pour profiter des avancées apportées par Bean Validation 1.1, comme par exemple l’ [amélioration du formatage des messages d'erreurs des contraintes](http://beanvalidation.org/1.1/changes/), vous avez le choix entre:

1. Effectuer une montée de version de Tomcat ou de JBoss
1. Utiliser une autre implémentation de Bean Validation 1.1 (personnellement je n’en connais pas)
1. **Patcher Hibernate Validator**.

C’est cette 3ième solution que je compte vous présenter.

## Mise en oeuvre

Pour être tout à fait exact, il ne faudra pas patcher qu’Hibernate Validator. **L’API EL 2.2 et son implémentation** devront également être **patchées**. En effet, afin de faire fonctionner de pair EL 2.1 (pour le conteneur de Servlet) et EL 2.2 (pour Hibernate Validator), le package des classes d’EL 2.2 doit être renommé. A cet effet, le package _javax.el_ pourra par exemple être changé en _com.javaetmoi.fork.javax.el_.
Récupérer le code source de [javax.el 2.2.6](https://svn.java.net/svn/uel~svn/tags/javax.el-2.2.6) et [javaxx.el-api 2.2.6](https://svn.java.net/svn/uel~svn/tags/javax.el-api-2.2.6) depuis le SVN de java.net ne pose guère de difficulté, construire le projet avec Maven non plus.
Une fois les projets importés dans votre IDE, la fonction de refactoring de ce dernier s’occupera de modifier automatiquement les imports.
Vous aurez à éditer les pom.xml et à changer le groupId ou l’artefactId afin de pouvoir dépendre des 2 versions d’EL. Builder les projets et déployer les dans votre repos local ou votre repo d’entreprise.

Patcher **Hibernate Validator** n’est guère plus compliqué. Commencer par forker ou cloner son [repo Github](https://github.com/hibernate/hibernate-validator).
Ensuite, renommer en masse de tous les imports vers le package javax.el.

Le contenu de 2 classes devra être changé manuellement :

**ResourceBundleMessageInterpolator**

```java
ResourceBundleMessageInterpolator.class.getClassLoader().loadClass( "com.javaetmoi.fork.javax.el.ExpressionFactory" );
```

 **ELIgnoringClassLoader**

```java
private final String EL_PACKAGE_PREFIX = "com.javaetmoi.fork.javax.el";
```

Editer le pom.xml. Afin de ne pas confondre ce fork avec l’originalhanger le groupId, l’artefactId et/ou le numéro de version du module hibernate-validator.
Ajouter les dépendances vers l’API et l’implémentation de EL 2.1. Construire le JAR et le déployer. Le tour est joué.

## Conclusion

En une petite heure, vous aurez réussi à faire en sorte qu’Hibernate Validator 5.x soit compatible avec votre conteneur de servlet 2.5 (ou votre serveur d’application JEE 5).
En soit, les adaptations ne sont ni compliquées ni risquées. Se posera la question de devoir les réappliquer lorsque vous voulez monter de version Hibernate Validator ou EL. Un fichier patch ou un fork sous Github permettront de faciliter les mises à jour.
Lors d’un passage à JEE 6 ou à un conteneur de servlet compatible Servlet 3.x, ces versions personnalisés d’EL et d’Hibernate Validator pourront être remplacées peur l’original.
