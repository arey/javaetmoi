---
_edit_last: "1"
_wp_old_slug: loffre-compute-de-google-cloud-platform
author: admin
categories:
  - conférence
date: "2016-07-04T17:09:05+00:00"
guid: http://javaetmoi.com/?p=1618
parent_post_id: null
post_id: "1618"
post_views_count: "3166"
summary: |-
  J’ai eu l’opportunité d’assister à une journée de découverte de la plateforme **Cloud** de Google. Dispensée dans les locaux parisiens de Google, cette formation d’une journée était animée par **Didier Girard**, Google Developer Expert et Directeur Général Délégué de Sfeir. Ce fut l’occasion de découvrir la diversité des offres proposées par la **Google Cloud Platform** et de pouvoir les comparer à celles, plus médiatisées, d’autres géants du web tels Amazon (AWS) et Microsoft (Azure).

  Large, la gamme de services Google Cloud Platform est répartie en 4 offres :

  - Compute : App Engine, Container Engine, Compute Engine
  - Storage : Bigtable, Cloud Storage, Cloud SQL, Cloud Datastore
  - Big Data: BigQuery, Pub/Sub, Dataflow, Dataproc, Datalab
  - Machine Learning: Vision API, Machine Leargning, Speech API, Translate API

  Cet article se focalisera sur l’ **offre Compute**. Mais avant d’aller plus loin, arrêtons-nous un moment sur ce qui est l’une des forces de la plateforme Cloud de Google : son infrastructure.

  ![Didier Girard à la formation Google](http://javaetmoi.com/wp-content/uploads/2016/06/Didier-Girard-à-la-formation-Google-1024x656.jpg)
tags:
  - cloud
  - docker
  - google
title: L’offre Compute de Google Cloud Platform
url: /2016/07/offre-compute-google-cloud-platform/

---
J’ai eu l’opportunité d’assister à une journée de découverte de la plateforme **Cloud** de Google. Dispensée dans les locaux parisiens de Google, cette formation d’une journée était animée par **Didier Girard**, Google Developer Expert et Directeur Général Délégué de Sfeir. Ce fut l’occasion de découvrir la diversité des offres proposées par la **Google Cloud Platform** et de pouvoir les comparer à celles, plus médiatisées, d’autres géants du web tels Amazon (AWS) et Microsoft (Azure).

Large, la gamme de services Google Cloud Platform est répartie en 4 offres :

- Compute : App Engine, Container Engine, Compute Engine
- Storage : Bigtable, Cloud Storage, Cloud SQL, Cloud Datastore
- Big Data: BigQuery, Pub/Sub, Dataflow, Dataproc, Datalab
- Machine Learning: Vision API, Machine Leargning, Speech API, Translate API

Cet article se focalisera sur l’ **offre Compute**. Mais avant d’aller plus loin, arrêtons-nous un moment sur ce qui est l’une des forces de la plateforme Cloud de Google : son infrastructure.

![Didier Girard à la formation Google](/wp-content/uploads/2016/06/Didier-Girard-à-la-formation-Google.jpg)

## L’Infrastructure de Google

Bien que la technologie de conteneurisation ait été placée sur le devant de la scène il y’a 2 ans par Docker, Google a une très longue expérience dans ce domaine. A titre d’exemple, Google App Engine est basée sur des **containers** depuis son début. Google n’utilise pas de VM.
Google a également une expertise indéniable dans la gestion à grande échelle de containers. Dans ses Data Centers, chaque semaine, 2 milliards de containers sont arrêtés et démarrés. Connu en interne sous le nom de [Borg](https://www.quora.com/What-is-Borg-at-Google), Google a d’ailleurs open sourcé son système d’orchestration de containers [**Kubernetes**](http://kubernetes.io/).

L’infrastructure technique de Google est l’une des plus puissantes au monde. Elle repose sur 3 piliers :

1. **Data Center**: parmi les Cloud Providers, Google n’a pas le plus de Data Center. Mais il va drastiquement augmenter leur création. En 2016, Google va en construire dans 12 nouveaux pays. Un Data Center est prévu en France pour 2018. Depuis 2015, les 2 infrastructures internes et externes convergent. Ainsi, votre application déployée sur le Cloud de Google s’exécutera sur les mêmes machines que, par exemple, Google Docs. Sauf Gmail continuera à fonctionner sur une infra interne.
1. **Backbone**: depuis 2008, Google cofinance le déploiement du réseau Internet sur la planète. Tous les Data Centers de Google sont reliés par fibre optique.
1. **Edge Caching**: pour ses services, Google a besoin de nombreux « points de présence ». Des systèmes de cache sont mis en place sur les points de présence (il s’agit de CDN). Ce cache est mis à disposition gratuitement sur App Engine et Compute Engine.

Enfin, l’infrastructure Cloud de Google est découpée en **zones** (un data center) et en **régions** (plusieurs zones).

L’offre Compute de Google regroupe 3 services vous permettant de déployer vos applications sur le Cloud de Google :

1. App Engine
1. Container Engine
1. Compute Engine

## Google App Engine

 **Google App Engine** (GAE) est une plateforme hautement scalable dédiée aux applications web, aux jeux et aux backends d’applications mobile. Didier a commencé à la béta-tester en 2008. Il nous cite plusieurs références :

1. **A bon entendeur**: développée par Didier, cette application Androïd de détection de zones de danger a atteint 1 millions de téléchargements et des pics de 10 000 utilisateurs simultanés. En forte charge, son coût mensuel n’est que de 2$.
1. **Snapchat**: son backend est sous App Engine. En 2015, sur 20 personnes, ils n’ont aucun Ops. Techniquement, ce sont les Ops de Google. Aujourd’hui, Snapchat dépasse Twiter en nombre d’utilisateurs.
1. **Conférence des évêques de France**: chaque année, le 24 décembre entre midi et 16h, le trafic de leur site permettant de consulter les horaires de messe est multiplié par 100. Economiquement, migrer vers GAE a été bien plus rentable (30$ mensuel) que de louer 100 machines.
1. **Google Street Art**: référencé sur la page d’accueil de Google Search, le site web doit supporter 50 millions de visiteurs en 24h. Pour des applications à fort trafic, Didier précise qu’il est nécessaire de vérifier les quotas de toutes les API utilisées (ex : nécessité d’une dérogation pour Google Maps qui est limité à 1)
1. Client présent dans le monde entier avec plein de micro-app (ex : note de frais). Pour des questions de temps de réponse, ces applications doivent être déployées dans plusieurs data centers. Le coût de développement de la migration vers Google Apps est prévu pour être amorti en 2 ans. Le ROI est très élevé car **28h de CPU par jour sont gratuits**.

Didier précise qu’il est **difficile de porter une application existante dans App Engine**. Si l’application n’est pas pensée pour ce type d’architecture, le coût sera prohibitif.
A la question _« Pourquoi GAE n’est-il pas plus utilisé ? »_, Didier répond que Google App Engine est trop en avance et souffre d’un problème de vocabulaire (ex : instance vs container).

Nativement, Google App Engine propose **4 runtimes managés**: Python 2.7, Java 7, Go et PHP. Didier nous fait un retour d’expérience sur les 3 premiers :

- **Python**: rapide au démarrage mais lent à l’exécution. Bien pour les applications web avec du cache.
- **Java**: démarre lentement, mais rapide à l’exécution. Possibilité de pré-chauffer des instances pour encaisser le trafic.
- **Go**: le meilleur des 2 mondes : démarre et s’exécute vite. Le service Uber de géolocalisation a été recodé en Go. Pour avoir un ordre d’idée, Go peut consommer 10x moins que du Python

Le fait d’utiliser l’un de ces 4 runtimes permet de bénéficier de runtimes pré-chauffés permettant d’absorber rapidement la charge. Lors d’une démo, une application Go a été mise en ligne en quelques ms.
L’ **historisation des versions** est l’une des fonctionnalités phares de GA : jusqu’à 10 versions d’une même application sont historisées. Toutes les versions sont utilisables via des URL dédiées. GAE offre la possibilité de faire du split trafic. Par exemple, 3% du trafic passent sur une nouvelle version. Cela permet de mesurer le business. Bien entendu, les logs sont splittés par version.

Didier nous sensibilise sur le fait que GAE a une approche très puriste du Cloud. De ce fait, il est interdit d’écrire sur le filesystem. Et il n’existe pas de sessions web. L’utilisation de solution de stockage est nécessaire. Par ailleurs, il est interdit d’installer de librairies tierces sur l’OS.
Pour pallier à ces limitations, il est possible de passer par des **Flexible Machines**. Elles remplacent les Managed VM et permettent de créer ses propres containers avec un **Dockerfile**. Ainsi, il est possible de faire exécuter une application **Java 8** dans GAE.
Cette personnalisation a un coût : le tarif d’une Flexible Machine est celui d’une instance Compute Engine.

## Google Container Engine

A mi-chemin entre le IaaS et le PaaS, **Google Container Engine** permet d’exécuter ses propres containers Docker sur l’infrastructure de Google. Container Engine est, en quelque sort, la version managée de **Kubnernetes**.

L’utilisation de Container Enfine demande pour pré-requis de connaître les concepts d’architecture suivant :

- **Container**: unité de base
- **Pod**: ensemble cohérent de conteneurs. C’est ce qu’on manipule avec Kubernetes. Un pod n’est pas public. On peut l’exposer via un service (association d’un port à un pod).
- **Node** : instance Google Compute Engine
- **Master**: supervise le fonctionnement des nœuds
- **Replication Controler**: à partir d’un template de pod, ce contrôleur peut créer des pods pour absorber la charge.

A noter que Google permet d’héberger des **images Docker privées** via son **Google Container Registry**.

## Google Compute

 **Google Compute** est la solution **IaaS** (bare-metal) de Google. La création d’une machine se fait sur mesure :

- CPU
- Image de Boot avec un image préinstallée (Ubuntu, Windows …) ou personnalisée
- Préemptible ou non : Google peut vous la reprendre à tout moment en échange d’un meilleur tarif.
- Taille du disque (max de 64 To) et type : Standard, SSD, local SSD
- Suppression ou non du disque au boot. Cette fonctionnalité a été utilisée au cours d’une démo pour créer une image du disque avec un serveur Apache installé
- Disque partageable entre plusieurs machines

Les fonctionnalités sont nombreuses :

- Snapshots (versionning de disque)
- Resizing de disque à chaud
- Startup scripts (fichier hébergé sur Cloud Storage)
- Auto-scaling
- Facturation à la minute (à partir de la 10ième minute).

Niveau **réseau**, on peut créer/manager VPN, DNS, Load Balancing (HTTP, UDP, TCP), CDN, interconnexion en fibre avec le data center Google. Tout est prévu pour recréer son infrastructure réseau dans les Data Center de Google.

Enfin, Compute Engine vient avec des outils :

- **Cloud Functions**: petit bout de code JS (s’exécute sous node.JS)
- **Stackdriver**: tableaux de bord de monitoring du Cloud Google et Amazon
- **Source Repositories**: repository Git, debugging en prod pour récupérer des valeurs de variables.

## Conclusion

Moi qui avait déjà [testé et apprécié Google App Engine en 2012](/2012/04/devoxx-initiation-google-app-engine/), cette formation m’aura plus particulièrement permis de découvrir les autres services de l’offre Compute. Basés sur Docker, Flexible Machine et Container Engine sont mes coups de cœur.

Sujet que je n’ai pas abordé mais qui est primordial pour les décideurs : les tarifs d’accès à la plateforme. Sachez qu’il n’y a **pas de contrat** spécifique. Les tarifs sont publics. Les dégressivités s’appliquent automatiquement. Bien entendu, plus on on descend vers du sur-mesure et du dédié, plus les tarifs s’élèvent. Et à l’inverse, plus on utilise les services managés de Google, plus la facture s’allège, l’utilisation de la plateforme se simplifie (moins d’Ops) et la scalabilité est facilitée.

Enfin, des produits comme App Engine et Big Query permettent à une entreprise de devenir **Server Less**. Nul besoin de se préoccuper des serveurs.
