---
_edit_last: "1"
_monsterinsights_sitenote_active: ""
_monsterinsights_skip_tracking: ""
_wp_old_slug: optimiez-vos-applications-spring-boot-avec-cds-et-le-projet-leyden
author: admin
categories:
  - conférence
  - spring
date: "2025-04-21T12:04:33+00:00"
footnotes: ""
guid: https://javaetmoi.com/?p=2482
parent_post_id: null
post_id: "2482"
post_views_count: "1455"
summary: "Conférence : [Devoxx France 2025](https://www.devoxx.fr/){{ double-space-with-newline }}Date : 17 avril 2025{{ double-space-with-newline }}Speaker : [Sébastien Deleuze](https://seb.deleuze.fr/) (Broadcom){{ double-space-with-newline }}Format : Conférence (45 mn) / [Replay Youtube](https://www.youtube.com/watch?v=4EAxhhSWgw4)\n\nSébastien est Core Commiter sur [Spring Framework](https://spring.io/projects/spring-framework). Il intervient également sur des sujets transverses au portfolio Spring : support de Kotlin, null-safety (avec [JSpecify](https://jspecify.dev/)) et les sujets d’optimisation. Dans ce talk, il a pour ambition de nous montrer **comment améliorer l’efficacité de 80% des applications Spring**, que ce soit de nouvelles applications ou des applications Legacy.\n\n \n\nLes raisons d’améliorer l’efficacité de nos applications sont multiples :\n\n- **Baisser le cout** de run des applications\n- **Développement durable** pour diminuer la consommation d’énergie, de mémoire et de CPU\n- **Optimiser** les applications pour les **containers** (sur le Cloud ou OnPremise)\n\nPour arriver à nos fins, Sébastien nous propose 3 technologies :\n\n1. **CDS** : techno relativement vieille mais qui s’est améliorée au fil des versions de Java\n2. **AOT cache** : Java 24 permet d’utiliser l’AOT cache qui est une version améliorée CDS. Sébastien prédit l’exploision de AOT Cache avec la LTS Java 25\n3. **AOT cache with profiling** : technologie expérimentale et prometeuse"
tags:
  - devoxx
  - spring-boot
  - spring-framework
title: Optimisez vos applications Spring Boot avec CDS et le projet Leyden
url: /2025/04/optimisez-vos-applications-spring-boot-avec-cds-et-le-projet-leyden/

---
Conférence : [Devoxx France 2025](https://www.devoxx.fr/)  
Date : 17 avril 2025  
Speaker : [Sébastien Deleuze](https://seb.deleuze.fr/) (Broadcom)  
Format : Conférence (45 mn) / [Replay Youtube](https://www.youtube.com/watch?v=4EAxhhSWgw4)

Sébastien est Core Commiter sur [Spring Framework](https://spring.io/projects/spring-framework). Il intervient également sur des sujets transverses au portfolio Spring : support de Kotlin, null-safety (avec [JSpecify](https://jspecify.dev/)) et les sujets d’optimisation. Dans ce talk, il a pour ambition de nous montrer **comment améliorer l’efficacité de 80% des applications Spring**, que ce soit de nouvelles applications ou des applications Legacy.

{{< figure src="/wp-content/uploads/2025/04/word-image-2482-1.jpeg" alt="Sébastien Deleuze at Devoxx France 2025" caption="Sébastien Deleuze at Devoxx France 2025" >}}

Les raisons d’améliorer l’efficacité de nos applications sont multiples :

- **Baisser le cout** de run des applications
- **Développement durable** pour diminuer la consommation d’énergie, de mémoire et de CPU
- **Optimiser** les applications pour les **containers** (sur le Cloud ou OnPremise)

Pour arriver à nos fins, Sébastien nous propose 3 technologies :

1. **CDS** : techno relativement vieille mais qui s’est améliorée au fil des versions de Java
1. **AOT cache** : Java 24 permet d’utiliser l’AOT cache qui est une version améliorée CDS. Sébastien prédit l’exploision de AOT Cache avec la LTS Java 25
1. **AOT cache with profiling** : technologie expérimentale et prometeuse

Ces 3 technologies nécessitent un **training run**. Cette « exécution d’entrainement de l’application » consiste à lancer l’application pour charger les classes et créer un cache utilisé par la suite pour les déploiements en production. Le gain est triple :

- **Temps de démarrage** réduit
- **Empreinte mémoire** réduite
- **Warmup** de la JVM plus rapide

{{< figure src="/wp-content/uploads/2025/04/word-image-2482-2.png" alt="Training run workflow" caption="Training run workflow" >}}

## 1\. Class Data Sharing (CDS)

Disponible depuis **Java 9**(2017), **CDS** a continué à évoluer au fil des versions de Java.

Par facilité (notamment pour la fonctionnalité d’extraction), un prérequis conseillé par Sébastien consiste à utiliser **Java 17** et **Spring Boot 3.3** et +.

Pour utiliser la fonctionnalité [CDS](https://docs.spring.io/spring-framework/reference/integration/cds.html), une **archive** CDS ( **format .jsa**) doit être créée pour le classpath de l'application. Spring Framework fournit un mécanisme facilitant la création de cette archive. Une fois l'archive disponible, on peut l'utiliser via un flag de la JVM.

La création de l’archive CDS nécessite 2 paramètres de JVM :

- **-Dspring.context.exit=onRefresh** : démarrage les beans singletons Spring non lazy puis arrête l’application.
- **-XX:ArchiveClassesAtExit=spring-petclinic.jsa** : création de l’archive CDS lorsque la JVM s’arrête.

{{< figure src="/wp-content/uploads/2025/04/word-image-2482-3.png" alt="java -Dspring.context.exit=onRefresh" caption="java -Dspring.context.exit=onRefresh" >}}

Les **plugins Maven** et **Gradle** de **Spring Boot** permettent de créer un **JAR auto-exécutable**. Disposer d’une seul JAR est bien pratique pour le déploiement et le téléchargement d’une application depuis le repository Maven d’entreprise, mais **pas efficiente** avec CDS qui ne supporte pas les JAR imbriqués. La version 3.3 de Spring Boot a facilité le [support de CDS](https://github.com/spring-projects/spring-boot/wiki/Spring-Boot-3.3-Release-Notes#cds-support) en ajoutant une **fonctionnalité d’auto-extraction du JAR** via le paramètre **-Djarmode=tools**. Son utilisation est illustrée par la commande suivante :

```
java -Djarmode=tools -jar spring-petclinic.jar extract
```

{{< figure src="/wp-content/uploads/2025/04/cds-file-layout.png" alt="CDS file layout" caption="CDS file layout" >}}

Sébastien fait une démonstration à l’aide de l’application [Spring Petclinic](https://github.com/spring-projects/spring-petclinic).

Commande permettant d’utiliser l’archive CDS au démarrage de l’application :

```
java -XX :SharedArchiveFile=spring-petclinic.jsa – jar spring-petclinic.jar
```

Le **gain au démarrage** est de **19%.** A noter que l’utilisation de CDS peut engendrer des effets de bord si l’on ne suit pas les **bonnes pratiques** suivantes :

- Utiliser idéalement la **même JVM** pour la capture du CDS et le run de l’application
- Spécifier le **classpath** avec la **liste complète des JAR** et **ne pas utiliser de wildcard \***
- Le **timestamp des JAR** doit être **préservé**
- Les éventuels JAR additionnels doivent être ajoutés à la fin du classpath.

L’étape de démarrage nécessaire à l’enregistrement de l’archive CDS est appelée le **training run**. Cette étape peut être intégrée dans le pipeline CI/CD de build de l’application Spring. Spring utilise une base de données H2 en mémoire. Une application d’entreprise se connectera à un PosgreSQL ou un MongoDB. Le paramétrage Spring diffère en fonction des dépendances externes de l’application. Sébastien nous recommande de consulter le repository [spring-lifecycle-smoke-tests](https://github.com/spring-projects/spring-lifecycle-smoke-tests/tree/main#training-run-configuration) donnant différents exemples de configuration pour Spring Data, Spring Batch, Spring Coud, Kafka, Spring Security …

{{< figure src="/wp-content/uploads/2025/04/word-image-2482-5.png" alt="Training run configuration for your database" caption="Training run configuration for your database" >}}

Par exemple, pour éviter qu’une application Spring Data JPA ne fasse appel à la base de données, il est possible de **désactiver la lecture des méta-données par Hibernate**. Ne pouvant plus déterminer automatiquement le dialect, il est alors nécessaire de lui spécifier.

```
# Specify explicitly the dialect (here for PostgreSQL, adapt for your database)
spring.jpa.database-platform=org.hibernate.dialect.PostgreSQLDialect

# Disable Hibernate usage of JDBC metadata
spring.jpa.properties.hibernate.boot.allow_jdbc_metadata_access=false

# Database initialization should typically be performed outside of Spring lifecycle
spring.jpa.hibernate.ddl-auto=none
spring.sql.init.mode=never
```

Le [support de Buildpack](https://docs.spring.io/spring-boot/maven-plugin/build-image.html#build-image) par les plugins Maven et Gradle de Spring Boo transforme une application Spring Boot en une image OCI (Docker). Commandes :

```
mvn spring-boot:build-image
gradle bootBuildImlage
```

{{< figure src="/wp-content/uploads/2025/04/word-image-2482-6.png" alt="CDS support in Buildpacks" caption="CDS support in Buildpacks" >}}

Le support de CDS est prévu dans Buildpacks via l’activation du **flag** [**BP\_JVM\_CDS\_ENABLED**](https://github.com/paketo-buildpacks/spring-boot). Exemple de configuration Maven :

```
<plugin>
	<groupId>org.springframework.boot</groupId>
	<artifactId>spring-boot-maven-plugin</artifactId>
	<configuration>
		<image>
			<env>
				<BP_JVM_CDS_ENABLED>true</BP_JVM_CDS_ENABLED>
			</env>
		</image>
	</configuration>
</plugin>
```

**Buildpack** effectue le **training run** et **ajoute l’archive jsa dans le container**.

Pour un effort mesuré, le **temps de démarrage de Spring Petclinic** est **réduit de 3 secondes** à 1,8 secondes.

## 2\. AOT Cache

Successeur de CDS, **AOT Cache** (Ahead-Of-Time Cache) est une fonctionnalité de la JVM intégrée à **Java 24** qui permet d’ **améliorer l’efficience de nos applications Java**. Permettant de diminuer les temps de démarrage, [**Spring AOT**](https://docs.spring.io/spring-framework/reference/core/aot.html) est une fonctionnalité Spring obligatoire pour les images natives mais optionnelle sur la JVM. Sébastien perçoit une synergie entre AOT Cache et Spring AOT.

L’utilisation Spring AOT impose certaines contraintes comme la pré-configuration des **profiles Spring**. Le repo Github [sdeuleuze/demo-profile-aot](https://github.com/sdeleuze/demo-profile-aot) montre comment activer les profils Spring dans un build Maven et Gradle.

Pensée dans le cadre du **projet Leyden**, La [JEP 483 Ahead-of-Time Class Loading & Linking](https://openjdk.org/jeps/483) est disponible dans Java 24 et des améliorations prévues dans les versions suivantes de Java. L’utiliser est un bon investissement.

{{< figure src="/wp-content/uploads/2025/04/word-image-2482-7.png" alt="AOT Cache and Spring AOT are different but they combine well" caption="AOT Cache and Spring AOT are different but they combine well" >}}

La création du cache AOT nécessite 2 étapes :

La **1ière étape** consiste à générer le **fichier .aotconf** à l’aide de l’option **-XX:AOTMode=record** et la ligne de commande suivante :

```
java -XX:AOTMode=record -XX:AOTConfiguration=spring-petclinic.aotconf \
-jar spring-petclinic.jar
```

Au préalable, comme avec CDS, le JAR auto-exécutable aura été extrait à l’aide de **-Djarmode=tools**.

La 2 **ième étape** consiste à générer un **fichier .aot** avec l’option **-XX:AOTMode=create** et la ligne de commande suivante :

```
java -XX:AOTMode=create -XX:AOTConfiguration=spring-petclinic.aotconf -XX:AOTCache=spring-petclinic.aot -jar spring-petclinic.jar
```

Le t **emps de démarrage de Spring Petclinic** **descend à 1,3 secondes** :

{{< figure src="/wp-content/uploads/2025/04/word-image-2482-8.png" alt="Spring Petclinic startup time (seconds)" caption="Spring Petclinic startup time (seconds)" >}}

## 3\. AOT Cache with code compilation and Spring AOT

Sébastien rappelle que ce n’est que le début de l’histoire et que ces temps de démarrage à l’aide d’AOT Cache ne pourront que s’améliorer dans le futur. En effet, le projet Leyden prévoit de nouvelles améliorations, donc les 3 JEPs en draft :

1. [**Ahead-of-Time Method Profiling**](Ahead-of-Time%20Methode%20Profiling): amelioration du temps de chauffe
1. [**Ahead-of-time Command Line Ergonomics**](https://openjdk.org/jeps/8350022) : une seule étape au lieu de 2 étapes pour créer les fichiers .aotconf et .aot
1. [**Ahead-of-time Code Compilation**](https://openjdk.org/jeps/8335368) : récupération du code natif du JIT pour le réutiliser en prod

Sébastien nous fait une démo live à partir d’une **version du JDK compilée en local avec les dernières fonctionnalités du projet Leyden**. Cette fois-ci, le workflow va être un peu différent : on ne fait pas de stop après le démarrage. On laisse tourner l’application. Sébastien utilise l’outil [**oha**](https://github.com/hatoo/oha) pour chauffer la JVM (faire le warmup). Il mesure des améliorations très significatives alors même que techno en work-in-progress. Jugez par vous-même :

{{< figure src="/wp-content/uploads/2025/04/word-image-2482-9.png" alt="Spring Petclinic startup time (secondes)" caption="Spring Petclinic startup time (secondes)" >}}

{{< figure src="/wp-content/uploads/2025/04/word-image-2482-10.png" alt="Warmup with and without AOT cache" caption="Warmup with and without AOT cache" >}}

- Courbe bleue : JVM classique qui prend son temps pour le warmup
- Courbe rouge : AOT profiling. Warmup assez rapide.
- Courbe jaune : warmup passé de 30 à 7 secondes. Fonctionne sur des applications Legacy

## Récapitulatif

Le tableau récapitulatif ci-dessous compare 3 technologies d’optimisation d’une application Java :

{{< figure src="/wp-content/uploads/2025/04/word-image-2482-11.png" alt="Comparing GraalVM, Project CRaC and AOT cache" caption="Comparing GraalVM, Project CRaC and AOT cache" >}}

1. [**GraalVM**](https://www.graalvm.org/): la version gratuite de GraalVM vient avec le [Garbage Collector serial](https://www.graalvm.org/latest/reference-manual/native-image/optimizations-and-performance/MemoryManagement/) adapté pour les applications ayant une faible empreinte mémoire et une petite taille du de Heap. Le GC G1 n’est disponible que dans la version commerciale Oracle de GraalVM. Avantage : conso mémoire réduite au max. Pas fait pour des applications qu’on déploie / construit plusieurs fois par jour. Dépend de la taille de l’appli : ok pour un microservice mais pas un monolith. Spring fait le travail pour préconfigurer GraalVM. Mais quid des autres librairies qui ne supporte pas GraalVM et pour lesquels les développeurs doivent ajouter des méta-données. Sébastien considère que GraalVM est une niche pour 5 à 10% des applications Spring. Cela dit, des travaux sont en cours pour améliorer le support dans Spring.
1. **JVM with** [**Project CRaC**](https://docs.azul.com/core/crac/crac-introduction): Sébastien est assez sévère sur cette technologie qui comporte 2 énorme défauts : Linux uniquement mais surtout à cause du cycle de vie nécessitant de restaurer l’application (handles filesystems, sockets réseaux …). Quid du support des autres librairies ? L’API de ces librairies peut bloquer. Plus encore : l’image snapshot de la JVM contient les credentials. Aussi, Sébastien de recommande pas CRaC pour la production. La techno a des limites malgré l’effort de l’équipe Spring.
1. **JVM with AOT cache** : utilisable sur un grand nombre de projets legacy. Temps de démarrages est réduit de 2 à 4 fois. Les effets de bord sont mesurés. La CI doit être adaptée pour lancer le warmup.

Le projet Leyden et la JVM continue à évoluer. Preuve en est la Pull Request [#44](https://github.com/openjdk/leyden/pull/44) datant de février 2025 du projet Leyden : **8350488: \[leyden\] Experimental AOT-only mode**

D’autres améliorations concernant les applications Legacy seront annoncées à la [conférence Spring IO](https://2025.springio.net/) qui aura lieu du 21 au 23 mai 2025 à Barcelone.

Enfin, pour ses benchmarks, Sébastien passe une annonce : il recherche de plus grosses applications Open Source basées sur Spring Boot et plus réalistes que l'application démo Petclinic.

Si vous voulez creuser le sujet, je vous recommande la lecture de l’article intitulé [Spring Boot CDS support and Project Leyden anticipation](https://spring.io/blog/2024/08/29/spring-boot-cds-support-and-project-leyden-anticipation) qu’a publié Sébastien le 29 aout 2024.
