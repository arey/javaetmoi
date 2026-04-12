---
_edit_last: "1"
author: admin
categories:
  - maven
  - test
date: "2014-03-04T09:27:15+00:00"
thumbnail: wp-content/uploads/2014/03/tester-code-javascript-webapp-logo.png
featureImage: wp-content/uploads/2014/03/tester-code-javascript-webapp-logo.png
featureImageAlt: "tester-code-javascript-webapp-logo"
guid: http://javaetmoi.com/?p=995
parent_post_id: null
post_id: "995"
post_views_count: "12511"
summary: |-
  [![tester-code-javascript-webapp-logo](http://javaetmoi.com/wp-content/uploads/2014/03/tester-code-javascript-webapp-logo.png)](http://javaetmoi.com/wp-content/uploads/2014/03/tester-code-javascript-webapp-logo.png) Vous développez une **application web** en **Java**. Le couche présentation est assurée typiquement par un **framework MVC** situé côté **serveur** : Spring MVC, Struts 2, Tapestry ou bien encore JSF.  Votre projet est parfaitement industrialisé : infrastructure de build sous maven, intégration continue, tests unitaires, tests Selenium, analyse qualimétrique via Sonar.

  A priori, vous n’avez rien à envier à la richesse grandissante de l’écosystème JavaScript, de l’outillage et des frameworks MV\* côté clients. Et pourtant, quelque chose vous manque cruellement. En effet, depuis que RIA et Ajax se sont imposés, votre application Java contient davantage de code JavaScript qu’il y’a 10 ans. S’appuyant sur des librairies telles que jQuery ou Underscore, ce code JavaScript est typiquement embarqué dans votre **WAR**. Pour le valider, les développeurs doivent démarrer leur conteneur web et accéder à l’écran sur lequel le code est utilisé. Firebug ou Chrome sont alors vos meilleurs amis pour la mise au point du script.

  Ce code JavaScript n’est généralement pas documenté. Le tester manuellement demande du temps.  Les modifications sont sources d’erreur. Tout changement est donc périlleux. Si, à l’instar de vos tests JUnit pour vous classes Java, vous disposiez de **tests JavaScript**, vous en seriez comblés. Or, c’est précisément ce qu’il vous manque. Et c’est là où **Jasmine** et **son plugin maven** viennent à votre rescousse.

  ![tester-code-javascript-webapp-logo](wp-content/uploads/2014/03/tester-code-javascript-webapp-logo.png)
tags:
  - htmlunit
  - jasmine
  - javascript
  - maven
  - phantomjs
  - saga
  - selenium
  - test
title: Tester le code JavaScript de vos webapp Java
url: /2014/03/tester-code-javascript-webapp-java/

---
[![tester-code-javascript-webapp-logo](wp-content/uploads/2014/03/tester-code-javascript-webapp-logo.png)](wp-content/uploads/2014/03/tester-code-javascript-webapp-logo.png) Vous développez une **application web** en **Java**. Le couche présentation est assurée typiquement par un **framework MVC** situé côté **serveur** : Spring MVC, Struts 2, Tapestry ou bien encore JSF.  Votre projet est parfaitement industrialisé : infrastructure de build sous maven, intégration continue, tests unitaires, tests Selenium, analyse qualimétrique via Sonar.

A priori, vous n’avez rien à envier à la richesse grandissante de l’écosystème JavaScript, de l’outillage et des frameworks MV\* côté clients. Et pourtant, quelque chose vous manque cruellement. En effet, depuis que RIA et Ajax se sont imposés, votre application Java contient davantage de code JavaScript qu’il y’a 10 ans. S’appuyant sur des librairies telles que jQuery ou Underscore, ce code JavaScript est typiquement embarqué dans votre **WAR**. Pour le valider, les développeurs doivent démarrer leur conteneur web et accéder à l’écran sur lequel le code est utilisé. Firebug ou Chrome sont alors vos meilleurs amis pour la mise au point du script.

Ce code JavaScript n’est généralement pas documenté. Le tester manuellement demande du temps.  Les modifications sont sources d’erreur. Tout changement est donc périlleux. Si, à l’instar de vos tests JUnit pour vous classes Java, vous disposiez de **tests JavaScript**, vous en seriez comblés. Or, c’est précisément ce qu’il vous manque. Et c’est là où **Jasmine** et **son plugin maven** viennent à votre rescousse.

## Présentation de Jasmine

Les développeurs AngularJS le connaissent déjà. Mis au point par Pivotal (ex SpringSource), **[Jasmine](https://github.com/pivotal/jasmine/)** est un **framework de tests unitaires** pour **JavaScript** et CoffeeScript. Contrairement à [QUnit](https://qunitjs.com/) qui est a été initialement créé pour tester le projet jQuery, Jasmine est indépendant de tout framework JavaScript. Son principal avantage réside dans le fait qu’il ne nécessite pas de navigateur pour exécuter les tests : un simple moteur JavaScript suffit.

Complet, Jasmine offre tout l’outillage nécessaire à l’écriture de tests :
**Fonctionnalité****Description****Frameworks Java équivalent****Structuration des tests**Suite de tests (describe), fonctions de tests (it), setUp et tearDown, ignoreJUnit, TestNG**Matchers**Fonctions utilisées pour les assertions : expect, toEqual, toBe, not, toBeDefined …Feist Assert, JUnit, Hamcrest**Bouchons**Création d’espions et de simulacres: createSpy, andReturn, andCallFake, toHaveBeenCalled …Mockito
Vous expliquez ici comment écrire des tests avec Jasmine dépasse le cadre de cet article. Je vous renvoie à la [documentation officielle](http://jasmine.github.io/1.3/introduction.html) et au tutorial [Testing JavaScript using the Jasmine framework](http://www.htmlgoodies.com/beyond/javascript/testing-javascript-using-the-jasmine-framework.html).

Dans la suite de cet article, les fichiers Player.js, Song.js, PlayerSpec.js et SpecHelper.js issus de la [version standalone de Jasmine](https://github.com/pivotal/jasmine/tree/master/dist) sont utilisés comme jeu d’exemple.
Pour les adeptes de jQuery, le projet **[jasmine-jquery](https://github.com/velesin/jasmine-jquery)** étend Jasmine de 2 manières :

1. Ajout de matchers liés au DOM : toBeSelected, toContainText, toHaveClass, toContainHtml, toBeVisible ...
1. Initialisation du DOM à partir d’un fichier HTML lors de l’étape de fixture.

Le fichier [PasswordSpec.js](https://github.com/arey/jasmine-test-webapp/blob/billet/src/test/javascript/PasswordSpec.js) en montre un exemple d’utilisation.

## Intégration de Jasmine à maven

Le plugin pour maven **[jasmine-maven-plugin](http://searls.github.com/jasmine-maven-plugin/)** permet d’ **exécuter vos tests Jasmine**(aussi appelés **specs**) lors de la **phase de test** de votre **build maven**.

[![tester-code-javascript-webapp-arbo](wp-content/uploads/2014/03/tester-code-javascript-webapp-arbo.png)](wp-content/uploads/2014/03/tester-code-javascript-webapp-arbo.png) Le **[pom.xml](https://github.com/arey/jasmine-test-webapp/blob/billet/pom.xml)** du projet **[jasmine-test-webapp](https://github.com/arey/jasmine-test-webapp)** donne un exemple de configuration du plugin. Pour mieux comprendre sa configuration, vous présenter l’organisation du projet est nécessaire.

L’arborescence du projet suit les conventions maven d’un war. Pages dynamiques et ressources statiques se trouvent dans le répertoire **_src/main/webapp_**.

Par choix, Le code JavaScript spécifique à l’application est localisé dans le sous-répertoire **_static/js/app_** du répertoire _src/main/webapp_. C’est ce code qui doit être testé.
Les librairies tierces comme ici jQuery sont placées dans un sous-répertoire _static/js/lib_.

Les fichiers de tests JavaScript sont quant à eux placés dans le répertoire **_src/test/javascript_**. Pour utiliser l’extension jasmine-jquery dans les specs, la seule présence du fichier [jasmine-jquery.js](https://github.com/arey/jasmine-test-webapp/blob/master/src/test/javascript/jasmine-jquery.js) suffit.

La configuration associée du **[jasmine-maven-plugin](http://searls.github.com/jasmine-maven-plugin/)** est la suivante :

```java
Configuration du jasmine-maven-plugin
```

Remarque : afin que l’objet $ soit défini lors du chargement du script _Password.js_, la librairie jQuery est chargée en premier.

Voici le résultat de la sortie console de la commande mvn test  :

```sh
[INFO] ------------------------------------------------------------------------
[INFO] Building JavaEtMoi Samples :: jasmine-test-webapp - war 1.0-SNAPSHOT
[INFO] ------------------------------------------------------------------------
...
[INFO]
[INFO] --- maven-surefire-plugin:2.10:test (default-test) @ jasmine-test-webapp ---
[INFO] No tests to run.
...
[INFO] --- jasmine-maven-plugin:1.3.1.4:test (default) @ jasmine-test-webapp ---
[INFO] Executing Jasmine Specs
[INFO]
-------------------------------------------------------
 J A S M I N E   S P E C S
-------------------------------------------------------
[INFO]
password validation label
  should become red when password is too short
  should be green when password length is more then 6 symbols
Player
  should be able to play a Song
  when song has been paused
    should indicate that the song is currently paused
    should be possible to resume
  tells the current song if the user has made it a favorite
  #resume
    should throw an exception if song is already playing
Results: 7 specs, 0 failures
...
[INFO] ------------------------------------------------------------------------
[INFO] BUILD SUCCESS
[INFO] ------------------------------------------------------------------------
[INFO] Total time: 14.035s
[INFO] Finished at: Sat Mar 01 19:26:03 CET 2014
[INFO] Final Memory: 10M/247M
[INFO] ------------------------------------------------------------------------
```

Mise à part l’installation de Java et de Maven, aucun prérequis n’est nécessaire. Magique, vous ne trouvez pas ? Mais alors, comment est interprété le code JavaScript ? Et qui met à disposition le DOM manipulé dans le JavaScript ?
En plus de Jasmine, le jasmine-maven-plugin embarque **[HmtlUnitDriver](https://code.google.com/p/selenium/wiki/HtmlUnitDriver)**, une implémentation de Selenium WebDriver. En interne, HmtlUnitDriver s’appuie sur **[HtmlUnit](http://htmlunit.sourceforge.net/)** pour le DOM et sur Rhino pour le JavaScript. Tous les deux sont écrits en Java et sont Open Source. Initié par la fondation Mozilla, le moteur JavaScript **[Rhino](https://developer.mozilla.org/en-US/docs/Rhino)** a été intégré à Java 6.
Respectant le standard HTML, HmtlUnitDriver permet d’émuler des spécificités de certains navigateurs.
Jasmine-maven-plugin permet de tirer parti cette fonctionnalité. A sa configuration, il est possible d’ajouter la balise suivante : <browserVersion>FIREFOX\_17</browserVersion>

## Behavior-Driven Development

Le plugin [jasmine-maven-plugin](http://searls.github.io/jasmine-maven-plugin/) permet de développer en TDD sans avoir à lancer un clean test à chaque changement de code.
La commande mvn jasmine:bdd  lance un serveur web qui scrute tout changement dans le répertoire du code JavaScript et des tests JavaScript. Rafraichir la fenêtre de son navigateur permet de réexécuter les tests.

[![tester-code-javascript-webapp-bdd](wp-content/uploads/2014/03/tester-code-javascript-webapp-bdd.png)](wp-content/uploads/2014/03/tester-code-javascript-webapp-bdd.png)

## Couverture de tests

A présent que [jasmine-maven-plugin](http://searls.github.io/jasmine-maven-plugin/) est en place sur votre projet, vous pouvez en profiter pour générer à moindre coût la couverture du code JavaScript testé. En effet,  ce plugin s’interface avec le **[saga-maven-plugin](http://timurstrekalov.github.io/saga/)**.
Par la ligne de configuration suivante, on indique au jasmine-maven-plugin de ne pas arrêter le serveur web une fois les tests unitaires exécutés :

<keepServerAlive>true</keepServerAlive>

La configuration du [saga-maven-plugin](http://timurstrekalov.github.io/saga/) est triviale et très [bien documentée](http://timurstrekalov.github.io/saga/) :

```java
Configuration du saga-maven-plugin
```

Des **rapports Cobertura** et **HTML** sont générés dans le sous-répertoire _target/coverage_ pendant la **phase verify** de maven :
[![tester-code-javascript-webapp-saga](wp-content/uploads/2014/03/tester-code-javascript-webapp-saga.png)](wp-content/uploads/2014/03/tester-code-javascript-webapp-saga.png)

## Utilisation de PhantomJS

Le principal inconvénient de la solution présentée jusqu’ici est que ni HtmlUnit ni Rhino ne sont  utilisés par un quelconque navigateur du marché. Comment être certain que votre code s’exécute sur un Chrome ou un Safari ? C’est là que **PhantomJS** rentre en jeu. En effet, PhantomJS est un navigateur headless (sans interface graphique) basé sur WebKit (le moteur HTML de Safari, d’Opera et du fork de Chrome). Le plugin Jasmine pour maven permet d’ [utiliser PhantomJS à la place de HtmlUnit](http://searls.github.io/jasmine-maven-plugin/phantomjs.html).

Pour utiliser PhantomJS, il est tout d’abord nécessaire de l’installer. Une archive existe pour chaque OS supporté : Windows, MacOSX, Linux 32 bits et 64 bits. Afin que maven puisse installer l’archive PhantomJS de l’OS sur lequel le build est exécuté, il est possible d’uploader ces archives dans votre repo d’entreprise (ex : Nexus, Artifactory). Voici un exemple de commande maven :

```default
mvn deploy:deploy-file -DgroupId=org.phantomjs -DartifactId=phantomjs -Dversion=1.9.7 -Dpackaging=zip -Dclassifier=windows -Dfile=phantomjs-1.9.7-windows.zip -DrepositoryId=javaetmoi-cloudbees-release -Durl=https://repository-javaetmoi.forge.cloudbees.com/release/
```

Une fois déployées, les archives sont disponibles dans le répertoire [org/phantomjs/phantomjs/1.9.7/](https://repository-javaetmoi.forge.cloudbees.com/release/org/phantomjs/phantomjs/1.9.7/)

Le **goal unpack** du plugin **[maven-dependency-plugin](http://maven.apache.org/plugins/maven-dependency-plugin/)** permet d’installer PhantomJS dans le répertoire _target/_ pendant la **phase initialize** de la commande mvn test  :

```xhtml
<plugin>
  <groupId>org.apache.maven.plugins</groupId>
  <artifactId>maven-dependency-plugin</artifactId>
  <executions>
    <execution>
      <phase>initialize</phase>
      <goals>
        <goal>unpack</goal>
      </goals>
      <configuration>
        <artifactItems>
          <artifactItem>
            <groupId>org.phantomjs</groupId>
            <artifactId>phantomjs</artifactId>
            <version>1.9.7</version>
            <type>zip</type>
            <classifier>windows</classifier>
            <outputDirectory>${project.build.directory}</outputDirectory>
          </artifactItem>
        </artifactItems>
      </configuration>
    </execution>
  </executions>
</plugin>
```

Une autre solution permettant d’installer automatiquement PhantomjS consiste à utiliser le [plugin PhantomJS pour maven](http://kylelieber.com/phantomjs-maven-plugin/index.html).

Enfin, pour substituer PhantomJS à HtmlUnit, le jasmine-maven-plugin doit être configuré de la manière suivante :

```xhtml
<webDriverClassName>org.openqa.selenium.phantomjs.PhantomJSDriver</webDriverClassName>
<webDriverCapabilities>
  <capability>
    <name>phantomjs.binary.path</name>
    <value>${project.build.directory}/phantomjs-1.9.7-windows/phantomjs.exe</value>
  </capability>
</webDriverCapabilities>
```

Lorsque des tests échouent, les erreurs remontées par PhantomJS sont, de manière générale, plus compréhensibles que leurs homologues HtmlUnit.
Voici un exemple de message d’erreur lorsqu’on oubli de rajouter la librairie underscore. js et que la variable globale \_ n’est pas définie :

Avec HtmlUnit :

```sh
[ERROR] java.lang.RuntimeException: org.openqa.selenium.WebDriverException: com.gargoylesoftware.htmlunit.ScriptException: TypeError: Impossible dappeler la méthode "{1}" de {0} (script in http://localhost:3213/ from (6, 34) to (15, 12)
```

Avec PhantomJS :

```sh
\[WARNING\] JavaScript Console Errors:
&nbsp; * TypeError: 'undefined' is not an object (evaluating '_.each')
```

Le [pom.xml](https://github.com/arey/jasmine-test-webapp/blob/billet/pom.xml) utilise les profiles maven pour utiliser à la demande PhantomJS. Il installe la version de PhantomJS correspondant à l’OS sur lequel la commande maven est exécutée. Le **profile phantomJS** permet d’exécuter les tests avec PhantomJS :
mvn test -PphantomJS

## Conclusion

Au travers de ce billet, nous avons vu comment intégrer l’exécution de tests unitaires JavaScript dans une infrastructure de build basée sur maven. L’intégration de Jasmine avec maven est telle qu’il n’est nullement nécessaire de mettre en place des outils du monde JavaScript basés sur [Node.JS](http://nodejs.org/) tel [Grunt](http://gruntjs.com/) ou [Gulp](http://gulpjs.com/).
Avec le plugin Jasmine pour maven, vos tests unitaires peuvent aussi  bien tester des fonctions métiers que des fonctions manipulant le DOM du navigateur. En outre, l’intégration de PhantomJS permet de se garantir que le code JavaScript testé fonctionnera sur les navigateurs basés sur WebKit.

Vos tests unitaires JavaScript peuvent dès à présent intégrer votre plateforme d’intégration continue. Preuve en est, les tests unitaires du projet [jasmine-test-webapp](https://github.com/arey/jasmine-test-webapp) ont été exécutés par [Travis CI](https://travis-ci.org/arey/jasmine-test-webapp)  et par le [Jenkins de CloudBees](https://javaetmoi.ci.cloudbees.com/job/jasmine-test-webapp/1/).
