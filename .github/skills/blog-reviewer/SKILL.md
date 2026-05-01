---
name: blog-reviewer
description: >-
  Révision complète d'un article de blog pour javaetmoi.com (Java & Moi).
  Utilise ce skill quand l'utilisateur veut relire, corriger, améliorer,
  finaliser ou préparer un article Hugo Clarity : correction orthographique et
  grammaticale en français, génération du frontmatter YAML selon les conventions
  du blog, limitation des lignes à 160 caractères pour la lisibilité IDE,
  application des bonnes pratiques Hugo (summary, images, TOC, code blocks),
  et revue d'exactitude technique pour tout billet technique (langages,
  frameworks, protocoles, sécurité, cloud, data, architecture, systèmes,
  standards, API), avec cross-check sur sources officielles, specs, docs
  éditeur, article de speaker et recherche web ciblée. Déclencher dès que
  l'utilisateur mentionne : relire un article, corriger l'orthographe,
  préparer le frontmatter, améliorer la lisibilité, publier un billet,
  revoir un index.md, challenger techniquement un billet, vérifier des
  références, fact-checker un article technique, valider qu'un contenu est
  vrai.
---

# Blog Reviewer — Java & Moi

Skill de relecture éditoriale complète pour les articles du blog javaetmoi.com.
Il couvre cinq domaines : correction de la langue, frontmatter Hugo, mise en
forme des lignes, bonnes pratiques Hugo Clarity, et vérification technique des
articles techniques.

## Étape 1 — Lire l'article

Lire le fichier `index.md` (ou `.md` plat) en entier. Repérer :

- Un frontmatter absent, incomplet ou mal formaté
- Des lignes dépassant 160 caractères (hors blocs de code)
- Des fautes d'orthographe ou de grammaire
- Des images sans texte alternatif
- L'absence du marqueur `<!--more-->`
- Des chemins d'images relatifs dans le champ `summary:` (ils doivent être absolus)
- Des affirmations techniques fortes ou potentiellement datées

## Étape 2 — Vérification technique et fact-check

Quand l'article traite d'un sujet technique, appliquer une relecture de fond et
pas seulement de forme.

- Vérifier les affirmations structurantes avec des **sources normatives ou
  officielles** : spécification, standard, RFC, JEP/PEP/KEP, documentation
  éditeur, release notes, API docs, notes de conception, source code, ou source
  du speaker si elle est fournie
- Commencer par une **recherche web ciblée** si les références ne sont pas déjà
  dans l'article, puis compléter avec les connaissances du modèle ; ne pas
  s'appuyer sur une simple intuition quand une source officielle est accessible
- Challenger les simplifications pédagogiques qui deviennent fausses si elles
  sont prises littéralement : performance, mémoire, compatibilité,
  concurrence, sécurité, réseau, coût, garanties runtime, sémantique langage,
  comportement d'un framework ou d'une plateforme
- Vérifier les généralisations : ne pas extrapoler une capacité, une migration,
  une optimisation ou une garantie à "tout" un produit, un package,
  un framework ou un code legacy sans source
- Si une affirmation dépend d'un contexte précis (version, plateforme,
  fournisseur cloud, runtime, compilateur, flag, niveau d'offre), exiger que ce
  contexte soit mentionné
- Préférer une formulation prudente pour le futur : `pourrait`, `à ce stade`,
  `la spécification indique`, `la documentation annonce`, `la syntaxe
  pressentie`, plutôt qu'une formulation catégorique

### Sortie attendue pour une revue technique

Si l'utilisateur demande de **challenger** ou **vérifier** un article sans
demander immédiatement une réécriture complète, produire d'abord une revue
priorisée.

- Lister et numéroter les remarques **par priorité décroissante**
- Associer à chaque remarque une **catégorie** (ex. `Exactitude spécification`,
  `API/framework`, `Runtime/performance`, `Compatibilité/migration`,
  `Sécurité`, `Formulation à nuancer`)
- Donner la **ligne ou section concernée**
- Expliquer **pourquoi** c'est faux, incomplet, trompeur ou acceptable avec
  nuance
- Proposer la **correction minimale** ou la reformulation recommandée
- Terminer par les **questions ouvertes** à poser à l'auteur si un point dépend
  de la conférence, d'une citation orale, d'un benchmark ou d'un choix
  éditorial

## Étape 3 — Correction orthographique et grammaticale

Le blog est rédigé en **français**. Appliquer les règles suivantes :

**Accents et caractères**

- Vérifier les accents : `é`, `è`, `ê`, `à`, `â`, `ç`, `ù`, `û`, `î`, `ô`,
  `ï`, `ë`, `ü`
- Ne jamais supprimer les majuscules accentuées : `É`, `À`, `Ç`

**Accords**

- Accord des adjectifs et participes passés avec le sujet ou le COD
- Pluriel des noms composés et des sigles

**Ponctuation française**

- Virgule d'apposition sans espace avant

**Caractères typographiques LLM (sanitisation)**

Les LLM génèrent fréquemment des caractères Unicode typographiques qui passent
inaperçus visuellement mais cassent des parsers et des comparaisons de chaînes.
Remplacer **systématiquement** chaque occurrence (hors blocs de code et URLs) :

| Caractère   | Unicode          | Nom                                   | Remplacement ASCII |
|-------------|------------------|---------------------------------------|--------------------|
| `…`         | U+2026           | Points de suspension                  | `...`              |
| `–`         | U+2013           | Tiret demi-cadratin (en dash)         | `-`                |
| `—`         | U+2014           | Tiret cadratin (em dash)              | `--` ou `-`        |
| `‒`         | U+2012           | Tiret figuratif                       | `-`                |
| `'`         | U+2018           | Guillemet simple ouvrant              | `'`                |
| `'`         | U+2019           | Guillemet simple fermant / apostrophe | `'`                |
| `"`         | U+201C           | Guillemet double ouvrant              | `"`                |
| `"`         | U+201D           | Guillemet double fermant              | `"`                |
| `„`         | U+201E           | Guillemet double bas                  | `"`                |
| `«`         | U+00AB           | Guillemet français ouvrant            | `<<`               |
| `»`         | U+00BB           | Guillemet français fermant            | `>>`               |
| ` ` (NBSP)  | U+00A0           | Espace insécable                      | espace normal      |
| ` ` (thin)  | U+2009           | Espace fine                           | espace normal      |
| ` ` (NNBS)  | U+202F           | Espace fine insécable                 | espace normal      |
| `×`         | U+00D7           | Signe multiplication                  | `x`                |
| `✓` / `✗`  | U+2713 / U+2717  | Coche / Croix                         | `ok` / `x`         |
| `•`         | U+2022           | Puce (bullet)                         | `-` ou `*`         |
| `′`         | U+2032           | Prime (minutes/pieds)                 | `'`                |
| `″`         | U+2033           | Double prime (secondes/pouces)        | `"`                |

Les plus fréquents en pratique : `…`, `–`, `—`, `'`, `"` et `"`.

**Ne pas remplacer** dans les blocs de code (` ``` `), le code inline, ni dans les URLs.

**Script de sanitisation automatique**

Plutôt que de laisser le LLM effectuer ces substitutions manuellement,
utiliser le script Python fourni dans ce skill :

```bash
# Aperçu sans modifier le fichier
python .github/skills/blog-reviewer/sanitize_unicode.py --dry-run content/posts/2026/mon-article/index.md

# Correction en place
python .github/skills/blog-reviewer/sanitize_unicode.py content/posts/2026/mon-article/index.md
```

Le script préserve automatiquement les blocs de code fencés, le code inline
et les URLs. Lancer ce script **avant** toute relecture manuelle.

**Termes techniques**

- Conserver les noms propres et termes techniques en anglais : Java, Spring,
  API, record, sealed, interface, etc.
- Ne pas traduire les noms de projets ni les identifiants de code
- Ne pas modifier le style ni le ton de l'auteur — corriger uniquement les
  erreurs avérées

## Étape 4 — Préparer le frontmatter

Générer ou mettre à jour le bloc YAML frontmatter. Consulter
[références frontmatter](./references/frontmatter.md) pour le détail complet.

### Champs obligatoires

```yaml
---
title: "Titre de l'article en français"
date: "YYYY-MM-DDTHH:MM:SS+00:00"
url: /YYYY/MM/slug/
author: Antoine Rey
categories:
  - <catégorie>
tags:
  - <tag1>
  - <tag2>
---
```

### Champs conditionnels

| Champ                            | Quand l'ajouter                                               |
|----------------------------------|---------------------------------------------------------------|
| `usePageBundles: true`           | Article en page bundle (images co-localisées dans le dossier) |
| `featureImage: filename.ext`     | L'article a une image de couverture                           |
| `featureImageAlt: "Description"` | Toujours présent quand `featureImage` est défini              |
| `thumbnail: filename.png`        | Miniature pour la sidebar (peut différer de `featureImage`)   |
| `toc: true`                      | L'article comporte 3 sections `##` ou plus                    |
| `featured: true`                 | Article phare à mettre en avant sur la homepage               |
| `summary: \|-`                   | Résumé personnalisé (prioritaire sur `<!--more-->`)           |

### Convention `summary:` du blog

- Le `summary` reprend en principe **mot pour mot le début de l'article**
- Pour une note de conférence, reprendre les lignes d'ouverture
  (`Conférence`, `Date`, `Speakers`, `Format`, éventuels liens)
  puis le ou les premiers paragraphes d'introduction
- Dans le frontmatter YAML, conserver les retours à la ligne du bloc et utiliser
  `<br>` pour les lignes de métadonnées de conférence
- Le `summary` se termine souvent par une image illustrative,
  typiquement la photo des speakers sur scène ou le visuel d'ouverture
- Toute image incluse dans le `summary` doit utiliser un **chemin absolu**
  (ex. `/2026/04/slug/image.jpg`), même pour un page bundle

### Catégories disponibles (kebab-case, français)

- `conférence` — notes de conférence (Devoxx, SnowCamp, etc.)
- `retour-d'expérience` — retours d'expérience terrain
- `spring` — écosystème Spring Framework
- `maven` — outillage de build Maven
- `orm` — accès aux données (JPA, Hibernate, jOOQ)
- `test` — tests (unitaires, intégration, e2e)

### Tags (minuscules, trait d'union)

Réutiliser les tags existants quand c'est possible.
Exemples fréquents : `devoxx`, `spring-boot`, `java`, `jpa`, `jooq`,
`architecture`, `ddd`, `hexagonal`, `langchain4j`, `genai`, `spring-modulith`.

### Champs legacy WordPress

Conserver tels quels si déjà présents (`post_id`, `guid`, `_edit_last`,
`post_views_count`). Ne pas les ajouter pour les nouveaux articles.

## Étape 5 — Mise en forme des lignes (160 caractères)

**Règle** : aucune ligne de prose ne dépasse **160 caractères**.

- Couper au niveau d'une **frontière de phrase ou de proposition**
- Chaque phrase peut occuper sa propre ligne
- Préserver les lignes vides entre paragraphes
- **Ne jamais modifier le contenu des blocs de code** — les lignes de code
  peuvent dépasser 160 caractères
- Les valeurs de frontmatter peuvent rester sur une ligne (notamment `summary:`,
  `guid:`, `featureImageAlt:`)

**Exemple — avant :**

```markdown
Ce talk sur le futur de Java présente les Value Types, une fonctionnalité attendue depuis longtemps qui permettra
d'améliorer les performances des applications Java.
```

**Exemple — après :**

```markdown
Ce talk sur le futur de Java présente les Value Types,
une fonctionnalité attendue depuis longtemps
qui permettra d'améliorer les performances des applications Java.
```

## Étape 6 — Vérification de la section Références

Pour tout article technique qui cite des spécifications, des APIs, des frameworks
ou des sources externes, vérifier la présence et la qualité d'une section
`## Références` en fin d'article.

### Présence et structure

- La section `## Références` doit exister si l'article cite des JEP, des specs,
  de la documentation officielle, du code source ou des publications externes
- Les références sont regroupées par type : `### Spécifications`, `### Documentation`,
  `### Code source`, `### Autres ressources`, ou toute organisation pertinente selon le sujet
- Chaque référence est un lien Markdown avec un libellé descriptif, jamais une URL brute

### Cohérence avec le corps de l'article

- Toute source citée dans le corps de l'article doit figurer en référence
- Les références ne doivent pas contenir de liens absents du corps de l'article,
  sauf pour les sources structurantes contextuelles (standard, spec de fond)
- Vérifier que les numéros de JEP, les noms de classes, les noms de projets et
  les URLs sont cohérents entre le corps de l'article et la section références

### Qualité des références

- Pas d'URL inventée ou non vérifiable — toute référence doit avoir été consultée
  ou confirmée par recherche web
- Pour les JEPs et drafts : vérifier leur statut actuel (Submitted, Preview,
  Draft, GA) et le mentionner dans le lien ou l'article si pertinent
- Pour les articles et talks : indiquer le nom du speaker et la date si disponibles
- Ne pas dupliquer les mêmes sources sous des libellés différents

### Sortie pour la revue des références

Dans le **mode revue technique**, signaler :

- Les références manquantes pour les affirmations importantes
- Les références présentes mais dont le statut ou le contenu a changé
- Les liens suspects ou non vérifiés
- Les références redondantes ou mal organisées

## Étape 7 — Bonnes pratiques Hugo Clarity

### Résumé / extrait

- Insérer `<!--more-->` après le paragraphe d'introduction (2 à 4 phrases max)
- Si le champ `summary:` est défini dans le frontmatter, il prime sur
  `<!--more-->` — ne pas ajouter le marqueur dans ce cas,
  et le retirer s'il est déjà présent
- Lors du reformatage des lignes longues dans le `summary:` YAML, préserver
  le bloc `|-` et l'indentation de 2 espaces — ne pas convertir en chaîne
  ordinaire
- Les images référencées dans `summary:` doivent utiliser des **chemins
  absolus** (ex. `/2026/04/slug/image.jpg`), car le rendu se fait depuis
  la homepage à la racine du site

### Images

- Tout `![texte alternatif](image.jpg)` doit avoir un texte alternatif
  descriptif et accessible
- Pour les conférences : indiquer le nom des intervenants ou le sujet de la
  diapositive dans l'alt text
- Éviter les alt text génériques comme "image", "screenshot" ou le nom du
  fichier seul
- Les images co-localisées dans le page bundle ne nécessitent pas de chemin
  (juste le nom de fichier)

### Convention de nommage des images (page bundle)

Nommer les images en **kebab-case sans accents** :
- `speakers.jpeg` pour la photo des intervenants
- `hierarchie-caches-cpu.jpeg` pour une diapositive d'architecture CPU
- `happens-before.jpeg` pour une diapositive sur le JMM
- `demo-vote-pizza.png` pour un screenshot d'application démo
- `systemes-distribues.jpeg` pour une diapositive sur les systèmes distribués

Règles :
- Pas de majuscules, pas d'espaces, pas d'accents, pas de caractères spéciaux
- Noms courts et descriptifs du **contenu** (pas du nom Obsidian ou WordPress)
- Utiliser `-` comme séparateur de mots
- Conserver l'extension d'origine (`.jpeg`, `.png`, etc.)

### Import depuis Obsidian

Les notes Obsidian utilisent la syntaxe wikilink pour les images :
`![[Nom du fichier.jpeg]]`. Hugo ne comprend pas cette syntaxe.

**Workflow de migration Obsidian → Hugo :**

1. **Convertir** chaque `![[Nom fichier.ext]]` en Markdown standard :
   `![alt text descriptif](nom-kebab-case.ext)`
2. **Renommer** les fichiers images en kebab-case sans accents (voir convention
   ci-dessus) — les noms Obsidian contiennent souvent des espaces et des
   accents (ex. `JCStress - Mémoire partagée.jpeg` → `memoire-partagee.jpeg`)
3. **Ajouter un alt text** descriptif basé sur le contenu de l'image et le
   contexte de l'article (visionner l'image si nécessaire)
4. Vérifier que tous les fichiers images sont bien présents dans le répertoire
   du page bundle (un fichier manquant provoque une image cassée sans erreur
   de build Hugo)

### Structure des titres

- Le titre H1 est défini dans le frontmatter (`title:`) — ne pas le répéter
  avec un `# Titre` dans le corps de l'article
- Utiliser `##` pour les sections principales, `###` pour les sous-sections
- Ne pas sauter de niveau (ex. ne pas passer de `##` à `####`)

### Blocs de code

- Toujours spécifier le langage : ` ```java `, ` ```kotlin `, ` ```bash `,
  ` ```yaml `, ` ```xml `, ` ```sql `, ` ```json `
- Ne pas modifier le contenu du code

### Liens

- Utiliser un texte de lien descriptif, jamais une URL brute dans le texte
  courant
- Les liens externes sont autorisés tels quels

### Structure selon le type d'article

**Notes de conférence** : ouvrir avec le nom de la conférence, la date,
le(s) intervenant(s) et le format (durée). Exemple :

```
Conférence : Devoxx France 2026
Date : 24 avril 2026
Speakers : Prénom Nom (Société)
Format : conférence (45 min)
```

**Articles techniques** : commencer par l'énoncé du problème avant la
solution. Conclure avec une section de synthèse ou les points clés.


## Sortie attendue

Deux modes de sortie sont possibles :

- **Mode réécriture** : produire le fichier `index.md` complet et révisé. Ne
  pas résumer les changements dans le fichier — produire le texte intégral.
  Après le fichier, lister brièvement les corrections effectuées (ex. :
  "3 fautes d'orthographe corrigées, frontmatter ajouté, 8 lignes
  reformatées, section Références ajoutée"). Ne pas commiter.
- **Mode revue technique** : produire d'abord les findings priorisés, puis les
  questions ouvertes, puis seulement si demandé une proposition de correction ou
  un patch du fichier. Ne pas commiter. Les findings incluent un point dédié
  sur la section Références : présence, cohérence, qualité des liens.
