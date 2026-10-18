---
title: Static Export
tags: hmd, integrations, publishing
---

Turn a namespace into a self-contained static website you can host anywhere, with no HMD instance behind it.

## Prerequisites

- A namespace with at least one page. The export action only appears then.
- A publishing URL in **Edit → Static site → export base URL**, such as `https://docs.example.org/`. Save it before previewing or exporting. If it is missing, the browser asks before using the main HMD URL for that download or preview, and does not save the fallback.
- Optional: a namespace `index` setting pointing to an existing page, to make it the homepage. Without it, the homepage asks readers to pick a page from the sidebar. See [[Namespace Configuration Reference]].

> The archive is publishable content, not an access-controlled backup. The static host does not inherit HMD accounts or namespace permissions. Review every page and attachment before making it public.

## Export a namespace

1. Open **Namespaces** from the settings menu. Each row shows name, page count, visibility and Edit / Preview / Export actions.

   ![Namespace list with preview and export actions](/_/attachments/holdmydocs/integrations/static-export/namespaces.png)

2. Click **Export static site** next to the namespace. Your browser downloads `{namespace}-export.zip`.
3. Unpack the archive. It holds an `index.html`, one folder per page, the namespace's attachments, and shared styles and scripts:

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

4. Serve the unpacked directory over HTTP and check the layout, links, sidebar and images. A local `file://` URL may block scripts or search.

   ![A static export of a fictional blog, served from a local directory](/_/attachments/holdmydocs/integrations/static-export/preview.png)

5. Upload the directory to a static file server or CDN.

The **Edit → Static site** page controls the publishing URL, sitemap, bot rules and external links:

![Namespace Static site settings](/_/attachments/holdmydocs/integrations/static-export/settings.png)

## Preview without downloading

Save the Static site settings, then choose **Preview** to open a snapshot in a new tab. Generate a new preview after each change.

- Only its creator can open it, and they need `settings` access to the namespace.
- Previews expire after 15 minutes. A new preview for the same namespace replaces your previous one.
- An instance allows four active previews. If it is full, wait for one to expire.
- Previewing does not publish the site or save settings.
- Sitemap entries use the publishing URL. Non-image attachments download instead of opening.

## What the export contains

| Setting | Behaviour |
| --- | --- |
| Sitemap | `sitemap.xml`, enabled by default. Turning it off removes an existing sitemap from reused output. |
| Bots | `robots.txt` blocks all bots by default. Allow a list of named bots, or a single `*` for every bot. `*` cannot be combined with names. |
| Sidebar links | One shared Text or Icons mode. Links placed **Before search** need an icon and are icon-only; the label stays as the accessible name and tooltip. |

- Bot rules are voluntary, not access control, and only work at a domain root. Under a path prefix, merge them into the host's root `robots.txt`.
- Selected Font Awesome 6.7.2 SVG icons are downloaded during generation and bundled with attribution, so no icon CDN is needed when viewing. Generation needs network access only when icons are selected, and fails if an icon cannot be retrieved safely.
- `robots.txt` and `sitemap.xml` are reserved as first page path segments in any letter case, including descendants such as `robots.txt/guide`. HMD rejects these paths before writing the export. Nested names such as `guides/robots.txt` are allowed.
- Other stale files remain in reused output, so publish from a clean directory.

Each page becomes `slug/index.html`. The configured namespace index is also rendered at the root as `index.html`. The export uses the namespace's skin, palette and ordered page tree, with a read-only layout.

- **Wiki-links within the namespace** become relative links. Missing targets and targets outside the namespace become plain text.
- **Navigation and bundled assets** use relative paths, so the site works at a domain root, under a prefix such as `/hmd/`, or locally.
- **Attachments** are all copied into `attachments/`, and `/_/attachments/{namespace}/` references are rewritten to match. This includes files no page links to, so review them all.
- **Ordinary Markdown links and external resources** are not generally rewritten. A link to a live HMD route still points to that route, and a remote image still needs network access. Prefer wiki-links between documentation pages.
- **Search** is browser-local over page titles and text. Click **Search docs** or press **Ctrl+K** (**Cmd+K** on macOS). It needs no server, sends no queries anywhere, and does not search attachments or offer the live wiki's filters.
- **Not exported:** hidden pages, editing, authentication, page history, backlinks and health reports.
- **JavaScript** adds code-copy buttons and Mermaid diagrams. Reading pages and following links work without it.

## Command-line export

The CLI uses the configured content repository and inherits the namespace's export settings. Flags override them for this export without changing `.namespace.yaml`:

```sh
hmd -export-namespace holdmydocs -export-dir ./site \
  -export-base-url https://docs.example.org/manual/ \
  -export-sitemap=true \
  -export-robots-allow Googlebot,bingbot \
  -export-links '[{"label":"GitHub","url":"https://github.com/soollabs/holdmydocs","icon":"fa-brands fa-github","location":"topbar","icon_only":true}]'
```

- Disable the sitemap with `-export-sitemap=false`.
- Clear permitted bots with `-export-robots-allow ''`.
- Clear external links with `-export-links '[]'`.

A publishing URL is required even with the sitemap disabled. If neither namespace settings nor flags provide one, the export fails before creating output; it does not prompt or fall back to the main HMD URL. Pass `-export-use-main-base-url` to use `server.base_url` explicitly. It cannot be combined with `-export-base-url`.

## Publication checklist

1. Export into a clean directory. Never merge into an older export: deleted pages and attachments could stay public.
2. Check the root homepage and a deeply nested page. Follow the site title, sidebar links, wiki-links and attachment links from both.
3. Check narrow and wide layouts, the outline, code blocks, images, Mermaid diagrams, keyboard navigation and link focus.
4. Preview over HTTP, not `file://`. From the unpacked directory:

   ```sh
   python3 -m http.server 8000 --bind 127.0.0.1
   ```

   Open `http://127.0.0.1:8000/`. If publishing under `/hmd/`, also preview at that prefix by serving a parent directory containing the export as `hmd/`.
5. In the browser's network panel, check for requests to the live application's `/_/` routes and for missing assets. Review external links separately.
6. Publish the complete directory, including fonts, scripts and attachments. Configure the host to serve directory `index.html` files. Keep the previous export for rollback and replace the published snapshot rather than leaving stale files.
7. Recheck the public homepage, a nested page and an attachment.

## Common pitfalls

- **No export action.** The namespace has no pages yet. Create one first.
- **Stale site.** The export is a snapshot. Re-export after editing pages or attachments, or after moving pages.

## Next steps

- [[Reverse Proxies]] for serving HMD itself behind a reverse proxy.
- [[Namespace Configuration Reference]] for the page tree, skin, and palette the export mirrors.
