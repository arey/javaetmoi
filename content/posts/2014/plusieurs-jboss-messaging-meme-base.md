---
_edit_last: "1"
author: admin
categories:
  - retour-d'expérience
date: "2014-03-24T18:26:20+00:00"
toc: true
thumbnail: wp-content/uploads/2014/03/2014-04-jboss-messaging-meme-schema.png
featureImage: wp-content/uploads/2014/03/2014-04-jboss-messaging-meme-schema.png
featureImageAlt: "Architecture JBoss Messaging"
guid: http://javaetmoi.com/?p=1019
parent_post_id: null
post_id: "1019"
post_views_count: "4734"
summary: |-
  Ce billet ne devrait intéresser que les développeurs Java ou administrateurs JBoss en charge de la configuration de **JBoss Messaging**, le broker JMS intégré aux versions  4.3 et 5.x du serveur d’application JBoss EAP.
  Pour fil conducteur, prenons l’exemple d’une application Java EE déployée dans un pseudo cluster  JBoss où, par choix d’architecture technique, **chaque serveur JBoss est autonome**. A ce titre, les sessions HTTP ne sont pas partagées entre les différents serveurs JBoss ; le répartiteur de charge fonctionne en affinité de session De plus, chaque serveur dispose de ses propres files JMS (clustering JBoss Messaging non mis en œuvre). Les **messages JMS** sont **persistés dans une base de données**, Oracle dans notre cas **.** La persistance des messages peut se faire de 2 manières :

  1. Utiliser un schéma Oracle différent pour chaque serveur JBoss du cluster
  2. **Utiliser le même schéma pour tous les serveurs JBoss du cluster**

  JBoss Messaging supportant le **multi-tenancy**, cet article explique comment mettre en œuvre la 2ième solution.

  [![Architecture JBoss Messaging](wp-content/uploads/2014/03/2014-04-jboss-messaging-meme-schema.png)](wp-content/uploads/2014/03/2014-04-jboss-messaging-meme-schema.png)

  ![Architecture JBoss Messaging](wp-content/uploads/2014/03/2014-04-jboss-messaging-meme-schema.png)
tags:
  - bug
  - jboss
  - jms
  - oracle
title: Plusieurs JBoss Messaging pour une même base
url: /2014/03/plusieurs-jboss-messaging-meme-base/

---
Ce billet ne devrait intéresser que les développeurs Java ou administrateurs JBoss en charge de la configuration de **JBoss Messaging**, le broker JMS intégré aux versions  4.3 et 5.x du serveur d’application JBoss EAP.
Pour fil conducteur, prenons l’exemple d’une application Java EE déployée dans un pseudo cluster  JBoss où, par choix d’architecture technique, **chaque serveur JBoss est autonome**. A ce titre, les sessions HTTP ne sont pas partagées entre les différents serveurs JBoss ; le répartiteur de charge fonctionne en affinité de session De plus, chaque serveur dispose de ses propres files JMS (clustering JBoss Messaging non mis en œuvre). Les **messages JMS** sont **persistés dans une base de données**, Oracle dans notre cas **.** La persistance des messages peut se faire de 2 manières :

1. Utiliser un schéma Oracle différent pour chaque serveur JBoss du cluster
1. **Utiliser le même schéma pour tous les serveurs JBoss du cluster**

JBoss Messaging supportant le **multi-tenancy**, cet article explique comment mettre en œuvre la 2ième solution.

[![Architecture JBoss Messaging](wp-content/uploads/2014/03/2014-04-jboss-messaging-meme-schema.png)](wp-content/uploads/2014/03/2014-04-jboss-messaging-meme-schema.png)

## Solution

Le [manuel d’administration de JBoss Messaging](https://access.redhat.com/site/documentation/en-US/JBoss_Enterprise_Application_Platform_Common_Criteria_Certification/5/html/JBoss_Messaging_User_Guide/) explique clairement comment configurer JBoss Messaging en cluster ; les files JMS sont alors partagées pour tous les serveurs JBoss du même cluster. Par contre, elle reste évasive sur l’utilisation d’une même base de données pour plusieurs serveurs qui ne seraient pas en cluster.

[![2014-04-jboss-messaging-meme-schema-tables-jbm](wp-content/uploads/2014/03/2014-04-jboss-messaging-meme-schema-tables-jbm.jpg)](wp-content/uploads/2014/03/2014-04-jboss-messaging-meme-schema-tables-jbm.jpg) Techniquement, les files JMS et leurs messages sont sauvegardées dans un ensemble de 11 tables, préfixées par le trigramme JBM\_.
Notre objectif est que la source de données dédiée à JBoss Messaging soit la même pour tous les serveurs. Ces tables sont ainsi partagées par l’ensemble des serveurs JBoss.

Sans paramétrage particulier, l’émission simultanée de plusieurs messages JMS à partir de serveurs différents génère les warnings suivants :

```default
2014-03-20 13:02:41,464 WARN [org.jboss.messaging.core.impl.JDBCSupport] (ajp-172.40.24.152-8009-20) SQLException caught,
java.sql.SQLIntegrityConstraintViolationException: ORA-00001: violation de contrainte unique (MYAPPUSER.SYS_C0018809)
at oracle.jdbc.driver.T4CTTIoer.processError(T4CTTIoer.java:439)
...
at org.jboss.messaging.core.impl.JDBCPersistenceManager.cacheID(JDBCPersistenceManager.java:1967)
```

La contrainte d’unicité concerne la table JBM\_ID\_CACHE : les serveurs réservent le même identifiant de message. Pour résoudre ce problème, **chaque serveur doit posséder son propre identifiant [ServerPeerID](https://access.redhat.com/site/documentation/en-US/JBoss_Enterprise_Application_Platform_Common_Criteria_Certification/5/html/JBoss_Messaging_User_Guide/c_configuration.html#sect-Unique_Server_Peer_ID)**.  Cet identifiant est utilisé dans la colonne NODE\_ID des différentes tables de JBoss Messaging.

Ainsi, la table _JBM\_POSTOFFICE_ sera alimentée avec autant de files du même nom qu’il y’a de ServerPeerID (ici 2):
**POSTOFFICE\_NAME****NODE\_ID****QUEUE\_NAME****COND****SELECTOR****CHANNEL\_ID****CLUSTERED****ALL\_NODES****JMS post office**

1

MyAppQueuequeue. MyAppQueue

3

N

N

**JMS post office**

2

MyAppQueuequeue. MyAppQueue

7383

N

N

## Mise en œuvre

Au démarrage du JBoss, nous passons en paramètre l’identifiant du serveur (seul un nombre entier est accepté) :

-Djboss.messaging.ServerPeerID=<identifiant du serveur >

Sous peine de retomber sur l’exception mentionnée ci-dessus, chaque serveur doit avoir un numéro distinct.

Une solution alternative à l’utilisation de la propriété système jboss.messaging.ServerPeerID est de paramétrer le fichier _messaging-service.xml_ de chaque nœud avec le numéro de nœud adéquat.

## Conclusion

En guise de conclusion, voici les avantages de l’architecture présentée dans ce billet :

- Réduction des couts d’administration de base de données : pas de schéma ou d’instance à créer pour chaque nœud du cluster.
- Même configuration pour tous les serveurs :
  - Facilite le déploiement d’un nouveau nœud
  - Réduit les risques de mauvaises configuration

Enfin, avec pour condition préalable que votre base de données soit correctement dimensionnée, le multi-tenancy de JBoss Messaging permet d’aller plus loin en utilisant la même base pour persister des files JMS de serveurs qui font tourner des applications différentes.
