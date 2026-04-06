---
_edit_last: "1"
author: admin
categories:
  - maven
date: "2016-11-08T16:22:45+00:00"
guid: http://javaetmoi.com/?p=1651
parent_post_id: null
post_id: "1651"
post_views_count: "6731"
summary: |-
  ![docker-logo](http://javaetmoi.com/wp-content/uploads/2016/11/docker-logo-150x150.png)Par le passé, j’ai publié 2 images Docker sur le registre **Docker Hub**, l’équivalent du Maven Central Repository pour Docker : un [client MySQL](https://hub.docker.com/r/arey/mysql-client/) et [une base PostgreSQL MusicBrainz](https://hub.docker.com/r/arey/musicbrainz-database/). Ces images étaient construites puis publiées automatiquement à partir d’un dépôt GitHub contenant un Dockerfile et, éventuellement, un script Shell.

  Plus récemment, j’ai souhaité mettre à disposition une **image Docker de l’** [**application Spring Petclinic basée sur Angular 1 et Spring Boot.**](https://github.com/spring-petclinic/spring-petclinic-angular1) Ce billet explique :

  1. Comment l’image Docker a été construire
  2. Et comment l’utiliser pour tester Petclinic
tags:
  - docker
  - maven
  - spring-boot
title: Image Docker pour Spring Boot Petclinic
url: /2016/11/image-docker-pour-spring-boot-petclinic/

---
![docker-logo](/wp-content/uploads/2016/11/docker-logo.png)Par le passé, j’ai publié 2 images Docker sur le registre **Docker Hub**, l’équivalent du Maven Central Repository pour Docker : un [client MySQL](https://hub.docker.com/r/arey/mysql-client/) et [une base PostgreSQL MusicBrainz](https://hub.docker.com/r/arey/musicbrainz-database/). Ces images étaient construites puis publiées automatiquement à partir d’un dépôt GitHub contenant un Dockerfile et, éventuellement, un script Shell.

Plus récemment, j’ai souhaité mettre à disposition une **image Docker de l’** [**application Spring Petclinic basée sur Angular 1 et Spring Boot.**](https://github.com/spring-petclinic/spring-petclinic-angular1) Ce billet explique :

1. Comment l’image Docker a été construire
1. Et comment l’utiliser pour tester Petclinic

## Automatisation de la construction

Pour utiliser le **mécanisme de construction automatique** proposé par Docker Hub, une 1ière solution aurait consisté à télécharger le JAR de Petclinic depuis un repo Maven public. Or, ce n’est pas (encore ?) le cas.
Une 2nde solution aurait été de faire construire le JAR par Docker. L’image aurait nécessité Git et Maven. Afin de garder une taille d’image raisonnable, le repo Maven local et le repo Git auraient dû être effacé après construction du JAR. Ce n’était pas la solution la plus optimale.

La solution que j’ai finalement retenue n’est pas basée sur le mécanisme proposé par Docker Hub mais sur l’utilisation du **plugin pour Maven** [**docker-maven-plugin**](https://github.com/spotify/docker-maven-plugin) développé par l’équipe de **Spotify**.

## Configuration du docker-maven-plugin

Disponible sur la plateforme spring.io, le guide [Starting Guide Spring Boot With Docker](https://spring.io/guides/gs/spring-boot-docker/) explique pas à pas comment créer une image Docker d’une application Spring Boot.

Sur Petclinic, la configuration du docker-maven-plugin a été adaptée afin de faciliter la publication de l’image sur Docker Hub.
Voici un extrait du [pom.xml](https://github.com/spring-projects/spring-petclinic/blob/angularjs/pom.xml) du module springboot-petclinic-server :

```xhtml
<plugin>
    <groupId>com.spotify</groupId>
    <artifactId>docker-maven-plugin</artifactId>
    <version>0.4.13</version>
    <configuration>
        <imageName>${docker.image.prefix}/springboot-petclinic</imageName>
        <dockerDirectory>src/main/docker</dockerDirectory>
        <resources>
            <resource>
                <targetPath>/</targetPath>
                <directory>${project.build.directory}</directory>
                <include>${project.build.finalName}.jar</include>
            </resource>
        </resources>
        <forceTags>true</forceTags>
        <imageTags>
            <imageTag>${project.version}</imageTag>
            <imageTag>latest</imageTag>
        </imageTags>
        <useConfigFile>true</useConfigFile>
    </configuration>
</plugin>
```

Le plugin est configuré pour utiliser la **version Maven** pour **tagger** l’image Docker.

La balise **useConfigFile** précise au plugin d’aller rechercher les paramètres d’authentification au registre Docker dans le fichier de configuration Docker. Sur mon mac, ce fichier de configuration **config.json** se situe dans le répertoire  ~/.docker :

```js
{
        "auths": {
                "https://index.docker.io/v1/": {
                        "auth": "xxxxxxxxxx=="
                }
        }
}
```

Enfin, La propriété **docker.image.** **prefix** pointe sur mon compte personnel Docker Hub :

```xhtml
<properties>
    <docker.image.prefix>arey</docker.image.prefix>
</properties>
```

## Dockerfile

Pour des images simples, le plugin **docker-maven-plugin permet de se passer complètement de Dockerfile** : image de base, nom de l’image et point d’entrée sont directement configurés dans le pom.xml. Charge au plugin de générer le Dockerfile.

Pour Petclinic, l’usage d’un Dockerfile été préféré.  Facultatives, quelques directives spécifiques ont été ajoutées. Par ailleurs, l’utilisation d’un Dockerfile présente l’avantage de pouvoir être utilisé en dehors de Maven. La propriété _dockerDirectory_ référence le répertoire contenant le Dockerfile.

Pour être opérationnelle, l’image Docker de SpringBoot Petclinic nécessite :

1. une **image Linux**,
1. une **JVM** Java 7 ou 8
1. et le **JAR** de **Spring Petclinic**.

L’ [image Docker basée sur OpenJDK](https://hub.docker.com/_/openjdk/) couvre les 2 premiers besoins. La version basée sur le projet [Alpine Linux](https://alpinelinux.org/) permet d’utiliser une image de base très réduite (environ 5 Mo).

Au final, voici le [Dockerfile](https://github.com/spring-petclinic/spring-petclinic-angular1/blob/master/springboot-petclinic-server/src/main/docker/Dockerfile) de SpringBoot Petclinic :

```sh
FROM openjdk:alpine
MAINTAINER Antoine Rey <antoine.rey@free.fr>
# Spring Boot application creates working directories for Tomcat by default
VOLUME /tmp
ADD petclinic.jar petclinic.jar
RUN sh -c 'touch /petclinic.jar'
# To reduce Tomcat startup time we added a system property pointing to "/dev/urandom" as a source of entropy.
ENTRYPOINT ["java","-Djava.security.egd=file:/dev/./urandom","-jar","/petclinic.jar"]
```

Pointue, l’utilisation du répertoire /tmp, du touch et du urandom sont détaillées dans le [Starting Guide Spring Boot With Docker](https://spring.io/guides/gs/spring-boot-docker/). Je vous laisse vous y référer.

## Construire l’image Docker

La construction de l’image Docker passer par **une unique commande Maven** :

```xhtml
mvn docker:build
```

Au préalable, il est nécessaire de **démarrer Docker**. Dans le cas contraire, vous obtiendrez un message d’erreur similaire :

```sh
[INFO] Building image arey/springboot-petclinic
nov. 04, 2016 8:47:21 AM org.apache.http.impl.execchain.RetryExec execute
INFOS: I/O exception (java.io.IOException) caught when processing request to {}->unix://localhost:80: No such file or directory
…
ERROR] Failed to execute goal com.spotify:docker-maven-plugin:0.4.13:build (default-cli) on project springboot-petclinic-server: Exception caught: java.util.concurrent.ExecutionException: com.spotify.docker.client.shaded.javax.ws.rs.ProcessingException: java.io.IOException: No such file or directory
```

Techniquement, le plugin maven dialogue avec Docker par l’intermédiaire d’un [client Java Docker](https://github.com/spotify/docker-client) également développé par Spotify. Les échanges se font en REST / JSON.

Une fois la commande mvn docker:build  exécutée, les étapes de construction de l’image apparaissent dans les logs Maven :

```sh
[INFO] --- docker-maven-plugin:0.4.13:build (default-cli) @ springboot-petclinic-server ---
[INFO] Copying /Users/arey/dev/github/spring-petclinic /springboot-petclinic-server/target/petclinic.jar -> /Users/arey/dev/github/spring-petclinic/springboot-petclinic-server/target/docker/petclinic.jar
[INFO] Copying src/main/docker/Dockerfile -> /Users/arey/dev/ github/spring-petclinic /springboot-petclinic-server/target/docker/Dockerfile
[INFO] Building image arey/springboot-petclinic
Step 1 : FROM openjdk:alpine
 ---> f1da3c7976d0
Step 2 : MAINTAINER Antoine Rey <antoine.rey@free.fr>
 ---> Using cache
 ---> 321262ba62a5
Step 3 : VOLUME /tmp
 ---> Using cache
 ---> 7de28ccfef3f
Step 4 : ADD petclinic.jar petclinic.jar
 ---> 2af817fea936
Removing intermediate container 939a70038030
Step 5 : RUN sh -c 'touch /petclinic.jar'
 ---> Running in e90cff88f24c
 ---> e95aaed6515b
Removing intermediate container e90cff88f24c
Step 6 : ENTRYPOINT java -Djava.security.egd=file:/dev/./urandom -jar /petclinic.jar
 ---> Running in 7d03e1941841
 ---> 3b9b33ffb62b
Removing intermediate container 7d03e1941841
Successfully built 3b9b33ffb62b
[INFO] Built arey/springboot-petclinic
[INFO] Tagging arey/springboot-petclinic with 1.4.1
[INFO] Tagging arey/springboot-petclinic with latest
```

L’ **image Docker arey/springboot-petclinic** est construite et est disponible localement.

Pour tester par vous-même la création de l’image Docker de Spring Boot Petclinic, exécuter les commandes suivantes :

```sh
git clone https://github.com/spring-projects/spring-petclinic
cd spring-petclinic
git checkout angularjs
mvn clean install
cd spring-petclinic-server
mvn docker:build
```

## Publier l’image Docker

Publier l’image Docker construite avec Maven dans le registre public Docker Hub est enfantin. Après avoir paramétré la propriété _docker.image.prefix_ du pom.xml et le fichier de configuration ~/.docker/config.json , exécuter la ligne de commande Maven suivante :

```sh
mvn docker:build -DpushImageTag
```

## Démarrer Spring Boot Petclinic

 **Démarrer l’image Docker** **arey/springboot-petclinic** disponible sur Docker Hub ou construite localement se fait en ligne de commande :

```sh
docker run -e "SPRING_PROFILES_ACTIVE=prod" -p 8080:8080 -t --name springboot-petclinic arey/springboot-petclinic
```

L’application web est alors disponible sur l’URL http://DOCKER\_HOST:8080/

Le profile Spring de prod permet d’activer la mise en cache et le versionning des ressources statiques (cf. [application-prod.properties](https://github.com/spring-petclinic/spring-petclinic-angular1/blob/master/springboot-petclinic-server/src/main/resources/application-prod.properties)).

Pour arrêter le conteneur, utiliser la commande :

```sh
docker stop springboot-petclinic
```

## Conclusion

Le packaging d’une application Spring Boot sous forme d’image Docker peut entièrement être automatisé avec Maven (mais également avec Gradle). Publier ensuite cette image sur Docker Hub et tout Internaute pourra tester votre application sans avoir à installer le moindre outil (mis à part Docker).

Concernant Petclinic, la prochaine étape pourrait consister à déployer cette image sur un Cloud public. A suivre ...

Ressources :

1. [Docker container for the Spring Boot Petclinic application](https://hub.docker.com/r/arey/springboot-petclinic/)
1. [Starting Guide Spring Boot With Docker](https://spring.io/guides/gs/spring-boot-docker/)
1. [Image Docker officielle pour Java basée sur OpenJDK](https://hub.docker.com/_/openjdk/)
1. [Documentation du plugin docker-maven-plugin](https://github.com/spotify/docker-maven-plugin)
1. [Version Angular JS](https://github.com/spring-petclinic/spring-petclinic-angular1) [de l’application SpringBoot Petclinic](https://github.com/spring-petclinic/spring-petclinic-angular1)
1. [Client Java pour Docker](https://github.com/spotify/docker-client)
