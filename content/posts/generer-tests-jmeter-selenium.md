---
_edit_last: "1"
_wp_old_slug: generer-tests-jmeter-a-partir-selenium
author: admin
categories:
  - test
date: "2012-05-26T18:51:06+00:00"
guid: http://javaetmoi.com/?p=166
parent_post_id: null
post_id: "166"
post_views_count: "16653"
summary: |-
  Chez mon client, des **tests de stress** sont réalisés sur toute nouvelle version d’une application. Outre le fait de **qualifier techniquement** l’environnement de pré-production, ces tirs permettent de **détecter toute** **dégradation** des performances et de **prévenir toute montée en charge** induite, par exemple, par une nouvelle fonctionnalité. Plus encore, ils permettent de  mesurer les gains apportés par d’éventuelles optimisations.  Ces tests de stress sont réalisés à l’aide de l’outil [Apache JMeter](http://jmeter.apache.org/) \[1\].

  Afin de pouvoir **comparer des mesures**, les cas fonctionnels utilisés lors des tests doivent, dans la mesure du possible, être identiques aux précédents tirs, sachant que ces derniers peuvent dater de plusieurs mois. Entre temps, nombre d’évolutions ont été susceptibles de casser vos tests JMeter. A priori, vous avez donc 2 choix : soit vous les réécrivez, soit vous les maintenez à jour. Si vous en avez déjà écrit, vous vous doutez bien que maintenir dans la durée des tests JMeter a un cout non négligeable.  Une 3ième solution présentée ici consiste à la générer !

  J’ai la chance de travailler dans une équipe ou l’outil [Selenium](https://selenium.dev/) \[2\] de tests IHM est rentré dans les mœurs. L’automatisation de leur exécution y joue un rôle indéniable. Notre hiérarchie s’est fortement impliquée ; elle a investi de l’énergie et du budget. Un DSL a été mis au point pour faciliter leur écriture et leur maintenance. Alors quand on peut les rentabiliser encore davantage, autant le faire. J’ai donc proposé de ne maintenir que les tests Selenium et de **générer les tests JMeter à partir de tests Selenium**.

  Cet article a pour objectif de vous présenter la démarche adoptée. Si vous êtes intéressés, vous pourrez librement l’adapter en fonction de votre contexte projet.
tags:
  - jmeter
  - selenium
  - test
title: Générer des tests JMeter à partir de Selenium
url: /2012/05/generer-tests-jmeter-selenium/

---
Chez mon client, des **tests de stress** sont réalisés sur toute nouvelle version d’une application. Outre le fait de **qualifier techniquement** l’environnement de pré-production, ces tirs permettent de **détecter toute** **dégradation** des performances et de **prévenir toute montée en charge** induite, par exemple, par une nouvelle fonctionnalité. Plus encore, ils permettent de  mesurer les gains apportés par d’éventuelles optimisations.  Ces tests de stress sont réalisés à l’aide de l’outil [Apache JMeter](http://jmeter.apache.org/) \[1\].

Afin de pouvoir **comparer des mesures**, les cas fonctionnels utilisés lors des tests doivent, dans la mesure du possible, être identiques aux précédents tirs, sachant que ces derniers peuvent dater de plusieurs mois. Entre temps, nombre d’évolutions ont été susceptibles de casser vos tests JMeter. A priori, vous avez donc 2 choix : soit vous les réécrivez, soit vous les maintenez à jour. Si vous en avez déjà écrit, vous vous doutez bien que maintenir dans la durée des tests JMeter a un cout non négligeable.  Une 3ième solution présentée ici consiste à la générer !

J’ai la chance de travailler dans une équipe ou l’outil [Selenium](https://selenium.dev/) \[2\] de tests IHM est rentré dans les mœurs. L’automatisation de leur exécution y joue un rôle indéniable. Notre hiérarchie s’est fortement impliquée ; elle a investi de l’énergie et du budget. Un DSL a été mis au point pour faciliter leur écriture et leur maintenance. Alors quand on peut les rentabiliser encore davantage, autant le faire. J’ai donc proposé de ne maintenir que les tests Selenium et de **générer les tests JMeter à partir de tests Selenium**.

Cet article a pour objectif de vous présenter la démarche adoptée. Si vous êtes intéressés, vous pourrez librement l’adapter en fonction de votre contexte projet.

# Les outils à disposition

## Serveur Proxy HTTP de JMeter

Le client lourd JMeter offre la possibilité d' **enregistrer toutes les requêtes HTTP** transitant entre le navigateur et l’application web à tester. Techniquement, il utilise le mécanisme de **proxy HTTP**. Le navigateur est configuré pour utiliser le Serveur Proxy HTTP créé dans le Plan de Travail JMeter. Couplé à un **Contrôleur Enregistreur**, le proxy enregistre les appels avant de les router vers le serveur d’application cible.

Le tutoriel [Proxy step by step](http://jakarta.apache.org/jmeter/usermanual/jmeter_proxy_step_by_step.pdf) \[3\] proposé sur le site de JMeter fournit toutes les étapes nécessaires pour configuration JMeter.

## Du code source

Le fichier .jmx généré lors de l’enregistrement va devoir être manipulé en Java (bien oui, vous êtes sur le blog d’un développeur java). Premier soulagement : il est au format XML et peut donc être aisément parsé une fois son schéma appréhendé. Mails là où il est intéressant d’avoir opté pour un outil open source, c’est que nous allons pouvoir utiliser son API Java pour manipuler les fichiers .jmx de description de plan de tests. Et pour mieux cerner l’API, l’accès au code source est précieux.

Lors de la mise au point du générateur, les artefacts maven de la version 2.5.1 n’étaient pas disponibles sur le repo central maven, chose révolue depuis la version 2.6.  JMeter est découpé en plusieurs modules. Dans le cadre du générateur, les modules Core, HTTP set Components ont été nécessaires. Sans oublier **jorphan**, dont le package _collections_ offre toutes les API nécessaires pour naviguer dans l’arbre du Plan de Tests.

Par transitivité, il est possible de récupérer tous les artefacts nécessaires en déclarant les dépendances maven suivantes :

```xhtml
<dependency>
	<groupId>org.apache.jmeter</groupId>
	<artifactId>ApacheJMeter_http</artifactId>
	<version>2.6</version>
</dependency>
<dependency>
	<groupId>org.apache.jmeter</groupId>
	<artifactId>jorphan</artifactId>
	<version>2.6</version>
</dependency>
```

# Mise en œuvre

Afin de pouvoir être rejoué, **un scénario de test Selenium enregistré à l’état brut** par le proxy JMeter **doit être épuré**, **retravaillé** et **variabilisé**. C’est d’ailleurs toute la plus-value apportée par le générateur.

## Template de test

Une première étape consiste à insérer le contenu du « fichier brut » (c’est-à-dire tous les éléments de tests enregistrés sous le _Contrôleur Enregistreur_) dans ce que j’appellerai un **template de test**.
Réutilisable, ce template contient toutes les caractéristiques d’un test de stress type.  Voici quelques-unes de ses composantes :

- _Contrôleur de Transaction_ dans lequel insérer par programmation tous les éléments de tests enregistrés
- _Variables pré-définies_ : host et port de l’environnement à tester, délai de réflexion, durée maximum attendue de chargement d’une page
- _Gestionnaire d’entêtes HTTP_, par exemple avec le user-agent d’IE 8 si ce dernier est cible
- _Gestionnaires de Cookies_ http
- _Gestionnaire de_ _Cache HTTP_
- Chargement des comptes utilisateurs (par exemple à partir d’un fichier CSV)
- Logique du test de stress, par exemple à l’aide d’un _Groupes d’Unités_ configuré pour un test aux limites
- _Compteur de temps fixe_ pour simuler le « Think Time » des utilisateurs

## Traitement des données brutes

La seconde étape consiste à implémenter les « **processeurs** » chargés de traiter les éléments de tests enregistrés par le proxy JMeter.
A titre d’exemples, voici les traitements effectués par le générateur mis en œuvre dans le cadre d’une application JSF / RichFaces :

- Variabilise le paramètre javax.faces.ViewState renvoyé dans les pages JSF
- Retire le nom et l'adresse IP du serveur web de chaque requête HTTP
- Supprime toutes les URL contenant des ressources vers selenium-server (ex:
- http://localhost:3333/selenium-server/core/selenium.css)
- Variabilise les paramètres d’authentification SSO
- Supprime tous les gestionnaires d'en-tête HTTP enregistrés par le proxy JMeter afin d’utiliser le gestionnaire global déclaré dans le template de test
- Regroupe tous les appels vers la même page JSF dans même un sous-contrôleur de transaction
- Supprime tous les appels vers des sites externes (ex : Google Analytics)
- Améliore la lisibilité des éléments de tests en les renommant
- Ajoute une assertion sur le temps d'exécution d'une requête
- Ajoute une assertion faisant échouer le test JMeter lorsque l'utilisateur est redirigé sur une page d'erreur technique de l’application

Afin d’illustrer cet article et de le rendre plus concret, voici un exemple de processeur :

Chez mon client, des **tests de stress** sont réalisés sur toute nouvelle version d’une application. Outre le fait de **qualifier techniquement** l’environnement de pré-production, ces tirs permettent de **détecter toute** **dégradation** des performances et de **prévenir toute montée en charge** induite, par exemple, par une nouvelle fonctionnalité. Plus encore, ils permettent de  mesurer les gains apportés par d’éventuelles optimisations.  Ces tests de stress sont réalisés à l’aide de l’outil [Apache JMeter](http://jmeter.apache.org/) \[1\].

Afin de pouvoir **comparer des mesures**, les cas fonctionnels utilisés lors des tests doivent, dans la mesure du possible, être identiques aux précédents tirs, sachant que ces derniers peuvent dater de plusieurs mois. Entre temps, nombre d’évolutions ont été susceptibles de casser vos tests JMeter. A priori, vous avez donc 2 choix : soit vous les réécrivez, soit vous les maintenez à jour. Si vous en avez déjà écrit, vous vous doutez bien que maintenir dans la durée des tests JMeter a un cout non négligeable.  Une 3ième solution présentée ici consiste à la générer !

J’ai la chance de travailler dans une équipe ou l’outil [Selenium](https://selenium.dev/) \[2\] de tests IHM est rentré dans les mœurs. L’automatisation de leur exécution y joue un rôle indéniable. Notre hiérarchie s’est fortement impliquée ; elle a investi de l’énergie et du budget. Un DSL a été mis au point pour faciliter leur écriture et leur maintenance. Alors quand on peut les rentabiliser encore davantage, autant le faire. J’ai donc proposé de ne maintenir que les tests Selenium et de **générer les tests JMeter à partir de tests Selenium**.

Cet article a pour objectif de vous présenter la démarche adoptée. Si vous êtes intéressés, vous pourrez librement l’adapter en fonction de votre contexte projet.<!--more-->

# Les outils à disposition

## Serveur Proxy HTTP de JMeter

Le client lourd JMeter offre la possibilité d' **enregistrer toutes les requêtes HTTP** transitant entre le navigateur et l’application web à tester. Techniquement, il utilise le mécanisme de **proxy HTTP**. Le navigateur est configuré pour utiliser le Serveur Proxy HTTP créé dans le Plan de Travail JMeter. Couplé à un **Contrôleur Enregistreur**, le proxy enregistre les appels avant de les router vers le serveur d’application cible.

Le tutoriel [Proxy step by step](http://jakarta.apache.org/jmeter/usermanual/jmeter_proxy_step_by_step.pdf) \[3\] proposé sur le site de JMeter fournit toutes les étapes nécessaires pour configuration JMeter.

## Du code source

Le fichier .jmx généré lors de l’enregistrement va devoir être manipulé en Java (bien oui, vous êtes sur le blog d’un développeur java). Premier soulagement : il est au format XML et peut donc être aisément parsé une fois son schéma appréhendé. Mails là où il est intéressant d’avoir opté pour un outil open source, c’est que nous allons pouvoir utiliser son API Java pour manipuler les fichiers .jmx de description de plan de tests. Et pour mieux cerner l’API, l’accès au code source est précieux.

Lors de la mise au point du générateur, les artefacts maven de la version 2.5.1 n’étaient pas disponibles sur le repo central maven, chose révolue depuis la version 2.6.  JMeter est découpé en plusieurs modules. Dans le cadre du générateur, les modules Core, HTTP set Components ont été nécessaires. Sans oublier **jorphan**, dont le package _collections_ offre toutes les API nécessaires pour naviguer dans l’arbre du Plan de Tests.

Par transitivité, il est possible de récupérer tous les artefacts nécessaires en déclarant les dépendances maven suivantes :

```xhtml
<dependency>
	<groupId>org.apache.jmeter</groupId>
	<artifactId>ApacheJMeter_http</artifactId>
	<version>2.6</version>
</dependency>
<dependency>
	<groupId>org.apache.jmeter</groupId>
	<artifactId>jorphan</artifactId>
	<version>2.6</version>
</dependency>
```

# Mise en œuvre

Afin de pouvoir être rejoué, **un scénario de test Selenium enregistré à l’état brut** par le proxy JMeter **doit être épuré**, **retravaillé** et **variabilisé**. C’est d’ailleurs toute la plus-value apportée par le générateur.

## Template de test

Une première étape consiste à insérer le contenu du « fichier brut » (c’est-à-dire tous les éléments de tests enregistrés sous le _Contrôleur Enregistreur_) dans ce que j’appellerai un **template de test**.
Réutilisable, ce template contient toutes les caractéristiques d’un test de stress type.  Voici quelques-unes de ses composantes :

- _Contrôleur de Transaction_ dans lequel insérer par programmation tous les éléments de tests enregistrés
- _Variables pré-définies_ : host et port de l’environnement à tester, délai de réflexion, durée maximum attendue de chargement d’une page
- _Gestionnaire d’entêtes HTTP_, par exemple avec le user-agent d’IE 8 si ce dernier est cible
- _Gestionnaires de Cookies_ http
- _Gestionnaire de_ _Cache HTTP_
- Chargement des comptes utilisateurs (par exemple à partir d’un fichier CSV)
- Logique du test de stress, par exemple à l’aide d’un _Groupes d’Unités_ configuré pour un test aux limites
- _Compteur de temps fixe_ pour simuler le « Think Time » des utilisateurs

## Traitement des données brutes

La seconde étape consiste à implémenter les « **processeurs** » chargés de traiter les éléments de tests enregistrés par le proxy JMeter.
A titre d’exemples, voici les traitements effectués par le générateur mis en œuvre dans le cadre d’une application JSF / RichFaces :

- Variabilise le paramètre javax.faces.ViewState renvoyé dans les pages JSF
- Retire le nom et l'adresse IP du serveur web de chaque requête HTTP
- Supprime toutes les URL contenant des ressources vers selenium-server (ex:
- http://localhost:3333/selenium-server/core/selenium.css)
- Variabilise les paramètres d’authentification SSO
- Supprime tous les gestionnaires d'en-tête HTTP enregistrés par le proxy JMeter afin d’utiliser le gestionnaire global déclaré dans le template de test
- Regroupe tous les appels vers la même page JSF dans même un sous-contrôleur de transaction
- Supprime tous les appels vers des sites externes (ex : Google Analytics)
- Améliore la lisibilité des éléments de tests en les renommant
- Ajoute une assertion sur le temps d'exécution d'une requête
- Ajoute une assertion faisant échouer le test JMeter lorsque l'utilisateur est redirigé sur une page d'erreur technique de l’application

Afin d’illustrer cet article et de le rendre plus concret, voici un exemple de processeur :

\[gist id=2783293\]

La classe _ViewStateExtractor_ est chargée d’extraire l'identifiant du view state JSF à l’aide d’une expression régulière. La valeur est stockée dans la variable JMeter _VIEWSTATE_. Cette extraction est effectuée lorsque l'utilisateur arrive la première fois sur une page donnée. La variable _VIEWSTATE_ est ensuite soumise dans la variable _javax.faces.ViewState_. Ce comportement est assuré par un second processeur : le _ViewStateReplacer_.

A noter que dans nos scénarios de tests, l’utilisateur ne revient jamais sur des pages précédemment visitées.
Classe maison, TestElementTree associe un élément de test (classe héritant de _org.apache.jmeter.testelement.TestElement_) à son arbre parent (de type _org.apache.jorphan.collections.HashTree_)

Voici le résultat du générateur vu depuis le client lourd JMeter :

[![Extracteur d'expression régulière JMeter](/wp-content/uploads/2012/05/jmeter-viewstate-extractor.png)](/wp-content/uploads/2012/05/jmeter-viewstate-extractor.png)

## Génération

Enfin, la troisième et dernière étape consiste à orchestrer la lecture du fichier brut, la fusion dans le template de test et l’exécution des différents processeurs. Rien de sorcier. Les méthodes _loadTree_ et _saveTree_ de la _classe org.apache.jmeter.save.SaveService_ sont là pour nous y aider. Parcourir l’arbre d’éléments de test JMeter et appliquer les traitements se code relativement facilement. Point d’attention : l’ordre d’exécution des traitements peut avoir son importance.

# Conclusion

En une petite semaine de développement et de mise au point, vous avez la possibilité de générer des tests JMeter reprenant les scénarios fonctionnels de vos tests Selenium. Vos tests de stress collent ainsi parfaitement aux use cases fonctionnels. En cas d’IHM web riche, les requêtes Ajax (par exemple liées à l’auto-suggestion) sont enregistrées.

Désormais, le client lourd JMeter n’est utilisé que pour créer le template de test et vérifier le résultat de la génération.

Pour aller encore plus loin, les quelques interventions manuelles décrites précédemment pourraient être automatisées :

- La configuration du proxy HTTP du navigateur pourrait par exemple être remplacée par l’utilisation d’un profile Firefox préconfiguré.
- La configuration et le démarrage du Server Proxy HTTP de JMeter pourraient être programmés via l’API JMeter.

Ceci réalisé, la génération des tests pourrait alors se faire en **un clic**. Et comme nos tests Selenium sont exécutés chaque nuit par une plateforme d’intégration continue. En cas de succès, il serait intéressant de déclencher la génération des tests JMeter. Nous disposerions alors de **tests de montée en charge toujours à jour sans plus aucune intervention humaine.** Références :

1. [Site officiel d’Apache JMeter](http://jmeter.apache.org/)
1. [Site official de Selenium](https://selenium.dev/)
1. Tutorial [JMeter Proxy step by step](http://jakarta.apache.org/jmeter/usermanual/jmeter_proxy_step_by_step.pdf)

La classe _ViewStateExtractor_ est chargée d’extraire l'identifiant du view state JSF à l’aide d’une expression régulière. La valeur est stockée dans la variable JMeter _VIEWSTATE_. Cette extraction est effectuée lorsque l'utilisateur arrive la première fois sur une page donnée. La variable _VIEWSTATE_ est ensuite soumise dans la variable _javax.faces.ViewState_. Ce comportement est assuré par un second processeur : le _ViewStateReplacer_.

A noter que dans nos scénarios de tests, l’utilisateur ne revient jamais sur des pages précédemment visitées.
Classe maison, TestElementTree associe un élément de test (classe héritant de _org.apache.jmeter.testelement.TestElement_) à son arbre parent (de type _org.apache.jorphan.collections.HashTree_)

Voici le résultat du générateur vu depuis le client lourd JMeter :

[![Extracteur d'expression régulière JMeter](/wp-content/uploads/2012/05/jmeter-viewstate-extractor.png)](/wp-content/uploads/2012/05/jmeter-viewstate-extractor.png)

## Génération

Enfin, la troisième et dernière étape consiste à orchestrer la lecture du fichier brut, la fusion dans le template de test et l’exécution des différents processeurs. Rien de sorcier. Les méthodes _loadTree_ et _saveTree_ de la _classe org.apache.jmeter.save.SaveService_ sont là pour nous y aider. Parcourir l’arbre d’éléments de test JMeter et appliquer les traitements se code relativement facilement. Point d’attention : l’ordre d’exécution des traitements peut avoir son importance.

# Conclusion

En une petite semaine de développement et de mise au point, vous avez la possibilité de générer des tests JMeter reprenant les scénarios fonctionnels de vos tests Selenium. Vos tests de stress collent ainsi parfaitement aux use cases fonctionnels. En cas d’IHM web riche, les requêtes Ajax (par exemple liées à l’auto-suggestion) sont enregistrées.

Désormais, le client lourd JMeter n’est utilisé que pour créer le template de test et vérifier le résultat de la génération.

Pour aller encore plus loin, les quelques interventions manuelles décrites précédemment pourraient être automatisées :

- La configuration du proxy HTTP du navigateur pourrait par exemple être remplacée par l’utilisation d’un profile Firefox préconfiguré.
- La configuration et le démarrage du Server Proxy HTTP de JMeter pourraient être programmés via l’API JMeter.

Ceci réalisé, la génération des tests pourrait alors se faire en **un clic**. Et comme nos tests Selenium sont exécutés chaque nuit par une plateforme d’intégration continue. En cas de succès, il serait intéressant de déclencher la génération des tests JMeter. Nous disposerions alors de **tests de montée en charge toujours à jour sans plus aucune intervention humaine.** Références :

1. [Site officiel d’Apache JMeter](http://jmeter.apache.org/)
1. [Site official de Selenium](https://selenium.dev/)
1. Tutorial [JMeter Proxy step by step](http://jakarta.apache.org/jmeter/usermanual/jmeter_proxy_step_by_step.pdf)
