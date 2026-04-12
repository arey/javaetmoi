---
_edit_last: "1"
_thumbnail_id: "1757"
_xmlsf_image_featured:
  caption: ""
  loc: https://javaetmoi.com/wp-content/uploads/2017/09/Kotlin_logo.png
  title: Logo Kotlin
author: admin
categories:
  - retour-d'expérience
  - spring
featureImage: /wp-content/uploads/2017/09/Kotlin_logo.png
featureImageAlt: Logo Kotlin
date: "2017-09-25T16:50:26+00:00"
thumbnail: /wp-content/uploads/2017/09/Kotlin_logo.png
guid: http://javaetmoi.com/?p=1753
parent_post_id: null
post_id: "1753"
post_views_count: "7609"
summary: |-
  ![](http://javaetmoi.com/wp-content/uploads/2017/09/Kotlin_logo-150x150.png)

  Lors la dernière conférence Google I/O qui s’est tenue en mai 2017, Google a officialisé le **support de Kotlin sur Android**. Google n’est pas le seul acteur de l’IT à miser sur ce nouveau langage créé par JetBrains (l’éditeur de l’IDE IntelliJ) et s’exécutant sur la JVM (mais pas que). En effet, dès février 2016, [Pivotal proposait de développer des applications **Spring Boot** avec Kotlin](https://spring.io/blog/2016/02/15/developing-spring-boot-applications-with-kotlin). En janvier 2017, ils annonçaient que [la version 5 du **framework Spring** proposerait des **fonctionnalités exclusives à Kotlin**](https://spring.io/blog/2017/01/04/introducing-kotlin-support-in-spring-framework-5-0). Chez Gradle, le langage Kotlin est désormais privilégié au détriment de Groovy.

  Pour découvrir ce nouveau venu dans la galaxie des langages de programmation, je me suis intéressé à migrer vers Kotlin l’application démo Spring Petclinic développée en Java et Spring Boot. Je souhaitais ici partager son code source : [**spring-petclinic-kotlin**](https://github.com/spring-petclinic/spring-petclinic-kotlin) et énumérer les différences notables avec sa version Java.

  ![Logo Kotlin](/wp-content/uploads/2017/09/Kotlin_logo.png)
tags:
  - kotlin
  - spring-boot
title: Découvrir Kotlin en migrant une webapp Spring Boot
url: /2017/09/migrez-application-java-spring-boot-vers-kotlin/

---
![](/wp-content/uploads/2017/09/Kotlin_logo.png)

Lors la dernière conférence Google I/O qui s’est tenue en mai 2017, Google a officialisé le **support de Kotlin sur Android**. Google n’est pas le seul acteur de l’IT à miser sur ce nouveau langage créé par JetBrains (l’éditeur de l’IDE IntelliJ) et s’exécutant sur la JVM (mais pas que). En effet, dès février 2016, [Pivotal proposait de développer des applications **Spring Boot** avec Kotlin](https://spring.io/blog/2016/02/15/developing-spring-boot-applications-with-kotlin). En janvier 2017, ils annonçaient que [la version 5 du **framework Spring** proposerait des **fonctionnalités exclusives à Kotlin**](https://spring.io/blog/2017/01/04/introducing-kotlin-support-in-spring-framework-5-0). Chez Gradle, le langage Kotlin est désormais privilégié au détriment de Groovy.

Pour découvrir ce nouveau venu dans la galaxie des langages de programmation, je me suis intéressé à migrer vers Kotlin l’application démo Spring Petclinic développée en Java et Spring Boot. Je souhaitais ici partager son code source : [**spring-petclinic-kotlin**](https://github.com/spring-petclinic/spring-petclinic-kotlin) et énumérer les différences notables avec sa version Java.

## Une migration en souplesse

En m’appuyant sur le [manuel de référence de Kotlin](https://kotlinlang.org/docs/reference/), j’ai pu migrer l’application sans trop de difficulté et en quelques heures. IntelliJ m’a grandement facilité la tâche puisqu’un copier/coller d’une classe Java dans un fichier Kotlin (extension .kt) lançait le plugin de conversion automatique. Quelques adaptations manuelles restaient néanmoins nécessaires.

Grâce à l’interopérabilité de Kotlin avec Java, j’ai pu faire cohabiter classes Kotlin et classes Java dans le même projet IntelliJ. Au cours de la migration, cela m’a permis de vérifier régulièrement le bon fonctionnement l’application.

## Des conventions qui changent

Kotlin changent certaines conventions du langage Java :

**1.** Les **classes** et les **méthodes** sont par défaut **finales** et ne peuvent être **héritées / redéfinies** sans l’utilisation du mot clé **_open_** Dans Petclinic, la classe [BaseEntity](https://github.com/spring-petclinic/spring-petclinic-kotlin/blob/master/src/main/kotlin/org/springframework/samples/petclinic/model/BaseEntity.kt) parente de toutes les entités JPA est déclarée ainsi :

```java
@MappedSuperclass
open class BaseEntity

```

L’omission du paramètre _open_ déclenche une erreur de compilation des classes filles : _« This type is final, so it cannot be inherited from »_.

Ce changement de comportement impacte le fonctionnement de certaines librairies tierces. En effet, lors de l’utilisation d’annotations tels que @Cacheable ou @Configuration, le framework Spring utilise l’héritage pour instrumenter le code. La configuration du [plugin Spring pour le compilateur Kotlin](https://kotlinlang.org/docs/reference/compiler-plugins.html#kotlin-spring-compiler-plugin) dans le [pom.xml](https://github.com/spring-petclinic/spring-petclinic-kotlin/blob/master/pom.xml) permet de s’affranchir de l’ajout du mot clé open sur les beans Spring de type @Component.

**2.** La **visibilité** des méthodes et des classes est par défaut **publique**
Appartenant au package _visit_, la classe [Visit](https://github.com/spring-petclinic/spring-petclinic-kotlin/blob/master/src/main/kotlin/org/springframework/samples/petclinic/visit/Visit.kt) est référencée par la classe [Pet](https://github.com/spring-petclinic/spring-petclinic-kotlin/blob/master/src/main/kotlin/org/springframework/samples/petclinic/owner/Pet.kt) du package de même niveau _owner_:

```kotlin
class Visit : BaseEntity()
```

 **3.** Les **types primitifs** de Java disparaissent. Plus besoin de choisir entre un int et un Integer : vous utiliserez un Int.

**4.** Le **type des variables** et de **retour de méthode** n’est plus **déclaré** à gauche mais **à droite**.
Extrait de l’interface OwnerRepository :

fun findById(@Param("id") id: Int): Owner

Il faut s’y faire et retrouver ses habitudes du bon vieux Turbo Pascal.

**5.** Par défaut, aucune variable ne peut être **null**. Le compilateur vous rappellera à l’ordre. Lorsqu’une variable peut prendre la valeur null, il est nécessaire de le préciser explicitement en faisant suivre son type par le caractère **?**

```kotlin
var name: String? = null
```

 **6.** Les **getter/setter** (mutateurs) des propriétés d’une classe sont générés automatiquement par Kotlin. Dans le code, on accède directement à une propriété sans passer par les mutateurs. Kotlin ajoute automatiquement l’appel au mutateur correspondant.
Là ou en Java on passait par un setter :

```java
james.setLastName("Carter");
```

en Kotlin, on affecte directement la valeur à la propriété :

```kotlin
james.lastName = "Carter"
```

Bien entendu, Kotlin offre la possibilité de ne générer qu’un des 2 mutateurs et/ou de redéfinir leur implémentation. Par exemple, dans la [BaseEntity](https://github.com/spring-petclinic/spring-petclinic-kotlin/blob/master/src/main/kotlin/org/springframework/samples/petclinic/model/BaseEntity.kt).kt, la propriété isNew est évaluée à partie de l’ID de l’entité :

```kotlin
val isNew: Boolean
    get() = this.id == null
```

## Une syntaxe allégée

Par rapport à Java, Kotlin se veut apporter de la **concision** sans perdre en lisibilité, et ceci par le biais de léger changements syntaxiques.

**1.** Le signe **point-virgule ;** en fin d’instruction devient facultatif. Et lorsqu’une méthode ne comporte qu’une seule instruction, l’utilisation d’ **accolades** et du mot clé **return** ne sont plus nécessaires.
Extrait du PetController Java :

```java
@ModelAttribute("types")
public Collection<PetType> populatePetTypes() {
    return this.pets.findPetTypes();
}
```

Extrait du [PetController](https://github.com/spring-petclinic/spring-petclinic-kotlin/blob/master/src/main/kotlin/org/springframework/samples/petclinic/owner/PetController.kt) Kotlin :

```kotlin
@ModelAttribute("types")
fun populatePetTypes(): Collection<PetType> = this.pets.findPetTypes()
```

 **2.** Concernant l’héritage et l’implémentation d’une interface, les mots clés **extends** et **implements** sont remplacés par le symbole **:**

Code Java :

```default
public interface VetRepository extends Repository<Vet, Integer> {
```

Code Kotlin :

```kotlin
interface VetRepository : Repository<Vet, Int> {
```

 **3.** Le compilateur Kotlin sait **inférer** le **type des variables**. Lorsque vous déclarez une variable en lui affectant une valeur (autre que null), il n’est plus nécessaire de spécifier son type.
Exemple issu de Owner.kt :

```kotlin
@Column(name = "city")
@NotEmpty
var city = ""
```

4\. L’instruction **for each** permettant d’itérer sur les éléments d’une collection change de syntaxe. Kotlin passe du : au **in**. A noter que le type de variable n’est plus exigé.

Version Java :

```java
for (Pet pet : getPetsInternal()) {
```

Version Kotlin :

```kotlin
for (pet in pets) {
```

## Des améliorations intéressantes

La plus-value de Kotlin par rapport à Java dépasse les conventions et les changements syntaxiques évoqués dans les 2 paragraphes précédents.

**1.** Kotlin propose de **créer automatiquement** des **POJO** avec getters, setters, méthodes equals(), hashCode(), toString() et copy() (cette dernière étant propre à Kotlin) via un mécanisme appelé [**data class**](https://kotlinlang.org/docs/reference/data-classes.html).
La classe [Vets](https://github.com/spring-petclinic/spring-petclinic-kotlin/blob/master/src/main/kotlin/org/springframework/samples/petclinic/vet/Vets.kt) profite de cette simplification :

```java
@XmlRootElement
data class Vets(var vetList: Collection<Vet>? = null)
```

 **2.** Dans les contrôleurs Spring MVC écrits en Java, il est courant d’avoir une **suite de conditions _if else_** dont chaque bloc renvoie sur une page différente.
Extrait de la méthode processFindForm de la classe Java OwnerController:

```java
if (results.isEmpty()) {
    result.rejectValue("lastName", "notFound", "not found");
    return "owners/findOwners";
} else if (results.size() == 1) {
    owner = results.iterator().next();
    return "redirect:/owners/" + owner.getId();
} else {
    model.put("selections", results);
    return "owners/ownersList";
}
```

Pour réduire le nombre de **_return_**, Kotlin permet d’utiliser le [if comme expression et non plus comme instruction](https://kotlinlang.org/docs/reference/control-flow.html). Lorsqu’une branche contient plusieurs instructions, la dernière est assignée au if ; dans l’exemple ci-dessous, c’est le nom de la page :

```kotlin
return if (results.isEmpty()) {
    result.rejectValue("lastName", "notFound", "not found")
    "owners/findOwners"
} else if (results.size == 1) {
    val foundOwner = results.iterator().next();
    "redirect:/owners/" + foundOwner.id
} else {
    model.put("selections", results)
    "owners/ownersList"
}
```

Autant dire que Kotlin sait faire plaisir à SonarQube en limitant l’usage de l’instruction return.

Une autre façon d’écrire ce code consiste à utiliser l’expression **_when_** qui est une sorte de super _switch_ _case_. Dans la classe [OwnerController](https://github.com/spring-petclinic/spring-petclinic-kotlin/blob/master/src/main/kotlin/org/springframework/samples/petclinic/owner/OwnerController.kt) Kotlin, les _if_ / _else_ disparaissent au profit de lambdas :

```java
return when {
    results.isEmpty() -> {
        result.rejectValue("lastName", "notFound", "not found")
        "owners/findOwners"
    }
    results.size == 1 -> {
       "redirect:/owners/" + results.first().id    }
    else -> {
        model.put("selections", results)
        "owners/ownersList"
    }
}
```

 **3.** Compatible avec Java 6, Kotlin avait introduit les **lambda** avant Java 8. Les **collections** ont été **enrichies** de **méthodes** permettant d’itérer, de filtrer, de trier, trouver un élément, récupérer le dernier … On peut y accéder directement, à savoir passer par un stream.

Extrait de la classe Owner codée en Java 6 :

```java
public List<Pet> getPets() {
    List<Pet> sortedPets = new ArrayList<>(getPetsInternal());
    PropertyComparator.sort(sortedPets, new MutableSortDefinition("name", true, true));
    return Collections.unmodifiableList(sortedPets);
}
```

Pendant en Kotlin :

```kotlin
fun getPets(): List<Pet> =
        pets.sortedWith(compareBy({ it.name }))
```

La méthode `find()` permet de rechercher un élément dans une collection. A noter l’utilisation de l’opérateur `?:` qui permet de lever une exception si find renvoie null.
Extrait de la classe [PetTypeFormatter.kt](https://github.com/spring-petclinic/spring-petclinic-kotlin/blob/165ce34e501da7a18ef4318edb16aafeb439145f/src/test/kotlin/org/springframework/samples/petclinic/owner/PetTypeFormatterTest.kt):

```kotlin
findPetTypes.find { it.name == text } ?:
            throw ParseException("type not found: " + text, 0)
```

 **4.** Bien que par défaut les variables ne puissent être null, nous avons vu qu’il était possible de les rendre nullable. L’ **opérateur elvis ?.** permet d’accéder à des propriétés sans craindre des NullPointerException :

```kotlin
val compName = pet.name?.toLowerCase()
```

Kotlin proposent d’autres fonctionnalités fortes intéressantes que je n’ai pas eu l’occasion de mettre en œuvre dans Spring Petclinic. Je pense notamment aux [**extension function** **s**](https://kotlinlang.org/docs/reference/extensions.html) qui permettent d’ajouter dynamiquement des méthodes à une classe.

## Des changements plus discutables

 **1.** La déclaration de **constantes** ne passe plus par l’usage des mots clés **static final** devant la propriété d’une classe. A la place, Kotlin propose de passer par des constantes de portée globale ou par des objets **companion**.

Constantes globales (extrait de [PetControllerTest.kt](https://github.com/spring-petclinic/spring-petclinic-kotlin/blob/master/src/test/kotlin/org/springframework/samples/petclinic/owner/PetControllerTest.kt)) :

```kotlin
const val TEST_OWNER_ID = 1
const val TEST_PET_ID = 1
```

Constantes internes à une classe (extrait de [PetValidator.kt](https://github.com/spring-petclinic/spring-petclinic-kotlin/blob/master/src/main/kotlin/org/springframework/samples/petclinic/owner/PetValidator.kt)) :

```kotlin
companion object {
    const val TEST_PET_ID = 1
}
```

 **2.** Un développeur Spring et JPA utilise massivement les **annotations**. Or, lorsque la propriété est multi-valuée (tableau), Kotlin requière l’utilisation du mot clé **arrayOf**
Exemple d’un mapping @OneToMany JPA extrait de [Owner.kt](https://github.com/spring-petclinic/spring-petclinic-kotlin/blob/master/src/main/kotlin/org/springframework/samples/petclinic/owner/Owner.kt) :

```kotlin
@OneToMany(cascade = arrayOf(CascadeType.ALL), mappedBy = "owner")
var pets: MutableSet<Pet> = HashSet()
```

Pour le coup, on perd en lisibilité par rapport à Java. Heureusement, ce désagrément devrait être corrigé dans une prochaine version de Kotlin : [KT-11235](https://youtrack.jetbrains.com/issue/KT-11235)

## Conclusion

Pour un développeur Java, l’apprentissage de Kotlin se fera sans trop d’effort.
Sans révolutionner Java, Kotlin permet de moderniser sa syntaxe. Il apporte quelques nouveautés fortes appréciables une fois qu’on y a goûté.

Débutant sur Kotlin, je suis preneur de toute suggestion d’amélioration (et il doit y en avoir !!). Tout contributeur est le bienvenu.

Pour aller jusqu’au bout de l’exercice, il serait intéressant de migrer le build Maven vers un build Gradle écrit en Kotlin (réf. [#2](https://github.com/spring-petclinic/spring-petclinic-kotlin/issues/2)). Là encore, avis aux amateurs.

Ressources :

- [Kotlin version of Spring Petclinic](https://github.com/spring-petclinic/spring-petclinic-kotlin)
- [Documentation de référence du language Kotlin](https://kotlinlang.org/docs/reference)
- [Developing Spring Boot applications with Kotlin](https://spring.io/blog/2016/02/15/developing-spring-boot-applications-with-kotlin)
- [Introducing Kotlin support in Spring Framework 5.0](https://spring.io/blog/2017/01/04/introducing-kotlin-support-in-spring-framework-5-0)
- [Java vs Kotlin : le comparatif des langages natifs Android](https://blog.kreactive.com/java-vs-kotlin-le-comparatif-des-langages-natifs-android)
