---
_edit_last: "1"
author: admin
categories:
  - test
date: "2016-03-24T07:36:23+00:00"
thumbnail: wp-content/uploads/2016/03/artist.png
featureImage: wp-content/uploads/2016/03/artist.png
featureImageAlt: "artist"
guid: http://javaetmoi.com/?p=1553
parent_post_id: null
post_id: "1553"
post_views_count: "6162"
summary: |-
  Les **jeux de données** font partie intégrante des tests. Elaborer un jeu de données demande une **connaissance fonctionnelle**, aussi bien sur la nature des données que sur le scénario de test envisagé. Utiliser des jeux de **données** **réalistes** participe à la compréhension du **scénario de test** et, donc, à sa documentation.
  S’il vous était possible de **générer** ces fameux jeux de données, seriez-vous intéressés ?C’est précisément l’objet de ce billet et d’un modeste **outil** baptisé **JavaBean Marshaller**.

  ![artist](wp-content/uploads/2016/03/artist.png)
tags:
  - javapoet
  - test
title: Génération de jeux de données Java
url: /2016/03/generation-jeux-donnees-java/

---
Les **jeux de données** font partie intégrante des tests. Elaborer un jeu de données demande une **connaissance fonctionnelle**, aussi bien sur la nature des données que sur le scénario de test envisagé. Utiliser des jeux de **données** **réalistes** participe à la compréhension du **scénario de test** et, donc, à sa documentation.
S’il vous était possible de **générer** ces fameux jeux de données, seriez-vous intéressés ?C’est précisément l’objet de ce billet et d’un modeste **outil** baptisé **JavaBean Marshaller**.

## Contexte

Au cours de mes missions, j’ai rencontré plusieurs **outils maisons de génération de jeux de données**(souvent abusivement appelés mocks). Leur fonctionnement consiste à pouvoir **sauvegarder** des grappe d’objets au format XML ou JSON, puis à les **recharger**. Ces jeux de données sont utilisés dans des tests ou pour bouchonner des adhérences indisponibles.
Le déclenchement de la sauvegarde des jeux de données peut-être réalisé en AOP.

Forts pratiques, ces outils souffrent malgré tout de certaines **limitations**:

- Relative lenteur de rechargement des fichier XML et JSON, en particulier pour des tests unitaires dont l’exécution doit rester rapide
- Impossibilité de factoriser des morceaux de jeux de données entre plusieurs tests
- Maintenance et refactoring rendus difficiles
- Complexité des graphes d’objets cycliques (IDREF en XML ou XStream JSON)
- Complexité des relations bidirectionnelles
- Format des jeux de données couplé à une technologie de marshalling (ex : JAXB, Jackson)

Partant de ce constat, je me suis demandé s’il était possible de remédier à ces limitations. La solution qui m’est instantanément venue à l’esprit fut d’utiliser un autre format que le XML ou le JSON, à savoir le **Java**. Après tout, lorsqu’on écrit manuellement des jeux de données, c’est en Java qu’on le fait (sauf si on passe par des outils tels DbUnit). Le langage Java reste ce qu’il y’a de plus naturel pour des développeurs Java. Qui plus est, vérifiés à la compilation, les jeux de données seront simples à maintenir.

## JavaBean Marshaller

Disponible en Open Source sur github, le [**projet JavaBean Marshaller**](https://github.com/arey/javabean-marshaller) fournit la classe utilitaire [JavaBeanMarshaller](https://github.com/arey/javabean-marshaller/blob/master/src/main/java/com/javaetmoi/javabean/JavaBeanMarshaller.java). En paramètre de la méthode **_generateJavaCode_**, vous passez l’objet racine de votre grappe d’objets Java. En sortie, **une classe Java permettant de réinstancier votre grappe sera créée.**

Un exemple sera bien plus parlant. Prenons le diagramme de classes ci-dessous.![artist](wp-content/uploads/2016/03/artist.png)
Non représentés sur ce diagramme, les classes _Album_ et _Artiste_ possèdent des getter / setter et constructeur sans argument.

Imaginons l’instance d’une classe _Artist_ référençant un seul et unique _Album_.
Voici le bout de code correspondant et volontairement très compact :

```java
Artist u2 = new Artist(1, "U2", ArtistType.GROUP);
Album joshuaTree = new Album("The Joshua Tree", LocalDate.of(1987, Month.MARCH, 9), u2);
u2.getAlbums().add(joshuaTree);
```

Ajoutons la dépendance maven :

```xhtml
<dependency>
    <groupId>com.javaetmoi.util</groupId>
    <artifactId>javaetmoi-javabean-marshaller</artifactId>
    <version>1.0.3</version>
</dependency>
```

Appelons ensuite la méthode JavaBeanMarshaller.generateJavaCode(u2);

Une classe _ArtistFactory_ contenant le code suivant est généré :

```java
import com.javaetmoi.javabean.domain.Album;
import com.javaetmoi.javabean.domain.Artist;
import com.javaetmoi.javabean.domain.ArtistType;
import java.time.LocalDate;
import java.time.Month;
import java.util.ArrayList;
import java.util.List;

public class ArtistFactory {
  public static Artist newArtist() {
    Artist artist1 = new Artist();
    List<Album> albums1 = new ArrayList<>();
    Album album1 = new Album();
    album1.setArtist(artist1);
    album1.setReleaseDate(LocalDate.of(1987, Month.MARCH, 9));
    album1.setName("The Joshua Tree");
    albums1.add(album1);
    artist1.setAlbums(albums1);
    artist1.setName("U2");
    artist1.setId(1L);
    artist1.setType(ArtistType.GROUP);
    return artist1;
  }
}
```

Cette classe compile.  Plus verbeuse que le code original, elle a le mérite de structurer la création d’une instance et présente un code lisible par tout développeur Java.
En fonction de vos cas de test, libre à vous de modifier les valeurs, ajouter d’autres albums …

## Fonctionnalités

Dans sa version 1.0.0, le projet **_JavaBean marshaller_** supporte :

- JDK 7 et 8
- Collections
- Maps
- Tableaux à 1 et 2 dimensions
- Relations unidirectionnelles et bidirectionnelles
- Graphe cyclique
- Nombreux types du JDK :
  - Types primitifs : boolean, short, float …
  - Types wrappers : Boolean, String, BigDecimal
  - Enumérations
  - Date : _util.Date_, _java.sql.Date_, _Calendar_, _XMLGregorianCalendar_
  - Java 8 Date & Time API : _LocalDate_, _Period_, _Instant_ …
- Librairies tierces :
  - JodaTime : _DateTime_, _Period_, _Instant_ …

## Extensible

Ouvert aux extensions, le générateur **_JavaBean marshaller_** permet d’enrichir les types supportés :

- Autres classes du JDK
- Classes de frameworks tiers
- Classes d’une application métier

Le mécanisme d’extension repose sur l’interface [**CodeGenerator**](https://github.com/arey/javabean-marshaller/blob/master/src/main/java/com/javaetmoi/javabean/generator/CodeGenerator.java). Implémenter cette interface puis enregistrer l’instance auprès du [_JavaBeanMarshaller_](https://github.com/arey/javabean-marshaller/blob/master/src/main/java/com/javaetmoi/javabean/JavaBeanMarshaller.java) suffisent. La classe abstraite [_DefaultCodeGenerator_](https://github.com/arey/javabean-marshaller/blob/master/src/main/java/com/javaetmoi/javabean/generator/DefaultCodeGenerator.java) allège l’implémentation.

Repartons de l’exemple précédent. Essayons de modifier le code généré. Au lieu de faire appel au constructeur sans argument de la classe [_Album_](https://github.com/arey/javabean-marshaller/blob/master/src/test/java/com/javaetmoi/javabean/domain/Album.java), on souhaite utiliser le constructeur prenant en paramètres ses propriétés.
Pour cela, on crée une classe [_AlbumGenerator_](https://github.com/arey/javabean-marshaller/blob/master/src/test/java/com/javaetmoi/javabean/generator/AlbumGenerator.java) implémentant la [_DefaultCodeGenerator_](https://github.com/arey/javabean-marshaller/blob/master/src/main/java/com/javaetmoi/javabean/generator/DefaultCodeGenerator.java).

```java
public class AlbumGenerator extends DefaultCodeGenerator<Album> {

    @Override
    public void generateSetter(MethodSpec.Builder method, SetterParam param) {
        Album album = getValue(param);
        Item releaseDate = param.getMarshaller().buildItem(album.getReleaseDate());
        String artistVarName = param.getMarshaller().getVariableName(album.getArtist());
        method.addStatement("$L.add(new $T(\"$L\", "+releaseDate.getPattern()+", $L))", param.getVarName(), param.getValueClass(), album.getName(), releaseDate.getVal(), artistVarName);
    }
}
```

Comme vous pouvez le constater, l’implémentation de la méthode _generateSetter_ demande à manier l’API du générateur. Les tokens $T et $L et la classe _MethodSpec.Builder_ viennent du framework [Javapoet](https://github.com/square/javapoet) sur lequel le générateur s’appuie. Nous en reparlerons dans le chapitre suivant.
Les nombreuses [implémentations existantes](https://github.com/arey/javabean-marshaller/tree/master/src/main/java/com/javaetmoi/javabean/generator) peuvent servir de documentation.

En reprenant la même grappe et en utilisant l’ _AlbumGenerator_,

```default
Artist u2 = new Artist(1, "U2", ArtistType.GROUP);
Album joshuaTree = new Album("The Joshua Tree", LocalDate.of(1987, Month.MARCH, 9), u2);
u2.getAlbums().add(joshuaTree);
JavaBeanMarshaller.register(new AlbumGenerator());
JavaBeanMarshaller.generateJavaCode(u2);
```

La méthode _newArtist_ gagne en concision :

```default
public static Artist newArtist() {
  Artist artist1 = new Artist();
  List<Album> albums1 = new ArrayList<>();
  albums1.add(new Album("The Joshua Tree", LocalDate.of(1987, 3, 9), artist1));
  artist1.setAlbums(albums1);
  artist1.setName("U2");
  artist1.setId(1L);
  artist1.setType(ArtistType.GROUP);
  return artist1;
}
```

## Le fonctionnement

En interne, la classe _JavaBeanMarshaller_ effectue un parcours de graphe. Pour y arriver, elle s’appuie sur la classe _PropertyUtils_ de **Commons BeanUtils**. Les propriétés déjà traitées sont mémorisées dans un _Set_.

La génération de code Java s’appuie sur la librairie **Javapoet** créée par Square. Bien que le code généré soit simple et aurait pu être fait sans librairie tierce, Javapoet apporte :

1. La gestion de l’import des packages
1. L’ajout des ; à la fin de chaque instruction
1. Une syntaxe inspirée de String.format() permettant d’éviter la concaténation de chaînes de caractères (tokens $T, $L et $N)

Un outil de génération de jeux de données facilitant les tests avait le devoir d’être testé. C’est chose faite. Sa [couverture de test est accessible sur Coveralls.io](https://coveralls.io/github/arey/javabean-marshaller?branch=master).

Les tests unitaires reposent tous sur la même stratégie :

1. Création d’une grappe d’objets
1. Appel à la méthode _generateJavaCode_ chargée de générer la classe Java
1. Compilation de la classe (via la méthode _getSystemJavaCompiler_ du JDK)
1. Appel à la méthode statique permettant de recréer la grappe d’objets
1. Comparaison des 2 grappes d’objets (méthode _assertReflectionEqual_ de Unitils)

## Conclusion

Dans ce billet, vous avez fait la connaissance avec un tout jeune générateur de Dataset Java (sa 1ière release date du 19 mars 2016). Je compte sur vous pour me confirmer (ou non) son utilité. N’hésitez pas non plus à me soumettre les cas que je n’ai pas prévu. Et si vous souhaitez y contribuer, vous êtes les bienvenus.

Une prochaine étape consistera à rendre ce générateur moins intrusif. En effet, une fois le dataset généré, il faut bien penser à retirer du code de prod l’appel au _JavaBeanMarshaller_ ainsi que la dépendance maven. L’utilisation d’un agent et d’une annotation serait une solution. A suivre …
