---
_edit_last: "1"
_encloseme: "1"
author: admin
categories:
  - conférence
date: "2025-10-30T16:45:25+00:00"
guid: https://javaetmoi.com/?p=2612
parent_post_id: null
post_id: "2612"
summary: |-
  Lors de la conférence [Devfest Nantes 2025](https://devfest2025.gdgnantes.com/), j'ai assisté au talk d' **[Hoani Cross](https://linktr.ee/hoani.cross)** portant sur la **prise de notes**. Loin d'être nouveau, ce sujet m'a particulièrement interpellé. Figurez-vous en effet qu'une partie des **articles publiés sur ce blog** (dont celui que vous avez sous les yeux) vient des notes rédigées lors de conférences, de projets personnels ou bien encore de ma veille techno.

  Dans son talk, Hoani nous présente le logiciel **[Obsidian](https://obsidian.md/)**, la manière dont **il l'utilise au quotidien** pour **noter** et **gérer son activité**, qu'elle soit professionnelle ou personnelle.{{ double-space-with-newline }}Je suis sorti de sa présentation quelque peu désarçonné. Hoani utilise Obsidian comme un **Bullet Journal** (qu'on appelle aussi « **bujo** ») numérique pour compiler **notes**, **pense-bêtes**, **objectifs**, **rappels**, **tracking**, **plannings** et **coups de coeur**. Son utilisation est vraiment avancée et très régulière. Je ne me voyais pas passer autant de temps que lui sur Obsidian.

  L'autre domaine dans lequel Obsidian semble exceller consiste en la possibilité de se créer un **Second Cerveau**. Les notes peuvent être reliées ensemble à l'aide de **Map Of Content** (MOC). Une alternative aux **hashtags** et l'organisation hiérarchisée en **dossiers** et sous-dossiers.{{ double-space-with-newline }}Une note de type Map of Content s'assimile à une thématique, un sujet principal, auquel on rattache bidirectionnellement des notes et qui va faire office de table de matières et de tableau de bord. La création de sous-MOCs spécialisés reste possible. On se rapproche du web, des liens hypertextes et du **mind mapping**.{{ double-space-with-newline }}Dans ce billet, j'aimerais vous restituer la prestation d'Hoani et vous laisser découvrir son utilisation Obsidian.
tags:
  - devfest
  - obsidian
title: 'Révolutionnez votre prise de notes : du Bullet Journal à Obsidian'
url: /2025/10/revolutionnez-votre-prise-de-notes-du-bullet-journal-a-obsidian/

---
Lors de la conférence [Devfest Nantes 2025](https://devfest2025.gdgnantes.com/), j'ai assisté au talk d' **[Hoani Cross](https://linktr.ee/hoani.cross)** portant sur la **prise de notes**. Loin d'être nouveau, ce sujet m'a particulièrement interpellé. Figurez-vous en effet qu'une partie des **articles publiés sur ce blog** (dont celui que vous avez sous les yeux) vient des notes rédigées lors de conférences, de projets personnels ou bien encore de ma veille techno.

Dans son talk, Hoani nous présente le logiciel **[Obsidian](https://obsidian.md/)**, la manière dont **il l'utilise au quotidien** pour **noter** et **gérer son activité**, qu'elle soit professionnelle ou personnelle.  
Je suis sorti de sa présentation quelque peu désarçonné. Hoani utilise Obsidian comme un **Bullet Journal** (qu'on appelle aussi « **bujo** ») numérique pour compiler **notes**, **pense-bêtes**, **objectifs**, **rappels**, **tracking**, **plannings** et **coups de coeur**. Son utilisation est vraiment avancée et très régulière. Je ne me voyais pas passer autant de temps que lui sur Obsidian.

L'autre domaine dans lequel Obsidian semble exceller consiste en la possibilité de se créer un **Second Cerveau**. Les notes peuvent être reliées ensemble à l'aide de **Map Of Content** (MOC). Une alternative aux **hashtags** et l'organisation hiérarchisée en **dossiers** et sous-dossiers.  
Une note de type Map of Content s'assimile à une thématique, un sujet principal, auquel on rattache bidirectionnellement des notes et qui va faire office de table de matières et de tableau de bord. La création de sous-MOCs spécialisés reste possible. On se rapproche du web, des liens hypertextes et du **mind mapping**.  
Dans ce billet, j'aimerais vous restituer la prestation d'Hoani et vous laisser découvrir son utilisation Obsidian.

{{< figure src="/wp-content/uploads/2025/10/DevFest-Nantes-2025-Obsidian.jpg" alt="" caption="" >}}

# Du papier à Obsidian

Senior backend architect chez Sfeir, Hoani Cross nous explique avoir utilisé de nombreux carnets manuscrits pour apprendre et structurer sa pensée. Hoani pratique le Bullet Journal et son talk se veut être un partage de ses résultats après des années de pratiques.  
Hoani commence par nous rappeler les **bienfaits** de prendre des notes :

- **Ralentir** pour assimiler, poser son téléphone pour se focaliser
- **Graver** dans la mémoire
- Transformer l’écoute en **savoir**, **résumer** avec ses propres mots
- **Entraîner** **le cerveau** : sport mental, reformulation, concentration
- **Connecter** **des idées** parfois éloignées les unes des autres
- **Améliorer sa compréhension** tout en construisant une bibliothèque personnelle (le fameux Second Cerveau)

Adepte du **Bullet Journal** (Bujo), Hoani a longtemps utilisé un carnet numéroté, un stylo et un index en début de carnet. Son carnet comportait une page par jour contenant des idées, des notes, le suivi des variables (énergie / humeur) et des sujets spéciaux. Pour s'y retrouver, il utilise des conventions de notation appelées [Bullet Journal Key](https://macoherence.com/les-clefs-du-bullet-journal/). Par exemple : un carré pour une tâche.  
Première limitation : les Bujo ne permettent pas de faire de recherche textuelle.

Hoani a essayé de basculer sur des carnets numériques avec le [reMarkable](https://remarkable.com/) et a testé différents logiciels : OneNote, EverNote, Notion, Keep, Joplin. Nul n'est arrivé à la hauteur d'Obsidian qui est presque parfait pour les raisons suivantes :

- Basé sur le langage de balisage léger **Markdown**, ce qui permet à l'auteur de rester propriétaire de ses données
- Rendu basé le **moteur web Electron** (comme VS Code)
- Logiciel **gratuit**, créé pendant le confinement de la Covid19, mais pas Open Source
- Plus de **2 500 plugins** OpenSource
- **Multiplateforme** : Windows, Linux, MacOS, Android, iOS

Obsidian intègre les **fonctionnalités** suivantes  :

- **Coffre avec navigateur de fichiers** : toutes les notes sont stockées localement dans un dossier (appelé "coffre"), consultable via un explorateur intégré.
- **Éditeur de Markdown intelligent** : éditeur fluide combinant texte brut et mise en forme instantanée, avec gestion des liens internes, blocs de code, formules et tableaux.
- **Canvas pour composer ses notes** : espace visuel libre pour organiser ses idées sous forme de cartes reliées, idéal pour le brainstorming et la modélisation de concepts.
- **Gestion des _daily notes_** : fonction de journal quotidien permettant de consigner rapidement pensées, tâches ou réflexions, avec génération automatique de notes datées.
- **Diapositives** : transformation instantanée d’une note en présentation interactive, pratique pour exposer un projet ou partager ses idées sans quitter Obsidian.
- **Enregistrement audio** : capture vocale intégrée pour enregistrer des idées, réunions ou commentaires, directement stockés et liés dans le coffre.
- **Vue graphique de l’arborescence des notes** : représentation visuelle du réseau de liens entre notes, offrant une cartographie claire et dynamique de son écosystème de connaissances.

L'une des forces du logiciel Obsidian réside dans le fait qu'il soit multiplafeforme : on peut commencer une note oralement sur son Smartphone puis la reprendre plus tard avec un clavier sur son laptop. Plusieurs [techniques de synchronisation des coffres](https://help.obsidian.md/sync-notes) entre différents devices existent :

1. Offre de service intégré payant : **Sync** (4$ par mois)
1. Stockage Cloud avec **iCloud**, **OneDrive**, **Google Drive**
1. **[Syncthing](https://syncthing.net/)** (OSS) : synchronisation Peer-to-Peer de fichiers. Vos données ne sont jamais stockées dans le Cloud
1. Plugin **Git** (instable sur mobile) : personnellement, c'est ce dernier que j'utilise avec un repo GitHub privé.

À noter que l'utilisation d'un repo Git rend possible le partage en équipe d'un coffre Obsidian.

# Utilisation d'Obsidian

Le coffre d'Hoani contient toutes ses données, tant personnelles que professionnelles. Cela peut poser un problème de confidentialité : faire sortir des données pros sur son ordi perso peut être contraire aux règles de sécurité de son entreprise.

L'organisation de son coffre comporte 8 grands dossiers :

- Notes persos
- Notes pros
- Notes de lecture (livres ou vidéo youtube)
- Notes non classées (temporaire)
- Second Brain : wiki perso
- Bullet Journal (Bujo)
- Archives
- Templates

Chaque note .md suit la structuration suivante :

- En-tête en **[front matter](https://docs.github.com/en/contributing/writing-for-github-docs/using-yaml-frontmatter)** pour ajouter des méta-données
- Corps en Markdown
- Tags hiérarchisés

Le tableau suivant présente la [syntaxe Markdown supportée par Obsidian](https://help.obsidian.md/obsidian-flavored-markdown) :

SyntaxDescription`[[Link]]`[Internal links](https://help.obsidian.md/links)`![[Link]]`[Embed files](https://help.obsidian.md/embeds)`![[Link#^id]]`[Block references](https://help.obsidian.md/links#Link%20to%20a%20block%20in%20a%20note)`^id`[Defining a block](https://help.obsidian.md/links#Link%20to%20a%20block%20in%20a%20note)`[^id]`[Footnotes](https://help.obsidian.md/syntax#Footnotes)`%%Text%%`[Comments](https://help.obsidian.md/syntax#Comments)`~~Text~~`[Strikethroughs](https://help.obsidian.md/syntax#Bold,%20italics,%20highlights)`==Text==`[Highlights](https://help.obsidian.md/syntax#Bold,%20italics,%20highlights)```` ``` ````[Code blocks](https://help.obsidian.md/syntax#Code%20blocks)`- [ ]`[Incomplete task](https://help.obsidian.md/syntax#Task%20lists)`- [x]`[Completed task](https://help.obsidian.md/syntax#Task%20lists)`> [!note]`[Callouts](https://help.obsidian.md/callouts)(see link)[Tables](https://help.obsidian.md/advanced-syntax#Tables)

Dans son dossier **Bujo**, Hoani s'appuie sur le plugin [Periodic Notes](https://github.com/liamcain/obsidian-periodic-notes) pour gérer ses notes périodiques et les hiérarchise en année / trimestre / mois / jours.

Le plugin [Tasks](https://github.com/obsidian-tasks-group/obsidian-tasks) permet de gérer les **tâches** dans Obsidian. La syntaxe Markdown \[x\] et \[\] permet de reconnaitre une tâche terminée d'une tâche à faire. L'utilisation d'Emojis est possible pour les méta-données.  
A noter la possibilité de créer des **tableaux dynamiques** à l’aide de requête, par exemple pour créer une **liste de TODO** à faire aujourd’hui.

Son **daily** est centré autour d’une simple bullet list renseignée tout au long de la journée.  
Chaque sujet commence par un tag (ex : #perso, #tech). Hoani utilise les sous-listes pour détailler le sujet.  
Chaque jour, Hoani ouvre son Daily du jour et

- Regarde les tâches à réaliser
- Note en bullet list
- Crée une tâche quand nécessaire
- Termine les tâches accomplies

# Le bénéfice du numérique

Comparé au manuscrit, les bénéfices du numérique sont nombreux :

- Personnaliser son daily en ajoutant toutes les infos qui lui passent par la tête
- Suivre des variables quotidiennes (comme le temps passé à s'entrainer au [Kendama](https://fr.wikipedia.org/wiki/Kendama))
- Afficher les tâches à réaliser et être notifié de celles en retard
- Automatiser certains traitements à l'aide de plugins additionnels : [Templater](https://github.com/SilentVoid13/Templater), [Tasks](https://github.com/obsidian-tasks-group/obsidian-tasks) et [Dataview](https://github.com/blacksmithgu/obsidian-dataview)

Le contenu du Daily peut être très riche et comporter :

- **Métadonnées** avec tags
- Cartouche de **navigation**
- **Widgets de progression** mois/année
- Définition de la **tâche ultime** de la journée
- Rappel des **tâches** via un filtre de recherche et un report facilité des tâches
- Le **journal** en lui-même  
- Entrainement au Kendama
- Des métriques sur livres (page en cours) et jeux vidéo (temps, winrate)

Exemples de métadonnées d'un Daily permettant de suivre des variables quotidiennes :

```text
energy_level_morning : 6
energy_level_evening : 7
mood_morning : insomniaque
mood_evening : détendu
walked : 400
working_place_morning : HOME
```

La **barre de navigation** du Daily permet de passer rapidement du daily précédent au suivant, à la semaine associée …  
L'ajout de **barres de progression** est possible via le plugin [Progressbar](https://github.com/zwpaper/obsidian-progressbar).

Le numérique permet de créer d' **autres types de notes périodiques** que le daily. On peut, par exemple, se fixer des objectifs annuels (ex: courir un marathon), suivre visuellement leurs avancements puis, une fois la période écoulée, faire un bilan de la période et définir de nouveaux objectifs. Hoani insiste sur le fait que l'ouverture et la fermeture d'une période doit être vécue comme un rituel.  
Pour automatiser la création de ces différentes notes périodiques, on peut s'aider du plugin [Templater](https://silentvoid13.github.io/Templater/) qui ajoute à Obsidian un langage de **templating** permettant d'exécuter des **fonctions** **JavaScript**. Ce plugin permet de pré-sélectionner un template en fonction du nom du fichier créé.

# Conclusion

Après la démonstration de son **utilisation avancée d'Obsidian**, Hoani reconnaît que le **démarrage peut être long**, qu'il peut être **difficile** de décider quoi noter et surtout **comment organiser son coffre**. Son conseil est de rester rigoureux, y noter ce que l'on souhaite et faire en sorte que cela reste amusant et donc pas une corvée. Ses slides sont en ligne : [\[Devfest Nantes 25\] Révolutionnez votre prise de notes - du Bullet Journal à Obsidian](https://docs.google.com/presentation/d/1PGu22MX_v3q34QKaUvci7ug9hPScYXPSIjAyAhgfToY/edit). Son [repo GitHub](https://github.com/hcross/obsidian) rend public ses templates Obsidian.

Pour ma part, j’ **expérimente Obsidian** depuis seulement **deux semaines**, dans un cadre purement personnel — ce billet a d’ailleurs été rédigé avec l’application. J’ai choisi de débuter sans installer le moindre plugin, histoire de me faire une idée précise de ce que le logiciel propose “out of the box”.  
Pour l’instant, l’expérience est très agréable : l’ergonomie est soignée, la prise en main rapide et la rédaction des notes en Markdown particulièrement efficace.  
Au travail, pour ma prise de notes, je reste néanmoins sur **OneNote**, qui s’intègre parfaitement à l’écosystème Microsoft 365 et tire parti de **Copilot** pour la recherche et la synthèse de contenus.

{{< figure src="/wp-content/uploads/2025/10/Obsidian-screenshot-1.0-hero-combo.png" alt="" caption="" >}}
