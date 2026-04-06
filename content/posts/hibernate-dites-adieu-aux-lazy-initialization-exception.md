---
_edit_last: "1"
author: admin
categories:
  - orm
date: "2012-03-30T20:39:43+00:00"
guid: http://javaetmoi.com/?p=54
parent_post_id: null
post_id: "54"
post_views_count: "23643"
summary: 'Dans ce deuxième ticket, j’aimerais vous parler du projet [**Hibernate Hydrate**](https://github.com/arey/hibernate-hydrate) \[1\] que j’ai récemment publié sur GitHub. Au cœur de ce projet : une seule classe Java proposant **une unique fonctionnalité**. En quelques années, c’est la seconde fois que j’ai eu besoin de coder ce genre de fonctionnalité. Aussi, je me suis dit qu’il serait pratique de l’avoir sous le coude pour une prochaine fois et, au passage, vous en faire profiter.'
tags:
  - cloudbees
  - github
  - hibernate
  - hql
  - jenkins
  - jpa
  - open-source
  - pattern
title: Dites adieu aux LazyInitializationException
url: /2012/03/hibernate-dites-adieu-aux-lazy-initialization-exception/

---
{{< figure src="/wp-content/uploads/2012/03/logo%5Fhibernate.png" alt="logo\_hibernate" caption="logo\_hibernate" >}}

Dans ce deuxième ticket, j’aimerais vous parler du projet [**Hibernate Hydrate**](https://github.com/arey/hibernate-hydrate) \[1\] que j’ai récemment publié sur GitHub. Au cœur de ce projet : une seule classe Java proposant **une unique fonctionnalité**. En quelques années, c’est la seconde fois que j’ai eu besoin de coder ce genre de fonctionnalité. Aussi, je me suis dit qu’il serait pratique de l’avoir sous le coude pour une prochaine fois et, au passage, vous en faire profiter.

**Origine des lazy exceptions**

En quoi consistent ce projet et cette fameuse fonctionnalité ? Eh bien, sous certaines conditions, résoudre un **problème récurrent** lors de l’utilisation d’Hibernate. En effet, lorsque l’on tente d’accéder à un **objet détaché de la session Hibernate**, ce dernier n’est pas forcément entièrement chargé en mémoire : son proxy ou ses propriétés peuvent ne pas être initialisés, ce qui est par exemple le cas d’une relation déclarée comme **paresseuse** (ou **lazy**). Et c’est à cet instant-là, qu’Hibernate lève la tant redoutée _**LazyInitializationException**_.  
Par objet détaché, j’entends un objet évincé de la session (retirée du cache de premier niveau par un _session.clear()_ ou un _evict()_) ou dont la session est fermée ( _session.close()_)  
Dans une application, ce phénomène est susceptible de se produire à plusieurs niveaux :

- **Couche** **présentation** : contrôleur (ex : action Struts) ou rendu de la vue (ex : JSP)
- Exposition d’un **web service** : marshalling XML, mapping dozer …

La documentation d’Hibernate propose plusieurs solutions pour remédier à ce problème. Plus encore, elle explique ce qu’il faut éviter de faire, comme par exemple ouvrir une autre unité de travail (transaction) pour charger les données manquantes.  
**Solutions préconisées**

Pattern Open Session In View  

Une première solution consiste à utiliser le pattern [**Open Session In View**](https://community.jboss.org/wiki/OpenSessionInView) \[2\]. Dans une application web, ce pattern peut par exemple être implémenté à l’aide d’un filtre de servlets. L’arrivée d’une requête HTTP initie l’ouverture d’une transaction et de la session Hibernate correspondante. Une fois la vue rendue et prête être renvoyée au client, la session est fermée et la transaction est validée.  
Le pattern Open Session In View ne peut pas s’appliquer dans une architecture technique 3 tiers où la couche présentation et la couche métier sont déployées physiquement sur 2 serveurs différents, et donc 2 JVMs. Ce pattern n’est également pas valable dans le cadre d’une application web riche utilisant Ajax et JavaScript pour récupérer puis parcourir le modèle métier.

Pré-chargement sur mesure

Personnellement, je recommande généralement à ce que les transactions soient gérées au niveau de **la couche métier**. En effet, à ce niveau, le service métier connait l’usage des objets qu’il va charger depuis la base de données. Il est capable d’utiliser le DAO ayant la [stratégie de pré-chargement](https://community.jboss.org/wiki/AShortPrimerOnFetchingStrategies) \[3\] (ou **fetching**) adaptée au traitement métier.

Pour rappel, le pré-chargement des relations peut être configuré de 2 manières :

1. **statiquement** au niveau du **mapping** Hibernate (en XML ou par annotations)
1. **dynamiquement** lors du requêtage en **HQL** ( _JOIN FETCH_) ou par l’API **Criteria** (méthode _setFetchMode()_)

Par défaut, dans Hibernate 3.x, les associations vers une autre entité ou une collection d’entités sont chargées tardivement ; c’est-à-dire à la demande, lorsque l’on essaie d’accéder à l’entité ou à la collection (et que la session est ouverte). Qui plus est, les stratégies définies statiquement ne sont pas forcément utilisées lors d’un requêtage HQL.

Une **bonne pratique** issue du [guide de référence d’Hibernate](http://docs.jboss.org/hibernate/orm/3.5/reference/en/html/performance.html#performance-fetching) \[4\] consiste à **conserver le comportement par défaut** d’Hibernate et à redéfinir la stratégie de pré-chargement à chaque usage. Cela permet d’optimiser votre code et de ramener les données dont vous avez strictement besoin.

Comme illustré dans l’article [Hibernate Survival Guide](http://wiki.objetdirect.com/wiki/index.php?title=Hibernate_Survival_Guide_Partie_3) \[5\], et grâce au **cache de premier niveau** d’Hibernate, il est parfois plus performant de découper sa requête en plusieurs requêtes, notamment lorsque la grappe d’objets est complexe et la cardinalité des associations importante.

**  
Hybernate Hydrate à la rescousse**

La solution que je vais vous présenter peut être utilisée conjointement avec la solution du pré-chargement sur mesure.

La méthode statique _deepHydrate_ de la classe _LazyLoadingUtil_ permet de charger dans sa globalité la grappe d’objets qui lui est passée en paramètre. Seule contrainte, cette méthode doit être appelée avant que la session Hibernate et la transaction associée ne soient clôturées.

Voici un exemple d’utilisation :

```java
Employee employee = (Employee) session.get(Employee.class, 1);
LazyLoadingUtil.deepHydrate(session, employee);
```

Techniquement, la méthode _deepHydrate()_ utilise le méta-modèle Hibernate (interface _ClassMetadata_) pour **parcourir l’ensemble du graphe des objets persistés** et déterminer le type des propriétés et des relations du modèle. Ainsi, elle peut naviguer **récursivement** dans le graphe. Les **proxy** rencontrés sont initialisés puis résolus. Les **collections persistantes** sont initialisés puis itérés.

Dans le cas d’un **graphe cyclique**, un mécanisme de garde permet d’éviter toute boucle infinie.

La classe _TestLazyLoadingUtil_ propose des exemples d’utilisation.

Une variante est disponible pour les applications utilisant JPA avec Hibernate pour provider : _JpaLazyLoadingUtil_.

Pour l’essayer, vous avez le choix entre un copier / coller, un git clone ou bien l’ajout d’une dépendance maven et du repo qui va avec :

```xml
<dependency>
    <groupId>com.javaetmoi.core</groupId>
    <artifactId>javaetmoi-hibernate4-hydrate</artifactId>
    <version>2.0</version>
</dependency>

```

Les artefacts du projet Hybernate Hydrate sont [disponibles sur Maven Central](http://repo1.maven.org/maven2/com/javaetmoi/core/javaetmoi-hibernate4-hydrate/).

**Conclusion**

Pour terminer cette présentation, voici un tableau récapitulatif qui devrait vous permettre d’orienter votre choix sur l’usage ou non de cette petite librairie :

**Scénarios pour lesquels écarter cette solution****Scénarios favorables à son utilisation**

1. Utilisation du pattern Open Session in View
1. Problématiques fortes de performance
1. Grappes d’objets risquant de remonter toute la base de données

1. Grappe d’objets constituée de nombreuses classes
1. Développement rapide d’une application avec chantier d’optimisations portant sur les requêtes critiques
1. Exploitation du cache de niveau 2 d’Hibernate pour les données en « bout de grappe » (ex : données du référentiel).
1. Outil ayant besoin de charger toute une grappe d’objets en mémoire

De mon côté, ce modeste travail de capitalisation m’a permis de renouer avec l’open-source ;  en tant que contributeur j’entends. Mon dernier code poussé sur Source Forge datait en effet de l’an 2000 …  
Cela m’aura également permis de me familiariser davantage avec GitHub : syntaxe MarkDown, pages wiki gérées par git ou bien encore les releases avec maven. Ce dernier point fera d’ailleurs l’objet d’un prochain article.  
J’ai également pu adhérer au programme Free and OpenSource (FOSS) de CloudBees, ce qui vous permet d’accéder librement au [Jenkins d’Hibernate Hydrate](https://javaetmoi.ci.cloudbees.com/job/Hibernate-Hydrate/) \[6\].

Enfin, si vous êtes un jour amené à utiliser ce code, je serais intéressé de le savoir. Et si vous voulez contribuer (ex : support d’autres ORM, annotation + post-processeur Spring …), les portes sont grandes ouvertes.

Références :

1. [Projet Hibernate Hydrate](https://github.com/arey/hibernate-hydrate) hébergé sur Github
1. [Open Session In View](https://community.jboss.org/wiki/OpenSessionInView) du wiki Hibernate de JBoss
1. [A Short Primer On Fetching Strategies](https://community.jboss.org/wiki/AShortPrimerOnFetchingStrategies) du wiki Hibernate de JBoss
1. [Performance fetching](http://docs.jboss.org/hibernate/orm/3.5/reference/en/html/performance.html#performance-fetching) du guide de référence d’Hibernate
1. [Hibernate Survival Guide](http://wiki.objetdirect.com/wiki/index.php?title=Hibernate_Survival_Guide_Partie_3) du wiki d’Object Direct
1. [Jenkins d’Hibernate Hydrate](https://javaetmoi.ci.cloudbees.com/job/Hibernate-Hydrate/) hébergé sur la plateforme DEV@Cloud de CloudBees\[6\].
