---
_edit_last: "1"
author: admin
categories:
  - conférence
  - spring
date: "2024-04-21T16:38:47+00:00"
thumbnail: /wp-content/uploads/2024/04/word-image-2317-2.jpeg
featureImage: /wp-content/uploads/2024/04/word-image-2317-2.jpeg
guid: https://javaetmoi.com/?p=2317
parent_post_id: null
post_id: "2317"
post_views_count: "19384"
summary: |-
  ## Le live coding qui rendra vos applications plus pérennes

  Conférence : [Devoxx France 2024](https://www.devoxx.fr/){{ double-space-with-newline }}Date : 19 avril 2024 {{ double-space-with-newline }}Speakers : [Julien Topçu](https://twitter.com/JulienTopcu) ( [Shodo](https://shodo.io/)) {{ double-space-with-newline }}Format : Conférence (45mn) {{ double-space-with-newline }}Repo GitLab : [https://gitlab.com/beyondxscratch/hexagonal-architecture-java-springboot](https://gitlab.com/beyondxscratch/hexagonal-architecture-java-springboot){{ double-space-with-newline }}Vidéo Youtube : [https://www.youtube.com/watch?v=-dXN8wkN0yk](https://www.youtube.com/watch?v=-dXN8wkN0yk)

  Cette session de live coding se déroule dans l’univers de Starwars et commence par une **citation de Maitre Yoda** :

  ![](https://javaetmoi.com/wp-content/uploads/2024/04/word-image-2317-1.png){{ double-space-with-newline }}
  En 45mn, Julien doit développer le système **Rebels Rescue** visant à reconstituer des flottes de sauvetage. N’en déplaise à l’Empire, les technos seront Spring Boot et Java 21.

  A cet effet, il s’appuiera sur l’API publique [SWAPI](https://swapi.dev/) permettant d’accéder à un référentiel de vaisseaux à disposition. L’application sélectionne les vaisseaux qui permettent d’effectuer la mission de sauvetage. Le code source est disponible dans le repo GitLab de Julien : [hexagonal-architecture-java-springboot](https://gitlab.com/beyondxscratch/hexagonal-architecture-java-springboot)

  Julien commence par rappeler les inconvénients d’une **architecture 3-tiers** basée sur le triptyque **Contrôleur -> Service -> Persistance**
tags:
  - architecture
  - ddd
  - devoxx
  - hexagonal
  - spring-boot
title: L’Architecture Hexagonale par la pratique
url: /2024/04/larchitecture-hexagonale-par-la-pratique/

---
## Le live coding qui rendra vos applications plus pérennes

Conférence : [Devoxx France 2024](https://www.devoxx.fr/)  
Date : 19 avril 2024   
Speakers : [Julien Topçu](https://twitter.com/JulienTopcu) ([Shodo](https://shodo.io/))   
Format : Conférence (45mn)   
Repo GitLab : [https://gitlab.com/beyondxscratch/hexagonal-architecture-java-springboot](https://gitlab.com/beyondxscratch/hexagonal-architecture-java-springboot)  
Vidéo Youtube : [https://www.youtube.com/watch?v=-dXN8wkN0yk](https://www.youtube.com/watch?v=-dXN8wkN0yk)

Cette session de live coding se déroule dans l’univers de Starwars et commence par une **citation de Maitre Yoda** :

![](/wp-content/uploads/2024/04/word-image-2317-1.png)  

En 45mn, Julien doit développer le système **Rebels Rescue** visant à reconstituer des flottes de sauvetage. N’en déplaise à l’Empire, les technos seront Spring Boot et Java 21.

A cet effet, il s’appuiera sur l’API publique [SWAPI](https://swapi.dev/) permettant d’accéder à un référentiel de vaisseaux à disposition. L’application sélectionne les vaisseaux qui permettent d’effectuer la mission de sauvetage. Le code source est disponible dans le repo GitLab de Julien : [hexagonal-architecture-java-springboot](https://gitlab.com/beyondxscratch/hexagonal-architecture-java-springboot)

Julien commence par rappeler les inconvénients d’une **architecture 3-tiers** basée sur le triptyque **Contrôleur -> Service -> Persistance**

{{< figure src="/wp-content/uploads/2024/04/word-image-2317-2.jpeg" alt="" caption="" >}}

Très utile, cette architecture n-tiers vieillit mal.   
 En théorie, la **logique métier** doit être centralisée dans la couche service. Mais en pratique, on la voit **diluée** partout, jusque dans les procédures stockées …   
Autre problème de taille : **les responsabilités techniques leaks** de tous les côtés.   
Julien prend un exemple de code GitHub avec une classe _Exercice_ mélangeant annotations JPA (ex: _@Column_) liée à la persistance de données et des annotations Jackson (ex : _@JsonProperty_) liées à la couche de présentation. Le couplage est évident. Le code métier casse si on migre d’une base relationnelle à MongoDB ou bien d’une API REST à GraphQL.   
Un upgrade de la version de Spring Boot ne devrait pas casser le code fonctionnel. C’est trop malheureusement le cas avec ce type d’architecture.

Les applications legacy sont souvent construites sur des stacks très vieilles. Opérationnelles, elles font tourner le business. Leur couplage à de vieux frameworks comme Servlets et EJB les rend particulièrement difficile à migrer vers Spring Boot ou Quarkus.   
**Le couplage amène de la fragilité**.

A contrario, l’ **architecture hexagonale sacralise ce qui apporte de la valeur métier.** Elle permet de faire des tests sur le métier. Le code métier est placé dans le **Domain**. A première vue, le Domain ressemble un peu au Service d’avant. A ceci près que **le Domain doit être agnostique**. On inverse la dépendance pour que la **Persistence** dépende du Domain et non l’inverse.

**Le Domain ne doit pas dépendre de frameworks.** Pour ne pas réinventer la roue, on peut toutefois y mettre quelques librairies.

A titre d’exemple, le Domain de Rebels Rescue ne contient que 2 dépendances de test : **junit-jupiter** et **assertj-core**. Pour éviter qu’un développeur ne vienne enfreindre cette règle, Julien s’appuie sur le plugin [**maven-enforcer-plugin**](https://maven.apache.org/enforcer/maven-enforcer-plugin/):

```xml
<plugin>
    <artifactId>maven-enforcer-plugin</artifactId>
    <version>3.0.0</version>
    <executions>
        <execution>
            <goals>
                <goal>enforce</goal>
            </goals>
            <configuration>
                <rules>
                    <bannedDependencies>
                        <excludes>
                            <!-- forbids non domain dependencies -->
                            <exclude>*</exclude>
                        </excludes>
                        <includes>
                            <include>*:*:*:*:test</include>
                        </includes>
                    </bannedDependencies>
                </rules>
            </configuration>
        </execution>
    </executions>
</plugin>
```

Le maven-enforcer-plugin bannit toutes les librairies qui ne sont pas en scope test. L’usage d’ **ArchUnit** pourrait s’envisager avec j’imagine des règles sur les imports de packages (JDK et domain).

Dans une architecture hexagonale, l’extérieur du Domain est appelé l’ **infrastructure.**

![](/wp-content/uploads/2024/04/word-image-2317-3.jpeg)

Les interfaces d’entrée et de sorties du domaine sont rangées au niveau des frontières nommées **API** et **SPI** :   
\- **Application Programming Interface** Java à ne pas confondre avec API REST.   
\- **Service Providing Interface** : le SPI ne dépend que des objets du domaine. De cette manière, les annotations ORM ne polluent pas le Domaine.   
La structuration de la base de données n’a pas d’impact sur la modélisation du domain métier.   
Dans la littérature, l’archi hexagonale est également appelée **Ports and Adapters**.

Lorsqu’on développe sur une application architecturée en hexagone, on commence par implémenter le Domain.   
Dans notre exemple, on retrouve les 2 classes : [**StarShip**](https://gitlab.com/beyondxscratch/hexagonal-architecture-java-springboot/-/blob/main/domain/src/main/java/rebelsrescue/fleet/StarShip.java) et [**Fleet**](https://gitlab.com/beyondxscratch/hexagonal-architecture-java-springboot/-/blob/main/domain/src/main/java/rebelsrescue/fleet/Fleet.java).

```java
public record Fleet (UUID id, List<StarShip> starships){
    public Fleet(List<StarShip> starships) {
        this(UUID.randomUUID(),starships);
    }
}public record StarShip(String name, int passengersCapacity, BigDecimal cargoCapacity) {
}
```

Ce n’était pas une pratique courante il y’a 10 ans, mais en 2024, **Julien recommande de créer un test fonctionnel** permettant de vérifier le contrat d’entrée dans le domaine.   
A cet effet, la méthode _should\_assemble\_a\_fleet\_for\_1050\_passengers_ de la classe [AssembleAFleetFunctionalTest](https://gitlab.com/beyondxscratch/hexagonal-architecture-java-springboot/-/blob/main/domain/src/test/java/rebelsrescue/fleet/AssembleAFleetFunctionalTest.java) assemble une flotte de 1050 passagers.

```java
// When
Fleet fleet = assembleAFleet.forPassengers(numberOfPassengers);
```

L’implémentation du test nécessite de créer l’interface [AssembleAFleet](https://gitlab.com/beyondxscratch/hexagonal-architecture-java-springboot/-/blob/main/domain/src/main/java/rebelsrescue/fleet/api/AssembleAFleet.java) :

```java
public interface AssembleAFleet {
    Fleet forPassengers(int numberOfPassengers);
}
```

Point d’entrée dans le Domain, cette interface doit être rangée dans le **package _api_**.   
Si le nommage vous gêne, le package _api_ peut être nommé **_features_**.   
La classe [FleetAssembler](https://gitlab.com/beyondxscratch/hexagonal-architecture-java-springboot/-/blob/main/domain/src/main/java/rebelsrescue/fleet/FleetAssembler.java) implémente l’interfacer AssembleAFleet. A noter : l’interface prend le nom d’une commande (verbe au présent), l’implémentation un nom commun.

```java
class FleetAssembler implements AssembleAFleet {@Override
    public Fleet forPassengers(int numberOfPassengers) {
        List<StarShip> starShips = getStarShipsHavingPassengersCapacity();
        List<StarShip> rescueStarShips = selectStarShips(numberOfPassengers, starShips);
        return fleets.save(new Fleet(rescueStarShips));
    }
```

L’implémentation de la méthode _getStarShipsHavingPassengersCapacity()_ demande d’introduire l’interface [StartSheepInventory](https://gitlab.com/beyondxscratch/hexagonal-architecture-java-springboot/-/blob/main/domain/src/main/java/rebelsrescue/fleet/spi/StarShipInventory.java) contenant l’unique méthode _starShips()_. Cette interface est ajoutée au package **spi** pour aller chercher l’inventaire par appel d’une API externe.

```java
private List<StarShip> getStarShipsHavingPassengersCapacity() {
    return starshipsInventory.starShips().stream()
            .filter(starShip -> starShip.passengersCapacity() > 0)
            .sorted(comparingInt(StarShip::passengersCapacity))
            .collect(Collectors.toCollection(ArrayList::new));
}public interface StarShipInventory {
    List<StarShip> starShips();
}
```

Dans la classe _FleetAssembler_, l’inventory _StarShipInventory_ est injecté par constructeur :

```java
private final StarShipInventory starshipsInventory;public FleetAssembler(StarShipInventory starShipsInventory) {
    this.starshipsInventory = starShipsInventory;
}
```

L’écriture du TU nécessite une instance de _FleetAssembler_. Pour simuler l’extérieur, on un **stub**. Technique intéressante : Julien se passe ici de Mockito et **crée le stub à l’aide d’une fonction lambda** :

```java
//Given
var starShips = asList(
        new StarShip("no-passenger-ship", 0, ZERO),
        new StarShip("xs", 10, new BigDecimal("1000")),
        new StarShip("s", 50, new BigDecimal("50000")),
        new StarShip("m", 200, new BigDecimal("70000")),
        new StarShip("l", 800, new BigDecimal("150000")),
        new StarShip("xl", 2000, new BigDecimal("500000")));StarShipInventory starShipsInventory = () -> starShips;
```

Le Domain de Rebels Rescue est prêt.

Julien poursuit par l’implémentation d’un contrôleur REST exposant cette logique sur le réseau. Un module Maven dédié à l’ **infrastructure** est créé. Ce module infrastructure dépend du module domain.

On retrouve un contrôleur Rest Spring MVC [RescueFleetController](https://gitlab.com/beyondxscratch/hexagonal-architecture-java-springboot/-/blob/main/infrastructure/src/main/java/rebelsrescue/controllers/RescueFleetController.java) exposant un endpoint POST /rescueFleets :

```java
@PostMapping
public ResponseEntity<FleetResource> assembleAFleet(@RequestBody RescueFleetRequest rescueFleetRequest){
    var fleet = assembleAFleet.forPassengers(rescueFleetRequest.numberOfPassengers);
    return created(fromMethodCall(on(this.getClass()).getFleetById(fleet.id())).build().toUri())
            .body(new FleetResource(fleet));
}
```

L’IDE ne trouve pas d’instance de bean _AssembleAFleet_. Ce qui est normal car le Domain n’a pas de dépendance vers Spring et la classe _FleetAssembler_ ne peut donc pas être annotée par l’annotation **@Component** de Spring.   
Pour résoudre cette problématique, certains développeurs utilisent des fabriques de bean. Julien n’est pas fan et préfère l’usage du **component scan**. **Il fait en sorte que ce soit Spring qui connaisse notre domaine et non l’inverse**. Pour cela, il introduit les 2 annotations customs   
[@DomainService](https://gitlab.com/beyondxscratch/hexagonal-architecture-java-springboot/-/blob/main/domain/src/main/java/ddd/DomainService.java) et [@Stub](https://gitlab.com/beyondxscratch/hexagonal-architecture-java-springboot/-/blob/main/domain/src/main/java/ddd/Stub.java) qu’il place dans un package **ddd**.

```java
/**
 * <p>
 * A Domain Service, i.e. a feature that belongs to the domain and the
 * ubiquitous language.
 * </p>
 *
 * @see <a href=
 * "https://www.domainlanguage.com/wp-content/uploads/2016/05/DDD_Reference_2015-03.pdf">Domain-Driven Design Reference</a>
 */
@Retention(RetentionPolicy.RUNTIME)
public @interface DomainService {}
```

Cette annotation permet de documenter les classes en faisant référence au document [Domain-Driven Design Reference](https://www.domainlanguage.com/wp-content/uploads/2016/05/DDD_Reference_2015-03.pdf) d’Eric Evans, le père du DDD.

Dans la couche d’infrastructure, la classe [DomainConfiguration](https://gitlab.com/beyondxscratch/hexagonal-architecture-java-springboot/-/blob/main/infrastructure/src/main/java/rebelsrescue/configuration/DomainConfiguration.java) configure Spring pour scanner les beans annotés par **_@DomainService_** et **_@Stub_**

```java
@Configuration
@ComponentScan(
        basePackageClasses = {Fleet.class},
        includeFilters = {@ComponentScan.Filter(type = FilterType.ANNOTATION, classes = {DomainService.class, Stub.class})},
        excludeFilters = {@ComponentScan.Filter(type = FilterType.ASSIGNABLE_TYPE, classes = {StarShipInventoryStub.class})})
public class DomainConfiguration {}
```

Cette approche est intéressante. Une autre approche consiste à intégrer le jeu d’annotations Dependency Injection de la JSR-330 via l’artefact **jakarta.inject-api**

Dans un premier temps, pour faire fonctionner l’application, on peut stubber l’implémentation de _StarShipInventory_ en réutilisant le stub du test [StarShipInventoryStub](https://gitlab.com/beyondxscratch/hexagonal-architecture-java-springboot/-/blob/main/domain/src/main/java/rebelsrescue/fleet/spi/stubs/StarShipInventoryStub.java) qui est donc placé dans le code de prod et annoté avec l’annotation _@Stub_.   
L’ajout de ce stub permet de déployer l’application en prod ou en préprod. Julien a exploité cette technique chez Expedia pour gagner du temps avec l’équipe mobile.

Pour terminer l’application, il reste à développer le client Swapi à l’aide de l’ **API StarWars** [https://swapi.dev/](https://swapi.dev/), référentiel sur l’univers de Starwars utilisable par tous.

La classe [SwapiClient](https://gitlab.com/beyondxscratch/hexagonal-architecture-java-springboot/-/blob/main/infrastructure/src/main/java/rebelsrescue/swapi/SwapiClient.java) implémente l’interface _StarShipInventory_. A noter que dans l’infrastructure, on peut utiliser l’annotation Spring _@Component_. L’API REST de Swapi est paginée. Le domaine ne sera pas pollué par le choix technique de Swapi.   
 De la même manière, les données inutilisées renvoyées Swapi n’auront pas leur place dans le Domain. L’usage de Swapi n’aura pas d’impact sur le Domain : type String de passengers alors que Julien veut un integer dans le Domain, champs nommés différemment …

La classe SwapiClient modélise le modèle de Swapi à l’aide des 2 records [SwapiReponse](https://gitlab.com/beyondxscratch/hexagonal-architecture-java-springboot/-/blob/main/infrastructure/src/main/java/rebelsrescue/swapi/model/SwapiResponse.java) et [SwapiStarship](https://gitlab.com/beyondxscratch/hexagonal-architecture-java-springboot/-/blob/main/infrastructure/src/main/java/rebelsrescue/swapi/model/SwapiStarShip.java). Elle utilise le _RestTemplate_ de Spring et convertit le modèle Swapi vers domaine (notion d’ **adaptateurs**). Elle traite également les cas particuliers comme les chaines _« n/a »_ et « _unknnown »_ renvoyées par l’API Swapi dans le nombre de passengers mais aussi le séparateur de millier. Ces traitements sont gérés dans l’adaptateur.


L’adaptateur agit comme une **anticorruption layer** et retire les _n/a_ et _unknown_. Il nettoie les données pour avoir un Domain propre.

Pour simuler de vraies réponses de SWAPI dans les TU, la classe de test [StarwarsRebelsRescueApplicationTests](https://gitlab.com/beyondxscratch/hexagonal-architecture-java-springboot/-/blob/main/infrastructure/src/test/java/rebelsrescue/StarwarsRebelsRescueApplicationTests) utilise un serveur de mock basé sur [wiremock](https://wiremock.org/)

Julien termine sa présentation en introduisant volontairement une régression. Suite à l’ajout du champs _cargoCapacity_, on renomme _capacity_ en _passengersCapacity_. On casse les consommateurs de notre API REST. A ce stade de la démo, le contrôleurs REST est couplé avec le domaine métier. Les ressources REST sont les objets du domaine. Il y’a nécessité de créer une représentation de ce qu’est une ressource REST. Julien introduit le record [FleetResource](https://gitlab.com/beyondxscratch/hexagonal-architecture-java-springboot/-/blob/main/infrastructure/src/main/java/rebelsrescue/controllers/FleetResource.java) et ajoute un champ _deprecation_ permettant de prévenir les consommateurs du renommage.

Architecture finale de l’application Rebels Rescue :

{{< figure src="/wp-content/uploads/2024/04/word-image-2317-4.jpeg" alt="" caption="" >}}
