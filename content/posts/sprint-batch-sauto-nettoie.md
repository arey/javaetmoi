---
_edit_last: "1"
author: admin
categories:
  - spring
date: "2012-06-26T18:49:09+00:00"
guid: http://javaetmoi.com/?p=187
parent_post_id: null
post_id: "187"
post_views_count: "10595"
summary: |-
  Lorsque vous mettez en œuvre **[Spring Batch](http://static.springsource.org/spring-batch/ "Page d'accueil du projet Spring Batch")** pour réaliser des traitements par lots, vous avez le  choix d’utiliser **une implémentation de _JobRepository_** soit **en mémoire** soit **persistante**. L’avantage de cette dernière est triple :

  1. Conserver un **historique des différentes exécutions** de vos instances de jobs.
  2. Pouvoir **suivre en temps réel le déroulement de votre batch** via, par exemple, l’excellent [Spring Batch Admin](http://static.springsource.org/spring-batch-admin/ "Page d'accueil du projet Spring Batch Admin").
  3. Avoir la possibilité de **reprendre un batch** là où il s’était arrêté en erreur.

  La contrepartie d’utiliser un JobRepository persistant est de devoir faire reposer le batch sur une **base de données** relationnelles. Le schéma sur lequel s’appuie Spring Bath est composé de **6 tables**. Leur MPD est disponible dans l’ [annexe  B. Meta-Data Schema](http://static.springsource.org/spring-batch/reference/html/metaDataSchema.html "Appendix B. Spring Batch Meta-Data Schema") du [manuel de référence de Spring Batch](http://static.springsource.org/spring-batch/reference/html/ "Manuel de référence de Spring Batch au format HTML"). SpringSource faisant bien les choses, les scripts DDL de différentes solutions du marché (ex : MySQL, Oracle, DB2, SQL Server, Postgres, H2 …) sont disponibles dans le package org.springframework.batch.core du JAR spring-batch-core-xxx.jar{{ double-space-with-newline }}Qui dit base de données, dit **dimensionnement** de cette dernière. L’ **espace disque requis** est alors **fonction** du **nombre d’exécutions** estimé, de la **nature des informations contextuelles persistées** et de la **durée de rétention** des données. Cette démarche prend tout son sens lorsqu’une instance de base de données est dédiée au schéma de Spring Batch.  En faisant quelques hypothèses (ex : sur le taux d’échec) et en mesurant le volume occupé sur plusieurs exécutions des batchs, il est possible de prévoir assez finement l’espace occupé par les données.

  A moins de disposer de ressources infinies ou de n’avoir qu’un seul batch annuel, il est fréquent de fixer une durée de rétention de l’historique. Première option : demander à l’équipe d’exploitation de régulièrement lancer un script SQL de purge. Deuxième option : **utiliser Spring Batch pour purger ses propres données** !!
tags:
  - spring-batch
  - spring-framework
  - sql
title: Spring Batch s'auto-nettoie
url: /2012/06/sprint-batch-sauto-nettoie/

---
Lorsque vous mettez en œuvre **[Spring Batch](http://static.springsource.org/spring-batch/ "Page d'accueil du projet Spring Batch")** pour réaliser des traitements par lots, vous avez le  choix d’utiliser **une implémentation de _JobRepository_** soit **en mémoire** soit **persistante**. L’avantage de cette dernière est triple :

1. Conserver un **historique des différentes exécutions** de vos instances de jobs.
1. Pouvoir **suivre en temps réel le déroulement de votre batch** via, par exemple, l’excellent [Spring Batch Admin](http://static.springsource.org/spring-batch-admin/ "Page d'accueil du projet Spring Batch Admin").
1. Avoir la possibilité de **reprendre un batch** là où il s’était arrêté en erreur.

La contrepartie d’utiliser un JobRepository persistant est de devoir faire reposer le batch sur une **base de données** relationnelles. Le schéma sur lequel s’appuie Spring Bath est composé de **6 tables**. Leur MPD est disponible dans l’ [annexe  B. Meta-Data Schema](http://static.springsource.org/spring-batch/reference/html/metaDataSchema.html "Appendix B. Spring Batch Meta-Data Schema") du [manuel de référence de Spring Batch](http://static.springsource.org/spring-batch/reference/html/ "Manuel de référence de Spring Batch au format HTML"). SpringSource faisant bien les choses, les scripts DDL de différentes solutions du marché (ex : MySQL, Oracle, DB2, SQL Server, Postgres, H2 …) sont disponibles dans le package org.springframework.batch.core du JAR spring-batch-core-xxx.jar  
Qui dit base de données, dit **dimensionnement** de cette dernière. L’ **espace disque requis** est alors **fonction** du **nombre d’exécutions** estimé, de la **nature des informations contextuelles persistées** et de la **durée de rétention** des données. Cette démarche prend tout son sens lorsqu’une instance de base de données est dédiée au schéma de Spring Batch.  En faisant quelques hypothèses (ex : sur le taux d’échec) et en mesurant le volume occupé sur plusieurs exécutions des batchs, il est possible de prévoir assez finement l’espace occupé par les données.

A moins de disposer de ressources infinies ou de n’avoir qu’un seul batch annuel, il est fréquent de fixer une durée de rétention de l’historique. Première option : demander à l’équipe d’exploitation de régulièrement lancer un script SQL de purge. Deuxième option : **utiliser Spring Batch pour purger ses propres données** !!

## Une Tasklet pour purger les données

De base, Spring Batch n’offre pas cette fonctionnalité. Et sur le Jira de SpringSource, je n’ai pas trouvé de demandes d’évolutions allant dans ce sens. Dans le ticket [BATCH-1747](https://jira.springsource.org/browse/BATCH-1747), Lucas Ward, commiteur Spring Batch,  invite les personnes intéressées à passer par des requêtes SQL de suppression après désactivation des contraintes d’intégrité.

Partant de ce constat, je me suis lancé dans l’écriture d’une **tasklet** **permettant de ne conserver l’historique Spring Batch des N derniers mois**.  Surement perfectible, en voici le résultat :

```java
public class RemoveSpringBatchHistoryTasklet implements Tasklet, InitializingBean {

    /**
     * SQL statements removing step and job executions compared to a given date.
     */
    private static final String  SQL_DELETE_BATCH_STEP_EXECUTION_CONTEXT = "DELETE FROM %PREFIX%STEP_EXECUTION_CONTEXT WHERE STEP_EXECUTION_ID IN (SELECT STEP_EXECUTION_ID FROM %PREFIX%STEP_EXECUTION WHERE JOB_EXECUTION_ID IN (SELECT JOB_EXECUTION_ID FROM  %PREFIX%JOB_EXECUTION where CREATE_TIME < ?))";
    private static final String  SQL_DELETE_BATCH_STEP_EXECUTION         = "DELETE FROM %PREFIX%STEP_EXECUTION WHERE JOB_EXECUTION_ID IN (SELECT JOB_EXECUTION_ID FROM %PREFIX%JOB_EXECUTION where CREATE_TIME < ?)";
    private static final String  SQL_DELETE_BATCH_JOB_EXECUTION_CONTEXT  = "DELETE FROM %PREFIX%JOB_EXECUTION_CONTEXT WHERE JOB_EXECUTION_ID IN (SELECT JOB_EXECUTION_ID FROM  %PREFIX%JOB_EXECUTION where CREATE_TIME < ?)";
    private static final String  SQL_DELETE_BATCH_JOB_EXECUTION_PARAMS   = "DELETE FROM %PREFIX%JOB_EXECUTION_PARAMS WHERE JOB_EXECUTION_ID IN (SELECT JOB_EXECUTION_ID FROM %PREFIX%JOB_EXECUTION where CREATE_TIME < ?)";
    private static final String  SQL_DELETE_BATCH_JOB_EXECUTION          = "DELETE FROM %PREFIX%JOB_EXECUTION where CREATE_TIME < ?";
    private static final String  SQL_DELETE_BATCH_JOB_INSTANCE           = "DELETE FROM %PREFIX%JOB_INSTANCE WHERE JOB_INSTANCE_ID NOT IN (SELECT JOB_INSTANCE_ID FROM %PREFIX%JOB_EXECUTION)";

    /**
     * Default value for the table prefix property.
     */
    private static final String  DEFAULT_TABLE_PREFIX                    = AbstractJdbcBatchMetadataDao.DEFAULT_TABLE_PREFIX;

    /**
     * Default value for the data retention (in month)
     */
    private static final Integer DEFAULT_RETENTION_MONTH                 = 6;

    private String               tablePrefix                             = DEFAULT_TABLE_PREFIX;

    private Integer              historicRetentionMonth                  = DEFAULT_RETENTION_MONTH;

    private JdbcTemplate         jdbcTemplate;

    private static final Logger  LOG                                     = LoggerFactory.getLogger(RemoveSpringBatchHistoryTasklet.class);

    @Override
    public RepeatStatus execute(StepContribution contribution, ChunkContext chunkContext) {
        int totalCount = 0;
        Date date = DateUtils.addMonths(new Date(), -historicRetentionMonth);
        DateFormat df = new SimpleDateFormat();
        LOG.info("Remove the Spring Batch history before the {}", df.format(date));

        int rowCount = jdbcTemplate.update(getQuery(SQL_DELETE_BATCH_STEP_EXECUTION_CONTEXT), date);
        LOG.info("Deleted rows number from the BATCH_STEP_EXECUTION_CONTEXT table: {}", rowCount);
        totalCount += rowCount;

        rowCount = jdbcTemplate.update(getQuery(SQL_DELETE_BATCH_STEP_EXECUTION), date);
        LOG.info("Deleted rows number from the BATCH_STEP_EXECUTION table: {}", rowCount);
        totalCount += rowCount;

        rowCount = jdbcTemplate.update(getQuery(SQL_DELETE_BATCH_JOB_EXECUTION_CONTEXT), date);
        LOG.info("Deleted rows number from the BATCH_JOB_EXECUTION_CONTEXT table: {}", rowCount);
        totalCount += rowCount;

        rowCount = jdbcTemplate.update(getQuery(SQL_DELETE_BATCH_JOB_EXECUTION_PARAMS), date);
        LOG.info("Deleted rows number from the BATCH_JOB_EXECUTION_PARAMS table: {}", rowCount);
        totalCount += rowCount;

        rowCount = jdbcTemplate.update(getQuery(SQL_DELETE_BATCH_JOB_EXECUTION), date);
        LOG.info("Deleted rows number from the BATCH_JOB_EXECUTION table: {}", rowCount);
        totalCount += rowCount;

        rowCount = jdbcTemplate.update(getQuery(SQL_DELETE_BATCH_JOB_INSTANCE));
        LOG.info("Deleted rows number from the BATCH_JOB_INSTANCE table: {}", rowCount);
        totalCount += rowCount;

        contribution.incrementWriteCount(totalCount);

        return RepeatStatus.FINISHED;
    }

    protected String getQuery(String base) {
        return StringUtils.replace(base, "%PREFIX%", tablePrefix);
    }

    public void setTablePrefix(String tablePrefix) {
        this.tablePrefix = tablePrefix;
    }

    public void setHistoricRetentionMonth(Integer historicRetentionMonth) {
        this.historicRetentionMonth = historicRetentionMonth;
    }

    public void setJdbcTemplate(JdbcTemplate jdbcTemplate) {
        this.jdbcTemplate = jdbcTemplate;
    }

    @Override
    public void afterPropertiesSet() throws Exception {
        Assert.notNull(jdbcTemplate, "The jdbcTemplate must not be null");
    }

}
```

Le code source de la classe **[RemoveSpringBatchHistoryTasklet](https://github.com/arey/spring-batch-toolkit/blob/master/src/main/java/com/javaetmoi/core/batch/tasklet/RemoveSpringBatchHistoryTasklet.java)** et sa classe de tests unitaires sont disponibles sur le **projet Github [spring-batch-toolkit](https://github.com/arey/spring-batch-toolkit/)**.

Cette tasklet peut être utilisée de 2 manières :

1. Dans un batch dédié à la purge de l’historique Spring Batch, batch qui pourrait par exemple être exécuté mensuellement ou annuellement selon la durée de rétention choisie.
1. Dans un step ajouté à un batch existant, par exemple en tant que step final.

Sur mon projet, nous avons opté pour l’option n°2 afin de ne pas démultiplier le nombre de batchs et parce que la mise en production d’un batch ainsi que sa planification s’avèrent toujours laborieux.

Outre le fait de valider les requêtes SQL et leur ordonnancement, le **test unitaire** permet de se parer face à une éventuelle **migration de schéma** suite à une montée de version de Spring Batch.

## Conclusion

Qui mieux que Spring Batch peut exécuter un traitement de purge pouvant potentiellement manipuler des enregistrements en masse ? Vous connaissez désormais la réponse.

Pour parfaire le code, il aurait été intéressant de déplacer l’exécution des requêtes SQL dans  un DAO héritant de la classe **AbstractJdbcBatchMetadataDao**. Outre un meilleur design, cela aurait permis de faire un appel au DAO de purge ailleurs que dans un batch. Une telle fonctionnalité pourrait très bien avoir sa place dans la console de [Spring Batch Admin](http://static.springsource.org/spring-batch-admin/ "Page d'accueil du projet Spring Batch Admin").

