---
_edit_last: "1"
_wp_old_slug: memoy-leak-client-cxf-attachment
author: admin
categories:
  - retour-d'expérience
date: "2014-02-22T09:28:31+00:00"
guid: http://javaetmoi.com/?p=977
parent_post_id: null
post_id: "977"
post_views_count: "7491"
summary: |-
  Les tests de charge d’une nouvelle fonctionnalité m’a récemment permis de détecter un comportement inattendu de **CXF** s’apparentant à une **fuite mémoire**. Fusion de Celtix et de XFire, le [framework CXF](http://cxf.apache.org/) propose une implémentation cliente et serveur de web services SOAP et REST. Le comportement suspect concerne la partie **cliente** d’un **web service SOAP** avec **pièce-jointes**.

  Les symptômes ont été observés dans les conditions suivantes. Un tir de charge avec JMeter simule l’upload de fichiers de 4 Mo. Trente utilisateurs connectés simultanément uploadent des fichiers PDF. D’une durée de 5mn, le scénario fonctionnel mettant en jeu l’upload de fichiers est réitéré pendant 3h. A l’issu du tir, aucune erreur technique ou fonctionnelle n’est remontée. Par contre, l’analyse de l’empreinte mémoire est suspecte : non seulement cette nouvelle fonctionnalité a nécessité davantage de mémoire que lors des tirs précédents, mais surtout : **la mémoire n’est jamais libérée**, même après l’expiration des sessions utilisateurs.

  [![2014-02-cxf-attachments-memory-leak-2](http://javaetmoi.com/wp-content/uploads/2014/02/2014-02-cxf-attachments-memory-leak-2.jpg)](http://javaetmoi.com/wp-content/uploads/2014/02/2014-02-cxf-attachments-memory-leak-2.jpg)
tags:
  - cxf
  - jmeter
  - soap
  - spring-framework
title: Memory Leak du client CXF
url: /2014/02/memory-leak-client-cxf-attachment/

---
Les tests de charge d’une nouvelle fonctionnalité m’a récemment permis de détecter un comportement inattendu de **CXF** s’apparentant à une **fuite mémoire**. Fusion de Celtix et de XFire, le [framework CXF](http://cxf.apache.org/) propose une implémentation cliente et serveur de web services SOAP et REST. Le comportement suspect concerne la partie **cliente** d’un **web service SOAP** avec **pièce-jointes**.

Les symptômes ont été observés dans les conditions suivantes. Un tir de charge avec JMeter simule l’upload de fichiers de 4 Mo. Trente utilisateurs connectés simultanément uploadent des fichiers PDF. D’une durée de 5mn, le scénario fonctionnel mettant en jeu l’upload de fichiers est réitéré pendant 3h. A l’issu du tir, aucune erreur technique ou fonctionnelle n’est remontée. Par contre, l’analyse de l’empreinte mémoire est suspecte : non seulement cette nouvelle fonctionnalité a nécessité davantage de mémoire que lors des tirs précédents, mais surtout : **la mémoire n’est jamais libérée**, même après l’expiration des sessions utilisateurs.

[![2014-02-cxf-attachments-memory-leak-2](/wp-content/uploads/2014/02/2014-02-cxf-attachments-memory-leak-2.jpg)](/wp-content/uploads/2014/02/2014-02-cxf-attachments-memory-leak-2.jpg)

## Origine du problème

Un Heap Dump de la JVM a permis de déterminer le type d’objets résidents en mémoire et également de quelles classes ces objets ont été alloués. Dans mon cas, près de 300 Mo de tableaux de bytes occupaient la Heap. La plupart de ces tableaux occupaient 5 Mo.
La pile d’appel ci-dessous montre que ces tableaux sont créés par le client CXF, et plus précisément par la classe [_AttachmentSerializer_](http://cxf.apache.org/javadoc/latest/org/apache/cxf/attachment/AttachmentSerializer.html) chargée de sérialiser en XML le [_SoapMessage_](https://cxf.apache.org/javadoc/latest/org/apache/cxf/binding/soap/SoapMessage.html) émis par le client CXF.

[![2014-02-cxf-attachments-memory-leak-5](/wp-content/uploads/2014/02/2014-02-cxf-attachments-memory-leak-5.jpg)](/wp-content/uploads/2014/02/2014-02-cxf-attachments-memory-leak-5.jpg) Reproductible sur un poste de développement, le debugger d’Eclipse permet de diagnostique que les 5 Mo de tableau de bytes correspondent au message SOAP et sa pièce-jointe encodée en base 64 :

[![2014-02-cxf-attachments-memory-leak-7](/wp-content/uploads/2014/02/2014-02-cxf-attachments-memory-leak-7.jpg)](/wp-content/uploads/2014/02/2014-02-cxf-attachments-memory-leak-7.jpg) En interne, la classe [_ClientImpl_](http://grepcode.com/file/repo1.maven.org/maven2/org.apache.cxf/cxf-rt-core/2.4.0/org/apache/cxf/endpoint/ClientImpl.java) de CXF maintient une _Map_ _requestcontext_  associant un thread à un message SOAP.  Les derniers messages émis par le client CXF sont stockés dans cette _Map_. Au final, **plus le nombre de threads faisant appel au client CXF est élevé, plus CXF demandera de mémoire**.

## Correction

La correction mise en œuvre a été d’implémenter un **intercepteur CXF** chargé de déréférencer l’instance de [_AttachmentSerializer_](http://cxf.apache.org/javadoc/latest/org/apache/cxf/attachment/AttachmentSerializer.html) une fois le message SOAP envoyé. Le Garbage Collector peut alors libérer la mémoire. L’intercepteur est positionné sur la toute dernière [phase CXF](https://cxf.apache.org/docs/interceptors.html) : SETUP\_ENDING.

```java
Extrait de la classe ClearAttachmentsOutInterceptor.java
```

Lors de la déclaration Spring d’un client CXF, l’intercepteur _[ClearAttachmentsOutInterceptor](https://gist.github.com/arey/9119018)_ doit être positionné dans la balise <jaxws:outInterceptors>  :

```xhtml
<jaxws:client id="myWebServiceClient" serviceClass="MyWebService"
    address="http://localhost:8080/ws/MyWebService">
  <jaxws:outInterceptors>
    <bean class="ClearAttachmentsOutInterceptor"/>
  </jaxws:outInterceptors>
</jaxws:client>
```

## Conclusion

Surpris de découvrir une telle problématique de mémoire dans un framework aussi populaire,  je ne comprends pas le choix pris par les développeurs de CXF de conserver trace d’un message une fois celui-ci émis et sa réponse reçue. Une hypothèse : éviter de réallouer une grappe d’objets à chaque appel de web service ?
Chose rassurante, je ne suis pas le seul à avoir rencontré ces soucis de mémoire lors de tirs de charge. Ce problème est en effet décrit sur les Jira des ESB Apache Service Mix ([SMXCOMP-855](https://issues.apache.org/jira/browse/SMXCOMP-855)) et Mule ESB ([MULE-6434](https://www.mulesoft.org/jira/browse/MULE-6434)). Chacun d’eux a apporté sa propre solution de contournement.
