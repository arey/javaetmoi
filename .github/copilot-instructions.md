# Copilot Instructions

## Build & Development Commands

```bash
# Start dev server (live reload on http://localhost:1313)
hugo serve

# Production build (outputs to public/)
hugo

# Build with verbose error output
hugo --logLevel error
```

There is no test suite or linter — `hugo build` (exit code 0, no ERROR lines) is the validation step.

## Verification Workflow

After making changes, the agent should:

1. **Start the dev server** (if not already running) and check for build errors:
   ```bash
   hugo serve --port 1313
   ```
   Verify the output contains no `ERROR` lines. The site reloads automatically on file changes.

2. **Verify visual rendering** using the MCP Google Chrome DevTools server (`mcp_io_github_chr_*` tools):
   - Navigate to the relevant page: `mcp_io_github_chr_navigate_page` with `http://localhost:1313/`
   - Take a screenshot: `mcp_io_github_chr_take_screenshot`
   - Inspect computed styles or DOM elements when debugging visual issues: `mcp_io_github_chr_evaluate_script`
   - Check the HTML snapshot: `mcp_io_github_chr_take_snapshot`

   These tools require the Chrome browser to be open and the MCP Chrome DevTools server to be running.

## Architecture

This is a **Hugo static blog** (`javaetmoi.com`) migrated from WordPress using wp2hugo. The theme is **Hugo Clarity** (`themes/hugo-clarity/`, installed as a git submodule).

### Content layout

- `content/posts/{year}/` — blog articles, one flat `.md` file per post (~114 posts), organized by year (2012–2026)
- `content/pages/{slug}/index.md` — static pages as leaf bundles (about, spring)
- `data/comments.yaml` — WordPress comments exported from the old site
- `data/library.yaml` — book/resource library data
- `static/wp-content/` — all post images (kept at their original WordPress paths)

### Configuration

Configuration lives in `config/_default/`:
- `hugo.toml` — site-level settings (baseURL, title, taxonomies, output formats)
- `params.toml` — Clarity theme parameters (author, logo, numberOfRecentPosts, etc.)
- `markup.toml` — Goldmark renderer and syntax highlight settings
- `menus/menu.fr.toml` — navigation menu items

### Custom templates

- `layouts/shortcodes/` — custom shortcodes: `gallery`, `catlist`, `audio`, `googlemaps`, `parallaxblur`
- `layouts/partials/wp-comments.html` — renders threaded comments from `data/comments.yaml`
- `layouts/partials/hooks/body-end.html` — invokes `wp-comments.html` via Clarity's body-end hook
- `layouts/partials/sidebar.html` — overrides Clarity sidebar; adds Devoxx France + Blogs Java widgets
- `layouts/_default/_markup/render-image.html` — overrides Clarity render-image to handle nil `.Page.File` for virtual pages
- `layouts/rss.xml` — custom RSS template; feed is served at `/feed.xml` (not `/index.xml`)

### Redirects

`nginx.conf` handles WordPress legacy URL redirects (`?p=<post_id>` → new slug). This file is used in the production container, not by Hugo itself.

## Key Conventions

### Post front matter

Posts preserve WordPress metadata fields (`post_id`, `guid`, `_edit_last`, etc.). **Do not remove them** — `post_id` is used by `wp-comments.html` to match comments from `data/comments.yaml`.

Post URLs follow the WordPress pattern and are set explicitly:
```yaml
url: /YYYY/MM/slug/
```

Cover/feature images use Clarity's flat front matter fields:
```yaml
featureImage: /wp-content/uploads/YYYY/MM/filename.jpg
featureImageAlt: "Description"
```

**Note:** PaperMod's nested `cover.image`/`cover.alt` format is no longer used.

### Taxonomies

Two taxonomies are active: `categories` and `tags`. Both are used in posts. Category values are kebab-case in French (e.g., `retour-d'expérience`, `conférence`).

### Summary splits

Use Hugo's native `<!--more-->` marker to split post summaries. Do **not** use `{{< more >}}` (this was a WordPress shortcode that is not defined).

### Raw HTML in content

`goldmark.renderer.unsafe: true` is intentional. Posts migrated from WordPress contain raw HTML (tables, iframes, embedded slideshare/YouTube). Do not remove this setting.

### Syntax highlighting

Syntax highlighting uses Hugo's built-in Chroma (style: monokai). Code blocks use standard fenced markdown syntax.

### Shortcode parameters

Shortcode string parameters containing single quotes or newlines break Hugo's parser. Multi-line `alt`/`caption` values in `{{< figure >}}` must be collapsed to a single line.

### Comments system

Comments are served from `data/comments.yaml` via `layouts/partials/wp-comments.html`. Access the data via `hugo.Data.comments` (not `.Site.Data.comments` which is deprecated since Hugo 0.156.0).

### Clarity theme notes

- `mainSections = ["posts"]` and `blogDir = "posts"` are required (Clarity defaults to `"post"`)
- `usePageBundles = false` — posts are flat `.md` files, not page bundles
- Clarity's own `layouts/partials/comments.html` (for Disqus/Giscus) is not used — our custom partial is invoked via the `body-end` hook instead
- Do not add a `content/search.md` or `content/archives.md` — these are PaperMod-specific and have no Clarity equivalent

## Hugo Theme Override System

Hugo resolves templates with this priority: **project `layouts/` > theme `layouts/`**. Project-level files are never overwritten by theme upgrades.

### How to override a theme template

Copy the file from the theme to the same relative path in the project root:

```bash
# Example: override a partial
cp themes/hugo-clarity/layouts/partials/header.html layouts/partials/header.html

# Example: override a default template
cp themes/hugo-clarity/layouts/_default/single.html layouts/_default/single.html
```

Edit the copy — Hugo will use the project version automatically.

### Clarity-specific extension points

Clarity explicitly supports two SASS override files at the **project root** (do not edit theme files):

| File | Purpose |
|---|---|
| `assets/sass/_custom.sass` | Additional styles and general CSS overrides |
| `assets/sass/_override.sass` | Override Clarity's SASS variables (`$theme`, colors, fonts) |

Clarity also supports two **template hooks** — create these files to inject HTML without copying full partials:

| Hook | Injected at |
|---|---|
| `layouts/partials/hooks/head-end.html` | Before `</head>` |
| `layouts/partials/hooks/body-end.html` | Before `</body>` |

### Current project overrides

| Project file | Overrides | Notes |
|---|---|---|
| `layouts/partials/header.html` | `themes/.../header.html` | Adds full-width banner above nav; nav changed to sticky |
| `layouts/partials/sidebar.html` | `themes/.../sidebar.html` | Adds Devoxx France + Blogs Java sections |
| `layouts/_default/_markup/render-image.html` | `themes/.../_markup/render-image.html` | Guards against nil `$.Page.File` on virtual pages |
| `assets/sass/_custom.sass` | `themes/.../sass/_custom.sass` | Banner width (100vw) + nav sticky positioning |
| `layouts/partials/hooks/body-end.html` | *(hook, no theme equivalent)* | Invokes `wp-comments.html` |

### Theme upgrade checklist

Before running `git submodule update --remote themes/hugo-clarity`, diff the files we override:

```bash
git -C themes/hugo-clarity diff HEAD origin/main -- \
  layouts/partials/header.html \
  layouts/partials/sidebar.html \
  layouts/_default/_markup/render-image.html
```

If Clarity changed a file we override, manually merge upstream changes into our version before updating. See `README.md` for the full upgrade procedure.


