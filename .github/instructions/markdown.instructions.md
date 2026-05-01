---
applyTo: "content/**/*.md"
---

## Caractères autorisés dans les fichiers de contenu

Utiliser exclusivement des caractères ASCII dans le texte courant.
Ne jamais générer les caractères Unicode typographiques listés ci-dessous.

| A éviter    | Unicode          | Remplacer par   |
|-------------|------------------|-----------------|
| `…`         | U+2026           | `...`           |
| `–`         | U+2013           | `-`             |
| `—`         | U+2014           | `--` ou `-`     |
| `‒`         | U+2012           | `-`             |
| `'`         | U+2018           | `'`             |
| `'`         | U+2019           | `'`             |
| `"`         | U+201C           | `"`             |
| `"`         | U+201D           | `"`             |
| `„`         | U+201E           | `"`             |
| `«`         | U+00AB           | `<<`            |
| `»`         | U+00BB           | `>>`            |
| ` ` (NBSP)  | U+00A0           | espace normal   |
| ` ` (thin)  | U+2009           | espace normal   |
| ` ` (NNBS)  | U+202F           | espace normal   |
| `×`         | U+00D7           | `x`             |
| `✓` / `✗`  | U+2713 / U+2717  | `ok` / `x`      |
| `•`         | U+2022           | `-` ou `*`      |
| `′`         | U+2032           | `'`             |
| `″`         | U+2033           | `"`             |

Cette règle s'applique au texte courant, aux titres, aux tableaux et aux
attributs Markdown (alt text, libellés de liens, frontmatter).
Elle ne s'applique pas aux blocs de code fencés ni aux URLs.
