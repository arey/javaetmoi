---
_edit_last: "1"
_thumbnail_id: "1788"
_xmlsf_image_featured:
  caption: ""
  loc: https://javaetmoi.com/wp-content/uploads/2017/11/gradle-logo.png
  title: gradle-logo
author: admin
categories:
  - retour-d'expérience
featureImage: /wp-content/uploads/2017/11/gradle-logo.png
featureImageAlt: gradle-logo
date: "2017-11-22T07:40:41+00:00"
guid: http://javaetmoi.com/?p=1786
parent_post_id: null
post_id: "1786"
post_views_count: "5751"
summary: |-
  [![](http://javaetmoi.com/wp-content/uploads/2017/11/gradle-logo-150x150.png)](http://javaetmoi.com/wp-content/uploads/2017/11/gradle-logo.png) En guise de conclusion de [mon précédent billet](http://javaetmoi.com/2017/09/migrez-application-java-spring-boot-vers-kotlin/), je proposais de **migrer le [build Maven](https://github.com/spring-petclinic/spring-petclinic-kotlin/blob/c66b152b83be2cdf8c28ca4e3e8869158b47a40b/pom.xml) d** **’une application web Spring Boot 2 en un build Gradle bas** **é sur le langage Kotlin**. C’est désormais chose faite. Mais bien que Gradle **privil** **égie** aujourd’hui l’usage du **DSL** **Kotlin** au détriment de **Groovy**, son [guide d’utilisation](https://docs.gradle.org/4.3.1/userguide/userguide.html) n’a pas encore été actualisé et il est difficile de trouver de la documentation. Il faut passer par le projet GitHub [kotlin-dsl](https://github.com/gradle/kotlin-dsl) pour accéder à quelques tutoriaux et des exemples. Heureusement, GitHub fourmille d’autres d’exemples, notamment du côté des projets soutenus par les contributeurs Pivotal sur Spring Boot.

  Sans plus tarder, voici le fichier de conf [build.gradle.kts](https://github.com/spring-petclinic/spring-petclinic-kotlin/blob/master/build.gradle.kts) de la version Kotlin de Spring Petclinic.
tags:
  - gradle
  - kotlin
  - spring-boot
title: Build Gradle en Kotlin d’une webapp Spring Boot
url: /2017/11/build-gradle-dsl-kotlin-webapp-spring-boot/

---
[![](/wp-content/uploads/2017/11/gradle-logo.png)](/wp-content/uploads/2017/11/gradle-logo.png) En guise de conclusion de [mon précédent billet](/2017/09/migrez-application-java-spring-boot-vers-kotlin/), je proposais de **migrer le [build Maven](https://github.com/spring-petclinic/spring-petclinic-kotlin/blob/c66b152b83be2cdf8c28ca4e3e8869158b47a40b/pom.xml) d** **’une application web Spring Boot 2 en un build Gradle bas** **é sur le langage Kotlin**. C’est désormais chose faite. Mais bien que Gradle **privil** **égie** aujourd’hui l’usage du **DSL** **Kotlin** au détriment de **Groovy**, son [guide d’utilisation](https://docs.gradle.org/4.3.1/userguide/userguide.html) n’a pas encore été actualisé et il est difficile de trouver de la documentation. Il faut passer par le projet GitHub [kotlin-dsl](https://github.com/gradle/kotlin-dsl) pour accéder à quelques tutoriaux et des exemples. Heureusement, GitHub fourmille d’autres d’exemples, notamment du côté des projets soutenus par les contributeurs Pivotal sur Spring Boot.

Sans plus tarder, voici le fichier de conf [build.gradle.kts](https://github.com/spring-petclinic/spring-petclinic-kotlin/blob/master/build.gradle.kts) de la version Kotlin de Spring Petclinic.

## Le fichier build.gradle.kts

```java
import org.jetbrains.kotlin.gradle.tasks.KotlinCompile

buildscript {

    extra["kotlinVersion"] = "1.1.60"
    extra["springBootVersion"] = "2.0.0.M6"
    extra["jUnitVersion"] = "5.0.0"
    extra["boostrapVersion"] = "3.3.6"
    extra["jQueryVersion"] = "2.2.4"
    extra["jQueryUIVersion"] = "1.11.4"

    val springBootVersion: String by extra

    repositories {
        mavenCentral()
        maven("https://repo.spring.io/milestone")
    }

    dependencies {
        classpath("org.springframework.boot:spring-boot-gradle-plugin:$springBootVersion")
        classpath("org.junit.platform:junit-platform-gradle-plugin:1.0.2")
    }
}

plugins {
    val kotlinVersion = "1.1.60"

    id("org.jetbrains.kotlin.jvm") version kotlinVersion
    id("org.jetbrains.kotlin.plugin.spring") version kotlinVersion
    id("io.spring.dependency-management") version "1.0.3.RELEASE"
}

apply {
    plugin("org.springframework.boot")
}

val kotlinVersion: String by extra
val springBootVersion: String by extra
val jUnitVersion: String by extra
val boostrapVersion: String by extra
val jQueryVersion: String by extra
val jQueryUIVersion: String by extra

version = springBootVersion

tasks {
    withType<KotlinCompile> {
        kotlinOptions {
            jvmTarget = "1.8"
            freeCompilerArgs = listOf("-Xjsr305=strict")
        }
    }
}

repositories {
    mavenCentral()
    maven("https://repo.spring.io/milestone")
}

dependencies {
    compile("org.springframework.boot:spring-boot-starter-actuator")
    compile("org.springframework.boot:spring-boot-starter-cache")
    compile("org.springframework.boot:spring-boot-starter-data-jpa")
    compile("org.springframework.boot:spring-boot-starter-web")
    compile("org.springframework.boot:spring-boot-starter-thymeleaf")
    compile("javax.cache:cache-api")
    compile("org.jetbrains.kotlin:kotlin-stdlib:$kotlinVersion")
    compile("org.jetbrains.kotlin:kotlin-reflect:$kotlinVersion")
    compile("org.webjars:webjars-locator")
    compile("org.webjars:jquery:$jQueryVersion")
    compile("org.webjars:jquery-ui:$jQueryUIVersion")
    compile("org.webjars:bootstrap:$boostrapVersion")

    testCompile("org.springframework.boot:spring-boot-starter-test")
    testCompile("org.junit.jupiter:junit-jupiter-api:$jUnitVersion")
    testRuntime("org.junit.jupiter:junit-jupiter-engine:$jUnitVersion")

    runtime("org.hsqldb:hsqldb")
    runtime("mysql:mysql-connector-java")
}
```

## Quelques explications

Le **DSL Kotlin pour Gradle** a facilité la déclaration des plugins en introduisant le [**bloc _plugins {}_**](https://github.com/gradle/kotlin-dsl/blob/master/doc/getting-started/Configuring-Plugins.md). Par exemple, le plugin de compilation du code source Kotlin de l’application est déclaré dans ce bloc.
Suite à [un bug JUnit 5](https://github.com/junit-team/junit5/issues/768), le plugin **junit-platform-gradle-plugin** a dû rester déclaré dans le bloc _buildscript {}._ Un contournement existe, mais il ne fonctionne pas correctement lorsque les plugins sont tirés de plusieurs repos Maven, ce qui est le cas du plugin **spring-boot-gradle-plugin** en version Milestone 2.0.0.M6 qui n’est pas encore publié dans Maven Central.

Le plugin Spring Boot pour Gradle **org.springframework.boot** joue un triple rôle :

1. La **construction** le **uber-JAR exécutable**
1. L’ **exécution** de la webapp via la ligne de commande _gradle bootRun_
1. La **gestion des dépendances**

Attardons-nous un moment sur la gestion des dépendances. Fonctionnant de concert avec le [plugin Dependency Management](https://github.com/spring-gradle-plugins/dependency-management-plugin/) **io.spring.dependency-management**, le plugin Spring Boot permet d’éviter de déclarer la version des dépendances déclarées dans le bloc _dependencies {}_ ; du moins, celles déclarées dans le **BOM Maven spring-boot-starter-parent** qu’il importe.

La centralisation des versions non déclarées dans le BOM passe par l’usage de la **propriété _extra_** déclarée sous forme d’extension Kotlin. Il est toutefois regrettable qu’ _extra_ ne soit pas visible du bloc _plugins {}_.

## Conclusion

Par rapport au [pom.xml](https://github.com/spring-petclinic/spring-petclinic-kotlin/blob/c66b152b83be2cdf8c28ca4e3e8869158b47a40b/pom.xml) d’origine, le build Gradle n’intègre pas encore la génération du CSS à partir de LESS ([issue #4](https://github.com/spring-petclinic/spring-petclinic-kotlin/issues/4)).
Novice en Kotlin et en Gradle, toute suggestion d’amélioration du [build.gradle.kts](https://github.com/spring-petclinic/spring-petclinic-kotlin/blob/master/build.gradle.kts) est la bienvenue.
J’attends vos pull requests :-)

Références :

- [Better dependency management for Gradle](https://spring.io/blog/2015/02/23/better-dependency-management-for-gradle) (Andy Wilkinson)
- [Spring Boot Gradle plugin](https://docs.spring.io/spring-boot/docs/current/reference/htmlsingle/#build-tool-plugins-gradle-plugin) (Manuel de référence de Spring Boot)
- Projet GitHub [sdeleuze/pring-kotlin-functional](https://github.com/sdeleuze/spring-kotlin-functional) (Sébastien Deleuze)
- Projet GitHub [mixitconf/mixit](https://github.com/mixitconf/mixit) (MiXiT website)
