---
_edit_last: "1"
_wp_old_slug: ma-petite-usine-logicielle-github-cloudbee
author: admin
categories:
  - maven
date: "2012-12-15T09:08:10+00:00"
thumbnail: /wp-content/uploads/2012/12/cloudbees-github-jenkins.png
featureImage: /wp-content/uploads/2012/12/cloudbees-github-jenkins.png
featureImageAlt: "cloudbees-github-jenkins"
guid: http://javaetmoi.com/?p=436
parent_post_id: null
post_id: "436"
post_views_count: "36910"
summary: |-
  Suite à [une question](https://github.com/arey/maven-config-github-cloudbees/issues/1) qui m’a récemment été posée sur Github, j’ai réalisé que ce que j’avais mis en place pour des besoins personnels pouvait intéresser d’autres développeurs.

  Dans ce billet, je vais donc vous expliquer comment créer **votre propre usine logicielle**. Déployée à cheval sur **GitHub** et l’offre **DEV@Cloud** de **CloudBees**, vous y retrouverez les briques les plus classiques : SCM, intégration continue, dépôt de binaires, bug tracker, wiki …
  Le gain : à chaque commit poussé dans GitHub, votre **code** est **compilé**, **testé** unitairement puis **déployé** dans un **repository maven public** dédié aux Snapshots. Par ailleurs, vous pourrez effectuer des **releases maven** en local depuis votre poste de développement ; les artefacts construits seront mis à disposition dans un repository maven dédié. Tout développeur pourra librement référencer l’un ou l’autre de ces repository et utiliser votre code.

  En bonus, si vous développez des projets open source, vous n’aurez même pas à sortir votre carte bancaire.
  [![cloudbees-github-jenkins](http://javaetmoi.com/wp-content/uploads/2012/12/cloudbees-github-jenkins.png)](http://javaetmoi.com/wp-content/uploads/2012/12/cloudbees-github-jenkins.png)
tags:
  - buildhive
  - cloudbees
  - git
  - github
  - jenkins
  - maven
title: Ma petite usine logicielle
url: /2012/12/ma-petite-usine-logicielle-github-cloudbees/

---
Suite à [une question](https://github.com/arey/maven-config-github-cloudbees/issues/1) qui m’a récemment été posée sur Github, j’ai réalisé que ce que j’avais mis en place pour des besoins personnels pouvait intéresser d’autres développeurs.

Dans ce billet, je vais donc vous expliquer comment créer **votre propre usine logicielle**. Déployée à cheval sur **GitHub** et l’offre **DEV@Cloud** de **CloudBees**, vous y retrouverez les briques les plus classiques : SCM, intégration continue, dépôt de binaires, bug tracker, wiki …
Le gain : à chaque commit poussé dans GitHub, votre **code** est **compilé**, **testé** unitairement puis **déployé** dans un **repository maven public** dédié aux Snapshots. Par ailleurs, vous pourrez effectuer des **releases maven** en local depuis votre poste de développement ; les artefacts construits seront mis à disposition dans un repository maven dédié. Tout développeur pourra librement référencer l’un ou l’autre de ces repository et utiliser votre code.

En bonus, si vous développez des projets open source, vous n’aurez même pas à sortir votre carte bancaire.
[![cloudbees-github-jenkins](/wp-content/uploads/2012/12/cloudbees-github-jenkins.png)](/wp-content/uploads/2012/12/cloudbees-github-jenkins.png)

## Composants de l’usine de développement

Le tableau ci-dessous liste les différentes briques de l’usine de développement ainsi que les motivations qui m’ont poussé à les choisir.
**Brique de l’usine logicielle****Outil****Plateforme****Raisons**Gestionnaire de Code Source (SCM)GitGitHubPour utiliser la pleine puissance de Git, bridé jusque-là par l’utilisation en entreprise du bridge git-svn.Outil de buildMavenPoste de Dev
\+ CloudbeesL’incontournable maven.  Mais cela aurait pu être l’occasion de  tester Gradle.Intégration ContinueJenkinsCloudBeesUn comble : probablement celui que je connaissais le moins par rapport à Continium, Bamboo et TeamCity.Dépôt de binairesRepository MavenCloudbeesOffre de base de CloudBees suffisante.
Accès par webdavEspace documentaireWikiGitHubPages versionnées avec Git
Syntaxte MarkDown
Le XWiki de CloudBees aurait pu être une alternativeBugTrackerNavigateur WebGitHubProjets OSS personnels pas suffisamment actifs pour bénéficier d’un Jira (ni même d’une licence JRebel)
Afin de vous donner une idée du résultat, je vous invite à jeter un coup d’œil aux différentes URLs :

- Jenkins DEV@Cloud : [https://javaetmoi.ci.cloudbees.com](https://javaetmoi.ci.cloudbees.com/)
- Repository maven : [https://repository-javaetmoi.forge.cloudbees.com/](https://repository-javaetmoi.forge.cloudbees.com/)
- Compte github : [https://github.com/arey](https://github.com/arey)

## Pré-requis

2 prérequis sont nécessaires au déploiement d’une telle usine de développement :

1. Disposer d’un [compte GitHub](https://github.com/signup/) et d’un repository contenant un projet java déjà mavenisé
1. Avoir accès à la [plateforme de build de CloudBees](http://www.cloudbees.com/dev.cb), soit en souscrivant à l’une des [offres gratuites ou payantes](http://www.cloudbees.com/platform/pricing/devcloud.cb), soit en souscrivant au [Free FOSS Programm](http://www.cloudbees.com/foss/foss-dev.cb)

## Configuration Maven

Afin de pouvoir intégrer un projet mavenisé dans l’usine de développement, il est préalablement nécessaire de compléter sa configuration maven pour prendre en compte :

- Le **gestionnaire de code source** pour que maven ait accès en lecture / écriture au repository git distant (hébergé ici sur GitHub), ce qui est par exemple nécessaire pour tagger et faire des releases maven.
- Les **repository maven** des **releases** et des **snapshots**, ce qui est utile à Jenkins ou au plugin release de maven pour déployer un artefact, et par maven pour télécharger des artefacts.
- La configuration de l’ **extension maven wagon-webdav**, utile lors du déploiement d’un artefact sur le repo maven CloudBees utilisant le protocole webdav.
- Les **credentials** d’accès en écriture au **webdav**, là encore utile pendant la phase de déploiement d’un artefact.

Toute cette configuration est détaillée dans un précédent billet intitulé [Release Maven sous Windows d’un projet GitHub déployé sur CloudBees](/2012/04/release-maven-windows-github-deploy-cloudbees/). Vous y trouverez notamment comment configurer les différentes balises maven au travers 2 fichiers :

- **pom.xml** : <scm>, <distributionManagement>, <repositories> et <extensions>
- **settings.xml** : <servers>

Gage de son intérêt, le projet github [maven-config-github-cloudbees](https://github.com/arey/maven-config-github-cloudbees/) à l’origine de l’article a été forké par [Ryan Cambell](http://www.cloudbees.com/company-team.cb) et est désormais proposé dans la [Cloudbees Community](https://github.com/cloudbees) de GitHub.

Une fois le pom.xml commité dans GitHub avec le reste du code source, le build Jenkins correspondant peut être configuré.

## Configuration Jenkins

Depuis la console d’administration de Jenkins, vérifier que le _[Jenkins GIT plugin](https://wiki.jenkins-ci.org/display/JENKINS/Git+Plugin)_ soit installé puis installer le _[GitHub plugin](https://wiki.jenkins-ci.org/display/JENKINS/Github+Plugin)_.

Dans la section _CloudBees DEV@Cloud Authorization_, configurer l’URL du chemin d’accès au repository Github qui sera utilisée par le plugin GitHub:

[![cloudbees-build-authorization](/wp-content/uploads/2012/12/cloudbees-build-authorization.png)](/2012/12/ma-petite-usine-logicielle-github-cloudbees/cloudbees-build-authorization/)

Dans la section _Gestion de code source_ du build Jenkins, sélectionner l’option _Git Repositories_ puis renseigner le _Repository URL_.
La syntaxe à utiliser est la suivante : https://github.com/<username>/<repository name>.gitExemple : https://github.com/arey/hibernate-hydrate.git
[![cloudbees-build-git](/wp-content/uploads/2012/12/cloudbees-build-git.png)](/2012/12/ma-petite-usine-logicielle-github-cloudbees/cloudbees-build-git/)

Afin que Jenkins lance le build lors de la réception d’un hook en provenance de GitHub, sélectionner la case _Build when a change is pushed to GitHub_ dans le panneau ci-dessous :
[![cloudbees-jenkins-build-trigger](/wp-content/uploads/2012/12/cloudbees-jenkins-build-trigger.png)](/2012/12/ma-petite-usine-logicielle-github-cloudbees/cloudbees-jenkins-build-trigger/)

La version de maven, le chemin vers le pom.xml racine ainsi que le goal à exécuter peuvent être configurés dans la section _Build_ :
[![cloudbees-jenkins-maven](/wp-content/uploads/2012/12/cloudbees-jenkins-maven.png)](/2012/12/ma-petite-usine-logicielle-github-cloudbees/cloudbees-jenkins-maven/) Lorsqu’aucun goal n’est précisé, Jenkins exécute un _install_.

A la fin du build, on indique à Jenkins de déployer les artefacts dans le repository CloudBees des Snapshots :
[![cloudbees-jenkins-deploy](/wp-content/uploads/2012/12/cloudbees-jenkins-deploy.png)](/2012/12/ma-petite-usine-logicielle-github-cloudbees/cloudbees-jenkins-deploy/)

Afin d’exploiter au mieux le plugin GitHub de Jenkins et laisser Jenkins configurer les hooks dans GitHub, il est possible de renseigner votre login / mot de passe dans l’encart GitHub Web Hook accessible depuis le menu _Administration Jenkins > Configurer le Système_.
[![cloudbees-jenkins-github-web-hook](/wp-content/uploads/2012/12/cloudbees-jenkins-github-web-hook.png)](/2012/12/ma-petite-usine-logicielle-github-cloudbees/cloudbees-jenkins-github-web-hook/)

Dernière étape de la mise en place de notre usine de développement : la configuration de GitHub.

## Configuration GitHub

Pour que Jenkins soit notifié à chaque push dans GitHub et relancer ainsi le build maven configuré précédemment, il est nécessaire de **configurer un Hook web** dans GitHub.
La _WebHook URL_ doit référencer votre forge  logicielle CloudBees.
Syntaxe : **https:// _<cloudbees username>_.ci.cloudbees.com/github-webhook/**
Exemple : https://javaetmoi.ci.cloudbees.com/github-webhook/
[![github-webhook-cloudbees](/wp-content/uploads/2012/12/github-webhook-cloudbees.png)](/2012/12/ma-petite-usine-logicielle-github-cloudbees/github-webhook-cloudbees/) Cette configuration n’est a priori pas nécessaire si vous utilisez le plugin GitHub Jenkins. Ce dernier se charge en effet d’ajouter les WebHooks pour vous.

Pour que CloudBees ait les habilitations nécessaires pour accéder à l’ensemble de vos repository GitHub, sa **clé publique** doit être ajoutée dans la partie _SSH Keys_ accessible via le menu d’administration de GitHub :
[![github-ssh-keys](/wp-content/uploads/2012/12/githun-ssh-keys.png)](/2012/12/ma-petite-usine-logicielle-github-cloudbees/githun-ssh-keys/)

En principe, si je n’ai rien omis de mentionner dans ce guide, tout est prêt. Et pour vérifier que votre usine de développement est opérationnelle, vous avez le choix entre :

1. pousser une modification dans votre repository GitHub
1. ou simuler un hook depuis GitHub.

## Conclusion

Suivant CloudBees depuis son lancement il y’a plus de 2 ans, j’ai eu la chance de pouvoir bénéficier début 2012 de l’offre gratuite Free and Open-Source Software. Après avoir passé un peu de temps au départ pour mettre en place mon usine, j’en suis aujourd’hui pleinement satisfait et je serais prêt à l’expérimenter en entreprise.

N’ayant utilisé qu’une infime partie des services proposés par CloudBees, de nombreuses découvertes s’offrent encore à moi : utiliser le plugin release de Jenkins, tester SauceLabs ou bien encore déployer une application web sur la plateforme RUN@CloudBees.

Apparu quelques mois après mes débuts sur DEV@cloud, CloudBees propose le produit **[BuildHive](http://wiki.cloudbees.com/bin/view/DEV/BuildHive)** aux développeurs utilisant GitHub et qui souhaitent mettre en place de l’intégration continue sur leur projet. Non seulement ce produit est gratuit, mais il simplifie considérablement la configuration de votre build, à la fois côté Jenkins que côté GitHub grâce au protocole OAuth. **Tout est automatisé**. Je me suis inscrit et j’ai créé [mon premier build](https://buildhive.cloudbees.com/job/arey/job/hibernate-hydrate/) en à peine 2 minutes. Un hook sur les **pull request** permet même de lancer un build afin de valider le code soumis. Néanmoins, il y’a tout de même quelques limitations par rapport à la solution que vous ai proposée : pas de repository maven, impossibilité d'installer des plugins Jenkins ... A vous de décider lequel vous convient !
