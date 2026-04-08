---
_edit_last: "1"
author: admin
categories:
  - retour-d'expérience
date: "2021-01-03T11:44:26+00:00"
thumbnail: /wp-content/uploads/2021/01/logo-splunk.jpg
featureImage: /wp-content/uploads/2021/01/logo-splunk.jpg
guid: https://javaetmoi.com/?p=2100
parent_post_id: null
post_id: "2100"
post_views_count: "46560"
summary: |-
  ![](https://javaetmoi.com/wp-content/uploads/2020/12/lof-file-1.png)

  Publier en 2021 un article sur les logs n’est pas très novateur ; je vous l’accorde. Le **logging** est une pratique vieille comme l’informatique, ou presque. C’est une **pratique universelle** qu’on retrouve **quel que soit le langage de programmation** et quel que soit le type d’application. Pour autant, elle est survolée en fac et en école d’ingénieur. Les dévs apprennent bien souvent à logger sur le tas, en fonction de leurs besoins et de ce qui est déjà mis en place sur leur application. Rares sont également les entreprises mettant à disposition des normes et des bonnes pratiques en termes de traces applicatives.

  Dans cet article, je ne vous expliquerai pas comment utiliser [SLF4J](http://www.slf4j.org/), [Logback](http://logback.qos.ch/), [Log4j 2](https://logging.apache.org/log4j/2.x/) ou la controversée [API de Logging](https://docs.oracle.com/javase/8/docs/technotes/guides/logging/index.html) du langage Java. C’est un prérequis que bon nombre d’entre vous connaissent déjà. Beaucoup de ressources existent à ce sujet, en commençant par leurs documentations officielles.

  Non, **je vous y exposerai plutôt les bonnes pratiques que je préconise**, tant au niveau d’une application que d’une organisation. Je répondrai également aux questions les plus courantes : **quand utiliser tel ou tel niveau de log ?** **que mettre dans les messages de logs ?**<br>Nom de mon blog oblige, j'utiliserai des exemples venant du monde Java. Mais vous pourrez aisément transposer ces bonnes pratiques à d’autres technologies. Et bien entendu, elles sont à adapter en fonction de votre contexte et de vos besoins.
tags:
  - elasticsearch
  - logback
  - logstash
  - slf4j
  - splunk
title: Bonnes pratiques de logging
url: /2021/01/bonnes-pratiques-de-logging/

---
![](/wp-content/uploads/2020/12/lof-file-1.png)

Publier en 2021 un article sur les logs n’est pas très novateur ; je vous l’accorde. Le **logging** est une pratique vieille comme l’informatique, ou presque. C’est une **pratique universelle** qu’on retrouve **quel que soit le langage de programmation** et quel que soit le type d’application. Pour autant, elle est survolée en fac et en école d’ingénieur. Les dévs apprennent bien souvent à logger sur le tas, en fonction de leurs besoins et de ce qui est déjà mis en place sur leur application. Rares sont également les entreprises mettant à disposition des normes et des bonnes pratiques en termes de traces applicatives.

Dans cet article, je ne vous expliquerai pas comment utiliser [SLF4J](http://www.slf4j.org/), [Logback](http://logback.qos.ch/), [Log4j 2](https://logging.apache.org/log4j/2.x/) ou la controversée [API de Logging](https://docs.oracle.com/javase/8/docs/technotes/guides/logging/index.html) du langage Java. C’est un prérequis que bon nombre d’entre vous connaissent déjà. Beaucoup de ressources existent à ce sujet, en commençant par leurs documentations officielles.

Non, **je vous y exposerai plutôt les bonnes pratiques que je préconise**, tant au niveau d’une application que d’une organisation. Je répondrai également aux questions les plus courantes : **quand utiliser tel ou tel niveau de log ?** **que mettre dans les messages de logs ?**  
Nom de mon blog oblige, j'utiliserai des exemples venant du monde Java. Mais vous pourrez aisément transposer ces bonnes pratiques à d’autres technologies. Et bien entendu, elles sont à adapter en fonction de votre contexte et de vos besoins.

## Objectifs des logs

Les **logs** permettent d’ **historiser les évènements normaux et anormaux** survenus au cours du fonctionnement de logiciels, d’équipements réseaux ou bien encore d’applications. Dans la suite de cet article, je me focaliserai sur les **logs applicatifs** qui sont les logs produits par les **applications métiers** que vous développez.

Les logs applicatifs sont utiles à divers moments du cycle de vie d'une application :

1. En phase de **développement**, les logs sont complémentaires au **debugger** et permettent **de comprendre le fonctionnement d’une application** en suivant pas à pas le fil d'exécution de différentes fonctions critiques.
1. En phase d' **intégration** et de **recette**, ils permettent de **faciliter l'analyse des anomalies remontées par la QA.**
1. Enfin, en phase d' **exploitation**, les logs peuvent permettre de **diagnostiquer des problèmes de prod** remontés par le service utilisateur ou l’équipe MCO. De manière proactive, il est également possible de configurer des alertes sur des patterns d’erreur détectés dans les logs.

## Centraliser les logs

Sur le poste de dév, logger dans la console ou dans un fichier est courant. En un coup d’œil, le développeur peut s’y référer.  
Sur les autres environnements, il est recommandé d’utiliser un système centralisé de collecte de logs, chargé de les indexer et proposant une IHM et une API REST de recherche. En cas d’incident, cela évite de se connecter en SSH sur les 15 nœuds de votre cluster pour trouver le fichier qui vous intéresse.

Depuis une dizaine d’années, ont émergés de nombreux systèmes de collecte appelés **SIEM** (Security Information and Event Management). **Splunk** est un système propriétaire. La stack Elasticsearch / Logstash - Beats / Kibana ( **ELK**) est Open Source.


{{< gallery cols="1" >}}  
{{< figure src="/wp-content/uploads/2021/01/logo-splunk.jpg" alt="" caption="" >}}  
{{< figure src="/wp-content/uploads/2021/01/logo-elastic.png" alt="" caption="" >}}  
{{< /gallery >}}  

Les logs générés par les applicatifs sont soit directement envoyés à ces systèmes par le réseau (risque de perte de logs en cas d’indisponilité du SIEM), soit générés temporairement sur le système de fichier puis ingérés via un collecteur préalablement installé sur l’hôte.

La collecte des logs n’est pas l’apanage des applications back. Une **application front** basée sur Angular peut par exemple envoyer ses logs au SIEM ou à son Backend for Frontend via un framework comme [NGX Logger](https://www.npmjs.com/package/ngx-logger).

## Normaliser les données de logs

A l’échelle d’une entreprise, l’utilisation d’un SIEM est recommandée. La collecte des logs applicatifs dans un SIEM est facilitée par la **normalisation** des **données** de logs et de leur **format**.

Parmi les **données courantes**, on retrouve couramment la **date et l’heure** de l’évènement, le **niveau** de log, le **message** de log, le **nom** du logger et la **stacktrace** en cas d’erreur.  
D’autres données peuvent enrichir ses logs et faciliter les recherches ultérieures : **login** de l’utilisateur authentifié, nom de l’ **application**, nom du **serveur**, **identifiant de corrélation**, nom du **thread** …

D’une application à une autre, il est intéressant d’utiliser le **même pattern de log** afin de simplifier l’ingestion des lignes de logs par un collecteur Splunk ou un Logstash.

Pour aller un cran plus loin, je vous recommande de **normaliser le format de sortie**. Utiliser du **JSON** et des **noms de champs standardisés** (ex : _"level"_ pour le niveau de log) permet en effet d’indexer directement vos logs dans des index Splunk ou Elasticsearch, sans prétraitement et ceci, si vous le souhaitez, dans le même index. L’enrichissement des logs reste possible.  
Applications Java, Python, Node ou bien encore .NET peuvent adopter les mêmes conventions.

Normaliser le nom des champs dans un document accessible aux développeurs et aux Ops (ex : un wiki ou un sharepoint).

En Java, si vous utilisez Logback, je vous recommande d’utiliser le **projet [Logstash Logback Encoder](https://github.com/logstash/logstash-logback-encoder)** pour formater des logs en JSON. Bien que conçu initialement pour Logstash, son encoder JSON est compatible avec Splunk. Ce projet vient avec un certain nombre de [Standard Fields](https://github.com/logstash/logstash-logback-encoder#standard-fields) (ex : _@timestamp, @version, message_); il est possible de les renommer et d’en ajouter.

Voici un exemple de log au format JSON :

```json
{
  "@timestamp": "2021-01-10T12:47:41.234+01:00",
  "@version": 1,
  "message": "Contract created id=3d2b6902-d25d-4d98-b260-3733b880c2ea",
  "loggerName": "com.mycompagny.myapp.web.ContractController",
  "threadName": "ajp-/127.0.0.14:8009-1",
  "level": "INFO",
  "levelValue": 20000,
  "httpSessionID": "yYOvS0RKBM5y7NOrJQYAmGwA",
  "req": {
    "method": "POST",
    "remoteHost": "10.152.34.13",
    "requestURI": "/api/v1/contract",
  },
  "user": "jdoe",
  "transactionID": " a94fb8af-6587-4283-a8bf-69ba98d0da72",
  "app": {
    "code": "MYAPP",
    "env": "Production"
  }
}

```

## De l'importance du niveau de log

Générer des logs a un **impact** sur les **performances** de l'application, le **trafic réseau** si un SIEM est utilisé, et l' **espace disque** nécessaire à leur rétention.  
Il y'a un compromis à trouver entre verbosité des logs et espace disque : trop de logs noient les logs importants et saturent le système (leur durée de rétention est alors plus faible), trop peu de logs nuit à l'exploitabilité de l'application.  
Les niveaux de logs permettent d'adresser cette problématique. En effet, en fonction de l'environnement, la charge est différente : sur l'environnement de dév, le développeur est seul alors qu'en prod il peut y avoir des milliers/millions d'utilisateurs. **Une bonne pratique consiste à configurer les niveaux de logs différemment d'un environnement à l'autre.**

Dans le monde Java, la façade de logging **SLF4J** propose **5 niveaux** de logs : **TRACE**, **DEBUG**, **INFO, WARN** et **ERROR**.  
Le logger affiche toutes les traces niveaux supérieurs ou égal au niveau sélectionné. Par exemple si sur l'environnement d'intégration, le logger est configuré en niveau DEBUG, les traces de niveau DEBUG/INFO/WARN/ERROR seront affichées ; les traces de niveau TRACE sont ignorées.  
A noter que le niveau de log peut être configuré au niveau de chaque logger. Un **niveau par défaut** est positionné au niveau du **logger racine (root).**  
Le **niveau de log applicatif** correspond au niveau de log du package Java racine de votre application (ex: com.mycompany.myapp).

### Niveau de log applicatif en fonction de l'environnement

En production et pré-production, il est recommandé de positionner le **niveau de log applicatif** à INFO. Ne tracer que les WARN et ERROR masquerait les logs précédents pouvant être utiles à l’interprétation de l'erreur. Les logs INFO trop verbeux sont à abaisser en DEBUG. Le niveau de log comme Spring et Hibernate peut également être positionné en INFO. Le niveau de logs des frameworks très verbeux est relevé à WARN ou ERROR (ex : Atomikos).  
En intégration et en recette, le niveau DEBUG est souvent pertinent. Il évite de devoir redémarrer le serveur d’application (ex : un JBoss) pour baisser le niveau de log ou faire appel au runtime à l’actuator _/actuator/loggers_ d’une application Spring Boot.  
Sur le poste de dév, vous pouvez alterner entre INFO, DEBUG ou TRACE en fonction de vos tâches.

### Types de log par niveau

Le tableau ci-dessous précise le niveau de gravité à utiliser en fonction de la nature de l’évènement que l'on souhaite tracer :

**Niveau****Usage****Exemples****TRACE**Utilisé pour le débogage fin en mode verbeux de l'application.  
Par expérience, ce niveau est très peu utilisé par les développeurs, mais pourrait l’être davantage.\- Nouvelle valeur d'une variable  
\- Résultat d'une évaluation conditionnelle  
\- Trace d'exécution d'une boucle   
\- Entrée / sortie d'une méthode**DEBUG**Utilisé pour le débogage courant de l'application. Les informations loguées avec ce niveau intéressent plus particulièrement le développeur.\- Flux entrées / sorties (ex: requêtes SQL / requêtes HTTP)  
\- Données saisies invalides**INFO**Traces fournissant des informations contextualisées sur le fonctionnement général de l'application et son utilisation.  
Ces traces à destination du métier et de la MCO.  
Les logs d'audit sont également logués avec le niveau INFO.\- Opérations en écriture qui ont un sens fonctionnel (ex: validation d’une commande, émission de contrat, génération de courrier)  
\- Opération en lecture au cas par cas  
\- Début et fin des grandes étapes d'un batch ou d'un traitement long  
\- Sauvegarde et fermeture de fichiers  
\- Connexion / déconnexion d'un utilisateur**WARN**Trace d'anomalies ne déstabilisant pas l'application et ne demandant pas une intervention immédiate (erreur d'ordre fonctionnel par exemple).  
Problème non bloquant ne faisant pas échouer la transaction métier. Permet de ne pas spammer les logs avec des logs de niveau ERROR.\- Un paramétrage applicatif est manquant mais ce cas est prévu par le système (une valeur par défaut est appliquée, par exemple) et son fonctionnement n'est pas remis en cause  
\- Erreur de login**ERROR**Trace d'anomalie signalant une erreur importante mais ne remettant pas en cause le fonctionnement général de l’application. Ce niveau de log signifie un arrêt de la requête/service en cours et fait généralement suite à une exception de type RuntimeException remontant au plus haut de la pile d’appel. Le niveau FATAL n'existant pas dans SLF4J, les erreurs critiques empêchant tout fonctionnement ultérieur de l'application sont également tracées avec le niveau ERROR.\- Adhérence momentanément indisponible (ex: erreur 503 remontée lors de l’appel une API REST)  
\- Erreur JDBC liée à une contrainte d'intégrité  
\- Arrêt inattendu d'un batch (ex : filesystem saturé)

## Contenu des messages des logs

Un message de log se doit d'être lisible, explicite et comporter suffisamment d’informations pour être exploité. Il **doit fournir des informations contextuelles** que ne permet pas de donner par exemple une stacktrace (ex: numéro de contrat).

Log sans intérêt :

```text
Echec du traitement
```

Log exploitable :

```text
Echec du traitement numéro=123: checksum=23 invalide
```

Lorsque vous ne pouvez pas structurer vos logs (en utilisant du JSON), il est intéressant d’utiliser des **paires clé=valeur**. Une plateforme comme Splunk peut automatiquement détecter ce pattern et extraire la clé et sa valeur.

### Données à ne pas logger

En accord avec la RGPD et la CNIL, les données sensibles listées dans la catégorie [A3:2017 Sensitive Data Exposure](https://owasp.org/www-project-top-ten/2017/A3_2017-Sensitive_Data_Exposure) de l’OWAP ne doivent pas apparaître dans les logs.

- Les mots de passe
- Informations nominatives : nom, prénom, nom de naissance, numéro de sécurité sociale
- Coordonnées bancaires : IBAN, RIB, numéro de carte bancaire
- Informations de localisation : adresse postale, adresse IP, e-mail
- Données de santé, génétiques et biométriques

Vous avez le choix entre ne pas les concaténer aux messages de logs ou bien de les masquer avec, par exemple, des wildcards \*\*\*\*. Cette seconde option a un cout sur les performances car elles utilisent souvent des regex.  
Le projet Logstash Logback Encoder propose un mécanisme basé sur le décorateur [MaskingJsonGeneratorDecorator](https://github.com/logstash/logstash-logback-encoder#masking). Avec Logback, vous trouverez facilement différents exemples comme [celui proposé par Dhaval Kolapkar](https://medium.com/@kolapkar.dhaval/mask-sensitive-data-in-logs-7e06496e56c1).

L’enregistrement systématique des flux REST et SOAP en production pose problème car il faut identifier les flux pouvant véhiculer certaines de ces informations et les masquer.

### Étiqueter les logs

Afin d'en simplifier la recherche et de leur donner un sens fonctionnel, il est possible d’étiqueter les messages de log à l'aide de **hashtags** comme sur Twitter.

Par exemple, les **pistes d’audit** demandées par les PO dans vos User Story peuvent être étiquetées avec le hashtag **#audit** :

```java
LOG.info("Envoi de la commande numero=" + order.getNumber() + " #audit");
```

Un autre exemple consiste à tagger les logs remontant des problèmes de performance (appels ou requêts longues) avec le hashtag **#perf**.

## Autres bonnes pratiques

Pour terminer ce billet, voici quelques autres bonnes pratiques que je vous recommande d’adopter :

- **Ne pas logger 2x la même erreur** : d'une manière générale, ne pas logger l'erreur lorsque l’exception interceptée est propagée ( _throw_ dans un _catch_). L'exception doit être loggée en haut de la pile d'appel, en général dans un handler d'exceptions générique.
- **Pertinence des messages des logs** : un log de niveau info sans information contextuelle ne peut pas être exploité en production (ex: "Contrat émis"). Le message doit être contextualisé (ex: "Contrat émis id=123").
- **Pertinence des messages des erreurs** : lorsqu'on encapsule une exception, le message doit apporter des informations supplémentaires sur le contexte d'appel (ex: numéro de client, étape de traitement ...)
- **Activer le logging des enveloppes SOAP / body REST jusqu'en recette** est pratique pour rejouer les flux posant soucis. Pensez à exclure les appels contenant des flux binaires (ex : téléchargement de fichiers).
- **Login utilisateur** : le login de l'utilisation authentifié avec un framework de sécurité (ex: Spring Security) doit systématiquement être ajouté en tête / métadonnées de log. Cela nécessite généralement un développement spécifique (ex : utilisation de filtre de servlet, du [MDC](http://logback.qos.ch/manual/mdc.html) de SLF4J et d’un _[PatternLayoutEncoder](http://logback.qos.ch/manual/layouts.html)_ Logback). Dans l’exemple de log JSON précédent, on retrouve le login au niveau de la propriété _user_.
- **Utiliser un identifiant de corrélation** : pouvoir lier des lignes de logs entre elles est une fonctionnalité très appréciable. Pour la mettre en œuvre, créer un identifiant de corrélation de type UUID au début d’une transaction métier et ajouter systématiquement cet UUID aux métadonnées de logs (comme le login). Pour aller plus loin, vous pouvez passer cet identifiant de système en système via une en-tête http ou JMS (ex : [X-Request-ID](https://doc.scalingo.com/platform/app/x-request-id)). Dans l’exemple de log JSON précédent, on retrouve cet identifiant au niveau de la propriété _transactionID_.
- **Changement à chaud du niveau de logs** : lors d’un incident de prod, il est parfois nécessaire d’abaisser temporairement le niveau de logs afin de qualifier le problème. Changer à chaud ce niveau de logs sans redémarrer l’application est souvent nécessaire. Certaines stacks techniques comme [Spring Boot et son **actuator levels**](https://www.baeldung.com/spring-boot-changing-log-level-at-runtime) le permettent facilement. L’utilisation de [Spring Boot Admin](https://github.com/codecentric/spring-boot-admin) en facilite l’usage. Pensez à sécuriser ces endpoints.
- **Se prémunir du log forging**: la vulnérabilité d’ [injection de logs](https://owasp.org/www-community/attacks/Log_Injection) par ajout de caractères CRLF (\\r\\n) dans des paramètres HTTP loggés figure dans le Top 10 du classement 2017 des failles de sécurité de l’OSWAP. La configuration de votre framework de logging permet de substituer ces caractères et ainsi de se prémunir de cette vulnérabilité : à l’aide d’un Pattern Layout avec Log4J 2 ou d’un conversionRule avec Logback.
- **Maitriser la volumétrie des logs** : lorsque les logs sont consignés dans des fichiers de log, il est nécessaire de dimensionner le filesystem en regard de la volumétrie maximum des logs, sans quoi vous pourriez perdre des logs (sans espace disque, plus de logs). Pour diminuer la taille des logs, ces derniers peuvent être historisés tout en étant compressés (une archive d'un fichier de 10 Mo occupe généralement moins de 500 Ko). Lorsque les logs sont indexés dans un SIEM, les fichiers servent alors de tampons. Leur dimensionnement permet de palier à l'indisponibilité du SIEM. C'est la taille de l'index Elasticsearch ou Splunk qui conditionne la durée de rétention des logs.
- **Configurer son IDE** pour déclarer rapidement le logger d’une classe, par exemple sous IntelliJ avec un [Live Template](https://medium.com/@motlin/intellij-live-templates-ca8082bedc3f).

## Conclusion

Dans cet article, je vous aurais présenté des bonnes pratiques de logs à appliquer ou adapter au niveau de votre application et de votre organisation.

Disposer de logs pertinentes et utiles nécessite un travail de fond. Il est rarement possible de viser juste du premier coup. Les logs se retravaillent et s’affinent sur plusieurs itérations. Analyser les logs de recette et de prod permet d’améliorer les logs existants en les complétant ou en rajoutant du contexte. Les incidents de prod sont également un moyen de vérifier si vos logs sont exploitables et de corriger le tir si besoin est.

Ressources :

- [Le logging](https://www.jmdoudoux.fr/java/dej/chap-logging.htm) (Jean-Michel Doudoux)
- [Comparatif de solutions SIEM : Splunk et ELK](https://maximepiazzola.wordpress.com/2018/01/19/introduction-aux-solutions-siem/) (Maxime Piazzola)
- [Log tagging creates smarter application logs #awesomelogs](https://stackify.com/get-smarter-log-management-with-log-tags/) (Alexandra Altaver)
- [Logging best practices in an app or add-on for Splunk Enterprise](https://dev.splunk.com/enterprise/docs/developapps/addsupport/logging/loggingbestpractices/)
- [Changing de log Logging Level at the Runtime  for a Spring Boot Application](https://www.baeldung.com/spring-boot-changing-log-level-at-runtime) (Baeldung)
- [Log Forging by CRLF Injection](https://www.srccodes.com/log-forging-by-crlf-log-injection-owasp-security-vulnerability-attacks-crlf) (Abhijit Ghosh)
- [Mask sensitive data in logs](https://medium.com/@kolapkar.dhaval/mask-sensitive-data-in-logs-7e06496e56c1) (Dhaval Kolapkar)
