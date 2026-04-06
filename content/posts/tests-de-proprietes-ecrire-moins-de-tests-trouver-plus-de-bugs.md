---
_edit_last: "1"
author: admin
categories:
  - conférence
date: "2020-02-17T16:58:30+00:00"
guid: https://javaetmoi.com/?p=2092
parent_post_id: null
post_id: "2092"
post_views_count: "9197"
summary: |-
  [![](https://javaetmoi.com/wp-content/uploads/2020/02/devfest_paris_2020-300x102.png)](https://javaetmoi.com/wp-content/uploads/2020/02/devfest_paris_2020.png) Lors de l’excellente conférence [**DevFest Paris 2020**](https://devfest.gdgparis.com/) qui s’est tenue le 14 février au Palais des Congrès d’Issy-les-Moulineaux, j’ai découvert une typologie de tests dont je n’avais jamais entendu parler : les **tests de propriétés**(property based tests en anglais).

  Pendant 2h, **[Thomas Haessle](https://twitter.com/Oteku)** (CTO de Cutii) et **[Julien Debon](https://twitter.com/sir4ur0n)** (Tech Lead chez Décathlon) nous ont fait travailler sur un **Code lab** disponible en pas moins de 5 langages de programmation : JavaScript, Java, OCaml, Haskell et Rust. Comme vous vous en doutez, j’ai suivi le lab Java.

  Les quelques slides de leur introduction sont disponibles sur [Google Docs](https://docs.google.com/presentation/d/1bkdvm96-9tPe-ldCVjziDhccV3lzS_DDeFibCQ_cY54/edit#slide=id.g4f013f4ff4_0_20). Le projet GitHub du **lab Troll of Fame** contenant les 5 repos se trouve quant à lui ici : [**trollaklass**](https://github.com/trollaklass)

  Au travers de ce cours billet, je tenais à mettre en avant leur travail et à partager mon enthousiasme. De chez vous, n’hésitez pas à suivre ce Lab pour vous familiariser avec les tests de propriétés. Le [README.md](https://github.com/trollaklass/troll-of-fame-java/blob/master/README.md) contient l’énoncé des 6 étapes et l’explication des concepts associés. Comme son nom l’indique, la **branche** [**solution**](https://github.com/trollaklass/troll-of-fame-java/tree/solution) contient l’ensemble des solutions.
title: 'Tests de propriétés : écrire moins de tests, trouver plus de bugs'
url: /2020/02/tests-de-proprietes-ecrire-moins-de-tests-trouver-plus-de-bugs/

---
[![](/wp-content/uploads/2020/02/devfest_paris_2020.png)](/wp-content/uploads/2020/02/devfest_paris_2020.png) Lors de l’excellente conférence [**DevFest Paris 2020**](https://devfest.gdgparis.com/) qui s’est tenue le 14 février au Palais des Congrès d’Issy-les-Moulineaux, j’ai découvert une typologie de tests dont je n’avais jamais entendu parler : les **tests de propriétés**(property based tests en anglais).

Pendant 2h, **[Thomas Haessle](https://twitter.com/Oteku)** (CTO de Cutii) et **[Julien Debon](https://twitter.com/sir4ur0n)** (Tech Lead chez Décathlon) nous ont fait travailler sur un **Code lab** disponible en pas moins de 5 langages de programmation : JavaScript, Java, OCaml, Haskell et Rust. Comme vous vous en doutez, j’ai suivi le lab Java.

Les quelques slides de leur introduction sont disponibles sur [Google Docs](https://docs.google.com/presentation/d/1bkdvm96-9tPe-ldCVjziDhccV3lzS_DDeFibCQ_cY54/edit#slide=id.g4f013f4ff4_0_20). Le projet GitHub du **lab Troll of Fame** contenant les 5 repos se trouve quant à lui ici : [**trollaklass**](https://github.com/trollaklass)

Au travers de ce cours billet, je tenais à mettre en avant leur travail et à partager mon enthousiasme. De chez vous, n’hésitez pas à suivre ce Lab pour vous familiariser avec les tests de propriétés. Le [README.md](https://github.com/trollaklass/troll-of-fame-java/blob/master/README.md) contient l’énoncé des 6 étapes et l’explication des concepts associés. Comme son nom l’indique, la **branche** [**solution**](https://github.com/trollaklass/troll-of-fame-java/tree/solution) contient l’ensemble des solutions.

## Le concept

Les **tests de propriétés** nous **viennent** des **langages fonctionnels** comme Haskell. Certains ne disposent d’ailleurs que de ce type de test.

Pour nous faire comprendre la différence entre nos tests unitaires habituels et les tests de propriétés (même si de mon point de vue, les tests de propriétés peuvent être considérés comme des tests unitaires), Julien prend l’exemple de la saint Sylvestre.

Pour tester si un jour du calendrier correspond à la St-Sylvestre, un test unitaire comporterait plusieurs scénarios de test avec des dates différentes : 31/12/2020, 31/01/2019, 30/11/2019 … Un test de propriétés accepterait n’importe quelle date et vérifierait le jour et le mois. En effet, quel que soit la date donnée, la St-Sylvestre tombe toujours le 31 décembre, peu importe l’année.

Un [autre exemple](https://pholser.github.io/junit-quickcheck/site/0.9.1/usage/getting-started.html) emprunté sur le site de JUnit Quickcheck consiste à tester un algorithme de chiffrement / déchiffrement à l’aide d’une clé symétrique : quel que soit la clé et le texte à chiffrer, le chiffrement du texte puis le déchiffrement du texte chiffré doit retourner le texte initial.

Les tests de propriétés ne fixent pas les données de tests. Ces derniers sont générés aléatoirement.

Voici une synthèse des différences :
**Tests unitaires****Tests de propriétés**Jeu de données fixeJeu de données aléatoireUne seule exécutionBeaucoup d’exécutionsRègles d’assertion (ex : true, 42, « toto »)Règles d’assertion ou comportement

## Le Lab Troll of Fame

L’objectif du Lab consiste à ajouter des tests de propriétés sur le logiciel Troll of Fame, sachant que tous les TU sont au vert. Certains tests de propriétés vont révéler des bugs d’implémentation qu’il faudra corriger.

Commencez par repo Git [https://github.com/trollaklass/troll-of-fame-java](https://github.com/trollaklass/troll-of-fame-java) puis suivez les instructions du [README.md](https://github.com/trollaklass/troll-of-fame-java/blob/master/README.md).

Les dépendances tirées par le build Gradle build.gradle.kts dévoilent la stack technique utilisée :

- [JUnit](https://junit.org/junit5/) pour les TU
- [AssertJ](https://joel-costigliola.github.io/assertj/) pour les assertions
- [JUnit Quickcheck](https://github.com/pholser/junit-quickcheck) pour les tests de propriétés
- [Lombok](https://projectlombok.org/) pour diminuer le code technique
- [Vavr](https://www.vavr.io/) pour utiliser des structures immuables
- [Google Auto Service](https://github.com/google/auto/tree/master/service) pour détecter les générateurs de paramètres (annotés avec @AutoService) et les mettre à disposition de JUnit Quickcheck

Les 2 classes [ElfGen](https://github.com/trollaklass/troll-of-fame-java/blob/master/src/test/java/ElfGen.java) et [TrollGen](https://github.com/trollaklass/troll-of-fame-java/blob/master/src/test/java/TrollGen.java) seront utilisés par Quickcheck pour générer des **jeux de données aléatoires.**

Par défaut, les tests par propriétés annotés avec l’annotation @com.pholser.junit.quickcheck.Property seront exécutés avec 100 jeux de données différents.

Lorsque le test échoue, un nombre aléatoire d’amorce (radom seed) est généré afin de pouvoir reproduire le cas de test :

```default
TrollProp > invariance FAILED
    java.lang.AssertionError: Property named 'invariance' failed (
    Expecting:
     <0>
    to be greater than or equal to:
     <1> )
    With arguments: [Troll(name=abc, killList=HashMap())]
    Seeds for reproduction: [-8851778975433212269]
        Caused by:
        java.lang.AssertionError:
        Expecting:
         <0>
        to be greater than or equal to:
         <1>

```

Lorsqu’un build Jenkins casse, on peut récupérer le seed.
Lors de TDD, on peut fixer la seed afin d’utiliser dans un premier temps le même jeu de données.

## Conclusion

Les différents exercices du Lab permettent d’implémenter différents tests de propriétés : **invariance**, **inversion**, **analogie**, **idempotence**, **métamorphisme** et **injection**.

L’utilisation de jeux de données aléatoires permet de couvrir davantage de cas de tests. Le **mutation testing** perd de l’intérêt.
De l’aveu de Julien, l’usage de TU reste néanmoins nécessaire pour tester les **cas limites** (ex : division par zéro).

Enfin, l’utilisation d’ **objets immutables**(via Vavr) prend tout son sens avec les tests par propriétés car on compare souvent les objets entre eux, ce qui nécessite de ne pas modifier le jeu de données passé en paramètre.
