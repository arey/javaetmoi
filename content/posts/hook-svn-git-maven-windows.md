---
_edit_last: "1"
author: admin
categories:
  - maven
date: "2015-01-13T06:29:47+00:00"
guid: http://javaetmoi.com/?p=1286
parent_post_id: null
post_id: "1286"
post_views_count: "4688"
summary: |-
  [![logo-maven](http://javaetmoi.com/wp-content/uploads/2014/12/logo-maven-150x108.gif)](http://javaetmoi.com/wp-content/uploads/2014/12/logo-maven.gif) Désormais ancrées dans le quotidien des développeurs, les plateformes d’ **intégration continue** permettent de détecter rapidement tout problème de compilation, de tests en erreur ou même d’ [ajout de défauts remontés par SonarQube](http://www.sonarqube.org/analysis-vs-preview-vs-incremental-preview-in-sonarqube/). L’objectif fixé par le team leader est de ne pas faire échouer le build et, si c’est malheureusement le cas, tout arrêter pour le réparer. Sur certains projets, le gage donné au développeur ayant cassé le build est de ramener les viennoiseries le lendemain.
  Pour être certain de ne pas faire chauffer sa carte de paiement, **une bonne pratique consiste à exécuter une ligne de commande maven (ou gradle) avant chaque commit dans le gestionnaire de code source**. Cependant, sur certains changements que l’on juge mineur, il peut être tentant de passer outre. Aujourd’hui, les PC ou les Mac multi-coeurs avec SSD permettent de lancer un build sans freezer le poste de développement. C’est donc davantage par excès de confiance qu’à cause du temps d’attente qu’il arrive de casser Jenkins, Bamboo ou bien encore TeamCity.

  Pour contrer tout oubli, il est possible de systématiser l’exécution du build Maven avant de commiter. Les outils de gestion de configuration SVN et Git offrent un mécanisme de hook. Lors de la phase de pre-commit, on va demander au SCM d’exécuter un script de hook chargé de vérifier le code source. En cas d’erreur, le commit est refusé.
  Ecrire de tels scripts n’est pas compliqué sous Linux car beaucoup d’exemples existent. Par contre, **sous Windows**, c’est plus rare. **L’objet d** **e cet article est donc de vous donner des exemples de scripts de hook de pre-commit et de vous expliquer comment les configurer dans Tortoise SVN et Git.**
tags:
  - git
  - maven
  - svn
title: Hook SVN et Git pour Maven sous Windows
url: /2015/01/hook-svn-git-maven-windows/

---
[![logo-maven](/wp-content/uploads/2014/12/logo-maven.gif)](/wp-content/uploads/2014/12/logo-maven.gif) Désormais ancrées dans le quotidien des développeurs, les plateformes d’ **intégration continue** permettent de détecter rapidement tout problème de compilation, de tests en erreur ou même d’ [ajout de défauts remontés par SonarQube](http://www.sonarqube.org/analysis-vs-preview-vs-incremental-preview-in-sonarqube/). L’objectif fixé par le team leader est de ne pas faire échouer le build et, si c’est malheureusement le cas, tout arrêter pour le réparer. Sur certains projets, le gage donné au développeur ayant cassé le build est de ramener les viennoiseries le lendemain.
Pour être certain de ne pas faire chauffer sa carte de paiement, **une bonne pratique consiste à exécuter une ligne de commande maven (ou gradle) avant chaque commit dans le gestionnaire de code source**. Cependant, sur certains changements que l’on juge mineur, il peut être tentant de passer outre. Aujourd’hui, les PC ou les Mac multi-coeurs avec SSD permettent de lancer un build sans freezer le poste de développement. C’est donc davantage par excès de confiance qu’à cause du temps d’attente qu’il arrive de casser Jenkins, Bamboo ou bien encore TeamCity.

Pour contrer tout oubli, il est possible de systématiser l’exécution du build Maven avant de commiter. Les outils de gestion de configuration SVN et Git offrent un mécanisme de hook. Lors de la phase de pre-commit, on va demander au SCM d’exécuter un script de hook chargé de vérifier le code source. En cas d’erreur, le commit est refusé.
Ecrire de tels scripts n’est pas compliqué sous Linux car beaucoup d’exemples existent. Par contre, **sous Windows**, c’est plus rare. **L’objet d** **e cet article est donc de vous donner des exemples de scripts de hook de pre-commit et de vous expliquer comment les configurer dans Tortoise SVN et Git.**

## Hook SVN

 [![logo-svn](/wp-content/uploads/2014/12/logo-svn.png)](/wp-content/uploads/2014/12/logo-svn.png) Deux types de hook existent dans Subversion : des hooks clients et des hooks serveurs.
Pour ne pas transformer le serveur SVN en serveur d’intégration continue, ce sont les hooks clients qui vont ici nous intéresser.
Le script appelé par le hook n’est rien d’autre qu’un .bat.
L’exemple de script _pre-commit.bat_ ci-dessous est localisé dans le même répertoire que le POM reactor du projet. Un pré-requis est que Maven et Java sont dans le PATH de Windows.

```sh
@echo on
call mvn clean –f myapp-parent\pom.xml  > target\pre-commit.log
if not exist target mkdir target
call mvn install sonar:sonar -Dsonar.analysis.mode=preview -Dsonar.issuesReport.html.enable=true -Dsonar.buildbreaker.skip=false –f myapp-parent\pom.xml > target\pre-commit.log
echo Maven error code: %ERROR_CODE%
cmd /C exit /B %ERROR_CODE%
```

Afin de pouvoir être consultée en cas d’échec du build, la sortie console est redirigée dans un fichier de logs. Le code d’erreur de maven est retourné à SVN qui sait l’interpréter. Tout code différent de 0 fait échouer le commit.
Exécuté dans à la racine de l’arborescence, le paramètre _–f myapp-parent\\pom.xml_ permet de spécifier à maven où se trouve le POM parent (structure de type _flat module_). Nul besoin d’ajouter ce paramètre lorsque le POM parent se situe à la racine du projet.

**TortoiseSVN** permet de configurer un hook client à 2 niveaux :

1. De manière globale pour tous les repos SVN du poste de dév. Chaque développeur doit individuellement configurer TortoiseSVN. Cette configuration peut être problématique lorsqu’un développeur est amené à travailler sur plusieurs repos et que le script de hook n’est pas assez générique. Le script précédent devra être généralisé pour fonctionner avec l’ensemble des projets.
1. De manière unitaire pour chaque repo SVN. A l’instar d’une propriété _svn:ignore_, TortoiseSVN ajoute récursivement une propriété **tsn:precommithook** au niveau du repository SVN. Tous les développeurs bénéficient alors de ce hook.

Etapes de configuration du mode global :

1. Depuis n’importe quel répertoire, sélectionner le menu contextuel T _ortoiseSVN > Settings_
1. Se rendre dans le menu _Hook Scripts_
1. Renseigner les champs suivants :
   - Hook type : pre-commit
   - Woking copy path : chemin vers le pom parent de l'application
   - Command line to execute : pre-commit.bat

**[![2014-12-hook-maven-git-svn-sous-windows-svn-hook-global-config](/wp-content/uploads/2014/12/2014-12-hook-maven-git-svn-sous-windows-svn-hook-global-config.jpg)](/wp-content/uploads/2014/12/2014-12-hook-maven-git-svn-sous-windows-svn-hook-global-config.jpg)** Etapes de configuration du mode local :

1. Sélectionner le répertoire racine du projet SVN
1. Ouvrir le menu contextuel et sélectionner le menu _TortoiseSVN > Properties_
1. Cliquer sur le bouton _New > Local Hooks_ (création d'une property tsvn:precommithook)
1. Choisir les paramètres suivants :
   1. Hook Type : Start Commit Hook
   1. Command Line to Execute : %REPOROOT+%/myproject-parent/pre-commit.bat
   1. Cocher les options suivantes :
      1. Wait for the script to finish
      1. Always execute the script
      1. Apply property recursively
1. Commiter ces modifications de manière récursive sur l'ensemble des sous répertoires du projet SVN

[![2014-12-hook-maven-git-svn-sous-windows-svn-hook-local-properties](/wp-content/uploads/2014/12/2014-12-hook-maven-git-svn-sous-windows-svn-hook-local-properties.png)](/wp-content/uploads/2014/12/2014-12-hook-maven-git-svn-sous-windows-svn-hook-local-properties.png) Remarque : les hooks clients sont une fonctionnalité propre à TortoiseSVN. De ce fait, le client en ligne de commande _svn.exe_ ou bien encore le plugin Subversive d’Eclipse ne reconnaissent pas la propriété _tsvn:precommithook_.

## Hook Git

 [![logo-git](/wp-content/uploads/2014/12/logo-git.jpg)](/wp-content/uploads/2014/12/logo-git.jpg) Git appartenant à la catégorie des DVCS, il n’existe pas de hook server. La configuration s’effectue donc au niveau du repository Git local. Les scripts de hook sont à positionner dans le sous-répertoire _.git\\hooks_. Par défaut, ce répertoire contient des exemples post-fixés par l’extension _.sample_. Le nom des scripts est conventionné et correspond au nom de la phase à laquelle il est exécuté. Ainsi, le script de hook exécuté avant le commit se nomme **_pre-commit_**.
Sous Windows, **Msysgit** est le client Git le plus populaire. Basé sur les utilitaires [Msys](http://www.mingw.org/wiki/MSYS), le script ne doitpas être écrit en script batch comme c’est le cas avec SVN, mais en bash Linux.

Voici un exemple de sript shell _pre-commit_ :

```sh
#!/bin/sh
echo "Executing pre-commit"
# Set Java and Maven:
export JAVA_HOME="C:/dev/jdk/1.7.0_45"
export MAVEN_OPTS="-Xmx1024m -XX:MaxPermSize=256m"
export MAVEN_HOME="C:/dev/maven/apache-maven-3.2.3"
echo "Running Maven clean install for errors and Sonar for testing if the project fails its quality gate."
# Retrieving current working directory
CWD=`pwd`
MAIN_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
# Go to main project dir
cd $MAIN_DIR/../../myapp-parent
# Running Maven clean install and Sonar
$MAVEN_HOME/bin/mvn clean install -U sonar:sonar -Dsonar.analysis.mode=preview -Dsonar.issuesReport.html.enable=true -Dsonar.buildbreaker.skip=false
if [ $? -ne 0 ]; then
echo "Error while compiling or testing the code"
# Go back to current working dir
cd $CWD
exit 1
fi
# Go back to current working dir
cd $CWD
exit 0
```

La commande _cd $MAIN\_DIR/../../myapp-parent_ permet de positionner dans le répertoire contenant le POM parent. Ce chemin est à adapter selon la structure du projet.

## Conclusion

Que ce soit avec Git ou avec TortoiseSVN, il est possible de systématiser l’appel à commande _mvn clean install_(ou à tout autre script) avant de commiter. Cette bonne pratique fait en sorte que le code historisé dans le gestionnaire de code source est toujours stable. L’intérêt de maintenir un serveur d’intégration continue peut donc se poser. Dès 2009, David Gageot montrait d’ailleurs qu’il était possible de monter [une intégration continue sans serveur](http://blog.javabien.net/2009/12/01/serverless-ci-with-git/). Pour autant, les serveurs d’intégration continue tels que Jenkins ont aujourd’hui davantage de responsabilités que par le passé : exécution des tests d’intégration, des tests Selenium et des tests de montée en charge, packaging, déploiement d’applications sur les différents environnements … Leurs jours ne sont donc pas comptés !
