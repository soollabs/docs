---
title: Namespace Configuration Reference
tags: hmd, reference
---

Place `.namespace.yaml` in a namespace directory:

```yaml
title: Documentation
description: Public product documentation
public: true
skin: journal
palette: nord
index: index
tree: [getting-started, guides, reference, about]
widgets: [pages, tags, backlinks]
new:
  template: entry
  slug: '{{.Now.Format "2006-01-02"}}'
export:
  base_url: https://docs.example.org/
  sitemap: true
  robots_allow: [Googlebot, bingbot]
  links:
    - label: GitHub
      url: https://github.com/soollabs/holdmydocs
      icon: fa-brands fa-github
      location: topbar
      icon_only: true
```

All keys are optional. `widgets` replaces the default composition rather than adding to it. `public` covers the entire namespace. `index` names the page served at the namespace root and is always first in the tree. `tree` is an optional ordered list of page or folder paths; unlisted siblings follow in alphabetical order. The same tree order is used in the live sidebar and static exports. `new` defines the hidden template and slug pattern used by quick-create.

<!-- generated:namespace -->

| Key | Environment variable | Type and default | Accepted values | Restart | Description |
| --- | --- | --- | --- | --- | --- |
| `title` | — | string; not specified | maximum length: `256` | — | Name readers see for the namespace, including as the static site title. Defaults to the namespace name. |
| `description` | — | string; not specified | maximum length: `255` | — | Short summary shown in namespace lists, at most 255 characters. |
| `public` | — | boolean, `false` | — | — | Let anyone read every page and attachment in the namespace without signing in. Public never means editable by everyone. |
| `index` | — | string; not specified | — | — | One-segment page name that opens at /&lt;namespace&gt;/ and is the static site's homepage. |
| `tree` | — | array; not specified | items: string | — | Order of pages and folders in the sidebar and static export. Drag to reorder; folders start collapsed and the index page stays first. |
| `skin` | — | string; not specified | `"phosphor"`, `"newsprint"`, `"journal"`, `"soft"`, `"bare"` | — | Skin shown to anonymous readers and in the static export. Signed-in users see their own skin. |
| `palette` | — | string; not specified | — | — | Colour palette shown to anonymous readers and in the static export. Empty uses the skin's own palette. |
| `widgets` | — | array, `["pages", "namespaces", "tags", "log", "page-meta", "backlinks"]` | items: string | — | Sidebar widgets, in order. Leave empty for the built-in set. |
| `new.template` | — | string, `"template"` | — | — | Hidden page whose body every quick-created page starts from. |
| `new.slug` | — | string; not specified | — | — | Go template that names a quick-created page, such as {{.Now.Format "2006-01-02"}} for a daily journal. Enables Ctrl+J. |
| `export.base_url` | — | string; not specified | — | — | Absolute URL where the static site will be published, including any path prefix. Used to build sitemap.xml. |
| `export.sitemap` | — | boolean, `true` | — | — | Include sitemap.xml in the static export. |
| `export.robots_allow` | — | array; not specified | maximum items: `64`; items: string | — | Search and AI bots allowed to crawl the static site. Every other bot is blocked in robots.txt. |
| `export.links` | — | array; not specified | maximum items: `32` | — | External links in the static site's sidebar or top bar. Labels are link text, or tooltips for icon-only links; icons use Font Awesome classes such as fa-brands fa-github. |

<!-- /generated:namespace -->

`export` controls the static site independently of the live server. `export.base_url` must be an HTTP(S) publishing URL and can include a path prefix.

External links default to `location: sidebar`. All sidebar links must share the same `icon_only` value: `false` for text links or `true` for an icon row. `location: topbar` places links before Search docs and always uses icons. Each link requires a label and an HTTP(S) URL. Icons require Font Awesome classes such as `fa-brands fa-github`; labels provide tooltips and accessible names.

See [[Static Export]] for preview access, bundled icons, reserved page paths and command-line overrides.
