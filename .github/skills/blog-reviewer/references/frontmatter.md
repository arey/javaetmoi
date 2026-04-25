# Référence Frontmatter — Java & Moi

Référence complète des champs YAML frontmatter utilisés sur javaetmoi.com.

## Frontmatter minimal (nouvel article)

```yaml
---
title: "Titre de l'article"
date: "2026-04-24T10:00:00+00:00"
url: /2026/04/slug-de-l-article/
author: Antoine Rey
categories:
  - retour-d'expérience
tags:
  - java
  - spring-boot
---
```

## Frontmatter complet (article avec images)

```yaml
---
title: "Titre de l'article"
date: "2026-04-24T10:00:00+00:00"
url: /2026/04/slug-de-l-article/
author: Antoine Rey
categories:
  - conférence
  - retour-d'expérience
tags:
  - devoxx
  - java
  - spring-boot
usePageBundles: true
featureImage: nom-image-couverture.jpg
featureImageAlt: "Description accessible de l'image de couverture"
thumbnail: logo/logo-devoxx-france.png
toc: true
summary: |-
  Premier paragraphe du résumé affiché sur la homepage.

  Deuxième paragraphe si nécessaire.

  ![Alt texte](/2026/04/slug-de-l-article/nom-image-couverture.jpg)
---
```

## Description de chaque champ

### Champs identité

| Champ    | Type            | Obligatoire | Description                                                      |
|----------|-----------------|-------------|------------------------------------------------------------------|
| `title`  | string          | ✅           | Titre de l'article, en français, entre guillemets                |
| `date`   | string ISO 8601 | ✅           | Date de publication au format `"YYYY-MM-DDTHH:MM:SS+00:00"`      |
| `url`    | string          | ✅           | URL canonique `/YYYY/MM/slug/` — correspond au pattern WordPress |
| `author` | string          | ✅           | Toujours `Antoine Rey`                                           |

### Taxonomies

| Champ        | Type       | Description                                     |
|--------------|------------|-------------------------------------------------|
| `categories` | liste YAML | Minimum 1. Voir liste des catégories ci-dessous |
| `tags`       | liste YAML | Mots-clés techniques, minuscules, trait d'union |

### Images

| Champ             | Type   | Description                                                                                        |
|-------------------|--------|----------------------------------------------------------------------------------------------------|
| `featureImage`    | string | Nom du fichier image de couverture (sans chemin si page bundle)                                    |
| `featureImageAlt` | string | Texte alternatif accessible, entre guillemets doubles                                              |
| `thumbnail`       | string | Miniature pour la sidebar. Peut pointer vers `logo/fichier.png` (static) ou vers un fichier bundle |
| `usePageBundles`  | bool   | `true` si le post est un page bundle (images co-localisées). Omis si `false`                       |

### Mise en page

| Champ      | Type             | Description                                                                             |
|------------|------------------|-----------------------------------------------------------------------------------------|
| `toc`      | bool             | `true` pour afficher une table des matières. Recommandé si l'article a 3+ sections `##` |
| `featured` | bool             | `true` pour mettre l'article en avant sur la homepage. Usage rare                       |
| `summary`  | string multiline | Résumé HTML/Markdown pour la homepage. Prioritaire sur `<!--more-->`. Utiliser `        |-` pour les blocs multilignes |

### Champs legacy WordPress

Ces champs proviennent de la migration wp2hugo. Les conserver sur les anciens
articles, **ne pas les ajouter sur les nouveaux**.

| Champ              | Description                                                                 |
|--------------------|-----------------------------------------------------------------------------|
| `post_id`          | ID numérique WordPress (string). Utilisé par Giscus pour l'og:title mapping |
| `guid`             | URL WordPress canonique `https://javaetmoi.com/?p=<id>`                     |
| `_edit_last`       | ID utilisateur WordPress de la dernière modification                        |
| `post_views_count` | Compteur de vues WordPress                                                  |
| `parent_post_id`   | ID du post parent (null pour les articles racines)                          |
| `_thumbnail_id`    | ID de l'image à la une WordPress                                            |

## Catégories disponibles

| Valeur YAML           | Description                                               |
|-----------------------|-----------------------------------------------------------|
| `conférence`          | Notes de conférence : Devoxx France, SnowCamp, BDX I/O…   |
| `retour-d'expérience` | Retours terrain, REX, feedbacks de mission                |
| `spring`              | Écosystème Spring Framework (Core, Boot, Data, Security…) |
| `maven`               | Build avec Maven, plugins, archetypes                     |
| `orm`                 | Accès aux données : JPA, Hibernate, jOOQ, JDBC            |
| `test`                | Tests unitaires, d'intégration, e2e, TDD                  |

## Tags fréquents

```
architecture    ddd             devoxx          docker
genai           hexagonal       hibernate       java
jooq            jpa             junit           kotlin
langchain4j     maven           mockito         openai
spring          spring-boot     spring-data     spring-modulith
spring-petclinic  spring-security  sql           testcontainers
```

## Convention de slug (URL)

Le slug correspond au nom du dossier du page bundle :

```
content/posts/2026/mon-super-article/index.md
                    ↑
              url: /2026/04/mon-super-article/
```

Règles :

- Minuscules, tirets entre les mots
- Pas d'accents dans le slug (l'URL doit être ASCII-safe)
- Pas de `/` finaux redondants — Hugo les ajoute automatiquement

## Exemples de frontmatter par type d'article

### Notes de conférence Devoxx

```yaml
---
title: "Titre du talk — Devoxx France 2026"
date: "2026-04-25T09:00:00+00:00"
url: /2026/04/titre-du-talk-devoxx-france-2026/
author: Antoine Rey
categories:
  - conférence
tags:
  - devoxx
  - java
usePageBundles: true
featureImage: speakers.jpeg
featureImageAlt: "Intervenants du talk Titre du talk"
thumbnail: logo/logo-devoxx-france.png
summary: |-
  Résumé en 2-3 phrases du talk.

  Conférence : Devoxx France 2026 — Speakers : Prénom Nom (Société)

  ![Intervenants](/2026/04/titre-du-talk-devoxx-france-2026/speakers.jpeg)
---
```

### Article technique / REX

```yaml
---
title: "Comment faire X avec Spring Boot"
date: "2026-05-15T14:30:00+00:00"
url: /2026/05/comment-faire-x-avec-spring-boot/
author: Antoine Rey
categories:
  - retour-d'expérience
  - spring
tags:
  - spring-boot
  - java
usePageBundles: true
featureImage: banner.png
featureImageAlt: "Bannière illustrant le sujet X avec Spring Boot"
toc: true
---
```
