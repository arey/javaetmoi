---
_edit_last: "1"
author: admin
categories:
  - retour-d'expérience
  - spring
date: "2022-07-03T12:25:17+00:00"
guid: https://javaetmoi.com/?p=2217
parent_post_id: null
post_id: "2217"
post_views_count: "15663"
summary: "Dans une **grande entreprise**, le **développement d’applications métiers** doit respecter les **règles** en vigueur : normes de développement, normes de sécurité, barrière qualité, socle technique borné, intégration à l’usine de dév …{{ double-space-with-newline }}Le **démarrage d’une nouvelle application Java** peut être accélérée de bien des manières : usage d’outils Low Code comme [Palmyra](https://www.vermeg.com/fr/produit-palmyra/), générateur de squelettes d’application comme [JHipster](https://www.jhipster.tech/), utilisation d’applications blanches déclinées par catégorie d’appli (ex : batch, web), copier/coller/élagage d’une application de référence, guide de démarrage sous forme wiki … Chaque technique présente ses avantages et ses inconvénients. Mais certaines ne couvrent pas toutes les règles évoquées précédemment.{{ double-space-with-newline }}Afin d’ **accélérer le développement** d’une nouvelle application, mon objectif était de générer un **squelette d’application minimaliste** dont le code généré est parfaitement maitrisé et avec des **dépendances choisies à la carte** par le tech lead. Libre à lui ensuite de retravailler le code généré pour mettre en place l’architecture cible de l’application, en choisissant par exemple de partir sur une architecture hexagonale.\n\n \n\nBien connu des développeurs Spring Boot, je me suis appuyé sur le code backend faisant tourner le site [https://start.spring.io/](https://start.spring.io/), à savoir le projet **[Spring Initializr](https://github.com/spring-io/initializr)** conçu et maintenu majoritairement par Stéphane Nicoll. Léger, codé en Java, reposant sur Spring Boot et documenté, ce projet a été conçu pour être personnalisé et extensible. Cela en a fait un excellent candidat.{{ double-space-with-newline }}La première mouture de ce générateur développé en quelques jours m’aura permis de générer :\n\n- la configuration du socle Spring Boot d’entreprise\n- la configuration du logger permettant de standardiser les logs au format JSON\n- la sécurisation des API REST avec Spring Security, OpenID Connect et le SSO d’entreprise\n- les contrôleurs et DTO d’une API REST à partir d’une spécification OpenAPI 3\n- le Dockerfile et la configuration du pipeline CI/CD"
tags:
  - openapi
  - spring-boot
  - spring-initializr
title: Générateur de squelette d’application basé sur Spring Initializr
url: /2022/07/generateur-de-squelette-dapplication-base-sur-spring-initializr/

---
Dans une **grande entreprise**, le **développement d’applications métiers** doit respecter les **règles** en vigueur : normes de développement, normes de sécurité, barrière qualité, socle technique borné, intégration à l’usine de dév …  
Le **démarrage d’une nouvelle application Java** peut être accélérée de bien des manières : usage d’outils Low Code comme [Palmyra](https://www.vermeg.com/fr/produit-palmyra/), générateur de squelettes d’application comme [JHipster](https://www.jhipster.tech/), utilisation d’applications blanches déclinées par catégorie d’appli (ex : batch, web), copier/coller/élagage d’une application de référence, guide de démarrage sous forme wiki … Chaque technique présente ses avantages et ses inconvénients. Mais certaines ne couvrent pas toutes les règles évoquées précédemment.  
Afin d’ **accélérer le développement** d’une nouvelle application, mon objectif était de générer un **squelette d’application minimaliste** dont le code généré est parfaitement maitrisé et avec des **dépendances choisies à la carte** par le tech lead. Libre à lui ensuite de retravailler le code généré pour mettre en place l’architecture cible de l’application, en choisissant par exemple de partir sur une architecture hexagonale.

{{< figure src="/wp-content/uploads/2022/07/logo-spring-boot.png" alt="" caption="" >}}

Bien connu des développeurs Spring Boot, je me suis appuyé sur le code backend faisant tourner le site [https://start.spring.io/](https://start.spring.io/), à savoir le projet **[Spring Initializr](https://github.com/spring-io/initializr)** conçu et maintenu majoritairement par Stéphane Nicoll. Léger, codé en Java, reposant sur Spring Boot et documenté, ce projet a été conçu pour être personnalisé et extensible. Cela en a fait un excellent candidat.  
La première mouture de ce générateur développé en quelques jours m’aura permis de générer :

- la configuration du socle Spring Boot d’entreprise
- la configuration du logger permettant de standardiser les logs au format JSON
- la sécurisation des API REST avec Spring Security, OpenID Connect et le SSO d’entreprise
- les contrôleurs et DTO d’une API REST à partir d’une spécification OpenAPI 3
- le Dockerfile et la configuration du pipeline CI/CD

## API REST

Le projet [Spring Initializr](https://github.com/spring-io/initializr) permet de développer un « **initializr** » d’applications maisons exposant une [API REST iso fonctionnelle](https://docs.spring.io/initializr/docs/current-SNAPSHOT/reference/html/#api-guide) à ce que fait Spring Initializr. Cet initialzr propriétaire peut donc être utilisé tel quel par différents outils s’interfaçant déjà ave l’API REST de Spring Initializr :

- depuis les principaux IDE Java du marché supportant Spring Initializr, nativement ou après installation d’un plugin : IntelliJ, Eclipse, STS, VSCode, NetBeans.
- en ligne de commande cUrl
- avec Spring Boot CLI
- et/ou une IHM web (adaptée ou non à partir du repo [spring-io/start.spring.io](https://github.com/spring-io/start.spring.io))

Un appel GET à l’API REST de l’initializr permet de renvoyer le paramétrage utilisés par les outils cités : choix du Langage (Java/Kotlin/Groovy), version de Java et de Spring Boot, outil de build (Maven/Gradle) ou bien encore les dépendances.

Extrait d’une réponse à un appel GET :

```
{
   "javaVersion":{
      "type":"single-select",
      "default":"11",
      "values":[
         {
            "id":"11",
            "name":"11"
         },
         {
            "id":"17",
            "name":"17"
         }
      ]
   },
   "bootVersion":{
      "type":"single-select",
      "default":"2.7.0.RELEASE",
      "values":[
         {
            "id":"2.7.0.RELEASE",
            "name":"2.7.0"
         }
      ]
   },
     "dependencies":{
      "type":"hierarchical-multi-select",
      "values":[
         {
            "name":"Java&Moi",
            "values":[
               {
                  "id":"openapi",
                  "name":"OpenAPI",
                  "description":"Configure the web application to expose a REST API designed with a contact-first OpenAPI Specification (OAS): \n - The openapi-generator-maven-plugin\n - SwaggerUI with Springdoc"
               }
            ]
         },
         {
            "name":"Spring",
            "values":[
               {
                  "id":"web",
                  "name":"Web",
                  "description":"Build web, including RESTful, applications using Spring MVC. Uses Apache Tomcat as the default embedded container."
               }
            ]
         }
      ]
   },
   ...
}

```

## Fil conducteur

Comme fil conducteur de ce billet, je vous propose de construire l’initializr **[javaetmoi-initializr](https://github.com/arey/javaetmoi-initializr)** chargé de générer la configuration d’une **application web Spring MVC** exposant une **API REST** en contract first au format OpenAPI 3. Le générateur configure le plugin **[openapi-generator-maven-plugin](https://openapi-generator.tech/docs/plugins/)** ainsi que **Springdoc** pour avoir accès à **Swagger UI**. C’est précisément le type d’architecture mis en œuvre sur le sample [spring-petclinic-rest](https://github.com/spring-petclinic/spring-petclinic-rest) (avec pour le moment Springfox à la place de Springdoc).

Depuis IntelliJ IDEA, voici les dépendances proposées :

{{< figure src="/wp-content/uploads/2022/07/image-1.png" alt="" caption="" >}}

Le code source de javaetmoi-initializr est disponible sur le repository : [arey/javaetmoi-initializr](https://github.com/arey/javaetmoi-initializr).

## Démarrage

Pour développer un initializr, commencez par créer une application Spring Boot à l’aide de [https://start.spring.io/](https://start.spring.io/) tout en ajoutant la dépendance **Spring Web** (ce qui déclarera l’artefact spring-boot-starter-web). Je recommande ensuite de suivre le paragraphe [Creating your own instance](https://docs.spring.io/initializr/docs/current-SNAPSHOT/reference/html/#create-instance) du [manuel de référence de Spring Intializr](https://docs.spring.io/initializr/docs/current-SNAPSHOT/reference/html/). Une fois le Bill of Materials **initializr-bom** ajouté au _<dependencyManagement>_, déclarerez les dépendances suivantes :

```
<dependencies>
    <dependency>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-web</artifactId>
    </dependency>
    <dependency>
        <groupId>io.spring.initializr</groupId>
        <artifactId>initializr-web</artifactId>
    </dependency>
    <dependency>
        <groupId>io.spring.initializr</groupId>
        <artifactId>initializr-generator-spring</artifactId>
    </dependency>
</dependencies>

```

Personnellement, j’ai utilisé la version **0.12.0** du **initializr-bom** datant du 24 janvier 2022 et compatible avec **Spring Boot 2.7** et **Java 17**. Comme conseillé dans la documentation, remplacez le fichier _application.properties_ par un fichier **_application.yaml_** plus enclin à accueillir une structure hiérarchique.

Il sera ensuite nécessaire de configurer la **propriété initializr** du fichier application.yaml avec :

- les versions de java supportées : 8, 11 et/ou 17
- les versions de Spring Boot proposées
- les langages supportés : Java, Kotlin et/ou Groovy
- le système de build supporté : Maven et/ou Gradle
- le nom de package par défaut
- Le type de packaging supporté : war ou jar
- le groupId par défaut
- la version par défaut de l’application
- les dépendances Maven

Voici un extrait configurant les 2 dépendances OpenAPI et Web aperçues dans la capture d’écran IntelliJ :

```
initializr:
  dependencies:
    - name: Java&Moi
      content:
        - id: openapi
          name: OpenAPI
          starter: false
          description: "Configure the web application to expose a REST API designed with a contact-first OpenAPI Specification (OAS): \n
          - The openapi-generator-maven-plugin\n
          - SwaggerUI with Springdoc"
    - name: Spring
      content:
        - name: Web
          id: web
          description: Build web, including RESTful, applications using Spring MVC. Uses Apache Tomcat as the default embedded container.

```

Pour une configuration complète, référez-vous au fichier _[application.yml](https://github.com/arey/javaetmoi-initializr/blob/main/src/main/resources/application.yml)_ du repo git.

Dans cet exemple, la version de Spring Boot à utiliser est codée en dur. Il est recommandé d’aller chercher dynamiquement la ou les versions proposées à l’utilisateur en déclarant un bean Spring implémentant l’interface **_[InitializrMetadataUpdateStrategy](https://github.com/spring-io/initializr/blob/v0.12.0/initializr-web/src/main/java/io/spring/initializr/web/support/InitializrMetadataUpdateStrategy.java)_** ou en utilisant la classe **_[SaganInitializrMetadataUpdateStrategy](https://github.com/spring-io/initializr/blob/v0.12.0/initializr-web/src/main/java/io/spring/initializr/web/support/SaganInitializrMetadataUpdateStrategy.java)_** clé en main.  
Non présent dans l’exemple, en attaquant l’API REST des différents composants de l’Usine de Dév (ex : Nexus, GitLab, ACR), on peut aller chercher la dernière version :

- du POM Parent d’entreprise
- du BOM Spring Boot d’entreprise
- des librairies maisons
- des images Docker privées et validées par les Ops

## Personnaliser la génération

L’ajout des dépendances **initializr-web** et **initializr-generator-spring** fait que votre initializr reproduit le fonctionnement de Spring Boot initializr et permet de facto de générer une classe main, sa classe de test, un fichier _application.properties_ ….

Pour adapter ce comportement à votre besoin, il est possible de déclarer des beans Spring en les regroupant dans des classes de configuration annotées par **[@ProjectGenerationConfiguration](https://github.com/spring-io/initializr/blob/v0.12.0/initializr-generator/src/main/java/io/spring/initializr/generator/project/ProjectGenerationConfiguration.java)**  
Ces classes doivent être enregistrées dans le fichier **[META-INF/spring.factories](https://github.com/arey/javaetmoi-initializr/blob/main/src/main/resources/META-INF/spring.factories)**. Voici un exemple enregistrant 2 classes de configuration : une première transverse et une seconde ne s’activant que lorsque la dépendance OpenAPI a été sélectionnée :

```
io.spring.initializr.generator.project.ProjectGenerationConfiguration=\
com.javaetmoi.initializr.generator.common.CommonSpringBootConfiguration,\
com.javaetmoi.initializr.generator.openapi.OpenAPIConfiguration
```

La classe **_[CommonSpringBootConfiguration](https://github.com/arey/javaetmoi-initializr/blob/main/src/main/java/com/javaetmoi/initializr/generator/common/CommonSpringBootConfiguration.java)_** a pour objectif de remplacer le fichier _application.properties_ par un fichier **_application.yml_** plus propice à accueillir la configuration générée par les autres générateurs. On y retrouve 2 beans Spring : un premier chargé de créer le fichier _application.yml_ à partir d’un template et le second chargé de supprimer le fichier _application.properties_ créé par la classe **_[ApplicationPropertiesContributor](https://github.com/spring-io/initializr/blob/v0.12.0/initializr-generator-spring/src/main/java/io/spring/initializr/generator/spring/configuration/ApplicationPropertiesContributor.java)_** du module _initializr-generator-spring_. Le plus simple aurait été de réussir à désactiver ce dernier.

```
@ProjectGenerationConfiguration
class CommonSpringBootConfiguration {

    @Bean
    ApplicationYamlContributor applicationYamlContributor() {
        return new ApplicationYamlContributor();
    }

    @Bean
    DeleteAplicationPropertiesContributor deleteAplicationPropertiesContributor() {
        return new DeleteAplicationPropertiesContributor();
    }

}

```

La classe **_[ApplicationYamlContributor](https://github.com/arey/javaetmoi-initializr/blob/main/src/main/java/com/javaetmoi/initializr/generator/common/ApplicationYamlContributor.java)_** hérite du contributeur _[SingleResourceProjectContributor](https://github.com/spring-io/initializr/blob/v0.12.0/initializr-generator-spring/src/main/java/io/spring/initializr/generator/spring/code/MainSourceCodeProjectContributor.java)_ facilitant la création d’un inique fichier. A noter la redéfinition de la méthode **_getOrder_** pour que ce bean soit appelé prioritairement, ceci afin que le fichier _application.yml_ existe pour les autres générateurs.

```
class ApplicationYamlContributor extends SingleResourceProjectContributor {

    @Override
    public int getOrder() {
        return Ordered.HIGHEST_PRECEDENCE;
    }

    ApplicationYamlContributor() {
        this("classpath:configuration/application.yml");
    }

    ApplicationYamlContributor(String resourcePattern) {
        super("src/main/resources/application.yml", resourcePattern);
    }
}

```

## Dépendance OpenAPI

Intéressons-nous à présent à la mise en place d’une API REST mettant en œuvre le plugin Maven **[openapi-generator-maven-plugin](https://github.com/OpenAPITools/openapi-generator/tree/master/modules/openapi-generator-maven-plugin)**. A partir d’une [spécification OpenAPI](https://github.com/OAI/OpenAPI-Specification) décrite dans un fichier _openapi.yaml_, ce plugin génère l’interface des contrôleurs REST et les classes du modèle représentant les ressources REST. A titre d’exemple, le fichier _openapi.yaml_ généré contient une API Hello World. Une implémentation basique de cette API est également générée.

La classe de configuration **_[OpenAPIConfiguration](https://github.com/arey/javaetmoi-initializr/blob/main/src/main/java/com/javaetmoi/initializr/generator/openapi/OpenAPIConfiguration.java)_** annotée avec _@ProjectGenerationConfiguration_ déclare pas moins de 7 beans. Notez l’usage de l’annotation **_[@ConditionalOnRequestedDependency](https://github.com/spring-io/initializr/blob/v0.12.0/initializr-generator/src/main/java/io/spring/initializr/generator/condition/ConditionalOnRequestedDependency.java)_** qui permet de n’activer cette classe de configuration Spring que si la dépendance OpenAPI a été sélectionnée. Quatre autres annotations du même genre existent : _[ConditionalOnPackaging](https://github.com/spring-io/initializr/blob/v0.12.0/initializr-generator/src/main/java/io/spring/initializr/generator/condition/ConditionalOnPackaging.java)_, _[ConditionalOnLanguage](https://github.com/spring-io/initializr/blob/v0.12.0/initializr-generator/src/main/java/io/spring/initializr/generator/condition/ConditionalOnLanguage.java)_, _[ConditionalOnBuildSystem](https://github.com/spring-io/initializr/blob/v0.12.0/initializr-generator/src/main/java/io/spring/initializr/generator/condition/ConditionalOnBuildSystem.java)_ et _[ConditionalOnPlatformVersion](https://github.com/spring-io/initializr/blob/v0.12.0/initializr-generator/src/main/java/io/spring/initializr/generator/condition/ConditionalOnPlatformVersion.java)_.

```
@ProjectGenerationConfiguration
@ConditionalOnRequestedDependency(DEPENDENCY_OPENAPI)
@AutoConfigureAfter({InitializrAutoConfiguration.class})
class OpenAPIConfiguration {

    @Bean
    OpenAPIPluginCustomizer openAPIPluginCustomizer(ProjectDescription projectDescription) {
        return new OpenAPIPluginCustomizer(projectDescription);
    }

    @Bean
    OpenApiDependenciesCustomizer openApiDependenciesCustomizer() {
        return new OpenApiDependenciesCustomizer();
    }

    @Bean
    SpecOpenApiContributor specOpenApiContributor() {
        return new SpecOpenApiContributor();
    }

    @Bean
    HelloControllerContributor helloControllerContributor(ProjectDescription projectDescription, MustacheTemplateRenderer mustacheTemplateRenderer) {
        return new HelloControllerContributor(mustacheTemplateRenderer, projectDescription);
    }

    @Bean
    SwaggerControllerContributor swaggerControllerContributor(ProjectDescription projectDescription, MustacheTemplateRenderer mustacheTemplateRenderer) {
        return new SwaggerControllerContributor(mustacheTemplateRenderer, projectDescription);
    }

    @Bean
    RemoveOpenAPIDependencyCustomizer removeOpenAPIDependencyCustomizer() {
        return new RemoveOpenAPIDependencyCustomizer();
    }

    @Bean
    TestOpenApiContributor testOpenApiContributor() {
        return new TestOpenApiContributor();
    }
}

```

**1.** Implémentant l’interface _BuildCustomizer_, la classe **_[OpenAPIPluginCustomizer](https://github.com/arey/javaetmoi-initializr/blob/main/src/main/java/com/javaetmoi/initializr/generator/openapi/OpenAPIPluginCustomizer.java)_** est chargée de configurer le plugin Maven _openapi-generator-maven-plugin_ :

```
class OpenAPIPluginCustomizer implements BuildCustomizer<MavenBuild> {

    private final ProjectDescription projectDescription;

    OpenAPIPluginCustomizer(ProjectDescription projectDescription) {
        this.projectDescription = projectDescription;
    }

    @Override
    public void customize(MavenBuild build) {
        build.plugins().add("org.openapitools", "openapi-generator-maven-plugin", c -> {
            c.version("5.4.0");
            c.execution("generate", e -> e.goal("generate"));
            c.configuration(configuration -> {
                configuration.add("inputSpec", "${project.basedir}/src/main/resources/openapi/openapi.yaml");
                configuration.add("generatorName", "spring");
                configuration.add("library", "spring-boot");
                configuration.add("modelNameSuffix", "Resource");
                configuration.add("apiPackage", projectDescription.getPackageName() + ".rest.controller");
                configuration.add("modelPackage", projectDescription.getPackageName() + ".rest.model");
                configuration.configure("configOptions", configOptions -> {
                    configOptions.add("interfaceOnly", "true");
                    configOptions.add("openApiNullable", "false");
                });
            });
        });
    }
}

```

A noter l’usage de lambda de type **_Consumer_** dans l’API de Spring Intializr.  
La configuration Maven générée est la suivante :

```
<plugin>
  <groupId>org.openapitools</groupId>
  <artifactId>openapi-generator-maven-plugin</artifactId>
  <version>5.4.0</version>
  <configuration>
    <inputSpec>${project.basedir}/src/main/resources/openapi/openapi.yaml</inputSpec>
    <generatorName>spring</generatorName>
    <library>spring-boot</library>
    <modelNameSuffix>Api</modelNameSuffix>
    <apiPackage>com.javaetmoi.myapp.demo.rest.controller</apiPackage>
    <modelPackage>com.javaetmoi.myapp.demo.rest.model</modelPackage>
    <configOptions>
      <interfaceOnly>true</interfaceOnly>
      <openApiNullable>false</openApiNullable>
    </configOptions>
  </configuration>
  <executions>
    <execution>
      <id>generate</id>
      <goals>
        <goal>generate</goal>
      </goals>
    </execution>
  </executions>
</plugin>

```

**2\.** La dépendance OpenAPI n’est pas une vraie dépendance au sens Maven. Non seulement elle déclare puis configure le plugin [openapi-generator-maven-plugin](https://github.com/OpenAPITools/openapi-generator/tree/master/modules/openapi-generator-maven-plugin), mais elle déclare également la dépendance Maven pour **[Springdoc](https://springdoc.org/)** (Swagger UI) et le starter **spring-boot-starter-validation** activant la validation des annotations Bean Validation positionnée par le plugin openapi. Pour se faire, la classe **_OpenApiDependenciesCustomizer_** implémente également l’interface _BuildCustomizer_ :

```
class OpenApiDependenciesCustomizer implements BuildCustomizer<MavenBuild> {

    @Override
    public void customize(MavenBuild build) {
        build.dependencies().add("springdoc", Dependency
            .withCoordinates("org.springdoc", "springdoc-openapi-ui")
            .version(VersionReference.ofValue("1.6.9"))
            .build());
        build.dependencies().add("spring-boot-starter-validation", "org.springframework.boot", "spring-boot-starter-validation", DependencyScope.COMPILE);
    }
}

```

La configuration Maven générée est ici évidente :

```
<dependency>
  <groupId>org.springframework.boot</groupId>
  <artifactId>spring-boot-starter-validation</artifactId>
</dependency>
<dependency>
  <groupId>org.springdoc</groupId>
  <artifactId>springdoc-openapi-ui</artifactId>
  <version>1.6.9</version>
</dependency>

```

**3\.** Sur le même principe que _ApplicationYamlContributor_, la classe **_[SpecOpenApiContributor](https://github.com/arey/javaetmoi-initializr/blob/main/src/main/java/com/javaetmoi/initializr/generator/openapi/SpecOpenApiContributor.java)_** ajoute le fichier _openapi.yaml_ au projet généré.

**4.** A partir du **template Mustache** _[HelloController.mustache](https://github.com/arey/javaetmoi-initializr/blob/main/src/main/resources/templates/openapi/HelloController.mustache),_ la classe **_[HelloControllerContributor](https://github.com/arey/javaetmoi-initializr/blob/main/src/main/java/com/javaetmoi/initializr/generator/openapi/HelloControllerContributor.java)_** génère un _@RestController_ implémentant l’interface _HelloApi_ généré par le plugin maven.

Voici le template HelloController.mustache :

```
package {{package}}.controller;

import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import {{package}}.model.MessageResource;

@RestController
@RequestMapping("/api/v1")
public class HelloController implements HelloApi {

    @Override
    public ResponseEntity<MessageResource> hello(String name) {
        return ResponseEntity.ok(new MessageResource().message(name));
    }
}

```

**5.** La classe **_[SwaggerControllerContributor](https://github.com/arey/javaetmoi-initializr/blob/main/src/main/java/com/javaetmoi/initializr/generator/openapi/SwaggerControllerContributor.java)_** génère un contrôleur Spring MVC redirigeant l’utilisateur sur l’IHM de Swagger UI lorsqu’il navigue sur [http://localhost:8080](http://localhost:8080)

```
@Controller
public class SwaggerController {

    @RequestMapping(value = "/")
    public String index() {
        return "redirect:swagger-ui/index.html";
    }
}

```

**6.** La classe **_[TestOpenApiContributor](https://github.com/arey/javaetmoi-initializr/blob/main/src/main/java/com/javaetmoi/initializr/generator/openapi/TestOpenApiContributor.java)_** ajoute un fichier _hello.http_ facilitant le test de l’API depuis IntelliJ :

{{< figure src="/wp-content/uploads/2022/07/image-2.png" alt="" caption="" >}}

```
<dependency>
  <groupId>org.springframework.boot</groupId>
  <artifactId>spring-boot-starter-openapi</artifactId>
</dependency>

```

**Tester javaetmoi-initializr** revient à [suivre les instructions données dans son **README.md**](https://github.com/arey/javaetmoi-initializr#use-the-service-from-intellij).

## Tests unitaires

Tester unitairement les différents générateurs de code est facilité par l’artefact **initializr-generator-test** que vous pouvez ajouter en scope test à votre projet :

```
<dependency>
  <groupId>io.spring.initializr</groupId>
  <artifactId>initializr-generator-test</artifactId>
  <scope>test</scope>
</dependency>

```

Cet artefact propose un ensemble de classes permettant de générer des projets. Je pense par exemple à la classe _[ProjectGeneratorTester](https://github.com/spring-io/initializr/blob/main/initializr-generator-test/src/main/java/io/spring/initializr/generator/test/project/ProjectGeneratorTester.java)_. Le résultat de la génération est  alors disponible dans la classe _[ProjectStructure](https://github.com/spring-io/initializr/blob/v0.12.0/initializr-generator-test/src/main/java/io/spring/initializr/generator/test/project/ProjectStructure.java)_ qui permet de récupérer le chemin vers le code généré mais propose également tout un jeu d’assertions AssertJ facilitant les tests sur le pom Maven, l’arborescence des fichiers et le contenu des fichiers/classes générées.

Extrait de la classe de teste **_[OpenApiTest](https://github.com/arey/javaetmoi-initializr/blob/main/src/test/java/com/javaetmoi/initializr/generator/openapi/OpenApiTest.java)_**, la méthode suivante vérifie que les dépendances Maven springdoc-openapi-ui et spring-boot-starter-validation ont été ajoutées au pom.xml :

```
@Test
void should_openapi_dependency_generate_pom_with_springdoc_and_spring_boot_starter_validation() {
    // Given
    var metadata = InitializrMetadataTestBuilder.withDefaults().build();

    // When
    var project = generateProject(DESCRIPTION, metadata);

    // Then
    assertThat(project).mavenBuild()
        .hasDependency("org.springdoc", "springdoc-openapi-ui")
        .hasDependency("org.springframework.boot", "spring-boot-starter-validation");
}

```

La méthode suivante vérifie quant à elle le contenu de la classe HelloController.java générée :

```
@Test
void should_openapi_dependency_generate_HelloController() {
    // Given
    var metadata = InitializrMetadataTestBuilder.withDefaults().build();

    // When
    var project = generateProject(DESCRIPTION, metadata);

    // Then
    // @formatter:off
    assertThat(project).textFile("src/main/java/com/javaetmoi/demo/rest/controller/HelloController.java").containsExactly(
        "package com.javaetmoi.demo.rest.controller;",
        "",
        "import org.springframework.http.ResponseEntity;",
        "import org.springframework.web.bind.annotation.RequestMapping;",
        "import org.springframework.web.bind.annotation.RestController;",
        "",
        "import com.javaetmoi.demo.rest.model.MessageResource;",
        "",
        "@RestController",
        "@RequestMapping(\"/api/v1\")",
        "public class HelloController implements HelloApi {",
        "",
        "    @Override",
        "    public ResponseEntity<MessageResource> hello(String name) {",
        "        return ResponseEntity.ok(new MessageResource().message(name));",
        "    }",
        "}"
    );
    // @formatter:on

```

## Conclusion

Au travers de ce billet, nous aurons vu comment personnaliser Spring Initializr à partir d’un exemple concret. Si vous êtes familiers à l’écosystème Spring, la prise en main de l’API Java de cet outil devrait se faire relativement rapidement.

Au cours de mes développements, je me suis aperçu certaines limitations de l’API. J’avais par exemple besoin de générer dynamiquement de la configuration Java de Spring Security. L’ajout de l’annotation _@Override_ ou d’un _throws Exception_ n’était pas proposée par la classe _[JavaMethodDeclaration](https://github.com/spring-io/initializr/blob/v0.12.0/initializr-generator/src/main/java/io/spring/initializr/generator/language/java/JavaMethodDeclaration.java)_ :

```
@Override
protected void configure(HttpSecurity http) throws Exception {

```

Comme suggéré dans l’ [issue #1043](https://github.com/spring-io/initializr/issues/1043), n’ayant besoin que du support de Java, je me suis tourné vers l’usage de [JavaPoet](https://github.com/square/javapoet) que j’avais déjà utilisé sur le projet [javabean-marshaller](https://github.com/arey/javabean-marshaller). Son intégration dans une implémentation de _ProjectContributor_ n’a pas posé de difficulté, preuve que Spring Initializr est extensible. Pour un support de Kotlin, j’aurais pu utiliser [KotlinPoet](https://github.com/square/kotlinpoet).

N’ayant pas regardé en détails ce que proposait JHipster, je ne saurais pas départager les 2 solutions. Mais je  serais curieux de vos retours d’expérience.

## Ressources

- [Manuel de reference Spring Initializr](https://docs.spring.io/initializr/docs/current-SNAPSHOT/reference/html/)
- [How to customize the Spring Initializr](https://medium.com/digitalfrontiers/how-to-customize-the-spring-initializr-2439ecabb069)
- [Start the Spring Initializr personalization journey](https://www.mo4tech.com/start-the-spring-initializr-personalization-journey.html)
- [Repository GitHub javaetmoi-initializr](https://github.com/arey/javaetmoi-initializr/)
