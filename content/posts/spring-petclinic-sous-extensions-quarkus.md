---
_edit_last: "1"
_monsterinsights_sitenote_active: ""
_monsterinsights_skip_tracking: ""
author: admin
categories:
  - retour-d'expérience
  - spring
date: "2025-04-13T16:55:14+00:00"
footnotes: ""
guid: https://javaetmoi.com/?p=2443
parent_post_id: null
post_id: "2443"
post_views_count: "770"
summary: "Spring et Quarkus dans le même repository Git, ou presque. Cela vous intrigue ? {{ double-space-with-newline }}Figurez-vous qu’il y’a quelques mois, la lecture du très bon **livre [Understanding Quarkus 2.x](https://agoncal.teachable.com/p/ebook-understanding-quarkus)** d’Antonio Gongalves m’a donné envie de pratiquer ce framework alternatif à Spring Boot. Et pour apprendre une nouvelle technologie, quoi de plus stimulant que de se fixer un objectif. Je me suis donc donné comme challenge de migrer vers Quarkus l’application démo Spring Boot que je connais bien. Une fois migrée, l’application devait rester **iso-fonctionnelle**. {{ double-space-with-newline }}A travers leur repo [quarkus-petclinic](https://github.com/redhat-developer-demos/quarkus-petclinic), RedHat avait fait l’exercice avant moi. Malheureusement, l’historique Git a été écrasé, ne laissant aucune trace du chemin de migration parcouru. Pendant 3 mois, j'ai donc travaillé sur un nouveau fork que je suis fier de vous présenter : [**quarkus-spring-petclinic**](https://github.com/arey/quarkus-spring-petclinic). Ajouté à la communauté Spring Petclinic, ce fork a un double objectif :\n\n1. Montrer comment **migrer une application Spring Boot 3.4 vers Quarkus 3.21**, avec le minium d'effort et en modifiant le moins de code possible\n2. Utiliser les **extensions Spring** proposées par **Quarkus** pour garder un lien avec le monde Spring tout en soulignant l'effort de l'équipe Quarkus pour supporter Spring, un framework incontournable de l'écosystème Java\n\nLes **extensions Spring pour Quarkus** utilisées sont au nombre de quatre : **Spring DI**, **Spring Web**, **Spring Data JPA** et **Spring Cache**.{{ double-space-with-newline }}Le changement majeur aura été de porter le templating des pages HTML de **Thymeleaf** vers **Qute**.\n\nDébutant en Quarkus, le code proposé ne respecte peut-être pas toutes les règles de l’art prônées par l’équipe de dév Quarkus. Je m’en excuse par avance. Si vous voulez contribuer et corriger le tir : [issue](https://github.com/spring-petclinic/quarkus-spring-petclinic/issues) et [Pull Request](https://github.com/spring-petclinic/quarkus-spring-petclinic/pulls) sont les bienvenues.\n\n \n\nLe [différenciel complet](https://github.com/spring-petclinic/quarkus-spring-petclinic/compare/spring-boot-version...v3.21.0) entre la version Spring Boot et la version Quarkus de Petclinic peut-être visualisé sur Github."
tags:
  - quarkus
  - spring-boot
title: Spring Petclinic sous extensions Quarkus
url: /2025/04/spring-petclinic-sous-extensions-quarkus/

---
Spring et Quarkus dans le même repository Git, ou presque. Cela vous intrigue ?   
Figurez-vous qu’il y’a quelques mois, la lecture du très bon **livre [Understanding Quarkus 2.x](https://agoncal.teachable.com/p/ebook-understanding-quarkus)** d’Antonio Gongalves m’a donné envie de pratiquer ce framework alternatif à Spring Boot. Et pour apprendre une nouvelle technologie, quoi de plus stimulant que de se fixer un objectif. Je me suis donc donné comme challenge de migrer vers Quarkus l’application démo Spring Boot que je connais bien. Une fois migrée, l’application devait rester **iso-fonctionnelle**.   
A travers leur repo [quarkus-petclinic](https://github.com/redhat-developer-demos/quarkus-petclinic), RedHat avait fait l’exercice avant moi. Malheureusement, l’historique Git a été écrasé, ne laissant aucune trace du chemin de migration parcouru. Pendant 3 mois, j'ai donc travaillé sur un nouveau fork que je suis fier de vous présenter : [**quarkus-spring-petclinic**](https://github.com/arey/quarkus-spring-petclinic). Ajouté à la communauté Spring Petclinic, ce fork a un double objectif :

1. Montrer comment **migrer une application Spring Boot 3.4 vers Quarkus 3.21**, avec le minium d'effort et en modifiant le moins de code possible
1. Utiliser les **extensions Spring** proposées par **Quarkus** pour garder un lien avec le monde Spring tout en soulignant l'effort de l'équipe Quarkus pour supporter Spring, un framework incontournable de l'écosystème Java

Les **extensions Spring pour Quarkus** utilisées sont au nombre de quatre : **Spring DI**, **Spring Web**, **Spring Data JPA** et **Spring Cache**.  
Le changement majeur aura été de porter le templating des pages HTML de **Thymeleaf** vers **Qute**.

Débutant en Quarkus, le code proposé ne respecte peut-être pas toutes les règles de l’art prônées par l’équipe de dév Quarkus. Je m’en excuse par avance. Si vous voulez contribuer et corriger le tir : [issue](https://github.com/spring-petclinic/quarkus-spring-petclinic/issues) et [Pull Request](https://github.com/spring-petclinic/quarkus-spring-petclinic/pulls) sont les bienvenues.

{{< figure src="/wp-content/uploads/2025/04/word-image-2443-1.png" alt="" caption="" >}}

Le [différenciel complet](https://github.com/spring-petclinic/quarkus-spring-petclinic/compare/spring-boot-version...v3.21.0) entre la version Spring Boot et la version Quarkus de Petclinic peut-être visualisé sur Github.

## Configuration du build Maven et Gradle

Spring Petclinic supporte les 2 principales plateformes de **build** de l’ecosystème Java, à savoir **Maven** et **Gradle**. Pour chaque dépendance Spring Boot, le tableau ci-dessous dresse l’équivalent utilisé sur la version Quarkus :

| **Dépendances Spring Boot**      | **Dépendances Quarkus correspondantes**                                             | **Commentaire**                                                                                                                                                                                  |
|----------------------------------|-------------------------------------------------------------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `spring-boot-starter-actuator`   | `quarkus-smallrye-health`                                                           | [SmallRye Health](https://github.com/smallrye/smallrye-health/) est une implementation de la [MicroProfile Health](https://github.com/eclipse/microprofile-health/).                             |
| `spring-boot-starter-cache`      | `cache-api`<br>`caffeine`<br>`quarkus-spring-cache`                                 | Extension Spring Cache pour Quarkus<br>Quarkus utilise par défaut Caffeine.                                                                                                                      |
| `spring-boot-starter-data-jpa`   | `quarkus-spring-data-jpa`<br>`quarkus-narayana-jta`                                 | Extension Spring Data JPA pour Quarkus<br>Quarkus s’appuie sur Hibernate ORM et Panache. Le gestionnaire de transactions JTA est à ajouter manuellement.                                         |
| `spring-boot-starter-web`        | `quarkus-spring-web`<br>`quarkus-rest-jackson`                                      | L’extension Spring Web pour Quarkus requère quarkus-rest-jackson ou quarkus-resteasy-jackson.                                                                                                    |
| `spring-boot-starter-validation` | `quarkus-hibernate-validator`                                                       | Les versions Spring Boot et Quarkus de Petclinic s’appuient toutes 2 sur Hibernate Validator.                                                                                                    |
| `spring-boot-starter-thymeleaf`  | `quarkus-qute`                                                                      | Pas de correspondance directe car Quarkus utilise Qute pour le templating.                                                                                                                       |
| `spring-boot-starter-test`       | `quarkus-junit5`<br>`quarkus-junit5-mockito`<br>`quarkus-test-h2`<br>`rest-assured` | Rest Assured remplace MockMvc pour tester les contrôleurs REST.                                                                                                                                  |
| `h2`                             | `quarkus-jdbc-h2`                                                                   |                                                                                                                                                                                                  |
| `mysql-connector-j`              | `quarkus-jdbc-mysql`                                                                | En plus des drivers JDBC, tire le pool de connexions Agroal qui remplace HikariCP.                                                                                                               |
| `postgresql`                     | `quarkus-jdbc-postgresql`                                                           |                                                                                                                                                                                                  |
| `webjars-locator-lite`           | `quarkus-web-dependency-locator`                                                    | Utiles pour les webjars.                                                                                                                                                                         |
| `spring-boot-devtools`           |                                                                                     | Pas de correspondance directe. Quarkus inclue le mode dev par défaut.                                                                                                                            |
| `spring-boot-docker-compose`     |                                                                                     | Utilisé par les tests d’intégration reposant sur Testcontainers.<br>Pas d’équivalent côté Quarkus qui sait nativement démarrer des conteneurs Docker lorsqu’aucune configuration n’est précisée. |
| `(spring-core et spring-beans)`  | `quarkus-spring-di`                                                                 | Support des annotations Spring d’injection de dépendance, mais en tirant ArC, une implémentation light de CDI spécifique à Quarkus.                                                              |
|                                  | `quarkus-container-image-docker`                                                    | Création d’images Docker multi-plateformes.                                                                                                                                                      |

Les dépendances vers les 2 **webjars** **bootstrap** et **font-awesome** sont restés inchangées.  
La migration a été faite avec une approche top-down : on part de la couche persistance pour remonter vers la couche de présentation.

## Adaptation de la couche Spring Data JPA

L’ [extension Spring Data JPA](https://quarkus.io/guides/spring-data-jpa) pour Quarkus présente l’avantage de pouvoir conserver les **conventions de nommage des interfaces des repository Spring Data JPA**. Sous le capot, l’implémentation est générée à l’aide de **[Panache](https://quarkus.io/guides/hibernate-orm-panache)**. Les repository migrés peuvent continuer à implémenter les interfaces **JpaRepository** et **ListCrudRepository**, à utiliser les interfaces Spring Data **Page** et **Pageable** pour la pagination.

Ce portage a permis de conserver 90% du code existant de la couche de persistance de Spring Petclinic. Je l’ai personnellement trouvé plus strict que l’original. Preuve en est ce premier exemple possible avec Spring Data JPA, mais qui ne fonctionne pas sous Quakus : déclarer sur l’interface OwnerRepository la méthode findPetTypes manipulant des entités JPA de type PetType et non de type Owner.  
L’erreur suivante était générée pendant le build :

> ```
> Query annotations may only use interfaces to map results to non-entity types. Offending query string is "SELECT ptype FROM PetType ptype ORDER BY ptype.name" on method findPetTypes of Repository org.springframework.samples.petclinic.owner.OwnerRepository
> ```
>
> Les messages d’erreur ne sont pas explicites. Aussi, pour debugger et trouver la cause, j’ai eu besoin d’ajouter temporairement la dépendance suivante :

```xml
<dependency>
  <groupId>io.quarkus</groupId>
  <artifactId>quarkus-spring-data-jpa-deployment</artifactId>
</dependency>
```

Le moyen de contournement a consisté tout simplement à découper en deux l’interface [OwnerRepository](https://github.com/spring-petclinic/quarkus-spring-petclinic/blame/v3.21.0/src/main/java/org/springframework/samples/petclinic/owner/OwnerRepository.java). L’interface [PetTypeRepository](https://github.com/spring-petclinic/quarkus-spring-petclinic/blob/v3.21.0/src/main/java/org/springframework/samples/petclinic/owner/PetTypeRepository.java) a été ajoutée et a pour responsabilité l'accès aux PetType. On a ainsi un meilleur découplage.

Second cas dysfonctionnant sous Quarkus :

```java
public interface VetRepository extends Repository<Vet, Integer> {
	Collection<Vet> findAll();
}
```

Quarkus génère l’exception suivante :

```text
Caused by: io.quarkus.spring.data.deployment.UnableToParseMethodException: Method 'findAll' of repository 'org.springframework.samples.petclinic.vet.VetRepository' cannot be parsed as there is no proper 'By' clause in the name.
```

La classe [**MethodNameParser**](https://github.com/quarkusio/quarkus/blob/main/extensions/spring-data-jpa/deployment/src/main/java/io/quarkus/spring/data/deployment/MethodNameParser.java) **ne supporte pas** le type de retour **Collection**. Triviale, la correction a consisté à le changer en **List**.

Dernier changement mineur apporté à la couche de persistance : l’exception non checkée **DataAccessException** n’est pas supportée par Quarkus. Elle a donc été retirée de l’interface des méthodes des Repository.

Une fois migrée, l’interface [OwnerRepository](https://github.com/spring-petclinic/quarkus-spring-petclinic/blob/v3.21.0/src/main/java/org/springframework/samples/petclinic/owner/OwnerRepository.java) n’a aucune adhérence à Quarkus ou Panache. Elle conserve ses **imports** sur les classes de **Spring Data Commons** et **Spring Data JPA** :

```java
package org.springframework.samples.petclinic.owner;

import java.util.Optional;

import jakarta.annotation.Nonnull;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.jpa.repository.JpaRepository;

public interface OwnerRepository extends JpaRepository<Owner, Integer> {

	Page<Owner> findByLastNameStartingWith(String lastName, Pageable pageable);

	Optional<Owner> findById(@Nonnull Integer id);

	Page<Owner> findAll(Pageable pageable);
```

## Adaptation des scripts SQL

Migrer les Repository Spring Data JPA, c’est bien. Les tester, c’est mieux. Les tests unitaires de Quarkus Spring Petclinic utilisent la base de données embarquées H2.   
L’exécution du script [data.sql](https://github.com/spring-petclinic/quarkus-spring-petclinic/blob/v3.21.0/src/main/resources/db/h2/data.sql) échouait avec l’erreur suivante :

```text
Caused by: org.h2.jdbc.JdbcSQLIntegrityConstraintViolationException: Intégrité référentielle violation de contrainte: "FK35UIBOYRPFN1BNDRR5JORCJ0M: PUBLIC.VET_SPECIALTIES FOREIGN KEY(SPECIALTY_ID) REFERENCES PUBLIC.SPECIALTIES(ID) (4)"
Referential integrity constraint violation: "FK35UIBOYRPFN1BNDRR5JORCJ0M: PUBLIC.VET_SPECIALTIES FOREIGN KEY(SPECIALTY_ID) REFERENCES PUBLIC.SPECIALTIES(ID) (4)"; SQL statement:
INSERT INTO vet_specialties VALUES (4, 2) [23506-230]
```

Cette différence de comportement s’explique par le fait que Quarkus utilise Hibernate pour générer le script DDL de création du schéma et non pas directement le script DDL [schema.sql](https://github.com/spring-petclinic/quarkus-spring-petclinic/blob/v3.21.0/src/main/resources/db/h2/schema.sql). L’ordre des colonnes diffère entre le script DDL généré par Hibernate et le script SQL existant. Je n’ai pas trouvé la possibilité d’utiliser le script schema.sql. [Je ne suis apparemment pas le seul](https://github.com/quarkusio/quarkus/discussions/30193). Si vous avez une idée, vous pouvez contribuer à l’ [issue #8](https://github.com/spring-petclinic/quarkus-spring-petclinic/issues/8).

En attendant de trouver une solution, j’ai modifié le script SQL en précisant le nom des colonnes dans l’instruction INSERT, ce qui est une bonne pratique :

{{< figure src="/wp-content/uploads/2025/04/word-image-2443-2.png" alt="" caption="" >}}

## Portage des tests AssertJ vers Hamcrest

Pour les tests unitaires, Quarkus recommande l’utilisation de **JUnit 5** déjà utilisé sur Spring Petclinic. Les assertions de JUnit sont limitées. Là où Spring Petclinic utilise la librairie [AssertJ](https://assertj.github.io/doc/), Quarkus préconise l’utilisation d’ [H **amcrest**](https://hamcrest.org/JavaHamcrest/). D’après l’ [issue #38689](https://github.com/quarkusio/quarkus/issues/38689) “Include AssertJ with Quarkus releases”, le support d’AssertJ dans Quarlus ne semble pas planifié.

Migrer des assertions AssertJ vers les matchers Hamcrest peut être facilitée par la recette Open Rewrite [MigrateHamcrestToAssertJ](https://docs.openrewrite.org/recipes/java/testing/hamcrest/migratehamcresttoassertj). L’inverse n’est pas vrai. C’est là où Github Copilot ou Codeium facilite la tâche. On migre un premier test, et l’IA vous assiste pour la suite.

Exemple avec la méthode shouldFindSingleOwnerWithPet() extrait de la classe [ClinicServiceTests](https://github.com/spring-petclinic/quarkus-spring-petclinic/blob/v3.21.0/src/test/java/org/springframework/samples/petclinic/service/ClinicServiceTests.java):

Avant migration sous AssertJ :

```java
@Test
void shouldFindSingleOwnerWithPet() {
	Optional<Owner> optionalOwner = this.owners.findById(1);
	assertThat(optionalOwner).isPresent();
	Owner owner = optionalOwner.get();
	assertThat(owner.getLastName()).startsWith("Franklin");
	assertThat(owner.getPets()).hasSize(1);
	assertThat(owner.getPets().get(0).getType()).isNotNull();
	assertThat(owner.getPets().get(0).getType().getName()).isEqualTo("cat");
}
```

Après migration sous Hamcrest :

```java
@Test
void shouldFindSingleOwnerWithPet() {
	Optional<Owner> optionalOwner = this.owners.findById(1);
	assertThat(optionalOwner.isPresent(), is(true));
	Owner owner = optionalOwner.get();
	assertThat(owner.getLastName(), startsWith("Franklin"));
	assertThat(owner.getPets(), hasSize(1));
	assertThat(owner.getPets().get(0).getType(), notNullValue());
	assertThat(owner.getPets().get(0).getType().getName(), is(equalTo("cat")));
}
```

## Passer à l’annotation @TestTransaction

Dans les classes de tests faisant appels à des Repository, l’annotation org.springframework.transaction.annotation.Transactional du module spring-tx a été remplacée par **io.quarkus.test.TestTransaction** du module quarkus-test-commons. Ces annotations permettent de rollbacker la transaction à la fin de l’exécution d’une méthode de test, laissant ainsi la base de données inchangée pour le prochain test.

Exemple avec la méthode _shouldInsertOwner()_ extrait de la classe [ClinicServiceTests](https://github.com/spring-petclinic/quarkus-spring-petclinic/blob/v3.21.0/src/test/java/org/springframework/samples/petclinic/service/ClinicServiceTests.java):

```java
@Test
@TestTransaction
void shouldInsertOwner() {
	Page<Owner> owners = this.owners.findByLastNameStartingWith("Schultz", pageable);
	int found = (int) owners.getTotalElements();

	Owner owner = new Owner();
	owner.setFirstName("Sam");
	owner.setLastName("Schultz");
	owner.setAddress("4, Evans Street");
	owner.setCity("Wollongong");
	owner.setTelephone("4444444444");
	this.owners.save(owner);
	assertThat(owner.getId(), is(not(0)));

	owners = this.owners.findByLastNameStartingWith("Schultz", pageable);
	assertThat(owners.getTotalElements(), is(equalTo(found + 1L)));
}
```

## De DataJpaTest à QuarkusTest

Pour tester les Repository JPA, Spring Boot met à disposition l’annotation **@DataJpaTest** automatisant la configuration des classes de test. Elle s’occupe notamment de démarrer en mémoire une base de données embarquée H2, de créer son schéma et de charger un jeu de données de test.

Pour arriver à un résultat similaire avec Quarkus, l’annotation @DataJpaTest a été remplacée par 2 annotations :

```java
@QuarkusTest
@QuarkusTestResource(H2DatabaseTestResource.class)
class ClinicServiceTests {
```

L’annotation @ **QuarkusTestResource** permet de référencer la classe **H2DatabaseTestResource** (fournie par l’artefact **io.quarkus:quarkus-test-h2**) chargée de démarrer / arrêter un serveur H2.

Par défaut, l’application Spring Petclinic démarre une base de données H2, la même que celle utilisée pour les tests. La propriété **quarkus.hibernate-orm.sql-load-script** du fichier [application.properties](https://github.com/spring-petclinic/quarkus-spring-petclinic/blob/v3.21.0/src/main/resources/application.properties) a été positionnée sur **h2** :

```properties
quarkus.datasource.db-kind=h2
quarkus.hibernate-orm.log.sql=true
quarkus.hibernate-orm.sql-load-script=db/${quarkus.datasource.db-kind}/data.sql
```

La propriété **quarkus.hibernate-orm.sql-load-script** a quant à elle permis de réutiliser le script DML existant [data.sql](https://github.com/spring-petclinic/quarkus-spring-petclinic/blob/v3.21.0/src/main/resources/db/h2/data.sql) insérant quelques **données de test**.

A ce stade de la migration vers Quarkus, les tests unitaires de la couche de persistance et de la couche service sont passants.

## Internationalisation

Le support de l’internationalisation ( **i18n** pour les intimes) est incomplet dans Spring Petclinic (cf. issue [#1854](https://github.com/spring-projects/spring-petclinic/issues/1854)). Le **ressource bundle** [**messages**](https://github.com/spring-petclinic/quarkus-spring-petclinic/tree/v3.21.0/src/main/resources/messages) contient différent fichiers properties de traduction. Les clés sont utilisées dans certains templates Thymeleaf (ex : welcome) et pour les messages d’erreur (ex : required, typeMismatch.birthDate). Ce ressource bundle a pu être réutilisé dans la version Quarkus.

Qute propose un [**mécanisme typesafe de ressource bundle**](https://quarkus.io/guides/qute-reference#type-safe-message-bundles) basé sur l’annotation **@ResourceBundle**. La classe [AppMessages](https://github.com/spring-petclinic/quarkus-spring-petclinic/blob/v3.21.0/src/main/java/org/springframework/samples/petclinic/system/AppMessages.java) a été ajoutée à Petclinic. En voici un extrait contenant 3 clés :

```java
import io.quarkus.qute.i18n.Message;
import io.quarkus.qute.i18n.MessageBundle;

@MessageBundle(value = "messages", locale = "en")
public interface AppMessages {

  @Message
  String welcome();

	@Message
	String required();

	@Message
	String typeMismatch_birthDate();
```

Le nom des clés des properties ne semble pas accepter le **caractère point** (ex : _@Message(value = "typeMismatch.birthDate"_). Certaines clés ont donc dû être renommées (ex : _typeMismatch.birthDate_ vers _typeMismatch\_birthDate_).

Au runtime, l’usage du ressource bundle Quarkus peut-être utilisé dans un template Qute via le namespace du message bundle. Exemple :

```html
 {#for err in errors}
  {#if err == 'notFound'}
    <p>{messages:notFound}</p>
  {#else}
    <p>{err}</p>
  {/if}
{/for}
```

Ce même ressource bundle peut également être exploité depuis un contrôleur REST. La création de classe [I18nHelper](https://github.com/spring-petclinic/quarkus-spring-petclinic/blob/v3.21.0/src/main/java/org/springframework/samples/petclinic/system/I18nHelper.java) permet d’exploiter dynamiquement l’en-tête HTTP **Accept-Language** :

```java
@GetMapping("/")
public TemplateInstance processFindForm(@RequestParam(defaultValue = "1") int page, @RequestParam String lastName,
		@HeaderParam("Accept-Language") String language) {
	Page<Owner> ownersResults = findPaginatedForOwnersLastName(page, lastName);

if (ownersResults.isEmpty()) {
	// no owners found
	String notFound = I18nHelper.lookupAppMessages(language).notFound();
	return OwnerTemplates.findOwners(List.of(notFound));
}
```

Possible que Quarkus propose nativement un mécanisme similaire. [Quarkus Renarde](https://docs.quarkiverse.io/quarkus-renarde/dev/advanced.html#localisation) utilise quant à lui le header Accept-Language et un cookie.

En passant, l’exemple précédent montre l’usage des **annotations Spring @GetMapping** et **@RequestParam**. L’annotation Spring **@RequestHeader** n’est pas supportée par Quarkus et a dû être substituée par l’annotation **@HeaderParam** de JAX-RS.

Le debuggage de la méthode MessageBundleProcessor:: **parseKeyToTemplateFromLocalizedFile** aura nécessité d’ajouter temporairement au classpath la dépendance io.quarkus:quarkus-qute-deployment.

## Ressources statiques

Afin de se conforter aux conventions de Quarkus, les ressources statiques (fonts, css et images) ont été **déplacées** du répertoire static/resources vers le **répertoire META-INF/resources**.

## Migration templates Thymeleaf vers Qute

Les templates Thymeleaf de Spring Petclinic utilisent le mécanisme **de fragments Thymeleaf** à la fois pour le **gabarit** **des pages** (layout.html) et pour les **tags HTML** réutilisables (inputField.html et selectField.html).

Une première étape a donc consisté à migrer ces fragments Thymeleaf vers une équivalence Qute. La syntaxe de ces 2 moteurs de templating Java diffère beaucoup. A l’aide du [guide de référence de Qute](https://quarkus.io/guides/qute-reference), le gabarit des pages layout.html a été migré sans difficulté majeure. La gestion dynamique du menu est désormais gérée en JavaScript. Ce gabarit est référencé dans les autres templates Qute via la [section {#include fragments/layout}](https://quarkus.io/guides/qute-reference#include_helper).

Template Thymeleaf de la page welcome originale :

```html
<!DOCTYPE html>
<html xmlns:th="https://www.thymeleaf.org" th:replace="~{fragments/layout :: layout (~{::body},'home')}">
  <body>
    <h2 th:text="#{welcome}">Welcome</h2>
    <div class="row">
        <div class="col-md-12">
          <img class="img-responsive" src="../static/resources/images/pets.png" th:src="@{/resources/images/pets.png}"/>
        </div>
    </div>
  </body>
</html>
```

Template Qute équivalent de la page welcome :

```html
{#include fragments/layout}
  <body>
    <h2>{messages:welcome}</h2>
    <div class="row">
        <div class="col-md-12">
          <img class="img-responsive" src="/images/pets.png" />
        </div>
    </div>
  </body>
{/include}
```

Afin d’être enregistrés automatiquement par Quarkus, les [**user-defined tags**](https://quarkus.io/guides/qute-reference#user_tags) **input** et **select** ont été déplacés dans le **répertoire src/main/resources/templates/tags**. Les 2 exemples de tags suivants permettent de comparer les syntaxes Thymeleaf et Qute.

Exemple du tag Thymeleaf inputField.html :

```html
<html>
<body>
  <form>
    <th:block th:fragment="input (label, name, type)">
      <div th:with="valid=${!#fields.hasErrors(name)}"
        th:class="${'form-group' + (valid ? '' : ' has-error')}"
        class="form-group">
        <label class="col-sm-2 control-label" th:text="${label}">Label</label>
        <div class="col-sm-10">
            <div th:switch="${type}">
                <input th:case="'text'" class="form-control" type="text" th:field="*{__${name}__}" />
                <input th:case="'date'" class="form-control" type="date" th:field="*{__${name}__}"/>
            </div>
          <span th:if="${valid}"
            class="fa fa-ok form-control-feedback"
            aria-hidden="true"></span>
          <th:block th:if="${!valid}">
            <span
              class="fa fa-remove form-control-feedback"
              aria-hidden="true"></span>
            <span class="help-inline" th:errors="*{__${name}__}">Error</span>
          </th:block>
        </div>
      </div>
    </th:block>
  </form>
</body>
</html>
```

Exemple équivalent du tag Qute inputField.html :

```javascript
 {#let invalid=result.hasErrors(name)}
      <div class="form-group {#if invalid} has-error {/if}">
        <label for="{name}" class="col-sm-2 control-label">{it}
        </label>
        <div class="col-sm-10">
          <input class="form-control" id="{name}" name="{name}" type="{type}" value="{field}" />
          <span class="fa {#if invalid}fa-remove{#else}fa-ok{/if} form-control-feedback" aria-hidden="true"></span>
          {#if invalid}
            <span class="help-inline">{result.getErrorMessage(name)}</span>
          {/if}
        </div>
      </div>
{/let}
```

## Binding du modèle

Une fois les templates Thymeleaf converties en Qute, des ajustements ont été nécessaire du côté des contrôleurs web, notamment au niveau du **binding des champs du formulaire**. Le binding est le processus par lequel les données envoyées par l’utilisateur, généralement via un formulaire, sont automatiquement associées à un objet du modèle. Spring Web MVC gère le binding en utilisant des **DataBinder** qui convertissent automatiquement les paramètres de requête HTTP en propriétés d’un objet Java, en s’appuyant sur les noms des champs du formulaire et les conventions de nommage. Dans l’exemple suivant, la méthode _processCreationForm_ accepte en paramètre un objet de type Owner bindé avec les champs du formulaire [createOrUpdateOwnerForm.html](https://github.com/spring-projects/spring-petclinic/blob/main/src/main/resources/templates/owners/createOrUpdateOwnerForm.html) :

```java
@PostMapping("/owners/new")
public String processCreationForm(@Valid Owner owner, BindingResult result, RedirectAttributes redirectAttributes) {
```

Positionnée sur le paramtètre owner, l’annotation **@Valid** permet d’exécuter la validation **Bean Validation / Hibernate Validator**. Je n’ai pas trouvé dans Quarkus l’équivalent des classes **BindingResult** et **RedirectAttibutes**. Ainsi, la signature de cette méthode s’allège en Quarkus :

```java
@PostMapping("/owners/new")
public TemplateInstance processCreationForm(Owner owner) {
```

On retrouve l’annotation Spring **@PostMapping** supportée par l’extension Quarkus. Le type de retour n’est plus une String correspondant à la vue MVC à afficher, mais une **TemplateInstance**.

Pour binder la classe Owner, un changement a dû être opéré au niveau de la classe [Owner](https://github.com/spring-petclinic/quarkus-spring-petclinic/blob/v3.21.0/src/main/java/org/springframework/samples/petclinic/owner/Owner.java) et de ses classes parentes [Person](https://github.com/spring-petclinic/quarkus-spring-petclinic/blob/v3.21.0/src/main/java/org/springframework/samples/petclinic/model/Person.java) et [NamedEntity](https://github.com/spring-petclinic/quarkus-spring-petclinic/blob/v3.21.0/src/main/java/org/springframework/samples/petclinic/model/NamedEntity.java) : **ajouter l’annotation JAX-RS @FormParam** sur les attributs bindés comme address. Extrait de la classe [Owner](https://github.com/spring-petclinic/quarkus-spring-petclinic/blob/v3.21.0/src/main/java/org/springframework/samples/petclinic/owner/Owner.java) :

```java
public class Owner extends Person {

	@Column(name = "address")
	@NotBlank
	@FormParam("address")
	private String address;
```

Sans ce changement, voici le message d’erreur obtenu lors de la création d’un nouveau propriétaire d’animal de compagnie :

```text
2025-04-12 17:36:04,095 ERROR [org.spr.sam.pet.sys.ExceptionMappers] (executor-thread-1) Internal server error: jakarta.ws.rs.NotSupportedException: HTTP 415 Unsupported Media Type
        at org.jboss.resteasy.reactive.server.handlers.RequestDeserializeHandler.handle(RequestDeserializeHandler.java:75)
```

Ce ciblage explicite des champs bindés depuis un formulaire HTML pourrait être justifié par des mesures de sécurité.

Pour terminer sur le binding du modèle, l’interface **org.springframework.ui.Model** est conservée dans quarkus-spring-context-api mais [ne semble pas être exploitée par Quarkus](https://github.com/search?q=org%3Aquarkusio%20ModelMap&type=code).

## Validation des données

Dans le paragraphe précédent, nous avons vu comment récupérer de manière typée les données saisies par l’utilisateur dans l’interface web de Petclinic. Nous allons voir à présent comment il est possible de **valider les données** avant de les insérer en base de données.

Le guide [Validation with Hibernate Validator](https://quarkus.io/guides/validation#a-frontend) explique comment mettre en place Bean Validation sur une API REST. L’annotation **@jakarta.validation.Valid** est supportée par Quakus. Pour autant, son usage n’a pas pu être conservé dans Petclinic. En effet, si on la laisse, Quarkus valide les données du Owner et, en cas d’erreur, ne rentre pas dans la méthode _processCreationForm_. Il renvoie directement un flux texte contenant le rapport d’erreur complet. Exemple de la soumission d’un formulaire vide :

```text
ViolationReport{title='Constraint Violation', status=400, violations=[Violation{field='processCreationForm.owner.address', message='ne doit pas être vide'}, Violation{field='processCreationForm.owner.telephone', message='ne doit pas être vide'}, Violation{field='processCreationForm.owner.telephone', message='Telephone must be a 10-digit number'}, Violation{field='processCreationForm.owner.city', message='ne doit pas être vide'}, Violation{field='processCreationForm.owner.lastName', message='ne doit pas être vide'}, Violation{field='processCreationForm.owner.firstName', message='ne doit pas être vide'}]}
```

Dans Petclinic, on souhaite renvoyer le formulaire HTML en erreur avec le message d’erreur à côté de chaque champ erroné.

Dans la documentation Quakus Qute, je n’ai pas trouvé l’équivalent de ce que propose Spring Web MVC, grâce notamment à la classe **BindingResult**. Pour contourner cette limitation, j’ai introduit le record [**Result**](https://github.com/spring-petclinic/quarkus-spring-petclinic/blob/v3.21.0/src/main/java/org/springframework/samples/petclinic/system/Result.java). L’appel au **Validator** Bean Validation est fait de manière impérative. Son résultat (un ensemble de ConstraintViolation) permet de construire une instance de Result.

Exemple en Spring :

```java
@PostMapping("/owners/new")
public String processCreationForm(@Valid Owner owner, BindingResult result, RedirectAttributes redirectAttributes) {
	if (result.hasErrors()) {
		redirectAttributes.addFlashAttribute("error", "There was an error in creating the owner.");
		return VIEWS_OWNER_CREATE_OR_UPDATE_FORM;
	}

	this.owners.save(owner);
	redirectAttributes.addFlashAttribute("message", "New Owner Created");
	return "redirect:/owners/" + owner.getId();
}
```

Exemple équivalent en Quarkus :

```java
@PostMapping("/new")
public TemplateInstance processCreationForm(Owner owner) {
	Result result = Result.from(validator.validate(owner));
	if (result.hasErrors()) {
		return OwnerTemplates.createOrUpdateOwnerForm(owner, result);
	}

	this.owners.save(owner);
	return OwnerTemplates.ownerDetails(owner, Result.success("New Owner Created"));
}
```

Noter l’appel à la méthode **OwnerTemplates::ownerDetails()** dont nous allons étudier le fonctionnement dans le paragraphe suivant.

A noter également un écart de fonctionnement entre les versions Spring Boot et Quarkus de Petclinic : lors de la soumission d’un formulaire (POST), la version Spring utilise une **redirection http** pour rediriger l’utilisateur sur l’URL de consultation (GET). Nativement, Quarkus et Qute ne supportent pas ce fonctionnement. Pour être iso-fonctionnel, il aurait fallu utiliser [Quarkus Renarde qui supporte les redirections](https://docs.quarkiverse.io/quarkus-renarde/1.x/index.html#_redirects_after_post) et le [scope flash](https://docs.quarkiverse.io/quarkus-renarde/1.x/index.html#_flash_scope).

Enfin, dans la version Spring, la classe [PetValidator](https://github.com/spring-projects/spring-petclinic/blob/main/src/main/java/org/springframework/samples/petclinic/owner/PetValidator.java) assure la validation des champs obligatoires name, type et birthDate. Dans la version Quarkus, cette classe a été supprimée au profit de l’utilisation de l'annotations **@NotNull** ajoutée sur classe Pet et du support de Bean Validation.

## Templates Qute type-safe

Dans la version Quarkus de Petclinic, on note l’introduction de 3 nouvelles classes annotées chacune avec **@CheckedTemplate :** [OwnerTemplates](https://github.com/spring-petclinic/quarkus-spring-petclinic/blob/v3.21.0/src/main/java/org/springframework/samples/petclinic/owner/OwnerTemplates.java), [PetTemplates](https://github.com/spring-petclinic/quarkus-spring-petclinic/blob/v3.21.0/src/main/java/org/springframework/samples/petclinic/owner/PetTemplates.java) et [VetTemplates](https://github.com/spring-petclinic/quarkus-spring-petclinic/blob/v3.21.0/src/main/java/org/springframework/samples/petclinic/vet/VetTemplates.java). Appelées depuis les contrôleurs REST, leurs méthodes natives permettent de sélectionner le template à rendre, ceci de manière type-safe. Exemple de la classe [OwnerTemplates](https://github.com/spring-petclinic/quarkus-spring-petclinic/blob/v3.21.0/src/main/java/org/springframework/samples/petclinic/owner/OwnerTemplates.java) :

```java
@CheckedTemplate(basePath = "owners")
public class OwnerTemplates {

	public static native TemplateInstance findOwners(List<String> errors);

	public static native TemplateInstance ownersList(List<Owner> owners, int currentPage, Page<Owner> page);

	public static native TemplateInstance ownerDetails(Owner owner, Result result);

	public static native TemplateInstance createOrUpdateOwnerForm(Owner owner, Result result);

}
```

Les **paramètres** des méthodes correspondent au **modèle de données** requis lors **du rendu des templates Qute**. Lors du build, la classe _QuteProcessor_ vérifie leur concordance. C’est la **magie de Quarkus**. Voici un exemple explicite d’erreur remontée si l’on omet le paramètre owners à la méthode ownersList:

```text
io.quarkus.qute.TemplateException: owners/ownersList.html:20:36 - {owner.firstName}: Only type-safe expressions are allowed in the checked template defined via: org.springframework.samples.petclinic.owner.OwnerTemplates.ownersList(); an expression must be based on a checked template parameter [page, currentPage], or bound via a param declaration, or the requirement must be relaxed via @CheckedTemplate(requireTypeSafeExpressions = false)
```

Au niveau de l’annotation @CheckedTemplate, l’attribut **basePath** permet de pointer sur le **répertoire templates/owners** et ne pas toucher à la localisation des fichiers te template html. Quarkus utilise le nom de la méthode pour retrouver le fichier html du même nom dans le répertoire _templates/owner_.

## Test des contrôleurs

Le test unitaire Spring Boot de la classe OwnerController utilise l’annotation **@WebMvcTest** pour configurer un contexte d'application limité, ciblant uniquement les composants liés à la couche web, ceci afin de tester les endpoints HTTP sans charger l'intégralité du contexte Spring de l'application.   
La classe utilitaire **MockMvc** permet à Spring de simuler des requêtes HTTP et de tester les contrôleurs Spring MVC sans démarrer un serveur web.

La migration des tests des contrôleurs REST vers Quarkus demande un peu de travail. En effet, Quarkus préconise l’utilisation de la bibilothèque [**REST-assured**](https://rest-assured.io/). Cette dernière permet de tester les API REST en facilitant l'envoi de requêtes HTTP et la vérification des réponses de manière fluide et intuitive à l’aide d’une fluent API.

Combinée à l’annotation **@QuarkusTest**, l’annotation **@TestHTTPEndpoint** permet de tester spécifiquement un contrôleur REST. Le support par Quarkus des annotations Spring demande quelques ajustements. En effet, la classe QuarkusTestExtension fait appel à la classe [SpringWebEndpointProvider](https://github.com/quarkusio/quarkus/blob/3.21.0/extensions/spring-web/core/runtime/src/main/java/io/quarkus/spring/web/runtime/SpringWebEndpointProvider.java) qui s’attend à ce qu’une annotation **@RequestMapping** annote le contrôleur REST testé. Pour être testable, **le code de prod a dû être refactoré** : il a été nécessaire de déclarer une annotation **@RequestMapping** au top niveau de chaque contrôleur REST.

Avant la mise en place du test OwnerControllerTests :

```java
@RestController
class OwnerController {

	@GetMapping("/owners/new")
	public TemplateInstance initCreationForm() {
```

Après la mise en place du test OwnerControllerTests :

```java
@RestController
@RequestMapping("/owners")
class OwnerController {

	@GetMapping("/new")
	public TemplateInstance initCreationForm() {
```

En prenant comme exemple la méthode testProcessCreationFormSuccess, vous pouvez comparer le code d'un test migré de Spring MockMvc vers REST-assured.  
Test avec Spring MockMvc :

```java
@Test
void testProcessCreationFormSuccess() throws Exception {
	mockMvc
		.perform(post("/owners/new").param("firstName", "Joe")
			.param("lastName", "Bloggs")
			.param("address", "123 Caramel Street")
			.param("city", "London")
			.param("telephone", "1316761638"))
		.andExpect(status().is3xxRedirection());
}
```

Test équivalent avec REST-assured :

```java
@Test
void testProcessCreationFormSuccess() {
	RestAssured
    .given()
		    .param("firstName", "Joe")
	      .param("lastName", "Bloggs")
  	    .param("address", "123 Caramel Street")
		    .param("city", "London")
		    .param("telephone", "1316761638")
		.when()
		    .post("/new")
		.then()
		    .statusCode(200)
		    .body("html.body.div.span", is("New Owner Created"));
}
```

## Du formatter Spring au ParamConverter JAX-RS

Dans la version Spring, la classe [PetTypeFormatter](https://github.com/spring-projects/spring-petclinic/blob/main/src/main/java/org/springframework/samples/petclinic/owner/PetTypeFormatter.java) est chargée de parser et d’afficher une instance de [PetType](https://github.com/spring-petclinic/quarkus-spring-petclinic/blob/v3.21.0/src/main/java/org/springframework/samples/petclinic/owner/PetType.java). Elle s’appuie sur l’interface [Formatter](https://github.com/spring-projects/spring-framework/blob/v6.2.5/spring-context/src/main/java/org/springframework/format/Formatter.java) de Spring Framework supportée par Spring MVC.

La migration de cette classe vers Quarkus a consisté à utiliser l’interface [**ParamConverter**](https://docs.redhat.com/en/documentation/red_hat_fuse/6.3/html/apache_cxf_development_guide/restparamconverter#RESTParamConverter) de JAX-RS. Le paragraphe [Parameter mapping](https://quarkus.io/guides/rest#parameter-mapping) du guide [Writing REST Services with Quarkus REST](https://quarkus.io/guides/rest) explique comment implémenter une telle classe et la mettre à disposition via un provider implémentant l’interface **ParamConverterProvider**, ce qui a été fait à travers la classe [PetclinicParamConverterProvider](https://github.com/spring-petclinic/quarkus-spring-petclinic/blob/v3.21.0/src/main/java/org/springframework/samples/petclinic/system/PetclinicParamConverterProvider.java).

Exemple de la classe [PetTypeFormatter](https://github.com/spring-petclinic/quarkus-spring-petclinic/blob/v3.21.0/src/main/java/org/springframework/samples/petclinic/owner/PetTypeFormatter.java):

```java
@Component
public class PetTypeFormatter implements ParamConverter<PetType> {

	private final PetTypeRepository petTypes;

	public PetTypeFormatter(PetTypeRepository petTypes) {
		this.petTypes = petTypes;
	}

	@Override
	public String toString(PetType petType) {
		return petType.getName();
	}

	@Override
	public PetType fromString(String text) {
		Collection<PetType> findPetTypes = this.petTypes.findAllByOrderByName();
		for (PetType type : findPetTypes) {
			if (type.getName().equals(text)) {
				return type;
			}
		}
		throw new IllegalArgumentException("type not found: " + text);
	}

}
```

Bien que le nom des méthodes ait changé, le code fonctionnel consistant à chercher un type d’animal dans les données de référence est resté inchangé.

## Conversion des dates

Les formulaires de l’application Petclinic permettent de saisir la **date de naissance** d’un animal ainsi que sa d **ate de visite** à la clinique vétérinaire. Ces champs dates peuvent être laissées **vides**. La validation des données saisies est faite côté serveur.

Or, la classe _org.jboss.resteasy.reactive.server.core.parameters.converters._ **_LocalDateParamConverter_ ne supporte pas les chaines vides** :

```text
Caused by: java.time.format.DateTimeParseException: Text '' could not be parsed at index 0 at java.base/java.time.format.DateTimeFormatter.parseResolved0(DateTimeFormatter.java:2108) at java.base/java.time.format.DateTimeFormatter.parse(DateTimeFormatter.java:2010) at java.base/java.time.LocalDate.parse(LocalDate.java:435) at org.jboss.resteasy.reactive.server.core.parameters.converters.LocalDateParamConverter.convert(LocalDateParamConverter.java:24) at org.jboss.resteasy.reactive.server.core.parameters.converters.LocalDateParamConverter.convert(LocalDateParamConverter.java:6) at org.jboss.resteasy.reactive.server.core.parameters.converters.TemporalParamConverter.convert(TemporalParamConverter.java:29) ... 14 more
```

Sur le même modèle que le PetTypeFormatter vu précédemment, la classe [**LocalDateParamConverter**](https://github.com/spring-petclinic/quarkus-spring-petclinic/blob/v3.21.0/src/main/java/org/springframework/samples/petclinic/system/LocalDateParamConverter.java) implémentant l’interface ParamConverter a été introduite puis déclarée dans le provider [PetclinicParamConverterProvider](https://github.com/spring-petclinic/quarkus-spring-petclinic/blob/v3.21.0/src/main/java/org/springframework/samples/petclinic/system/PetclinicParamConverterProvider.java).

## Cache applicatif

Spring Petclinic utilise Spring Cache et **Caffeine** pour mettre en cache la liste des vétérinaires. La version Quarkus s’appuie sur l’ [Extension Quarkus for Spring Cache API](https://quarkus.io/guides/spring-cache) qui permet de conserver l’usage de l’annotation **@Cacheable** de **Spring Cache**.

Une **différence de comportemen** t entre Quarkus et Spring Boot a été identifiée lors des tests. En effet, apposée initialement sur les méthodes du repository VetRepository, les annotations @Cacheable n’étaient prises en compte par Quarkus. Une correction a consisté à déplacer l’annotation @Cacheable au niveau du contrôleur [VetController](https://github.com/spring-petclinic/quarkus-spring-petclinic/blob/v3.21.0/src/main/java/org/springframework/samples/petclinic/vet/VetController.java) :

```java
@GetMapping
@Cacheable("vets")
public TemplateInstance showVetList(@RequestParam(defaultValue = "1") int page) {
	Vets vets = new Vets();
	Page<Vet> paginated = findPaginated(page);
	vets.getVetList().addAll(paginated.toList());
	return VetTemplates.vetList(paginated.getContent(), page, paginated);
}
```

Devenue inutile avec Quarkus, la classe [CacheConfiguration](https://github.com/spring-projects/spring-petclinic/blob/main/src/main/java/org/springframework/samples/petclinic/system/CacheConfiguration.java) a été supprimée.

## Gestion transactionnelle

L’extension [Narayana JTA](https://quarkus.io/extensions/io.quarkus/quarkus-narayana-jta/) apporte à Quarkus un gestionnaire de transaction JTA utilisable par Hibernate ORM.

L’annotation Spring **org.springframework.transaction.annotation.Transactional** a été remplacée par son équivalant JTA **jakarta.transaction.Transactional**.

Comme pour l’annotation @Cacheable, l’annotation **@Transactional** n’est pas prise en compte par Quarkus lorsqu’elle est utilisée au niveau du VetRepository. Spring Petclinic n’ayant plus de couche service, l’annotation @Transactional a été déplacée au niveau du contrôleur [VetController](https://github.com/spring-petclinic/quarkus-spring-petclinic/blob/v3.21.0/src/main/java/org/springframework/samples/petclinic/vet/VetController.java) :

```java
@GetMapping
@Cacheable("vets")
@Transactional
public TemplateInstance showVetList(@RequestParam(defaultValue = "1") int page) {
	Vets vets = new Vets();
	Page<Vet> paginated = findPaginated(page);
	vets.getVetList().addAll(paginated.toList());
	return VetTemplates.vetList(paginated.getContent(), page, paginated);
}
```

## Propriétés Spring Boot

Déclarée le temps de la migration puis supprimée une fois celle-ci terminée, l’ [extension Quarkus for Spring Boot properties](https://quarkus.io/extensions/io.quarkus/quarkus-spring-boot-properties/) a permis d’identifier les clés Quarkus à convertir dans le fichier [application.properties](https://github.com/spring-petclinic/quarkus-spring-petclinic/blob/v3.21.0/src/main/resources/application.properties). C’est le cas par exemple de la **durée du cache des ressources statiques**, configurées par défaut à 24h dans Quarkus, ramenée à 12h dans Petclinic.

```properties
// Avant
spring.web.resources.cache.cachecontrol.max-age=12h
// Après
quarkus.http.static-resources.max-age=12h
```

## Tests d’intégration avec Testcontainers

En complément des tests unitaires, Spring Petclinic utilise [**Testcontainers**](https://testcontainers.com/) pour ses tests d’intégration avec les bases MySQL et PostgreSQL. C’est par exemple le cas du test @SpringBootTest [PostgresIntegrationTests](https://github.com/spring-projects/spring-petclinic/blob/main/src/test/java/org/springframework/samples/petclinic/PostgresIntegrationTests.java) qui démarre une base PostgreSQL configurée dans le fichier [docker-compose.yml](https://github.com/spring-projects/spring-petclinic/blob/main/docker-compose.yml), utilisant à ce titre la dépendance **spring-boot-docker-compose**.

Le support par Quarkus de la bibliothèque Testcontainers est particulièrement bien aboutie et presque transparent. La version @QuarkusTest de [PostgresIntegrationTests](https://github.com/spring-petclinic/quarkus-spring-petclinic/blob/v3.21.0/src/test/java/org/springframework/samples/petclinic/PostgresIntegrationTests.java) ressemble à un test sans Docker :

```java
@QuarkusTest
@TestProfile(Profiles.Postgres.class)
class PostgresIntegrationTests {

	@Autowired
	private VetRepository vets;

	@Test
	void testFindAll() {
		vets.findAll();
	}

	@Test
	void testOwnerDetails() {
		RestAssured.when()
			.get("/owners/1")
			.then()
			.statusCode(200)
			.contentType(ContentType.HTML)
			.body(containsString("Owner Information"))
			.body(containsString("George Franklin"))
			.body(containsString("110 W. Liberty St."))
			.body(containsString("Madison"))
			.body(containsString("6085551023"))
			.body(containsString("Leo"))
			.body(containsString("cat"));
	}

}
```

L’annotation Quarkus **@TestProfile** permet de référencer l’inner-class Postgres implémentant l’interface **QuarkusTestProfile**.

```java
import io.quarkus.test.junit.QuarkusTestProfile;

public class Profiles {

	public static class Postgres implements QuarkusTestProfile {
		@Override
		public String getConfigProfile() {
			return "postgres-it";
		}
	}

	public static class MySQL implements QuarkusTestProfile {
		@Override
		public String getConfigProfile() {
			return "mysql-it";
		}
	}
}
```

Notez la présence de **2 profils Quarkus** **posgres-it** et **mysql-it** dédiés aux tests d’intégrations   
Dans le fichier [application.properties](https://github.com/spring-petclinic/quarkus-spring-petclinic/blob/v3.21.0/src/main/resources/application.properties), une ligne a été ajoutée pour chacun de ces profils :

```properties
%postgres-it.quarkus.datasource.db-kind=postgresql
%mysql-it.quarkus.datasource.db-kind=mysql
```

Ces 2 profils ont été ajoutés afin que l’URL JDBC de la base de données ne soit pas valorisée et que Quarkus utilise **[Dev Services](https://quarkus.io/guides/dev-services)** pour démarrer l’image Docker PostgreSQL.

## Binaire natif GraalVM

Grâce aux plugins native-maven-plugin et spring-boot-maven-plugin, la version Spring Boot de Petclinic permet de générer un binaire natif en s’appuyant sur GraalVM.

Le [guide Building a Native Executable](https://quarkus.io/guides/building-native-image) a permis de mettre en place facilement la génération d’un **exécutable natif de Quakus Spring** **Petclinic**. Dans le [pom.xml](https://github.com/spring-petclinic/quarkus-spring-petclinic/blob/v3.21.0/pom.xml), la configuration d’un profile maven **native** permet d’activer la propriété **quarkus.native.enabled**.

Contrairement à la version Spring Boot qui s’appuyait sur une base H2, la version Quarkus requière le démarrage d’une base PosgreSQL ou MySQL.

L’installation de GraalVM (ex : sdk install java 21-graal ) et la déclaration de la variable d’environnement GRAALVM\_HOME est nécessaire.

```bash
./mvnw package -Dnative -Dquarkus.profile=postgres
docker compose up postgres
./target/quarkus-spring-petclinic-*-runner
```

Quarkus Spring Petclinic démarre en 126 millisecondes :

```text
2025-04-13 15:54:29,755 INFO [io.quarkus] (main) quarkus-spring-petclinic 3.21.0 native (powered by Quarkus 3.21.0) started in 0.126s. Listening on: http://0.0.0.0:8080
2025-04-13 15:54:29,755 INFO [io.quarkus] (main) Profile postgres activated.
2025-04-13 15:54:29,755 INFO [io.quarkus] (main) Installed features: [agroal, cache, cdi, hibernate-orm, hibernate-orm-panache, hibernate-validator, jdbc-h2, jdbc-mysql, jdbc-postgresql, narayana-jta, qute, rest, rest-jackson, rest-qute, smallrye-context-propagation, smallrye-health, spring-cache, spring-data-jpa, spring-di, spring-web, vertx, web-dependency-locator]
```

## Conclusion

A travers ce billet, vous aurez entre-aperçu les différentes **étapes nécessaires** pour **migrer vers Quarkus et Qute** une **application Spring Web MVC** avec **Thymeleaf** comme moteur de templating et **Spring Data JPA** pour la persistance. L’usage des **extensions Quarkus pour Spring** facilite grandement cette migration. Les ingénieurs de chez Quarkus ont fait du très bon travail. Malgré les quelques écarts de fonctionnement soulignés dans cet article, j’en ai été assez bluffé. Bravo à eux !

J’ai profité de cette migration pour soumettre une dizaine de Pull Request dans la version originale de Spring Petclinic (ex : PR [#1775](https://github.com/spring-projects/spring-petclinic/pull/1775)).

Débutant en Quarkus, je ne serais pas surpris d’apprendre par mes lecteurs des axes d’améliorations. Utilisateur et amateur de Spring depuis 20 ans, j’ai essayé de rester neutre. **A vous de comparer les 2 versions de Petclinic et de vous faire votre avis**. Mon ressenti personnelle est que l’éco-système Java se porte bien et que la concurrence est saine et stimulante !

## Ressources

- [Repo Github Quarkus Spring Petclinic](https://github.com/arey/quarkus-spring-petclinic)
- [Repo Github Spring Boot Petclinic](https://github.com/spring-projects/spring-petclinic)
- [Quarkus for Spring developers: Getting started](https://developers.redhat.com/articles/2021/09/20/quarkus-spring-developers-getting-started)
- [Migrating a Spring Boot microservices application to Quarkus](https://developers.redhat.com/blog/2020/04/10/migrating-a-spring-boot-microservices-application-to-quarkus)
- [Migrating SpringBoot PetClinic REST to Quarkus](https://aytartana.wordpress.com/2020/08/26/migrating-springboot-petclinic-rest-to-quarkus/)
