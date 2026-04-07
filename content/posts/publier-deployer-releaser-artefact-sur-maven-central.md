---
_edit_last: "1"
author: admin
categories:
  - maven
date: "2014-09-08T04:30:59+00:00"
thumbnail: /wp-content/uploads/2014/09/2014-09-publier-sur-maven-central-javaetmoi-search.png
featureImage: /wp-content/uploads/2014/09/2014-09-publier-sur-maven-central-javaetmoi-search.png
featureImageAlt: "2014-09-publier-sur-maven-central-javaetmoi-search"
guid: http://javaetmoi.com/?p=1184
parent_post_id: null
post_id: "1184"
post_views_count: "8450"
summary: |-
  Lorsque vous rendez open-source un projet, même le plus modeste soit-il, quoi de plus naturel que de vouloir faciliter son utilisation par la communauté de développeurs intéressés ? Dans le monde Java, le dépôt de binaires Open Source le plus connu est le **Central Repository**, également connu sous le nom de [**Maven Central**](http://central.sonatype.org/). En effet, lors de la construction d’un projet Java, [Apache Maven](http://maven.apache.org/) essaie par défaut de localiser ses dépendances depuis Maven Central. D’autres outils de build comme Gradle et Ant/Ivy y font également référence. Géré par Sonatype et reposant sur Nexus, **Maven Central est accessible en écriture par les développeurs Open-Source en faisant la demande**. Ayant récemment publié des artefacts sur ce repo, ce billet présente les différentes étapes qui m’ont permis d’y arriver.

  [![2014-09-publier-sur-maven-central-javaetmoi-search](http://javaetmoi.com/wp-content/uploads/2014/09/2014-09-publier-sur-maven-central-javaetmoi-search-1024x510.png)](http://javaetmoi.com/wp-content/uploads/2014/09/2014-09-publier-sur-maven-central-javaetmoi-search.png)
tags:
  - maven
title: Publiez vos artefacts sur Maven Central
url: /2014/09/publier-deployer-releaser-artefact-sur-maven-central/

---
Lorsque vous rendez open-source un projet, même le plus modeste soit-il, quoi de plus naturel que de vouloir faciliter son utilisation par la communauté de développeurs intéressés ? Dans le monde Java, le dépôt de binaires Open Source le plus connu est le **Central Repository**, également connu sous le nom de [**Maven Central**](http://central.sonatype.org/). En effet, lors de la construction d’un projet Java, [Apache Maven](http://maven.apache.org/) essaie par défaut de localiser ses dépendances depuis Maven Central. D’autres outils de build comme Gradle et Ant/Ivy y font également référence. Géré par Sonatype et reposant sur Nexus, **Maven Central est accessible en écriture par les développeurs Open-Source en faisant la demande**. Ayant récemment publié des artefacts sur ce repo, ce billet présente les différentes étapes qui m’ont permis d’y arriver.

[![2014-09-publier-sur-maven-central-javaetmoi-search](/wp-content/uploads/2014/09/2014-09-publier-sur-maven-central-javaetmoi-search.png)](/wp-content/uploads/2014/09/2014-09-publier-sur-maven-central-javaetmoi-search.png)

## Les limites d’un repository personnel

Il y’a 2 ans, [j’expliquais comment monter sa propre usine de développement Java dans le Cloud à l’aide de GitHub et de Cloudbees](/2012/12/ma-petite-usine-logicielle-github-cloudbees/). Pour Repository Maven, j’utilisais le Webdav mis gracieusement à disposition par Cloudbees. L’inconvénient principal de cet hébergement est que les artefacts publiés sur ce repository ne sont pas nativement accessibles par Maven. Il est en effet nécessaire de configurer la balise _distributionManagement_ du _pom.xml_ nécessitant ces artefacts. En entreprise, lorsque les builds maven passent systématiquement par un proxy maven, cela se complique pour le développeur. Plusieurs choix s’offrent à lui :

1. Référencer le repository Cloudbees dans le proxy maven de son Entreprise
1. Déployer les artefacts maven dans le repository maven de son Entreprise
1. Copier/coller le code qui l’intéresse
1. Renoncer à l’utilisation du code convoité

Sans débat, **la disponibilité d’artefacts dans le repository Maven Central facilite leur adoption.** C’est un critère qui m'avait d'ailleurs [convaincu d'adopter DbSetup](/2013/09/dbsetup-spring-test-vs-dbunit/ "DbSetup, une alternative à DbUnit").

Autre argument et pas des moindres : contrairement à un repository personnel, **la pérennité du repository Maven Central est garantie**.

## Demander à l’accès au service OSSRH

Le [manuel utilisateur de maven](http://maven.apache.org/guides/mini/guide-central-repository-upload.html) explique les différentes solutions permettant de déployer un artefact dans Maven Central.
Le moyen le plus simple est de passer par l’intermédiaire du service [Open-Source Software Repository Hosting](https://oss.sonatype.org/) ( **OSSRH**) offert par Sonatype. **Ce service offre un espace de staging dans lequel des artefacts « releasés » peuvent être publiés avant d’être promus puis synchronisés vers Maven Central**.

Le **[guide du service OSSRH](http://central.sonatype.org/pages/ossrh-guide.html)** explique quelles sont les démarches nécessaires à l’obtention des habilitations permettant de publier un artefact dans le repository Nexus OSSRH.
L’accès au **[Jira de Sonatype](https://issues.sonatype.org/)** est un pré-requis. Il suffit de renseigner un [formulaire d’inscription](https://issues.sonatype.org/secure/Signup!default.jspa). Les login / mot de passe de ce Jira serviront à se connecter sur le [Nexus de Sonatype](https://oss.sonatype.org/) et à déployer les artefacts dans OSSRH.

L’accès au Jira permet également d’ [ouvrir un ticket Jira de demande de création d’un projet](https://issues.sonatype.org/secure/CreateIssue.jspa?issuetype=21&pid=10134). L’information principale à communiquer concerne le **groupId** maven des artefacts que vous souhaitez déployer. La demande est examinée par un employé de Sonatype . Pour des raisons de sécurité et de confiance, [le groupId est vérifié](http://central.sonatype.org/articles/2014/Feb/27/why-the-wait).

Dans la demande [OSSRH-11327](https://issues.sonatype.org/browse/OSSRH-11327), le groupId _com.javaetmoi_ m’a été accordé. Cela me permet de publier des artefacts avec des « sous » groupId comme _com.javaetmoi.core_.
Moins de 24h après, [Joel Orlina](http://blog.sonatype.com/author/jorlina/) avait traité ma demandé.

[![2014-09-publier-sur-maven-central-javaetmoi-jira](/wp-content/uploads/2014/09/2014-09-publier-sur-maven-central-javaetmoi-jira.png)](/wp-content/uploads/2014/09/2014-09-publier-sur-maven-central-javaetmoi-jira.png)

## Préparer sa signature PGP

Un pré-requis nécessaire à la publication d’un artefact dans Maven Central consiste à signer son artefact à l’aide du standard OpenPGP.
L’installation de GnuPG, la génération de clés privés / publiques et la diffusion de la clé publique sont décrits sur la page [Working with PGP signatures](http://central.sonatype.org/pages/working-with-pgp-signatures.html).
Les instructions sont claires et une installation sous Windows 7 ne m’a posé aucune difficulté.

Dans le settings.xml local à l'utilisateur, pense à indiquer le chemin complet du binaire _gpg2.exe_ :

```xhtml
<profiles>
  <profile>
    <id>ossrh</id>
    <activation>
      <activeByDefault>true</activeByDefault>
    </activation>
    <properties>
      <gpg.executable>C:/Software/Dev/GnuPG/gpg2.exe</gpg.executable>
      <gpg.passphrase>xxxxxx</gpg.passphrase>
    </properties>
  </profile
</profiles>
```

## Configuration maven

La dernière étape avant de pouvoir déployer les artefacts de son projet dans Maven Central, consiste à configurer le POM de votre projet (le POM parent pour un projet multi-modules). La page  [Apache Maven du Central Repository](http://central.sonatype.org/pages/apache-maven.html) explique pas à pas quels sont les **plugins maven à configurer** et les **coordonnées du repository à déclarer**.
Pour exemple, je vous invite à vous référer au [pom.xml du projet spring-batch-toolkit](https://github.com/arey/spring-batch-toolkit/blob/v0.1.x/pom.xml).

Ne pas oublier de déclarer le server _ossrh_ dans _le settings.xml_ local de l'utilisateur.

## Publication dans Maven Central

Déployer une version release de son projet dans Maven Central peut se faire de plusieurs manières :

1. [L’utilisation du Maven Release Plugin](http://central.sonatype.org/pages/apache-maven.html#performing-a-release-deployment-with-the-maven-release-plugin)
1. [La commande deploy de maven](http://central.sonatype.org/pages/apache-maven.html#performing-a-release-deployment)
1. [Une publication manuelle à l’aide du plugin maven nexus-staging](http://central.sonatype.org/pages/apache-maven.html#nexus-staging-maven-plugin-for-deployment-and-release)

La page [Apache Maven du Central Repository](http://central.sonatype.org/pages/apache-maven.html) explique les commandes maven à exécuter.

Pour ma part, j’ai souhaité publié dans Maven Central des artefacts que j’avais déjà releasé sur mon repo personnel Cloudbees.
J’ai créé une branche à partir du tag créé lors de la release maven. J’ai ensuite reconfiguré le pom.xml comme expliqué ci-dessus. La commande maven suivante a fait le reste :  mvn clean deploy -P release

Voici un exemple de sortie console que vous obtiendrez en cas de succès :

```batch
....
Uploading: https://oss.sonatype.org:443/service/local/staging/deployByRepositoryId/comjavaetmoi-1004/com/javaetmoi/core/javaetmoi-hibernate4-hydrate/2.0/javaetoi-hibernate4-hydrate-2.0-sources.jar.asc
Uploaded: https://oss.sonatype.org:443/service/local/staging/deployByRepositoryId/comjavaetmoi-1004/com/javaetmoi/core/javaetmoi-hibernate4-hydrate/2.0/javaetmi-hibernate4-hydrate-2.0-sources.jar.asc (499 B at 0.1 KB/sec)
[INFO]  * Upload of locally staged artifacts finished.
[INFO]  * Closing staging repository with ID "comjavaetmoi-1004".
Waiting for operation to complete.......
[INFO] Remote staged 1 repositories, finished with success.
[INFO] Remote staging repositories are being released...
Waiting for operation to complete........
[INFO] Remote staging repositories released.
[INFO] ------------------------------------------------------------------------
[INFO] BUILD SUCCESS
[INFO] ------------------------------------------------------------------------
[INFO] Total time: 1:47.675s
[INFO] Finished at: Thu Sep 04 20:41:33 CEST 2014
[INFO] Final Memory: 15M/247M
[INFO] ------------------------------------------------------------------------
```

Avant publication dans Maven Central, le nexus-staging-maven-plugin effectue des vérifications. Ainsi, ma première publication a été rejetée car aucun développeur n’était mentionné dans le _pom.xml_. Le nom de la licence Open Source choisie pour le projet est également indispensable.

Lors de futures releases, j’utiliserais directement le Maven Release Plugin comme je le faisais jusque-là sur CloudBees.

## Résultat

A l’issu de la publication, vous recevrez successivement 2 mails :

1. Nexus: Staging Completed
1. Nexus: Promotion Completed

Voici un extrait du second  mail :

```sh
Message from: https://oss.sonatype.org

Description:
com.javaetmoi.core:javaetmoi-hibernate-hydrate:1.0

Deployer properties:
•	"userAgent" = "Nexus-Client/2.7.2-01"
•	"userId" = xxxx
•	"ip" = xxxx
Details:

The following artifacts have been promoted to the "Releases"[id=releases] repository

/com/javaetmoi/core/javaetmoi-hibernate-hydrate/1.0/javaetmoi-hibernate-hydrate-1.0.jar
(SHA1: cd0d87951fc2c5ac5c8bef1ca10cd5c40a5a3e3c)
/com/javaetmoi/core/javaetmoi-hibernate-hydrate/1.0/javaetmoi-hibernate-hydrate-1.0-javadoc.jar
(SHA1: d43dc47450d0acbed4ce21a2e8ff69de06f03fd3)
/com/javaetmoi/core/javaetmoi-hibernate-hydrate/1.0/javaetmoi-hibernate-hydrate-1.0.pom.asc
(SHA1: cbfdc56ff91926164dacd6954782a2b1ade8eef2)
/com/javaetmoi/core/javaetmoi-hibernate-hydrate/1.0/javaetmoi-hibernate-hydrate-1.0.pom
(SHA1: 7336a648dc1deb3f6b223eb121ac2a1c0ef6053b)
/com/javaetmoi/core/javaetmoi-hibernate-hydrate/1.0/javaetmoi-hibernate-hydrate-1.0-javadoc.jar.asc
(SHA1: a91a7f1f2e5603346c43325c7d009008a9d0de18)
/com/javaetmoi/core/javaetmoi-hibernate-hydrate/1.0/javaetmoi-hibernate-hydrate-1.0-sources.jar.asc
(SHA1: 7e014101817772f1b90e5835b2b6b4e45713dcf6)
/com/javaetmoi/core/javaetmoi-hibernate-hydrate/1.0/javaetmoi-hibernate-hydrate-1.0-sources.jar
(SHA1: 45dbc2f47bcd690a00604f9c38be54383a99cc46)
/com/javaetmoi/core/javaetmoi-hibernate-hydrate/1.0/javaetmoi-hibernate-hydrate-1.0.jar.asc
(SHA1: 267be3c43664fa096fd38b77df205c4477c51ad0)
Action performed by Antoine Rey (mon email)
```

Dès réception de ce mail, l’artefact peut alors être télécharg dans votre repo local maven.
Pour se faire, ajouter la dépendance dans le pom.xml :

```xhtml
<dependency>
    <groupId>com.javaetmoi.core</groupId>
    <artifactId>javaetmoi-hibernate4-hydrate</artifactId>
    <version>2.0</version>
</dependency>
```

Puis lancer un build : mvn clean install

Les artefacts sont directement téléchargés depuis Maven Central :

```default
Downloading: http://repo.maven.apache.org/maven2/com/javaetmoi/core/javaetmoi-hibernate4-hydrate/2.0/javaetmoi-hibernate4-hydrate-2.0.pom
Downloaded: http://repo.maven.apache.org/maven2/com/javaetmoi/core/javaetmoi-hibernate4-hydrate/2.0/javaetmoi-hibernate4-hydrate-2.0.pom (12 KB at 9.3 KB/sec)
Downloading: http://repo.maven.apache.org/maven2/com/javaetmoi/core/javaetmoi-hibernate4-hydrate/2.0/javaetmoi-hibernate4-hydrate-2.0.jar
Downloaded: http://repo.maven.apache.org/maven2/com/javaetmoi/core/javaetmoi-hibernate4-hydrate/2.0/javaetmoi-hibernate4-hydrate-2.0.jar (11 KB at 25.0 KB/sec)
```

## Conclusion

La publication d’un JAR dans Maven Central n’est pas si compliqué. Elle n’est pas non plus réservée aux projets les plus connus. Votre groupId doit être choisi rigoureusement. Si vous disposez d’un nom de domaine, utilisez-le.

Pour automatiser encore davantage la publication de me releases dans Maven Central, il me reste une dernière étape : le faire depuis [mon instance Jenkins sur Dev@Cloud](https://javaetmoi.ci.cloudbees.com/). Les plugins Jenkins [M2 Release](https://wiki.jenkins-ci.org/display/JENKINS/M2+Release+Plugin) et [Promoted Builds](http://www.technologies-ebusiness.com/solutions/orchestrez-vos-deploiements-avec-jenkins) devraient m’y aider. Le plus compliqué sera sans doute d’installer et de faire perdurer une clé PGP privé.

Références :

- [OSSRH Guide](http://central.sonatype.org/pages/ossrh-guide.html)
- [Repository Nexus OSSRH de Sonatype](https://oss.sonatype.org/)
- [Jira de Sonatype](https://issues.sonatype.org/)
- [Page Apache Maven du Central Repository](http://central.sonatype.org/pages/apache-maven.html)
- [PGP signatures](http://central.sonatype.org/pages/working-with-pgp-signatures.html)
- [Apache Maven GPG plugin](http://maven.apache.org/plugins/maven-gpg-plugin/sign-mojo.html)
- [Guide pour uploader des artefacts dans le Maven Central Repository](http://maven.apache.org/guides/mini/guide-central-repository-upload.html)
