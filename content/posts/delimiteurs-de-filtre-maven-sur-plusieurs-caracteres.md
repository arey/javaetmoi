---
_edit_last: "1"
author: admin
categories:
  - maven
date: "2012-07-22T16:24:28+00:00"
guid: http://javaetmoi.com/?p=205
parent_post_id: null
post_id: "205"
post_views_count: "6130"
summary: |-
  ## Contexte

  Chez mon client, les **fichiers de configuration** sont **variabilisés** (ex : fichiers de configuration logback, hosts des différents référentiels et back office, paramétrage applicatif, configuration ehcache …). Cette technique permet d’avoir le **même gabarit quel que soit l’environnement** sur lequel est déployée l’application (ex : intégration, recette, production). Charge à l’outil de déploiement de générer le fichier de configuration final à partir du gabarit et du fichier de variables spécifiques à l’environnement cible sur lequel le déploiement s’effectue.
tags:
  - maven
title: Délimiteurs de filtre maven sur plusieurs caractères
url: /2012/07/delimiteurs-de-filtre-maven-sur-plusieurs-caracteres/

---
## Contexte

Chez mon client, les **fichiers de configuration** sont **variabilisés** (ex : fichiers de configuration logback, hosts des différents référentiels et back office, paramétrage applicatif, configuration ehcache …). Cette technique permet d’avoir le **même gabarit quel que soit l’environnement** sur lequel est déployée l’application (ex : intégration, recette, production). Charge à l’outil de déploiement de générer le fichier de configuration final à partir du gabarit et du fichier de variables spécifiques à l’environnement cible sur lequel le déploiement s’effectue.

Peu souple, l’ **outil de déploiement délimite** les variables du gabarit par un **double caractère @** qu’il n’est pas possible de redéfinir. Exemple : @@PROJECT\_LOG\_DIRECTORY@@
En développement, sur un environnement Windows, la variable PROJECT\_LOG\_DIRECTORY  peut prendre par exemple la valeur c:\\temp\\log\\myapp alors qu’en production, sur un serveur Linux, elle aura la valeur /app/log/myapp

Comme vous pouvez vous en douter, l’outil de déploiement n’est pas utilisé en développement pour déployer son application depuis Eclipse. Cependant, les gabarits des fichiers de configuration sont réutilisés (et donc testés). Utilisé pour les tâches de build, c’est tout naturellement **maven** qui a la responsabilité de substituer les variables par leurs valeurs. Le répertoire contenant les fichiers de configuration générés est ajouté au classpath de l’application.

## Le maven resources plugin en action

Nativement, maven est capable de filtrer des ressources. La **balise _<resources>_** spécifiée dans la XSD 4.0.0 de maven permet de déclarer une liste de répertoire contenant les ressources (dont les fichiers de configuration font parties). La **balise <filters>** permet quant à elle de lister les fichiers filtres qui seront utilisés pendant la phase _process-resources_ de maven, cette dernière étant chargée de copier et filtrer les fichiers de ressources vers le répertoire cible.

En interne, ce mécanisme repose sur le plugin [maven-resources-plugin](http://maven.apache.org/plugins/maven-resources-plugin/). Deux délimiteurs sont positionnés par défaut :

```xhtml
<delimiters>
 <delimiter>${*}</delimiter>
  <delimiter>@</delimiter>   <!-- equivalent à @*@ -->
</delimiters>
```

Depuis la version 2.4 du plugin, il est possible de redéfinir les délimiteurs. La syntaxe à utiliser est la suivante : **_'beginToken\*endToken'_**. Lorsque les tokens de début et de fin sont identiques, la syntaxe est simplifiée : _'token'_.

Certain d’être sur la bonne piste, j’ai tenté de redéfinir le délimiteur pour coller à mon besoin. Hélas, la déclaration d’un délimiteur @@\*@@ ne fonctionne pas. Le plugin semble limité à la définition d’un seul caractère pour le token de fin.

Qu’à cela ne tienne, un svn checkout [http://svn.apache.org/viewvc/maven/shared/tags/maven-filtering-1.0](http://svn.apache.org/viewvc/maven/shared/tags/maven-filtering-1.0) et me voilà rapidement entrainé dans les méandres de la classe _org.apache.maven.shared.filtering.MultiDelimiterInterpolatorFilterReaderLineEnding_

Si j’avais eu plus de temps devant moi, j’aurais pu tenter d’améliorer son fonctionnement, voire proposer un patch à la communauté. Seulement, il m’aurait été difficile de déployer une version de maven patchée sur l’ensemble des postes de développement et encore moins sur la plateforme d’intégration continue. Il me fallait une solution plus facile à mettre en œuvre et bien plus rapide à déployer.

## Le plugin maven replacer à la rescousse

Changeons de stratégie : au lieu de demander au [maven-resources-plugin](http://maven.apache.org/plugins/maven-resources-plugin/) d’accepter le délimiteur @@, autant lui fournir directement un fichier qu’il saura nativement consommer avec un simple @ pour délimiteur.
C’est dans ces moments que l’on est heureux d’utiliser un outil ayant un écosystème aussi riche. L’opération recherchée est précisément la fonction du [maven-replacer-plugin](http://code.google.com/p/maven-replacer-plugin/) hébergé sur Google Code.

Afin d’être exécuté avant l’opération de filtrage, le goal replace du [maven-replacer-plugin](http://code.google.com/p/maven-replacer-plugin/) est associé à la phase _generate-resources_ de maven. Le plugin est configuré pour substituer les caractères @@ en @. Les fichiers sont générés dans le répertoire target/generated-resources. Ce dernier sera utilisé en entrée du [maven-resources-plugin](http://maven.apache.org/plugins/maven-resources-plugin/)  pour filtrer et copier les ressources dans le répertoire target/classes lors de la phase _process-resources_.

Voici un exemple concret de configuration maven :

## Contexte

Chez mon client, les **fichiers de configuration** sont **variabilisés** (ex : fichiers de configuration logback, hosts des différents référentiels et back office, paramétrage applicatif, configuration ehcache …). Cette technique permet d’avoir le **même gabarit quel que soit l’environnement** sur lequel est déployée l’application (ex : intégration, recette, production). Charge à l’outil de déploiement de générer le fichier de configuration final à partir du gabarit et du fichier de variables spécifiques à l’environnement cible sur lequel le déploiement s’effectue.
<!--more-->
Peu souple, l’ **outil de déploiement délimite** les variables du gabarit par un **double caractère @** qu’il n’est pas possible de redéfinir. Exemple : @@PROJECT\_LOG\_DIRECTORY@@
En développement, sur un environnement Windows, la variable PROJECT\_LOG\_DIRECTORY  peut prendre par exemple la valeur c:\\temp\\log\\myapp alors qu’en production, sur un serveur Linux, elle aura la valeur /app/log/myapp

Comme vous pouvez vous en douter, l’outil de déploiement n’est pas utilisé en développement pour déployer son application depuis Eclipse. Cependant, les gabarits des fichiers de configuration sont réutilisés (et donc testés). Utilisé pour les tâches de build, c’est tout naturellement **maven** qui a la responsabilité de substituer les variables par leurs valeurs. Le répertoire contenant les fichiers de configuration générés est ajouté au classpath de l’application.

## Le maven resources plugin en action

Nativement, maven est capable de filtrer des ressources. La **balise _<resources>_** spécifiée dans la XSD 4.0.0 de maven permet de déclarer une liste de répertoire contenant les ressources (dont les fichiers de configuration font parties). La **balise <filters>** permet quant à elle de lister les fichiers filtres qui seront utilisés pendant la phase _process-resources_ de maven, cette dernière étant chargée de copier et filtrer les fichiers de ressources vers le répertoire cible.

En interne, ce mécanisme repose sur le plugin [maven-resources-plugin](http://maven.apache.org/plugins/maven-resources-plugin/). Deux délimiteurs sont positionnés par défaut :

```xhtml
<delimiters>
 <delimiter>${*}</delimiter>
  <delimiter>@</delimiter>   <!-- equivalent à @*@ -->
</delimiters>
```

Depuis la version 2.4 du plugin, il est possible de redéfinir les délimiteurs. La syntaxe à utiliser est la suivante : **_'beginToken\*endToken'_**. Lorsque les tokens de début et de fin sont identiques, la syntaxe est simplifiée : _'token'_.

Certain d’être sur la bonne piste, j’ai tenté de redéfinir le délimiteur pour coller à mon besoin. Hélas, la déclaration d’un délimiteur @@\*@@ ne fonctionne pas. Le plugin semble limité à la définition d’un seul caractère pour le token de fin.

Qu’à cela ne tienne, un svn checkout [http://svn.apache.org/viewvc/maven/shared/tags/maven-filtering-1.0](http://svn.apache.org/viewvc/maven/shared/tags/maven-filtering-1.0) et me voilà rapidement entrainé dans les méandres de la classe _org.apache.maven.shared.filtering.MultiDelimiterInterpolatorFilterReaderLineEnding_

Si j’avais eu plus de temps devant moi, j’aurais pu tenter d’améliorer son fonctionnement, voire proposer un patch à la communauté. Seulement, il m’aurait été difficile de déployer une version de maven patchée sur l’ensemble des postes de développement et encore moins sur la plateforme d’intégration continue. Il me fallait une solution plus facile à mettre en œuvre et bien plus rapide à déployer.

## Le plugin maven replacer à la rescousse

Changeons de stratégie : au lieu de demander au [maven-resources-plugin](http://maven.apache.org/plugins/maven-resources-plugin/) d’accepter le délimiteur @@, autant lui fournir directement un fichier qu’il saura nativement consommer avec un simple @ pour délimiteur.
C’est dans ces moments que l’on est heureux d’utiliser un outil ayant un écosystème aussi riche. L’opération recherchée est précisément la fonction du [maven-replacer-plugin](http://code.google.com/p/maven-replacer-plugin/) hébergé sur Google Code.

Afin d’être exécuté avant l’opération de filtrage, le goal replace du [maven-replacer-plugin](http://code.google.com/p/maven-replacer-plugin/) est associé à la phase _generate-resources_ de maven. Le plugin est configuré pour substituer les caractères @@ en @. Les fichiers sont générés dans le répertoire target/generated-resources. Ce dernier sera utilisé en entrée du [maven-resources-plugin](http://maven.apache.org/plugins/maven-resources-plugin/)  pour filtrer et copier les ressources dans le répertoire target/classes lors de la phase _process-resources_.

Voici un exemple concret de configuration maven :
\[gist id=3124220\]

Dans le répertoire src/main/resources/configuration, on peut retrouver par exemple un fichier application.properties ressemblant à :

```css
log.directory=@@APPLICATION_LOG_DIRECTORY@@
reporting.email=@@SUPPORT_EMAIL@@
backoffice.url=http://@@BACK_OFFICE_HOST@@
```

Et voici à quoi ressemblerait le fichier associé src/main/filters/dev.properties :

```css
APPLICATION_LOG_DIRECTORY=c:/temp/log/myapp
SUPPORT_EMAIL=dev-team@myapp.com
BACK_OFFICE_HOST=my.backoffice.com
```

Utilisée depuis plusieurs mois, cette solution a démontré sa viabilité. Notez tout de même un point de vigilance consistant à ne pas utiliser de caractère @ dans les gabarits.

## Conclusion

Sans prétention, cet article permet de se confronter à la fois à la rigidité et à la souplesse de maven :

- **Rigidité** dans le sens où lorsqu’un plugin ne sait pas faire ce qu’on essaie de lui demander,  maven n’offre pas de points d’extension (ex : par scripting, plugins de plugins).
- **Souplesse** par la possibilité de faire fonctionner de pair plusieurs plugins : la sortie de l’un est l’entrée de l’autre, retrouvant ainsi une certaine similarité avec les pipes sous linux.

Seul regret : le temps passer à rédiger ce billet aurait peut-être dû être employé à debugger la classe _MultiDelimiterInterpolatorFilterReaderLineEnding_.

Dans le répertoire src/main/resources/configuration, on peut retrouver par exemple un fichier application.properties ressemblant à :

```css
log.directory=@@APPLICATION_LOG_DIRECTORY@@
reporting.email=@@SUPPORT_EMAIL@@
backoffice.url=http://@@BACK_OFFICE_HOST@@
```

Et voici à quoi ressemblerait le fichier associé src/main/filters/dev.properties :

```css
APPLICATION_LOG_DIRECTORY=c:/temp/log/myapp
SUPPORT_EMAIL=dev-team@myapp.com
BACK_OFFICE_HOST=my.backoffice.com
```

Utilisée depuis plusieurs mois, cette solution a démontré sa viabilité. Notez tout de même un point de vigilance consistant à ne pas utiliser de caractère @ dans les gabarits.

## Conclusion

Sans prétention, cet article permet de se confronter à la fois à la rigidité et à la souplesse de maven :

- **Rigidité** dans le sens où lorsqu’un plugin ne sait pas faire ce qu’on essaie de lui demander,  maven n’offre pas de points d’extension (ex : par scripting, plugins de plugins).
- **Souplesse** par la possibilité de faire fonctionner de pair plusieurs plugins : la sortie de l’un est l’entrée de l’autre, retrouvant ainsi une certaine similarité avec les pipes sous linux.

Seul regret : le temps passer à rédiger ce billet aurait peut-être dû être employé à debugger la classe _MultiDelimiterInterpolatorFilterReaderLineEnding_.
