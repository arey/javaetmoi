---
_edit_last: "1"
author: admin
categories:
  - retour-d'expérience
date: "2015-12-04T07:27:57+00:00"
guid: http://javaetmoi.com/?p=1488
parent_post_id: null
post_id: "1488"
post_views_count: "6683"
summary: |-
  [![editorconfig-stickers](http://javaetmoi.com/wp-content/uploads/2015/11/editorconfig-stickers.png)](http://javaetmoi.com/wp-content/uploads/2015/11/editorconfig-stickers.png) Lors du démarrage d’un projet sur lequel plusieurs développeurs vont être amenés à travailler, se pose très tôt la question des **styles et règles de formatage** à appliquer au code. En effet, afin de pouvoir comparer l’historique des révisions d’un fichier, une bonne pratique veut que l’on ne change pas les règles de formatage au cours de route. Si tel était le cas, les changements importants seraient noyés par les changements d’indentations et autres retours à la ligne.
  Parmi les normes de développements d’une entreprise ou d’un projet Open Source, un chapitre couvre généralement les règles de formatage. C’est par exemple le cas du [guide de style de code](https://github.com/spring-projects/spring-framework/wiki/Spring-Framework-Code-Style) du projet Spring Framework. Ces règles peuvent également être définies au sein d’un outil de qualimétrie comme [SonarQube](http://nemo.sonarqube.org/coding_rules#qprofile=java-sonar-way-45126|activation=true). Chaque violation de règle entraine alors un défaut.
  Ce **billet propose 2 solutions** permettant à des développeurs [IntelliJ](https://www.jetbrains.com/idea/), [Spring Tools Suite](https://spring.io/tools) (STS) et [Eclipse](https://eclipse.org/home/index.php) de travailler ensemble.
tags:
  - eclipse
  - editorconfig
  - intellij
title: Formatez votre code
url: /2015/12/formatez-votre-code-editorconfig/

---
[![editorconfig-stickers](/wp-content/uploads/2015/11/editorconfig-stickers.png)](/wp-content/uploads/2015/11/editorconfig-stickers.png) Lors du démarrage d’un projet sur lequel plusieurs développeurs vont être amenés à travailler, se pose très tôt la question des **styles et règles de formatage** à appliquer au code. En effet, afin de pouvoir comparer l’historique des révisions d’un fichier, une bonne pratique veut que l’on ne change pas les règles de formatage au cours de route. Si tel était le cas, les changements importants seraient noyés par les changements d’indentations et autres retours à la ligne.
Parmi les normes de développements d’une entreprise ou d’un projet Open Source, un chapitre couvre généralement les règles de formatage. C’est par exemple le cas du [guide de style de code](https://github.com/spring-projects/spring-framework/wiki/Spring-Framework-Code-Style) du projet Spring Framework. Ces règles peuvent également être définies au sein d’un outil de qualimétrie comme [SonarQube](http://nemo.sonarqube.org/coding_rules#qprofile=java-sonar-way-45126|activation=true). Chaque violation de règle entraine alors un défaut.
Ce **billet propose 2 solutions** permettant à des développeurs [IntelliJ](https://www.jetbrains.com/idea/), [Spring Tools Suite](https://spring.io/tools) (STS) et [Eclipse](https://eclipse.org/home/index.php) de travailler ensemble.

## Le formateur Eclipse

Nativement, Eclipse embarque un formateur de code source Java bien connu des développeurs. Afin de pouvoir partager des règles de formatage, il propose des [fonctionnalités d’import / export](http://help.eclipse.org/mars/index.jsp?topic=%2Forg.eclipse.jdt.doc.user%2Freference%2Fpreferences%2Fjava%2Fcodestyle%2Fref-preferences-formatter.htm). Au format XML, le fichier décrivant les règles de formatage est très répandu. Par exemple, le projet [Spring AMQP](http://projects.spring.io/spring-amqp/) fournit le fichier [eclipse-code-formatter.xml](https://github.com/spring-projects/spring-amqp/blob/master/eclipse-code-formatter.xml). Ces règles peuvent être importés dans STS mais également dans IntelliJ IDEA via le plugin [**Eclipse Code Formater**](https://plugins.jetbrains.com/plugin/6546). Afin qu’aucune différence ne puisse être constaté entre du code formaté sous Eclipse et sous IntelliJ, ce plugin embarque directement le code du formateur d’Eclipse. Il existe un [plugin similaire pour Netbeans](http://plugins.netbeans.org/plugin/50877/eclipse-code-formatter-for-java), mais je ne l’ai jamais testé.

La principale limite du plugin Eclipse Code Formater réside dans le nombre de langages supportés : Java, GWT et JavaScript. Autrement dit, vos fichiers XML, pages JSP, HTML, et autres feuilles de styles CSS ne seront pas pris en compte. Le plugin est dépendant des fonctionnalités d’export d’Eclipse. Par exemple, il n’est actuellement pas possible d’exporter les règles de formatage du XML.

## EditorConfig

J’ai découvert l’outil [**EditorConfig**](http://editorconfig.org/) suite à une [pull request](https://github.com/spring-projects/spring-petclinic/pull/93) réalisée sur le projet Spring Petclinic. Cet outil a fait ses preuves puisque de [nombreux projets Open Source l’ont adopté](https://github.com/editorconfig/editorconfig/wiki/Projects-Using-EditorConfig) : AngularJS, Jenkins, Bootstrap, Wordpress …

La configuration d’EditorConfig est bien plus restreinte que celle du formateur d’Eclipse : seulement [8 paramètres](https://github.com/editorconfig/editorconfig/wiki/EditorConfig-Properties) dont le style d’indentation (espace ou tabulation), le nombre d’indentations, ou bien la suppression des espaces superflus en fin de ligne.
Là où il se distingue, c’est de pouvoir fixer l’encodage des fichiers et le type de retour à la ligne (Unix, Windows).
Sa configuration est simple. Voici le fichier **_.editorconfig_** mis en place sur Petclinic :

```default
# Configuration racine pouvant être affinée pour chaque sous-répertoire
root = true

# Section de configuration valable pour tous les types de fichiers
[*]

# Encodage de des fichiers
charset = utf-8

# Fin de ligne à la Linux
end_of_line = lf

# Insère une ligne à la fin des fichiers
insert_final_newline = true

# Caractère espace pour indentater
indent_style = space

# Section de configuration spécifique aux classes Java et aux fichiers XML
[*.{java,xml}]

# Nombre d’espaces d’indentation
indent_size = 4

# Suppression des espaces de fin
trim_trailing_whitespace = true
```

Le principal avantage d’EditorConfig est le nombre d’éditeur de code supporté. [Pas moins de 27](http://editorconfig.org/#download). Certains nativement comme IntelliJ, WebStorm ou [GitHub](https://github.com/editorconfig/editorconfig.github.com/pull/48). Pour Eclipse, Netbeans ou encore Notepadd++, [l’installation d’un plugin](http://editorconfig.org/#download) sera nécessaire.

## Conclusion

Ce modeste billet vous aura montré 2 moyens de partager la configuration de vos formateurs, et ceci quel que soit votre IDE Java.
Pour des besoins simples, sur des projets multi-technos, EditorConfig est un bon candidat. Il convient également aux développeurs détestant que leur code soit formaté.
Pour une application d’Entreprise centrée sur Java, l’utilisation du formateur Eclipse reste à mon avis le meilleur choix.
