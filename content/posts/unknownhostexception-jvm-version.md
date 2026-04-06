---
_edit_last: "1"
author: admin
categories:
  - retour-d'expérience
date: "2013-01-27T18:29:58+00:00"
guid: http://javaetmoi.com/?p=587
parent_post_id: null
post_id: "587"
post_views_count: "13872"
summary: Après un précédent billet relatant un bug lié à la version du driver Oracle utilisé, voici un nouveau  billet portant sur **bug** lié, cette fois ci, à la **version de la JVM utilisée**. Ce bug nous a été révélé très tardivement dans le cycle de développement de l’application Java incriminée. En effet, PV de recette en poche, les tests de charge menés avec JMeter sur l’environnement de pré-production ne nous avaient rien révélé. Seuls les tests de robustesse nous ont  alertés d’une mystérieuse **_java.net.UnknownHostException_** survenant 4 à 5 minutes après l’arrêt volontaire d’une application tierce.
tags:
  - bug
  - jvm
title: Une bien mystérieuse UnknownHostException
url: /2013/01/unknownhostexception-jvm-version/

---
Après un précédent billet relatant un bug lié à la version du driver Oracle utilisé, voici un nouveau  billet portant sur **bug** lié, cette fois ci, à la **version de la JVM utilisée**. Ce bug nous a été révélé très tardivement dans le cycle de développement de l’application Java incriminée. En effet, PV de recette en poche, les tests de charge menés avec JMeter sur l’environnement de pré-production ne nous avaient rien révélé. Seuls les tests de robustesse nous ont  alertés d’une mystérieuse **_java.net.UnknownHostException_** survenant 4 à 5 minutes après l’arrêt volontaire d’une application tierce.

## **Les symptômes**

Techniquement, l’application testée consomme différents web services SOAP. Le framework Apache CXF est utilisé comme client SOAP. Développée en **Java 6**, l’application est déployée sur un serveur d’application JBoss.
Lors de l’arrêt de l’application tierce exposant les web services, le client n’arrive plus à s’y connecter. Comme attendu, une _java.net. SocketException_ est levée. Jusque-là, tout est normal.
Par contre, après plusieurs minutes d’arrêt, le _SocketException_ se transforme en _UnknownHostException_. Et c’est là que commence nos interrogations. En effet, une _UnknownHostException_ est levée en principe lorsque l’adresse IP d’un hôte n’a pas pu être résolue. Or, jusqu’à cette erreur, l’adresse IP avait pu être résolue.
Voici la pile d’appel observée :

```java
Caused by: java.net.UnknownHostException: www.monappli.fr
at java.net.PlainSocketImpl.connect(PlainSocketImpl.java:177)
at java.net.SocksSocketImpl.connect(SocksSocketImpl.java:366)
at java.net.Socket.connect(Socket.java:525)
at sun.net.NetworkClient.doConnect(NetworkClient.java:158)
at sun.net.www.http.HttpClient.openServer(HttpClient.java:394)
at sun.net.www.http.HttpClient.openServer(HttpClient.java:529)
at sun.net.www.http.HttpClient.<init>(HttpClient.java:233)
at sun.net.www.http.HttpClient.New(HttpClient.java:306)
at sun.net.www.http.HttpClient.New(HttpClient.java:323)
at sun.net.www.protocol.http.HttpURLConnection.getNewHttpClient(HttpURLConnection.java:860)
at sun.net.www.protocol.http.HttpURLConnection.plainConnect(HttpURLConnection.java:801)
at sun.net.www.protocol.http.HttpURLConnection.connect(HttpURLConnection.java:726)
at sun.net.www.protocol.http.HttpURLConnection.getOutputStream(HttpURLConnection.java:904)
at org.apache.cxf.transport.http.HTTPConduit$WrappedOutputStream.handleHeadersTrustCaching(HTTPConduit.java:1375)
at org.apache.cxf.transport.http.HTTPConduit$WrappedOutputStream.onFirstWrite(HTTPConduit.java:1317)at org.apache.cxf.io.AbstractWrappedOutputStream.write(AbstractWrappedOutputStream.java:42)at org.apache.cxf.io.AbstractThresholdOutputStream.write(AbstractThresholdOutputStream.java:69)at org.apache.cxf.transport.http.HTTPConduit$WrappedOutputStream.close(HTTPConduit.java:1395)
... 34 more
```

D'après le code source, l’exception est levée par la classe _PlainSocketImpl_  lors d’un appel natif.

Bien qu’incompris, ce problème aurait pu être acceptable s’il s’était limité à un fonctionnement en mode dégradé. Malheureusement, plusieurs semaines après une mise en production en avance de phase, ce problème est réapparu de manière intempestive et, plus grave encore, sans aucune interruption de service de l’application tierce.

## **L’investigation**

Plusieurs pistes ont alors été envisagées : coupures réseaux, [utilisation d’IP V6](http://www.unitask.com/oracledaily/2012/10/04/missing-ipv6-address-for-local-network-interfaces-causes-service-timeout/), problème d’accès aux DNS, excès de zèle du firewall, problème de cache DNS côté serveur comme côté JVM, bug applicatif …
D’éventuels problèmes de DNS ou de firewall ont rapidement été écartés par l’ingénierie système.

Ecartant le problème d’un bug applicatif, la mise au point du programme java ci-dessous nous a permis de reproduire systématiquement le _UnknownHostException_. Basique, ce programme lit en boucle la 1ière ligne d’un des WSDL exposés par l’application tierce. Deux minutes à peine après son exécution, des _UnknownHostException_ fleurissaient.

```java
import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.net.URL;
import java.net.URLConnection;
import java.net.UnknownHostException;

public class TestUrlConnection {

    public static void main(String... args) throws Exception {

        final URL url = new URL("http://www.monappli.fr/ws/MonWebService/v1_0?wsdl");

        for (long i = 0; i < 10000000000L; i++) {
            try {
                URLConnection conn = url.openConnection();
                BufferedReader in = new BufferedReader(new InputStreamReader(conn.getInputStream()));
                in.readLine();
                in.close();
            } catch (UnknownHostException e) {
                e.printStackTrace();
            }
        }
    }
}
```

L’ajout des adresses IP dans le fichier /etc/hosts du serveur Linux fut le premier contournement trouvé.

## **Solution**

Le contournement définitif consista à utiliser une **JVM Sun / Oracle 1.6.0\_25** à la place de la version **1.6.0\_16** initialement installée. Aucun risque de régression fonctionnelle n’était à craindre puisque la version 1.6.0\_25 équipait déjà les environnements d’intégration de recette. De nouveaux tests de charge ont validé techniquement cette montée de version.

Malheureusement, les [release notes de la JVM](http://www.oracle.com/technetwork/java/javase/releasenotes-136954.html) ne nous ont pas permis de trouver le problème corrigé entre ces 2 versions de JVM. Notre hypothèse est que, datant d’août 2009, la version 1.6.0\_16 du JRE ne supportait pas encore la Red Hat 6 de novembre 2011 sur laquelle s’exécute notre application.
Quant au fait que l’exception soit apparue plus systématiquement lors de tests de robustesse, une explication plausible est que, lorsque le web service est indisponible, sa fréquence d’appel est plus grande, ce qui accroit la sollicitation aux appels système de résolution de nom de domaine.
