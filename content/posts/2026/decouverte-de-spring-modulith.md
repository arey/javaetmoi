---
_edit_last: "1"
_encloseme: "1"
_thumbnail_id: "2677"
_xmlsf_image_featured:
  caption: ""
  loc: https://javaetmoi.com/wp-content/uploads/2026/04/Sans-titre.png
  title: Bannière Spring PetClinic Modulith
author: admin
categories:
  - retour-d'expérience
  - spring
thumbnail: wp-content/uploads/2026/03/logo-spring-modulith.png
featureImage: wp-content/uploads/2026/04/banner-spring-petclinic-modulith.png
featureImageAlt: Bannière Spring PetClinic Modulith
date: "2026-04-06T13:26:43+00:00"
guid: https://javaetmoi.com/?p=2642
parent_post_id: null
post_id: "2642"
toc: true
summary: |-
  En 2025, j’ai eu l’opportunité de mettre en place [**Spring Modulith**](https://spring.io/projects/spring-modulith) sur une nouvelle application web. Pour partager cette expérience avec mes collègues, j’ai préparé une démonstration live montrant comment intégrer Spring Modulith dans une application Spring Boot.

  J’avais besoin pour cela d’une application simple et universelle. Vous commencez à me connaitre : mon choix s’est naturellement porté sur la version canonique de **Spring Petclinic**.

  Pris au jeu, j’ai progressivement enrichi l’application afin d’illustrer plusieurs fonctionnalités clés de Spring Modulith. J’ai ensuite mis ce fork à disposition de la communauté Spring Petclinic dont le code source complet est disponible sur GitHub : [spring-petclinic-modulith](https://github.com/spring-petclinic/spring-petclinic-modulith).

  Dans ce billet, je vous propose de découvrir Spring Modulith, puis de suivre pas à pas comment l’application démo Spring Petclinic a été enrichie pour tirer parti de ses fonctionnalités.

  ![Bannière Spring PetClinic Modulith](wp-content/uploads/2026/04/banner-spring-petclinic-modulith.png)
tags:
  - spring-boot
  - spring-modulith
  - spring-petclinic
title: Découverte de Spring Modulith
url: /2026/04/decouverte-de-spring-modulith/

---
![:left](wp-content/uploads/2026/03/logo-spring-modulith.png)

En 2025, j’ai eu l’opportunité de mettre en place [**Spring Modulith**](https://spring.io/projects/spring-modulith) sur une nouvelle application web. Pour partager cette expérience avec mes collègues, j’ai préparé une démonstration live montrant comment intégrer Spring Modulith dans une application Spring Boot.

J’avais besoin pour cela d’une application simple et universelle. Vous commencez à me connaitre : mon choix s’est naturellement porté sur la version canonique de **Spring Petclinic**.

Pris au jeu, j’ai progressivement enrichi l’application afin d’illustrer plusieurs fonctionnalités clés de Spring Modulith. J’ai ensuite mis ce fork à disposition de la communauté Spring Petclinic dont le code source complet est disponible sur GitHub : [spring-petclinic-modulith](https://github.com/spring-petclinic/spring-petclinic-modulith).

Dans ce billet, je vous propose de découvrir Spring Modulith, puis de suivre pas à pas comment l’application démo Spring Petclinic a été enrichie pour tirer parti de ses fonctionnalités.

{{< figure src="wp-content/uploads/2026/04/illustration-spring-petclinic-modulith-v2.png" alt="Illustre le découpage en modules de l'application Spring Modulith à l'aide de Spring Modulith" caption="Illustre le découpage en modules de l'application Spring Modulith à l'aide de Spring Modulith" >}}

## Architecture modulaire

L'architecture en **microservices** a le vent en poupe depuis une quinzaine d’années. Pourtant, force est de constater que nombre d’applications métiers restent des **monolithes**. Ce n'est pas nécessairement une mauvaise chose. Partir systématiquement d’un monolith avant de l’éclater (ou pas) en microservices est une approche préconisée par de nombreux architectes logiciels (cf. article [Monolith First](https://martinfowler.com/bliki/MonolithFirst.html) de Martin Fowler). Un monolithe bien structuré, celui qu'[Oliver Drotbohm](https://github.com/odrotbohm) (le créateur de Spring Modulith) appelle le **modulith** ou que certains qualifient de **modular monolith**, représente souvent le meilleur compromis entre simplicité opérationnelle et maintenabilité au quotidien. Le projet Spring Modulith permet d’outiller cette approche.

Après plusieurs années de gestation, Spring Modulith a été rendu GA en **août 2023**. Relativement jeune, ce projet apporte un cadre structurant aux applications Spring Boot monolithiques en y introduisant la notion de **modules applicatifs**. Vérification de l'architecture au build, documentation générée automatiquement, communication inter-modules par événements, tests d'intégration ciblés… le tout sans nécessairement d’infrastructure externe.

## Les fonctionnalités de Spring Modulith

Avant de plonger dans le code, prenons un peu de hauteur. Spring Modulith repose sur un principe simple : **chaque sous-package direct du package de la classe principale Spring Boot**(celle annotée avec **_@SpringBootApplication_**) **constitue un module applicatif**. Par convention, le package racine du module expose l'API publique ; tous les sous-packages sont considérés comme privés.

À partir de cette convention d’organisation, Spring Modulith propose un ensemble de fonctionnalités complémentaires :

| **Fonctionnalité** | **Description** |
|---|---|
| **Vérification structurelle** | Lors de la construction de l’application, le test d’architecture `ApplicationModules.verify()` vérifie qu’aucun module n’accède aux packages internes d’un autre module et qu’il n’existe pas de dépendances cycliques. |
| **Communication par événements** | `ApplicationEventPublisher` et `@ApplicationModuleListener` permettent de découpler les modules sans appel direct entre beans Spring. |
| **Registre de publication des événements** | Persiste chaque événement en base de données (table `event_publication`) avant l’exécution du listener, ce qui garantit la livraison des évenements au moins une fois (le _at-least-once delivery_). |
| **Moments** | Publie automatiquement des événements temporels (`DayHasPassed`, `HourHasPassed` …) pour remplacer les `@Scheduled`. |
| **Tests d’intégration modulaires** | `@ApplicationModuleTest` restreint le chargement du contexte Spring Boot au module applicatif testé. L’API `Scenario` orchestre les tests asynchrones. |
| **Documentation** | L’API `Documenter` produit des diagrammes C4 PlantUML et des Application _Module Canvas_ AsciiDoc décrivant l’architecture du code. |
| **Actuator** | La sonde `/actuator/modulith` expose le graphe de modules applicatifs au runtime. |
| **Observabilité** | L’artefact `spring-modulith-observability` instrumente automatiquement les beans exposés et génère des _spans_ Micrometer pour chaque interaction inter-modules. |

La [documentation officielle de Spring Modulith](https:/docs.spring.io/spring-modulith/reference/index.html) est très complète. Je vous encourage à vous y référer. Dans les paragraphes qui suivent, nous allons voir concrètement comment chaque fonctionnalité a été intégrée dans [Spring Petclinic](https://github.com/spring-projects/spring-petclinic), ceci en 11 étapes. Pour rappel, cette application Spring Boot créée en 2003 met en scène une clinique vétérinaire avec ses propriétaires d'animaux, ses vétérinaires et la prise de rendez-vous.

## Étape 1 - Ajouter les dépendances Maven

L’application Spring Petclinic supporte les deux principaux systèmes de build du monde Java : Maven et Gradle. Spring Petclinic Modulith également. Dans ce billet, par simplicité, nous nous focaliserons sur le **build** **Maven**.

Toute intégration de Spring Modulith commence par l' **ajout du BOM** et des premières dépendances. Dans le [pom.xml](https://github.com/spring-petclinic/spring-petclinic-modulith/blob/4.0.0/pom.xml), nous déclarons d'abord la version sous forme de properties (bonne pratique Maven) :


```xml
<spring-modulith.version>2.0.5</spring-modulith.version>
```

La version 2.x de Spring Modulith est compatible Spring Boot 4.

Puis on importe le BOM dans `<dependencyManagement>`:


```xml
<dependencyManagement>
  <dependencies>
    <dependency>
      <groupId>org.springframework.modulith</groupId>
      <artifactId>spring-modulith-bom</artifactId>
      <version>${spring-modulith.version}</version>
      <type>pom</type>
      <scope>import</scope>
    </dependency>
  </dependencies>
</dependencyManagement>
```

Et enfin les dépendances minimales :


```xml
<!-- Annotations et API publique Spring Modulith -->
<dependency>
  <groupId>org.springframework.modulith</groupId>
  <artifactId>spring-modulith-api</artifactId>
</dependency>
<!-- Support JUnit 5 pour la vérification modulaire -->
<dependency>
  <groupId>org.springframework.modulith</groupId>
  <artifactId>spring-modulith-starter-test</artifactId>
  <scope>test</scope>
</dependency>
```

Deux dépendances suffisent pour démarrer. D’autres dépendances seront ajoutées au fil de l'article.

## Étape 2 - Le test de vérification modulaire

C'est le point d'entrée incontournable de Spring Modulith. En quelques lignes, on écrit un test JUnit qui analyse la structure du code et vérifie que les modules respectent leurs frontières :


```java
package org.springframework.samples.petclinic;

import org.junit.jupiter.api.Test;
import org.springframework.modulith.core.ApplicationModules;

class ModularityTests {

    ApplicationModules modules = ApplicationModules.of(PetClinicApplication.class);

    @Test
    void verifiesModularStructure() {
        modules.verify();
    }
}
```

L’appel `ApplicationModules.of(...)` scanne les packages de l'application et construit un modèle en mémoire des modules détectés. L'appel à la méthode `verify() ` s'assure ensuite trois aspects :

1. **Pas de cycle** entre les modules applicatifs
1. **Pas d'accès aux packages internes** d'un module depuis un autre module
1. **Respect des dépendances explicites** (si configurées via l’annotation `@ApplicationModule`)

Si une de ces règles est violée, le test échoue avec un message d'erreur précis. Voici un exemple dans lequel un cycle est détecté :

```text
org.springframework.modulith.core.Violations: - Cycle detected: Slice owner ->
                Slice vet ->
                Slice owner
```

La version Ultimate d’ **IntelliJ IDEA** est packagée avec le **plugin Spring Modulith**. Le support de Spring Modulith permet à IntelliJ de mettre en évidence les utilisations de beans Spring (ou de toute autre classe) qui enfreignent les règles de Spring Modulith. IntelliJ propose de refactoriser le code afin de le rendre conforme à la structure modulaire. Je vous renvoie à la [documentation de cette fonctionnalité](https://www.jetbrains.com/help/idea/spring-modulith.html#apply-the-spring-modulith-guidelines).

## Étape 3 - Identifier les modules applicatifs

Spring Modulith détecte automatiquement les modules à partir des **sous-packages directs** du package contenant la classe main `@SpringBootApplication`. Dans Spring Petclinic, la classe `PetClinicApplication` est localisée au niveau du package **_org.springframework.samples.petclinic_**.

Les modules identifiés étaient à ce stade au nombre de quatre :

| **Module** | **Package racine** |
|---|---|
| owner | `org.springframework.samples.petclinic.owner` |
| vet | `org.springframework.samples.petclinic.vet` |
| system | `org.springframework.samples.petclinic.system` |
| model | `org.springframework.samples.petclinic.model` |

{{< figure src="wp-content/uploads/2026/03/word-image-2642-1.png" alt="" caption="" >}}

Cette modularisation fonctionnelle de l’application Spring Petclinic avait été réalisée en 2016 par Dave Syer dans la PR [#200 Modernize Spring apps structure](https://github.com/spring-projects/spring-petclinic/pull/200). Oliver Drotbohm avait d’ailleurs participé à la conversation.

Le module `model` mutualisait 3 classes de base JPA `BaseEntity`, `Person`, `NamedEntity` partagées entre les modules `owner` et `vet`. Conservé en 2016, 10 ans plus tard à l’heure du Modulith, j’ai préféré reconsidérer ce choix. En effet, en DDD, chaque **Bounded Context** possède intégralement son modèle du domaine métier. Les classes `BaseEntity`, `Person`, `NamedEntity` ne sont pas des concepts métier. Ce sont des raccourcis techniques. Inliner le contenu de ces classes techniques dans `vet` et `owner` rend chaque module prêt pour un éventuel découpage en microservices, sans aucun type partagé. Plutôt que d’être exposé sous forme de module partagé (shared module), le package `model` a été purement et simplement supprimé.

{{< figure src="wp-content/uploads/2026/03/word-image-2642-2.png" alt="" caption="" >}}

## Étape 4- Séparer l'API publique des détails d'implémentation

Spring Modulith attribue un rôle bien défini à chaque package :

1. Le **package racine du module**(ex : `vet/` _)_ expose l'API publique : les types que les autres modules ont le droit d'utiliser
1. Les **sous-packages** (ex : `vet/internal/`) sont considérés comme internes : leur utilisation est interdite depuis les autres modules

Pour chaque module de Spring Petclinic, j'ai donc commencé par déplacer les classes d'implémentation — contrôleurs, repositories, entités JPA dans un sous-package nommé `internal` (nom de package donné par convention, mais tout autre nommage est possible). A ma grande surprise, le package racine de chaque module était vide : les 3 modules étaient parfaitement découplés.

Les classes de test suivent la même organisation. Trivial, ce refactoring peut paraitre déroutant. Il présente pourtant un gain immédiat : on rend explicite ce qui relève de l'API publique du module et ce qui est un détail d'implémentation. Et c'est Spring Modulith qui garantit que cette frontière est respectée via le test `verify()` **_._**

Dans un module applicatif, le développeur est libre d’organiser le code comme il l’entend. Chaque module peut d’ailleurs avoir sa propre organisation : découpage en couches techniques pour l’un, architecture hexagonale pour l’autre.   
 Dans Petclinic, le package `internal` du module `owner` contenait 13 classes à plat. Cela fait beaucoup. On s’éloigne du SRP. J’ai ainsi fait le choix de ventiler ces classes dans 3 packages différents : `ui`, `application` et `domain`.

{{< figure src="wp-content/uploads/2026/03/word-image-2642-3.png" alt="" caption="" >}}

## Étape 5 - Communication par événements entre modules


 La communication par évènements est une fonctionnalité phare de Spring Modulith qu’on peut utiliser en déclarant l’artefact `spring-modulith-events-api` :


```xml
<dependency>
  <groupId>org.springframework.modulith</groupId>
  <artifactId>spring-modulith-events-api</artifactId> </dependency>
```

Pour illustrer ce mécanisme, j'ai ajouté à Spring Petclinic un nouveau cas d’utilisation métier : lorsqu'un rendez-vous est réservé, le système affecte automatiquement le vétérinaire le moins chargé.

{{< figure src="wp-content/uploads/2026/04/screenshot-spring-petclinic-modulith.png" alt="Screenshot of the Veterinarians menu of the Spring Modulith version of Spring Petclinic" caption="Screenshot of the Veterinarians menu of the Spring Modulith version of Spring Petclinic" >}}

Plutôt que d'injecter un bean du module `vet` dans le module `owner`, on remplace l'appel direct d’une méthode par la publication d’un événement applicatif. Lors de la réservation d’un rendez-vous, la classe [VisitScheduler](https://github.com/spring-petclinic/spring-petclinic-modulith/blob/4.0.0/src/main/java/org/springframework/samples/petclinic/owner/application/VisitScheduler.java) utilise la classe `ApplicationEventPublisher` de Spring Framework pour émettre l’évènement [VisitBooked](https://github.com/spring-petclinic/spring-petclinic-modulith/blob/4.0.0/src/main/java/org/springframework/samples/petclinic/owner/VisitBooked.java).


```java
@Transactional
public void bookVisit(Owner owner, Integer petId, Visit visit) {
    Owner managedOwner = owners.findById(owner.getId()).orElseThrow();
    managedOwner.addVisit(petId, visit);
    owners.flush();
    eventPublisher.publishEvent(new VisitBooked(visit.getId(), petId, visit.getDate()));
}
```

Le record [VisitBook](https://github.com/spring-petclinic/spring-petclinic-modulith/blob/4.0.0/src/main/java/org/springframework/samples/petclinic/owner/VisitBooked.java) fait partie de l’ **interface publique** du module `owner`. On le déclare donc au niveau du package racine du module `owner` :


```java
package org.springframework.samples.petclinic.owner;

public record VisitBooked(int visitId, int petId, LocalDate date) {
}
```

La classe [VetEventListener](https://github.com/spring-petclinic/spring-petclinic-modulith/blob/4.0.0/src/main/java/org/springframework/samples/petclinic/vet/internal/VetEventListener.java) du module `vet` réagit à cet événement via l’annotation `@ApplicationModuleListener ` de Spring Modulith :


```java
@Component
class VetEventListener {

    private final VetRoster vetRoster;

    VetEventListener(VetRoster vetRoster) {
       this.vetRoster = vetRoster;
    }

    @ApplicationModuleListener
    void on(VisitBooked event) {
       vetRoster.assignVet(event);
    }
}
```

L'annotation `@ApplicationModuleListener` (source: `spring-modulith-events-api`) est un sucre syntaxique combinant trois annotations en une : `@Async` (source: `spring-context`), **`@Transactional `**(source: `spring-tx`) et **`@TransactionalEventListener `**(source: `spring-tx`). Ce listener s'exécute après le commit de la transaction émettrice, dans une nouvelle transaction, de façon asynchrone. Le module `owner` ne connaît pas le module `vet`. Le découplage est garanti par la structure des packages.

La mise à jour du tableau de garde des vétérinaires est assurée par le service [VetRoster](https://github.com/spring-petclinic/spring-petclinic-modulith/blob/4.0.0/src/main/java/org/springframework/samples/petclinic/vet/internal/VetRoster.java). L'affectation est persistée dans une nouvelle table `visit_assignments` qui appartient conceptuellement au module **_vet_**.


```sql
CREATE TABLE IF NOT EXISTS visit_assignments (
  visit_id   INT  NOT NULL PRIMARY KEY,
  vet_id     INT  NOT NULL REFERENCES vets (id),
  visit_date DATE NOT NULL
);
```

Notez ici un point important : la colonne `visit_id` de cette table est une **référence lâche**, intentionnellement sans clé étrangère vers la table `visits` du module `owner`. C'est le miroir en base de données du découplage Java : le module `vet` ne connaît que l'identifiant publié dans l'événement [VisitBooked](https://github.com/spring-petclinic/spring-petclinic-modulith/blob/4.0.0/src/main/java/org/springframework/samples/petclinic/owner/VisitBooked.java), pas l'entité [Visit](https://github.com/spring-petclinic/spring-petclinic-modulith/blob/4.0.0/src/main/java/org/springframework/samples/petclinic/owner/domain/Visit.java) elle-même. Les modules communiquent par identifiants, pas par références d'objets ni par clés étrangères croisées.

## Étape 6 – Déclarer les dépendances autorisées

Cette étape permet de donner un nom au système et de déclarer explicitement les dépendances inter-modules autorisées. Deux annotations entrent ici en jeu : **`@Modulithic`** et `@ApplicationModule`.

On commencer par annoter la classe main de l’application Petclinic avec **`@Modulithic`**:


```java
@Modulithic(systemName = "PetClinic")
@SpringBootApplication
public class PetClinicApplication { ...}
```

Puis, dans les fichiers `package-info.java` de chaque module, on utilise `@ApplicationModule `:


```java
// owner/package-info.java — aucune dépendance
@ApplicationModule
package org.springframework.samples.petclinic.owner;

// vet/package-info.java — dépend du module owner
@ApplicationModule(allowedDependencies = { "owner" })
package org.springframework.samples.petclinic.vet;

// system/package-info.java — aucune dépendance
@ApplicationModule
package org.springframework.samples.petclinic.system;
```

Ces garde-fous architecturaux sont ici exploités par le [ModularityTests](https://github.com/spring-petclinic/spring-petclinic-modulith/blob/4.0.0/src/test/java/org/springframework/samples/petclinic/ModularityTests.java). Si un développeur (ou un agent de codage) introduit une dépendance non autorisée, le test échoue immédiatement.

## Étape 7 - L'Event Publication Registry

Sans harnais de sécurité, un événement publié mais dont le listener échoue serait perdu à jamais. L'[Event Publication Registry](https://docs.spring.io/spring-modulith/reference/events.html#publication-registry) résout ce problème en persistant chaque événement en base de données **avant** l'exécution du listener.   
 Spring Modulith supporte 4 technologies de persistance : JDBC, JPA, MongoDB et Neo4j.   
 Bien que Spring Petclinic repose sur des repositories Spring Data JPA, j’ai choisi d’exploiter le **support** **JDBC** de Spring Modulith. Compatible JPA, il propose la **propriété `spring.modulith.events.jdbc.schema-initialization.enabled`** permettant de créer la **table `event_publication`**.

La mise en place tient en une dépendance :


```xml
<dependency>
  <groupId>org.springframework.modulith</groupId>
  <artifactId>spring-modulith-starter-jdbc</artifactId>
</dependency>
```

Et trois propriétés dans le fichier de configuration `application.properties` :


```properties
# Crée automatiquement la table event_publication au démarrage
spring.modulith.events.jdbc.schema-initialization.enabled=true

# Supprime les publications complétées immédiatement
spring.modulith.events.completion-mode=DELETE

# Re-publie les événements non traités au redémarrage
spring.modulith.events.republish-outstanding-events-on-restart=true
```

Spring Modulith intercepte chaque appel à `publishEvent() ` et insère une ligne dans la table `event_publication ` au sein de la transaction initiale. Si le listener s'exécute avec succès, l'entrée est supprimée (mode **`DELETE`**). Si le listener échoue ou si l'application crashe, l'entrée reste en base et sera rejouée au redémarrage de Petclinic. Cette garantie _at-least-once delivery_ fonctionne sans infrastructure externe : pas besoin de Kafka, de RabbitMQ ni de quelconque broker de messages. Un simple SGBD relationnel suffit.

## Étape 8 - Moments : les événements temporels


 Spring Modulith propose un module **`spring-modulith-moment` s** qui publie automatiquement des événements marquant le passage du temps : **`HourHasPassed`**, **`DayHasPassed`**, **`WeekHasPassed`**, etc. C'est une alternative élégante aux classiques **`@Scheduled `** de Spring.

Sur notre application, le module vet utilise l’évènement **`DayHasPassed`** pour nettoyer quotidiennement les affectations aux vétérinaires dont la date est passée. Dans la classe [VetEventListener](https://github.com/spring-petclinic/spring-petclinic-modulith/blob/4.0.0/src/main/java/org/springframework/samples/petclinic/vet/internal/VetEventListener.java), on déclare une seconde méthode :


```java
@EventListener
void on(DayHasPassed event) {
    vetRoster.cleanupPastAssignments(event.getDate());
}
```

Notez l'utilisation de l’annotation Spring Framework `@EventListener `(et non `@ApplicationModuleListener`) : l'événement **`DayHasPassed`** est publié par Spring Modulith lui-même en dehors de toute transaction applicative.

## Étape 9 - Tests d'intégration modulaires

La modularité apportée par Spring Modulith présente un autre avantage : sa capacité à **bootstrapper un seul module** en isolation. L'annotation `@ApplicationModuleTest ` remplace ainsi **`@SpringBootTest`** et ne charge que le contexte application Spring nécessaire au module dans lequel le test se trouve. En théorie, le temps d’exécution du test devrait être amélioré.

Exemple d’utilisation sur le test **[VisitSchedulerTests](https://github.com/spring-petclinic/spring-petclinic-modulith/blob/4.0.0/src/test/java/org/springframework/samples/petclinic/owner/application/VisitSchedulerTests.java)** :


```java
@ApplicationModuleTest
class VisitSchedulerTests {

    @Autowired
    OwnerRepository owners;

    @Autowired
    VisitScheduler visitScheduler;

    @Test
    void bookVisitShouldPublishVisitBookedEvent(Scenario scenario) {
       // Given
       Owner owner = owners.findById(1).orElseThrow();
       Pet pet = owner.getPets().iterator().next();
       Visit visit = new Visit();
       visit.setDescription("Annual checkup");

       // When / Then
       scenario.stimulate(() -> visitScheduler.bookVisit(owner, pet.getId(), visit))
          .andWaitForEventOfType(VisitBooked.class)
          .matching(event -> event.petId() == pet.getId())
          .toArriveAndVerify(event -> then(event.petId()).isEqualTo(pet.getId()));
    }

}
```

Notez ici l’utilisation de l' **API Scenario** de Spring Modulith Test. On définit un stimulus (l'appel à `bookVisit`), on déclare l'événement attendu ([VisitBooked](https://github.com/spring-petclinic/spring-petclinic-modulith/blob/4.0.0/src/main/java/org/springframework/samples/petclinic/owner/VisitBooked.java)), on pose un critère de correspondance ( _matching_) et on vérifie. Le tout de manière fluide.

Les logs d’exécution du test donnent un aperçu des beans Spring chargés par `@ApplicationModuleTest` :

```text
Bootstrapping @org.springframework.modulith.test.ApplicationModuleTest for Owner in mode STANDALONE (class org.springframework.samples.petclinic.PetClinicApplication)…

\# Owner  
\> Logical name: owner  
\> Base package: org.springframework.samples.petclinic.owner  
\> Excluded packages: none  
\> Direct module dependencies: none  
\> Spring beans:  
 o ….application.VisitScheduler  
 o ….domain.OwnerRepository  
 o ….domain.PetTypeRepository  
 o ….ui.OwnerController  
 o ….ui.PetController  
 o ….ui.PetTypeFormatter  
 o ….ui.VisitController
```

 Appartenant au module system, la classe de test existante [CrashControllerIntegrationTests](https://github.com/spring-petclinic/spring-petclinic-modulith/blob/main/src/test/java/org/springframework/samples/petclinic/system/internal/CrashControllerIntegrationTests.java) a pu bénéficier de l’annotation `@ApplicationModuleTest`.   
 Contrairement à `@SpringBootTest`, `@ApplicationModuleTest` n’expose pas d’attribut `properties`. Cette limitation a pu être contournée grâce à l’annotation `TestPropertySource` de Spring Test.


```java
// Avant
@SpringBootTest(webEnvironment = RANDOM_PORT,
       properties = { "spring.web.error.include-message=ALWAYS", "management.endpoints.access.default=none" })
@AutoConfigureTestRestTemplate
class CrashControllerIntegrationTests {

// Après
@ApplicationModuleTest(webEnvironment = RANDOM_PORT)
@TestPropertySource(
       properties = { "spring.web.error.include-message=ALWAYS", "management.endpoints.access.default=none" })
@AutoConfigureTestRestTemplate
class CrashControllerIntegrationTests {
```

Contrairement à ce dont on pouvait s’attendre, le temps d’exécution a légèrement augmenté, passant en moyenne de 500 à 520 ms. La détection des beans du module explique sans doute cet overhead. A vérifier sur d’autres testes, dans d’autres applications plus conséquentes.

## Étape 10 - Génération de documentation

Spring Modulith permet de générer automatiquement de la documentation à partir du modèle de modules. Il suffit d’ajouter l’artefact **`spring-modulith-docs`** dans le `pom.xml` puis d'enrichir notre classe [ModularityTests](https://github.com/spring-petclinic/spring-petclinic-modulith/blob/4.0.0/src/test/java/org/springframework/samples/petclinic/ModularityTests.java) :


```java
@Test
void writeDocumentation() {
    new Documenter(modules).writeDocumentation();
}
```

L'appel à `writeDocumentation() ` produit dans le répertoire `target/spring-modulith-docs/` :

1. Des **diagrammes C4 au format PlantUML** ( _.puml_) représentant les relations entre modules
1. Des « **modules Canvas » au format AsciiDoc** ( _.adoc_) listant pour chaque module : les beans Spring exposés (non visible sur Petclinic) ainsi que les événements publiés et écoutés
1. Un **document de synthèse** ( _all-docs.adoc_) agrégeant l'ensemble des diagrammes et canvas  

Exemple de rendu du fichier `module-vet.puml `:

{{< figure src="wp-content/uploads/2026/03/word-image-2642-4.png" alt="" caption="" >}}



Exemple de rendu du fichier `module-vet.adoc `:   
![](wp-content/uploads/2026/03/word-image-2642-5.png)

L'intérêt de cette living documentation est double : le rendu de l’architecture du code est rendu sous nos yeux et la documentation reste synchronisée avec le code sans effort supplémentaire.


Cela dit, dans une application d’entreprise, je vous recommande de ne pas regénérer systématiquement la doc à chaque exécution du build Maven, mais à la demande lorsque vous (ou votre agent IA) avez besoin de publier ou consulter la doc.

# Étape 11 - l'endpoint Actuator

Cette dernière étape consiste exposer le graphe de modules au runtime. Deux dépendances Maven sont nécessaires :


```xml
<dependency>
  <groupId>org.springframework.modulith</groupId>
  <artifactId>spring-modulith-actuator</artifactId>
  <scope>runtime</scope>
</dependency>
<dependency>
  <groupId>org.springframework.modulith</groupId>
  <artifactId>spring-modulith-runtime</artifactId>
  <scope>runtime</scope>
</dependency>
```

Un appel GET sur l’URL `http://localhost:8080/actuator/modulith ` renvoie le graphe complet des modules au format JSON : noms, packages et dépendances. Cette sonde est pratique pour visualiser l'architecture de l’application déployée sans avoir besoin d'aller regarder le code ou la documentation. En production, pensez néanmoins à désactiver ou sécuriser cet actuator.


```json
{
  "owner": {
    "displayName": "Owner",
    "basePackage": "org.springframework.samples.petclinic.owner",
    "nested": [],
    "type": "closed",
    "shared": false,
    "namedInterfaces": {
      "<<UNNAMED>>": [
        "org.springframework.samples.petclinic.owner.VisitBooked"
      ]
    },
    "initializers": [],
    "dependencies": []
  },
  "system": {
    "displayName": "System",
    "basePackage": "org.springframework.samples.petclinic.system",
    "nested": [],
    "type": "closed",
    "shared": false,
    "namedInterfaces": {
      "<<UNNAMED>>": []
    },
    "initializers": [],
    "dependencies": []
  },
  "vet": {
    "displayName": "Vet",
    "basePackage": "org.springframework.samples.petclinic.vet",
    "nested": [],
    "type": "closed",
    "shared": false,
    "namedInterfaces": {
      "<<UNNAMED>>": []
    },
    "initializers": [],
    "allowedDependencies": [
      "owner"
    ],
    "dependencies": [
      {
        "target": "owner",
        "types": [
          "EVENT_LISTENER"
        ]
      }
    ]
  }
}
```


## Conclusion

Vous l’aurez vu : **intégrer Spring Modulith** dans **Spring Petclinic** s'est fait **facilement** et de manière très **progressive**. Un projet d’entreprise n’exploitera pas nécessairement toutes les fonctionnalités présentées dans cet article. Seules les étapes 1 à 5 sont obligatoires. Le fait de pouvoir ouvrir certains sous-packages à d’autres modules permet d’intégrer Spring Modulith dans des applications legacy, le temps de refactorer le code. D’expérience **, le plus simple consiste néanmoins à intégrer Spring Modulith dès la mise en œuvre de l’architecture logicielle d’un nouveau monolith modulaire**.

Les 3 modules initiaux de Spring Petclinic étant isolés et indépendants, l’interface publique exposée par chaque module au travers son package racine ne présentait que peu d’intérêt. L’ajout de la fonctionnalité d’affectation automatique d’un vétérinaire à un futur rendez-vous aura permis de montrer comment faire communiquer 2 modules à l’aide d ' **évènements** puis de montrer comment utiliser l’ **Event Publication Registry**. La base de données existante aura été réutilisée, facilitant son adoption (nul besoin d’infrastructure externe).

Ayant encore peu d’expérience avec Spring Modulith, je suis ouvert à toute proposition d’amélioration. Le code source du fork Spring Petclinic Modulith est disponible sur repo GitHub : [spring-petclinic-modulith](https://github.com/spring-petclinic/spring-petclinic-modulith). Tous les changements apportés sont visibles à travers [**cet unique commit**](https://github.com/spring-petclinic/spring-petclinic-modulith/commit/512e6b5b41857f85dfa30f77f84a48e81dd1338f). N'hésitez pas à l’étudier, à expérimenter et à soumettre vos contributions à travers des issues et de Pull Requests.

**Ressources**

- [spring-petclinic-modulith](https://github.com/spring-petclinic/spring-petclinic-modulith) : le code source complet de la démo
- [Documentation officielle de Spring Modulith](https://docs.spring.io/spring-modulith/reference/index.html)
- [Spring Modulith examples](https://github.com/spring-projects/spring-modulith/tree/main/spring-modulith-examples) : les exemples fournis par l'équipe Spring
- [Guide to Modulith with Spring Boot](https://piotrminkowski.com/2023/10/13/guide-to-modulith-with-spring-boot/) : article de blog de Piotr Mińkowski datant de 2023
- [spring-modulith-with-ddd](https://github.com/xsreality/spring-modulith-with-ddd) : code source d’une application Modular Monolith basée sur Spring Modulith et le Domain Driven Design
- [Migrating to Modular Monolith using Spring Modulith and IntelliJ IDEA](https:/blog.jetbrains.com/idea/2026/02/migrating-to-modular-monolith-using-spring-modulith-and-intellij-idea)
- [Monolith First](https://martinfowler.com/bliki/MonolithFirst.html) : article de Martin Fowler datant de 2015  
