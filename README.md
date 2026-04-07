# Java & Moi — Blog Hugo

Blog personnel [javaetmoi.com](https://javaetmoi.com) d'Antoine Rey, migré de WordPress vers [Hugo](https://gohugo.io/) avec le thème [Hugo Clarity](https://github.com/chipzoller/hugo-clarity).

## Prérequis

- [Hugo Extended](https://gohugo.io/installation/) ≥ 0.160 (Extended requis pour la compilation SASS)
- Git (avec support des submodules)

```bash
# Cloner avec le submodule du thème
git clone --recurse-submodules <repo-url>

# Ou, après un clone sans --recurse-submodules
git submodule update --init --recursive
```

## Commandes

```bash
# Serveur de développement (live reload sur http://localhost:1313)
hugo serve

# Build de production (sortie dans public/)
hugo

# Build avec affichage des erreurs uniquement
hugo --logLevel error
```

La validation se fait via `hugo --logLevel error` : exit code 0 et aucune ligne `ERROR`.

## Structure du projet

```
config/_default/        Configuration Hugo (hugo.toml, params.toml, markup.toml, menus/)
content/
  posts/                Articles de blog (fichiers .md plats)
  pages/                Pages statiques (about, spring) en leaf bundles
data/
  comments.yaml         Commentaires WordPress exportés
  library.yaml          Données bibliothèque
static/wp-content/      Images des articles (chemins WordPress conservés)
layouts/                Overrides et templates custom (voir ci-dessous)
assets/sass/            Overrides SASS du thème
themes/hugo-clarity/    Thème (git submodule)
nginx.conf              Redirections legacy WordPress (?p=ID → slug)
```

---

## Mise à jour du thème Hugo Clarity

Le thème est installé en **git submodule**. Tes personnalisations sont toutes dans le projet racine et ne sont **jamais** écrasées par une mise à jour du thème.

### 1. Inspecter les changements amont

```bash
# Voir les commits disponibles sur le thème
git -C themes/hugo-clarity fetch
git -C themes/hugo-clarity log HEAD..origin/main --oneline
```

### 2. Vérifier l'impact sur les overrides locaux

Avant de mettre à jour, vérifier si Clarity a modifié les partials qu'on surcharge :

```bash
git -C themes/hugo-clarity diff HEAD origin/main -- \
  layouts/partials/header.html \
  layouts/partials/sidebar.html \
  layouts/_default/_markup/render-image.html
```

Si un de ces fichiers a changé, **fusionner manuellement** les modifications de Clarity avec nos ajouts (voir section [Overrides locaux](#overrides-locaux) ci-dessous).

### 3. Appliquer la mise à jour

```bash
git submodule update --remote themes/hugo-clarity

# Vérifier que le build est toujours clean
hugo --logLevel error

# Committer la montée de version
git add themes/hugo-clarity
git commit -m "chore: upgrade hugo-clarity theme to $(git -C themes/hugo-clarity rev-parse --short HEAD)"
```

---

## Overrides locaux du thème

Hugo résout les templates dans cet ordre de priorité : **projet > thème**. Tous les fichiers ci-dessous surchargent leur équivalent dans `themes/hugo-clarity/` sans modifier le thème.

| Fichier projet | Surcharge | Raison |
|---|---|---|
| `layouts/partials/header.html` | `themes/.../header.html` | Bannière au-dessus de la nav |
| `layouts/partials/sidebar.html` | `themes/.../sidebar.html` | Widgets Devoxx + Blogs Java |
| `layouts/_default/_markup/render-image.html` | `themes/.../_markup/render-image.html` | Fix nil `Page.File` sur pages virtuelles |
| `assets/sass/_custom.sass` | `themes/.../sass/_custom.sass` | Styles bannière + nav sticky (pattern officiel Clarity) |
| `layouts/partials/hooks/body-end.html` | *(hook — n'existe pas dans le thème)* | Injection des commentaires WordPress |
| `layouts/partials/wp-comments.html` | *(spécifique au projet)* | Rendu commentaires depuis `data/comments.yaml` |
| `layouts/rss.xml` | `themes/.../rss.xml` | Feed servi en `/feed.xml` (compat. WordPress) |
| `layouts/shortcodes/` | *(shortcodes custom)* | gallery, catlist, audio, googlemaps, parallaxblur |

### Fichiers SASS officiellement supportés pour l'override

Clarity documente deux points d'extension SASS à créer à la racine du projet :

- **`assets/sass/_custom.sass`** — styles additionnels et overrides généraux
- **`assets/sass/_override.sass`** — override des variables CSS du thème (`$theme`, couleurs, etc.)

Ces deux fichiers sont fusionnés automatiquement par Hugo dans le pipeline SASS.

---

## Mise à jour de Hugo

```bash
# macOS avec Homebrew
brew upgrade hugo

# Vérifier la version
hugo version

# Valider le build après upgrade
hugo --logLevel error
```

> ⚠️ Hugo Extended est requis (compilation SASS). La version standard ne suffit pas.
