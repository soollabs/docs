---
title: Static Export
tags: hmd, integrations, publishing
---

Turn a namespace into a self-contained static website you can host anywhere, with no HMD instance behind it.

## Prerequisites

- A namespace that already has pages. The export action only appears for namespaces with at least one page.
- A namespace `index` setting pointing to an existing page, if you want that page to be the site homepage. Without this setting, the homepage asks readers to select a page from the sidebar. See [[Namespace Configuration Reference]].
- An export base URL identifying the published static site, including any path prefix. This is independent of the main HMD `base_url`.

> Treat the archive as publishable content, not an access-controlled backup. The static host does not inherit HMD accounts or namespace permissions. Review every page and attachment before making the archive public.

## Export a namespace

1. Open **Namespaces** from the settings menu. Each namespace lists an **Export static site** action.


2. Set the publishing URL and options in **Namespaces → Edit → static export**, then save. Click **Export static site** to download `{namespace}-export.zip`. If no publishing URL is set, HMD asks whether to use its main URL for this export.
3. Unpack the archive. It contains an `index.html`, one folder per page, the namespace's attachments, and the shared styles and scripts:

   ```text
   index.html
   readme/index.html
   servers/index.html
   networking/index.html
   docker/index.html
   backups/index.html
   monitoring/index.html
   attachments/…
   style.css
   skins.css
   app.js
   …
   ```

4. Serve the unpacked directory over HTTP and open its `index.html` in a browser. Check the layout, links, sidebar and embedded images before publishing. Opening a local `file://` URL may block scripts or search.


5. Upload the unpacked directory to an ordinary static file server or CDN.

## Preview without downloading

Save your settings, then choose **Preview static site** to open the export in a new tab without downloading a ZIP. The preview uses current pages and saved settings. Changes require a new preview.

Only you can access your preview, and you must retain settings access. Previews expire after 15 minutes; generating another for the same namespace replaces the previous one. The instance allows four active previews at a time. If it is full, wait for one to expire.

Previewing does not publish the site or change its settings. Sitemap entries still use the publishing URL. Non-image attachments download rather than open in the preview. Download the ZIP when you are ready to host the site.

## What the export contains

Each page becomes `slug/index.html`, so every page gets its own folder and a stable location. The configured namespace index is also rendered at the root as `index.html`. The export uses the namespace's skin, palette, and ordered page tree, with a read-only page layout rather than the live application's controls.

The first page segment cannot be `robots.txt` or `sitemap.xml`, including case variants, because these names are reserved for root crawler files. This also applies to descendants such as `robots.txt/guide`, even when sitemap generation is disabled. Rename the first segment before exporting; HMD rejects these collisions before writing output. Nested names such as `guide/robots.txt` are allowed.

- **Wiki-links within the namespace** become ordinary relative links. Missing targets and targets outside the exported namespace become plain text.
- **Navigation and bundled assets** use relative paths, so the site can be served at a domain root, under a prefix such as `/hmd/`, or opened locally.
- **Namespace attachments** are copied into `attachments/`, and references using `/_/attachments/{namespace}/` are rewritten to that exported directory. Review attachments even if no current page links to them: the export copies the namespace's attachments, not just the files used by its pages.
- **Ordinary Markdown links and external resources** are not generally rewritten. A link to a live HMD route can still lead to that route; a remote image still needs network access. Prefer wiki-links for links between documentation pages.

The export includes browser-local search of exported page titles and text. Click **Search docs**, or press **Ctrl+K** (**Cmd+K** on macOS). Search works without an HMD server and sends no queries to an external service. It does not search inside attachments or provide the live wiki's search filters.

Hidden pages are not exported. Editing, authentication, page history, backlinks, and health reports require a running HMD instance and are not part of the static site. The exported pages also include code-copy buttons and render Mermaid diagrams when JavaScript is enabled. Reading pages and following ordinary links do not require JavaScript.

This documentation site is generated from HMD itself: its source is the `holdmydocs` namespace in the shared Soollabs Docs repository.

## Export settings and command line

Store export settings in the namespace's `.namespace.yaml`, or edit them in **Namespaces → Edit → static export**:

```yaml
export:
  base_url: https://docs.example.org/manual/
  sitemap: true
  robots_allow: [Googlebot, bingbot, CustomBot]
  links:
    - label: GitHub
      url: https://github.com/soollabs/holdmydocs
      icon: fa-brands fa-github
      location: topbar
      icon_only: true
```

`sitemap.xml` is generated by default, with absolute URLs for exported pages only. The configured index page is listed at the site root rather than duplicated. Set `sitemap: false` to disable generation. When reusing a CLI output directory, this removes an existing `sitemap.xml` and omits its reference from `robots.txt`; a removal failure fails the export. The export URL remains required even when sitemap generation is disabled. Other stale files are not removed, so use a clean directory for publication.

`robots.txt` is always generated and defaults to `User-agent: *` with `Disallow: /`. Select Google, Bing, DuckDuckGo or Apple search bots in the UI, or add custom bot names, to generate specific `Allow: /` groups while other bots remain blocked. An empty `robots_allow` list blocks all bots. These directives are voluntary crawler preferences, not access controls, and not all crawlers respect them. Crawlers only read `/robots.txt` at the domain root: for a subpath export, merge the rules into the host's root file rather than relying on the exported subpath file.

Each external link needs a label and an HTTP(S) URL. Labels appear as text, or as tooltips and accessible names for icons. Links open in a new tab or window.

- **Sidebar:** choose **Text** for centred links, one per line, or **Icons** for a centred row that wraps. All sidebar links share this mode. In YAML or CLI JSON, use the same `icon_only` value for every sidebar link.
- **Before search:** set `location: topbar`. These links are always icon-only.

Icons use free Font Awesome classes such as `fa-brands fa-github` or `fa-solid fa-heart`. Both classes are required. During export or preview generation, HMD downloads the selected SVGs from Font Awesome 6.7.2 and saves them under `export-icons/`, with a local stylesheet and licence notices. Readers need no CDN access. Generation requires access to `raw.githubusercontent.com` and fails if an icon is unavailable; text-only links require no icon downloads.

The CLI inherits namespace settings unless a corresponding flag is explicitly supplied:

```sh
hmd -export-namespace docs -export-dir ./site \
  -export-base-url https://docs.example.org/manual/ \
  -export-sitemap=true \
  -export-robots-allow Googlebot,bingbot \
  -export-links '[{"label":"GitHub","url":"https://github.com/soollabs/holdmydocs","icon":"fa-brands fa-github","location":"topbar","icon_only":true}]'
```

Use `-export-sitemap=false` to disable the sitemap, `-export-robots-allow ''` to clear permitted bots, or `-export-links '[]'` to clear configured links. These overrides do not modify namespace settings. Use `-export-use-main-base-url` to explicitly choose the main HMD URL instead of the namespace export URL; it cannot be combined with `-export-base-url`.

CLI export fails before creating output if neither namespace settings nor flags provide an export base URL. It does not prompt or silently fall back to the main URL. Existing automated exports must supply `export.base_url` or an explicit URL flag when upgrading.

## Publication checklist

Before each release:

1. Export into a clean directory. Do not merge the archive into an older export: deleted pages and attachments could remain publicly accessible.
2. Check the root homepage and a deeply nested page. Follow the site title, sidebar links, wiki-links, and attachment links from both.
3. Check narrow and wide layouts, the on-page outline, code blocks, images, and any Mermaid diagrams. Check that keyboard navigation and link focus work.
4. Preview through a static HTTP server rather than relying on `file://`. For example, from the unpacked directory, with Python installed:

   ```sh
   python3 -m http.server 8000 --bind 127.0.0.1
   ```

   Visit `http://127.0.0.1:8000/`. If publishing under `/hmd/`, also preview at that prefix by serving a parent directory containing the export as `hmd/`.
5. Check for requests to the live application's `/_/` routes and for missing assets in the browser's network panel. Review external links separately.
6. Publish the complete directory, including fonts, scripts, and attachments. Configure the host to serve directory `index.html` files. Keep a copy of the previous export so you can roll back, and replace the published snapshot rather than leaving stale files behind.
7. Recheck the public homepage, a nested page, and an attachment after deployment.

## Common pitfalls

- **The export action is missing.** It only shows for namespaces that already have pages. Create a page first, then export.
- **The static site is a snapshot.** Re-export after editing pages or attachments. The export never follows your live namespace.
- **Links break after you move pages.** The export mirrors the page tree at the moment you export. Re-export after reorganising a namespace.

## Next steps

- [[Reverse Proxies]] for serving HMD itself behind a reverse proxy.
- [[Namespace Configuration Reference]] for the page tree, skin, and palette the export mirrors.
