---
_edit_last: "1"
author: admin
categories:
  - retour-d'expérience
date: "2015-11-02T06:12:35+00:00"
thumbnail: /wp-content/uploads/2015/07/docker-logo.jpg
featureImage: /wp-content/uploads/2015/07/docker-logo.jpg
featureImageAlt: "docker-logo"
guid: http://javaetmoi.com/?p=1471
parent_post_id: null
post_id: "1471"
post_views_count: "4873"
summary: |-
  [![docker-logo](http://javaetmoi.com/wp-content/uploads/2015/07/docker-logo-300x265.jpg)](http://javaetmoi.com/wp-content/uploads/2015/07/docker-logo.jpg) Lorsqu’on développe dans son coin une démo basée sur une nouvelle techno, il est fréquent d’avoir besoin de données de tests. Soit on se les construit à la main, soit on en récupère sur Internet. Le mouvement [Open Data](https://fr.wikipedia.org/wiki/Open_data) et les API mises à disposition par les grands du Web permettent de récupérer des données en temps réel. Dans les conférences, nombre de démos live utilisent les API de Twitter ou de Github. Ces données sont généralement formatées en JSON. Une connexion réseau est alors nécessaire.

  Dans le cadre d’une série d’articles sur Elasticsearch et AngularJS, j’ai eu le besoin d’indexer des données de manière **offline**. Cherchant une **source de donnée musicale**, j’ai opté pour [**MusicBrainz**](https://musicbrainz.org/) qui, à l’instar d’IMDb pour le cinéma, est une plateforme ouverte collectant des méta-données sur les artistes, leurs albums et leurs chansons puis les mettant à disposition du publique. Cette plateforme est composée d’une base de données relationnelles et d’une interface web permettant d’effectuer des recherches, de consulter les données et de participer à l’enrichissement de la base. [Last.fm](http://blog.last.fm/2011/11/24/the-brainz-are-back-in-town), [The Guardian](http://www.theguardian.com/open-platform/blog/linked-data-open-platform) ou bien encore la [BBC](http://www.bbc.co.uk/music/brainz/) s’interfacent avec MusicBrainz.

  Dans l’article [Elastifiez la base MusicBrainz sur OpenShift](http://javaetmoi.com/2013/11/musicbrainz-elasticsearch-angularjs-openshift/), je proposais 2 méthodes pour installer la base de données : récupérer une VM ou un dump de la base PostgreSQL. Dans les 2 cas, la procédure d’installation demandait une intervention humaine.
  Ce billet vous en propose une 3ième : automatiser l’installation de base de données à l’aide de [**Docker**](https://www.docker.com/). Après **quelques lignes de commande** et un peu de **patience** le temps de l’import du dump PostgreSQL, vous pourrez vous connecter localement à la base musicale contenant des données à jour.

  ![docker-logo](/wp-content/uploads/2015/07/docker-logo.jpg)
tags:
  - docker
  - postresql
title: Docker file de la database MusicBrainz
url: /2015/11/docker-file-database-musicbrainz/

---
[![docker-logo](/wp-content/uploads/2015/07/docker-logo.jpg)](/wp-content/uploads/2015/07/docker-logo.jpg) Lorsqu’on développe dans son coin une démo basée sur une nouvelle techno, il est fréquent d’avoir besoin de données de tests. Soit on se les construit à la main, soit on en récupère sur Internet. Le mouvement [Open Data](https://fr.wikipedia.org/wiki/Open_data) et les API mises à disposition par les grands du Web permettent de récupérer des données en temps réel. Dans les conférences, nombre de démos live utilisent les API de Twitter ou de Github. Ces données sont généralement formatées en JSON. Une connexion réseau est alors nécessaire.

Dans le cadre d’une série d’articles sur Elasticsearch et AngularJS, j’ai eu le besoin d’indexer des données de manière **offline**. Cherchant une **source de donnée musicale**, j’ai opté pour [**MusicBrainz**](https://musicbrainz.org/) qui, à l’instar d’IMDb pour le cinéma, est une plateforme ouverte collectant des méta-données sur les artistes, leurs albums et leurs chansons puis les mettant à disposition du publique. Cette plateforme est composée d’une base de données relationnelles et d’une interface web permettant d’effectuer des recherches, de consulter les données et de participer à l’enrichissement de la base. [Last.fm](http://blog.last.fm/2011/11/24/the-brainz-are-back-in-town), [The Guardian](http://www.theguardian.com/open-platform/blog/linked-data-open-platform) ou bien encore la [BBC](http://www.bbc.co.uk/music/brainz/) s’interfacent avec MusicBrainz.

Dans l’article [Elastifiez la base MusicBrainz sur OpenShift](/2013/11/musicbrainz-elasticsearch-angularjs-openshift/), je proposais 2 méthodes pour installer la base de données : récupérer une VM ou un dump de la base PostgreSQL. Dans les 2 cas, la procédure d’installation demandait une intervention humaine.
Ce billet vous en propose une 3ième : automatiser l’installation de base de données à l’aide de [**Docker**](https://www.docker.com/). Après **quelques lignes de commande** et un peu de **patience** le temps de l’import du dump PostgreSQL, vous pourrez vous connecter localement à la base musicale contenant des données à jour.

## L’image arey/musicbrainz-database

Basée sur l’ [image officielle de postgres](https://hub.docker.com/_/postgres/), [**l’image Docker arey/musicbrainz-database**](https://registry.hub.docker.com/u/arey/musicbrainz-database/) installe la base de données PostgreSQL 9.4 ainsi que toutes les librairies nécessaires au fonctionnement de la base de données MusicBrainz (ex : postgresql-server-dev-9.4, postgresql-musicbrainz-unaccent).

Cette image vient avec le script shell [create-database.sh](https://github.com/arey/musicbrainz-database/blob/master/create-database.sh) utilisé pour créer la structure de données et importer le dump de la base de données MusicBrainz. Les étapes le décomposant sont les suivantes :

1. Crée le schéma musicbrainz
1. Crée les tables à partir des scripts DDL présent sur le GitHub de MusicBrainz
1. Télécharge le dump de la base de données
1. Importe le dump après l’avoir téléchargé par FTP
1. Ajoute les index et les clés primaires

Le [code source de l’image arey/musicbrainz est disponible sur GitHub](https://github.com/arey/musicbrainz-database).

## Lignes de commande

Deux lignes de commandes sont nécessaires pour obtenir une base de données alimentées et accessibles depuis n’importe quel client SQL :

```sh
docker run -t -d -p 5432:5432 --name musicbrainz-database -e POSTGRES_USER=musicbrainz -e POSTGRES_PASSWORD=musicbrainz arey/musicbrainz-database

docker run -it --link musicbrainz-database:postgresql -e POSTGRES_USER=musicbrainz -e POSTGRES_PASSWORD=musicbrainz --rm arey/musicbrainz-database /create-database.sh
```

Pour tester l’installation de la base, exécuter la requête SQL suivante comptant le nombre d’artistes référencés :

```sh
docker run -it --link musicbrainz-database:postgresql --rm arey/musicbrainz-database sh -c 'exec psql -h postgresql -d musicbrainz -U musicbrainz -a -c "SELECT COUNT(*) FROM artist"'
```

Lorsque le client _psql_ demande de saisir un mot de passe, sairi ‘musicbrainz’. Vous obtiendrez la sortie suivante :

```default
Password for user musicbrainz:
SELECT COUNT(*) FROM artist
 count
--------
 995899
(1 row)
```

Depuis une application Java, la chaine de connexion JDBC à utiliser est la suivante : jdbc:postgresql://localhost:5432/musicbrainz
Login et mot de passe sont identiques : musicbrainz / musicbrainz
Pour les utilisateurs Windows ou MacOSX utilisant boot2docker, il est nécessaire de remplacer _localhost_ par l’IP donnée par la commande _boot2docker ip_.

## Sous le capot

Avant de construite ma propre image Docker, j’ai étudié les images Docker existantes telles que [rickatnight11/docker\_musicbrainz](https://github.com/rickatnight11/docker_musicbrainz) et [jsturgis/musicbrainz-docker](https://github.com/jsturgis/musicbrainz-docker). Elles installent un serveur MusicBrainz complet avec sa partie front. Je souhaitais une image plus légère centrée sur la base PostgreSQL. Cela dit, je mentirais en disant que je ne m’en suis pas inspiré.
Vous trouverez ci-dessous le fichier Dockerfile et le script de création de la base.

**Dockerfile**

```default
FROM postgres:9.4

RUN apt-get update

RUN DEBIAN_FRONTEND=noninteractive apt-get -y -q install git-core build-essential libxml2-dev libpq-dev libexpat1-dev libdb-dev libicu-dev postgresql-server-dev-9.4 wget

RUN git clone https://github.com/metabrainz/postgresql-musicbrainz-unaccent.git && git clone https://github.com/metabrainz/postgresql-musicbrainz-collate.git

RUN cd postgresql-musicbrainz-unaccent && make && make install && cd ../postgresql-musicbrainz-collate && make && make install && cd ../

RUN echo "listen_addresses='*'" >> /var/lib/postgresql/data/postgresql.conf

ADD create-database.sh /create-database.sh
```

 **Script shell createdatabase.sh**

```sh
#!/bin/bash

cd /tmp

echo "Creating Musicbrainz database structure"

echo "postgresql:5432:musicbrainz:$POSTGRES_USER:$POSTGRES_PASSWORD"  > ~/.pgpass
chmod 0600 ~/.pgpass

psql -h postgresql -d musicbrainz -U $POSTGRES_USER -a -c "CREATE SCHEMA musicbrainz"

wget https://raw.githubusercontent.com/metabrainz/musicbrainz-server/master/admin/sql/Extensions.sql
psql -h postgresql -d musicbrainz -U $POSTGRES_USER -a -f Extensions.sql
rm Extensions.sql

wget https://raw.githubusercontent.com/metabrainz/musicbrainz-server/master/admin/sql/CreateTables.sql
psql -h postgresql -d musicbrainz -U $POSTGRES_USER -a -f CreateTables.sql
rm CreateTables.sql

echo "Downloading last Musicbrainz dump"
wget -nd -nH -P /tmp http://ftp.musicbrainz.org/pub/musicbrainz/data/fullexport/LATEST
LATEST="$(cat /tmp/LATEST)"
wget -nd -nH -P /tmp http://ftp.musicbrainz.org/pub/musicbrainz/data/fullexport/$LATEST/mbdump-derived.tar.bz2
wget -nd -nH -P /tmp http://ftp.musicbrainz.org/pub/musicbrainz/data/fullexport/$LATEST/mbdump.tar.bz2

echo "Uncompressing Musicbrainz dump"
tar xjf /tmp/mbdump-derived.tar.bz2
rm mbdump-derived.tar.bz2
tar xjf /tmp/mbdump.tar.bz2
rm mbdump.tar.bz2

for f in mbdump/*
do
 tablename="${f:7}"
 echo "Importing $tablename table"
 echo "psql -h postgresql -d musicbrainz -U $POSTGRES_USER -a -c COPY $tablename FROM '/tmp/$f'"
 chmod a+rX /tmp/$f
 psql -h postgresql -d musicbrainz -U $POSTGRES_USER -a -c "\COPY $tablename FROM '/tmp/$f'"
done

rm -rf mbdump

echo "Creating Indexes and Primary Keys"

wget https://raw.githubusercontent.com/metabrainz/musicbrainz-server/master/admin/sql/CreatePrimaryKeys.sql
psql -h postgresql -d musicbrainz -U $POSTGRES_USER -a -f CreatePrimaryKeys.sql
rm CreatePrimaryKeys.sql

wget https://raw.githubusercontent.com/metabrainz/musicbrainz-server/master/admin/sql/CreateIndexes.sql
psql -h postgresql -d musicbrainz -U $POSTGRES_USER -a -f CreateIndexes.sql
rm CreateIndexes.sql
```

## Conclusion

Le script shell de création de la base m’aura demandé plus d’efforts que le Dockerfile. Indépendant de tout script externe, il devrait être stable dans le temps. L’image devra par contre évoluer au fil du temps, par exemple lors de montée de version de PostgreSQL.

L’image [arey/musicbrainz-database](https://registry.hub.docker.com/u/arey/musicbrainz-database/) peut être utilisée avec **docker-compose.** C’est désormais le cas sur le projet [musicbrainz-elasticsearch](https://github.com/arey/musicbrainz-elasticsearch/tree/master/docker) qui l’utilise pour démarrer la base de données MusicBrainz et un cluster Elasticsearch.
