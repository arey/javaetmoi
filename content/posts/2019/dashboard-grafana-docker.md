---
_thumbnail_id: "1960"
_xmlsf_image_featured:
  caption: ""
  loc: https://javaetmoi.com/wp-content/uploads/2019/03/2019-03-Dashboard-Grafana-dockerisé-grafana.png
  title: 2019-03 - Dashboard Grafana dockerisé - grafana
author: admin
categories:
  - retour-d'expérience
featureImage: wp-content/uploads/2019/03/2019-03-Dashboard-Grafana-dockerisé-grafana.png
featureImageAlt: 2019-03 - Dashboard Grafana dockerisé - grafana
date: "2019-03-28T17:27:32+00:00"
toc: true
thumbnail: wp-content/uploads/2019/03/2019-03-Dashboard-Grafana-dockerisé-grafana.png
guid: http://javaetmoi.com/?p=1959
parent_post_id: null
post_id: "1959"
post_views_count: "12565"
summary: |-
  A l’instar de SLF4J pour les logs, **[Micrometer](https://micrometer.io/)** est la **façade d’export de métriques** utilisée par Spring Boot et ses Actuators. Micrometer supporte une douzaine de systèmes de monitoring : Datalog, Netflix Atlas, New Relic, JMX, CloudWatch, InfluxDB ou bien encore Prometheus.

  Récemment, j’ai poursuivi le travail initié par Kevin Crawley pour intégrer **Prometheus** et **Grafana** dans la version microservices de Spring Petclinic. Proposée par Maciej Szarliński, l’idée consistait à remplacer les compteurs **Micrometer** de typeregistry.counter("create.visit").increment() par l’ [annotation @Timed.](https://micrometer.io/docs/concepts)

  J’ai profité de ce changement pour améliorer le packaging **Docker** de Grafana et en simplifier l’accès. Pour accéder au dashboard personnalisé exposant l’évolution du nombre d’animaux et de propriétaires, un _docker-compose up_ suivi d’un clic sur l’ [URL du dashboard](http://localhost:3000/d/69JXeR0iw/spring-petclinic-metrics) sont désormais suffisant.<br>**Ce billet présente les configurations Docker et Grafana mises en oeuvre**.

  [![Dashboard Grafana Spring Petclinic Metrics](wp-content/uploads/2019/03/2019-03-Dashboard-Grafana-dockerisé-grafana.png)](wp-content/uploads/2019/03/2019-03-Dashboard-Grafana-dockerisé-grafana.png)

  ![2019-03 - Dashboard Grafana dockerisé - grafana](wp-content/uploads/2019/03/2019-03-Dashboard-Grafana-dockerisé-grafana.png)
tags:
  - docker
  - grafana
  - microservices
  - prometheus
title: Dashboard Grafana dockerizé
url: /2019/03/dashboard-grafana-docker/

---
A l’instar de SLF4J pour les logs, **[Micrometer](https://micrometer.io/)** est la **façade d’export de métriques** utilisée par Spring Boot et ses Actuators. Micrometer supporte une douzaine de systèmes de monitoring : Datalog, Netflix Atlas, New Relic, JMX, CloudWatch, InfluxDB ou bien encore Prometheus.

Récemment, j’ai poursuivi le travail initié par Kevin Crawley pour intégrer **Prometheus** et **Grafana** dans la version microservices de Spring Petclinic. Proposée par Maciej Szarliński, l’idée consistait à remplacer les compteurs **Micrometer** de typeregistry.counter("create.visit").increment() par l’ [annotation @Timed.](https://micrometer.io/docs/concepts)

J’ai profité de ce changement pour améliorer le packaging **Docker** de Grafana et en simplifier l’accès. Pour accéder au dashboard personnalisé exposant l’évolution du nombre d’animaux et de propriétaires, un _docker-compose up_ suivi d’un clic sur l’ [URL du dashboard](http://localhost:3000/d/69JXeR0iw/spring-petclinic-metrics) sont désormais suffisant.  
**Ce billet présente les configurations Docker et Grafana mises en oeuvre**.

[![Dashboard Grafana Spring Petclinic Metrics](wp-content/uploads/2019/03/2019-03-Dashboard-Grafana-dockerisé-grafana.png)](wp-content/uploads/2019/03/2019-03-Dashboard-Grafana-dockerisé-grafana.png)

## Docker compose

Le [docker-compose.yml](https://github.com/spring-petclinic/spring-petclinic-microservices/blob/master/docker-compose.yml) de Spring Petclinic Microservices est relativement simple : il pointe sur 2 Dockerfile Grafana et Promotheus personnalisés.

L’usage de volume Docker n’est pas nécessaire.  
A noter que le port 9090 de Prometheus est mappé sur le port 9091 car le port 9090 était déjà occupé par Spring Boot Admin.

```yaml
grafana-server:
  build: ./docker/grafana
  container_name: grafana-server
  mem_limit: 256M
  ports:
  - 3000:3000

prometheus-server:
  build: ./docker/prometheus
  container_name: prometheus-server
  mem_limit: 256M
  ports:
  - 9091:9090
```

## Dockerfile Prometheus

Prometheus est un outil de supervision chargé de collecter et de stocker les métriques collectées (dans notre étude de cas depuis des actuators Spring Boot). Les métriques sont stockées dans une [base de données de type Time Series](https://prometheus.io/docs/prometheus/latest/storage/). Prometheus propose bien évidemment une [API HTTP](https://prometheus.io/docs/prometheus/latest/querying/api/) pour consulter ces métriques et créer de jolis tableaux de bord dans des outils comme [Grafana](http://www.grafana.org/) ou [WaveFront](https://www.wavefront.com/).

Mise en place par Kevin Crawley, l’image Docker de Prometheus [docker/prometheus/Dockerfile](https://github.com/spring-petclinic/spring-petclinic-microservices/blob/master/docker/prometheus/Dockerfile) personnalise [l’image officielle de Prometheus 2.4.2](https://hub.docker.com/r/prom/prometheus) en ajoutant le fichier [prometheus.yml](https://github.com/spring-petclinic/spring-petclinic-microservices/blob/master/docker/prometheus/prometheus.yml) dans le répertoire de configuration /etc/prometheus :

```dockerfile
FROM prom/prometheus:v2.4.2
ADD prometheus.yml /etc/prometheus/
```

Le fichier de configuration [prometheus.yml](https://github.com/spring-petclinic/spring-petclinic-microservices/blob/master/docker/prometheus/prometheus.yml) précise quels sont les actuators Spring Boot que Prometheus doit interroger périodiquement pour récupérer et historiser les métriques. Chose amusante : Prometheus se monitore lui-même.

```yaml
# my global config
global:
  scrape_interval:     15s # Set the scrape interval to every 15 seconds. Default is every 1 minute.
  evaluation_interval: 15s # Evaluate rules every 15 seconds. The default is every 1 minute.
  # scrape_timeout is set to the global default (10s).

# A scrape configuration containing exactly one endpoint to scrape:
# Here it's Prometheus itself.
scrape_configs:
- job_name: prometheus
  static_configs:
  - targets: ['localhost:9090']

- job_name: api-gateway
  metrics_path: /actuator/prometheus
  static_configs:
  - targets: ['api-gateway:8080']

- job_name: customers-service
  metrics_path: /actuator/prometheus
  static_configs:
  - targets: ['customers-service:8081']

- job_name: visits-service
  metrics_path: /actuator/prometheus
  static_configs:
  - targets: ['visits-service:8082']

- job_name: vets-service
  metrics_path: /actuator/prometheus
  static_configs:
  - targets: ['vets-service:8083']
```

Les métriques préfixées par _petclinic\__ sont accessibles depuis l’interface web de Prometheus [http://localhost:9091/](http://localhost:9091/) :

![Prometheus UI](wp-content/uploads/2019/03/2019-03-Dashboard-Grafana-dockerisé-prometheus.png)

Dans l’exemple ci-dessus, la métrique
petclinic\_pet\_seconds\_count comptabilise le nombre d’appels différents au contrôleur
REST [PetResource](https://github.com/spring-petclinic/spring-petclinic-microservices/blob/master/spring-petclinic-customers-service/src/main/java/org/springframework/samples/petclinic/customers/web/PetResource.java) :

- Le GET sur /petTypes pour lister les types d’animaux
- Le POST sur /owners/{ownerId}/pets pour ajouter
  un animal à un propriétaire

## Dockerfile Grafana

Pratique, l’IHM de consultation des métriques proposée par Prometheus ne permet pas de construire de jolis tableaux de bord. C’est pourquoi [les auteurs de Prometheus préconisent l’utilisation de Grafana](https://prometheus.io/docs/visualization/grafana/).

Le [Dockerfile](https://github.com/spring-petclinic/spring-petclinic-microservices/blob/master/docker/grafana/Dockerfile) de Grafana repose sur l’image officielle 5.2.4 de Grafana, y ajoute 2 répertoires /provisioning et /dashboard et le fichier de configuration grafana.ini :

```dockerfile
FROM grafana/grafana:5.2.4
ADD ./provisioning /etc/grafana/provisioning
ADD ./grafana.ini /etc/grafana/grafana.ini
ADD ./dashboards /var/lib/grafana/dashboards
```

L’image Grafana est livrée avec un fichier grafana.ini dont toutes les options sont commentées avec les valeurs par défaut. Pour le personnaliser, je me suis référé à la [documentation](http://docs.grafana.org/installation/configuration/) :

1. Spécifier le répertoire contenant les fichiers permettant de pré-configurer Grafana avec la source de données Prometheus et le dashboard pour Petclinic
1. Désactiver l’authentification et permettre ainsi à un utilisateur non authentifié de consulter le dashboard _Spring Petclinic Metrics_

Au final, voici à quoi ressemble le fichier de configuration [grafana.ini](https://github.com/spring-petclinic/spring-petclinic-microservices/blob/master/docker/grafana/grafana.ini) :

```ini
##################### Spring Petclinic Microservices Grafana Configuration #####################

#################################### Paths ####################################
[paths]
# folder that contains provisioning config files that grafana will apply on startup and while running.
provisioning = /etc/grafana/provisioning

#################################### Anonymous Auth ##########################
# Anonymous authentication has been enabled in the Petclinic sample with Admin role
# Do not do that in Production environment
[auth.anonymous]
# enable anonymous access
enabled = true

# specify organization name that should be used for unauthenticated users
org_name = Main Org.

# specify role for unauthenticated users
org_role = Admin
```

Le fichier de pré-configuration de la source de données
Prometheus [provisionning/datasources/all.yml](https://github.com/spring-petclinic/spring-petclinic-microservices/blob/master/docker/grafana/provisioning/datasources/all.yml)
référence l’URL de Prometheus avec son port interne à Docker :

```yaml
apiVersion: 1

datasources:
- name: Prometheus
  type: prometheus
  access: proxy
  org_id: 1
  url: http://prometheus-server:9090
  is_default: true
  version: 1
  editable: true
```

Le fichier de pré-configuration des dashboards [provisioning/dashboards/all.yml](https://github.com/spring-petclinic/spring-petclinic-microservices/blob/master/docker/grafana/provisioning/dashboards/all.yml) référence le répertoire **/** var **/** lib **/** grafana **/** dashboards dans lequel a été copié le fichier de configuration du dashboard Spring Petclinic Metrics [grafana-petclinic-dashboard.json](https://github.com/spring-petclinic/spring-petclinic-microservices/blob/master/docker/grafana/dashboards/grafana-petclinic-dashboard.json) (cf. Dockerfile) :

```yaml
apiVersion: 1

providers:
- name: 'default'
  orgId: 1
  folder: ''
  type: file
  disableDeletion: false
  updateIntervalSeconds: 10
  options:
    path: /var/lib/grafana/dashboards
```

Le fichier de configuration du dashboard _Spring Petclinic Metrics_ [grafana-petclinic-dashboard.json](https://github.com/spring-petclinic/spring-petclinic-microservices/blob/master/docker/grafana/dashboards/grafana-petclinic-dashboard.json) s’appuie à la fois sur les métriques personnalisées préfixées par _petclinic\__ et sur les métriques générées nativement par Spring Boot.

Extrait d’utilisation de la métrique **http\_server\_requests\_seconds\_sum** :

```json
"expr": "sum(rate(http_server_requests_seconds_sum{status!~\"5..\"}[1m]))/sum(rate(http_server_requests_seconds_count{ status!~\"5..\"}[1m]))",
"format": "time_series",
"intervalFactor": 1,
"legendFormat": "HTTP - AVG",
"refId": "A"
```

Extrait d’utilisation de la métrique **petclinic\_owner\_seconds\_count** :

```json
"expr": "sum(petclinic_owner_seconds_count{method=\"POST\", status=\"201\"})",
"format": "time_series",
"instant": false,
"intervalFactor": 1,
"legendFormat": "owner create",
"refId": "A"
```

## Conclusion

Cet article aura montré comment construire une image docker de Grafana pour vos démos.

Au démarrage de Grafana, la source de données vers Prometheus est pré-configurée. Le tableau de bord _Spring Petclinic Metrics_ utilise cette source de données pour récupérer les métriques Spring Boot et Petclinic historisées par Prometheus.  
L’accès au tableau de bord est public. L’URL est connue : [http://localhost:3000/d/69JXeR0iw/spring-petclinic-metrics](http://localhost:3000/d/69JXeR0iw/spring-petclinic-metrics.)

Les instructions de démarrage des images Docker peuvent être retrouvées dans le [README.md](https://github.com/spring-petclinic/spring-petclinic-microservices/blob/master/README.md) du repo GitHub [spring-petclinic/spring-petclinic-microservices](https://github.com/spring-petclinic/spring-petclinic-microservices).

Ressources :

- [Micrometer concepts](https://micrometer.io/docs/concepts) (Micrometer website)
- [Grafana support for Prometheus](https://prometheus.io/docs/visualization/grafana/) (official Prometheus documentation)
- [Découverte de l’outil de supervision Prometheus](https://linuxfr.org/news/decouverte-de-l-outil-de-supervision-prometheus#d%C3%A9couverte-de-prometheus-principe-de-fonctionnement) (Linuxfr.org)
- [Monitoring using Spring Boot 2, Prometheus and Grafana](https://dzone.com/articles/monitoring-using-spring-boot-2-prometheus-and-graf) (DZone)
