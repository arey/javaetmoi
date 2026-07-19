---
name: github-class-linker
description: >-
  Ajoute des liens hypertextes GitHub vers le code source d'un repository
  cité dans un article Java & Moi, pour chaque nom de classe, interface,
  enum ou classe de test mentionné en Markdown inline (backticks). Utilise
  ce skill quand l'utilisateur veut lier des noms de classes Java vers
  github.com, référencer le code source d'un repo (ex. spring-petclinic,
  spring-petclinic-terminal) sur un tag ou une release précise, ou ajouter
  des liens vers un repo GitHub à côté des noms de classes dans un article.
  Déclencher dès que l'utilisateur mentionne : lier les classes vers GitHub,
  ajouter des liens vers le code source, référencer un repo GitHub,
  linker les noms de classe, pointer vers le tag/release d'un repo.
---

# GitHub Class Linker — Java & Moi

Transforme les noms de classes/interfaces/enums cités en Markdown inline
(`` `NomDeClasse` ``) dans un article en liens hypertextes pointant vers le
fichier source correspondant sur GitHub, à un tag donné.

Exemple :

```
AVANT : C'est le rôle de la classe `AppState` : elle porte le contexte...
APRÈS : C'est le rôle de la classe [`AppState`](https://github.com/OWNER/REPO/blob/TAG/chemin/AppState.java) : elle porte le contexte...
```

## Étape 1 — Calibrer avec l'utilisateur

Ne jamais deviner silencieusement ces paramètres — les confirmer explicitement
(ils changent radicalement le résultat) :

1. **Repo et tag cible** : `owner/repo` et le tag exact (ex. `v0.4.0`). Si
   l'utilisateur donne un exemple d'URL, vérifier qu'il correspond bien au tag
   annoncé dans sa demande — signaler toute incohérence avant de continuer.
2. **Périmètre** : uniquement les classes qui appartiennent réellement à ce
   repo, ou aussi des classes de librairies tierces mentionnées dans
   l'article (auquel cas il faut un autre repo/tag pour celles-ci) ?
3. **Répétition** : lier chaque occurrence d'une classe, ou seulement sa
   première apparition dans l'article ?
4. **Blocs de code** : les noms de classes à l'intérieur de blocs ` ```java `
   doivent-ils aussi être transformés en liens, ou seulement le texte
   narratif (recommandé — un lien Markdown dans un bloc de code cassé
   la coloration syntaxique) ?
5. **Types inclus** : les interfaces, enums et classes de test comptent-ils
   comme des "classes" à lier au même titre ?

## Étape 2 — Extraire les candidats

Chercher dans l'article les noms entourés de backticks simples qui
ressemblent à un identifiant Java `CamelCase` (première lettre majuscule) :

```bash
grep -noE '`[A-Z][A-Za-z0-9]*`' content/posts/YYYY/slug/index.md
```

Ignorer les faux positifs : annotations (`@Component`), types génériques
standard (`List`, `Map`, `Page`), mots-clés en gras/italique, noms de
variables en camelCase minuscule.

## Étape 3 — Vérifier la liste réelle des fichiers du repo au tag

Ne jamais construire une URL de fichier sans l'avoir vérifiée : les chemins
de package peuvent différer du nom de la classe (sous-package, module,
`src/test` vs `src/main`).

```bash
gh api repos/OWNER/REPO/git/trees/TAG?recursive=1 \
  --jq '.tree[] | select(.path | endswith(".java")) | .path'
```

Pour chaque candidat de l'étape 2, chercher son fichier exact
(`grep -F "/NomDeClasse.java"` dans la sortie ci-dessus). Si aucun fichier ne
correspond, **exclure** ce candidat (c'est probablement une classe d'une
librairie tierce ou du JDK) — ne jamais inventer un chemin plausible.

## Étape 4 — Localiser les occurrences à transformer

Pour chaque classe retenue, localiser ses occurrences avec `grep -n` et
déterminer, selon les réponses de l'étape 1 :

- La première occurrence uniquement, ou toutes
- En excluant les occurrences situées entre deux lignes ` ```...``` ` (blocs
  de code), sauf si l'utilisateur a explicitement demandé de les inclure
- En excluant le frontmatter YAML

## Étape 5 — Appliquer les remplacements

Remplacer `` `NomDeClasse` `` par
`` [`NomDeClasse`](https://github.com/OWNER/REPO/blob/TAG/chemin/complet/NomDeClasse.java) ``.

Attention à la syntaxe Markdown : les deux backticks doivent encadrer le nom
**à l'intérieur** des crochets — `[`Nom`](url)`, jamais `[`Nom](url)` (backtick
fermant manquant, erreur fréquente).

Utiliser l'outil `edit` avec un `old_str` suffisamment large (la phrase
complète) pour cibler la bonne occurrence sans ambiguïté, surtout quand un
nom de classe apparaît plusieurs fois dans le fichier.

## Étape 6 — Récapituler avant validation finale

Avant de conclure, présenter à l'utilisateur la liste des classes liées et,
séparément, la liste des candidats exclus avec la raison (bloc de code,
classe tierce non trouvée dans le repo, doublon déjà lié). Cela permet de
détecter une erreur de périmètre avant qu'elle ne se propage à tout
l'article.

## Étape 7 — Valider

```bash
hugo --logLevel error
```

Vérifier l'absence de ligne `ERROR`. Vérifier aussi qu'aucun lien
`[`...]` mal fermé ne subsiste :

```bash
grep -n '\[`[A-Za-z0-9]*\]' content/posts/YYYY/slug/index.md | grep -v '\](http'
```

Une sortie vide confirme qu'il n'y a pas de lien Markdown mal formé.
