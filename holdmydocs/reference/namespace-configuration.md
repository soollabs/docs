---
title: Namespace Configuration Reference
tags: hmd, reference
---

Put `.namespace.yaml` in a namespace directory. All keys are optional.

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

- `widgets` replaces the default composition instead of adding to it.
- `public` covers the whole namespace.
- `index` names the page served at the namespace root. It is always first in the tree.
- `tree` lists page or folder paths in order. Unlisted siblings follow alphabetically. Live sidebar and static exports use the same order.
- `new` sets the hidden template and slug pattern for quick-create.

Widgets you can list in `widgets`:

| Widget | Heading | Shows |
| --- | --- | --- |
| `pages` | recently viewed | Pages you opened recently in this namespace, in this browser, with your palette pins first. |
| `namespaces` | namespaces | Every namespace with its page count. |
| `pinned` | pinned | Pages with `pin: true`. |
| `tags` | tags | The five most used tags in this namespace, with a link to the rest. |
| `log` | log | The last few commits to the current page. |
| `health` | health | Missing links and orphaned pages, linking to the full report. |
| `calendar` | | A month of daily pages, with entries highlighted. |
| `writing-stats` | this month | Days written, streak and word count for this month. |
| `page-meta` | | Tags, last editor and revision count, above the page. |
| `backlinks` | linked from | Pages that link to this one, below the page. |
| `prev-entries` | earlier | The daily entries just before this one, below the page. |

<!-- generated:namespace -->

| Key | Environment variable | Type and default | Accepted values | Restart | Description |
| --- | --- | --- | --- | --- | --- |
| `title` | — | string; not specified | maximum length: `256` | — | Name readers see for the namespace, including as the static site title. Defaults to the namespace name. |
| `description` | — | string; not specified | maximum length: `255` | — | Short summary shown in namespace lists, at most 255 characters. |
| `public` | — | boolean, `false` | — | — | Let anyone read every page and attachment in the namespace without signing in. Public never means editable by everyone. |
| `index` | — | string; not specified | — | — | One-segment page name that opens at /&lt;namespace&gt;/ and is the static site's homepage. |
| `tree` | — | array; not specified | items: string | — | Order of pages and folders in the sidebar and static export. Drag to reorder; folders start collapsed and the index page stays first. |
| `skin` | — | string; not specified | `"bare"`, `"phosphor"`, `"newsprint"`, `"journal"`, `"soft"` | — | Skin shown to anonymous readers and in the static export. Signed-in users see their own skin. |
| `palette` | — | string; not specified | — | — | Colour palette shown to anonymous readers and in the static export. Empty uses the skin's own palette. |
| `image` | — | string; not specified | — | — | Link preview image for pages without an image of their own, shown when a page is shared in a chat app or social network, on public pages and in the static export. Names a PNG or JPEG attachment in this namespace as page/filename, e.g. index/hero.png. The export fails if the attachment is missing. |
| `widgets` | — | array, `["pages", "namespaces", "tags", "log", "page-meta", "backlinks"]` | items: string | — | Sidebar widgets, in order. Leave empty for the built-in set. |
| `new.template` | — | string, `"template"` | — | — | Hidden page whose body every quick-created page starts from. |
| `new.slug` | — | string; not specified | — | — | Go template that names a quick-created page, such as {{.Now.Format "2006-01-02"}} for a daily journal. Enables Ctrl+J. |
| `export.base_url` | — | string; not specified | — | — | Absolute URL where the static site will be published, including any path prefix. Used to build sitemap.xml. |
| `export.sitemap` | — | boolean, `true` | — | — | Include sitemap.xml in the static export. |
| `export.robots_allow` | — | array; not specified | maximum items: `64`; items: string | — | Search and AI bots allowed to crawl the static site. Every other bot is blocked in robots.txt. Use a single "*" to allow every bot. |
| `export.links` | — | array; not specified | maximum items: `32` | — | External links in the static site's sidebar or top bar. Labels are link text, or tooltips for icon-only links; icons use Font Awesome classes such as fa-brands fa-github. |

<!-- /generated:namespace -->

## Export links

- `export` controls the static site independently of the live server.
- `export.base_url` must be an HTTP(S) URL and can include a path prefix.
- Links default to `location: sidebar`. All sidebar links must share the same `icon_only` value: `false` for text links, `true` for an icon row.
- `location: topbar` places links before Search docs and always uses icons.
- Each link needs a label and an HTTP(S) URL. Icons use Font Awesome classes such as `fa-brands fa-github`. Labels become tooltips and accessible names.

See [[Static Export]] for preview access, bundled icons, reserved page paths and command-line overrides.
