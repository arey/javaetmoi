---
_edit_last: "1"
author: admin
categories:
  - retour-d'expérience
date: "2024-08-25T15:54:14+00:00"
guid: https://javaetmoi.com/?p=2374
parent_post_id: null
post_id: "2374"
post_views_count: "4929"
summary: |-
  ## De Java EE à Jakarta EE

  En **2017**, **Oracle** a fait **don de la spécification Java EE** (précédemment connu sous le nom de J2EE) à la fondation **Eclipse**. Java EE regroupe différentes API utilisées aussi bien par des serveurs d’applications, des containers de servlets et des frameworks comme Quarkus ou Spring : **Servlet**, JSP, JSF, JPA, JTA, JAX-WS, JAX-RS, JAXB, WebSocket, Bean Validation, CDI, EL … {{ double-space-with-newline }}

  ![](https://javaetmoi.com/wp-content/uploads/2024/08/Jakarta_ee_logo.png)

  Sous l’égide d’Eclipse, Java EE a été rebaptisé Jakarta EE. La fondation a récupéré la base de code Java et les TCK. En **2019** est sortie une version **Jakarta EE 8** pleinement compatible avec Java EE 8. Comme seul changement notable pour les dév **, le groupId des artefacts Maven a été renommé de javax à jakarta**. Le patch du numéro de version a été incrémenté. A titre d’exemple, l’artefact jakarta.faces:jakarta.faces-api:2.3.1 est identique à javax.faces:javax.faces-api:2.3. Pas si anodin, ce changement de GAV Maven fait que notre outil de build peut être amené, via le mécanisme de dépendances transitives, à placer dans le classpath deux mêmes artefacts ayant des groupId différents. Les exclusions maven permettent de corriger le tir.

  En décembre 2020, la communauté Java est secouée par la sortie de **Java EE 9**. 20 ans de rétrocompatibilité s’écroulent. Oracle a souhaité conserver la **marque Java**. Les **packages javax.\* de la spécification Java EE ont été renommés en jakarta.\***. Certains sous-packages ont également été renommés.  {{ double-space-with-newline }} Pour exemple, la classe **_Marshaller_** de l’API JAXB change de package : de _javax.xml.bind.Marshaller_ vers jakarta.xml.bind.Marshaller
tags:
  - javaee
  - spring-boot
  - tomcat
title: Compatibilité Jakarta EE 9 de vieux frameworks
url: /2024/08/compatibilite-jakarta-ee-9-de-vieux-frameworks/

---
## De Java EE à Jakarta EE

En **2017**, **Oracle** a fait **don de la spécification Java EE** (précédemment connu sous le nom de J2EE) à la fondation **Eclipse**. Java EE regroupe différentes API utilisées aussi bien par des serveurs d’applications, des containers de servlets et des frameworks comme Quarkus ou Spring : **Servlet**, JSP, JSF, JPA, JTA, JAX-WS, JAX-RS, JAXB, WebSocket, Bean Validation, CDI, EL …   

![](/wp-content/uploads/2024/08/Jakarta_ee_logo.png)

Sous l’égide d’Eclipse, Java EE a été rebaptisé Jakarta EE. La fondation a récupéré la base de code Java et les TCK. En **2019** est sortie une version **Jakarta EE 8** pleinement compatible avec Java EE 8. Comme seul changement notable pour les dév **, le groupId des artefacts Maven a été renommé de javax à jakarta**. Le patch du numéro de version a été incrémenté. A titre d’exemple, l’artefact jakarta.faces:jakarta.faces-api:2.3.1 est identique à javax.faces:javax.faces-api:2.3. Pas si anodin, ce changement de GAV Maven fait que notre outil de build peut être amené, via le mécanisme de dépendances transitives, à placer dans le classpath deux mêmes artefacts ayant des groupId différents. Les exclusions maven permettent de corriger le tir.

En décembre 2020, la communauté Java est secouée par la sortie de **Java EE 9**. 20 ans de rétrocompatibilité s’écroulent. Oracle a souhaité conserver la **marque Java**. Les **packages javax.\* de la spécification Java EE ont été renommés en jakarta.\***. Certains sous-packages ont également été renommés.    
 Pour exemple, la classe **_Marshaller_** de l’API JAXB change de package : de _javax.xml.bind.Marshaller_ vers jakarta.xml.bind.Marshaller

A cette occasion, le numéro de version majeur a été incrémenté.   
Les coordonnées Maven Jakarta EE 8 de l’API JSF jakarta.faces:jakarta.faces-api:2.3.1 changent en jakarta.faces:jakarta.faces-api: **3.0.0** sous Jakarta EE 9.

A noter que les **packages javax du JDK** et qui n’appartiennent donc pas à Java EE ne sont **pas renommés**. On peut citer : javax.sql, javax.swing, javax.naming, javax.transaction.xa et javax.naming.

Ce changement de package Java est on ne peut plus impactant :

1. **Le code Java non migré ne fonctionne pas avec un container/runtime plus récent**
1. **Un ancien container/runtime ne fonctionne pas avec du code Java récent migré**  

Ce changement a impacté tout l’écosystème Java : les projets Open Source, le code propriétaire / métier, les IDE, les outils de build …

Quatre ans plus tard, la grande majorité des projets Open Source actifs proposent une version de leurs artefacts compatibles jakarta. Les frameworks les plus utilisés comme Quarkus ou Spring étaient attendus par leur communauté et l’ont fait relativement rapidement. Par exemple, [Spring Framework 6.0](https://spring.io/blog/2022/11/16/spring-framework-6-0-goes-ga) et [Spring Boot 3.0](https://spring.io/blog/2022/11/24/spring-boot-3-0-goes-ga) sont tous les deux sortis en novembre 2022.   
Pour migrer vers Jakarta EE 9 et le package jakarta, un projet reposant lui-même sur d’autres librairies tierces doit attendre que ses dépendances soient migrées. Cela a créé une certaine inertie dans l’écosystème Java. Par exemple, le framework Apache CXF, qui offre un support pour Spring, a dû attendre la sortie de Spring Framework 6 pour sortir à son tour en décembre 2022 la version [CXF 4](https://cxf.apache.org/docs/40-migration-guide.html).

## Migrer des applications legacy

Prenons l’exemple d’un SI composé de dizaines d’applications Java qui, pour des questions de sécurité et d’obsolescence, doivent migrer sur un Tomcat 10.

Les applications les plus modernes, basées sur **Spring Boot**, **Quarkus** ou **Micronaut**, s’appuient en général sur des stacks techniques récentes et actives. Migrer de Spring Boot 2.7 à Spring Boot 3 ne pose pas de difficultés majeures. Armé du [guide de migration Spring Boot 3](https://github.com/spring-projects/spring-boot/wiki/Spring-Boot-3.0-Migration-Guide) et d’outils comme la [recette OpenRewrite Migrate to Spring Boot 3.0](https://docs.openrewrite.org/recipes/java/spring/boot3/upgradespringboot_3_0), le projet [Spring Boot Migrator](https://github.com/spring-projects-experimental/spring-boot-migrator) (SBM) ou bien encore l’ [IntelliJ IDEA's migration tool](https://www.jetbrains.com/guide/java/tutorials/migrating-javax-jakarta/use-migration-tool/), les développeurs sont assistés dans leur travail et trouvent les ressources nécessaires sur le Net.

A contrario, les applications Java les plus anciennes du SI, pouvant avoir jusqu’à 25 ans, peuvent continuer pour certaines à s’appuyer sur des frameworks et des librairies non maintenus, abandonnés depuis des années par leurs créateurs. Lorsque cela est possible, identifier puis migrer vers une alternative est recommandé. Par exemple, l’équipe projet [Dozer](https://github.com/DozerMapper/dozer) invite à migrer vers MapStruct ou ModelMapper et propose même un plugin IntelliJ pour faciliter la tâche.


Qu’en est-il de frameworks plus structurants ? Je pense notamment à de vieux frameworks frontends sur lesquels sont conçus des centaines d’écrans d’applications de gestion.

Par exemple, **Struts 1** n’est pas compatible Jakarta EE 9 et les nouveaux packages en jakarta.\* Il s'appuie sur l'API javax.servlet.http.HttpServlet du package javax.servlet. Le conteneur web Tomcat 10 manipule quant à lui la classe jakarta.servlet.http.HttpServlet. Même chose pour **Richfaces** abandonné par JBoss depuis 2016.

Migrer les écrans d’une application de Struts 1vers Struts 6, React ou Angular est envisageable. Le cout en sera nettement plus élevé. Les délais aussi. L’automatisation aura ses limites. Autre solution : utiliser [Struts 1 Reloaded](https://github.com/weblegacy/struts1) dont la version 1.5.0 est compatible Jakarta EE 9. Maintenu par un seul et unique développeur, la base de code a divergé de l’original. Il pourrait y avoir des régressions.

Faute de budget conséquent, ces applications seraient-elles vouées à rester ad vitam æternam sur du Spring Boot 2 ? Non, la suite de cet article explique comment automatiser la compatibilité jakarta de vieux frameworks et de vielles librairies.

## Solution technique

Les développeurs du conteneur Tomcat ont adressé cette problématique lors de la sortie de Tomcat 10. En effet, Tomcat 10 sait convertir une application web existante de Java EE 8 à Jakarta EE 9 au moment du déploiement en utilisant l'[**outil de migration Apache Tomcat pour Jakarta EE.**](https://github.com/apache/tomcat-jakartaee-migration) Pratique, cet outil peut être utilisé en dehors de Tomcat, sous forme d'un **jar auto-exécutable** ou d'une tâche Ant. Contrairement à ce que son nom pourrait laisser penser, il n’est pas lié au conteneur Tomcat et pourrait être utilisé pour cibler des versions récentes de Jetty et de Wildfly.

Le projet tomcat-jakartaee-migration effectue tous les changements nécessaires pour migrer une application de Java EE 8 vers Jakarta EE 9 en **renommant chaque package** Java EE 8 vers son remplaçant Jakarta EE 9. Cela inclut les références aux package dans les classes, les constantes de type String, les fichiers de configuration, les JSP, les TLD ...   
Tous les packages javax.\* ne font pas partie de Java EE. Seuls ceux définis par Java EE sont déplacés vers l'espace de noms jakarta.\*.   
Il n'est pas nécessaire de migrer les références aux schémas XML. Les schémas ne font pas directement référence aux packages javax et Jakarta EE 9 continuera à supporter l'utilisation des schémas de Java EE 8 et antérieurs.

Cet outil propose [2 profils](https://github.com/apache/tomcat-jakartaee-migration/blob/main/src/main/java/org/apache/tomcat/jakartaee/EESpecProfiles.java): le profil partiel **TOMCAT** ciblant les conteneurs web comme Tomcat et Jetty et le **profil EE** ciblant toutes les dépendances Java EE 8.


L'outil sait parcourir différents types d'archives : jar, zip, war ... Via ses converters ([TextConverter](https://github.com/apache/tomcat-jakartaee-migration/blob/1.0.8/src/main/java/org/apache/tomcat/jakartaee/TextConverter.java), [ClassConverter](https://github.com/apache/tomcat-jakartaee-migration/blob/1.0.8/src/main/java/org/apache/tomcat/jakartaee/ClassConverter.java), [ManifestConvert](https://github.com/apache/tomcat-jakartaee-migration/blob/1.0.8/src/main/java/org/apache/tomcat/jakartaee/ManifestConverter.java)), il sait également manipuler plusieurs formats de fichiers : les classes compilées contenues dans les JAR comme le code source Java, les fichiers XML, JSON et properties, les pages JSP (jsp, jspxf, jspx), les tags JSP (tag, tld, tagx) ...

L' **outil tomcat-jakartaee-migration** peut donc aussi bien **travailler** sur des **JAR de librairies tierces** que sur du **code source métier qu'on souhaite migrer vers Jakarta EE 9 et même Jakarta EE 10**.

## Guide d'utilisation

Rendre compatible Jakarta EE 9 des librairies tierces puis les utiliser dans le code métier se fait en 2 étapes :

### Etape 1 : migrer les librairies tierces

1\. Récupérer le binaire depuis la page [https://tomcat.apache.org/download-migration.cgi](https://tomcat.apache.org/download-migration.cgi)

2\. Executer la ligne de commande suivante (exemple avec jsf-api-1.2\_14.jar) :

```
set MIGRATION_TOOL=C:\dev\jakartaee-migration\lib\jakartaee-migration-1.0.8.jar
set M2_REPO=C:\dev\maven\repository
java -jar %MIGRATION_TOOL% -profile=EE %M2_REPO%\javax\faces\jsf-api\1.2_14\jsf-api-1.2_14.jar %M2_REPO%\javax\faces\jsf-api\1.2_14-jakarta\jsf-api-1.2_14-jakarta.jar
```

Le fichier JAR jsf-api-1.2\_14-jakarta.jar généré est désormais compatible Jakarta EE 9.  
Extrait de la classe FacesServlet :

<table>
<thead><tr><th>jsf-api-1.2_14.jar compatible Java EE 8</th><th>jsf-api-1.2_14-jakarta.jar migré à Jakarta EE 9</th></tr></thead>
<tbody><tr>
<td><pre><code>package javax.faces.webapp;

import javax.faces.FacesException;
import javax.faces.FactoryFinder;
import javax.faces.context.FacesContext;
import javax.faces.context.FacesContextFactory;
import javax.faces.lifecycle.Lifecycle;
import javax.faces.lifecycle.LifecycleFactory;
import javax.servlet.Servlet;
import javax.servlet.ServletConfig;
import javax.servlet.ServletException;
import javax.servlet.ServletRequest;
import javax.servlet.ServletResponse;
import javax.servlet.UnavailableException;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

import java.io.IOException;
import java.util.ResourceBundle;
import java.util.logging.Level;
import java.util.logging.Logger;

public final class FacesServlet implements Servlet {</code></pre></td>
<td><pre><code>package jakarta.faces.webapp;

import jakarta.faces.FacesException;
import jakarta.faces.FactoryFinder;
import jakarta.faces.context.FacesContext;
import jakarta.faces.context.FacesContextFactory;
import jakarta.faces.lifecycle.Lifecycle;
import jakarta.faces.lifecycle.LifecycleFactory;
import jakarta.servlet.Servlet;
import jakarta.servlet.ServletConfig;
import jakarta.servlet.ServletException;
import jakarta.servlet.ServletRequest;
import jakarta.servlet.ServletResponse;
import jakarta.servlet.UnavailableException;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;

import java.io.IOException;
import java.util.ResourceBundle;
import java.util.logging.Level;
import java.util.logging.Logger;

public final class FacesServlet implements Servlet {</code></pre></td>
</tr></tbody>
</table>

3\. Renouveler l'opération pour le JAR du code source.  
Exemple sur jsf-api-1.2\_14-sources.jar :

```
java -jar $MIGRATION_TOOL -profile=EE $M2_REPO/javax/faces/jsf-api/1.2_14/jsf-api-1.2_14-sources.jar $M2_REPO/javax/faces/jsf-api/1.2_14-jakarta/jsf-api-1.2_14-jakarta-sources.jar
```

4\. Uploader le JAR et ses sources dans le repository binaire d’entreprise (ex : [Artifactory](https://jfrog.com/fr/artifactory/) ou [Nexus Sonatype](https://www.sonatype.com/products/sonatype-nexus-oss-download)). Privilégiez l’ajout du suffixe -jakarta au numéro de version Maven à l’utilisation d’un classifier Maven.

Cette étape de migration peut être **complètement automatisée** par un pipeline CI **Jenkins** ou **GitLab**.

### Etape 2 : utiliser les librairies tierces migrées

1\. Comme pré-requis, le code source de l'application doit avoir commencé sa migration à Jakarta EE 9 (ou supérieur).

2\. Une fois les différentes librairies et frameworks migrés et uploadés dans le repository d’entreprise, il est possible de les référencer dans les pom.xml de l'application

3\. Il est ensuite nécessaire d'adapter le code métier utilisant les classes de ces librairies qui ont changé de package, au niveau des imports du code source java, mais également dans le fichiers XML.   
Exemple du web.xml référençant jakarta.faces.webapp.FacesServlet :

```
<servlet>
    <servlet-name>Faces Servlet</servlet-name>
    <servlet-class>jakarta.faces.webapp.FacesServlet</servlet-class>
    <load-on-startup>1</load-on-startup>
</servlet>
```

Pour y arriver, 4 possibilités s'offrent à nous :

- Changements manuels par search / replace
- Appliquer la recette OpenRewrite [javaxmigrationtojakarta](https://docs.openrewrite.org/recipes/java/migrate/jakarta/javaxmigrationtojakarta) (ne gère pas le web.xml)
- Utiliser l’ [IntelliJ IDEA's migration tool](https://www.jetbrains.com/guide/java/tutorials/migrating-javax-jakarta/use-migration-tool/)
- Utiliser une nouvelle fois l'outil **tomcat-jakartaee-migration**

```
java -jar %MIGRATION_TOOL% -logLevel=FINEST -profile=EE C:\dev\project\my-webapp C:\dev\project\my-webapp-jakarta
```

Cette dernière option est à privilégier. En attente de prise en compte de la [PR #60](https://github.com/apache/tomcat-jakartaee-migration/pull/60) de mon collègue [Marco](https://github.com/marcosemiao) pour exclure le sous-répertoire .git et utiliser le répertoire source comme cible.

5\. Vérifier que tout compile

```
mvn clean install
```

## Conclusion

Cette solution présente plusieurs avantages :

- **Simplicité**
- **Cout** défiant toute concurrence
- Réutilisation d'un **outil Open Source maintenu par l'équipe Tomcat** et massivement éprouvé
- **Automatisation** possible  

Son principal inconvénient réside dans le fait que **l’application continue à utiliser une librairie non maintenue**. A moyen termes, trouver un financement pour refondre ou migrer l’application vers une technologie cible reste donc préconisé.

Enfin, d’autres outils que celui d’Apache existe, par exemple [Eclipse Transformer](https://github.com/eclipse/transformer). Avant de vous lancer, comparez-les.

**Ressources** :

- [Apache Tomcat migration tool for Jakarta EE](https://github.com/apache/tomcat-jakartaee-migration) (GitHub)
- [Transition from Java EE to Jakarta EE](https://blogs.oracle.com/javamagazine/post/transition-from-java-ee-to-jakarta-ee) (Oracle Java Magazine)
- [Javax to Jakarta Namespace Ecosystem Progress](https://jakarta.ee/blogs/javax-jakartaee-namespace-ecosystem-progress/) (Jakarta EE)
- [Using IntelliJ IDEA's migration tool](https://www.jetbrains.com/guide/java/tutorials/migrating-javax-jakarta/use-migration-tool/) (Jetbrains)
- [Eclipse Transformer](https://github.com/eclipse/transformer) (GitHub)
- [Javax to Jakarta Tales From the Crypt](https://communityovercode.org/wp-content/uploads/2023/10/javax-to-jakarta-tales-from-the-crypt-v2-shawn-mckinney.pdf) (Shawn McKinney)  
