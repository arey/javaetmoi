---
_edit_last: "1"
_thumbnail_id: "2336"
_xmlsf_image_featured:
  caption: ""
  loc: https://javaetmoi.com/wp-content/uploads/2024/04/word-image-2335-1.jpeg
  title: word-image-2335-1
author: admin
categories:
  - conférence
featureImage: /wp-content/uploads/2024/04/word-image-2335-1.jpeg
featureImageAlt: word-image-2335-1
date: "2024-04-26T17:55:09+00:00"
thumbnail: /wp-content/uploads/2024/04/word-image-2335-1.jpeg
guid: https://javaetmoi.com/?p=2335
parent_post_id: null
post_id: "2335"
post_views_count: "13436"
summary: |-
  Conférence : [Devoxx France 2024](https://www.devoxx.fr/)<br>Date : 17 avril 2024<br>Speakers : [Damien Lucas](https://www.linkedin.com/in/damien-lucas/) (OnePoint)<br>Format : Conférence (45 mn)<br>Slides : [https://dlucasd.github.io/la-doc-va-bien-ne-t-en-fais-pas/devoxx/#/](https://dlucasd.github.io/la-doc-va-bien-ne-t-en-fais-pas/devoxx/#/)<br>Vidéo Youtube : [https://www.youtube.com/watch?v=zQ0A75HqFuA](https://www.youtube.com/watch?v=zQ0A75HqFuA)<br>Repo GitHub : [https://github.com/dlucasd/la-doc-va-bien-ne-t-en-fais-pas](https://github.com/dlucasd/la-doc-va-bien-ne-t-en-fais-pas)

  La **documentation**, sujet atemporel. Travaillant sur des projets en TMA, Damien faisait le constat suivant : d’un projet à l’autre, la structure, l’organisation et le niveau d’informations de la documentation diffèrent. De temps à autres, Damien assistait à des réunions visant à restructurer la documentation. Chaque participant a sa vision. Trouver un consensus n’est pas facile. <br>Damien s’est ainsi demandé s’il n’existait pas clé en main un **template de rédaction de la documentation**, si possible **Open Source** et **reconnu** par la communauté des dévs et architectes.

  Au cours de ses recherches, il est tombé sur le framework [**arc42**](https://arc42.org/) créé en 2005 par 2 allemands : Gernot Starke et Peter Hruschka. Ce template se focalise sur l’ **architecture des logiciels et des systèmes**. Plusieurs formats sources sont possibles en téléchargement depuis la page [https://arc42.org/download](https://arc42.org/download) : **asciidoc**, **markdown**, latex, Word, Confluence, html, Doxygen, IBM Rhapsody … Voici par exemple le template arc42 pour Word : [arc42-template-FR-withhelp-docx.zip](https://github.com/arc42/arc42-template/raw/master/dist/arc42-template-FR-withhelp-docx.zip)

  Damien a une **préférence pour l’asciidoc** qui permet d’avoir une **approche docs-as-code** : on peut le commiter dans un repository **git** puis générer un document au format souhaité (ex : PDF)

  Les templates arc42 au format asciidoc (extension .adoc) sont disponibles sur le repo GitHub [arc42-template](https://github.com/arc42/arc42-template/tree/master/FR/asciidoc): une **dizaine de langues** est supportée dont le **français**.

  Ce template nous guide et nous pose les bonnes questions :

  1. **Contenu** : que faut-il documenter ?
  2. **Motivation** : pourquoi documenter et pour qui ?
  3. **Représentation** : comment documenter ? Faut-il préférer un diagramme ou une liste à puce ?

  Arc42 propose de documenter une application en **12 chapitres**. Chaque chapitre est lui-même généralement composé de 3 sous-parties. <br>Dans de ce talk, Damien s’appuie sur un projet fictif pour illustrer chacun des 12 chapitres. Ce projet consiste à développer une application de billetterie pour les JO. Il en profitera pour nous présenter des **outils de génération de diagrammes** (PlantUML et Mermaid), des **outils de modélisation** (C4 et Structurizr) et des **outils de génération de documentation** (avec CLI et donc intégrable à la CI).
tags:
  - arc42
  - asciidoc
  - c4
  - compodoc
  - devoxx
  - diataxis
  - k8sviz
  - mermaid
  - openapi
  - plantuml
  - redoc
  - spingdoc
  - structurizr
title: La doc va bien, ne t’en fais pas
url: /2024/04/la-doc-va-bien-ne-ten-fais-pas/

---
Conférence : [Devoxx France 2024](https://www.devoxx.fr/)  
Date : 17 avril 2024  
Speakers : [Damien Lucas](https://www.linkedin.com/in/damien-lucas/) (OnePoint)  
Format : Conférence (45 mn)  
Slides : [https://dlucasd.github.io/la-doc-va-bien-ne-t-en-fais-pas/devoxx/#/](https://dlucasd.github.io/la-doc-va-bien-ne-t-en-fais-pas/devoxx/#/)  
Vidéo Youtube : [https://www.youtube.com/watch?v=zQ0A75HqFuA](https://www.youtube.com/watch?v=zQ0A75HqFuA)  
Repo GitHub : [https://github.com/dlucasd/la-doc-va-bien-ne-t-en-fais-pas](https://github.com/dlucasd/la-doc-va-bien-ne-t-en-fais-pas)

La **documentation**, sujet atemporel. Travaillant sur des projets en TMA, Damien faisait le constat suivant : d’un projet à l’autre, la structure, l’organisation et le niveau d’informations de la documentation diffèrent. De temps à autres, Damien assistait à des réunions visant à restructurer la documentation. Chaque participant a sa vision. Trouver un consensus n’est pas facile.   
Damien s’est ainsi demandé s’il n’existait pas clé en main un **template de rédaction de la documentation**, si possible **Open Source** et **reconnu** par la communauté des dévs et architectes.

Au cours de ses recherches, il est tombé sur le framework [**arc42**](https://arc42.org/) créé en 2005 par 2 allemands : Gernot Starke et Peter Hruschka. Ce template se focalise sur l’ **architecture des logiciels et des systèmes**. Plusieurs formats sources sont possibles en téléchargement depuis la page [https://arc42.org/download](https://arc42.org/download) : **asciidoc**, **markdown**, latex, Word, Confluence, html, Doxygen, IBM Rhapsody … Voici par exemple le template arc42 pour Word : [arc42-template-FR-withhelp-docx.zip](https://github.com/arc42/arc42-template/raw/master/dist/arc42-template-FR-withhelp-docx.zip)

Damien a une **préférence pour l’asciidoc** qui permet d’avoir une **approche docs-as-code** : on peut le commiter dans un repository **git** puis générer un document au format souhaité (ex : PDF)

Les templates arc42 au format asciidoc (extension .adoc) sont disponibles sur le repo GitHub [arc42-template](https://github.com/arc42/arc42-template/tree/master/FR/asciidoc): une **dizaine de langues** est supportée dont le **français**.

Ce template nous guide et nous pose les bonnes questions :

1. **Contenu** : que faut-il documenter ?
1. **Motivation** : pourquoi documenter et pour qui ?
1. **Représentation** : comment documenter ? Faut-il préférer un diagramme ou une liste à puce ?

Arc42 propose de documenter une application en **12 chapitres**. Chaque chapitre est lui-même généralement composé de 3 sous-parties.   
Dans de ce talk, Damien s’appuie sur un projet fictif pour illustrer chacun des 12 chapitres. Ce projet consiste à développer une application de billetterie pour les JO. Il en profitera pour nous présenter des **outils de génération de diagrammes** (PlantUML et Mermaid), des **outils de modélisation** (C4 et Structurizr) et des **outils de génération de documentation** (avec CLI et donc intégrable à la CI).

{{< figure src="/wp-content/uploads/2024/04/word-image-2335-1.jpeg" alt="" caption="" >}}

## 1\. Introduction et objectifs

Vue haut niveau du projet décrivant les grandes fonctionnalités.   
Exemple : permet acheter place + télécharger billet   
Il est recommandé d’ajouter des liens vers la documentation existante.   
Exemple : vers les maquettes, les spécifications fonctionnelles

Dans le projet fictif, OpenAPI est utilisé pour documenter les API REST.   
L’outil [**OpenAPI Generator**](https://openapi-generator.tech/) permet de générer la documentation AsciiDoc. L’équipe aurait pu également faire le choix de générer un site statique.   
Pour documenter une API, Julien préfère l’outil [**ReDoc**](https://github.com/Redocly/redoc): plus moderne, l’interface est plus pratique. Preuve en est, elle est utilisée nativement dans IntelliJ lors de l’édition d’une spécification OpenAPI.

{{< figure src="/wp-content/uploads/2024/04/word-image-2335-2.png" alt="" caption="" >}}


Ces 2 outils exploitent les informations du contrat d’interface. Julien rappelle la nécessité de documenter au maximum le contrat d’interface.   
Lorsque l’approche API First n’est pas utilisée sur un projet, il reste possible de générer le contrat à partir du code avec des outils comme [**Springdoc**](http://springdoc.org/).

## 2\. Contraintes d’architecture

Lors de la création d’un système, les décisions et la liberté des architectes sont guidées par les contraintes qu’ils doivent respecter : **contraintes techniques**, contraintes **organisationnelles**, contraintes **politiques** et **conventions** (de code, de nommage, de comit).

Exemples : la webapp doit être compatible Firefox, Edge et Chrome   
L’application doit être déployée sur un serveur Tomcat OnPremise   

## 3\. Contexte et périmètre

Le contexte et le périmètre délimitent le système de tous les systèmes connexes voisins. Les interfaces fonctionnelles et techniques avec les partenaires sont décrites dans ce paragraphe. Un **diagramme de contexte** a toute sa place.   
Traditionnellement, les outils **Visio** ou **draw.io** peuvent être utilisés pour réaliser de tels diagrammes. Vous vous en doutez, Damien recommande de privilégier les diagrammes as code afin de faciliter les revues et préconise [**C4 model**](https://c4model.com/), créé par Simon Brown entre 2006 et 2011 et inspiré de UML.   
La modélisation C4 documente l'architecture d'un système logiciel en utilisant plusieurs points de vue et avec 4 niveaux d’abstraction. Nous y reviendrons.

Exemple de diagramme de contexte conçu à l’aide de [C4-PlantUML](https://github.com/plantuml-stdlib/C4-PlantUML) :

![](/wp-content/uploads/2024/04/word-image-2335-3.png)

## 4\. Stratégie de solution

Résumé et explication des décisions fondamentales et des stratégies de solution qui régissent l’architecture du système.   
Exemple : un fort trafic sur le site lors de l’ouverture de la billetterie a suscité la mise en œuvre d’une solution de file d’attente à l’achat. On ajoute dans la documentation d’un lien vers l’étude menée.   
On peut utiliser ici un simple tableau :

{{< figure src="/wp-content/uploads/2024/04/word-image-2335-4.png" alt="" caption="" >}}

## 5\. Vue en boites

Décomposition du système en boîte avec différents niveaux d’abstraction. On retrouve ici les 4 niveaux du modèle C4 :

1. Level 1 : Context
1. Level 2 : Containers
1. Level 3 : Components
1. Level 4 : Code (diagramme de classes)

{{< figure src="/wp-content/uploads/2024/04/word-image-2335-5.png" alt="" caption="" >}}

Depuis la vue Context, on peut zoomer dans l’une des vues Container, et ainsi de suite.   
Par expérience, Damien nous explique que le niveau 4 est peu utilisé.

La problématique n°1 de C4 est la redondance d’informations. On peut retrouver le même système externe dans chacun des fichiers représentants les 4 niveaux.   
La problématique n°2 de C4 est provoquée par l’auto-layout des outils lorsque le nombre de boites devient conséquent.

Créé par Simon Brown comme C4, l’outil [**Structurizr**](https://structurizr.com/) permet de créer des diagrammes clairs et informatifs qui illustrent la structure d'un système logiciel. Il s’appuie sur le domain specific language [Structurizr DSL](https://docs.structurizr.com/dsl) supporté dans VS Code et IntelliJ :

{{< figure src="/wp-content/uploads/2024/04/word-image-2335-6.png" alt="" caption="" >}}

Les diagrammes Structurizr sont dynamiques et permettent de zoomer.   
Les avantages :

- plus de redondance d’information car, dans l’exemple ci-dessus extrait su site officiel, le _softwareSystem_ est réutilisée
- permet de générer tous les flux entrants sur la base de données
- export vers de nombres formats comme plantuml, marmaid et c4

Pour documenter les applications **Angular**, l’outil [**Compodoc**](https://compodoc.app/) créé par Vincent Ogloblinsky nous est conseillé. Compodoc permet de zoomer sur des modules Angular, de représenter les routes et s’appuie sur la JSDoc.

{{< figure src="/wp-content/uploads/2024/04/word-image-2335-7.png" alt="" caption="" >}}

Pour **React** et **Vue.js**, Damien n’a pas trouvé d’autres outils que **Storybook**.

## 6\. Vue exécution

La vue exécution décrit le comportement concret des briques du système à travers des scénarios.   
On y retrouve différents types de diagrammes UML : activités, flux, séquences …   
Exemple d’un diagramme de séquence généré avec **[Mermaid](https://mermaid.js.org/)**:

{{< figure src="/wp-content/uploads/2024/04/sequence-achat-billet.png" alt="sequence achat billet" caption="sequence achat billet" >}}

Mairmaid est très bien intégré dans GitLab et GitHub qui savent nativement afficher le rendu graphique des diagrammes, contrairement à **[PlantUML](https://plantuml.com/fr/)** qui nécessite l’installation de [GraphViz](https://plantuml.com/fr/graphviz-dot).

## 7\. Vue déploiement

La vue déploiement décrit l’infrastructure technique utilisée pour exécuter le système ainsi que la correspondance entre les briques logicielles et les éléments d’infrastructure.

On y retrouve bien évidemment des diagrammes de déploiement sur les environnements avec des informations de type infrastructure : VM, type de base de données, version de RHEL …   
Lorsque l’application est déployée dans **Kubernetes**, il est possible d’utiliser [k8sviz](https://github.com/mkimuram/k8sviz) et [KubeView](https://github.com/benc-uk/kubeview).   
Pour **Docker Compose**, il existe des outils comme [docker-compose-diagram](https://skonik.github.io/docker-compose-diagram/#/).

## 8\. Concepts transversaux

Ce chapitre est généralement le plus conséquent. Il décrit les règles principales et les idées de solutions pertinentes du système. On y retrouve des informations sur le packaging, le mécanisme de déploiement, le pattern d’architecture employé (ex : n-tiers vs hexagonale), observabilité, le modèl de données …

L’outil [**SchemaSpy**](https://schemaspy.org/) permet de générer un MPD à partir d’une URL de connexion. Il s’appuie notamment sur les commentaires SQL ajoutées sur les tables, les colonnes et les contraintes.   
Une de ses fonctionnalités pratiques est de pouvoir zoomer sur une table en affichant ses relations de niveau 1 ou 2 puis d’en fait un export en images.

Exemple : zoom sur la table Track et ses relations au 2ième degré

![](/wp-content/uploads/2024/04/word-image-2335-9.png)

## 9\. Décisions d’architecture

Ce chapitre consigne les décisions d’architectures significatives. On retrouve une certaine similarité avec les [**Architecture Decision Records**](https://github.com/joelparkerhenderson/architecture-decision-record) (ADR).   
Cela permet de retracer les décisions prises au cours du temps.   
Exemple : pourquoi avoir utilisé telle base de données NoSQL ?   
Y sont décrits le contexte et le problème constatés, la décision et le statut (proposé, accepté, rejeté, obsolète …).

## 10\. Critères de qualité

Ce paragraphe contient toutes les exigences de qualité sous la forme d’un arbre de qualité avec des scénarios et des cas d’utilisation concret.

Exemple sur l’exigence de performance : gestion d’au moins 10 000 transactions simultanées lors de la vente de billets tout en répondant aux utilisateurs en moins d’une seconde.

D'expérience, travaillant sur des projets en TMA, Damien utilise peu cette partie.

## 11\. Risques et dettes techniques

Cette section liste les risques et les dettes techniques identifiés, classés par ordre de priorité.

Exemple de risque : mise à l’échelle insuffisante pour gérer le trafic.   
Exemple de dette technique : absence de tests automatisés pour le processus d’achat.

## 12\. Glossaire

Tableau listant les **termes techniques et métier** les plus importants.

Dans le cadre du **Domain-Driven Design** (DDD) et de l' **Ubiquitous Language**, un glossaire joue un rôle crucial en centralisant et en formalisant la terminologie propre au domaine métier.   
Un glossaire permet également de maintenir une **traduction de référence** (ex : anglais <-> français).

Damien cite les **annotations Java** de Cyrille Martraire permettant d’extraire le glossaire et dont je vous avais [déjà parlé en 2016](/wp-content/uploads/2016/05/Devoxx_France-2016-Live_documentation.pdf).

## Bilan de arc42

Sur les 12 chapitres, **le contenu de la moitié peut été généré**.   
Cette documentation permet de comprendre l’application sans lire la moindre ligne de code.   
A priori, se lancer dans la documentation peut faire peur, mais Damien insiste qu’en une semaine on peut avoir un squelette de documentation tout à fait satisfait et qu’il sera possible de l’enrichir par incrément.   
Le format asciidoc est très flexible puisqu’il permet de générer un site statique, un PDF et/ou une publication dans Confluence.

## Documentation utilisateur

La documentation utilisateur n’est pas abordé dans arc42.

Damien nous recommande le framework **[Diataxis](https://diataxis.fr/)** qui encourage à découper la documentation en 4 parties :

1. **Tutoriel** avec le Hello World
1. **How to**: listes d’étapes avec but bien précis
1. **Concepts** : comment fonctionne l’outil
1. **Documentation de référence**

![](/wp-content/uploads/2024/04/word-image-2335-10.png)  
La [documentation de Quarkus](https://quarkus.io/guides/doc-concept) s’appuie désormais sur le concept Diataxis.

## Conclusion

Pour conclure, voici les bénénéfices d’utilisation du template :

1. **Homogénéité** d’un projet à l’autre, ce qui permet de s’y retrouver
1. Le template sert de **guide**. Il est très riche
1. **Moins de charge mentale** lors de la rédaction de la documentation : on se laisse guider
