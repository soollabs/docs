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

`export` applies to static exports, not live pages:

- `base_url`: required HTTP(S) publishing URL, including any path prefix.
- `sitemap`: generate `sitemap.xml`; defaults to `true`. When `false`, an existing sitemap in the CLI output directory is removed.
- `robots_allow`: permitted bot names; empty by default, blocking all bots. Maximum 64 names.
- `links`: ordered external links. Each needs `label` and `url`; maximum 32 links.

Links default to `location: sidebar`. All sidebar links must share the same `icon_only` value: `false` for centred text links, one per line; `true` for a centred, wrapping icon row. `location: topbar` places an icon immediately before Search docs and always uses icon-only display. Icons require Font Awesome classes; their labels become tooltips and accessible names.

HMD downloads the selected SVG icons during generation and includes them in the export with their licence notices. No CDN access is needed to view them. See [[Static Export]] for generation requirements and CLI overrides.

Static exports reserve `robots.txt` and `sitemap.xml` as first page segments, including case variants and descendants, even when sitemaps are disabled. Nested names such as `guide/robots.txt` remain valid. Rename conflicting first segments before exporting.
