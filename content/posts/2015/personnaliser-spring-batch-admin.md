---
_edit_last: "1"
author: admin
categories:
  - retour-d'expérience
date: "2015-06-23T19:15:14+00:00"
toc: true
thumbnail: wp-content/uploads/2015/06/spring-batch-admin-screenshot.jpg
featureImage: wp-content/uploads/2015/06/spring-batch-admin-screenshot.jpg
featureImageAlt: "spring-batch-admin-screenshot"
guid: http://javaetmoi.com/?p=1410
parent_post_id: null
post_id: "1410"
post_views_count: "9255"
summary: |-
  [![spring-batch-admin-screenshot](wp-content/uploads/2015/06/spring-batch-admin-screenshot.jpg)](wp-content/uploads/2015/06/spring-batch-admin-screenshot.jpg) Pour rappel, **Spring Batch Admin** est une **console de supervision des traitements par lots implémentés avec Spring Batch**. En plus d'un **frontal web**, elle offre une **API JSON** et expose des métriques via JMX.
  Bien que dépendant du projet Spring Batch, Spring Batch Admin dispose de [son propre repo GitHub](https://github.com/spring-projects/spring-batch-admin) et de son propre cycle de vie. Cet article se base sur la [version 2.0.0.M1 sortie en janvier 2015.](https://spring.io/blog/2015/01/16/spring-batch-and-spring-batch-admin-releases) Développé en Spring MVC et composé de 3 JARs, Spring Batch Admin peut aussi bien être intégrée dans une application existante que déployée dans son propre WAR.

  Ouvert aux extensions, Spring Batch Admin a tout pour devenir un véritable **serveur de batchs** : monitoring, chargement et mise à jour à chaud de la configuration des jobs, ordonnancement, exécution de jobs sur réception de fichiers …
  En 3 ans, c'est la seconde fois que je suis amené à personnaliser Spring Batch Admin. Le manuel de référence fourmille d'explications. Ce billet recense quelques informations complémentaires qui, je l'espère, pourront vous être utiles :

  - Transformer Spring Batch Admin en une application auto-exécutable embarquant sa propre base de données et son propre conteneur de servlet
  - Personnaliser l’interface d’admin
  - Adapter les templates FreeMarker au besoin métier
  - Exécuter un job suite à la réception d’un fichier
  - Router un message en fonction du résultat de l’exécution d’un job
  - Ajouter un contrôleur REST

  ![spring-batch-admin-screenshot](wp-content/uploads/2015/06/spring-batch-admin-screenshot.jpg)
tags:
  - spring-batch
  - spring-integration
title: Personnaliser Spring Batch Admin
url: /2015/06/personnaliser-spring-batch-admin/

---
[![spring-batch-admin-screenshot](wp-content/uploads/2015/06/spring-batch-admin-screenshot.jpg)](wp-content/uploads/2015/06/spring-batch-admin-screenshot.jpg) Pour rappel, **Spring Batch Admin** est une **console de supervision des traitements par lots implémentés avec Spring Batch**. En plus d'un **frontal web**, elle offre une **API JSON** et expose des métriques via JMX.
Bien que dépendant du projet Spring Batch, Spring Batch Admin dispose de [son propre repo GitHub](https://github.com/spring-projects/spring-batch-admin) et de son propre cycle de vie. Cet article se base sur la [version 2.0.0.M1 sortie en janvier 2015.](https://spring.io/blog/2015/01/16/spring-batch-and-spring-batch-admin-releases) Développé en Spring MVC et composé de 3 JARs, Spring Batch Admin peut aussi bien être intégrée dans une application existante que déployée dans son propre WAR.

Ouvert aux extensions, Spring Batch Admin a tout pour devenir un véritable **serveur de batchs** : monitoring, chargement et mise à jour à chaud de la configuration des jobs, ordonnancement, exécution de jobs sur réception de fichiers …
En 3 ans, c'est la seconde fois que je suis amené à personnaliser Spring Batch Admin. Le manuel de référence fourmille d'explications. Ce billet recense quelques informations complémentaires qui, je l'espère, pourront vous être utiles :

- Transformer Spring Batch Admin en une application auto-exécutable embarquant sa propre base de données et son propre conteneur de servlet
- Personnaliser l’interface d’admin
- Adapter les templates FreeMarker au besoin métier
- Exécuter un job suite à la réception d’un fichier
- Router un message en fonction du résultat de l’exécution d’un job
- Ajouter un contrôleur REST

## Pré-requis

Certaines classes utilisées dans ce billet sont issues [du projet **spring-batch-toolkit** hébergé sur GitHub](https://github.com/arey/spring-batch-toolkit). Disponible sur Maven Central, n’hésitez pas à l’utiliser sur vos projets.

## Créer sa propre application

Pour créer from scratch une application Spring Batch Admin, le plus simple consiste à s'inspirer de l'application web d'exemple [spring-batch-admin-sample](https://github.com/spring-projects/spring-batch-admin/tree/master/spring-batch-admin-sample) : pom.xml maven, web.xml, index.jsp, fichiers de configuration XML et properties pourront être repris puis adaptés.

Pour stocker l’historique de l’exécution des jobs dans une base de données HSQLDB, la recopie des fichiers `batch-hsql.properties` et `business-schema-hsqldb.sql` s’avère nécessaire. Remplacer `hsql` par le nom d’une autre base supportée.

A noter que [l’IHM devrait être retirée de la version finale de Spring Batch Admin 2.0.0](https://jira.spring.io/browse/BATCHADM-214) et déplacée dans un projet sample séparé. Il sera donc alors nécessaire de reprendre les templates FreeMarker, les ressources statiques et le code Java lié à la UI.

## Personnaliser le nom de l'application et de la société

Les différents libellés affichés dans l'en-tête et le pied page de l'application Spring Batch Admin peuvent être chargés depuis un ressource bundle `messages`.

Pour se faire, créer un fichier `messsages.properties` dans le répertoire `src/main/resources` de votre projet. Puis ajouter et personnaliser les propriétés suivantes :

```java
site.name=Java & Moi Blog
company.url=/
company.name=Java & Moi
product.url=/tags/spring-batch
product.name=Batch Server
copyright=2015 Java & Moi
company.contact.url=/about/
company.contact=Contact
```

Créer  ensuite le fichier de configuration Spring _src/main/resources/META-INF/spring/batch/servlet/override/ **manager-context.xml**_ et déclarer le bean `messageSource` :

```xhtml
<?xml version="1.0" encoding="UTF-8"?>
<beans xmlns="http://www.springframework.org/schema/beans"
       xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
       xsi:schemaLocation="http://www.springframework.org/schema/beans
           http://www.springframework.org/schema/beans/spring-beans-3.0.xsd">
  <!-- Override messageSource bean in order to provide custom text content -->
  <bean id="messageSource" class="org.springframework.context.support.ResourceBundleMessageSource">
    <property name="basename" value="messages" />
  </bean>
</beans>
```

## Personnaliser le logo

Déployer Spring Batch Admin avec le logo de SpringSource, c'est bien. Le déployer avec le logo de votre société ou de votre client, c'est mieux.
Pour changer de logo :

1. Copier l'image spring-batch-admin-resources-2.0.0.M1.jar!/META-INF/images/header-right.png dans le répertoire webapp/images/header-right.png
1. Ouvrir ce fichier avec votre éditeur préféré (Gimp, Paint.NET …) et remplacer le logo SpringSource par celui de votre choix. Attention aux bords arrondis.

## Paramétrer le nombre de jobs exécutés en parallèle

Pour exécuter les jobs, Spring Batch Admin s'appuie sur la classe `SimpleJobLauncher` de Spring Batch. Son pool de threads est dimensionné à 6 threads. De ce fait, un maximum de 6 jobs peuvent être exécutés simultanément. Pour augmenter ou diminuer le nombre de thread, il est nécessaire de redéfinir le bean `jobLauncherTaskExecutor`

Ajouter un fichier `META-INF/spring/batch/override/execution-context.xml` contenant la définition de bean :

```xhtml
<?xml version="1.0" encoding="UTF-8"?>
<beans xmlns="http://www.springframework.org/schema/beans"
       xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
       xmlns:task="http://www.springframework.org/schema/task"
       xsi:schemaLocation="http://www.springframework.org/schema/beans http://www.springframework.org/schema/beans/spring-beans.xsd
      http://www.springframework.org/schema/task http://www.springframework.org/schema/task/spring-task.xsd">
    <!-- Override jobLauncherTaskExecutor bean in order to customize the pool-size -->
    <task:executor id="jobLauncherTaskExecutor" pool-size="${batch.job.threadpool.size}" rejection-policy="ABORT" />
</beans>
```

Puis ajouter la propriété `batch.job.threadpool.size` dans le fichier `batch-<xxx>.properties` :

```java
## Maximum jobs that could be launched in parallel
batch.job.threadpool.size=10
```

Remarque : un autre moyen de contrôler le nombre de traitements réalisés en parallèle est d'utiliser le `poolTaskExecutor` déclaré par Spring Batch Admin (mais non utilisé par ce dernier). C'est particulièrement vrai si vos Jobs utilisent des [techniques de parallélisation](/2012/12/parallelisation-de-traitements-batchs-spring-batch/) tels le partitionnement ou la parallélisation de steps. Mutualiser le pool de threads sur plusieurs jobs permet un dimensionnement optimal : les ressources serveur seront ainsi réparties en fonction de la charge globale. Lorsqu'un seul job est exécuté, ce dernier pourra profiter de l'intégralité des threads mis à disposition du serveur de batch (600 par défaut).

## Une base de données auto-installable

Pour fonctionner, Spring Batch Admin nécessite une base de données. C'est la base qui lui permet de suivre l'exécution des batchs. Tous les jobs à monitorer, qu'ils soient exécutés dans Spring Batch Admin ou depuis un autre serveur, doivent utiliser un `JobRepository` persistant. Et ceci, même si vos jobs ne font que de la manipulation de fichiers.

Si vos batchs n'ont pas besoin de base de données pour fonctionner, la création de la base peut être confiée à Spring Batch Admin lors de son démarrage.
Nativement, Spring Batch Admin ne sait pas automatiquement détecter si la base existe. L’utilisateur doit lui spécifier ou non de (re)créer la base via la propriété `batch.data.source.init` exploitée dans le fichier `/META-INF/spring/batch/bootstrap/manager/data-source-context.xml` de spring- `batch-admin-manager-2.0.0.M1.jar`

En redéfinissant le bean `initialize-database`, Spring Batch Admin peut être configuré pour ne créer le schéma que s’il n’existe pas. L’exécution du script de destruction du schéma est retirée et on précise à Spring d’ignorer les erreurs. Ainsi, si une table existe, l’exécution du CREATE TABLE ne fera pas échouer l’exécution du script.

En pratique, créer dans votre web app un fichier `META-INF/spring/batch/override/data-source-context.xml` contenant le bean suivant :

```xhtml
<jdbc:initialize-database data-source="dataSource" enabled="true" ignore-failures="ALL">
    <jdbc:script location="${batch.schema.script}"/>
    <jdbc:script location="${batch.business.schema.script}"/>
</jdbc:initialize-database>
```

Pour supprimer une base, supprimer le répertoire racine contenant ses fichiers.

## Packager Spring Batch Admin

Au début de ce billet, nous avons vu comment distribuer Spring Batch Admin dans son propre WAR ou comment l’inclure dans une application web existante.
Se posera ensuite la question de l’installation. L’installation de la base de données a déjà été abordée dans un paragraphe précédent. Concentrons nous à présent sur le conteneur de servlet. Au lieu de devoir installer préalablement sur le serveur un conteneur web comme Jetty ou Tomcat, je vous propose de l’embarquer directement dans le binaire de Spring Batch Admin. A la manière de Spring Boot, il est possible de démarrer Jetty depuis un simple main.
Pour y arriver, je vous invite à suivre le tutoriel [Embarquer Jetty dans une web app](/2015/06/web-app-jetty-standalone/) récemment publié sur ce blog.

## Exécuter un job suite à la réception d’un fichier

Spring Batch Admin offre une intégration poussée de Spring Integration avec Spring Batch. Le chargement à chaud de la configuration XML d’un nouveau job utilise précisément un adaptateur de type file ( `<file:inbound-channel-adapter>`) pour détecter la mise à disposition d’un nouveau fichier. Pour davantage de détails, je vous invite à consulter le fichier `META-INF/spring/batch/bootstrap/integration/configuration-context.xml` du module `spring-batch-admin-manager`.

La UI et les endpoints REST de Spring Batch Admin offrent la possibilité d’uploader un fichier qui sera déposé dans le `pusblish-subscribe-channel` nommé `input-file` et déclaré dans le fichier `META-INF/spring/batch/bootstrap/integration/file-context.xml` du module `spring-batch-admin-manager`. Charge au développeur de s’abonner au channel pour, par exemple, déclencher un job.

En combinant ces 2 fonctionnalités, il est possible de déclencher l’exécution d’un job Spring Batch lors de la réception d’un fichier dans un répertoire donné. Ce cas d’utilisation est particulièrement intéressant lorsque le job exécuté prend en entrée le fichier reçu.
Pour exemple, on peut imaginer un batch chargé de prendre un fichier CSV et d’insérer chaque ligne dans une base de données NoSQL. Le chemin complet du fichier est passé au batch à l’aide du paramètre `input.file`. Le chemin du fichier est préfixé par `file://` Le nom du job à déclencher est déduit du nom du fichier à partir, par exemple, d’une convention de nommage.

La **première étape** consiste à créer le fichier `META-INF/spring/batch/override/admin-context.xml` et à déclarer toute une série d’espaces de nom :

```xhtml
<?xml version="1.0" encoding="UTF-8"?>
<beans xmlns="http://www.springframework.org/schema/beans"
       xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
       xmlns:context="http://www.springframework.org/schema/context"
       xmlns:file="http://www.springframework.org/schema/integration/file"
       xmlns:int="http://www.springframework.org/schema/integration"
       xmlns:int-mail="http://www.springframework.org/schema/integration/mail"
       xmlns:bean="http://www.springframework.org/schema/beans"
       xsi:schemaLocation="http://www.springframework.org/schema/integration http://www.springframework.org/schema/integration/spring-integration.xsd
      http://www.springframework.org/schema/beans http://www.springframework.org/schema/beans/spring-beans.xsd
      http://www.springframework.org/schema/context http://www.springframework.org/schema/context/spring-context.xsd
      http://www.springframework.org/schema/integration http://www.springframework.org/schema/integration/spring-integration.xsd
      http://www.springframework.org/schema/integration/file http://www.springframework.org/schema/integration/file/spring-integration-file.xsd
      http://www.springframework.org/schema/integration/mail http://www.springframework.org/schema/integration/mail/spring-integration-mail.xsd">
```

La **seconde étape** consiste à brancher un `<file:inbound-channel-adapter>` sur le channel `input-files` existant. Ainsi, que ce soit par un upload de fichier via HTTP ou un transfert de fichier par SFTP, CFT ou rsync, la suite du traitement du fichier est identique.

```xhtml
<file:inbound-channel-adapter directory="/data/sas-in" channel="input-files" filename-pattern="*.csv" prevent-duplicates="true">
    <int:poller max-messages-per-poll="10" fixed-rate="1000"/>
</file:inbound-channel-adapter>
```

Le corps du message déposé dans le channel `input-files` est de type `File`.

Une **3ième étape** consiste à transformer ce fichier en une demande d’exécution de job, à savoir un objet de type `JobLaunchRequest` (appartenant au module `spring-batch-integration`).

Une chaîne de 2 endpoints est nécessaire :

```xhtml
<context:annotation-config/>
<int:chain input-channel="input-files" output-channel="job-requests">
    <int:service-activator>
        <bean class="com.javaetmoi.core.batch.integration.DynamicFileToJobLaunchRequestAdapter "/>
    </int:service-activator>
    <int:transformer>
        <bean class="org.springframework.batch.admin.integration.LastJobParametersJobLaunchRequestEnhancer">
            <property name="jobService" ref="jobService"/>
        </bean>
    </int:transformer>
</int:chain>
```

L’auto-wiring est activé pour faciliter l’injection de beans dans la classe [**FilenameToJobLaunchRequestAdapter**](https://github.com/arey/spring-batch-toolkit/blob/blog-spring-batch-admin/src/main/java/com/javaetmoi/core/batch/integration/DynamicFileToJobLaunchRequestAdapter.java). En interne, cet adaptateur fait appel à un bean implémentant l’interface [FileToJobNameConverter](https://github.com/arey/spring-batch-toolkit/blob/blog-spring-batch-admin/src/main/java/com/javaetmoi/core/batch/integration/FileToJobNameConverter.java) qui est capable de déduire le nom du job à exécuter en fonction du nom du fichier.

Voici un exemple d’implémentation :

```java
@Service
public class CsvFileToJobConverter implements FileToJobNameConverter {

    private final static String FILE`NAME`PATTERN = "(\\w*)_(.*)\\.csv";
    private static final String JOB_SUFFIX = "Job";

    @Override
    public String getJobNameFromFile(File file) throws NoSuchJobException {
        String filename = file.getName().trim().toLowerCase(Locale.FRANCE);
        if (!filename.matches(FILE`NAME`PATTERN)) {
            throw new NoSuchJobException("Filename in wrong format: "+filename);

        }
        return filename.replaceAll(FILE`NAME`PATTERN, "$1") + JOB_SUFFIX;
    }
}
```

A l’issu de l’exécution du `FilenameToJobLaunchRequestAdapter`, une instance de `JobLaunchRequest` est créée et envoyée sur le channel. Fourni par Spring Batch Admin, le transformeur `LastJobParametersJobLaunchRequestEnhancer` complète les paramètres de lancement du job en reprenant ceux utilisés lors de la dernière exécution du job.
L’infrastructure de Spring Batch Admin prend ensuite la relève : récupérant le `JobLaunchRequest` depuis le channel `job-requests`, elle fait appel à un `SimpleJobLauncher` pour exécuter immédiatement le job. Une instance de `JobExecution` est alors déposée dans le channel `job-operator`.

## Attendre la fin de l’exécution d’un batch

La classe `SimpleJobLauncher` délègue l’exécution  des jobs à un pool de threads. Elle rend donc la main avant la fin de l’exécution du job.
Dans la milestone 2.0.0-M1 de Spring Batch Admin, les messages déposés dans le channel `job-operator` sont simplement loggés. Un TODO présage que, dans une prochaine version, Spring Batch Admin proposera de réaliser des traitements en fonction de l’exécution du batch. Extrait de la configuration _[META-INF/spring/batch/bootstrap/integration/launcher-context.xml](https://github.com/spring-projects/spring-batch-admin/blob/2.0.0.M1/spring-batch-admin-manager/src/main/resources/META-INF/spring/batch/bootstrap/integration/launcher-context.xml)_:

```xhtml
<!-- TODO: filter into success and failure channels -->
<publish-subscribe-channel id="job-operator" />

<logging-channel-adapter channel="job-operator" />
```

En attendant, la classe [**JobExitStatusRouter**](https://github.com/arey/spring-batch-toolkit/blob/blog-spring-batch-admin/src/main/java/com/javaetmoi/core/batch/integration/JobExitStatusRouter.java) de `spring-batch-toolkit` permet de router le message dans 2 channels en fonction du code de retour du job ( `ExitStatus`) :

```xhtml
<int:router input-channel="job-operator">
    <bean class="com.javaetmoi.core.batch.integration.JobExitStatusRouter"/>
</int:router>

<int:publish-subscribe-channel id="job-success"/>
<int:publish-subscribe-channel id="job-error"/>
```

Pour accéder au code de retour du job, la classe `JobExitStatusRouter` attend la fin de son exécution. L’implémentation est très sommaire puisqu’elle utilise la technique du pooling pour interroger à intervalle réguler le statut du job.
Un mécanisme de notification aurait été préférable. Mais à ma connaissance, Spring Bach n’offre pas nativement une telle possibilité.

## Envoi d’un mail en cas d’erreur

Lorsque le batch tombe en erreur, si ce dernier ne propose pas déjà un système d’alertes, il est possible d’envoyer un mail à l’équipe en charge de sa supervision.
Disponible dans le projet `spring-batch-toolkit`, la classe [**JobExecutionToMailOutTransformer**](https://github.com/arey/spring-batch-toolkit/blob/blog-spring-batch-admin/src/main/java/com/javaetmoi/core/batch/integration/JobExecutionToMailOutTransformer.java) permet de construire le corps du mail à partir du `JobExecution` récupérée dans le channel `job-error`. Est ensuite utilisé les endpoints du module `spring-integration-mail` pour compléter le mail puis l’envoyer :

```xhtml
<chain input-channel="job-error" xmlns="http://www.springframework.org/schema/integration">
    <filter expression="${batch.mail.error.alert}"/>
    <transformer>
        <bean:bean class="com.javaetmoi.core.batch.integration.JobExecutionToMailOutTransformer"/>
    </transformer>
    <int-mail:header-enricher>
        <int-mail:subject value="${batch.mail.error.subject}"/>
        <int-mail:to value="${batch.mail.error.to}"/>
        <int-mail:cc value="${batch.mail.error.cc}"/>
        <int-mail:from value="${batch.mail.error.from}"/>
    </int-mail:header-enricher>
    <int-mail:outbound-channel-adapter host="${batch.mail.server.host}"
                                       username="${batch.mail.server.username}"
                                       password="${batch.mail.server.password}"/>
</chain>
```

## Personnaliser un template JSON

En fonction des besoins métiers, il est parfois nécessaire de devoir modifier ou compléter la réponse d’un service REST de Spring Batch Admin.
Qu’elles soient en RSS, XML ou JSON, les réponses sont templatisées avec FreeMarker.
En attendant la prise en compte du ticket [BATCHADM-223](https://jira.spring.io/browse/BATCHADM-223), j’ai par exemple été contraint de transformer une map en un array. Issu du JAR `spring-batch-admin-manager-2.0.0-M1.jar`, le fichier `org/springframework/batch/admin/web/manager/jobs/json/executions.ftl` a été dupliqué puis renommé en `executions-custom.ftl`. Il a été placé dans un package identique.

Une fois le template modifié, la redéfinition du bean **jobs/executions.json** a été réalisé dans le fichier `/META-INF/spring/batch/servlet/override/manager-context.xml`:

```xhtml
<!-- Override provided beans in order to use our custom FreeMarker template -->
<bean name="jobs/executions.json" parent="standard.json">
    <property name="attributes">
        <props merge="true">
            <prop key="body">/manager/jobs/json/executions-custom.ftl</prop>
        </props>
    </property>
</bean>
```

## Empêcher l’exécution simultanée d’un même job

Précédemment, nous avons vu comment la réception d’un fichier peut déclencher l’exécution d’un job. Mais que se passe-t-il lorsque 2 fichiers sont reçus et que ces 2 fichiers déclenchent le même job ? Et bien 2 instances du job sont créés puis exécutées en parallèle. Ce comportement peut introduire des effets de bord. Il peut alors être nécessaire de sérialiser le traitements de ces fichiers.

Comme son nom l’indique, la classe [**AcceptOnceFilePerJobListFilter**](https://github.com/arey/spring-batch-toolkit/blob/blog-spring-batch-admin/src/main/java/com/javaetmoi/core/batch/integration/AcceptOnceFilePerJobListFilter.java) du projet spring-batch-toolkit permet de n’exécuter à la fois qu’une seule instance du même job. Elle s’appuie sur l’interface [FileToJobNameConverter](https://github.com/arey/spring-batch-toolkit/blob/blog-spring-batch-admin/src/main/java/com/javaetmoi/core/batch/integration/FileToJobNameConverter.java) utilisée précédemment. Le nom du job que le fichier va déclencher est conservé en mémoire.

L’attribut **filter** du `<file:inbound-channel-adapter>` doit alors être paramétré de la manière suivante :

```xhtml
<file:inbound-channel-adapter directory="/data/sas-in" channel="input-files" filter="receivedFileListFilter">
    <int:poller max-messages-per-poll="10" fixed-rate="1000" task-executor="receivedFileTaskExecutor"/>
</file:inbound-channel-adapter>

<bean id="receivedFileListFilter" class="org.springframework.integration.file.filters.CompositeFileListFilter">
    <constructor-arg>
        <list>
            <bean class="org.springframework.integration.file.filters.SimplePatternFileListFilter">
                <constructor-arg value="*.csv"/>
            </bean>
	    <bean ref="acceptOnceFilePerJobListFilter"/>
        </list>
    </constructor-arg>
</bean>

<bean id="acceptOnceFilePerJobListFilter" class="com.javaetmoi.core.batch.integration.AcceptOnceFilePerJobListFilter">
    <property name="fileToJobNameConverter" ref="fileToJobNameConverter"/>
</bean>

<bean id="rollbackProcessedCatalogServiceActivator" class="com.sparkow.batch.admin.endpoint.RollbackProcessedFileServiceActivator">
    <property name="acceptOnceCatalogListFilter" ref="acceptOnceCatalogListFilter"/>
</bean>
```

Une fois l’exécution du job terminée, il est nécessaire de notifier le bean **acceptOnceCatalogListFilter** afin qu’il puisse de nouveau laisser passer les fichiers traités par ce job. C’est le rôle de la classe [**RollbackProcessedFileServiceActivator**](https://github.com/arey/spring-batch-toolkit/blob/blog-spring-batch-admin/src/main/java/com/javaetmoi/core/batch/integration/RollbackProcessedFileServiceActivator.java).

## Attendre la fin du chargement de la configuration XML des Jobs

Lorsque Spring Batch Admin démarre, les fichiers préalablement déposés dans le répertoire `/data/sas-in` sont analysés par l’ `inbound-channel-adapter` alors que la configuration XML du job chargé de les traiter n’est pas encore chargé. Le fichier tombe alors en erreur et est déplacé dans le répertoire `/data/sas-error`

Pour remédier à ce problème, une solution consiste à démarrer manuellement le bean de type `inbound-channel-adapter` du _« Root WebApplicationContext »_ initié par le `ContextLoaderListener` _._
Pour se faire, la propriété **auto-startup** doit être positionnée à `false` et un **id** doit être renseigné :

```xhtml
<file:inbound-channel-adapter id="fileInboundChannelAdapter"
directory="/data/sas-in" channel="input-files" filter="receivedFileListFilter" auto-startup="false">
```

Pour chaque job, Spring Batch Admin crée un contexte Spring. Qui plus est, le `DispatcherServlet` de Spring MVC déclaré dans le `web.xml` crée également un contexte applicatif enfant du _« Root WebApplicationContext »_ Au total, N+2 contextes Spring sont créés.

On démarre le bean `inbound-channel-adapter` une fois l’ensemble des contextes initialisés.  Le bean `ServerStartEventHandler` s’abonne aux évènements de type `ContextRefreshedEvent` émis par le conteneur Spring à chaque fois qu’un contexte applicatif est initialisé ou rafraichit :

```java
/**
 * Start the adapter that read CSV files once jobs xml configuration files are loaded.
 */
public class ServerStartEventHandler
        implements ApplicationListener<ContextRefreshedEvent> {

    @Override
    public void onApplicationEvent(ContextRefreshedEvent event) {
        ApplicationContext applicationContext = event.getApplicationContext();
        if (applicationContext.getDisplayName().contains("Batch Servlet-servlet")) {
            SourcePollingChannelAdapter adapter = (SourcePollingChannelAdapter) applicationContext.getBean("fileInboundChannelAdapter");
            adapter.start();
        }
    }
}
```

Au cours du démarrage, la méthode `onApplicationEvent` est appelée autant de fois que de contextes. Le nom du contexte Spring MVC qui est le dernier chargé contient le nom du servlet _« Batch Servlet »._

## Ajouter un contrôleur REST

Spring Batch Admin propose un frontal REST permettant d’accéder à des ressources au format HTML, RSS et JSON. Par exemple, un GET sur le chemin `/jobs/{jobName}/executions.json` listera l’historique des exécutions d’un job. De par l’extension, les données échangées sont au format JSON.
Ouvert aux extensions, Spring Batch Admin permet d’ajouter ses propres ressources REST.

La **première étape** consiste à ajouter un contrôleur Spring MVC respectant les propriétés suivantes :

- Hériter de la classe abstraite `AbstractBatchJobsController`
- Etre déclaré en tant que contrôleur REST via l’annotation `@RestController`
- Définir un chemin d’accès racine par l’annotation `@RequestMapping("/<nom ressource>")`
- Ajouter autant de handlers de requêtes HTTP que souhaité

Bien que tous les contrôleurs REST de Spring Batch Admin les utilisent, l’utilisation de Spring Data et Spring HATEOS est optionnelle.

Afin que ces nouvelles API soient connues des utilisateurs et apparaissent sur la page d’accueil, une **seconde étape** consiste à les déclarer dans un fichier properties normalisé. La clé contient le verbe HTTP et l’URI de la ressource. La valeur correspond au commentaire affiché sur la page d’accueil.
Voici un exemple de fichier `mycustom-json-resources.properties`:

```java
POST/myresource/{id}.json=Update an existing resource
GET/myresource.json=List all the resources, in order of the most recent to least.
```

La **3ième et dernière étape** consiste à déclarer le contrôleur et le fichier properties dans le fichier `META-INF/spring/batch/servlet/override/controller-context.xml` :

```xhtml
<?xml version="1.0" encoding="UTF-8"?>
<beans xmlns="http://www.springframework.org/schema/beans" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
       xmlns:util="http://www.springframework.org/schema/util"
       xsi:schemaLocation="http://www.springframework.org/schema/beans http://www.springframework.org/schema/beans/spring-beans.xsd
      http://www.springframework.org/schema/util http://www.springframework.org/schema/util/spring-util.xsd">

    <bean class="com.javaetmoi.batch.admin.web.MyResourceController"/>

    <util:properties id="jsonResources" location="classpath:/org/springframework/batch/admin/web/manager/json-resources.properties,
            classpath:com/javaetmoi/batch/admin/web/myresources-json-resources.properties"/>

</beans>
```

Le bean `jsonResources` fournit par Spring Batch Admin est ici redéfini afin de prendre en compte notre fichier properties personnalisé.
Le nom du répertoire `META-INF/spring/batch/servlet/override` est prédéfini par Spring Batch Admin. Ce dernier assure que les fichiers de configuration Spring s’y trouvant seront chargés après les siens, permettant ainsi au développeur de redéfinir des beans et/ou d’en ajouter.

## Conclusion

Afin de pouvoir personnaliser de manière avancée Spring Batch Admin, une appropriation de son code source est nécessaire. Il est en effet fréquent de devoir identifier les beans qui devront être redéfinis.

Pour la version 2.0.0, l’équipe de Spring Batch Admin ambitionne de déplacer le frontal web dans une application démo. Une fois réalisée, certaines explications données dans ce billet seront obsolètes. En contre partie, ce changement d’architecture devrait simplifier la personnalisation de l’interface utilisateur et permettre, par exemple, [l'internationalisation des IHM](https://jira.spring.io/browse/BATCHADM-215).

Depuis janvier 2015 et la release de la 2.0.0-M1, le [repo github Spring Batch](https://github.com/spring-projects/spring-batch-admin/commits/master) recense peu d’activités. Le chemin vers la version 2.0.0 semble donc encore loin. Au cours de mes développements, j’ai soumis [7 pull request](https://github.com/spring-projects/spring-batch-admin/pulls/arey) et [8 tikets Jira](https://jira.spring.io/browse/BATCHADM-223?jql=project%20%3D%20BATCHADM%20AND%20reporter%20in%20(elryk)). Certaines ont dors et déjà acceptées pour la version 2.0.0. D’autres restent à valider et à planifier. J’ai hâte de les retrouver et de pouvoir ainsi simplifier mon code.
