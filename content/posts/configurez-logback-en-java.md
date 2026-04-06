---
_edit_last: "1"
_thumbnail_id: "1812"
_xmlsf_image_featured:
  caption: ""
  loc: https://javaetmoi.com/wp-content/uploads/2018/03/logback-logo.jpg
  title: logback-logo
author: admin
categories:
  - retour-d'expérience
cover:
  alt: logback-logo
  image: /wp-content/uploads/2018/03/logback-logo.jpg
date: "2018-03-30T17:01:59+00:00"
guid: http://javaetmoi.com/?p=1811
parent_post_id: null
post_id: "1811"
post_views_count: "18410"
summary: |-
  [![](http://javaetmoi.com/wp-content/uploads/2018/03/logback-logo.jpg)](http://javaetmoi.com/wp-content/uploads/2018/03/logback-logo.jpg)

  Afin de **normaliser** la **configuration Logback** des applications web sur lesquelles j’interviens, j’ai récemment eu besoin de programmer Logback via son **API en Java** et non en utilisant la syntaxe XML Joran.
  Moins courant que le traditionnel **logback.xml**, cette possibilité de configurer Logback par le code offre davantage de possibilités, ne serait-ce que par son caractère dynamique.

  Par le passé, j’avais déjà eu l’occasion de manipuler l’API Logback dans des tests unitaires afin de changer dynamiquement le niveau de log des loggers.
  Cette fois-ci, je l’ai utilisé pour déclarer les différents appenders et configurer toute l’ **infrastructure applicative de logs**:

  - Activer l’appender Console uniquement sur le poste de dév (afin qu’en prod, les logs ne se retrouvent pas en double dans le fichier server.log de JBoss)
  - Factoriser la stratégie de journalisation des différents appenders fichiers (troubleshooting, overview, soap …)
  - Récupérer différentes informations applicatives (ex : nom de la JVM, application, nom de l’environnement, login de l’utilisateur authentifié) à destination du collecteur de logs (Logstash ou Splunk)
  - Exposer l’accès aux loggers au travers d’une API REST

  La configuration des logs reste paramétrable via un fichier de properties externe. En effet, le paramétrage peut différer d’un environnement de déploiement à l’autre (ex : chemin du répertoire des fichiers logs). La configuration Logback reste extensible par l’inclusion d’un fichier XML au format Joran.

  Dans cet article, je vais vous présenter quelques bouts de code simplifié manipulant l’API Java de Logback.
tags:
  - logback
title: Configurez Logback en Java
url: /2018/03/configurez-logback-en-java/

---
[![](/wp-content/uploads/2018/03/logback-logo.jpg)](/wp-content/uploads/2018/03/logback-logo.jpg)

Afin de **normaliser** la **configuration Logback** des applications web sur lesquelles j’interviens, j’ai récemment eu besoin de programmer Logback via son **API en Java** et non en utilisant la syntaxe XML Joran.
Moins courant que le traditionnel **logback.xml**, cette possibilité de configurer Logback par le code offre davantage de possibilités, ne serait-ce que par son caractère dynamique.

Par le passé, j’avais déjà eu l’occasion de manipuler l’API Logback dans des tests unitaires afin de changer dynamiquement le niveau de log des loggers.
Cette fois-ci, je l’ai utilisé pour déclarer les différents appenders et configurer toute l’ **infrastructure applicative de logs**:

- Activer l’appender Console uniquement sur le poste de dév (afin qu’en prod, les logs ne se retrouvent pas en double dans le fichier server.log de JBoss)
- Factoriser la stratégie de journalisation des différents appenders fichiers (troubleshooting, overview, soap …)
- Récupérer différentes informations applicatives (ex : nom de la JVM, application, nom de l’environnement, login de l’utilisateur authentifié) à destination du collecteur de logs (Logstash ou Splunk)
- Exposer l’accès aux loggers au travers d’une API REST

La configuration des logs reste paramétrable via un fichier de properties externe. En effet, le paramétrage peut différer d’un environnement de déploiement à l’autre (ex : chemin du répertoire des fichiers logs). La configuration Logback reste extensible par l’inclusion d’un fichier XML au format Joran.

Dans cet article, je vais vous présenter quelques bouts de code simplifié manipulant l’API Java de Logback.

## Où brancher l’initialisation ?

Notre étude de cas porte sur une application web démarrée dans un conteneur de servlets (ex : Tomcat) ou un serveur d’application (ex : JBoss).
Pour logger, les développeurs utilisent l’API SLF4J. Logback a été retenue comme implémentation de SLF4J.

Pour brancher la configuration Java, le moyen le plus courant est d’utiliser un **ServletContextListener** dédié. Afin d’être démarré en premier, ce listener est déclaré tout en haut du web.xml, en tête des autres listeners (avant le listener Spring).

Outre la configuration Logback, on retrouve également dans ce listener la configuration SLF4J. Par exemple, pour initialiser le **bridge JUL SLF4JBridgeHandler**.

Exemple de Listener :

```java
@WebListener
public class LogbackListener extends ContextAwareBase implements ServletContextListener {

    @Override
    public void contextInitialized(ServletContextEvent servletContextEvent) {
        setContext(getLobackContext());
        // TODO : initialisation de Logback
    }
```

A noter l’utilisation de la classe helper **ContextAwareBase** dont nous verrons l’usage par la suite.

## Accèder au LoggerContext

Afin de pouvoir programmer Logback, il est nécessaire de récupérer l’instance de **LoggerContext**. Classe centrale de Logback, [LoggerContext](https://github.com/qos-ch/logback/blob/master/logback-classic/src/main/java/ch/qos/logback/classic/LoggerContext.java) implémente l’interface ILoggerFactory de SLF4J.
Pour la récupérer, on demande à SLF4J de nous retourner l’interface en passant par la méthode statique getILoggerFactory de la classe utilitaire **LoggerFactory** de SLF4J.

Un bout de code est bien plus parlant. Pour s’y retrouver entre SLF4J et Logback, le nom qualifié des classes est utilisé :

```java
private LoggerContext getLogbackContext() {
    return (ch.qos.logback.classic.LoggerContext) org.slf4j.LoggerFactory.getILoggerFactory();
}
```

## Usage du ContextAwareBase

La classe **ContextAwareBase** héritée par notre _LogbackListener_ est une classe utilitaire proposée par Logback. Elle implémente l’interface _ContextAware_. Elle apporte 2 fonctionnalités :

- Conserver en mémoire le contexte Logback (accessible via la méthode _getContext_) pour un accès ultérieur plus rapide.
- Fournir des méthodes de logs internes : _addInfo_, _addWarn_ et _addError_. A priori, cela peut paraître étrange, mais vous allez bientôt connaître la raison.

Dans le code du framework Logback comme dans le code applicatif chargé d’initialiser Logback, nous ne pouvons pas encore utiliser le système de logs de SLF4J/Logback pour tracer des erreurs ou tout simplement des informations utiles. A ce stade  SLF4J/Logback n’est en effet pas encore prêt.

Pour pallier à cette problématique, Logback propose un mécanisme de statuts matérialisé par l’interface _ch.qos.logback.core.status.Status_. Les méthodes _addInfo_, _addWarn_ et _addError_ ajoutent un statut dans une liste de statuts interne à Logback et gérée par le [StatusManager](https://github.com/qos-ch/logback/blob/master/logback-core/src/main/java/ch/qos/logback/core/status/StatusManager.java). Nous verrons par la suite comment exploiter ces statuts.

Dans notre Listener, nous pouvons ainsi tracer des informations importantes :

```java
addInfo("Suppression du handler JUL : "+ handler.getClass().getName());
```

## Installation du bridge SLF4J

Afin de rediriger les logs de Java Util Logging (JUL) vers Logback, il est nécessaire d’ajouter au classpath le JAR jul-to-slf4j.jar puis d’installer le bridge [**SLF4JBridgeHandler**](https://github.com/qos-ch/slf4j/blob/master/jul-to-slf4j/src/main/java/org/slf4j/bridge/SLF4JBridgeHandler.java). Ce bridge route tous les logs JUL vers l’API SLF4J qui redirige à son tour les logs vers Logback.

Voici un exemple d’installation du SLF4JBridgeHandler. A noter qu’il met en application l’usage des méthodes _addInfo_ et _addError_.

```java
private void configureJdkLoggingBridgeHandler() {
    try {
        if (isBridgeHandlerAvailable()) {
            java.util.logging.Logger rootLogger = LogManager.getLogManager().getLogger("");
            Handler[] handlers = rootLogger.getHandlers();
            for (Handler handler : handlers) {
                if (handler instanceof ConsoleHandler) {
                    addInfo("Suppression du handler JUL : " + handler.getClass().getName());
                    rootLogger.removeHandler(handler);
                }
            }
            SLF4JBridgeHandler.install();
        }
    } catch (RuntimeException ex) {
        addError("Le bridge SLF4J pour JUL n'a pas été installé", ex);
    }
}
```

Bien plus safe que l’appel à la méthode SLF4JBridgeHandler:: removeHandlersForRootLogger, le code ci-dessus retire le ConsoleHandler mais laisse ceux éventuellement ajoutés par le serveur d’application.

La méthode _isBridgeHandlerAvailable()_ teste l’existence du bridge dans le classpath :

```java
private boolean isBridgeHandlerAvailable() {
    return ClassUtils.isPresent("org.slf4j.bridge.SLF4JBridgeHandler", ClassUtils.getDefaultClassLoader());
}
```

## Synchronisation

Lorsque Logback est configuré à partir d’un fichier XML, Logback se prémunit de toute demande de configuration concurrente en utilisant le **verrou LogbackLock** (se référer à la méthode [GenericConfigurator:: doConfigure(List<SaxEvent>)](https://github.com/qos-ch/logback/blob/master/logback-core/src/main/java/ch/qos/logback/core/joran/GenericConfigurator.java)).

Par précaution, toute la configuration du LogbackContext est réalisée dans un **bloc synchronisé** sur ce verrou :

```java
synchronized (getLogbackContext().getConfigurationLock()) {
    stopAndReset();
    enableDebugMode();
    // ...
}
```

## Réinitialisation du contexte

Avant de pouvoir configurer par programmation les appenders et le niveau des loggers, il est nécessaire de **réinitialiser Logback**. En apparence, cela ne semble pas nécessaire puisque l’application vient tout juste de démarrer. C’est oublier qu’avant d’arriver dans le code du listener, la JVM aura déjà instancié de nombreuses classes. Or, **la toute 1ière instanciation d’un logger déclenche automatiquement l’initialisation de SLF4J** (méthode LoggerFactory::performInitialization) qui appelle à son tour l’initialisation de Logback (instanciation du LoggerContext par la classe StaticLoggerBinder). Logback recherche alors sa configuration dans le classpath en testant la présence des fichiers logback-test.xml, logback.groovy et logback.xml.

Vous avez compris : lorsqu’on arrive dans le listener, Logback s’est déjà initialisé. Il est donc préférable de faire le ménage en réinitialisant sa configuration par défaut.  Pour se faire, on appelle successivement les méthodes stop() et reset() du LoggerContext. Et si le SLF4JBridgeHandler est installé, on propage à JUL les réinitialisations des niveaux des loggers :

```java
private void stopAndReset(LoggerContext loggerContext) {
    loggerContext.stop();
    loggerContext.reset();
    if (isBridgeHandlerAvailable()) {
        LevelChangePropagator levelChangePropagator = new LevelChangePropagator();
        levelChangePropagator.setResetJUL(true);
        levelChangePropagator.setContext(loggerContext);
        loggerContext.addListener(levelChangePropagator);
    }
}
```

## Activation du mode debug

Nous avons vu que Logback conserve en mémoire une liste de Status permettant d’historiser certains évènements.
Lorsque le **mode debug** de Logback est activé, **les statuts sont affichés dans la sortie console standard** (qui dans un serveur d’application comme JBoss est redirigé vers le fichier server.log).

En XML, l’activation du mode debug se fait dans au niveau de la balise racine <configuration> : <configuration debug="true">

En Java, on enregistre le listener [**OnConsoleStatusListener**](https://github.com/qos-ch/logback/blob/master/logback-core/src/main/java/ch/qos/logback/core/status/OnConsoleStatusListener.java) auprès du StatusManager du contexte Logback :

```java
StatusListenerConfigHelper.addOnConsoleListenerInstance(loggerContext, new OnConsoleStatusListener());
```

## Déclaration des appenders

Logback délègue la tâche d’écriture des logs à des composants appelés « **appenders**». Implémentant l’interface [Appender](https://github.com/qos-ch/logback/blob/master/logback-core/src/main/java/ch/qos/logback/core/Appender.java), les appenders permettent d’afficher les logs sur la console, de les archiver dans des fichiers ou bien encore de les stocker en base de données.

La déclaration des appenders communs à tous les loggers non exclusifs passe par la configuration du **logger racine** (le « root logger »). La méthode utilitaire _root_ permet de spécifies son niveau et la liste des appenders :

```java
private void root(Level level, List<Appender<ILoggingEvent>> rootAppenders) {
    ch.qos.logback.classic.Logger logger = this.getLogbackContext().getLogger(org.slf4j.Logger.ROOT_LOGGER_NAME);
    rootAppenders.forEach(logger::addAppender);

}
```

La déclaration de l’ **appender Console** permettant d’afficher les logs dans la sortie console est relativement simple :

```java
private ConsoleAppender<ILoggingEvent> consoleAppender() {
    ConsoleAppender<ILoggingEvent> appender = new ConsoleAppender<ILoggingEvent>();
    PatternLayoutEncoder encoder = new PatternLayoutEncoder();
    encoder.setPattern(CONSOLE_LOG_PATTERN);
    start(encoder);
    appender.setEncoder(encoder);
    appender("console", appender);
    return appender;
}
```

Comme son nom l’indique, la classe **PatternLayoutEncoder** permet d’indiquer à Logback le format d’affichage des logs. Voici un exemple de pattern :

```java
private static final String CONSOLE_LOG_PATTERN =     "%d{HH:mm:ss.SSS} | %highlight(%-5level) | %cyan(%-50.50logger{49}) | %-200m %C.%M\\(%F:%L\\)%n";
```

Notez l’utilisation des [sous-patterns de couleur](https://logback.qos.ch/manual/layouts.html)%highlight et %cyan

L’appel à la méthode _start_ de l’encoder est nécessaire :

```java
private void start(LifeCycle lifeCycle) {
    if (lifeCycle instanceof ContextAware) {
        ((ContextAware) lifeCycle).setContext(this.context);
    }
    lifeCycle.start();
}
```

De la même manière, il est nécessaire de démarrer l’appender. On passe par l’appel de la méthode _appender_:

```java
private void appender(String name, Appender<?> appender) {
    appender.setName(name);
    start(appender);
}
```

La déclaration d’un **appender fichier** est bien plus verbeuse :

```java
private RollingFileAppender<ILoggingEvent> troubleshootingAppender() {
    RollingFileAppender<ILoggingEvent> appender = new RollingFileAppender<>();
    PatternLayoutEncoder encoder = new PatternLayoutEncoder();
    // Do not rely on the OS default charset
    encoder.setCharset(APPENDER_CHARSET);
    encoder.setPattern(FILE_LOG_PATTERN);
    appender.setEncoder(encoder);
    start(encoder);
    appender.setFile("/log/MyApp-troubleshooting.log");

    SizeBasedTriggeringPolicy<ILoggingEvent> triggeringPolicy = new SizeBasedTriggeringPolicy<ILoggingEvent>();
    triggeringPolicy.setMaxFileSize(FileSize.valueOf("10MB"));
    triggeringPolicy.start();
    appender.setTriggeringPolicy(triggeringPolicy);

    FixedWindowRollingPolicy rollingPolicy = new FixedWindowRollingPolicy();
    rollingPolicy.setMinIndex(1);
    rollingPolicy.setMaxIndex(10);
    String rollingName = "/log/backup/MyApp-troubleshooting_%i.log.zip";
    rollingPolicy.setFileNamePattern(rollingName);
    appender.setRollingPolicy(rollingPolicy);
    rollingPolicy.setParent(appender);
    start(rollingPolicy);

    appender("troubleshooting-file", appender);
    return appender;
}
```

En complément du pattern d’affichage, la stratégie de journalisation doit être spécifiée. Dans notre exemple, lorsque le fichier de logs atteint 10 Mo, il est compressé en une archive zip qui est déplacée dans le sous-répertoire backup. Un total de 10 archives est conservé. La compression d’un fichier de log est généralement très efficiente et sera bien antérieure à 10% de la taille initiale. On garantit ainsi que, sur le filesystem, la taille totale des logs n’excèdera pas 20 Mo.

Le pattern utilisé par cet appender diffère légèrement de celui de l’appender console en ajoutant le jour et le nom du thread et en n’utilisant pas les sous-patterns de couleur :

```java
private static final String FILE_LOG_PATTERN =     "%d{yyyy/MM/dd HH:mm:ss.SSS} | %-50.50logger{49} | %-200m |  %-5thread |%C.%M\\(%F:%L\\) %n";

```

Une fois déclarés les appenders racines, on appelle la méthode _root_ présentée ci-dessus :

```java
root(Level.INFO, appenders);
```

## Niveau des loggers

Le niveau de logs des principaux frameworks est simple à configurer :

```java
private void base() {
    logger("com.atomikos", Level.WARN);
    logger("org.apache.cxf", Level.INFO);
    logger("org.hibernate", Level.INFO);
    logger("org.springframework", Level.INFO);
}

private void logger(String name, Level level) {
    Logger logger = this.getLogbackContext().getLogger(name);
    logger.setLevel(level);
}
```

## Activation de JMX

Afin de pouvoir pour exemple activer les niveaux des logs à chaud, il peut être intéressant d’exposer les MBean de Logback via JMX.

```java
private void enableJMX(ServletContext servletContext) {
    LoggerContext loggerContext = this.getLogbackContext();
    String servletContextName = servletContext.getServletContextName();
    if (servletContextName != null) {
        loggerContext.setName(servletContextName);
    }
    JMXConfiguratorAction jmxConfiguratorAction = new JMXConfiguratorAction();
    jmxConfiguratorAction.setContext(loggerContext);
    try {
        jmxConfiguratorAction.begin(null, null, new AttributesImpl());
    } catch (ActionException e) {
        addError("The Logback JMX configuration failed", e);
    }
}
```

Lorsque plusieurs WAR sont déploés dans une JVM, il est préférable de nommer le LoggerContext de chaque web app à partir du nom déclaré dans le web.xml.

L’exposition des MBean sur HTTP est possible à l’aide de librairies tierces tels [Jolokia](https://jolokia.org/).

## Pour aller plus loin

La configuration Logback présentée dans cet article pourrait être complétée par :

- La configuration d’un appender **LogstashEncoder** permettant de générer les logs au format JSON et de les indexer les logs dans Elasticsearch
- La déclaration conditionnelle de l’appender Console sur le poste de dév (utilisation d’un fichier properties ou d’un paramètre de JVM)
- L’utilisation du **contexte MDC** pour afficher systématiquement dans les logs le login de l’utilisateur authentifié et l’identifiant de la session
- Un mécanisme d’extension de la configuration Logback par l’inclusion d’un fichier XML ou d’une classe Java externe.

## Conclusion

Au cours de cet article, nous aurons vu comment configurer Logback à travers son API Java. Les classes manipulées sont les mêmes que celles utilisées par la [syntaxe Groovy](https://logback.qos.ch/manual/groovy.html).
Le **code complet des snippets** est disponible dans ce [Gist](https://gist.github.com/arey/bc09e0d77520dc97f12707c6064c8c4e).

Le choix de privilégier la configuration Java a été fait par l’équipe de **Sp** r **ing Boot**. Je vous recommande d’aller jeter un coup d’œil aux classes [DefaultLogbackConfiguration](https://github.com/spring-projects/spring-boot/blob/master/spring-boot-project/spring-boot/src/main/java/org/springframework/boot/logging/logback/DefaultLogbackConfiguration.java) et [LogbackConfigurator](https://github.com/spring-projects/spring-boot/blob/master/spring-boot-project/spring-boot/src/main/java/org/springframework/boot/logging/logback/LogbackConfigurator.java).
Etant donné qu’il n’y a plus de fichier XML à parser, le temps de démarrage de l’application est sensiblement amélioré (100 ms d’après la [documentation Logback](https://logback.qos.ch/manual/configuration.html)).

Ressources :

- [Manuel d’utilisation de Logback](https://logback.qos.ch/manual/)
- [Spring Boot - LoggingSystem abstraction and logging configuration properties](https://www.logicbig.com/tutorials/spring-framework/spring-boot/logging-system.html)
- [Code source LogbackListener.java](https://gist.github.com/arey/bc09e0d77520dc97f12707c6064c8c4e)
