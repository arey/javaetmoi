---
_edit_last: "1"
author: admin
categories:
  - conférence
date: "2015-11-13T13:00:47+00:00"
guid: http://javaetmoi.com/?p=1480
parent_post_id: null
post_id: "1480"
post_views_count: "6961"
summary: |-
  Sur les 12 représentations mondiales, la 3ième date de la tournée européenne de l [a conférence Elastic{ON}](https://www.elastic.co/elasticon) a eu lieu le 5 novembre 2015 à Paris.

  Invité par la société [Adelean](http://adelean.com/), j’ai pu y participé. Pour toutes celles et ceux qui n’ont pas eu cette chance, ce billet me permet de vous faire partager cette journée.

  [![elasticon-patis-2015-keynote](http://javaetmoi.com/wp-content/uploads/2015/11/elasticon-patis-2015-keynote.jpeg)](http://javaetmoi.com/wp-content/uploads/2015/11/elasticon-patis-2015-keynote.jpeg)
tags:
  - bigdata
  - elasticsearch
  - kibana
  - logstash
  - spark
title: Tout sur le Elastic{ON} Tour Paris 2015
url: /2015/11/tout-sur-elastic-on-tour-paris-2015/

---
Sur les 12 représentations mondiales, la 3ième date de la tournée européenne de l [a conférence Elastic{ON}](https://www.elastic.co/elasticon) a eu lieu le 5 novembre 2015 à Paris.

Invité par la société [Adelean](http://adelean.com/), j’ai pu y participé. Pour toutes celles et ceux qui n’ont pas eu cette chance, ce billet me permet de vous faire partager cette journée.

[![elasticon-patis-2015-keynote](/wp-content/uploads/2015/11/elasticon-patis-2015-keynote.jpeg)](/wp-content/uploads/2015/11/elasticon-patis-2015-keynote.jpeg)

# Plongée dans le produit et la roadmap

## Keynote de Shay Banon

Créateur du moteur de recherche Elasticsearch, Shay Banon a tout naturellement ouvert cette journée. Ce fut pour lui l’occasion de retracer la genèse de son bébé.
L’histoire d’Elasticsearch a commencé il y’a 15 ans par une **application de cuisine** baptisée iCook et que Shay avait développé pour sa femme. Basée sur Spring, Hibernate et Eclipse RCP, la fonctionnalité centrale était la barre de recherche positionnée sur la page d’accueil. Shay a très vite compris que le SQL n’était pas adapté à la recherche full text. Il a donc adapté l’architecture pour utiliser Apache Lucene. Voyant que son API de haut niveau pouvait adresser d’autres cas d’utilisation que la cuisine, il l’a open sourcé sous le nom de **Compass**.
Pour un utilisateur, Shay rappelle que le search doit être rapide. C’est d’ailleurs la fierté de Google qui affiche le temps d’exécution de ses requêtes.
Le temps a passé. Il y’a 5 ou 6 ans, le volume de données à indexer a considérablement augmenté. Shay a été confronté à de nouvelles problématiques pour distribuer les données et gérer les pannes. Il a alors initié un nouveau projet. Après 5 mois de développement, Shay l’a open-sourcé sous le nom d’ **Elasticsearch** (ES).
Très vite, l’adoption d’ES a dépassé ses espérances. Sa popularité a explosé. Un éco-système s’est construit autour. Accompagné de Steven Schuurman et Simon Willnauer, Shay décide alors de monter la société Elasticsearch qui a récemment été rebaptisé en **Elastic**.

S’ensuit alors quelques chiffres :

- Communauté de 35 000 membres
- 120 groupes utilisateurs répartis dans 80 villes
- 32 000 commits réalisés sur la stack Elasticsearch-Logstash-Kibana (ELK)
- 35 000 000 téléchargements

En France, David Pilato a grandement contribué au succès d’ES. Shay a été impressionné par tout ce qu’il a fait sur ES et l’a rapidement embauché.
Aujourd’hui, ES est composé d’ingénieurs venant de tout horizon, dont quelques français (j’ai d’ailleurs recroisé à Elastic{On} [Tanguy Leroux](https://github.com/tlrx)).
Des besoins ont très vites émergés autour Elasticsearch. La visualisation des données a été permise par Kibana. L’indexation de données a été facilitée Logstash. Et, plus récemment, Packedbeats a rendu possible la capture de trafic réseau. Ces 3 projets ont intégré Elastic
Aujourd’hui, la **Core Elastic Stack** est composée des 4 produits suivants :

- UI: **Kibana**
- Store, Index, Analyze: **Elasticsearch**
- Ingest: **Logstah**, **Beats**

A cette stack s’ajoute des **extensions**, parmi lesquels des produits commerciaux comme **Marvel**.

La keynote se termine par une liste de sociétés utilisatrices de solutions Elastic et dont la notoriété n’est plus à démonter :

- **Wikimedia**: Elasticsearch est la colonne vertébrale de Wikipedia
- **Mozilla**: afin de détecter des menaces en termes de sécurité, la stack ELK permet d’analyser en temps réel 300 millions d’évènements par jour.
- **NASA**: 30 000 messages et 100 000 documents envoyés 4 fois par jour par la sonde Mars Rover afin d’optimiser sa mission
- **Verizon**: 500 bilions de documents pour analyse temps réel des logs

Bien connus des développeurs, des acteurs comme GitHub ou Stackoverflow n’ont pas été cités.

## Elasticsearch 2 by Climton Gormley

Team Leader d’Elasticsearch, Climton Gormley a un background de **développeur Perl**. C’est l’un des tout premiers utilisateur d’Elasticsearch qui a contribué au développement de la communauté sur IRC et la mailing list.

Cimton commence son intervention par rappeler ce qu’est ES. C’est avant tout une couche d’abstraction permettant de **distribuer** les indexations et les requêtes sur plusieurs index Lucene. ES doit détecter les pannes. L’idée est de pouvoir utiliser ES de la même façon, que ce soit en local sur un poste de développement ou sur un cluster de 500 nœuds.
Dès le départ, un gros effort a été réalisé sur l’API, ceci afin qu’elle soit facile à utiliser pour les développeurs, quel que soit leur langage de programmation. Un peu plus tard dans la journée, un développeur Java me confirmait qu’il donnait 5 étoiles à leur API.
La recherche et l’analyse temps-réel est également une fonctionnalité centrale d’ES. Les agrégations ont été créées dans ce sens.
Climton enchaine sur les nouveautés apportées par **Elasticsearch 2.0** sorti la semaine précédente :

1. Amélioration de la **gestion des nœuds défaillants** et du temps de **restauration**.
1. **Ecritures durables**: lors de l’indexation d’un document, ES garantie dorénavant qu’un fsync est réalisé sur le disque.
1. Utilisation du **Java Security Manager** pour empêcher un hacker d’exploiter des failles de sécurité.
1. Afin de diminuer le trafic réseau sur de gros clusters, les états des shards sont envoyés sous forme de **deltas**.
1. Meilleure **compression des index** par utilisation des nouveautés apportées par Lucene 5.0.
1. Réduction de l’ **usage de la Heap** au profit de l’accès direct à la mémoire (off-Heap). Introduction des **doc-values**. Leur mise en cache est géré par le cache du filesytem (bien mieux que ne peut le faire la JVM). Gains en performance pour une Heap réduite.
1. La mise en **cache** automatique et le **merge des segments** sont plus intelligents.
1. Simplification du **Query DSL** en supprimant les filter au profit des query.

Le **pipeline d’agrégation** est une fonctionnalité majeure apportée par Elasticsearch 2.0. Adrien Grand est monté sur scène nous en parler.
Successeurs des facettes, Elasticsearch 1.0 avait introduit les **agrégations**.
Les pipelines d’agrégations d’Elasticsearch 2.0 permettent d’agréger des données agrégées. Autrement dit, ils permettent de combiner le résultat de plusieurs agrégations (ex : comparer 2 moyennes). Plusieurs opérations sont possibles : dérivé, somme cumulative, moyenne mouvante, min/mx/agv/sum …

Climton termine son talk par la roadmap d’Elasticsearch :

- Réécriture complète de la géo-localisation : moins d’espace sur disque et amélioration de la vitesse.
- [Query Profiling](https://github.com/elastic/elasticsearch/pull/12974): permet de mieux diagnostiquer la cause d’une requête lente. Graphiquement, un camembert permet de localiser les lenteurs.
- Administration :
  - API pour réindexer : besoin récurrent de réindexer les données. Change le mappings, reindex les données … en tâche de fond.
  - [API de gestion de tâches](https://github.com/elastic/elasticsearch/issues/6914): permet de suivre et d’interagir avec les traitements réalisés par ES en arrière plan (ex : réindexation)
- Enrichissements & Computations
  - Simplifier le pipeline alimentation de l’index
  - [Nouveau langage de script](https://github.com/elastic/elasticsearch/issues/13084). Propriétaire, il a été pensé pour fiabiliser le cluster.

## Kibana 4 par Boaz Leskes

Software Developer chez Elastic, Boaz précise que Kibana 4 est une réécriture complète de Kibana 3. Regroupées par thèmes, en voici les nouveautés :

- Powefull Analytics
  - Ajout du support des agrégations
  - Nouvelles fonctions d’analyse
- Robust Deployment
  - Kibana est packagé avec un server backend (node.JS). Cela permet de ne plus avoir à exposer son cluster Elasticsearch sur Internet.
  - Niveau de sécurité affiné
- Flexible Architecture
  - Design modulaire
  - Framework front-end moderne
  - Diagrammes rendus avec le framework D3
- Personnalisation
  - Carte personnalisable
  - Formateurs de champs
  - Field formatters
- Administration
  - Page de status du serveur Kibana
  - Niveau de logs configurable

## Ingest par Shay Banon

Par le terme « **Ingest**», on entend extraire des données et les pousser dans ES.

La force de Logstash 1 venait du nombre de plugins existants, permettant de gérer de nombreux use cases.  En effet, plus de 200 plugins existent. Et de nouveaux sortent régulièrement : Kafka, JDBC, HTTP et Salesforce.

Sorti le 28 octobre 2015, **Logstash** **2.0** apporte les nouveautés suivantes :

- Performance et résilience
  - Consistance de shutdown entre les plugins
  - Performances multipliées par 3 sur les plugins grok, useragent, geoip et JSON.
- Logstash 1 n’utilisait qu’un seul cœur. La version 2 profite désormais de toute la puissance du serveur.

Quelques annonces ont ensuite été réalisées au sujet des **futures fonctionnalités** de Logstash :

- Utilisation de files (queue)
  - Persistantes
  - A taille variables
  - Avec gestion d’une Dead Letter Queue
- Gestion et securité
  - Health monitoring
  - Gestion centralisée
  - Installation de plugins en offline

Shay rappelle la dualité de Logstash : être à la fois très léger en tant qu’agent (prendre le moins de CPU) et consommer un maximum de ressources en tant que serveur.
Désormais, Logstash sera cantonné à la partie serveur. Son remplaçant côté client est **[Beats](https://www.elastic.co/products/beats)**, une API très légère permettant de collecter des données.

Plusieurs projets bâtis au dessus de Beats existent dans le GitHub elastic :

- **[Packetbeat](https://github.com/elastic/packetbeat)** : un analyseur réseau supportant les protocoles HTTP, MySQL, PostgreSQL (et bientôt ICMP et AMQP).
- **[Topbeat](https://github.com/elastic/topbeat)** : index l’utilisation processeur des processus d’un OS (Windows, Mac OSX, Linux sont supportés).
- [**Filebeat**](https://github.com/elastic/filebeat) : envoi de fichiers (ex : logs) remplaçant logstash-forwarder.

A l’instar de **Metricsbeat**, de nouveaux projets basés sur Beats verront le jour.

## Extensions par Steve Mayzak

Steve se présente comme Solutions Architect Team Lead. Au cours de sa session, il nous a présenté différentes extensions d’Elasticsearch. Produits commerciaux, ils sont offerts lors de la souscription d’un support ES.

Un besoin récurrent des clients étaient de sécuriser leurs données. C’est chose faite avec **Shield** :

- Protection par login / mot de passe
- Restrictions au niveau des documents et des champs
- S’interface aux solutions SSO des entreprises
- ES accepte désormais le login des utilisateurs

Prochainement, Shield améliorera son intégration avec une API de configuration et le support de Kibana.

**Watcher** est une extension permettant de gérer des alertes et dres notifications :

- Mise en place d’alertes liées à vos données
- Notifications flexibles

**Marvel** permet de monitorer, diagnostiquer et optimiser un cluster ES.  Changements de Marvel 2.0 :

- Redesigné afin de profiter de Kibana 4
- Plus simple d’utilisation

Future de Marvel : monitoring de Logstash, Kibana, Beats

De **prochaines extensions** sont dors et déjà inscrites à la roadmap d’Elastic :

- API et IHM de graphe
- Réplications de cluster sur plusieurs data center (ex d’usage : Disaster Recovery)
- Utilisation d’ES pour du Machine learning

## Found : Elasticsearch as a Service par Morten Ingrebrigsten

 [**Found**](https://www.elastic.co/found) est présenté comme le seul service complet hébergeant les produits Elastic. Gage de qualité pour les DSI, son support est assuré par l’équipe de développement ELK.
Basé sur Docker, 2 offres sont disponibles : Standard et Premium.
L’offre Found on Premise package toute la stack ELPK pour un déploiement sur un Cloud privé ou public.

## Elasticsearch for Apache Hadoop

Ingénieur Elastic, Costin Lea est venu nous parler du produit **[Elasticsearch for Apache Hadoop](https://www.elastic.co/products/hadoop)**. Costin commence par nous rappeler que l’écosystème Hadoop est très vaste: Hive, Storm, HDFS, Cloudera, Hortonworks.

L’intégration d’Hadoop et d’ES a été pensée dans les 2 sens :

1. ES => Hadoop : backup des données sur HDSF + requête ES depuis Hadoop
1. Hadoop => ES : indexer les données directement dans ES

Depuis ses prémices, Hadoop a beaucoup évolué.

**Hadoop 0.20.x/1.x :**

1. storage (HSFS)
1. et framework Map / Reduce pour extraire et traiter les données de manière distribuée

Hadoop est alors un produit difficile à prendre en main. Cascading et Hive ont été crées pour en simplifier l’usage.

**Hadoop 2.x**:

Entre HDFS et Map / Reduce, l’introduction de la couche [YARN](http://hadoop.apache.org/docs/current/hadoop-yarn/hadoop-yarn-site/YARN.html) a permis d’ouvrir Hadoop à d’autres traitements que le Map / Reduce.

**ES-Hadoop** est certifié pour fonctionner avec les principales distribution d’Hadoop : Cloudera, Hortonworks, Mapr, Concurrent, Databriks.

Costin continue son talk par un slide présentant un exemple d’intégration de Spark et d’ES avec Scala. Une [initiation à Spark](/2015/04/initiation-apache-spark-en-java-devoxx/) était nécessaire pour le comprendre. Ce que j’en ai retenu est que la classe **_SparkContext_** (package _org.elasticsearch.spark_) d’ES-Spark apporte 2 méthodes :

1. _esRDD_ pour charger un RDD depuis ES
1. _saveToEs_ pour écrire un RDD dans ES

Le RDD ES supporte Spark SQL. Au runtime, le Spark SQK est converti en Query DSL ES.
Enfin, aucun setup n’est nécessaire pour faire fonctionner le code donné en exemple (pas de settings particulier d’ES).

La Roadmap d’ES-Hadoop est la suivante :

- Support des agrégations
- Intégration avec Marvel
- Machine Learning : utilisation dans Spark d’informations connues. Les workers Hadoop ne communiquant pas ensemble, le partage de données permettra l’alléger la charge globale de travail

# Retours d’expérience

L’après-midi a été consacrée à différents retours d’expérience de mise en place d’Elasticsearch dans de grandes entreprises : Orange, ERDF, Natixis, PSA et AXA.

## How Orange is moving its French web search engine to Elastic products

Depuis 1996, Orange propose sur son portail un moteur de recherche destiné aux Internautes francophones. Le moteur propose des recherches thématiques. Derrière chaque recherche thématique, il y’a une [technologie propriétaire différente.](https://www.elastic.co/blog/how-elasticsearch-helped-orange-to-build-out-their-website-search) Depuis 2013, [Orange migre peu à peu tous ces moteurs thématiques vers Elasticsearch](http://blog.lemoteur.fr/pourquoi-le-moteur-de-recherche-dorange-est-un-utilisateur-delasticsearch/).
Le 1er moteur thématique a été mis en prod en 2014.
Début 2016, les 1,2 milliards d’URL analysées par Orange le seront par Elasticsearch.

Dès le crawl des pages web, un indicateur de qualité est calculé à partir de l’URL.
Techniquement, Orange maintient un fichier contenant des expressions régulières (regex) permettant de détecter si une page est en français, contient des spams … Les regex permettent de tagger des URL avec des labels. A chaque label correspond un score. Les URL sont consultables dans Kibana.
La pertinence du résultat ne se limite pas au TF/IDF d’ES. Orange effectue des calculs de graphes.

L’architecture technique retenue par Orange est la suivante :

- Architecture dockerisée
- 6 clusters ES gérant chacun 200 millions d’URL
- Chaque cluster est formé de 13 machines
- Répartition des nœuds d’un cluster : 3 nœuds clients et 10 nœuds data

Les performances sur **ES 1.5** ont été obtenues de manière empirique en effectuant plusieurs essais avec des paramétrages différents. Voici les valeurs remarquables retenues :

- Filter cache size : 20%, 30%, 60%
- Nombre de machines : 10 (mieux que 20). L’ajout de machines engendrait de l’overhead pour agréger les résultats.
- Nombre d’ _processor_: pas réglé (ne sait pas si ce paramétrage est lié à l’usage de Docker ou non ?)
- Parser JSON : librairie RapidJSON (C++)
- Nombre de shards : 20. Deux shards par machines ont permis une utilisation efficiente du CPU.
- Nombre de réplica : 0 (ne sert à rien de répliquer dans leur cas)
- Volume de RAM : 48 Go. Le passage de 8 à 48 a augmenté les performances, sans les doubler. Possibilité de redescendre à 8 Go si besoin de libérer des ressources matérielles.
- Agrégation en 2 requêtes : la 1ière pour remonter les ID des documents, et la 2ième pour récupérer les champs souhaités
- Les 3 nœuds clients permettent de déterminer sur quel nœud data les documents doivent être indexés.

Jean-Pierre Paris explique que la montée de version vers Elasticsearch 2 nécessitera de revoir ce paramétrage et de refaire des benchs. Afin d’être exploitable, la collecte des résultats des tests demande de la rigueur. Orange a spécifiquement développé un outil pour ses benchs. Ils comptent obtenir un Licence Agreement auprès Elastic afin de pouvoir commiter sur GitHub (CCLA).

Pour finir, voici quelques chiffres sur l’indexation :

- 1,2 milliards de documents à indexer
- 4,2 To d’index
- Durée d’indexation de 2h45 (avec leur ancien système, c’était de 10 ou 12h)

## Centralisation de grands volumes de logs chez ErDF

Architecte chez ErDF, Vladislav Pernin présente l’architecture basée sur la stack ELK, Kafka et Ansible retenue pour gérer ses logs. [Ses slides sont disponibles sur Speaker Deck](https://speakerdeck.com/vladislavpernin/elastic-on-tour-paris-centralisation-de-grands-volumes-de-logs).

Contexte :

- Beaucoup de serveurs
- Architecture distribuée & asynchrone
- Accès aux logs limités

Cas d’utilisation :

- Surveiller les environnements : de dév à la prod
  - Bouton pour créer des anomalies sur Jira avec tout le contexte du log
- Pattern de recherche de bug. Exemple : depuis quand cette exception est-elle apparue ?
- Audit pro-actif (enchainement de logs)
- Tracer le chemin d’un utilisateur
- Statistiques métiers : taux d’utilisation des fonctionnalités
- Surveillance des 35 millions de compteurs électriques communiquant en cours de déploiement

Quelques chiffres :

- En production depuis 4 ans.
- 8 projets, 50 environnements, 900 serveurs
- 65 types de log
- 1,1 milliards de doc & 290 Go d’espace disque
- 250 logs / secondes

Vladislav poursuit son intervention par un retour d’expérience de chacune des solutions techniques mises en œuvre.

**Logstash**

En 2011, le choix d’utiliser Logstash a été guidé par :

- Son tail intelligent
- Sa richesse fonctionnelle
- Son installation facile
- La facilité de créer un patch en attendant sa prise en compte par l’équipe de dév

Vladislav donne 3 conseils sur groks :

- Tester unitairement
- Tests de performances afin d’affiner les regex
- Multiplier les logs pour la scalabilité horizontale

Problèmes rencontrés :

- Encore jeune et mouvant
- Perte de données possibles (queue non persistance)
- 40 secondes de démarrage
- Ligne de logs partielles lors de la journalisation des logs (sur Apache) et liée a problème des inodes Linux

**Kafka**

Les logs ont d’abord été transportés via RabbitMQ.
Au dessus de 5000 logs/s, RabbitMQ ne supportait plus la charge.
Le passage à Apache Kafka a permis d’atteindre le débit à 200 000 logs/s sans tuning.
Malgré quelques défauts de jeunesse, Kafka est robuste, persistant et scalable.
Désormais, les applications Java envoient directement leurs logs au format JSON (appender Kafka pour Logback. Kafka shadé pour éviter les conflits de version). Ainsi, elles n’ont plus besoin de logger sur le filesystem.

**Elasticsearch**

Ses points fort selon Vladislav :

- Outil mature
- Grande communauté
- Documentation de bonne qualité
- Installation facile
- Release fréquente, upgrade facilitée

Lors de son choix en 2011, ES était balbutiant.

Quelques problèmes

- Sur versions anciennes : tri, indexes corrompus, OutOfMemory
- Recovery trop long
- River RabbitMQ remplacée par Lohstash en push direct
- Volumétrie fluctuante mais sharding fixe
- Aucun support natif de la Sécurité (Shield comme produit commercial)
- Prises-en compte du nouveau mapping lors de la rotation d’index

API query :

- Puissante mais compliquée
- Jointures impossibles pour les développeurs venant du monde SQL. Un document ES doit en effet être auto-suffisant.

Mapping :

- Nécessite de connaître le type de recherche pour définir le mapping

Bonnes performances sur SAN et VM.

En 2011, l’IHM de Logstash ne fonctionnait pas et celle de Kibana était non utilisable. ErDF a donc développé sa propre IHM propriétaire. Aujourd’hui, ils partiraient sur du Kibana

Travail à réaliser sur la qualité des logs :

- Uniformisation de la structure
- Utilisation d’un ID de corrélation : permet de suivre les appels d’un système à l’autre
- Enrichissement : environnement, projet, application

Leur déploiement est automatisé avec Ansible.
ErDF a fait le choix de groker sur le serveur plutôt que sur les clients.

Pour superviser cette architecture, ils génèrent un log toutes les 5 secondes sur chaque machine puis vérifient sa présence dans ES.

A l’avenir, la volumétrie va être x 100.

## Comment Natixis Financement a enrichi sa vision client avec Elasticsearch

Natixis est la banque de financements du Groupe Banque Populaire Caisse d’Epargne. Elle vend des prêts personnels et du crédit revolving. Cette entité compte aujourd’hui 6 millions de clients.

Pendant le développement d’un poste de travail pour les chargés de clientèle, ils ont eu besoin d’agréger des données (interactions avec les clients) issues d’une dizaine d’applications. Les données sont reçues depuis différents canaux : SMS, site Internet, appels téléphoniques … Et leur collecte est réalisée à la fois par batch (intégration de fichiers CSV) et en temps réel (WS REST).
Leur exigence fonctionnelle était de pouvoir y accéder à la fois par Web Service et par une IHM de recherche multi-critères intégrée au poste de travail.
Le projet a été réalisé en 4 mois (de mars à juin 2015).

Quelques chiffres :

- 350 utilisateurs
- 10 critères de recherche : identifiant client, agence, date, canal de contact, motif de l’interaction, nom du client …
- Temps de réponse < 3 secondes
- Volume de données croissant : plusieurs dizaines de millions à l’horizon 2017

Aucune donnée confidentielle n’est stockée dans ES.

## Kibana l’efficience à PSA

Architecte Big Data à PSA Peugeot Citroën, Alexandre Fricker débute son intervention par nous confier que PSA n’autorise l’utilisation de composants Open Source que depuis 2006.
En 2015, leur stack de développement a été open sourcé.
De manière confidentielle, Elasticsearch est utilisé depuis 2011 pour la gestion des logs.
En 2013, il a réalisé une démo d’Elasticsearch à 4 BU.
Suite à sa démo, 20 projets ES été développés en 2014. L’utilisation d’Es couvre plusieurs domaines : logs centralisés, mesure de la qualité de service, géolocalisation par IP (identifier des tentatives de déni de services).
En 2015, pas moins de 75 projets sont menés avec ES. Son usage se diversifie encore davantage : maintenance de la chaine de production de l’usine de Poissy, analyse des pannes.
Une présentation d’Elasticsearch est faite au DSI et à la Direction Industrielle.
En 2016-2017, est prévue la systématisation des usages démontrés en 2015.
De nouveaux usages sont encore possibles :

- Traitements des logs de sécurité
- Indexation et recherche documentaire
- Big Data : données venant du véhicule connecté
- Métrologie davantage plus réelle
- GTC, monde industriel et logistique

L’architecture technique est simple. Tous les projets sont hébergés sur un cluster 8 nœuds.
1 index est créé par projet.

## Panel de discussion avec Axa

Fabien Janssens, IT Solution Design chez Axa, conclue cette journée par une intervention sous forme de questions / réponses.
Il rappelle que la donnée est au cœur du business d’Axa. Leurs données centrales sont leurs clients et leurs contrats.
Le SI d’AXA souffre d’un gros problème de technologies legacy liées aux fusions / acquisitions successives.
En 2013, Axa crée un [Data Innovation Lab](http://www.latribune.fr/entreprises-finance/banques-finance/20140605trib000833675/axa-se-lance-dans-le-big-data.html). Son premier projet a été la création d’un **Data Lake**. Toutes les données du SI y sont conservées à tout jamais, sans traitement. Ce lac peut être vu comme un disque géant. L’historique des données est conservé.

Apache Spark est utilisé pour réaliser des traitements et faire parler des données. La détection de fraude et le marketing sont 2 cas d’usage parmi d’autres.
Un Data Lake est crée pour chaque catégorie de données. Leur premier Data Lake fut consacré aux clients. Axa a modélisé un document JSON par client. Ce document est enrichi avec les nouvelles sources de données connectées au Data Lake. Au total, 3 millions de clients sont référencés. Et tous les champs sont indexés. Le scoring réalisé par Spark est remonté dans ES.
Techniquement, le cluster ES tourne avec 3 nœuds.
Le prochain Data Lake sera dédié aux produits.
