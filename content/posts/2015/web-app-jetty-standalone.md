---
_edit_last: "1"
_wp_old_slug: embarquer-jetty-dans-une-web-app
author: admin
categories:
  - retour-d'expérience
date: "2015-06-03T05:19:45+00:00"
thumbnail: /wp-content/uploads/2015/04/jetty-logo.png
featureImage: /wp-content/uploads/2015/04/jetty-logo.png
featureImageAlt: "jetty-logo"
guid: http://javaetmoi.com/?p=1339
parent_post_id: null
post_id: "1339"
post_views_count: "7188"
summary: |-
  [![jetty-logo](http://javaetmoi.com/wp-content/uploads/2015/04/jetty-logo-300x136.png)](http://javaetmoi.com/wp-content/uploads/2015/04/jetty-logo.png) Une fois le développement d’une **application web** terminé, vient le moment (douloureux ou non) de son **installation sur un serveur**. En général, plusieurs pré-requis sont nécessaires : JRE, **serveur d’application**, base de données … Aujourd’hui, Docker et/ou des outils comme Ansible et Puppet facilitent le provisionning du middleware. Néanmoins, il est possible de simplifier encore davantage cette phase d’installation. Des applications comme Sonar et Jenkins le font depuis des années : **packager l’application avec son propre conteneur de Servlets** et sa propre base de données. Afin de pouvoir déployer des applications les plus légères possibles, les architectures micro-services poussent dans ce sens. Et c’est d’ailleurs ce que proposent des frameworks comme Play Framework et Spring Boot. Ce dernier permet en effet de créer un JAR exécutable démarrant au choix un Tomcat ou un Jetty.

  **Ce billet  explique pas à pas comment embarquer un conteneur Jetty dans sa propre application**. Nul besoin d’utiliser Spring ou Scala.

  Pour distribuer votre web app, vous aurez le choix entre :

  1. une **archive ZIP** contenant JARs, scripts shells et fichiers de configuration.
  2. ou un unique **JAR auto-exécutable**

  Le packaging est assuré par différents plugins Maven.

  Disposer d’une JVM et le seul pré-requis. Sachant qu’OpenJDK est installé sur la plupart des distributions Linux, ce n’est pas nécessairement une contrainte. Seule la version de Java devra être vérifiée avec soin.

  ![jetty-logo](/wp-content/uploads/2015/04/jetty-logo.png)
tags:
  - devops
  - jetty
  - maven
title: Embarquer Jetty dans une web app
url: /2015/06/web-app-jetty-standalone/

---
[![jetty-logo](/wp-content/uploads/2015/04/jetty-logo.png)](/wp-content/uploads/2015/04/jetty-logo.png) Une fois le développement d’une **application web** terminé, vient le moment (douloureux ou non) de son **installation sur un serveur**. En général, plusieurs pré-requis sont nécessaires : JRE, **serveur d’application**, base de données … Aujourd’hui, Docker et/ou des outils comme Ansible et Puppet facilitent le provisionning du middleware. Néanmoins, il est possible de simplifier encore davantage cette phase d’installation. Des applications comme Sonar et Jenkins le font depuis des années : **packager l’application avec son propre conteneur de Servlets** et sa propre base de données. Afin de pouvoir déployer des applications les plus légères possibles, les architectures micro-services poussent dans ce sens. Et c’est d’ailleurs ce que proposent des frameworks comme Play Framework et Spring Boot. Ce dernier permet en effet de créer un JAR exécutable démarrant au choix un Tomcat ou un Jetty.

**Ce billet  explique pas à pas comment embarquer un conteneur Jetty dans sa propre application**. Nul besoin d’utiliser Spring ou Scala.

Pour distribuer votre web app, vous aurez le choix entre :

1. une **archive ZIP** contenant JARs, scripts shells et fichiers de configuration.
1. ou un unique **JAR auto-exécutable**

Le packaging est assuré par différents plugins Maven.

Disposer d’une JVM et le seul pré-requis. Sachant qu’OpenJDK est installé sur la plupart des distributions Linux, ce n’est pas nécessairement une contrainte. Seule la version de Java devra être vérifiée avec soin.

## Code source

Le code source utilisé pour illustrer ce billet provient du projet [**embedded-jetty-webapp**](https://github.com/arey/embedded-jetty-webapp) hébergé sur GitHub. Pour des raisons de lisibilité, certaines parties ont été simplifiées.
Si vous souhaitez rendre autonome votre propre application, je vous conseille de vous inspirer directement du code disponible sur GitHub ([pom.xml](https://github.com/arey/embedded-jetty-webapp/blob/master/pom.xml) maven et [classes Java](https://github.com/arey/embedded-jetty-webapp/tree/master/src/main/java/com/javaetmoi/jetty)).

## Dépendances Maven

Avant de pouvoir utiliser l’API de Jetty pour démarrer / arrêter un serveur, il faut tout d’abord tirer toutes les dépendances nécessaires au fonctionnement d’une web app. Voici la configuration Maven :

```xhtml
<properties>
    <version.javax-servlet>3.1.0</version.javax-servlet>
    <version.jetty>9.2.7.v20150116</version.jetty>
</properties>
```

```xhtml
<!-- Jetty -->
<dependency>
    <groupId>org.eclipse.jetty</groupId>
    <artifactId>jetty-server</artifactId>
    <version>${version.jetty}</version>
</dependency>
<dependency>
    <groupId>org.eclipse.jetty</groupId>
    <artifactId>jetty-webapp</artifactId>
    <version>${version.jetty}</version>
</dependency>
<dependency>
    <groupId>org.eclipse.jetty</groupId>
    <artifactId>jetty-servlet</artifactId>
    <version>${version.jetty}</version>
</dependency>
<dependency>
    <groupId>org.eclipse.jetty</groupId>
    <artifactId>jetty-util</artifactId>
    <version>${version.jetty}</version>
</dependency>
<dependency>
    <groupId>org.eclipse.jetty</groupId>
    <artifactId>jetty-servlets</artifactId>
    <version>${version.jetty}</version>
</dependency>
<dependency>
    <groupId>org.eclipse.jetty</groupId>
    <artifactId>jetty-jsp</artifactId>
    <version>${version.jetty}</version>
</dependency>
<dependency>
    <groupId>org.eclipse.jetty</groupId>
    <artifactId>jetty-http</artifactId>
    <version>${version.jetty}</version>
</dependency>

<!--  Servlet API -->
<dependency>
    <groupId>javax.servlet</groupId>
    <artifactId>javax.servlet-api</artifactId>
    <version>${version.javax-servlet}</version>
</dependency>
```

Comme vous pouvez le constater, Jetty est particulièrement modulaire. Si vous utilisez JSP comme technologie de rendu, il faudra ajouter l’artefact _jetty-jsp_ sous peine du message d’erreur _« JSP support not configured »._

## Démarrer un Jetty

Manipuler l’API Jetty pour démarrer un conteneur de servlet depuis une classe _Main_ ne présente pas de difficulté :

```java
public static void main(String[] args) throws Exception {

    Server server = new Server(8080);

    WebAppContext root = new WebAppContext();
    root.setContextPath("/");
    root.setDescriptor("webapp/WEB-INF/web.xml");
    URL webAppDir = Thread.currentThread().getContextClassLoader().getResource("webapp");
    if (webAppDir == null) {
        throw new RuntimeException("No webapp directory was found into the JAR file");
    }
    root.setResourceBase(webAppDir.toURI().toString());
    root.setParentLoaderPriority(true);

    server.setHandler(root);
    server.start();
}
```

 [![2015-05 - WAR-less Java web application with Jetty](/wp-content/uploads/2015/04/2015-05-WAR-less-Java-web-application-with-Jetty.png)](/wp-content/uploads/2015/04/2015-05-WAR-less-Java-web-application-with-Jetty.png) Une 1ière subtilité réside dans l’utilisation du _ClassLoader_ du thread courant. Sans quoi, en dehors d’un IDE, le répertoire webapp ne sera pas trouvé.

La 2nde subtilité vient du fait que l’artefact construit est de type JAR et non un WAR. Bien qu’elle y ressemble, l’arborescence du projet n’est donc pas celle d’un WAR.
Le répertoire webapp ne se trouve pas dans le répertoire src/main/webapp mais dans src/main/resources/webapp. Ainsi, lors de la construction du JAR, le répertoire webapp sera copié à la racine du JAR sans configuration maven particulière.

Dans notre exemple, la web app utilise un descripteur de déploiement web.xml. Optionnel depuis Servlet 3.0, l’appel à la méthode _setDescriptor_ est facultatif.

Enfin, le port HTTP utilisé dans notre exemple est le 8080. Ce dernier aurait pu être passé en paramètre du `main()` ou bien chargé depuis un fichier de configuration.

Lors de l’appel à la méthode `start()`, le conteneur Jetty démarre. L’application web est ensuite aussitôt démarrée. Il n’y a pas réellement de phase de déploiement.

## Arrêter proprement Jetty

Pour arrêter le serveur, une solution peu recommandée est d’utiliser un _kill -9_ sur le PID du process Java. Les traitements en cours s’arrêtent brutalement et les ressources ne sont pas correctement libérées.
Une solution plus élégante est de demander au serveur Jetty de s’arrêter proprement. Le contexte de servlets est alors fermé par Jetty. Les listeners JEE implémentant l’interface _ServletContextListener_ en sont notifiés.

Pour communiquer avec Jetty, une solution possible est d’utiliser un socket TCP. Je me suis grandement inspiré du code Java utilisé par le [plugin Jetty pour maven](https://github.com/eclipse/jetty.project).

Le principe est simple, un thread [**Monitor**](https://github.com/arey/embedded-jetty-webapp/blob/master/src/main/java/com/javaetmoi/jetty/Monitor.java) est démarré à la suite du serveur Jetty, et ceci dans la même JVM :

```java
server.start();

Monitor monitor = new Monitor(8090, new Server[] {server});
monitor.start();
server.join();
```

Ce thread démarre un _SocketServer_ écoutant sur le port 8090. Il attend que l’instruction _stop_ lui soit envoyée.
Pour davantage de détails, vous pouvez vous reportez à la méthode statique _stop_ de la classe [JettyServer](https://github.com/arey/embedded-jetty-webapp/blob/master/src/main/java/com/javaetmoi/jetty/JettyServer.java) ainsi qu’à la classe [Monitor](https://github.com/arey/embedded-jetty-webapp/blob/master/src/main/java/com/javaetmoi/jetty/Monitor.java).

Une autre technique serait d’utiliser JMX pour communiquer avec Jetty. L’ajout du [module jetty-jmx](http://mvnrepository.com/artifact/org.eclipse.jetty/jetty-jmx) est alors nécessaire.

## Création du package

Comme je vous l’indiquais en introduction, je vous propose de packager votre application web de 2 manières différentes.

**1\. Appassembler**

Le [plugin Appassembler pour maven](http://mojo.codehaus.org/appassembler/appassembler-maven-plugin/) permet de créer un répertoire _target/appass_ _embler_ qu’il suffit de copier/coller pour installer l’application. Ce dernier contient 3 sous-répertoires :

1. **bin**: scripts start.sh, start.bat, stop.sh et stop.bat permettant de démarrer / arrêter la webapp. Ces scripts se chargent de trouver le JRE, sont compatibles avec cygwin et positionnent le classpath.
1. **conf**: facultatif, ce répertoire contient la configuration de l’application (fichiers properties ou YAML, logback.xml …)
1. **lib**: tous les JARs nécessaires au fonctionnement de l’application

Activé par défaut, le profile maven _appassembler_ regroupe la configuration nécessaire :

```xhtml
<profile>
    <id>appassembler</id>
    <activation>
        <activeByDefault>true</activeByDefault>
    </activation>
    <build>
        <plugins>
            <!-- Generate both Windows and Linux bash shell execution scripts -->
            <plugin>
                <groupId>org.codehaus.mojo</groupId>
                <artifactId>appassembler-maven-plugin</artifactId>
                <version>${version.plugin.appassembler-maven-plugin}</version>
                <executions>
                    <execution>
                        <goals>
                            <goal>assemble</goal>
                        </goals>
                    </execution>
                </executions>
                <configuration>
                    <repositoryLayout>flat</repositoryLayout>
                    <useWildcardClassPath>true</useWildcardClassPath>
                    <!-- Set the target configuration directory to be used in the bin scripts -->
                    <configurationDirectory>conf</configurationDirectory>
                    <!-- Copy the contents from "/src/main/config" to the target
                         configuration directory in the assembled application -->
                    <copyConfigurationDirectory>true</copyConfigurationDirectory>
                    <!-- Include the target configuration directory in the beginning of
                         the classpath declaration in the bin scripts -->                    <includeConfigurationDirectoryInClasspath>true</includeConfigurationDirectoryInClasspath>

                    <!-- Extra JVM arguments that will be included in the bin scripts -->
                    <extraJvmArguments>-Xmx1024m</extraJvmArguments>

                    <programs>
                        <program>
                            <id>start</id>
                            <mainClass>com.javaetmoi.jetty.JettyServer</mainClass>
                            <name>start</name>
                        </program>
                        <program>
                            <id>stop</id>
                            <mainClass>com.javaetmoi.jetty.Stop</mainClass>
                            <name>stop</name>
                        </program>
                    </programs>
                    <binFileExtensions>
                        <unix>.sh</unix>
                    </binFileExtensions>
                </configuration>
            </plugin>
        </plugins>
    </build>
</profile>
```

Voici les commandes à exécuter pour tester ce type de packaging :

```sh
git clone git://github.com/arey/embedded-jetty-webapp.git
cd embedded-jetty-webapp
mvn clean install
target/appassembler/bin/start.sh &
curl http://localhost:8080/HelloWorld
target/appassembler/bin/stop.sh
```

1. **Assembly**

L’une des fonctionnalités offertes par le [plugin Assembly pour Maven](http://maven.apache.org/plugins/maven-assembly-plugin/) est de rassembler tous les JAR d’une application en un seul gros JAR couramment suffixé par _jar-with-dependencies_ (exemple : jetty-webapp-1.0.0-SNAPSHOT-jar-with-dependencies.jar). Afin de rendre ce JAR auto-exécutable, sa class main doit être spécifier dans son manifeste.

Voici la configuration du profile maven _flatjar_:

```xhtml
<profile>
    <id>fatjar</id>
    <build>
        <plugins>
            <plugin>
                <artifactId>maven-assembly-plugin</artifactId>
                <version>${version.plugin.maven-assembly-plugin}</version>
                <configuration>
                    <descriptorRefs>
                        <descriptorRef>jar-with-dependencies</descriptorRef>
                    </descriptorRefs>
                    <archive>
                        <manifest>
                            <mainClass>com.javaetmoi.jetty.JettyServer</mainClass>
                        </manifest>
                    </archive>
                </configuration>
                <executions>
                    <execution>
                        <id>make-assembly</id>
                        <phase>package</phase>
                        <goals>
                            <goal>single</goal>
                        </goals>
                    </execution>
                </executions>
            </plugin>
        </plugins>
    </build>
</profile>
```

Voici les commandes à exécuter pour tester ce type de packaging :

```sh
git clone git://github.com/arey/embedded-jetty-webapp.git
cd embedded-jetty-webapp
mvn clean install -Pflatjar
java -jar target/jetty-webapp-1.0.0-SNAPSHOT-jar-with-dependencies.jar &
curl http://localhost:8080/HelloWorld
java -cp target/jetty-webapp-1.0.0-SNAPSHOT-jar-with-dependencies.jar com.javaetmoi.jetty.Stop
```

## Conclusion

Par cet article, j’espère vous avoir convaincu de la facilité d’embarquer Jetty dans n'importe quelle web app. [Tomcat s’intègre d’une manière similaire](https://devcenter.heroku.com/articles/create-a-java-web-application-using-embedded-tomcat).
Avec cette approche, la mise à jour de Jetty ne nécessite qu’une simple montée de version de Jetty dans le pom.xml

Autre atout : l’exécution d’un Jetty au démarrage de son application est profitable lors du développement. En effet, il n’est plus nécessaire d’installer et/ou d’utiliser le moindre plugin dans son IDE. L’application web est démarrée par un simple _Run_ ou _Debug_ sur la classe _main_.

Références :

- [Appassembler maven plugin](http://mojo.codehaus.org/appassembler/appassembler-maven-plugin/)
- [Eclipse Maven Jetty Plugin](https://github.com/eclipse/jetty.project)
- [Apache Assembly Maven Plugin](http://maven.apache.org/plugins/maven-assembly-plugin/)
- [WAR-less Java Web Apps de James Ward](http://www.jamesward.com/2011/08/23/war-less-java-web-apps)
