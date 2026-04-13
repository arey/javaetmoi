---
_edit_last: "1"
author: admin
categories:
  - retour-d'expérience
date: "2013-05-23T18:45:16+00:00"
toc: true
guid: http://javaetmoi.com/?p=692
parent_post_id: null
post_id: "692"
post_views_count: "8454"
summary: |-
  Au cours de la migration d’une cinquantaine d’applications web de Websphere vers **JBoss 5.1 EAP**, nous avons été confrontés à un problème de sécurité mis en évidence par l’infrastructure de pré-production : le firewall bloquait systématiquement toute requête comportant un **jsessionid** dans l’ **URL**.
  Modifier les règles du firewall pour laisser passer ce type de requêtes aurait introduit une faille de sécurité exploitable par appropriation de session web. Cette faille nous a d’ailleurs été révélée en parallèle par l’outil d’audit de sécurité [IBM AppScan](http://www-03.ibm.com/software/products/us/en/appscan/).
  Ce billet rappelle l’origine du problème et précise quelle solution a été employée pour le résoudre le plus rapidement possible.
tags:
  - apache
  - jboss
  - servlet
  - tomcat
title: Mod_headers à la rescousse du jsessionid
url: /2013/05/mod_headers-rescousse-jsessionid-jboss/

---
Au cours de la migration d’une cinquantaine d’applications web de Websphere vers **JBoss 5.1 EAP**, nous avons été confrontés à un problème de sécurité mis en évidence par l’infrastructure de pré-production : le firewall bloquait systématiquement toute requête comportant un **jsessionid** dans l’ **URL**.
Modifier les règles du firewall pour laisser passer ce type de requêtes aurait introduit une faille de sécurité exploitable par appropriation de session web. Cette faille nous a d’ailleurs été révélée en parallèle par l’outil d’audit de sécurité [IBM AppScan](http://www-03.ibm.com/software/products/us/en/appscan/).
Ce billet rappelle l’origine du problème et précise quelle solution a été employée pour le résoudre le plus rapidement possible.

## Description du problème

Les requêtes HTTP bloquées par le firewall à l’entrée de la DMZ ont le format suivant :

```apache
GET http://www.monapli.com/index.faces;jsessionid=4A3D4C11876FC7B22F98B0E14287BC8E.monappliServer01
```

Ces requêtes sont renvoyées par le navigateur lors de la première tentative d’accès d’un utilisateur à l’une des pages d’une application web, à savoir lorsque qu’aucune session web n’était encore créée.

Une analyse plus fine montre que ces requêtes sont émises par le navigateur suite à une demande de redirection 302 effectuée par le framework de sécurité mis en œuvre côté applicatif.
La requête initiale ayant déclenchée la redirection a la forme suivante :

```apache
POST http://www.monapli.com/index.faces + token d’authentification à usage unique
```

Et voici un exemple de réponse du serveur web :

```apache
HTTP/1.1 302 Found
Date: Wed, 22 May 2013 19:32:24 GMT
X-Powered-By: Servlet 2.5; JBoss-5.0/JBossWeb-2.1
Location: http://www.monappli.com/ index.faces;jsessionid=4A3D4C11876FC7B22F98B0E14287BC8E.monappliServer01
Content-Type: text/plain
```

## Les origines

L’ajout du ;jsessionid=xxx est pris à l’initiative du conteneur web lors de l’appel à la méthode HttpServletResponse:: **encodeRedirectURL**. Bien que pouvant s’apparenter à un bug, ce comportement fait partie intégrante de l’ **API Servlet**. En effet, lorsqu’une nouvelle session est créée, le serveur ne sait pas si le client supporte les cookies et les a activé. Il génère alors un **cookie JSESSIONID** spécifiant le jsessionid et réécrit ce jsessionid dans l’URL. Lorsque le client émet une seconde requête, le serveur vérifie la présence du cookie. Deux scénarios sont alors possibles :

1. Lorsque le serveur détecte le cookie JSESSIONID dans la requête, il désactive la réécriture d’URL avec les jsessionid.
1. Lorsque le cookie JSESSIONID n’est pas transmis mais que l’URL de la requête comporte un jsessionid, le serveur continue à réécrire toute URL en concaténant le jsessionid. Ce comportement s’applique tout au long de la navigation.

Initialement parti d’une bonne attention à l’époque où les navigateurs ne supportaient pas tous les cookies, ce mécanisme de suivi de session pose aujourd’hui plus de problèmes qu’il n’en résout : référencement dans les moteurs de recherche, stockage des URL dans le cache des proxys, déséquilibrage de clusters …
Devenu inutile, IBM l’a par défaut désactivé depuis au moins la version 5 de son serveur d’application Websphere. C’est pourquoi nous n’avions jusque-là jamais rencontré ce problème. Redhat JBoss a mis davantage de temps à se rendre compte de cette problématique de jsessionid [référencée sur son bugtracker](https://bugzilla.redhat.com/show_bug.cgi?id=CVE-2012-4529).

## Solutions

Pour contrer ce problème, [plusieurs solutions existent](http://fr.softuses.com/125807).
Certaines ne s’appliquent pas à nos contraintes d’environnements :

- JBossWeb 2.1 étant basé sur la version 6.0.15 de Tomcat, il n’est pas possible d’utiliser l’ [attribut disableURLRewriting du context.xml](http://tomcat.apache.org/tomcat-6.0-doc/config/context.html#Common_Attributes) introduit dans Tomcat 6.0.30
- Forcer le [SessionTrackingMode](http://docs.oracle.com/javaee/6/api/javax/servlet/SessionTrackingMode.html) à COOKIE dans le web.xml n’est possible que sur un conteneur de servlet 3.0 (ex : JBoss 6 EAP).

D’autres solutions nécessitent de modifier, releaser puis relivrer l’ensemble des applications web :

- La [solution proposée par RedHat](https://access.redhat.com/knowledge/solutions/16169) consistant à écrire un filtre de servlet JEE ressemblant au [JsessionIdRemoveFilter du framework Seam](https://jira.jboss.org/jira/browse/JBSEAM-3018) et dont le code source est proposé [page 44 du guide d’administration de JBoss EAP 5](https://access.redhat.com/site/documentation/en-US/JBoss_Enterprise_Application_Platform/5/pdf/Administration_And_Configuration_Guide/JBoss_Enterprise_Application_Platform-5-Administration_And_Configuration_Guide-en-US.pdf).
- La mise en place dans le web.xml  du filtre [Tuckey UrlRewriterFilter](http://www.tuckey.org/urlrewrite/) et la configuration du fichier urlrewrite.xml associé

La solution finalement retenue consiste à exploiter le module [mod\_headers](http://httpd.apache.org/docs/2.2/mod/mod_headers.html) du **serveur** **Apache 2.2** situé en frontal des JBoss. Alors que le [mod\_rewrite](http://httpd.apache.org/docs/2.2/fr/mod/mod_rewrite.html) ne peut agir que sur les requêtes HTTP,  le mod\_headers peut **modifier les en-têtes des réponses HTTP**. Toutes les en-têtes Location comportant un ;jsessionid= sont réécrites sans le  ;jsessionid=

Pour se faire, le module mod\_headers a été activé dans le fichier de configuration Apache htppd.conf :

```apache
LoadModule headers_module modules/mod_headers.so
```

La ligne suivante a ensuite été ajoutée dans le fichier de configuration de l‘hôte virtuel  vhost.conf :

```apache
Header edit Location ^(.*);jsessionid=(.*)$ $1
```

La réponse précédente réencodée par le mod\_headers donne :

```apache
HTTP/1.1 302 Found
Date: Wed, 22 May 2013 19:35:38 GMT
X-Powered-By: Servlet 2.5; JBoss-5.0/JBossWeb-2.1
Location: http://www.monappli.com/index.faces
Content-Type: text/plain
```

La redirection GET http://www.monapli.com/index.faces n’est plus bloquée par le firewall.

## Conclusion

Rapide à déployer, ce palliatif a permis d’adresser le plus grand nombre des applications.
Pour une  poignée d’entre elles, l’ajout du filtre de servlet a été nécessaire car aucune redirection n’était effectuée lors du premier accès à l’application. La page HTML rendue côté serveur comportait directement des liens comprenant le fameux jsessionid, la méthode HttpServletResponse::encodeUrl étant appelée par les différents tags positionnés sur la page.
