---
title: Links And Navigation
tags: hmd, writing
---

Link pages together with wiki-links, follow backlinks, and find pages with search.

## Markdown links vs wiki-links

Use a standard Markdown link when you want custom link text or an external destination:

```markdown
See [the HMD website](https://example.com) for details.
```

Link another HMD page with a title-only wiki-link:

```markdown
See [[Pages]] for details.
```

Wiki-links resolve by exact page title, preferring a match in the current namespace and falling back to other namespaces. They do not support a pipe alias: `[[Backups|backup]]` targets a page whose title is literally `backups-backup`, so use a Markdown link when you need different link text.

A wiki-link to a page that does not exist yet renders with a trailing `+` and opens the create flow, so a red link becomes a new page in one click. Links inside fenced code blocks are never treated as wiki-links.

The rendered page shows wiki-links and, below the content, the backlinks widget listing every page that links to the current one:


## Table of contents

Insert `<!-- hmd:toc -->` anywhere in a page to generate a bullet list of every page in the current namespace, sorted by title. The namespace's own index page is excluded.

Add tags after the colon to include only pages matching any listed tag:

```markdown
<!-- hmd:toc:operations,git -->
```

The table of contents is namespace-scoped: it never lists pages from another namespace.

## Search

Press `ctrl-k` (`cmd-k` on macOS), or press `/`, to open the command palette. Type to search pages and attachments, press `>` for verbs such as `>new` and `>ns`, or choose the **create** row to start a new page from your query.

The full search page lives at `/_/search?q=...`:

![Search in a fictional homelab wiki](/_/attachments/holdmydocs/writing/links-and-navigation/search.png)

## Common pitfalls

- Wiki-links have no pipe alias and no custom text. For different link text, use a Markdown link.
- A wiki-link only links within the wiki. External URLs need `[text](https://...)` Markdown links.
- The `<!-- hmd:toc -->` token must be exactly as written; it is replaced at render time and never appears on the page.

## Next steps

[[Pages]], [[Markdown And The Editor]], [[Namespace Configuration Reference]].
