---
_edit_last: "1"
_encloseme: "1"
author: admin
categories:
  - maven
  - retour-d'expérience
date: "2025-07-05T17:06:00+00:00"
thumbnail: /wp-content/uploads/2025/07/Screenshot-site-JSpecify.png
featureImage: /wp-content/uploads/2025/07/Screenshot-site-JSpecify.png
guid: https://javaetmoi.com/?p=2599
parent_post_id: null
post_id: "2599"
summary: '<br>La gestion de la **nullabilité** en Java a longtemps été source de bugs et de fragmentation. Contrairement à Kotlin par exemple, Java ne possède pas encore nativement de moyen d’exprimer la nullité d’un type. Qui n’aura donc jamais ragé contre une **NullPointerException** survenue en production ? En juin 2024, avec l’arrivée de la spécification [**JSpecify**](https://jspecify.dev/), soutenue par des acteurs majeurs comme Google, Microsoft, JetBrains, Oracle, Sonar ou bien encore Broadcom (Spring), l’écosystème Java dispose enfin d’une **bibliothèque unifiée d’annotations de nullité**. Pour bénéficier d’une détection efficace des NullPointerException dès la compilation, il est nécessaire de coupler JSpecify à des outils d’analyse statique comme [**NullAway**](https://github.com/uber/NullAway) (Uber) et [**ErrorProne**](https://errorprone.info/) (Google). <br> Ce court article explique comment mettre en place sur un projet d’entreprise la **configuration Maven** correspondante qui fera casser votre build et votre CI lorsque vous essayerez de passer une variable _null_ en paramètre d’une méthode qui ne les accepte pas.'
tags:
  - errorprone
  - jspecify
  - maven
  - nullaway
title: 'JSpecify + NullAway + ErrorProne : la configuration Maven ultime pour dire adieu aux NullPointerException'
url: /2025/07/jspecify-nullaway-errorprone-la-configuration-maven-ultime-pour-dire-adieu-aux-nullpointerexception/

---
  
La gestion de la **nullabilité** en Java a longtemps été source de bugs et de fragmentation. Contrairement à Kotlin par exemple, Java ne possède pas encore nativement de moyen d’exprimer la nullité d’un type. Qui n’aura donc jamais ragé contre une **NullPointerException** survenue en production ? En juin 2024, avec l’arrivée de la spécification [**JSpecify**](https://jspecify.dev/), soutenue par des acteurs majeurs comme Google, Microsoft, JetBrains, Oracle, Sonar ou bien encore Broadcom (Spring), l’écosystème Java dispose enfin d’une **bibliothèque unifiée d’annotations de nullité**. Pour bénéficier d’une détection efficace des NullPointerException dès la compilation, il est nécessaire de coupler JSpecify à des outils d’analyse statique comme [**NullAway**](https://github.com/uber/NullAway) (Uber) et [**ErrorProne**](https://errorprone.info/) (Google).   
 Ce court article explique comment mettre en place sur un projet d’entreprise la **configuration Maven** correspondante qui fera casser votre build et votre CI lorsque vous essayerez de passer une variable _null_ en paramètre d’une méthode qui ne les accepte pas.

{{< figure src="/wp-content/uploads/2025/07/Screenshot-site-JSpecify.png" alt="" caption="" >}}

### Dépendance Maven JSpecify

Ajoutez simplement la dépendance suivante au niveau de la balise <dependencies> de votre pom.xml :


```xml
<dependency>
    <groupId>org.jspecify</groupId>
    <artifactId>jspecify</artifactId>
    <version>1.0.0</version>
</dependency>
```

A ce stade, les IDE comme [IntelliJ supportant JSpecify](https://www.jetbrains.com/idea/whatsnew/#page__content-jspecify-support) seront à même de détecter des erreurs. Exemple extrait de [Sring Petclinic](https://github.com/spring-projects/spring-petclinic) dont les packages Java sont annotés avec **@NullMarked** :

![](/wp-content/uploads/2025/07/word-image-2599-1.png)

Dans le cas où ces warnings n’apparaissent pas dans IntelliJ, vérifier que les **inspections Nullability problems** sont bien activées :

{{< figure src="/wp-content/uploads/2025/07/word-image-2599-2.png" alt="" caption="" >}}

### Configuration du Maven Compiler Plugin avec NullAway et ErrorProne

Pour faire échouer le build Maven dans le cas où un développeur ne respecterait pas les annotations JSpecify, le compilateur Java doit être strictement configuré à l’aide des plugins **Error Prone** de Google et de son extension **NullAway** d'Uber :


```xml
<plugin>
 <groupId>org.apache.maven.plugins</groupId>
 <artifactId>maven-compiler-plugin</artifactId>
 <configuration>
   <parameters>true</parameters>
   <compilerArgs>
     <arg>-XDcompilePolicy=simple</arg>
     <arg>--should-stop=ifError=FLOW</arg>
     <arg>-XDaddTypeAnnotationsToSymbol=true</arg>
     <arg>-Xplugin:ErrorProne
       -XepOpt:NullAway:AnnotatedPackages=com.javaetmoi.myapp
       -XepOpt:NullAway:UnannotatedSubPackages=com.javaetMoi.myapp.controller.api,com.javaetMoi.myapp.controller.dto
       -XepOpt:NullAway:JSpecifyMode=true
       -XepDisableAllChecks
       -Xep:NullAway:ERROR
       -XepExcludedPaths:.*/src/test/java/.*
       -XepDisableWarningsInGeneratedCode
     </arg>
   <annotationProcessorPaths>
     <path>
       <groupId>com.google.errorprone</groupId>
       <artifactId>error_prone_core</artifactId>
       <version>2.42.0</version>
     </path>
     <path>
       <groupId>com.uber.nullaway</groupId>
       <artifactId>nullaway</artifactId>
       <version>0.12.11</version>
     </path>
   </annotationProcessorPaths>
 </configuration>
</plugin>
```

**Explications clés :**

- L'option **-Xep:NullAway:ERROR** fait échouer le build Maven lorsqu’un éventuel NullPointerException est détecté. Par défaut, de simples WARNING sont générés dans la console et risquent donc de passer inaperçus.  

- L’option - **Xplugin:ErrorProne** active le plugin ErrorProne.  

- L’option **-XepDisableAllChecks** désactive toutes les règles de vérification de code ErrorProne. On n’utilise ici ErrorProne que pour la nullsafety. Libre à vousd’utiliser pleinement ErrorProne ou pas.  

- L’option **-XepOpt:NullAway:AnnotatedPackages=com.javaetmoi.myapp** active NullAway sur le package Java racine de l’application métier. A noter que cette option peut être remplacer par **-XepOpt:NullAway:OnlyNullMarked** afin de ne scanner que les packages annotés avec **@NullMarked**.  

- A contrario, l’option **-XepOpt:NullAway:UnannotatedSubPackages=com.javaetMoi.myapp.controller.api,com.javaetMoi.myapp.controller.dto** désactive NullAway sur une liste de sous-packages. Cela permet d’exclure le code généré par des plugins comme cxf-codegen-plugin ou MapStruct qui ne supportent pas encore JSpecify.  

- Dans le cadre d’utilisation de JSpecify dans un projet legacy, il peut-être intéressant d’exclure de l’analsyse les classes de tests avec l'option **-XepExcludedPaths:.\*/src/test/java/.\***  

- L'option **-XepOpt:NullAway:JSpecifyMode=true** active le support complet de JSpecify et exploite pleinement la [sémantique de JSpecify](https://github.com/uber/NullAway/wiki/JSpecify-Support), notamment au niveau des types génériques.   

- L'argument javac **-XDaddTypeAnnotationsToSymbol=true** est requis par la version 0.12.11 de NullAway lors de l'[utilisation d'une version de Java antérieure à **Java 22**](https://github.com/uber/NullAway/wiki/JSpecify-Support#supported-jdk-versions).

Toutes les options de [NullAway](https://github.com/uber/NullAway) peuvent être retrouvées sur sa page de [Configuration](https://github.com/uber/NullAway/wiki/Configuration).

A partir de la version 16 du langage Java, la [documentation d'installation d'error prone](https://errorprone.info/docs/installation) explique comment activer des flags à la JVM via le fichier **.mvn/jvm.config**:


```bash
--add-exports jdk.compiler/com.sun.tools.javac.api=ALL-UNNAMED
--add-exports jdk.compiler/com.sun.tools.javac.file=ALL-UNNAMED
--add-exports jdk.compiler/com.sun.tools.javac.main=ALL-UNNAMED
--add-exports jdk.compiler/com.sun.tools.javac.model=ALL-UNNAMED
--add-exports jdk.compiler/com.sun.tools.javac.parser=ALL-UNNAMED
--add-exports jdk.compiler/com.sun.tools.javac.processing=ALL-UNNAMED
--add-exports jdk.compiler/com.sun.tools.javac.tree=ALL-UNNAMED
--add-exports jdk.compiler/com.sun.tools.javac.util=ALL-UNNAMED
--add-opens jdk.compiler/com.sun.tools.javac.code=ALL-UNNAMED
--add-opens jdk.compiler/com.sun.tools.javac.comp=ALL-UNNAMED
```



Avec cette configuration Maven, toute tentative d’accès à une référence potentiellement nulle sera détectée… dès la compilation, que ce soit sur notre poste de dév ou notre CI Jenkins, GitHub ou GitLab ! Fini les NullPointerException surprises en production.

Exemple d’une commande **_mvn compile_** sur l’exemple précédent :


```text
[ERROR] COMPILATION ERROR :
[INFO] -------------------------------------------------------------
[ERROR] /Users/arey/Dev/GitHub/spring-petclinic/spring-petclinic/src/main/java/org/springframework/samples/petclinic/owner/OwnerController.java:[106,82] [NullAway] passing @Nullable parameter 'lastName' where @NonNull is required
    (see http://t.uber.com/nullaway )
```

### Conclusion

Cinq années auront été nécessaires par le groupe de travail JSpecify pour formaliser et se mettre d’accord sur **quatre annotations Java**. Depuis un an, nos **outillages**, nos **IDE** et nos **frameworks** convergent vers ce lot d’annotations. Quelques **bugs de jeunesse** existent encore, à l’image de [ce bug Maven Build Cache Extension](https://github.com/apache/maven-build-cache-extension/pull/358) corrigé par mon collègue Marco et qui faisait échouer la synchronisation Maven IntelliJ avec le message "java: plug-in not found: ErrorProne".   

A nos **projets métiers** de se mettre à JSpecify et d’être prêts pour Spring Framework 7 et Spring Boot 4 qui sortiront fin 2025.   
 Si vos projets exploitent les annotations JSR-305 ou JetBrains, migrez vers JSpecify à l’aide de la recette OpenRewrite [MigrateToJSpecify](https://docs.openrewrite.org/recipes/java/jspecify/migratetojspecify).

Sachez enfin que Dan Smith a proposé la [JEP draft: Null-Restricted and Nullable Types (Preview)](https://openjdk.org/jeps/8303099) visant à ajouter des marqueurs syntaxiques directement au niveau du langage Java. Adopter JSpecify aujourd’hui facilitera l’adoption de cette JEP.
