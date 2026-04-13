---
_edit_last: "1"
_thumbnail_id: "1821"
_xmlsf_image_featured:
  caption: cof
  loc: https://javaetmoi.com/wp-content/uploads/2018/04/IMG_20180418_132919.jpg
  title: cof
author: admin
categories:
  - conférence
featureImage: wp-content/uploads/2018/04/IMG_20180418_132919.jpg
featureImageAlt: cof
date: "2018-04-22T15:08:55+00:00"
toc: true
thumbnail: wp-content/uploads/2018/04/IMG_20180418_132919.jpg
guid: http://javaetmoi.com/?p=1820
parent_post_id: null
post_id: "1820"
post_views_count: "18759"
summary: |-
  Lors de **Devoxx France 2018**, j’ai participé au **[Hands-on Lab d’initiation à Apache Cassandra](https://cfp.devoxx.fr/2018/talk/GVY-2134/Initiation_a_Apache_Cassandra)**. Animé par Alexander Dejanovski (The LastPickle) et Maxence Lecointe (Ippon), ce Lab m’aura enfin permis de découvrir cette **base de donnée NoSQL**, d’appréhender ses concepts fondamentaux, de jouer avec un cluster en local et d’écrire quelques requêtes CQL par le biais de son client Java.

  Le Lab était construit autour d’un support de présentation et de 5 exercices pratiques. Les **slides** [Devoxx France – Initiation àApache Cassandra - Avril 2018.pdf](https://github.com/thelastpickle/devoxxfr2018/raw/master/Devoxx%20France-%20Initiation%20%C3%A0%20Apache%20Cassandra%20-%20Avril%202018.pdf) et les **exercices** sont disponibles sur le dépôt GitHub [thelastpickle/devoxxfr2018](https://github.com/thelastpickle/devoxxfr2018/).

  Ce billet a pour objectif de permettre aux développeurs n’ayant pas eu la chance de suivre ce Lab de profiter du travail préparatif des 2 speakers (un grand merci à eux) en lui donnant de la visibilité. Vous pourrez ainsi vous former par vous-même à Cassandra. Les explications données dans ce billet complètent les slides mais ne remplacent pas leur lecture.

  [![](wp-content/uploads/2018/04/IMG_20180418_132919.jpg)](wp-content/uploads/2018/04/IMG_20180418_132919.jpg)

  ![cof](wp-content/uploads/2018/04/IMG_20180418_132919.jpg)
tags:
  - cassandra
  - devoxx
  - nosql
title: Initiation à Apache Cassandra
url: /2018/04/lab-initiation-apache-cassandra/

---
Lors de **Devoxx France 2018**, j’ai participé au **[Hands-on Lab d’initiation à Apache Cassandra](https://cfp.devoxx.fr/2018/talk/GVY-2134/Initiation_a_Apache_Cassandra)**. Animé par Alexander Dejanovski (The LastPickle) et Maxence Lecointe (Ippon), ce Lab m’aura enfin permis de découvrir cette **base de donnée NoSQL**, d’appréhender ses concepts fondamentaux, de jouer avec un cluster en local et d’écrire quelques requêtes CQL par le biais de son client Java.

Le Lab était construit autour d’un support de présentation et de 5 exercices pratiques. Les **slides** [Devoxx France – Initiation àApache Cassandra - Avril 2018.pdf](https://github.com/thelastpickle/devoxxfr2018/raw/master/Devoxx%20France-%20Initiation%20%C3%A0%20Apache%20Cassandra%20-%20Avril%202018.pdf) et les **exercices** sont disponibles sur le dépôt GitHub [thelastpickle/devoxxfr2018](https://github.com/thelastpickle/devoxxfr2018/).

Ce billet a pour objectif de permettre aux développeurs n’ayant pas eu la chance de suivre ce Lab de profiter du travail préparatif des 2 speakers (un grand merci à eux) en lui donnant de la visibilité. Vous pourrez ainsi vous former par vous-même à Cassandra. Les explications données dans ce billet complètent les slides mais ne remplacent pas leur lecture.

[![](wp-content/uploads/2018/04/IMG_20180418_132919.jpg)](wp-content/uploads/2018/04/IMG_20180418_132919.jpg)

## Installation de CCM

Slides : 4 à 5

Une partie du Lab repose sur l’utilisation du Cassandra Cluster Manager (CCM). Cet outil est particulièrement pratique pour développer en local avec Cassandra. En effet, il permet de créer des clusters multi-nœuds et multi Data Centers (DC). Un pré-requis de ce Lab consiste donc à installer CCM en suivant son [guide d’installation](https://pypi.org/project/ccm/).

Cassandra n’est pas encore compatible avec Java 9 (cf. [CASSANDRA-9608](https://issues.apache.org/jira/browse/CASSANDRA-9608)). Il est donc nécessaire d’utiliser un JDK 8 pour le démarrer.

Pour tester son installation, vous pouvez simuler la création d’un cluster de 3 nœuds sur 3 DC via la commande suivante :

```sh
ccm create my_cluster_3016 -v binary:3.0.16 -n 3:3
```

D’autres cas d’usage de CCM sont :

- le teste d’un programme sur différentes versions de Cassandra, et réaliser ainsi des tests d’upgrade / downgrade,
- l’exécution des tests d’intégration sur un cluster éphémère.

## Concepts fondamentaux

Slides : 6 à 48

Avant de pouvoir commencer le Lab, il est nécessaire d’acquérir quelques connaissances sur Cassandra et le Cassandra Query Language ( **CQL**). Ce dernier ressemble à du SQL.

Dans Cassandra, l’unité de stockage et de réplication est le **Keyspace**. Il s’apparente au schéma du monde des bases de données relationnelles.
Lors de la création du Keyspace, on spécifie le **facteur de réplication** sur les nœuds du cluster. De ce paramétrage, va dépendre la montée en charge et la tolérance aux pannes de l’application.
A noter que la réplication multi-datacenter est native dans Cassandra.

La création d’une **Table** requière la déclaration d’une **clé primaire** composée d’une **partition key**(id\_flux dans la suite de l’article) et d’un **clustering key**. Comme en SQL, la clé primaire est unique.
Le système de partition est basé sur des hashs. Chaque clé de partition est hachée.
L’algorithme de hashing Murmur3 permet d’utiliser toute la plage des Long en Java.
Avant Cassandra 1.2 et l’apparition des VNodes, un cluster de 4 nœuds se répartissait les tokens (hash) par plage (range). Le nœud A était responsable d’une des 4 plages. Lorsqu’on ajoutait des nœuds, le nœud A devenait responsable d’une plus petite plage.
Problématique : on devait doubler le nombre de nœuds du cluster pour scaler proprement le cluster (chaque plage est alors de même taille).
Avec les **VNodes**, chaque nœud s’attribue un range de tokens de manière aléatoire.

Comment déterminer la partition auquel appartient un enregistrement ?
En appliquant la formule : Hash(id\_flux) = token
Chaque nœud dispose d’un répertoire interne contenant la répartition des tokens.

La réplication des données est gérée lors de leur enregistrement. L’id\_flux est à la main du développeur.

Le Storage Engine est inspiré de celui d’InnoDB. Il n’est pas maitre/esclave. Il existe une notion de range primaire, mais elle est purement logique.

Chose très importante : **Cassandra est optimisée pour récupérer des données d’une seule partition**. **Pour être performante, les requêtes doivent donc requêter une seule partition**.

La **clé de clustering** sert à **ordonner les données**.
Clé de partition et clé de clustering peuvent être composites.

Les **types CQL** sont nombreux : counter, inet, les collections (pour dénormaliser car pas de jointure), les tuples, uuid … (se référer au slide 17 pour une liste plus exhaustive)

Limites du CQL par rapport au SQL (slide 18) :

- Pas de jointures entre tables
- Pas de OR dans les clauses WHERE (que des AND)
- Limitations sur les champs du WHERE
- Pas d’INSERT/SELECT. Cette limitation implique l’utilisation d’un programme pour transvaser les données d’une table à une autre. Il est nécessaire de bien prévoir le modèle de données.
- Pas de vues. L’utilisation de Vues Dématérialisées est fortement déconseillée par Alexander
- Index peu performants
- Le GROUP BY introduit en 3.10 ne fonctionne que sur une partition.

Comment requêter une table ?

Les requêtes sont conditionnées par les colonnes définissant la clé primaire.
Par exemple, avec la PRIMARY KEY (id\_flux, id\_etape, start\_time), il est possible de réaliser une requête dont la clause WHERE porte sur

- _id\_flux_
- _id\_flux_ et _id\_etape_
- _id\_flux_, _id\_etape_ et _start\_time_

L’ordre des colonnes est très important.
Il est en effet interdit de requêter Cassandra sur :

- id\_etape
- id\_flux et start\_time, car il manquerait la clause sur _id\_etape_ qui est avant _start\_time_ dans la clé primaire

Cette limitation est très restrictive. Il est en effet nécessaire de maintenir autant de tables qu’il y’aura de requêtes. La modélisation des tables dépend donc directement de leur usage en lecture.

En résumé, **l’usage dans Cassandra est** **1 table par requête**. Cela augmente le volume de données. Mais les écritures dans Cassandra sont peu chères (écriture en mémoire puis écriture séquentielle sur disque).
Les données sont compressées dans Cassandra. La version 3.0 a grandement amélioré l’occupation de l’espace disque.
Cassandra assure-t-elle la cohérence entre les 2 tables ? Oui, si tout se passe bien.

Les slides 25 et 26 abordent le caractère d’ **idempotence** de Cassandra.
Deux même INSERT (avec la même clé primaire) vont s’exécuter sans erreur. La dernière écriture prévaut sur la 1ière. La 1ière ligne est donc écrasée. Il n’existe pas de contraintes d’intégrité comme en SQL.
Un INSERT et équivalent à un UPDATE. Avant d’insérer une ligne, il n’est plus besoin de savoir si l’enregistrement existe ou non.
A noter qu’on travaille plus souvent avec des Sets que des Lists car les Sets garantissent l’idempotence. Différenciation syntaxique : utilisation des {} au lieu des \[\]

La notion de **Tombstone** est très importante, car à l’origine de nombreux problèmes de performance.
Un DELETE place une donnée spéciale appelée TOMBSTONE. Il s’agit d’un **marqueur logique de suppression**.
Cassandra est codée en Java. Lire en mémoire des TOMBSTONE génère non seulement beaucoup d’I/O pour rien, mais exerce également beaucoup de pression sur le GC.
Les enregistrements peuvent avoir une durée de vie (un TTL). Une fois la durée de vie passée, ils passent en TOMBSTONE. Pour garder un historique de 3 mois, fixer le TTL à ~7776000.
Les conditions de purge des Tombstones sont complexes. La durée de vie minimale d’un Tombstone est de 10 jours. A partir de 100 000 Tombstones, Cassandra va killer la requête, se protégeant ainsi envers le GC.

Une colonne de type **Counter** est mise à jour par incréments. Elle n’est pas idempotente. C’est parfait pour créer des statistiques approximatives en temps réels (ex : un compteur par heure, jour et mois).
Spotify utilise les counters pour calculer en journée le nombre approximatif d’écoute. La nuit, ils utilisent un batch pour calculer le nombre exact.

Pour garantir des performances optimales, une règle de base est d’essayer d’avoir des **partitions de moins de 100 Mo** à cause du Heap. Pour s’en prémunir, on peut ajouter le jour dans la clé de partition.
Exemple : PRIMARY KEY ((id\_flux, jour), id\_etape, start\_time).
Il devient alors nécessaire de lancer plusieurs requêtes en // pour requêter sur plusieurs jours.
Bien que Cassandra offre la possibilité de créer des **Index Secondaires**, il est recommandé de les éviter. Les temps de réponse peuvent être considérablement dégradés. A noter que le timeout par défaut d’une requête est de 10 secondes.

A présent que les présentations sont faites, le Lab va se dérouler en 2 parties :

1. Une 1ière partie dédiée à l’administration d’un cluster et à son requêtage
1. Une 2nde partie où vous allez écrire un programme Java chargée de lire et d’écrire dans une base Cassandra

## Lab – Part 1

Slides : 49 à 99

Vous allez commencer par créer un cluster Cassandra 3.0.16, puis apprendre à le démarrer, à consulter son statut et à savoir comment accéder à la configuration de chaque nœud.

La connexion à un cluster Cassandra repose sur le principe des **Seed** **Nodes**. C’est le même principe que sur les réseaux Peer-to-Peer type eMule. Pour accéder au cluster, il est nécessaire de connaître au moins un Seed Node. En règle général, on configure 3 Seeds nodes par Data Center. Les Seeds Nodes sont uniquement **utilisés au démarrage d’un client pour prendre connaissance de la typologie du cluster**.
Un nœud est identifié par son **Host ID** (et non son IP). On peut donc changer l’IP d’un nœud.
Un Rack peut être assimilé à une zone de disponibilité AWS ou bien encore à un rack électrique. Cassandra place une réplique par rack. Il est recommandé d’avoir 3 racks au minimum.

La suite du Lab requière l’utilisation d’un [Cassandra Dataset Manager](https://github.com/rustyrazorblade/cdm/) (CDM). Cet outil va être utilisé pour importer des données de films dans votre cluster Cassandra.
Le Keyspace _movielens_ est composé de 5 tables.
La table principale _movies_ utilise la colonne ID de type UUID comme clé primaire et donc clé de répartition. Il y’a donc un 1 enregistrement (1 film) par partition.
Les 2 tables _ratings\_by\_user_ et _ratings\_by\_movie_ permettent de répondre à des requêtes différentes : par utilisateur ou par film.
A noter qu’une base Cassandra n’est pas sécurisée de base. Il sera nécessaire d’activer l’authentification.
Le Lab met en exergue qu’il est impossible de rechercher en l’état un film par titre partiel ou par sa première lettre. Vous allez être amenés à créer la table movies\_by\_first\_letter qui permet une recherche par 1ière lettre ou 1er mot. Pour se faire, la 1ière lettre et le 1er mot du titre d’un film doivent avoir leur propre colonne.
Cette table ne permet pas de faire une recherche de type like et encore moins une recherche approximative.
**Cassandra n’est pas fait pour de la recherche**. Il est préférable de privilégier un moteur de recherche type Elasticsearch.
Alexander précise qu’il existe une distribution commerciale alignant le sharding d’Elasticsearch avec celui de Cassandra.
Pour combler ce vide en termes de recherche, Apple a contribué à l’amélioration de l’Index Secondaire avec [SASSI](https://docs.datastax.com/en/dse/5.1/cql/cql/cql_using/useSASIIndex.html). Cette fonctionnalité est à utiliser avec précaution.

Lors du Lab, la commande _ccm node2 nodetool decommission_ permet de streamer les données sur les autres nœuds avant la décommision du nœud 2.

Cassandra tolère la perte de données en fonction du **niveau de cohérence**(Consistency Level) configuré :

- Cohérence in fine : niveau ONE / LOCAL\_ONE : lecture pas forcément à jour si mise à jour non terminée (1 seule réplique)
- Cohérence forte : Cassandra utilise le timestamp pour renvoyer la donnée à jour en fonction du quorum

Lorsqu’une opération d’écriture nécessite d’avoir le **Quorum**, Cassandra attend d’avoir une majorité de répliques avant de valider l’écriture. Le nombre de réplique impacte le quorum, pas le nombre de nœuds.
Lorsqu’on n’a que 2 Data Centers, on est obligé de faire du Local Quorum à cause du problème du split-brain. Lors de la resynchro des 2 DS, c’est la dernière écriture qui gagne.
La lecture en Quorum ne requête pas toutes les répliques. Elle interroge un nombre suffisant de répliques (quel que soit le Data Center)
Conseil d’Alexander : **partez du principe que les applications ont besoin de cohérence et faites du Quorum.** Lorsqu’on vient du Relationnel, on est habitué à voir de la cohérence. Démarrez avec du Local Quorum qui est plus simple que le Quorum.

Intéressons-nous à présent au **Client** d’une base Cassandra. Une seule connexion est nécessaire pour l’ensemble des requêtes CQL. Il est toutefois possible de créer une connexion par cœur d’un CPU.
Créer une connexion coute cher car elle se connecte à tous les nœuds du cluster. La connexion connaît le schéma et la typologie des nœuds (distribution des tokens). Cela permet au drivers de savoir si des nœuds tombent ou sont ajoutés.
Une grande partie de l’intelligence se trouve dans le cluster.

Lors de la création d’une connexion, peuvent être spécifiées plusieurs stratégies  :

1. **Load Balancing** policies: permet de choisir le nœud qui va traiter la requête CQL. Cassandra permet de créer sa propre policy.
1. **Retry** policies : dans un système distribué, il peut y avoir des problèmes passager de réseau. Attention à bien positionner un setIdempotent(true) sur la requête lors d’un Retry. Certains drivers sont un peu plus complet que d’autres : le SpeculativeRetry n’est disponible que sur le driver Java.

Les slides 84 à 99 expliquent comment coder un client Cassandra en Java :

1. Ajout de la dépendance Maven **cassandra-driver-core**
1. Création et configuration de l’objet **Cluster**
1. Création de l’objet **Session**: une fois l’objet Cluster créé, il faut créer un objet Session qui va permettre d’exécuter des requêtes CQL.
1. Exécution d’une requête CQL puis récupération des données renvoyées
1. Utilisation d’un **PreparedStatement**(recommandée)
1. Exécution de requêtes **asynchrones**: le `executeAsync()` renvoie la main après avoir d’envoyer des écritures dans le cluster. On boucle ensuite sur la liste de Futures pour attendre la fin de l’écriture. Guava permet de simplifier l’écriture : `Futures.successfulAsList(futures)`

## Lab – Part 2

Slides : 100 à 140

Dans cette seconde partie, vous allez coder en Java 2 classes main :

1. Une classe **Writer** chargée d’écrire des messages dans la table _messages_
1. Une classe **Reader** chargée de lire les messages de la table _messages_, de les recopier dans une seconde table _devoxx.messages\_ack_ puis de les supprimer dans la 1ière table.

Pour vous y aider, vous pourrez vous référer aux exemples de code des slides précédents.
La branche [part2-first-design-squelette](https://github.com/thelastpickle/devoxxfr2018/tree/part2-first-design-squelette) met à votre disposition un projet Maven ainsi que des squelettes de classes qui sont à compléter.

Le correctif est disponible dans la branche [part2-first-design](https://github.com/thelastpickle/devoxxfr2018/tree/part2-first-design). Pour le tester en local, pensez à changer le ContactPoint.

En l’état, cette implémentation pose 2 problèmes :

1. Une **dégradation des performances** au cours du temps. A force des suppressions, on lit de plus en plus de Tombstones.
1. De la **concurrence de lecture**: les messages peuvent être traités par plusieurs participants.

La suite du Lab consiste à coder une deuxième implémentation corrigeant ces 2 problèmes.
Partez du squelette proposé dans la branche [part2-second-design-squelette](https://github.com/thelastpickle/devoxxfr2018/tree/part2-second-design-squelette).
Pour corriger le problème de performance, une solution consiste à designer la base autour des Tombstones.  On est contraint de supprimer les enregistrements, mais on limite la durée de vie des partitions en utilisant un bucketing temporel (à la minute). Du coup, on aura moins de tombstone par partition/lecture.
Pour résoudre le problème de concurrence de traitement, un système de verrou est mis en œuvre via l’introduction d’une colonne _processed\_by_. Ce sont les LightWeights Transactions effectuées sur le champ _processed\_by_ qui vont nous permettre de verrouiller les enregistrements.

La solution est disponible sur la branche [part2-second-design](https://github.com/thelastpickle/devoxxfr2018/tree/part2-second-design/).

Le Lab se termine par une présentation du mécanisme de compaction. La compaction permet de merger les données afin d’avoir des données à jour. Elle permet également de supprimer la Tombstone.
Lors d’opération en écriture, Cassandra écrit dans le Heap puis flushe sur disque dans un SSTable (fichier immuable). Lors d’une opération de lecture, Cassandra va essayer d’adresser le moins de SSTable possible.
