---
_edit_last: "1"
author: admin
categories:
  - spring
date: "2013-02-26T10:35:42+00:00"
guid: http://javaetmoi.com/?p=604
parent_post_id: null
post_id: "604"
post_views_count: "9417"
summary: Dans [un précédent billet](http://javaetmoi.com/2012/12/parallelisation-de-traitements-batchs-spring-batch/ "Parallélisation de traitements batchs"), je vous ai présenté les solutions mises en œuvre sur un projet pour paralléliser un batch d’indexation alimentant un moteur de recherche d’entreprise. Utilisée pour initialiser l’index de recherche puis le resynchroniser quotidiennement, la technique d’intégration par batch ne permet cependant pas d’indexer les données au fil de l’eau. Ce billet aborde précisément cet aspect. En effet, le fil de l’eau ou le quasi temps réel  fut dès le départ une exigence forte du métier. Recherches instantanées et auto-complétion révolutionnent le traditionnel formulaire de recherche mettant plusieurs secondes à renvoyer les résultats. Mais au prix de faire des recherches sur des données pouvant dater de J-1 ? Ce n’était pas acceptable ! Un middle d’indexation fut la réponse apportée.
tags:
  - architecture
  - elasticsearch
  - jms
  - soa
  - spring-framework
  - spring-integration
title: Architecture d’un middle d’indexation
url: /2013/02/architecture-middle-indexation-elasticsearch/

---
Dans [un précédent billet](/2012/12/parallelisation-de-traitements-batchs-spring-batch/ "Parallélisation de traitements batchs"), je vous ai présenté les solutions mises en œuvre sur un projet pour paralléliser un batch d’indexation alimentant un moteur de recherche d’entreprise. Utilisée pour initialiser l’index de recherche puis le resynchroniser quotidiennement, la technique d’intégration par batch ne permet cependant pas d’indexer les données au fil de l’eau. Ce billet aborde précisément cet aspect. En effet, le fil de l’eau ou le quasi temps réel  fut dès le départ une exigence forte du métier. Recherches instantanées et auto-complétion révolutionnent le traditionnel formulaire de recherche mettant plusieurs secondes à renvoyer les résultats. Mais au prix de faire des recherches sur des données pouvant dater de J-1 ? Ce n’était pas acceptable ! Un middle d’indexation fut la réponse apportée.

## Architecture technique

L’intégration d’un moteur de recherche dans un SI doit se fondre dans l’architecture technique en place. Voici quelques patterns d’architectures appliqués dans de nombreuses entreprises :

- **Haute-disponibilité** : applications déployées en cluster actif / actif, réparties sur N nœuds, robustes aux pannes et aux indisponibilités
- **Données sécurisées** : données non publiques, règles de visibilité assujetties  aux habilitations, DMZ
- **Architecture SOA** : nombreuses couches (Front Office / Middle Office / Back Office / Référentiels), couplage lâche, exposition des services en SOAP ou en REST, communications asynchrones passant par un EAI

Partant de ces règles, voici les exigences supplémentaires qui nous ont été formulées :

- Moteur de recherche installé comme infrastructure transverse au SI
- APIs du moteur de recherche non accessibles aux applications sources et utilisatrices
- Overhead minimal sur les transactions métiers déclenchant une indexation

Pour les respecter, a été développé un moteur d’indexation faisant office de middle avec le moteur de recherche ElasticSearch. Implémenté sous forme d’application web Java, l’utilisation d’une River ou d’un plugin auraient pu être des alternatives. Quelques avantages à la solution mise en œuvre :

- Industrialisation des livraisons sur un serveur d’application JEE
- Monitoring de l’application normalisé
- Livraisons sans interruption des services de recherche

Dialoguant avec les applications métiers et ElasticSearch, ce middle embarque la logique d’indexation et gère les montées de version du moteur de recherche avec leurs changements d’API.

Pour que les différents systèmes puissent notifier au middle d’indexation qu’une donnée a été créée / modifiée / supprimée, un composant de notification a été proposé aux applications JEE. Ce composant inclue un mécanisme d’interception des mises à jour des objets métiers.

Le diagramme ci-dessous démontre l’orchestration du processus d’indexation au fil de l’eau.

{{< figure align="alignnone" width=584 src="/wp-content/uploads/2013/02/architecture-middle-indexation.png" alt=" Chaque mise à jour d’une entité métier implique une opération d’indexation atomique." caption=" Chaque mise à jour d’une entité métier implique une opération d’indexation atomique." >}}

Le processus d’indexation se déroule en 4 étapes :

1. **Action de mise à jour** : vise à créer, mettre à jour ou supprimer un (ou plusieurs) objet du domaine métier ; cette action peut être réalisée aussi bien par un utilisateur (post d’un formulaire Struts, requête Ajax) que par un appel de web services (SOAP ou REST).
1. **Notifications**: information de mise à jour chargée de notifier le middle d’indexation qu’il est probablement nécessaire de (ré)indexer un document ou de le supprimer de l’index. Cette notification peut-être de 2 types :

   1. Autoportante : contient les données nécessaires à l’indexation
   1. Minimale : contient le  type de la données, son identifiant et la nature de l’action. Dans la suite de ce billet, c’est de ce type de notification dont nous parlerons.
1. **Lecture des données** : dans le cas d’une création ou d’une modification d’objet métier, les informations véhiculées par la notification autoportante permettent de déterminer quelles données sont nécessaires pour construire le document Lucene. En fonction du Back Office ou du Référentiel interrogé, ces données peuvent être récupérées de différentes manières : SOAP, REST, JDBC (vue base de données), JCA / CICS …  Plusieurs appels peuvent parfois être nécessaires pour agréger l’ensemble des données à indexer.
1. **Indexation**: construction du document Lucene à indexer, gestion du versionning et utilisation de l’API Java ElasticSearch.

## Composant de notification

Utilisé lors de la 1ière étape du processus d’indexation, un composant de notification est mis à disposition des applications développées en Java et dont le socle technique s’appuie sur le framework Spring. Conçu pour une intégration peu intrusive, il met à disposition une poignée d’annotations Java et se configure en quelques lignes de XML ou de Java.

Ce composant est lui-même décomposé en 3 phases :

1. **Interception des modifications**
1. **Construction de la notification**
1. **Publication vers le middle**

Techniquement, il s’appuie sur différents modules du Framework Spring :

- **AOP**: interception et interprétation des annotations
- **SpEL**: expressions acceptées par les annotations
- **Task**: parallélisation des phases de construction et de publication avec @Async
- **OXM** : marshalling XML des notifications
- **JMS**: publication de la notification vers l’EAI par le biais du JmsTemplate

Le niveau d’interception est généralement positionné sur les services métiers transactionnels de mise à jour unitaire ou massive des objets métiers. Une donnée n’est ainsi indexée que lorsque ses modifications sont effectives dans l’application source. En cas de crash, toute perte de notification est rattrapée par le batch de nuit ; l’utilisation d’un commit à 2 phases ou d’un mécanisme de rejeu ne sont donc pas nécessaires.

Voici un exemple d’application des annotations fournies par la brique d’interception sur le service métier CustomerService :

```java
@Transactional
@DataOperation
public void addPostalAddress(@DataRef(type="Person", id="#{id}") Customer customer, Address address)

@Transactional
@DataOperation(action = DataAction.DELETE)
public void deleteCustomer(@DataId(type="Customer") int id)
```

L’annotation _@DataRef_ permet de spécifier le type d’objet métier et offre la possibilité d’utiliser une Spring Expression Language pour récupérer dynamiquement l’identifiant de l’objet.

## Technique d’interception

A lui seul, le mécanisme d’interception pourrait faire office d’un second billet. Succinctement, il s’appuie sur un **post-processeur de beans Spring** qui analyse chaque bean Spring créé par le conteneur léger. Son implémentation s’inspire de celle des post-processeurs du Framework Spring tels _AsyncAnnotationBeanPostProcessor_ et _TransactionProxyFactoryBean_, tous deux responsables de respectivement traiter les annotations @Async et @Transactional.

Une fois le bean Spring initialisé, le post-processeur de bean intercale un **proxy AOP** héritant de la classe _AdvisedSupport_. Cette étape est facultative si un proxy a déjà été placé par un précédent post-processeur. Un aspect héritant de la classe _AbstractPointcutAdvisor_ est ensuite inséré en début de la chaîne d’aspects du proxy.

Cet aspect _DataOperationAnnotationAdvisor_ possède 2 composantes :

1. Un **point de coupe** ciblant les méthodes annotées avec _@DataOperation_
1. Un **greffon** implémentant l’interface _MethodInterceptor_ et en charge de parcourir la signature des méthodes à la recherche des éventuelles annotations _@DataId_ et _@DataRef_, de gérer les appels réentrants et les imbrications, de se synchroniser si besoin est avec le gestionnaire des transactions et, bien entendu, de tracker tout changement opéré sur les objets métiers.

Le diagramme ci-dessous illustre la mise en place du greffon _DataOperationInterceptor_ devant le bean _customerService_ :

{{< figure align="alignnone" width=584 src="/wp-content/uploads/2013/02/intercepteur-spring-notification.png" alt=" Intercepteur positionné par un post-processeur de beans Spring" caption=" Intercepteur positionné par un post-processeur de beans Spring" >}}

Toutes les modifications d’objet métier identifiées au cours d’une transaction sont ensuite assemblées au sein d’une notification qui est émise via JMS vers le middle d’indexation.

Bien qu’introduisant une adhérence supplémentaire, l’utilisation du support AspectJ de Spring aurait probablement proposée une implémentation plus légère. Attention toutefois à bien conserver l’ordre des intercepteurs : le _DataOperationInterceptor_ doit être placé avant le _TransactionalInterceptor_.

## Middle d’indexation

Le middle d’indexation n’est ni plus ni moins qu’un moteur de messages chargé de lire les notifications, de les traiter et de gérer les cas d’erreur.

Son implémentation peut être réalisée à l’aide de MDB, de Spring JMS, d’Apache Camel ou bien encore de Spring Integration. Ces 2 derniers présentent un intérêt tout particulier pour ce type d’architecture orientée messages et faisant appel à de nombreuses techniques d’intégration : JMS, SOAP, JDBC, REST, JCA, ElasticSearch …

Quel que soit la technologie, le middle est décomposée en 3 parties ayant chacune leur responsabilité :

**1\. Réception des notifications**

Le middle d’indexation traite les notifications en parallèle. L’utilisation de files JMS permet de lisser les pics de charge. La scalabilité horizontale du middle est assurée par un simple ajout de nœud (une Nième  JVM du serveur d’application).
Pour dimensionner le système en fonction, par exemple, de la volumétrie d’un type d’objet métier, différents pools de threads peuvent être configurés.

Une notification comportant plusieurs informations de mises à jour peut être découpée ; cela permet de segmenter le traitement d’une notification composite. Certains utiliseront l’EIP Message Splitter.
Les informations de mises à jour portant sur le même type d’objet métier sont ensuite acheminées vers le service dédié à la construction du document. L’usage de l’EIP Message Router est ici possible.

< !\-\- Lecture des notifications reçues sur la file JMS à l’aide du pattern EIP Channel Adapter -->

```xhtml
<int-jms:message-driven-channel-adapter "  destination=" inNotificationQueue" channel="notificationChannel" />
```

 **2\. Construction du document**

L’étape de construction du document à indexer demande tout d’abord de récupérer les données appropriées. Un ou plusieurs appels à des systèmes tiers sont nécessaires. Dans notre contexte, l’usage de web services SOAP était préconisé.
La construction du document Lucene est liée au mapping de l’index préalablement défini dans ElasticSearch, mapping lui-même créé en fonction du besoin métier en termes de recherche.
Une connaissance fonctionnelle et une expertise sur les moteurs de recherche sont ici indispensables et indissociables.  Les compétences de [Lucian Precup](https://twitter.com/lucianprecup) en ce domaine ne sont plus à démonter.

Une partie du code java peut être mutualisée avec le batch.

**3\. Indexation du document dans ElasticSearch**

L’indexation du document Lucene se fait à l’aide de l’API Java ElasticSearch.
Afin de pas perdre de notifications en cas d’erreurs volatiles, l’écriture est réalisée en synchrone.
Le versionning ElasticSarch permet de faire cohabiter simultanément batch quotidien et indexation fil de l’eau.

Côté code, le client ElasticSearch _[org.elasticsearch.client.Client](https://github.com/elasticsearch/elasticsearch/blob/master/src/main/java/org/elasticsearch/client/Client.java)_ est injecté dans le service chargé d’indexer les documents à l’aide d’une fabrique de beans Spring créée pour l’occasion ou de celle mise à disposition par [Dadoonet](https://github.com/dadoonet) dans le [projet spring-elasticsearch](https://github.com/dadoonet/spring-elasticsearch) hébergé sur Github.
Une extension Spring Integration pour ElasticSearch pourrait également avoir son intérêt.

## Conclusion

Si je ne vous ai pas perdus en route au fil de ces longues explications, vous vous dites probablement que le travail accompli est relativement conséquent alors qu’il parait plus simple et plus efficace d’indexer les données directement depuis l’application qui en est maitre.
C’est oublier que dans les grandes entreprises, séparation des préoccupations, découplage et sécurité sont de rigueur.
Pour garantir les performances, le middle d’indexation est déployé dans la même bulle réseau que les nœuds du cluster ElasticSearch. Niveau sécurité, le firewall garanti que seul le middle d’indexation a le droit d’indexer des données dans ElasticSearch.
Enfin, la mise en œuvre du composant de notification est facilitée sur les applications convenablement architecturées.
