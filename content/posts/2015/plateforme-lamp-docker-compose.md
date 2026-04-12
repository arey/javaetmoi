---
_edit_last: "1"
author: admin
categories:
  - retour-d'expérience
date: "2015-07-15T05:31:19+00:00"
thumbnail: wp-content/uploads/2015/07/docker-logo.jpg
featureImage: wp-content/uploads/2015/07/docker-logo.jpg
featureImageAlt: "docker-logo"
guid: http://javaetmoi.com/?p=1429
parent_post_id: null
post_id: "1429"
post_views_count: "16261"
summary: |-
  [![docker-logo](http://javaetmoi.com/wp-content/uploads/2015/07/docker-logo-300x265.jpg)](http://javaetmoi.com/wp-content/uploads/2015/07/docker-logo.jpg)

  Afin de préparer la migration technique d’un site web, j’ai eu besoin de reconstruire un environnement à l’identique de la production.

  Hébergé sur un serveur Linux, ce site est propulsé par Apache 2.2, PHP 5.6 et MySQL 5.5.
  C’était l’occasion parfaite pour découvrir **Docker**. Une première étape consiste à décomposer cette plateforme LAMP en **conteneurs** Docker ayant chacun leur responsabilité. Voici les 3 conteneurs identifiés :

  1. **site**: conteneur Apache et PHP sur lequel les pages PHP du site sont déployées
  2. **database**: conteneur MySQL hébergeant la base de données utilisée par les pages PHP
  3. **phpmyadmin**: conteneur dédié à l’outil d’administration de base de données phpMyAdmin

  Pour orchestrer le démarrage des conteneurs, gérer leur configuration et définir leurs interactions, l’utilisation de l’outil [**Docker Compose**](https://docs.docker.com/compose/) paraissait évidente.

  Dans ce billet, vous trouverez le fichier docker-compose correspondant, un Dockerfile personnalisant l’image officielle php:5.6-apache, les lignes de commandes démarrant les conteneurs sous MacOSX et alimentant la base à partir d’un script SQL.

  ![docker-logo](wp-content/uploads/2015/07/docker-logo.jpg)
tags:
  - apache
  - docker
  - lamp
  - mysql
  - php
title: Plateforme LAMP avec Docker Compose
url: /2015/07/plateforme-lamp-docker-compose/

---
[![docker-logo](wp-content/uploads/2015/07/docker-logo.jpg)](wp-content/uploads/2015/07/docker-logo.jpg)

Afin de préparer la migration technique d’un site web, j’ai eu besoin de reconstruire un environnement à l’identique de la production.

Hébergé sur un serveur Linux, ce site est propulsé par Apache 2.2, PHP 5.6 et MySQL 5.5.
C’était l’occasion parfaite pour découvrir **Docker**. Une première étape consiste à décomposer cette plateforme LAMP en **conteneurs** Docker ayant chacun leur responsabilité. Voici les 3 conteneurs identifiés :

1. **site**: conteneur Apache et PHP sur lequel les pages PHP du site sont déployées
1. **database**: conteneur MySQL hébergeant la base de données utilisée par les pages PHP
1. **phpmyadmin**: conteneur dédié à l’outil d’administration de base de données phpMyAdmin

Pour orchestrer le démarrage des conteneurs, gérer leur configuration et définir leurs interactions, l’utilisation de l’outil [**Docker Compose**](https://docs.docker.com/compose/) paraissait évidente.

Dans ce billet, vous trouverez le fichier docker-compose correspondant, un Dockerfile personnalisant l’image officielle php:5.6-apache, les lignes de commandes démarrant les conteneurs sous MacOSX et alimentant la base à partir d’un script SQL.

## Configuration Docker Compose

Le fichier docker-compose.yml décrit en YAML les 3 conteneurs présentés en introduction :

```yaml
site:
  build: site
  ports :
   - "80:80"
  volumes:
   - /Users/arey/dev/mysite/www:/var/www/html/
  links:
   - database
phpmyadmin:
   image: corbinu/docker-phpmyadmin
   ports :
    - "8080:80"
   environment:
    - MYSQL_USERNAME=root
    - MYSQL_PASSWORD=password
   links:
    - database:mysql
database:
  image: mysql:5.5
  ports:
   - "3306:3306"
  environment:
     - MYSQL_ROOT_PASSWORD=password
     - MYSQL_DATABASE=mysite
     - MYSQL_USER=mysite
     - MYSQL_PASSWORD=password
```

Voici quelques explications :

- Le conteneur **site** est créé à partir d’un Dockerfile que nous étudierons par la suite. Le port 80 d’Apache est exposé à l’hôte sur le port 80. Le répertoire _/Users/arey/dev/mysite/_ www contenant les pages PHP est monté dans le répertoire _/var/www/html/_ correspondant au répertoire home d’Apache. Enfin, ce conteneur dépend du conteneur database.
- Le conteneur **database** utilise l’image officielle [**mysql** **:5.5**](https://registry.hub.docker.com/_/mysql/). Le port par défaut 3306 de MySQL est exposé aux autres conteneurs et à l’hôte. La base de données **mysite** est crée au démarrage du conteneur. Les credentials de l’administrateur et d’un utilisateur sont paramétrés.

- Le conteneur **phpmyadmin** utilise l’image [**corbinu/docker-phpmyadmin**](https://registry.hub.docker.com/u/corbinu/docker-phpmyadmin/dockerfile/). Il se connecte au conteneur database en utilisant les credential définis dans le conteneur **database**. L’IHM de phpMyAdmin est accessible depuis un navigateur sur le port 8080.

## Dockerfile

Créé dans le **sous-répertoire _site_**, le Dockerfile suivant permet de construire une image personnalisée Docker à partir de l’image officielle **php:5.6-apache**:

```yaml
FROM php:5.6-apache

# Install PDO MySQL driver
# See https://github.com/docker-library/php/issues/62
RUN docker-php-ext-install pdo mysql
RUN docker-php-ext-install pdo mysqli

# Workaround for write permission on write to MacOS X volumes
# See https://github.com/boot2docker/boot2docker/pull/534
RUN usermod -u 1000 www-data

# Enable Apache mod_rewrite
RUN a2enmod rewrite
```

Les commentaires sont suffisamment explicites.
Si besoin, la commande RUN a2emod permet d’activer d’autres modules Apache.

## Démarrer les conteneurs

Sur MacOSX, l’utilisation de Docker passe par la VM [Boot2Docker](http://boot2docker.io/). L’installation de [VirtualBox](https://www.virtualbox.org/) est un pré-requis à l’utilisation de boot2docker.

Le gestionnaire de package [Homebrew](http://brew.sh/) permet d’installer Docker et boot2docker en quelques lignes :

```sh
brew install boot2docker
brew install docker
```

La commande **boot2docker init** permet de télécharger et d’installer la VM _boot2docker-vm_.
Et les commandes ci-dessous permettent de démarrer la VM et d’obtenir son adresse IP.

```sh
boot2docker start
$(boot2docker shellinit 2> /dev/null)
boot2docker ip
```

Le téléchargement des images, la construction de l’image _site_ et le démarrage des 3 conteneurs ne demandent que 2 lignes de commande :

```sh
docker-compose build
docker-compose up
```

Une fois démarrés, phpMyAdmin est accessible depuis votre hôte sur l’adresse [http://192.168.59.104:8080/index.php](http://192.168.59.104:8080/index.php) (renseigner l’adresse IP obtenue précédemment)

## Chargement de la base de données

Le site web ne peut pas fonctionner avec une **base vide**. La dernière étape consiste donc à **charger la base MySQL à partir d’un export de la base de données de production**.
Une première solution est d’utiliser phpMyAdmin.
Une seconde solution consiste à installer un client MySQL.
Une 3ième est d’utiliser un conteneur docker doté d’un client MySQL :

```sh
docker run -v /Users/arey/dev/mysite/sql:/sql --link mysite_database_1:mysql -it arey/mysql-client -h mysql -ppassword -D mysite -e "source /sql/export.sql"
```

Voici quelques explications :

- Le répertoire _/Users/arey/dev/mysite/sql_ contient le script _sql_
- _mysite\_database\_1_ correspond au nom de l’image docker attribué par docker-compose
- L’image [arey/mysql-client](https://registry.hub.docker.com/u/arey/mysql-client/) est publiée sur Docker Hub. Je l’ai créé spécifiquement pour ce type de besoin. Son [code source](https://github.com/arey/mysql-client) est sur GitHub.

## Conclusion

En 2 fichiers textes et une dizaine de lignes de commandes, vous disposerez d’une plateforme LAMP opérationnelle. Cela s’avère très pratique pour tester des montées de version de base de données, de CMS ou bien encore de PHP. Elle peut également être utilisée lors de la phase de développement.

Une fois mon projet de migration terminé, j’ai archivé ces 2 fichiers dans un repo git privé sur BitBucket puis j’ai supprimé les images téléchargées, libérant ainsi autant d’espace sur mon SSD.

Références :

- [Conteneurisation d’un LAMP avec Docker](http://blog.lecacheur.com/2015/04/22/conteneurisation-dun-lamp-avec-docker/)
- [Documentation officielle de Docker Compose](https://docs.docker.com/compose/)
