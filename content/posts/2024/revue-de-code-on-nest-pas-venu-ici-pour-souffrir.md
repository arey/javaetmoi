---
_edit_last: "1"
author: admin
categories:
  - conférence
date: "2024-05-03T13:15:02+00:00"
toc: true
thumbnail: wp-content/uploads/2024/05/image.png
featureImage: wp-content/uploads/2024/05/image.png
guid: https://javaetmoi.com/?p=2356
parent_post_id: null
post_id: "2356"
post_views_count: "6988"
summary: |-
  <br>Conférence : [Devoxx France 2024](https://www.devoxx.fr/)<br>Vidéo Youtube : [https://www.youtube.com/watch?v=KeM1cjKiMr4](https://www.youtube.com/watch?v=KeM1cjKiMr4)<br>Date : 18 avril 2024<br>Speakerines : [Pauline Rambaud](https://twitter.com/@pauinegu) et [Anne-Laure de Boissieu](https://twitter.com/AnneLaure2B) (Bedrock Streaming)<br>Format : Conférence (45mn)

  Déjà donnée à plusieurs reprises dans différents meetups et conférences, Pauline et Anne-Laure ont repensé spécialement cette présentation pour Devoxx France. Quel honneur !

  Afin de démontrer à l’assistance qu’un commentaire laissé dans une **revue de code** peut amener de la **confusion**, nos deux speakerines commencent leur show en nous montrant **une Pull Request** sur le repo git de leurs slides reveal : une simple émoticône. Mal interprétée, elle entraine un **biais de communication**.

  ## C’est quoi la revue de code ?

  Développeuses GO, Anne-Laure et Pauline rappellent que **la revue de code fait partie intégrante du métier de développeur**. Elle consiste à examiner le code écrit par un autre développeur afin d'en améliorer la qualité, détecter les bugs et s'assurer du respect des normes de codage. Il existe différents types de revue. Au cours de cette présentation, elles se focaliseront sur les revues centrées sur le delta du code écrit pour corriger bug ou implémenter une feature.

  ![](https://javaetmoi.com/wp-content/uploads/2024/05/word-image-2356-1.jpeg)
tags:
  - craft
  - devoxx
title: Revue de code, on n’est pas venu-e-s ici pour souffrir !
url: /2024/05/revue-de-code-on-nest-pas-venu-ici-pour-souffrir/

---
  
Conférence : [Devoxx France 2024](https://www.devoxx.fr/)  
Vidéo Youtube : [https://www.youtube.com/watch?v=KeM1cjKiMr4](https://www.youtube.com/watch?v=KeM1cjKiMr4)  
Date : 18 avril 2024  
Speakerines : [Pauline Rambaud](https://twitter.com/@pauinegu) et [Anne-Laure de Boissieu](https://twitter.com/AnneLaure2B) (Bedrock Streaming)  
Format : Conférence (45mn)

Déjà donnée à plusieurs reprises dans différents meetups et conférences, Pauline et Anne-Laure ont repensé spécialement cette présentation pour Devoxx France. Quel honneur !

Afin de démontrer à l’assistance qu’un commentaire laissé dans une **revue de code** peut amener de la **confusion**, nos deux speakerines commencent leur show en nous montrant **une Pull Request** sur le repo git de leurs slides reveal : une simple émoticône. Mal interprétée, elle entraine un **biais de communication**.

## C’est quoi la revue de code ?

Développeuses GO, Anne-Laure et Pauline rappellent que **la revue de code fait partie intégrante du métier de développeur**. Elle consiste à examiner le code écrit par un autre développeur afin d'en améliorer la qualité, détecter les bugs et s'assurer du respect des normes de codage. Il existe différents types de revue. Au cours de cette présentation, elles se focaliseront sur les revues centrées sur le delta du code écrit pour corriger bug ou implémenter une feature.

![](wp-content/uploads/2024/05/word-image-2356-1.jpeg)

## Intérêts d’une revue de code

- Obtenir une meilleure **qualité de code**
- Rechercher et **corriger des bugs** au plus tôt
- **Partager** de la **connaissance**
- **Partager** la **responsabilité** : si bug, faute de l’équipe et pas du dév
- **Se former** en continue : on apprend des autres et on fait grandir l’équipe  

Il existe d’autres formats que les revues asynchrones via Pull Request : le **MOB programming**, le **Pair Programming** ou même pas de revue de code. A chaque équipe de choisir.

## Pas de raison apparente de souffrir ?

Contrastant avec tous les bénéfices évoqués, les revues peuvent néanmoins faire souffrir auteurs et relecteurs à cause d’ **incompréhensions** et de **maladresses**. Dans certaines situations, les commentaires et les retours s’accumulent, on se retrouve submerger et on n’arrive pas à les prendre en compte.

## Bonnes pratiques plus efficaces

Apportant peu de valeur ajoutée, certaines catégories de commentaires pourraient être détectés et écrits par des robots. Les erreurs de formatage en sont un exemple flagrant. Utiliser un **outil** comme un **linter** et un **formateur** fait gagner du temps aux relecteurs humains. De la même manière, les anomalies évidentes de code et les anti-patterns communs peuvent être détectés automatiquement par des outils d’analyse statique de code comme **SonarLint**. Ces outils sont **intégrables** **à la** **CI**.

Autre bonne pratique : mettre à disposition de la **documentation** pour les nouveaux arrivants. Utile pour l’ **onboarding**, elle doit expliquer les pratiques mises en œuvre sur le projet ou dans l’entreprise.   

## Template de Pull Request

Créer un **modèle de template pour les Pull Request** (PR) permet de faciliter la création d’une demande de changement et donner du contexte aux reviewers. GitHub et GitLab proposent cette fonctionnalité. Elle permet au développeur de se poser les questions essentielles à la bonne délimitation de sa PR. Dans le template, on peut retrouver les questions des [Five W's](https://fr.wikipedia.org/wiki/QQOQCCP) mais également la référence à la User Story implémentée (ex : lien Jira).  

![ ](wp-content/uploads/2024/05/image.png " ")

##   
Definition of Done de la PR

Avant de soumettre une Pull Request, une bonne pratique consiste à vérifier **la checklist de Definition of Done des PR**. Voici quelques exemples de points à contrôler :

- Tests unitaires écrits
- Code testé fonctionnement à la main via la UI
- Code propre exempt de TODO et de code commenté
- …

Vérifier tous ces points fera gagner du temps aux relecteurs et permet d’anticiper d’éventuels retours.

## Definition of Reviewed

Sur le même principe, un relecteur de code peut suivre une checklist :

- Je commente uniquement si besoin (et pas pour le fun)
- J’envoie tous mes retours en une seule fois (fonctionnalité de « batch comment »)
- Je vérifie que le code est testé
- Je teste une fois sur un tenant

Pour approfondir le sujet, je vous renvoie à mon billet [Check-list revue de code Java](/2015/08/check-list-revue-code-et-architecture-java/).

## Conventional comments

**Certains commentaires sont sujets à interprétation** : « Ce n’est pas clair », « Pourquoi tu as fait çà comme çà ? », « Oh my Gosh », « Poubelle », « Je n’aurais pas fait çà comme çà » …   
 L’utilisation d’ **emoji** n’aide pas toujours à en faciliter l’interprétation. Par exemple, d’une génération à l’autre, certaines emojis n’ont pas le même sens.

Les **commentaires interrogatifs** sont multi-interprétables. Dans l’exemple « Pourquoi tu as fait çà comme çà ? », on ne sait pas s’il s’agit d’une vraie question visant à progresser ou s’il s’agit d’une moquerie.

Pour se prémunir de ces incompréhensions, il parait nécessaire de **standardiser les commentaires de revue de code** en utilisant, par exemple, l’approche des [**Conventional Comments**](https://conventionalcomments.org/) fortement inspiré des [Conventional Commits](https://www.conventionalcommits.org/).   
 Les conventional comments proposent **de formatter ses commentaires** de commit en suivant ce formalisme :

```xml
<label> [decorations]: <subject>[discussion]
```

**Décorations** et **discussions** sont **optionnels**.

L’utilisation de **libellés** (label) permet de donner son intention :

**praise:**

Les **éloges** soulignent un élément positif. Essayez de laisser au moins un de ces commentaires par revue de code. Ne laissez pas de fausses louanges (qui peuvent en fait être préjudiciables). Cherchez à être **sincère**. Second degré interdit.

**nitpick:**

Les « nitpicks » sont des **demandes de changements triviaux**. Elles ne devraient pas être bloquantes.

**suggestion:**

Les suggestions **proposent des** **améliorations**. Il est important d'être **explicite** et **clair** sur ce qui est suggéré et **pourquoi** il s'agit d'une amélioration. Envisagez d'utiliser les décorations bloquantes ou non bloquantes pour mieux communiquer votre intention.

**issue:**

Les **problèmes** mettent en évidence des **dysfonctionnements** du code examiné. **Bloquants** par nature, ces problèmes peuvent affecter directement la fonctionnalité implémentée ou introduire une régression ailleurs. Il est fortement recommandé d'associer un problème à une suggestion de correction. Si vous n'êtes pas certain de l'existence d'un problème, posez une question pour clarifier la situation.

**question:**

Les **questions** sont pertinentes si vous avez un **doute potentiel** sur le code, même s'il n'est pas clair s'il s'agit d'un vrai problème. Demander à l'auteur de **clarifier certains points** ou de **mener une investigation** plus poussée peut permettre une résolution rapide.

**thought:**

Des **réflexions** représentent des **idées** qui ont émergé lors de l'examen du code. Ces commentaires **ne bloquent pas** l'avancement de la Pull Request. Cependant, ils peuvent être très précieux car ils **peuvent mener à des initiatives plus ciblées** ou à des opportunités de **mentorat**.

**chore:**

Les **corvées** représentent des **tâches simples** qui **doivent être effectuées** avant que la Pull Request puisse être "officiellement" acceptée. En général, ces commentaires font référence à un processus standard. Essayez de fournir un lien vers la description du processus pour que l'auteur puisse savoir comment résoudre la corvée.

Pauline et Anne-Laure nous invitent à sélectionner un **sous-ensemble** de ces libellés et même à les **personnaliser**. A titre d’exemple, elles-mêmes utilisent **applause** à la place de **praise**. Elles n’utilisent pas thought et chore mais ont introduit 2 autres notations : **todo** et **typo**.   
Pour standardiser les revues et faciliter la vue des nouveaux arrivants, elles mettent à disposition de leurs équipes un **markdown** avec les libellés et les emojis associés :   
![](wp-content/uploads/2024/05/word-image-2356-2.png)

![ ](wp-content/uploads/2024/05/word-image-2356-3.jpeg " ")

Les **commentaires conventionnels de commit** permettent de moins souffrir grâce à :

- Une compréhension facilitée
- Une meilleure lisibilité grâce aux labels
- Moins de mauvaises impressions sur le ton employé
- Moins de perte de temps

Ils permettent d’éviter ce type de commentaire inutile : « On pourrait être plus efficace »

Afin d’éviter de spammer la Pull Request, lorsqu’une même erreur de typographie est détectée plusieurs fois, Anne-Laure et Pauline recommandent de créer un seul commentaire référençant toutes les lignes où l’erreur apparait.

Pour terminer sur les commentaires de PR, voici quelques bonnes pratiques :

- Le mentoring paie : cela fait progresser les dévs et l’équipe récoltera le fruit de ce travail
- Laisser des commentaires exploitables fait gagner en efficacité
- Combiner les commentaires similaires
- Utiliser le « Nous » plutôt que le « Tu »
- Remplacer le « Nous devons » par « Nous pourrions »  

Toute grande organisation dispose de ses propres règles de revue de code. C’est par exemple le cas de Google qui les publie sur GitHub : [Google Engineering Practices Documentation](https://google.github.io/eng-practices/).

## L’attitude avant tout

Dans la catégorie du « commentaire difficile à exploiter », on retrouve :

- « Je t’ai déjà dit 2 fois qu’il ne fallait pas faire ça comme çà »
- « Ce n’est pas très élégant »
- « Beuh »

Non aidant, ces commentaires questionnent sur l’attitude qu’un relecteur doit adopter.

Une attitude bienveillante et constructive est un pré-requis à la communication asynchrone.   
Théorisée en 1971 par Gerald Weinbert, la [**Programmation sans ego**](https://fr.wikipedia.org/wiki/Programmation_sans_ego) (ergoless programming) reste d’actualités. Elle vise à ce que notre égo ait le moins d’impact. On minimise les facteurs personnels et on émet des critiques respectueuses.

Quelques principes clés de Gerald Weinbert :

- Comprenez et acceptez que vous faites des erreurs. C’est formateur. Traitez les autres comme vous aimeriez qu’on vous traite.
- **Vous n’êtes pas votre code**. Se détacher de son code permet d’accepter des critiques sur le code.
- Ne réécrivez pas le code de l’autre sans consultation : vous n’aiderez pas le dév qui l’a écrit, et cela est très frustrant de voir son code réécrit.
- Traiter les personnes avec respect, considération et patience. Le risque est que les personnes ne fassent pas de retour et n’osent pas s’exprimer.
- Battez-vous pour ce en quoi vous croyez, mais acceptez la défaite avec grâce. Lorsque votre solution / proposition est rejetée par l’équipe, ne pas prendre la mouche. Se dire que sa solution était bonne, mais que l’équipe a décidé d’en prendre une autre. Egoless ne veut pas dire sans égo.
- **Critiquez le code, pas les personnes**

## Que retenir ?

- Tenter de moins laisser notre ego nous contrôler
- Faisons preuve d’empathie
- C’est en groupe qu’on produit les meilleures choses

Dans certaines équipes, personne ne fait de revue de code. La revue de code est un muscle. Il faut s’entrainer et le faire travailler. Alors lancez-vous et entrainez-vous !

Les débutants ne savent peut-être pas toujours comment s’y prendre, d’autant plus lorsqu’ils sont amenés à revoir du code de développeurs plus senior. Pour les aider, il faut absolument éviter de réécrire le code à leur place, laisser des commentaires plus constructifs et faire part d’empathie (on a tous été junior).

Pratiques à essayer :

- Organiser un vis ma vie : permet de voir comment le tech lead fait ses retours de PR
- Animer un MOB programming autour des revues
- Proposer une méthode et découper le travail ensemble
- Expliquer et discuter ensemble
- Accepter le temps passé à relire

Après toutes ces recommandations, arriverez-vous à la conclusion qu’on ne peut plus rien dire dans une revue ? Et bien non ! Les **feedbacks négatifs** sont nécessaires pour :

- Améliorer la qualité du code
- Garantir sa maintenabilité
- Prévenir les risques de bug

Lorsqu’aucun label n’est associé à un commentaire, on peut se demander si ce commentaire va être exploitable ? Peut-être que ce commentaire n’a pas lieu d’être, du moins à l’écrit.   
 En cas de **conflits**, parlons-en ailleurs que dans une PR. La PR ne doit pas être le lieu de gestion des conflits.

**Ne restons pas en souffrance.** Lorsqu’un dév souffre, il n’est souvent pas le seul. Il est nécessaire d’en discuter avec d’autres dévs.   
Améliorer la revue de code, c’est avant tout se poser des questions et améliorer l’équipe   
