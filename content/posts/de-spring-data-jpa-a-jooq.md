---
_edit_last: "1"
_monsterinsights_sitenote_active: ""
_monsterinsights_skip_tracking: ""
author: admin
categories:
  - conférence
  - retour-d'expérience
  - spring
date: "2025-06-16T06:57:01+00:00"
footnotes: ""
guid: https://javaetmoi.com/?p=2580
parent_post_id: null
post_id: "2580"
post_views_count: "1518"
summary: |-
  ![jOOQ: The easiest way to write SQL in Java](https://javaetmoi.com/wp-content/uploads/2025/06/jooq-the-easiest-way-to-write-sql-in-java.png)

  Lors de la conférence Devoxx France 2025, j’ai participé à un hands-on lab de 2h intitulé [Sortir des ORMs avec jOOQ](https://www.devoxx.fr/agenda-2025/talk/sortir-des-orms-avec-jooq/). Acronyme de « **Java Object Oriented Querying** », **jOOQ** se présente comme une **alternative à JPA** permettant d’ **écrire des requêtes SQL** en Java via une **fluent API**. Animé par Sylvain Decout et Samuel Lefebvre, cet atelier visait à migrer une application Spring Boot / JPA vers jOOQ à l’aide du **starter Spring Boot** pour jOOQ. Pour les curieux, le repo de l’atelier est disponible sur Github : [jooq-handson](https://github.com/sylvaindecout/jooq-handson).

  Fort de cette découverte, je me suis à mon tour prêté à l’exercice de migrer vers jOOQ la couche de persistance Spring Data JPA de l’application démo Spring Petclinic. Un nouveau fork est né : [**spring-petclinic-jooq**](https://github.com/spring-petclinic/spring-petclinic-jooq). Bienvenue à ce dernier dans la communauté Spring Petclinic.

  L’usage de jOOQ se rapproche de l’utilisation de JdbcTemplate. Le développeur maitrise le nombre de requêtes envoyées à la base de données relationnelle. Ce qui les différencie, c’est la syntaxe : pas de SQL, mais une **API Java fluide** et **type-safe** spécifique à jOOQ qu’il va falloir appréhender. Rassurez-vous, cette API se rapproche du SQL : on y retrouve les mots clés **select**, **update**, **insertInto**, **where**, **from**, **join**, **on**, **as**… A ceux-ci, on ajoute des mots clés spécifiques à jOOQ : **paginate**, **fetch**, **convertFrom** … La [**documentation**](https://www.jooq.org/learn/) de jOOQ est très **complète**. On y apprend comment écrire des requêtes complexes à base de window function ou de Common Table Expressions (CTE) et comment utiliser des fonctionnalités avancées de SQL que peu de frameworks ORM supportent nativement : [JSON functions](https://www.jooq.org/doc/latest/manual/sql-building/column-expressions/json-functions/), [PIVOT](https://blog.jooq.org/how-to-use-sql-pivot-to-compare-two-tables-in-your-database/), [MERGE](https://www.jooq.org/doc/latest/manual/sql-building/sql-statements/merge-statement/), [UNION](https://www.jooq.org/doc/latest/manual/sql-building/sql-statements/select-statement/set-operations/set-operation-union/) …

  Cet article a pour objectif d’expliquer les **étapes** adoptées pour **migrer l’implémentation Spring Data JPA des repository vers jOOQ**. Des exemples de code avant / après y sont proposés.
tags:
  - devoxx
  - jooq
  - jpa
  - spring-data
  - sql
title: De Spring Data JPA à jOOQ
url: /2025/06/de-spring-data-jpa-a-jooq/

---
![jOOQ: The easiest way to write SQL in Java](/wp-content/uploads/2025/06/jooq-the-easiest-way-to-write-sql-in-java.png)

Lors de la conférence Devoxx France 2025, j’ai participé à un hands-on lab de 2h intitulé [Sortir des ORMs avec jOOQ](https://www.devoxx.fr/agenda-2025/talk/sortir-des-orms-avec-jooq/). Acronyme de « **Java Object Oriented Querying** », **jOOQ** se présente comme une **alternative à JPA** permettant d’ **écrire des requêtes SQL** en Java via une **fluent API**. Animé par Sylvain Decout et Samuel Lefebvre, cet atelier visait à migrer une application Spring Boot / JPA vers jOOQ à l’aide du **starter Spring Boot** pour jOOQ. Pour les curieux, le repo de l’atelier est disponible sur Github : [jooq-handson](https://github.com/sylvaindecout/jooq-handson).

Fort de cette découverte, je me suis à mon tour prêté à l’exercice de migrer vers jOOQ la couche de persistance Spring Data JPA de l’application démo Spring Petclinic. Un nouveau fork est né : [**spring-petclinic-jooq**](https://github.com/spring-petclinic/spring-petclinic-jooq). Bienvenue à ce dernier dans la communauté Spring Petclinic.

L’usage de jOOQ se rapproche de l’utilisation de JdbcTemplate. Le développeur maitrise le nombre de requêtes envoyées à la base de données relationnelle. Ce qui les différencie, c’est la syntaxe : pas de SQL, mais une **API Java fluide** et **type-safe** spécifique à jOOQ qu’il va falloir appréhender. Rassurez-vous, cette API se rapproche du SQL : on y retrouve les mots clés **select**, **update**, **insertInto**, **where**, **from**, **join**, **on**, **as**… A ceux-ci, on ajoute des mots clés spécifiques à jOOQ : **paginate**, **fetch**, **convertFrom** … La [**documentation**](https://www.jooq.org/learn/) de jOOQ est très **complète**. On y apprend comment écrire des requêtes complexes à base de window function ou de Common Table Expressions (CTE) et comment utiliser des fonctionnalités avancées de SQL que peu de frameworks ORM supportent nativement : [JSON functions](https://www.jooq.org/doc/latest/manual/sql-building/column-expressions/json-functions/), [PIVOT](https://blog.jooq.org/how-to-use-sql-pivot-to-compare-two-tables-in-your-database/), [MERGE](https://www.jooq.org/doc/latest/manual/sql-building/sql-statements/merge-statement/), [UNION](https://www.jooq.org/doc/latest/manual/sql-building/sql-statements/select-statement/set-operations/set-operation-union/) …

Cet article a pour objectif d’expliquer les **étapes** adoptées pour **migrer l’implémentation Spring Data JPA des repository vers jOOQ**. Des exemples de code avant / après y sont proposés.

## Configuration du build

[Spring Boot supporte nativement l’usage des versions commerciales et Open Source de jOOQ](https://docs.spring.io/spring-boot/reference/data/sql.html#data.sql.jooq). Dans le **pom.xml** ou le fichier **build.gradle**, commencer par déclarer le starter Spring Boot pour jOOQ **spring-boot-starter-jooq** :

```
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-jooq</artifactId>
</dependency>
```

L’étape suivante consiste à générer les classes Java à partir du schéma de la base de données. [jOOQs propose différentes possibilités](https://www.jooq.org/doc/latest/manual/code-generation/codegen-configuration/): à partir du **script DDL** de création du schéma comme sur Petclinic, de scripts **Liquibase** ou bien encore des **méta-données** d’une base existante.   
 Les plugins [**jooq-codegen-maven**](https://www.jooq.org/doc/latest/manual/code-generation/codegen-execution/codegen-maven/) ou [**jooq-codegen-gradle**](https://www.jooq.org/doc/latest/manual/code-generation/codegen-execution/codegen-gradle/) sont à configurer.   
 Voici un exemple extrait de jOOQ Spring Petclinic :

```
<plugin>
  <groupId>org.jooq</groupId>
  <artifactId>jooq-codegen-maven</artifactId>
  <executions>
    <execution>
      <goals>
        <goal>generate</goal>
      </goals>
    </execution>
  </executions>
  <configuration>
    <generator>
      <database>
        <name>org.jooq.meta.extensions.ddl.DDLDatabase</name>
        <properties>
          <property>
            <key>scripts</key>
            <value>src/main/resources/db/h2/schema.sql</value>
          </property>
          <property>
            <key>sort</key>
            <value>semantic</value>
          </property>
          <property>
            <key>unqualifiedSchema</key>
            <value>none</value>
          </property>
          <property>
            <key>defaultNameCase</key>
            <value>as_is</value>
          </property>
        </properties>
      </database>
    </generator>
  </configuration>
  <dependencies>
    <dependency>
      <groupId>org.jooq</groupId>
      <artifactId>jooq-meta-extensions</artifactId>
      <version>${jooq-meta-extensions.version}</version>
    </dependency>
  </dependencies>
</plugin>

```

La classe org.jooq.meta.extensions.ddl. **DDLDatabase** provenant de l’extension [jooq-meta-extensions](https://www.jooq.org/doc/latest/manual/code-generation/codegen-meta-sources/codegen-ddl/) permet au plugin jooq-codegen-maven d’exploiter le script DDL src/main/resources/db/h2/ [schema.sql](https://github.com/spring-petclinic/spring-petclinic-jooq/blob/v3.4.2/src/main/resources/db/h2/schema.sql) utilisé par défaut lors du démarrage de l’application avec le profil Spring par défaut.

Dans le package org.jooq.generated.tables, l’exécution du plugin jOOQ génère une **classe Vets** héritant de la classe TableImpl<VetsRecord> et modélisant la table éponyme. La **classe VetsRecord** a également été générée dans le sous-package records. Elle représente une ligne de la table pets.


Nous verrons leurs usages lors de la migration de la classe PetRepository.

## Migration des repositories

**L’une des forces de jOOQ est qu’il sait cohabiter aux côtés de JPA**. On peut donc migrer au fil de l’eau les respositories d’une application et même choisir de conserver les 2 solutions en fonction des besoins. Cette capacité a été pratique dans le travail de migration : chaque repository a été migré l’un après l’autre. L’application Petclinic est restée fonctionnelle tout du long.

Premier changement notable : la nature des repositories qui passent d’une interface héritant de l’interface **Repository** de **Spring Data JPA** à une **classe concrète** qu’on annote avec **@Repository** et dont le constructeur accepte une instance de **DSLContext**.

Avant :

```
public interface VetRepository extends Repository<Vet, Integer> {
```

Après:

```
@Repository
public class VetRepository {

    private final DSLContext dsl;

    public VetRepository(DSLContext dslContext) {
       this.dsl = dslContext;
    }
```

Continuons par changer l’implémentation d’une première requête SQL simple utilisant un SELECT.   
Requête native SQL utilisée par Spring Data JPA :

```
@Query("SELECT ptype FROM PetType ptype ORDER BY ptype.name")
List<PetType> findPetTypes();
```

Implémentation équivalente avec jOOQ :

```
public List<PetType> findPetTypes() {
    return dsl
       .selectFrom(TYPES)
       .orderBy(TYPES.NAME)
       .fetchInto(PetType.class);
}
```

On retrouve ici tous les éléments de la requête SQL, mais avec une syntaxe Java jOOQ équivalente. Le mot clé SQL « SELECT » est remplacé par la méthode **selectFrom()**, le « ORDER BY » par la méthode **orderBy()**. A noter que nous n’utilisons pas de chaines de caractères pour nommer les tables et les colonnes, mais les constantes générées par le plugin jOOQ. Ainsi, en cas de changement de schéma (ex : nom de colonne renommée), le code Java ne compilera plus et il faudra l’adapter. Avec cette approche, les erreurs de syntaxe ne sont plus possibles. On perçoit ici toute la sécurité apportée par la type-safety de jOOQ.   
Enfin, la méthode **fetchInto()** mappe les lignes retournées par la base dans une liste d’instance de PetType.

Là où JPA et Hibernate nous facilitaient la sauvegarde de nos entités JPA, jOOQ va demander un travail nettement plus important. En effet, la méthode save() de l’interface CrudRepository de Spring Data JPA ne demandait qu’à être appelée. La magie des ORM opérait grâce aux annotations JPA apposées sur les entités. jOOQ nécessite de prévoir les 2 requêtes SQL correspondantes et d’effectuer à la main le binding des propriétés du Owner vers les colonnes. Exemple de sauvegarde d’un Owner :

```
public Integer saveOrUpdateDetails(Owner owner) {
    if (owner.isNew()) {
       return requireNonNull(
          dsl.insertInto(OWNERS)
             .set(mapOwnerToRecord(owner))
             .returningResult(OWNERS.ID)
             .fetchOne())
          .getValue(OWNERS.ID);
    } else {
       dsl.update(OWNERS)
          .set(mapOwnerToRecord(owner))
          .where(OWNERS.ID.eq(owner.getId()))
          .execute();
       return owner.getId();
    }
}

private Map<Field<?>, Object> mapOwnerToRecord(Owner owner) {
    return Map.of(OWNERS.FIRST_NAME, owner.getFirstName(), OWNERS.LAST_NAME, owner.getLastName(), OWNERS.ADDRESS,
       owner.getAddress(), OWNERS.CITY, owner.getCity(), OWNERS.TELEPHONE, owner.getTelephone());
}
```

Rien de compliqué, mais un peu plus verbeux.   
L’un des principaux avantages de jOOQ consiste à maitriser le nombre de requêtes SQL envoyées à la base. En l’occurrence, dans cet exemple, une seule et unique requête de type UPDATE est envoyée lors d’un mise à jour.   
Avec l’implémentation Spring Data JPA, dans le cadre de la mise à jour d’un Owner, [comme expliqué dans l’article Skip Select Before Insert in Spring Data JPA](https://www.baeldung.com/spring-data-jpa-skip-select-insert), Spring Data JPA appelle la méthode **merge()** de l’entity manager JPA qui, si l’entité n’est pas en cache, va charger le Owner en exécutant autant de requêtes SQL de type SELECT que nécessaires.

Autre différence notable : jOOQ laisse décider du ou des champs à mettre à jour. Dans notre exemple, les Pets associés à leur Owner ne seront par exemple pas mis à jour. Avec JPA, on utilisait le **cascading** et l’attribut cascade des annotations comme @OneToMany.

Dans la même idée, lors de requêtes de type SELECT, les **jointures** entre tables devront être systématiquement précisées. A titre d’exemple, charger un animal et son type nécessitera un appel à **join()** :

```
@Transactional(readOnly = true)
public Optional<Pet> findByIdWithoutVisits(Integer petId) {
    return dsl.select()
       .from(PETS)
       .join(PETS.types_())
       .where(PETS.ID.eq(petId))
       .fetchOptional(PetRepository::toPet);
}
```

Noter ici l’utilisation d’une [**jointure implicite**](https://www.jooq.org/doc/latest/manual/sql-building/sql-statements/select-statement/from-clause/implicit-join/) basée sur la **clé étrangère**, évitant ainsi d’ajouter une clause **ON** entre la PK de PETS et la FK de TYPES.   
Avec une **association 1:1**, le chargement et le mapping du type d’animal ne présente aucune difficulté :

```
private static Pet toPet(org.jooq.Record row) {
    return new Pet(row.get(PETS.ID), row.get(PETS.NAME), row.get(PETS.BIRTH_DATE),
          new PetType(row.get(PETS.TYPE_ID), row.get(TYPES.NAME)));
}
```

Le chargement des **associations 1:N** se complexifie. L’usage de l’ [**opérateur mulstiset()**](https://blog.jooq.org/jooq-3-15s-new-multiset-operator-will-change-how-you-think-about-sql/) du SQL qui est supporté par jOOQ permet de charger les Vets et leurs Specialities en une seule requête :

```
public List<Vet> findAll(){
    return dsl.select(VETS.ID, VETS.FIRST_NAME, VETS.LAST_NAME, MULTISET_SPECIALITIES)
       .from(VETS)
       .leftJoin(VETS.vetSpecialties())
       .orderBy(VETS.ID)
       .fetch(VetRepository::toVet);
}

private static final Field<List<Specialty>> MULTISET_SPECIALITIES = multiset(
    select(VET_SPECIALTIES.specialties().ID, VET_SPECIALTIES.specialties().NAME)
       .from(VET_SPECIALTIES)
       .where(VET_SPECIALTIES.VET_ID.eq(VETS.ID)))
    .as("specialties")
    .convertFrom(result -> result.map(it -> new Specialty(it.get(SPECIALTIES.ID), it.get(SPECIALTIES.NAME))));

private static Vet toVet(Record4<Integer, String, String, List<Specialty>> row) {
    return new Vet(row.get(VETS.ID), row.get(VETS.FIRST_NAME), row.get(VETS.LAST_NAME),
       new HashSet<>(row.get(MULTISET_SPECIALITIES)));
}
```

jOOQ permet d’imbriquer plusieurs multiset afin de charger les visites des animaux d’un propriétaire en une seule requête. Je vous renvoie à la classe [OwnerRepository](https://github.com/spring-petclinic/spring-petclinic-jooq/blob/main/src/main/java/org/springframework/samples/petclinic/owner/OwnerRepository.java).

Pour finir, les écrans « Find Owners » et « Veterinarians » affichent les résultats de manière paginée. jOOQ supporte la pagination au travers de la [Seek Method](https://github.com/spring-petclinic/spring-petclinic-jooq/blob/main/src/main/java/org/springframework/samples/petclinic/owner/OwnerRepository.java) (aussi appelée [Keyset paging](https://blog.jooq.org/faster-sql-pagination-with-keysets-continued/)) ou du [calcul des méta-données de pagination en une seule requête SQL](https://blog.jooq.org/calculating-pagination-metadata-without-extra-roundtrips-in-sql/). C’est cette dernière approche qui a été utilisée sur jOOQ Petclinic afin de garder iso-fonctionnels les **écrans paginés**. Les plus curieux peuvent se référer à l’implémentation de la méthode findAll(Pageable pageable) de [VetRepository](https://github.com/spring-petclinic/spring-petclinic-jooq/blob/main/src/main/java/org/springframework/samples/petclinic/vet/VetRepository.java) et à la méthode paginate() du [JooqHelper](https://github.com/spring-petclinic/spring-petclinic-jooq/blob/main/src/main/java/org/springframework/samples/petclinic/system/JooqHelper.java). Sur le même modèle que ce que propose Spring Data, des **records Pageable** et **Page** ont été introduits dans la base de code.   
![](/wp-content/uploads/2025/06/word-image-2580-2.png)

## Au revoir JPA

Une fois l’ensemble des Repository migrés, la dernière étape a consisté à retirer la dépendance spring-boot-starter-data-jpa ainsi que toutes les annotations JPA apposées sur les entités (@Entity, @Table, @ ManyToMany …).

Débarrassé de JPA, nous pouvons revoir en partie le design de l’application qui avait été limité par ce dernier. En effet, [les entités JPA ne peuvent pas être modélisées avec des record Java](ManyToMany). Suite à la migration vers jOOQ, les entités du domaine métier de Spring Petclinic n’ont plus d’adhérence avec la couche de persistance. Les **classes immutables** ont pu être converties en **record**. Exemple du value object [Speciality](https://github.com/spring-petclinic/spring-petclinic-jooq/blob/v3.4.2/src/main/java/org/springframework/samples/petclinic/vet/Specialty.java) :

```
public record Specialty(Integer id, String name) {
}
```

Le refactoring de la modélisation aurait pu aller plus loin, mais ce n’était pas l’objectif de cette version de Petclinic dédiée à jOOQ et non à la Clean Architecture. Peut-être l’objet d’un prochain article ?

## Conclusion

A travers l’exemple de migration de l’application démo Spring Petclinic, cet article donne un aperçu des possibilités offertes par jOOQ. Cette librairie est mature, a plus de 15 ans (la version 1.0.0 de jOOQ est [sortie en 2010](https://www.jooq.org/notes?version=3.4)) et est utilisée par de grands comptes comme Apple, Allianz et Mastercard.   
Notez néanmoins que jOOQ possède un système de [double licence](https://www.jooq.org/legal/licensing): commerciale et Open Source. [Les distributions commerciales de jOOQ maintiennent un support versionné des SGBDR](https://www.jooq.org/download/support-matrix). A contrario, l'édition Open Source de jOOQ ne supporte que la dernière version des SGBDR Open Source. A ce titre, l’utilisation de jOOQ avec Oracle et SQL Server requière une licence commerciale.

En replongeant dans le SQL, je me suis aperçu que j’étais passé à côté de certaines fonctionnalités avancées comme les [MULTISET](https://reintech.io/blog/understanding-sql-multiset-data-type). A retenir.

Enfin, je remercie Sylvain pour sa relecture du code de Spring Petclinic jOOQ et ses conseils avisés. J’invite tous les autres experts jOOQ à venir améliorer le repository [spring-petclinic-jooq](spring-petclinic-jooq) en soumettant des Issues ou en proposant des Pull Requests.   
