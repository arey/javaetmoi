---
_edit_last: "1"
author: admin
categories:
  - test
date: "2013-09-06T16:46:25+00:00"
thumbnail: /wp-content/uploads/2013/09/test-database.jpg
featureImage: /wp-content/uploads/2013/09/test-database.jpg
featureImageAlt: "test-database"
guid: http://javaetmoi.com/?p=757
parent_post_id: null
post_id: "757"
post_views_count: "7897"
summary: |-
  Lors du développement de **tests d’intégration**, j’ai récemment eu besoin de charger une base de données à l’aide de jeux de données. Pour écrire mon premier test, j’ai simplement commencé par écrire un fichier SQL. En un appel de méthode (JdbcTestUtils::executeSqlScript) ou une ligne de déclaration XML (<jdbc:script location="" />), Spring m’aidait à charger mes données.<br>Pour tous ceux qui se sont déjà prêtés à l’exercice, maintenir des jeux de données est relativement fastidieux, qui plus en SQL. Cette solution n’était donc pas pérenne.

  Depuis une dizaine d’années, j’utilise régulièrement [DbUnit](http://www.dbunit.org/) pour tester la couche de persistance des applications Java sur lesquelles j’interviens, qu’elle soit développée avec JDBC, Hibernate ou bien encore JPA. Cette librairie open source est également très appréciable pour tester unitairement des procédures stockées manipulant des données par lot. Pour mon besoin, j’aurais donc pu naturellement me tourner vers cet outil qui a fait ses preuves et dont je suis familier.

  Mais voilà, commençant à apprécier les avantages de la configuration en Java offerte par Spring et les **APIs fluides** des frameworks FestAssert ou ElasticSearch utilisés sur l’application, l’idée d’ **écrire des jeux de données en Java** me plaisait bien. Et justement, il y’a quelques temps, l’argumentaire de l’article [Why use DbSetup?](http://dbsetup.ninja-squad.com/approach.html) ne m’avait pas laissé indifférent. C’était donc l’occasion d’utiliser cette jeune librairie développée par [les français de Ninja Squad](http://ninja-squad.fr/team) et qui mérite de se faire connaitre, j’ai nommé **[DbSetup](http://dbsetup.ninja-squad.com/)**.

  Le [guide utilisateur de DbSetup](http://dbsetup.ninja-squad.com/user-guide.html) étant particulièrement bien conçu, l'objectif de cet article n’est pas de vous en faire une simple traduction, mais de vous donner envie de l’essayer et de vous présenter la manière dont je l’ai mis en oeuvre. Celle-ci s’éloigne en effet quelque peu de celle présentée dans la documentation, la faute à mes vieux réflexes d’utilisateur de DbUnit et au bienheureux **[rollback pattern](http://xunitpatterns.com/Transaction%20Rollback%20Teardown.html)** de Spring.<br>

  ![test-database](/wp-content/uploads/2013/09/test-database.jpg)
tags:
  - database
  - dbsetup
  - dbunit
  - spring-framework
  - test
title: DbSetup, une alternative à DbUnit
url: /2013/09/dbsetup-spring-test-vs-dbunit/

---
{{< figure src="/wp-content/uploads/2013/09/test-database.jpg" alt="test-database" caption="test-database" >}}

Lors du développement de **tests d’intégration**, j’ai récemment eu besoin de charger une base de données à l’aide de jeux de données. Pour écrire mon premier test, j’ai simplement commencé par écrire un fichier SQL. En un appel de méthode (JdbcTestUtils::executeSqlScript) ou une ligne de déclaration XML (<jdbc:script location="" />), Spring m’aidait à charger mes données.  
Pour tous ceux qui se sont déjà prêtés à l’exercice, maintenir des jeux de données est relativement fastidieux, qui plus en SQL. Cette solution n’était donc pas pérenne.

Depuis une dizaine d’années, j’utilise régulièrement [DbUnit](http://www.dbunit.org/) pour tester la couche de persistance des applications Java sur lesquelles j’interviens, qu’elle soit développée avec JDBC, Hibernate ou bien encore JPA. Cette librairie open source est également très appréciable pour tester unitairement des procédures stockées manipulant des données par lot. Pour mon besoin, j’aurais donc pu naturellement me tourner vers cet outil qui a fait ses preuves et dont je suis familier.

Mais voilà, commençant à apprécier les avantages de la configuration en Java offerte par Spring et les **APIs fluides** des frameworks FestAssert ou ElasticSearch utilisés sur l’application, l’idée d’ **écrire des jeux de données en Java** me plaisait bien. Et justement, il y’a quelques temps, l’argumentaire de l’article [Why use DbSetup?](http://dbsetup.ninja-squad.com/approach.html) ne m’avait pas laissé indifférent. C’était donc l’occasion d’utiliser cette jeune librairie développée par [les français de Ninja Squad](http://ninja-squad.fr/team) et qui mérite de se faire connaitre, j’ai nommé **[DbSetup](http://dbsetup.ninja-squad.com/)**.

Le [guide utilisateur de DbSetup](http://dbsetup.ninja-squad.com/user-guide.html) étant particulièrement bien conçu, l'objectif de cet article n’est pas de vous en faire une simple traduction, mais de vous donner envie de l’essayer et de vous présenter la manière dont je l’ai mis en oeuvre. Celle-ci s’éloigne en effet quelque peu de celle présentée dans la documentation, la faute à mes vieux réflexes d’utilisateur de DbUnit et au bienheureux **[rollback pattern](http://xunitpatterns.com/Transaction%20Rollback%20Teardown.html)** de Spring.  

## Intégration de DbSetup avec Spring Test

Comme énoncé en introduction, le framework Spring et DbSetup peuvent fonctionner de concert, chacun ayant des rôles bien précis :

Spring :

- Démarrage de la base de données embarquée [H2](http://www.h2database.com/)
- Création du schéma de la base de données de l’application par exécution d’un script SQL contenant des ordres DDL
- Gestion de la source de données et des transactions
- Assertions facilitées par l’exécution de requêtes SQL via JdbcTemplate

Db Setup

- Insertion des données de test dans les tables de la base de données

Remarque : _dans mon contexte projet, chaque méthode de test a besoin de **son propre jeu de données**. Les données insérées ou modifiées par la précédente méthode testée doivent donc être purgées. Par choix, ce ménage n’est pas assuré par la classe [DbSetupTracker](http://dbsetup.ninja-squad.com/apidoc/1.0/com/ninja_squad/dbsetup/DbSetupTracker.html) proposée par DbSetup, mais par le support transactionnel offert par [Spring Test](http://static.springsource.org/spring/docs/3.2.x/spring-framework-reference/html/testing.html). Une transaction base de données est ouverte par Spring avant l’appel de la méthode de test puis est annulée une fois la fin de la méthode atteinte. Par contre, les données sont insérées par DbSetup au début de la méthode de test. Parce qu’il est parfois utile de pouvoir consulter l’état de la base après un test en échec, l’annotation [@Rollback(false)](http://static.springsource.org/spring/docs/3.2.x/spring-framework-reference/html/testing.html#integration-testing-annotations) peut être apposée temporairement sur la méthode incriminée afin que Spring valide la transaction._  
Pour que Spring Test puisse charger le contexte applicatif et initier le contexte transactionnel, les 3 annotations suivantes décorent la classe de test :

```xhtml
@RunWith(SpringJUnit4ClassRunner.class)
@ContextConfiguration
@Transactional
public class TestSpringDbSetup { … }
```

Le code source complet de la classe [TestSpringDbSetup.java](https://gist.github.com/arey/6460147) peut être consulté sur GitHub .

La configuration du contexte Spring est déclarée en java, dans une nested class du test. A noter que cette classe de configuration pourrait être externalisée afin d’être utilisée par toutes les classes de tests unitaires. Y sont déclarés : une source de données, un gestionnaire de transaction, une instance de _JdbcTemplate_ pouvant être utilisées par les assertions et une _Destination_ DbSetup.

```xhtml
@Configuration
static class Config {

    @Bean
    public DataSource dataSource() {
        return new EmbeddedDatabaseBuilder()
                .setType(EmbeddedDatabaseType.H2)
                .addScript("schema.sql")
               .build();
    }

    @Bean
    public PlatformTransactionManager transactionManager() {
        return new DataSourceTransactionManager(dataSource());
    }

    @Bean
    public JdbcTemplate jdbcTemplate() {
        return new JdbcTemplate(dataSource());
    }

    @Bean Destination destination() {
        return new TransactionAwareDestination(dataSource(), transactionManager());
    }
}
```

L’interface _Destination_ fournie par DbSetup permet à ce dernier d’accéder à une connexion JDBC. De base, DbSetup vient avec 2 implémentations : l’une pour récupérer une connexion depuis une _DataSource_ et une autre pour la récupérer directement depuis le _DriverManager_.  
Notre exemple utilise l’implémentation spécifique **_[TransactionAwareDestination](https://gist.github.com/arey/6453086)_** dont le code source est disponible sous forme de Gist. Basé sur le proxy _[TransactionAwareDataSourceProxy](http://static.springsource.org/spring/docs/3.2.4.RELEASE/javadoc-api/org/springframework/jdbc/datasource/TransactionAwareDataSourceProxy.html)_  proposé par Spring, cette destination permet à DbSetup d’utiliser le contexte transactionnel géré par Sring pour récupérer et clôturer une connexion, commiter ou bien rollbacker. La classe _[TransactionAwareDestination](https://gist.github.com/arey/6453086)_ apporte une amélioration reportée dans la Jira [SPR-6441](https://jira.springsource.org/browse/SPR-6441).  
Afin de pouvoir être utilisés dans les méthodes de test, les beans _JdbcTemplate_ et _Destination_ sont injectés en tant que propriétés de la classe _TestSpringDbSetup_ :

```xhtml
@Autowired
private JdbcTemplate jdbcTemplate;

@Autowired
private Destination destination;
```

Du plus simple effet, le script schema.sql contient la création d’une table :

```sql
create table customer(id number primary key, name varchar not null);
```

La configuration de notre classe de test est terminée. Mis à part une référence sur l’interface _Destination_, le code ne fait pour l’instant aucun usage de DbSetup. C’est précisément l’objectif du paragraphe suivant.

## Utilisation de DbSetup

Au travers de 2 méthodes de tests, nous allons voir quelles sont les **facilitées proposées par DbSetup** pour écrire des jeux de données. Attention, les scénarios de test proposés n’ont aucune valeur métier et permettent uniquement d’illustrer cet article.

Notre **première méthode de test** insère en base de données 4 clients dont les prénoms ont une racine commune ou une casse différente :

```xhtml
@Test
public void indexCustomerWithSimilarName() throws SQLException {
    // Prepare
    Operation operation = insertInto("CUSTOMER")
            .withGeneratedValue("ID", ValueGenerators.sequence())
            .columns("NAME")
            .values("Antoine")
            .values("ANTOINE")
            .values("Antoinette")
            .values("Pierre-Antoine")
            .build();
    new DbSetup(destination, operation).launch();

    // Execute test
    // ...

    // Assertions
      assertEquals(4,  jdbcTemplate.queryForObject("select count(*) from customer",
            Integer.class);
    assertEquals(4, count);
}
```

Sans même connaitre l'API de DbSetup, la premier constat est que **le code est lisible** et reste donc maintenable par tout développeur Java.

L’identifiant de chaque client n’ayant pas d’importance dans notre scénario de test, un **générateur de valeurs séquentielles** est utilisé à l’aide de la classe utilitaire [_ValueGenerators_](http://dbsetup.ninja-squad.com/apidoc/1.0/com/ninja_squad/dbsetup/generator/ValueGenerators.html). Cette possibilité offerte par DbSetup est fort appréciable dans le cas où des colonnes non _null_ doivent être valorisées alors que leurs valeurs n’ont pas d’impact sur le test.

Si elle avait été plus longue, la liste de noms à insérer aurait pu être construite à partir d’une **boucle** parcourant une liste de valeurs. Merci Java.

Une fois la méthode de test terminé, Spring Test rollback l’insertion de ces 4 clients.

Notre **seconde méthode de test** utilise 2 autres fonctionnalités offertes par DbSetup et qui font défaut à DbUnit :

```xhtml
private static final int CUSTOMER_1 = 1;
@Test
public void indexSingleCustomer() {
    Operation operation = insertInto("CUSTOMER")
            .columns("ID", "NAME")
            .values(CUSTOMER_1, "James")
            .build();
    new DbSetup(destination, operation).launch();

    int id = jdbcTemplate.queryForObject(
               "select id from customer where id=?", Integer.class, CUSTOMER_1);
    assertEquals(CUSTOMER_1, id) ;
}
```

En effet, là où les fichiers XML de DbUnit sont limités à de simples chaînes de caractères, DbSetup permet d’ **utiliser des valeurs typées** pour écrire des jeux de données. Dans l’exemple précédent, un _int_ est utilisé pour renseigner la valeur de la colonne "ID". DbSetup supporte nativement de nombreux types Java. Le framework de test se charge de binder les types Java en type SQL (java.sql.Types). Il laisse néanmoins la possibilité d’étendre cette liste en implémentant l’interface _[BinderConfiguration](http://dbsetup.ninja-squad.com/apidoc/1.0/com/ninja_squad/dbsetup/bind/BinderConfiguration.html)_ et/ou en créant ses propres _[Binder](http://dbsetup.ninja-squad.com/apidoc/1.0/com/ninja_squad/dbsetup/bind/Binder.html)_.

Déclarer ses jeux de données en Java permet d’ **utiliser des constantes**, ici CUSTOMER\_1. La même constante peut être réutilisée pour plusieurs jeux de données, utilisée lors des assertions ou lors de l’exécution du test. Le code en devient plus lisible. Les constantes sont particulièrement intéressantes avec les clés étrangères.  
Ces 2 exemples ne mettent en pratique qu’une partie des fonctionnalités de DbSetup. Valeurs par défaut, exécution de requêtes SQL, chainage d’opération en sont d’autres.

## Avantages et inconvénients

Après avoir utilisé DbSetup pendant quelques semaines, j’en suis particulièrement satisfait. Voici les avantages et inconvénients que j’en retire :

**Avantages****Faiblesses**

- Un DbUnit like dopé aux bonnes pratiques contemporaines
- Intégration possible à Spring Test
- Prise en main rapide
- Factorisation des jeux de données rendue possible
- Qualité de la documentation, de la javadoc et du code source
- Disponible sur le repo maven central
- Légèreté, aucune dépendance tierce
- Equipe ouverte aux améliorations

- Fonctionnalité restreinte au chargement
- Aucun log pour le debug
- Qui de la pérennité ?

Pour les intéressés qui souhaiteraient migrer de DbUnit vers DbSetup, voici les fonctionnalités proposées par DbUnit mais non couvertes par DbSetup :

1. Chargement de jeux de données depuis les formats XML et CSV (à nuancer car DbSetup propose une alternative en Java, ce qui en fait son principal intérêt)
1. Création d’une XSD à partir du schéma de la base de données pour une validation stricte des jeux de données
1. Export de données depuis une base de données source
1. Assertion des données présentes en base après l’exécution d’un test
1. Récupération du graphe de dépendances des tables ([TablesDependencyHelper](http://dbunit.sourceforge.net/apidocs/org/dbunit/database/search/TablesDependencyHelper.html))

## Conclusion

Retrouver du plaisir dans l’écriture de jeux de données n’était pas gagné d’avance. DbSetup remporte haut la main ce challenge. Est-ce l’attrait pour la nouveauté ? Il est trop tôt pour me prononcer.  
Si vous souhaitez contribuer à ce projet open source, ses auteurs sont particulièrement ouverts à toute suggestion. Les 2 tickets que j’ai ouverts sur Github ont été traités dans les heures qui suivent, et de manière très professionnelle.

Pour terminer, je me demande s’il ne serait pas possible d’étendre DbUnit afin lui apporter les facilités d’écriture de DbSetup. A quand une implémentation _JavaDataSet_ de l’interface _[IDataSet](http://dbunit.sourceforge.net/apidocs/org/dbunit/dataset/IDataSet.html)_?
