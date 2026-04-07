---
_edit_last: "1"
author: admin
categories:
  - retour-d'expérience
date: "2014-06-28T16:19:58+00:00"
guid: http://javaetmoi.com/?p=1165
parent_post_id: null
post_id: "1165"
post_views_count: "13664"
summary: |-
  [![JBoss Richfaces Logo](http://javaetmoi.com/wp-content/uploads/2014/06/2014-07-jsf2-richfaces4-dans-jboss5-richfaces-logo-252x300.png)](http://javaetmoi.com/wp-content/uploads/2014/06/2014-07-jsf2-richfaces4-dans-jboss5-richfaces-logo.png) Début 2014, j’ai étudié la faisabilité technique d’une **migration** de **JSF 1.2** **\+ Richfaces 3.3** **vers JSF 2.1 + Richfaces 4.3** sans changer de serveur d’application.
  Notre serveur [JBoss 5.1 EAP](https://access.redhat.com/site/articles/112673#EAP_5) étant certifié **JavaEE 5**, la première difficulté consistait à **désinstaller l’implémentation [Mojarra](https://javaserverfaces.java.net/) de JSF 1.2 embarquée dans JBoss**. Cette opération est le pré-requis à l’installation de la version de JSF de son choix. Cette dernière aura alors pour unique contrainte d’être compatible avec le moteur de **Servlet 2.5** sur lequel repose JBoss Web.
  Plus classique, la seconde difficulté consistait à **monter les versions de JSF et de Richfaces** d’une application existante.
  J’ai arrêté mon étude après avoir migré le premier écran de cette application. Ayant conservé quelques notes, je me suis dit qu’elles pourraient intéresser certains ou certaines d’entre vous.
  Ce billet commence par expliquer comment **désinstaller JSF 1.2**, se poursuit par le déploiement du **Showcase de Richfaces 4.3.5** dans JBoss 5.1 EAP et se termine par la mise à disposition de mes **notes de migration**.
tags:
  - jboss
  - jsf
  - richfaces
title: Notes de migration vers JSF 2 et Richfaces 4
url: /2014/06/notes-migration-jsf2-richfaces4-jboss5-eap/

---
[![JBoss Richfaces Logo](/wp-content/uploads/2014/06/2014-07-jsf2-richfaces4-dans-jboss5-richfaces-logo.png)](/wp-content/uploads/2014/06/2014-07-jsf2-richfaces4-dans-jboss5-richfaces-logo.png) Début 2014, j’ai étudié la faisabilité technique d’une **migration** de **JSF 1.2** **\+ Richfaces 3.3** **vers JSF 2.1 + Richfaces 4.3** sans changer de serveur d’application.
Notre serveur [JBoss 5.1 EAP](https://access.redhat.com/site/articles/112673#EAP_5) étant certifié **JavaEE 5**, la première difficulté consistait à **désinstaller l’implémentation [Mojarra](https://javaserverfaces.java.net/) de JSF 1.2 embarquée dans JBoss**. Cette opération est le pré-requis à l’installation de la version de JSF de son choix. Cette dernière aura alors pour unique contrainte d’être compatible avec le moteur de **Servlet 2.5** sur lequel repose JBoss Web.
Plus classique, la seconde difficulté consistait à **monter les versions de JSF et de Richfaces** d’une application existante.
J’ai arrêté mon étude après avoir migré le premier écran de cette application. Ayant conservé quelques notes, je me suis dit qu’elles pourraient intéresser certains ou certaines d’entre vous.
Ce billet commence par expliquer comment **désinstaller JSF 1.2**, se poursuit par le déploiement du **Showcase de Richfaces 4.3.5** dans JBoss 5.1 EAP et se termine par la mise à disposition de mes **notes de migration**.

## Désinstaller JSF 1.2

La [base de connaissance de RedHat](https://access.redhat.com/site/solutions/17236) indique la procédure à suivre. Elle met en garde sur le fait que le support RedHat n’applique pas sur les versions de JSF ajoutées en dehors d’une distribution EAP.

1. **Supprimer les JAR de JSF**

Supprimer les JAR _jsf-impl.jar_, _jsf-api.jar_ et _jboss-faces.jar_ du répertoire _deploy/jbossweb.sar/jsf-libs_.

1. **Supprimer la configuration JSF de JBoss**

La désactivation de JSF dans JBoss passe par la suppression des 4 blocs de lignes XML suivantes dans le fichier _deployers/jbossweb.deployer/web.xml_ :

```xhtml
<context-param>
     <param-name>com.sun.faces.injectionProvider</param-name>
     <param-value>org.jboss.web.jsf.integration.injection.JBossDelegatingInjectionProvider</param-value>
</context-param>
```

```xhtml
<listener>
    <listener-class>org.jboss.web.jsf.integration.config.JBossJSFConfigureListener</listener-class>
</listener>
```

```xhtml
<listener>
    <listener-class>com.sun.faces.application.WebappLifecycleListener</listener-class>
</listener>
```

```xhtml
<init-param>
         <description>JSF standard tlds</description>
         <param-name>tagLibJar0</param-name>
         <param-value>jsf-libs/jsf-impl.jar</param-value>
</init-param>
```

La dernière manipulation consiste à supprimer la ligne suivante dans le fichier _deploy/jbossweb.sar/META-INF/jboss-structure.xml_ :
<path name="jsf-libs" suffixes=".jar" />

Pour se prémunir de toute erreur de syntaxe, démarrer JBoss à vide.

## Déployer une application JSF 2

Afin de valider le déploiement d’une application JSF 2 / Richfaces 4, le candidat retenu a naturellement été l’ [**application démo Richfaces Showcase de JBoss**](http://showcase.richfaces.org/). Seuls les quelques composants utilisant les fonctionnalités asynchrones de Servlet 3.0 ne seront pas disponibles. Sortie début 2014, la version utilisée est la 4.3.5.
Disponible librement sur le site de JBoss, l’archive [richfaces-4.3.5.Final.zip](http://downloads.jboss.org/richfaces/releases/4.3.X/4.3.5.Final/richfaces-4.3.5.Final.zip) donne accès au code source de Richfaces et de son Showcase. Accessible dans le sous-répertoire _examples\\richfaces-showcase\_, le WAR de l’application web peut être construit avec maven.
Plusieurs profiles maven sont configurés dans le _pom.xml_. Certains permettent de choisir l’implémentation de JSF (Myfaces ou Sun RI/Mojarra). D’autres permettent de construire le WAR en fonction du serveur d’application cible : Tomcat 6, JBoss AS 7 et 7.1 ou bien encore un serveur certifié JavaEE 6. Les derniers permettent de le déployer sur les PAAS OpenShift et Google App Engine.
Aucun profil n’existe pour JBoss 5.1 EAP. Le profil se rapprochant le plus de notre JBoss 5.1 EAP est celui pour Tomcat 6. Ce profil est celui activé par défaut lors d’un _mvn clean install_.

Quelques adaptations du _pom.xml_ sont nécessaires afin que le WAR généré par maven puisse être déployé dans JBoss 5.1 EAP :

**1\. Supprimer les dépendances vers Hibernate**

Les 4 dépendances suivantes peuvent être supprimées car JBoss embarque ses propres versions d’Hibernate 3.3. A noter que le showcase est rétro-compatible avec Hibernate 3.3 et JPA 1:

- hibernate-commons-annotations-4.0.1.Final.jar
- hibernate-core-4.0.0.Final.jar
- hibernate-entitymanager-4.0.0.Final.jar
- hibernate-jpa-2.0-api-1.0.1.Final.jar

Dans le fichier _src/main/resources-tomcat/META-INF/persistence.xml_, la déclaration suivante doit être supprimée :
<provider>org.hibernate.ejb.HibernatePersistence</provider> **2\. Adapter les descripteurs de déploiement à JBoss 5**

Les descripteurs de déploiement de tomcat6 ont été adaptés, en particulier le fichier _src/main/webapp-tomcat/WEB-INF/web.xml_.
Premier changement, son namespace référence l’API Servlet 2.5 :

```xhtml
<web-app xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns="http://java.sun.com/xml/ns/javaee" xmlns:web="http://java.sun.com/xml/ns/javaee/web-app_2_5.xsd"  xsi:schemaLocation="http://java.sun.com/xml/ns/javaee http://java.sun.com/xml/ns/javaee/web-app_2_5.xsd" id="richfaces-showcase"  version="2.5">
```

La fonctionnalité de requête asynchrone, la balise < async-supported> du filtre _PushFilter_ doit être supprimée.

JSF étant désormais embarqué dans le répertoire lib du war, l’ajout du _ConfigureListener_ est nécessaire :

```xhtml
<listener>
        <listener-class>com.sun.faces.config.ConfigureListener</listener-class>
</listener>
```

Enfin, CDI n’étant pas géré par le conteneur JEE, la ressource _BeanManager_ doit être supprimée.

Une fois déployé dans JBoss, le showcase RichFaces est disponible à cette URL : [http://localhost:8080/richfaces-showcase-tomcat6/](http://localhost:8080/richfaces-showcase-tomcat6/) [![Richfaces Showcase Screenshot](/wp-content/uploads/2014/06/2014-07-jsf2-richfaces4-dans-jboss5-screenshot.png)](/wp-content/uploads/2014/06/2014-07-jsf2-richfaces4-dans-jboss5-screenshot.png)

Les logs de démarrage du serveur JBoss et de l’application montrent clairement que JSF 2 et Richfaces 4 sont utilisés :

```apache
20:51:53,781 INFO  [ServerImpl] Starting JBoss (Microcontainer)...
20:51:53,782 INFO  [ServerImpl] Release ID: JBoss [EAP] 5.1.1 (build: SVNTag=JBPAPP_5_1_1 date=201105171607)
20:51:53,782 INFO  [ServerImpl] Home Dir: D:\jboss-eap-5.1\jboss-as
20:51:56,080 INFO  [ServerInfo] Java version: 1.6.0_31,Sun Microsystems Inc.
20:51:56,081 INFO  [ServerInfo] Java Runtime: Java(TM) SE Runtime Environment (build 1.6.0_31-b05)
20:51:56,081 INFO  [ServerInfo] Java VM: Java HotSpot(TM) 64-Bit Server VM 20.6-b01,Sun Microsystems Inc.
20:51:56,081 INFO  [ServerInfo] VM arguments: -Dprogram.name=JBossTools: JBoss EAP 5.x Runtime -Xms256m -Xmx768m -XX:MaxPermSize=256m -Dsun.rmi.dgc.client.gcInterval=3600000 -Dsun.rmi.dgc.server.gcInterval=3600000 -Djava.endorsed.dirs=D:\jboss-eap-5.1\jboss-as\lib\endorsed -Dfile.encoding=ISO-8859-1
20:52:15,315 INFO  [AjpProtocol] Initializing Coyote AJP/1.3 on ajp-localhost%2F127.0.0.1-8009
20:52:15,332 INFO  [StandardService] Démarrage du service jboss.web
20:52:15,334 INFO  [StandardEngine] Starting Servlet Engine: JBoss Web/2.1.11.GA
20:52:15,377 INFO  [Catalina] Server startup in 62 ms
20:52:18,375 INFO  [PersistenceUnitDeployment] Starting persistence unit persistence.unit:unitName=#richfaces-showcase
20:52:18,455 INFO  [Version] Hibernate Annotations 3.4.0.GA_CP01
20:52:18,466 INFO  [Environment] Hibernate 3.3.2.GA_CP04
20:52:18,593 INFO  [Version] Hibernate EntityManager [WORKING]
20:52:18,620 INFO  [Ejb3Configuration] Processing PersistenceUnitInfo [name: richfaces-showcase ...]
20:52:18,688 WARN  [Ejb3Configuration] Persistence provider caller does not implement the EJB3 spec correctly. PersistenceUnitInfo.getNewTempClassLoader() is null.
20:52:18,755 INFO  [AnnotationBinder] Binding entity from annotated class: org.richfaces.demo.arrangeablemodel.Person
20:52:18,950 INFO  [SettingsFactory] JDBC driver: HSQL Database Engine Driver, version: 1.8.0
20:52:18,979 INFO  [Dialect] Using dialect: org.hibernate.dialect.HSQLDialect
20:52:19,030 INFO  [Version] Hibernate Validator 3.1.0.GA
20:52:19,270 INFO  [TomcatDeployment] deploy, ctxPath=/richfaces-showcase
20:52:19,440 INFO  [Version] WELD-000900 1.1.4 (Final)
20:52:19,534 INFO  [config] Initialisation de Mojarra 2.1.19 ( 20130213-1512 https://svn.java.net/svn/mojarra~svn/tags/2.1.19@11614) pour le contexte «/richfaces-showcase»
20:52:24,347 INFO  [application] JSF1048 : Présence d?annotations PostConstruct/PreDestroy  Les méthodes de beans gérés marquées avec ces annotations auront des annotations dites traitées.
20:52:30,174 INFO  [Application] RichFaces Core Implementation by JBoss by Red Hat, version 4.3.5.Final
20:52:30,217 INFO  [Application] Startup initialization of PushContext
20:52:30,232 WARNING [Application] JMS API was found on the classpath; if you want to enable RichFaces Push JMS integration, set context-param 'org.richfaces.push.jms.enabled' in web.xml
20:52:30,292 INFO  [AnnotationBinder] Binding entity from annotated class: org.richfaces.demo.arrangeablemodel.Person
20:52:30,292 INFO  [EntityBinder] Bind entity org.richfaces.demo.arrangeablemodel.Person on table Person
20:52:30,298 INFO  [HibernateSearchEventListenerRegister] Unable to find org.hibernate.search.event.FullTextIndexEventListener on the classpath. Hibernate Search is not enabled.
20:52:30,299 INFO  [NamingHelper] JNDI InitialContext properties:{}
20:52:30,517 INFO  [Bootstrap] WELD-000101 Transactional services not available. Injection of @Inject UserTransaction not available. Transactional observers will be invoked synchronously.
20:52:30,855 INFO  [Tomcat6Container] Tomcat 6 detected, CDI injection will be available in Servlets and Filters. Injection into Listeners is not supported
20:52:31,392 WARNING [Webapp] PushFilter has been deprecated, you should use PushServlet instead
20:52:31,446 INFO  [ProfileServiceBootstrap] Loading profile: ProfileKey@1b83ee9a[domain=default, server=default, name=jsf2]
20:52:31,454 INFO  [Http11Protocol] D?marrage de Coyote HTTP/1.1 sur http-localhost%2F127.0.0.1-8080
20:52:31,478 INFO  [AjpProtocol] Starting Coyote AJP/1.3 on ajp-localhost%2F127.0.0.1-8009
20:52:31,487 INFO  [ServerImpl] JBoss (Microcontainer) [5.1.1 (build: SVNTag=JBPAPP_5_1_1 date=201105171607)] Started in 37s:701ms

```

## Migrer vers JSF 2 et Richfaces 4

Migrer une application développée en Richfaces 3 vers du Richfaces 4 est loin d’être indolore. Outre la montée de version de JSF, c’est le passage à Richfaces 4 qui demande le plus d’efforts. En effet, cette version majeure n’est pas rétro-compatible avec la précédente. De nombreux changements ont été apportés :

- Réduction du code d’ **Ajax4Jsf** au profit du support Ajax introduit dans JSF 2
- **Renommage** de classes, packages, tags et paramètres
- **Suppression de tags Richfaces**

Pour faciliter le travail du développeur, JBoss met à disposition un [Guide de migration de Richfaces 3 vers Richfaces 4](https://community.jboss.org/wiki/RichFacesMigrationGuide33x-4xMigration). Et pour le compléter, voici mes notes de travail :

**Migration Richfaces**

1. Retirer le context parameter _org.ajax4jsf.VIEW\_HANDLERS_ nécessite de réimplémenter la classe _ParameterizedFaceletViewHandler_
1. La classe _org.richfaces.renderkit.html.HtmlRichMessageRenderer_ est renommée en _HtmlMessageRenderer_
1. [La classe _AjaxContext_ d'A4JSF a disparu](https://community.jboss.org/wiki/ProgrammaticControlOfPartialProcessingInRichFaces4). Nécessiter d’utiliser l'API JSF2  _context.getPartialViewContext().isAjaxRequest()_ pour savoir si la requête http est une requête Ajax. Le code _ajaxContext.getAjaxSingleClientId()_ est migré en _context.getPartialViewContext().getExecuteIds().size() == 1_
1. [Supprimer la déclaration du filtre _org.ajax4jsf.Filter_ dans le _web.xml_ qui n'est plus nécessaire dans RichFaces 4.](http://stackoverflow.com/questions/8448427/configuring-for-richfaces-java-lang-classnotfoundexception-org-ajax4jsf-filter)
1. [Classes InternetResourceBuilder et InternetResource non trouvées](http://stackoverflow.com/questions/20218396/richfaces-3-to-4-migration-internetresourcebuilder/) : constante DEFAULT\_EXPIRE redéfinie à 1 jour.
1. [Les composants <a4jloadScript> et  <a4jloadStyle> ont été supprimés de RichFaces 4](http://stackoverflow.com/questions/8154232/richfaces-4-replacement-for-a4jloadscript). Les tags natifs de JSF 2 doivent être utilisés h:outputStylesheet and h:outputScript
1. [Remplacer le tag <a4j:loadBundle> par <f:loadBundle>](https://community.jboss.org/thread/166111?tstart=0)
1. Sous peine d’une _javax.faces.FacesException: No enum const class org.richfaces.component.JQueryTiming.onload_, la déclaration _<rich:jQuery timing="onload" selector="document" query="loadMyCombo()"/>_ doit être corrigée avec l’attribut _timing="domready"_.
1. [Renommer l’objet JavaScript Richfaces en RichFaces.](http://stackoverflow.com/questions/10403889/richfaces-is-not-defined-javascript-error)

**Migration des composants RichFaces**

1. Prendre connaissance du [guide de migration des composants](https://community.jboss.org/wiki/RichFacesMigrationGuide33x-4xMigration-ComponentsMigration-RichPanelOutputComponents).
1. Migrer _<rich:modalPanel>_ vers _<rich:_ _popupPanel>_
1. Tag _<rich:spacer>_ supprimé. Pas d'équivalent. [Création nécessaire d'un custom tag](https://community.jboss.org/wiki/SpacerImplementationForJSF2OrRichFaces4).
1. Migrer le tag _<rich:simpleTogglePanel>_ en _<rich:collapsiblePanel>_
1. Tag _<a4j:include>_ remplacé par _<ui:include_ \> \+ paramètre _viewId_ changé en _src_
1. Tag _<aj4:form>_ remplacé par _<h:form>_
1. Tag _<a4j:support>_ remplacé par _<a4j:ajax>_
1. Tag _<rich:toolTip>_ remplacé par _<rich:tooltip>_
1. [Tag <rich:suggestionbox> des snippets à migrer vers l’autocomplete](https://community.jboss.org/message/568610).
1. Noms d’évènements JavaScript à renommer. Exemple de message d’erreur si oubli : _<a4j:ajax> onclickevent is not supported for the HtmlSelectOneRadio_
    1. HtmlSelectOneRadio : event="onclick" à changer en "select"
    1. _HtmlSelectOneMenu_ : event="onchange" à changer en "select"
    1. _HtmlInputText_ : event="onchange" à changer en "change"
    1. _UICalendar_ : event="onchanged" à changer en "change"

**Migration Facelets**

1. Facelets est désormais inclu dans l'API JSF 2 et l'implémentation JSF RI Mojara 2 ( _jsf-impl-2.1.19-jbossorg-1.jar_ et _jboss-jsf-api\_2.1\_spec-2.1.19.1.Final.jar_)
1. Package _com.sun.facelets_ scindé en 2 : _javax.faces.view.facelets_ pour l’API et _com.sun.faces.facelets_ pour l’implémentation
1. Classe _com.sun.facelets.impl.ResourceResolver_ relocalisée dans _javax.faces.view.facelets.ResourceResolver_
1. Supprimer le parameter _<param-name>org.ajax4jsf.VIEW\_HANDLERS</param-name>_ du _web.xml_
1. Renommer les variables suivantes dans le _web.xml_:

   1. facelets.SKIP\_COMMENTS en javax.faces.FACELETS\_SKIP\_COMMENTS
   1. facelets.LIBRARIES en javax.faces.FACELETS\_LIBRARIES

**Migration Apache Tomahawk**

1. Utiliser la version MyFaces Tomahawk 1.1.14 for JSF 2.0.
1. L'artefact tomahawk change en tomahawk20
   _<dependency>_
   _<groupId>org.apache.myfaces.tomahawk</groupId>_
   _<artifactId>tomahawk20</artifactId>_
   _<version>1.1.14</version>_
   _</dependency>_

**Migration JSF 2**

1. L’extension .jspx des pages ne fonctionne plus => géré par le moteur JSP de Tomcat. Passage à xhtml + suppression conf JSF
1. Classe _com.sun.faces.application.ConfigNavigationCase_ de JSF 1 à remplacer :

   1. Utilisation de la classe _javax.faces.application.NavigationCase_ introduite dans JSF 2.
   1. Le constructeur prend 3 nouveaux paramètres : _condition_, _includeViewParams_ et _parameters_
   1. La méthode _getToViewId_ prend désormais un _FacesContext_ en paramètre => nécessite de faire appel à _FacesContext.getCurrentInstance()_
1. [Remplacer <head> du HTML par <h:head> de JSF 2](http://forum.primefaces.org/viewtopic.php?f=3&t=1721) sous peine d’obtenir l’erreur jSf précisant qu’une ou plusieurs ressources partagent la cible «body», mais qu’aucun composant «body» n’a été défini dans la vue.

## Conclusion

En l’espace 2 jours, j’aurais réussi à démarrer mon application puis à migrer partiellement un premier écran, et ceci sans changer de serveur d’application. J’ai chiffré à 30 jours de développement le temps nécessaire pour migrer l’intégralité d’une application comportant une vingtaine d'écrans.
Pour les applications comportant de nombreux écrans, afin de réduire les coûts et les erreurs humaines, **l’automatisation des tâches récurrentes de migration pourrait être intéressante**. Dommage que JBoss ne propose pas un tel outil.

Références :

- [RichFaces Migration Guide. 3.3.x - 4.x Migration](https://community.jboss.org/wiki/RichFacesMigrationGuide33x-4xMigration)
- [RichFaces 3.3 - > 4.x migration guide. Unleashed](https://community.jboss.org/wiki/RichFaces33-4xMigrationGuideUnleashed)
- [Write a JSF 2 custom EL resolver](http://www.java-tutorial.ch/java-server-faces/write-a-jsf-2-custom-el-resolver)
- [For JSF 2.0, How to Enable EL 2.2 on Tomcat 6](http://www.javaplex.com/for-jsf-2-how-to-enable-el-2-2-on-tomcat-6/)
- [JSF 2 Configuration parameters](http://www.java-tutorial.ch/java-server-faces/jsf-2-configuration-parameters)
- [What’s New in JSF 2?](http://andyschwartz.wordpress.com/2009/07/31/whats-new-in-jsf-2/)
- [Richfaces 4.X Sandbox Components](https://community.jboss.org/wiki/4XSandboxComponents)
