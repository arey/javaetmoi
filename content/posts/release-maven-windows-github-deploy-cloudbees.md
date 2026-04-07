---
_edit_last: "1"
author: admin
categories:
  - maven
date: "2012-04-12T19:42:24+00:00"
thumbnail: /wp-content/uploads/2012/04/logo_github.png
featureImage: /wp-content/uploads/2012/04/logo_github.png
featureImageAlt: "logo_github"
guid: http://javaetmoi.com/?p=81
parent_post_id: null
post_id: "81"
post_views_count: "14394"
summary: |-
  [![logo_github](http://javaetmoi.com/wp-content/uploads/2012/04/logo_github-229x300.png)](http://javaetmoi.com/wp-content/uploads/2012/04/logo_github.png) Habitué aux releases maven avec SVN, j’ai rencontré quelques difficultés pour effectuer la première release du projet [Hibernate Hydrate](https://github.com/arey/hibernate-hydrate) \[1\] hébergé sur GitHub et présenté dans un [précédent billet](http://javaetmoi.com/2012/03/hibernate-dites-adieu-aux-lazy-initialization-exception/).

  Pour rappel, lors d’une release, le plugin maven accède au gestionnaire de code source pour commiter les modifications effectuées sur les pom.xml et créer un tag. Il déploie ensuite les artefacts sur le repo maven distant.

  Mes contraintess techniques étaient les suivantes :

  - Plateforme de développement : **Windows** 7, JDK 6, **mSysGit**
  - Code source Java **mavenisé** et hébergé sur **GitHub**
  - Le repo maven sur lequel déployer les artefacts maven est hébergé par **CloudBees** et accessible par le protocople [Webdav](http://fr.wikipedia.org/wiki/WebDAV) \[2\]

  Les réponses apportées par ce billet sont :

  1. **Configuration maven pour GitHub**
  2. **Problème de passphrase SSH spécifique à Windows**
  3. **Configuration maven du repo CloudBees
tags:
  - cloudbees
  - git
  - github
  - maven
title: Release Maven sous Windows d’un projet GitHub déployé sur CloudBees
url: /2012/04/release-maven-windows-github-deploy-cloudbees/

---
[![logo_github](/wp-content/uploads/2012/04/logo_github.png)](/wp-content/uploads/2012/04/logo_github.png) Habitué aux releases maven avec SVN, j’ai rencontré quelques difficultés pour effectuer la première release du projet [Hibernate Hydrate](https://github.com/arey/hibernate-hydrate) \[1\] hébergé sur GitHub et présenté dans un [précédent billet](/2012/03/hibernate-dites-adieu-aux-lazy-initialization-exception/).

Pour rappel, lors d’une release, le plugin maven accède au gestionnaire de code source pour commiter les modifications effectuées sur les pom.xml et créer un tag. Il déploie ensuite les artefacts sur le repo maven distant.

Mes contraintess techniques étaient les suivantes :

- Plateforme de développement : **Windows** 7, JDK 6, **mSysGit**
- Code source Java **mavenisé** et hébergé sur **GitHub**
- Le repo maven sur lequel déployer les artefacts maven est hébergé par **CloudBees** et accessible par le protocople [Webdav](http://fr.wikipedia.org/wiki/WebDAV) \[2\]

Les réponses apportées par ce billet sont :

1. **Configuration maven pour GitHub**
1. **Problème de passphrase SSH spécifique à Windows**
1. **Configuration maven du repo CloudBees**

# Configuration maven pour GitHub

Pour permettre à maven d’accéder en lecture et en écriture à votre repo GitHub, vous devez tout d’abord configurer comme suit la balise <scm> de votre pom.xml :

```xml
<scm>
<url>https://github.com/arey/maven-config-github-cloudbees</url>
<connection>scm:git:ssh://git@github.com/arey/maven-config-github-cloudbees.git</connection>
<developerConnection>scm:git:ssh://git@github.com/arey/maven-config-github-cloudbees.git</developerConnection>
</scm>
```

L’accès en écriture sur un repo GitHub requière l’utilisation du protocole **SSH**. L’URL est conforme à ce qui est spécifié dans la [documentation de référence maven](http://maven.apache.org/scm/git.html)\[3\] :

```sh
scm:git:ssh://server_name[:port]/path_to_repository
```

A noter une syntaxe légèrement différent au chemin SSH affiché sur GitHub : **/arey** et non **:arey**, le **caractère :** étant utilisé pour préciser le port de connexion.

[![URL SSH de GitHub](/wp-content/uploads/2012/04/github-ssh-url.png)](/wp-content/uploads/2012/04/github-ssh-url.png)

Pour tester la configuration maven, vous pouvez par exemple utiliser le plugin scm pour **créer un tag**. C’est ce plugin qui est utilisé par le plugin release.

```sh
mvn org.apache.maven.plugins:maven-scm-plugin:1.6:tag -Dtag=test -Dbasedir=.
```

Vous devriez obtenir les logs suivants :

```default
[INFO] --- maven-scm-plugin:1.6:tag (default-cli) @ maven-config-github-cloudbees ---
[INFO] Final Tag Name: 'test'
[INFO] Executing: cmd.exe /X /C "git tag -F D:\tmp\maven-scm-1264232534.commit test"
[INFO] Working directory: D:\dev\workspaces\WS_GitHub\maven-config-github-cloudbees
[INFO] Executing: cmd.exe /X /C "git push ssh://git@github.com/arey/maven-config-github-cloudbees.git test"
[INFO] Working directory: D:\dev\workspaces\WS_GitHub\maven-config-github-cloudbees
```

1 minute. 2 minutes. Le plugin s’arrête là, comme bloqué. L’occupation CPU est à 0%. Ne cherchez pas, vous êtes sous Windows.

# Problème SSH spécifique à Windows

En interne, le plugin scm exécute des lignes de commandes git.
Sous Windows, la ligne de commande git est exécutée par l’interpréteur de commandes cmd.exe en mode non interactif.
Or, lorsque vous essayez manuellement de pousser vos modifications vers GitHub depuis un bash git ou une ligne de commande avec git dans le path, Git vous demande systématiquement votre passphrase :

```shell
git push
Enter passphrase for key '/c/Users/Antoine/.ssh/id_rsa':
```

L’explication est là : **lors d’un tag** ou d’un **push**, **le plugin scm est bloqué** car il attend votre passphrase. Pour autant, il ne vous demande jamais de le saisir. Vous vous retrouvez bloqué.

L’une des solutions permettant de résoudre ce problème est de répondre à la question _: « Comment faire pour que Windows retienne ma passphrase ? »_  Stackoverflow.com vous donne [la réponse](http://stackoverflow.com/questions/370030/why-git-cant-remember-my-passphrase-under-windows) \[4\].

En résumé, vous allez demander à git d’utiliser PuTTY pour communiquer en SSH avec GitHub. L’agent d’authentification SSH Pageant sera utilisé pour conserver votre clés privée Github en mémoire pour que vous puissiez vous authentifier sans avoir besoin de retaper votre phrase de passe à chaque fois. Voici le mode opératoire :

1. Télécharger puis décompresser l’archive **putty.zip** librement téléchargeable depuis le [site de Putty](http://www.chiark.greenend.org.uk/~sgtatham/putty/download.html) \[5\].
1. Utiliser **[PuTTYGen.exe](http://marc.terrier.free.fr/docputty/Chapter8.html#pubkey-puttygen)** \[6\] pour **convertir** au format PuTTY (.ppk) **votre clé RSA GitHub** généré avec open SSH.
1. Exécuter **[pageant.exe](http://marc.terrier.free.fr/docputty/Chapter9.html#pageant)** \[7\], ajouter la clé au format PuTTY and saisir le passphrase [![](/wp-content/uploads/2012/04/variables-environnement-git-ssh-plink.png)](/wp-content/uploads/2012/04/variables-environnement-git-ssh-plink.png)
1. Déclarer la variable d’environnement **GIT\_SSH** en spécifiant le **chemin vers [plink.exe](http://marc.terrier.free.fr/docputty/Chapter7.html#plink)** \[8\], outil de connexion en ligne de commande utilisé pour automatiser des connexions.

Pour tester la configuration, ouvrir une nouvelle fenêtre de commande et exécuter la commande suivante :

```shell
C:\Software\Dev\Putty>plink.exe git@github.com
Using username "git".
Server refused to allocate pty
Hi arey! You've successfully authenticated, but GitHub does not provide shell access.
```

La création d’un tag par le plugin scm de maven doit désormais aboutir.

# Configuration des repository Cloudbees

Avant de pouvoir effectuer une release, il est encore nécessaire de configurer les repository maven de votre forge CloudBees. Il s’agit ici de configuration maven relativement ordinaire.

Lors de la phase de déploiement d’un artefact, 2 repositories sont nécessaires, l’un pour déployer des releases,et  l’autre pour déployer des snapshots :

```xml
<distributionManagement>
    <downloadUrl>https://github.com/arey/maven-config-github-cloudbee</downloadUrl>
    <repository>
      <id>javaetmoi-cloudbees-release</id>
      <name>javaetmoi-cloudbees-release</name>
      <url>dav:https://repository-javaetmoi.forge.cloudbees.com/release/</url>
    </repository>
    <snapshotRepository>
      <id>javaetmoi-cloudbees-snapshot</id>
      <name>javaetmoi-cloudbees-snapshot</name>
      <url>dav:https://repository-javaetmoi.forge.cloudbees.com/snapshot/</url>
    </snapshotRepository>
 </distributionManagement>
```

Point d’attention : les repositories CloudBees ne sont accessibles en écriture que par le protocole WebDAV. Les URL des repository doivent donc être préfixées par un **dav:**

L’extension maven wagon-webdav est requis pour que maven puisse interpréter le dav:.  A ajouter dans la balise <build> de votre configuration :

```xml
<extensions>
    <extension>
        <groupId>org.apache.maven.wagon</groupId>
        <artifactId>wagon-webdav</artifactId>
        <version>1.0-beta-2</version>
    </extension>
</extensions>
```

Afin que maven puisse accéder à ces repository pour télécharger les snapshots et les releases, il est nécessaire de les déclarer, soit dans le pom.xml de votre projet, soit dans le fichier setting.xml global ou local à l’utilisateur (ce qui est une bien meilleure pratique) :

```xml
<repositories>
    <repository>
      <id>javaetmoi-cloudbees-release</id>
      <name>javaetmoi-cloudbees-release</name>
      <url>https://repository-javaetmoi.forge.cloudbees.com/release/</url>
      <releases>
        <enabled>true</enabled>
      </releases>
      <snapshots>
        <enabled>false</enabled>
      </snapshots>
    </repository>
    <repository>
      <id>javaetmoi-cloudbees-snapshot</id>
      <name>javaetmoi-cloudbees-snapshot</name>
      <url>https://repository-javaetmoi.forge.cloudbees.com/snapshot/</url>
      <releases>
        <enabled>false</enabled>
      </releases>
      <snapshots>
        <enabled>true</enabled>
      </snapshots>
    </repository>
  </repositories>
```

Lors d’un déploiement distant (ex : mvn deploy), maven doit disposer des paramètres de connexion pour écrire dans l’un ou l’autre des repository. A configurer dans le fichier setting.xml global ou local de l’utilisateur :

```xhtml
<servers>
    <server>
      <id>javaetmoi-cloudbees-snapshot</id>
      <username>javaetmoi</username>
      <password>Mot de passe CloudBees</password>
    </server>
    <server>
      <id>javaetmoi-cloudbees-release</id>
      <username>javaetmoi</username>
      <password>Mot de passe CloudBees </password>
</server>
```

 [![](/wp-content/uploads/2012/04/github-webdav-username.png)](/wp-content/uploads/2012/04/github-webdav-username.png)

Attention, bien que le mot de passe soit celui que vous utilisez pour vous connecter à vore compte CloudBees, le **username** ne correspond pas à votre adresse email, mais celui spécifié dans la forge CloudBees comme le montre la capture d’écran ci-contre.

Pour figer sa version, le plugin maven release peut également être déclaré dans votre pom.xml :

```xml
<plugin>
    <groupId>org.apache.maven.plugins</groupId>
    <artifactId>maven-release-plugin</artifactId>
    <version>2.2.2</version>
</plugin>
```

Ca y’est, toute la configuration est en place. A vous de jouer :

```default
mvn release:prepare release:perform
```

# Conclusion

Afin d’avoir sous la main un squelette pour un prochain projet, j’ai initié **un projet GitHub regroupant toute la configuration maven nécessaire : [https://github.com/arey/maven-config-github-cloudbees](https://github.com/arey/maven-config-github-cloudbees)** \[9\]. Vous pouvez y télécharger l’intégralité du **pom.xml** et du **settings.xml** décrits dans cet article\]. Ce projet a fait des émules puisque le code a été forké par la [CloudBees-Community](https://github.com/CloudBees-community) \[10\] de Github.

Pour ne plus avoir besoin à configurer PuTTY, un axe d’amélioration du plugin release serait de pouvoir s’appuyer un provider Git en full java, basé par exemple sur [**JGit**](http://eclipse.org/jgit/)\[11\] (projet utilisé par le plugin Eclipse EGit).  Initié par Olivier Lamy, le [projet maven-scm-provider-jgit](http://code.google.com/a/apache-extras.org/p/maven-scm-provider-jgit) \[12\] semble malheureusement s’être arrêté avant que jgit ne bascule sous le giron de la fondation Eclipse. Avis aux contributeurs !!

Références :

1. [Projet Hibernate Hydrate](https://github.com/arey/hibernate-hydrate) hébergé sur Github
1. [Définition du protocole WebDAV](http://fr.wikipedia.org/wiki/WebDAV) sur Wikipédia
1. [Apache Maven SCM Git Implementation](http://maven.apache.org/scm/git.html) dans la documentation de référence maven
1. [Why git can’t remembrer my passphrase under Windows](http://stackoverflow.com/questions/370030/why-git-cant-remember-my-passphrase-under-windows) sur stackoverflow.com
1. [Télechargement de PuTTY](http://www.chiark.greenend.org.uk/~sgtatham/putty/download.html)
1. [Manuel utilisateur de PuTTYgen](http://marc.terrier.free.fr/docputty/Chapter8.html#pubkey-puttygen)
1. [Manuel utilisateur de Pageant](http://marc.terrier.free.fr/docputty/Chapter9.html#pageant)
1. [Manuel utilisateur de plink](http://marc.terrier.free.fr/docputty/Chapter7.html#plink)
1. [Projet Maven Config  pour GitHub & CloudBees](https://github.com/arey/maven-config-github-cloudbees) hébergé sur GitHub
1. [Communauté CloudBees](https://github.com/CloudBees-community) sur GitHub
1. [Site officiel du projet JGit](http://eclipse.org/jgit/) hébergé sur Eclipse.org
1. [Site officiel du projet maven-scm-provider-jgit](http://code.google.com/a/apache-extras.org/p/maven-scm-provider-jgit) hébergé sur Google Code
