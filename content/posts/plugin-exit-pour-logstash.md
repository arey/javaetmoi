---
_edit_last: "1"
author: admin
categories:
  - retour-d'expérience
date: "2014-11-09T11:15:07+00:00"
thumbnail: /wp-content/uploads/2014/11/logstash.png
featureImage: /wp-content/uploads/2014/11/logstash.png
featureImageAlt: "logstash"
guid: http://javaetmoi.com/?p=1254
parent_post_id: null
post_id: "1254"
post_views_count: "6594"
summary: |-
  [![logstash](http://javaetmoi.com/wp-content/uploads/2014/11/logstash-187x300.png)](http://javaetmoi.com/wp-content/uploads/2014/11/logstash.png) Ce billet a pour objectif de vous présenter un cas d’usage du **plugin exit** pour LogStash.
  Une utilisation répandue de LogStash consiste à alimenter Elasticsearch à partir de fichiers de logs.
  Extensible via un mécanisme de plugins, LogStash sait gérer plusieurs types de source et plusieurs types de destinations.
  **Une utilisation alternative de LogStash consiste à l’utiliser comme batch d’indexation**. Le fichier à indexer a une fin. Et **l’utilisateur souhaite que LogStash s’arrête une fois les données importées**.
tags:
  - elasticsearch
  - jruby
  - logstash
  - plugin
title: Plugin exit pour LogStash
url: /2014/11/plugin-exit-pour-logstash/

---
[![logstash](/wp-content/uploads/2014/11/logstash.png)](/wp-content/uploads/2014/11/logstash.png) Ce billet a pour objectif de vous présenter un cas d’usage du **plugin exit** pour LogStash.
Une utilisation répandue de LogStash consiste à alimenter Elasticsearch à partir de fichiers de logs.
Extensible via un mécanisme de plugins, LogStash sait gérer plusieurs types de source et plusieurs types de destinations.
**Une utilisation alternative de LogStash consiste à l’utiliser comme batch d’indexation**. Le fichier à indexer a une fin. Et **l’utilisateur souhaite que LogStash s’arrête une fois les données importées**.

## Solution possible

A l’instar de la commande _tail_, LogStash est conçu pour attendre la suite d’un fichier. **Il n’a pas connaissance de la fin de fichier**. Une première étape consiste donc à informer LogStash que la dernière ligne du fichier a été atteinte et qu’il peut s’arrêter.
Une solution possible est donnée comme réponse à la [la question « How to automatically kill a logstash agent when tests are done » posée sur Stackoverfow](http://stackoverflow.com/questions/18299337/how-to-automatically-kill-a-logstash-agent-when-tests-are-done).
Elle consiste **à ajouter un tag _endfile_** lorsqu’un pattern est détecté dans le message (la ligne) qui vient d’être lue, ici la chaîne _END FILE_ :

```js
filter {
  if [message] =~ "^END FILE" {
    mutate {
      add_tag => ["endfile"]
    }
  }
}
```

L’ajout du tag est réalisé dans la section _filter_.
Cette solution nécessite d’avoir la main sur le fichier : soit en le générant, soit en ayant la possibilité de lui concaténer une ligne END FILE.

Dans la section _output_, avant d’écrire le message, on vérifie si le tag _endfile_ existe. Si c’est le cas, on quitte l’agent LogStash en faisant appel au plugin exit :

```js
output {
  if "endfile" in [tags] {
      exit  { }
  }
  stdout { }
}
```

## Le plugin exit

Le plugin exit pour LogStash est écrit en **JRuby**. Il a été testé sous **LogStash 1.4.2**. Son code source est disponible dans le repo [https://github.com/arey/logstash-exit-plugin](https://github.com/arey/logstash-exit-plugin)

Les commandes suivantes permettent de le récupérer et de le tester :

1. git clone git://github.com/arey/logstash-exit-plugin.git
1. cd logstash-exit-plugin
1. set LOGSTASH\_HOME=<your logstash installation directory>
1. %LOGSTASH\_HOME%\\bin\\logstash agent --pluginpath .\\plugins -f exit-example.conf

Un effet de bord lié à l'implémentation de ce plugin est que la JVM s’arrête brutalement. Et ceci, alors que les plugins chargés d’écrire les messages ont peut-être encore des données à flusher. Le plugin permet de contourner ce problème en prévoyant une pause avant l’arrêt subite de la JVM (paramètre _pause\_second_). Sans le garantir à 100%, une pause de 10 secondes devrait donner suffisamment de temps aux writers pour terminer leur job.

Un autre usage de ce plugin consiste à sortir de LogStash dès qu’une erreur est rencontrée. Le paramètre _exit\_code_ permet de spécifier le code d’erreur retournée par la JVM à l’appelant.

Pour les plus curieux, le code du plugin est des plus trivial :

```ruby
Extrait de la classe ruby Exit
```

## Conclusion

Par faute d’avoir trouvé mieux, le plugin exit sort brutalement de la JVM (équivalent à un _System.exit()_). Une solution plus élégante serait de demander à LogStash de s’arrêter et de pouvoir propager l’évènement _LogStash::ShutdownSignal_. Je fais appel à la communauté LogStash pour m’indiquer comment procéder.

Enfin, rattaché à la section _output_, un plugin similaire pourrait également être codé au niveau de la section _filter_. A vous de jouer !
