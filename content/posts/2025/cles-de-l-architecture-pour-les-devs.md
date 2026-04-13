---
_edit_last: "1"
_monsterinsights_sitenote_active: ""
_monsterinsights_skip_tracking: ""
author: admin
categories:
  - retour-d'expérience
date: "2025-04-22T17:54:32+00:00"
thumbnail: logo/logo-devoxx-france.png
featureImage: wp-content/uploads/2025/04/word-image-2508-1.jpeg
footnotes: ""
guid: https://javaetmoi.com/?p=2508
parent_post_id: null
post_id: "2508"
post_views_count: "711"
summary: |-
  Conférence : [Devoxx France 2025](https://www.devoxx.fr/)<br>
  Date : 17 avril 2025<br>
  Speakers : [Cyrille Martraire](https://www.linkedin.com/in/martraire/?originalSubdomain=fr) (Arolla), [Eric Le Merdy](https://www.linkedin.com/in/eric-le-merdy-bb60704/?originalSubdomain=fr) (QuickSign) remplaçant de [Christian Sperandio](https://www.linkedin.com/in/christian-sperandio-25182a12) (Arolla)<br>
  Format : Conférence (45mn) / [Replay Youtube](https://www.youtube.com/watch?v=ZoYDxF_7LoI&t=528s)

  Cette conférence a pour **objectif** d’ **ouvrir les portes** en nous donnant les **clés de l’architecture**. Pour seconder Cyrille, Eric a du remplacer Christian au pied levé. <br>
  Un constat est posé. Sur les **dix dernières années**, les **systèmes** ont changé : ils sont devenus **modulaires**, de plus en plus **distribués**. La modularité permise par le Cloud permet de répartir la charge. Il y’a **de** **plus en plus d’interconnexions entre briques applicatives**. <br>
  **L’architecture bouge tout le temps**, évolue constamment. <br>
  ![Cyrille Martraire et Eric Le Merdy sur la scène de Devoxx France 2025](https://javaetmoi.com/wp-content/uploads/2025/04/word-image-2508-1.jpeg)

  Que doit-on savoir ? Pour commencer, on ne saura jamais tout et il faudra vivre avec. Personne ne sait tout. Même le plus capé des architectes.

  Comme fil conducteur, Cyrille et Eric prennent un **exemple réel** issu du monde des **télécommunications**. <br>
  Pour cahier des charges, le client précise que le **système** va **recevoir des fichiers chaque minute** et doit **les intégrer tous les 15mn**. Contexte : ces fichiers viennent d’équipements télécom.
tags:
  - architecture
  - devoxx
title: Les clés de l'architecture pour les dévs
url: /2025/04/cles-de-l-architecture-pour-les-devs/

---
Conférence : [Devoxx France 2025](https://www.devoxx.fr/)  
Date : 17 avril 2025  
Speakers : [Cyrille Martraire](https://www.linkedin.com/in/martraire/?originalSubdomain=fr) (Arolla), [Eric Le Merdy](https://www.linkedin.com/in/eric-le-merdy-bb60704/?originalSubdomain=fr) (QuickSign) remplaçant de [Christian Sperandio](https://www.linkedin.com/in/christian-sperandio-25182a12) (Arolla)  
Format : Conférence (45mn) / [Replay Youtube](https://www.youtube.com/watch?v=ZoYDxF_7LoI&t=528s)

Cette conférence a pour **objectif** d’ **ouvrir les portes** en nous donnant les **clés de l’architecture**. Pour seconder Cyrille, Eric a du remplacer Christian au pied levé.   
Un constat est posé. Sur les **dix dernières années**, les **systèmes** ont changé : ils sont devenus **modulaires**, de plus en plus **distribués**. La modularité permise par le Cloud permet de répartir la charge. Il y’a **de** **plus en plus d’interconnexions entre briques applicatives**.   
**L’architecture bouge tout le temps**, évolue constamment.   

Que doit-on savoir ? Pour commencer, on ne saura jamais tout et il faudra vivre avec. Personne ne sait tout. Même le plus capé des architectes.

Comme fil conducteur, Cyrille et Eric prennent un **exemple réel** issu du monde des **télécommunications**.   
Pour cahier des charges, le client précise que le **système** va **recevoir des fichiers chaque minute** et doit **les intégrer tous les 15mn**. Contexte : ces fichiers viennent d’équipements télécom.

Première question à se poser : « est-ce possible de synchroniser la temporalité ? ».  
Réponse du client : « Non, ce n’est pas possible ».   
La brique centrale est nommée **Aggregator**.   
![Diagramme de contexte C4 du système](wp-content/uploads/2025/04/word-image-2508-2.png)

[Diagramme de contexte C4](https://c4model.com/diagrams/system-context) correspondant :

![ ](wp-content/uploads/2025/04/word-image-2508-3.png " ")

**Première clé** donnée dans ce talk : commencer par **identifier le problème**.   
Comment l’appliquer : quel est le but ? Ici c’est d’agréger les données reçues.   
Cette première clé parait banal : penser problème avant de penser à la solution. Cet adage bien connu s’applique : « un problème bien posé est à moitié une solution ».

Après avoir cerner le problème, on continue en prenant en compte les nombreux [**Software** **Quality Attributes**](https://softwaremill.com/the-importance-of-software-quality-attributes/) dont font partis le cout, la performance, la sécurité ou bien encore le sourcing des dévelopeurs. Liste complète sur [arc42-templates](http://github.com/arc42/arc42-template) et la [FAQ C-1-2](https://faq.arc42.org/questions/C-1-2/).

Examinons à présent les\* contraintes du système.   
1ière contrainte : **disponibilité**  
Toujours Up pour recevoir les données. Calcule de données toutes les 15mn.

2nde contrainte : **performance**  
Le besoin initial mentionnait la réception d’un fichier par minute. En questionnant le métier, on dénombre un fichier par équipement. Sachant qu’il y’a 50 équipements, cela ferait 50 fichiers. Pas tout à fait, puisqu’un équipement compte 40 000 capteurs. Au total, ce sont **6 milliards de données** que le système devra traiter toutes les 15 minutes.   
![Quality Attributes Clusters](wp-content/uploads/2025/04/word-image-2508-4.png)  
La formule de calcul de l’agrégation est compliquée ; ce n’est pas de simples additions.   
Le métier souhaiterait que le calcul soit instantané. Jouant sur le cout financier d’une telle exigence, Eric a réussi à négocier avec le client un temps de traitement de 2 minutes max. Cette durée est acceptable au vu du besoin : anticiper les pannes et remonter des alertes.

**Seconde clé** donnée dans ce talk : **négocier**, **étudier**, **éduquer** les gens.   
Pas nécessaire de mettre systématiquement de la cohérence transactionnelle partout.

Les contraintes techniques nous guident pour définir l’architecture technique. Cette approche n’est pas antinomique avec le **DDD**. Dans notre exemple, il existe une corrélation entre les contraintes techniques et le découpage en sous-domaine.   
On peut identifier **2 sous-domaines** : le parsing lors de l’ingest et le calcul de statistiques.

Une **troisième clé** nous est donnée : **penser modulaire** pour adresser le problème.

Voyons à présent comment implémenter ces 2 sous-domaines.   
On pourrait partir sur 2 services. Mais dans un premier temps, Eric propose de **commencer par seul service**, **plus simple**, **plus facile à implémenter** et livrer. Par contre, afin de préparer un éventuel futur découplage, on utilise l’approche pragmatique de **modular monolith**. Bel exercice de **frugalité** : une solution distribuée est remplacée par un monolith.

![Modular monolith](wp-content/uploads/2025/04/word-image-2508-5.png)

L’architecture se pense à différents niveaux, à plusieurs.   
![Architectural perspectives](wp-content/uploads/2025/04/word-image-2508-6.png)  
Les architectes d’entreprise ont souvent une vue d’ensemble globale. Les développeurs vont quant à eux s’intéresser davantage aux technologies.   
Un conseil, garder en tête cet objectif : bien s’entendre avec tout le monde

Les différents types d’architectures ont leurs avantages et inconvénients. Voici celles qui auraient pu être choisies :

1. **Microservices** : modularité jusqu’au bout
1. **Modular monolith** : facilite le découpage en microservices
1. **Function as a Service**
1. [**Big Ball of Mud**](big%20ball%20of%20mud) : monolith avec archi spaghetti

Parmi les contraintes techniques, le vrai **risque** consiste à tenir le **délai de traitement d’agrégation des données** en dessous des 2 minutes. La première étape consiste à lever ce risque. Il faut lever ce risque et commencer les développements.

![Integration options between modules 1](wp-content/uploads/2025/04/word-image-2508-7.png)

![Integration options between modules 2](wp-content/uploads/2025/04/word-image-2508-8.png)

**Réversible**, l’ **architecture n°2 est retenue** avec une approche **hexagonale**. On reste pragmatique : les deux sous-domaines s’appellent dans la même JVM par appel de fonction. Cyrille rappelle que l’architecture hexagonale demande de créer un peu plus de code, mais ce n’est pas les 30 secondes que met la création d’une interface qui va les ralentir. Cela permet de prévoir des options pas chères pour être réversible et changer son architecture en cours de route. Les décisions sont réversibles.

![ ](wp-content/uploads/2025/04/word-image-2508-9.png " ")

Une première version de l’application est déployée en production. Passent 1mn, puis 2, puis 5. On coupe tout. Trop long. Cela ne marche pas. Cyrille invite à célébrer ce constat : **on sait que çà ne marche pas**. Et on l’a découvert très vite.

La cause est rapidement identifiée : l’agrégateur du monolith est mono-thread. 3 solutions son envisagées :   
**1\. Solution 1** : **mono instance** avec du **multi-threading**. Plus de vCPU, worker pools.   
![](wp-content/uploads/2025/04/word-image-2508-10.png)  
**2\. Solution 2** : **multi instance avec du pub-sub**. Rien à faire. On s’appuie sur un service du Cloud Provider. Clé : on reconnait les problèmes difficiles et on les délègue à du middleware en managé.   
![](wp-content/uploads/2025/04/word-image-2508-11.png)  
**3\. Solution 3** : combine multi-thread et multi-instance : trop compliqué et trop chère. Combine tous les inconvénients. A ne pas faire.

Approche choisie : solution 2. L’architecture est l’art du **tradeoff** (du compromis).

![](wp-content/uploads/2025/04/word-image-2508-12.png)

La solution retenue impose la **fin du modular monolith**. Nécessité de passer en **micro-services** : 2 services, 2 deployments et N services

Réfléchissons à présent sur ce qui pourrait mal se passer avec un **tuyau asynchrone** : messages en double ou triple, manque de ressources, messages perdus …   
![](wp-content/uploads/2025/04/word-image-2508-13.png)  
Le fournisseur de Cloud garantie une partie des problèmes évoqués.   
Cyrille rappelle la nécessité d’un consumer à être **idempotent** pour gérer les messages en double.

![Pubsub architecture tradeoffs](wp-content/uploads/2025/04/word-image-2508-14.png)

Avant de faire un choix sur l’implémentation de l’adaptateur et assurer la persistance des données (ex : PostgreSQL vs Redis), **Eric propose de rester en mémoire pour tester rapidement en prod**. Cela **permet** de gagner du temps et **de** **vérifier les hypothèses**.   
On va livrer en prod un mock. Pas de honte. Vrai essaie sur de vraies machines avec les vraies données. On utilise la prod, le vrai environnement.

![](wp-content/uploads/2025/04/word-image-2508-15.png)  
Le calcul dure moins de 2 minutes : l’hypothèse est validée. L’adaptateur peut désormais être implémenté avec Redis.

Message de fond : **l’architecture est évolutive**. Il ne faut pas la mettre en place dès le début. L’architecture est dynamique. Tout bouge.

L’application est composée de 2 systèmes qui doivent se parler. Un contrat JSON est définit entre dispatcher et aggregator. Le contrat est très explicite avec les unités.   
Cyrille fait remarquer un problème de typo sur un champ : latency **y**\_ms avec 2 lettres y

![ ](wp-content/uploads/2025/04/word-image-2508-16.png " ")

Un renommage serait possible mais il est recommandé de positionner 2 champs pour respecter le contrat.

![](wp-content/uploads/2025/04/word-image-2508-17.png)  
Autre clé : **on ne change pas un contrat**. A partir du moment où il est publié, on doit rester dans la même version majeure pour toujours. Contracts are forever. On ne doit pas casser les clients existants.

Cyrille rappelle les utiles à l’heure de l’IA :   
\- **Architectural Decision Records** (**ADR)** : template   
\- **ArchUnit** : try architecture tests

![](wp-content/uploads/2025/04/word-image-2508-18.png)

Autres clés proposées par Cyrille pour avoir des **réunions constructives**.   
Commencer par **time boxer les réunions**. Utiliser un tableau blanc ou numérique.   
Alterner raisonnement individuel et raisonnement en équipe :

1\. Chacun s’isole pour réfléchir de son côté au même problème   
2\. Chacun vient ensuite expliquer son architecture. On essaie de dépersonnaliser sa solution. Cet exercice permet d’apprendre de ses collègues et de connaitre leurs points d’attention.

**Remember** :

- **The system = the software + the people**
- **Baby steps** : on apprend progressivement, par petits pas, rapidement => réduit le risque dans un monde avec beaucoup d’incertitudes
- **Rester simple**
- **Books** : toutes ces attitudes nécessaires à l’Architecture restent inchangées depuis 30 ans : couplage et cohésion, contrats, modularités, API … Cet apprentissage est pérenne et en vaut donc la peine. Les livres recommandés par Cyrille resteront intemporels.

![3 livres recommandés par Cyrille Martraire](wp-content/uploads/2025/04/word-image-2508-19.png)
