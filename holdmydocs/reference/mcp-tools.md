---
title: MCP Tool Reference
tags: hmd, reference, mcp
---

Tools on the MCP endpoint (`POST /_/mcp`) and the scope each requires. Your instance's `tools/list` response is authoritative: each tool's schema carries its limits and allowed values, and its annotations mark it read-only or destructive. Setup is on [[MCP Integration]].

The endpoint speaks MCP `2026-07-28` and the older `2025-11-25`, `2025-06-18` and `2025-03-26` versions.

## Tools and scopes

Each tool needs one token scope. **Read-only** tools change nothing; **destructive** tools can replace or remove existing content; **writes** only adds.

<!-- generated:mcp-tools -->

| Tool | Scope | Effect | What it does |
| --- | --- | --- | --- |
| `backlinks` | read | read-only | List accessible pages whose `[[wiki-links]]` point at a page. |
| `delete_page` | write | destructive | Delete a page in one Git commit; it stays recoverable from history. Pass basehash to delete only the revision you read. |
| `move_page` | write | destructive | Move a page to a new slug in one Git commit, keeping its title, tags, pin, history and attachments. The destination namespace must exist and new_slug must not hold a page. A namespace index page cannot be moved. Wiki-links to the page are not rewritten; check backlinks first. A conflict error returns the current hash: re-read and retry. |
| `rename_page` | write | destructive | Change a page's title and its slug to match, in place, and rewrite wiki-links to it in other pages. A namespace index page keeps its slug. The rename is one commit; each page whose links are rewritten is its own commit, and failed_links lists pages that could not be updated. A conflict error returns the current hash: re-read and retry. |
| `edit_page` | write | destructive | Replace exact text in an existing page's Markdown body without resending it; title, tags and pin are kept. Each oldText must match exactly once when its edit is applied, and any failed edit cancels the whole call. All edits land in one commit; dryRun returns the diff without committing. A conflict error returns the current hash: re-read and retry. |
| `health` | read | read-only | Report dangling `[[wiki-links]]` whose target page is missing, orphan pages with no incoming links, and stale pages with no commit in 180 days. |
| `list_namespaces` | read | read-only | List accessible namespaces with their description, page count and whether anonymous visitors can read them. Use read_namespace for full settings. |
| `list_pages` | read | read-only | List accessible pages with their slug, title and tags, sorted by slug. When more is true, pass next_offset as offset for the next pages. Use search to find pages by content. |
| `read_attachment` | read | read-only | Read the text extracted from an attachment, in windows of characters. When truncated is true, call again with offset set to next_offset. Use search_attachments to find the relevant part of a large document first. |
| `read_namespace` | admin | read-only | Read a namespace's full settings and hash. Pass the hash as basehash to save_namespace. |
| `read_page` | read | read-only | Read one page: its Markdown body, title, tags, pin state and hash. Pass the hash as basehash to edit_page, save_page or delete_page. A long body comes in windows: when truncated is true, call again with offset set to next_offset, or name a section to read only that part. After a partial read, change the body with edit_page, not save_page. |
| `recent_changes` | read | read-only | List the newest wiki commits first, with author, time and changed files. A commit that touches any file outside your namespace access is left out. |
| `save_namespace` | admin | destructive | Create a namespace's settings, or update them with the basehash from read_namespace. Each save is one Git commit and never changes pages. On update, fields you omit keep their current values; lists and objects replace the stored value whole. A conflict error returns the current hash: re-read and retry. |
| `save_page` | write | destructive | Create a page, or update one with the basehash from read_page. Each save is one Git commit. On update, fields you omit keep their current values; body and tags replace the stored value whole. Prefer edit_page to change part of a body. A conflict error returns the current hash and body: merge and retry with that hash. |
| `search` | read | read-only | Full-text search over accessible page titles, bodies and tags, best match first. Snippets are escaped HTML with &lt;mark&gt; around matches; use read_page for the whole page. When more is true, pass next_offset as offset for the next hits, or narrow the query or namespace. |
| `search_attachments` | read | read-only | Search the text extracted from accessible attachments by keyword and meaning, best match first. Excerpts are escaped HTML with &lt;mark&gt; around matches; use read_attachment for more of a document. Listed only when document search is enabled. |
| `upload_attachment` | write | writes | Get a one-use URL for uploading a document or image to a page, then POST the file to it as the multipart field file. Link the upload from the page with edit_page using the returned attachment_url, as `[name](attachment_url)` or `![alt text](attachment_url)` for an image. Supported documents are indexed for search_attachments when document search is on. |

<!-- /generated:mcp-tools -->

Page tools take a `slug` in `namespace/page` form; namespace tools take the namespace name. No segment may start with `_` or `.`, and an invalid slug fails with an error that names the problem. A call beyond the caller's scopes returns an MCP tool error naming the required scope. There is no namespace-deletion tool; delete namespaces in the web UI.

## Edit a page

`edit_page` applies exact-text replacements to an existing page's body and keeps its title, tags and pin. It needs `slug`, `basehash` and a non-empty `edits` array; `dryRun` is optional.

```json
{
  "slug": "notes/example",
  "basehash": "<hash returned by read_page or the previous edit/save>",
  "edits": [{"oldText": "exact existing Markdown", "newText": "replacement Markdown"}],
  "dryRun": false
}
```

- Edits run in order. `oldText` must occur exactly once in the current body at that step, or the whole request fails without a write.
- `newText` may be empty to delete text.
- The result is one atomic commit. A stale hash fails, and a no-op makes no commit.
- The response contains `slug`, `hash`, `changed` and a unified `diff` of the changed lines with a little context.
- With `dryRun: true`, HMD validates and returns the same values without committing; `hash` stays current.
- The page body must stay valid UTF-8 and at most 1 MiB. The number of edits per call is in the `edit_page` parameters below.

## The basehash contract

1. Call `read_page` (or `read_namespace`) and keep its `hash`.
2. Send it as `basehash` with the save or edit.
3. Use the new hash the write returns for the next update.

A stale `basehash` fails with a conflict instead of overwriting another writer. The error is a JSON object with the current `hash`, empty when the target no longer exists; a `save_page` conflict also carries the current `body`. Re-read, merge and retry. Omit `basehash` on `save_page` or `save_namespace` to create; creating something that already exists fails. `edit_page` always needs `basehash` and cannot create pages. `delete_page` accepts an optional `basehash` and then deletes only that revision.

## Updates keep what you leave out

On an update, `save_page` and `save_namespace` change only the fields you send. To retag a page, send `slug`, `basehash` and `tags`; the body, title and pin stay as they are. A list or object you send replaces the stored one whole, so send the complete `tags`, `widgets` or `tree`. An empty string clears a text field, and on `save_namespace` an empty `new` object removes the new-page template. Creating a page needs a `body`.

## Large results

Lists come in pages. `list_pages` and `search` return `more` and `next_offset`: when `more` is true, call again with `offset` set to `next_offset`. Narrowing the query or the namespace is often better than paging. `search` can return fewer hits than `limit` while `more` is true, because it drops matches the caller cannot read.

Long text comes in windows. `read_page` and `read_attachment` return up to `limit` characters from `offset` with `next_offset`, `total_chars` and `truncated`. When `truncated` is true, call again with `offset` set to `next_offset`. An offset past the end is an error.

`read_page` can also return one section: pass the heading text as `section`, and the result holds that heading and everything under it, up to the next heading of the same or a higher level. Matching ignores case. An unknown section fails with a list of the page's headings. `offset` and `limit` then count within the section.

The `hash` from a partial read is still the whole page's. Change the page with `edit_page` after a partial read; `save_page` with a `body` replaces the whole body, including the parts you did not read.

## Namespace restrictions

A token restricted to certain namespaces can only list, read and write pages in them. List tools (`list_pages`, `list_namespaces`, `search`, `backlinks`, `health`, `search_attachments`) filter results to what the caller can access. `read_attachment` and `upload_attachment` apply the restriction through the attachment's page.

`recent_changes` drops any commit that touches a file outside the caller's access, so a mixed commit disappears entirely.

Hidden pages, hidden templates and `.wiki.yaml` are never visible to MCP tools.

## Tool parameters

Generated from `internal/mcp/schema/tools.json` in the pinned HMD release, the same definitions served by `tools/list`. Parameter defaults are the values used by the handlers when a parameter is omitted.

<!-- generated:mcp-parameters -->

### `backlinks`

| Parameter | Type | Required | Accepted values | Description |
| --- | --- | --- | --- | --- |
| `slug` | string | Yes | — | page identifier in namespace/page form, e.g. notes/my-page; no segment may start with _ or . |

### `delete_page`

| Parameter | Type | Required | Accepted values | Description |
| --- | --- | --- | --- | --- |
| `slug` | string | Yes | — | page identifier in namespace/page form, e.g. notes/my-page; no segment may start with _ or . |
| `basehash` | string | No | — | hash from read_page; when set, the page is deleted only if it is still that revision |

### `move_page`

| Parameter | Type | Required | Accepted values | Description |
| --- | --- | --- | --- | --- |
| `slug` | string | Yes | — | page identifier in namespace/page form, e.g. notes/my-page; no segment may start with _ or . |
| `new_slug` | string | Yes | — | destination page identifier in namespace/page form |
| `basehash` | string | Yes | — | hash from read_page; the page moves only if it is still that revision |

### `rename_page`

| Parameter | Type | Required | Accepted values | Description |
| --- | --- | --- | --- | --- |
| `slug` | string | Yes | — | page identifier in namespace/page form, e.g. notes/my-page; no segment may start with _ or . |
| `title` | string | Yes | — | new title; the new slug is derived from it |
| `basehash` | string | Yes | — | hash from read_page; the page is renamed only if it is still that revision |

### `edit_page`

| Parameter | Type | Required | Accepted values | Description |
| --- | --- | --- | --- | --- |
| `slug` | string | Yes | — | page identifier in namespace/page form, e.g. notes/my-page; no segment may start with _ or . |
| `basehash` | string | Yes | — | hash from read_page or the last save or edit |
| `edits` | array | Yes | minimum items: `1`; maximum items: `128`; items: object; item `oldText`: minimum length: `1`; item `newText`: —; required item fields: oldText, newText | replacements, applied in order |
| `dryRun` | boolean | No | — | return the diff without committing |

### `health`

| Parameter | Type | Required | Accepted values | Description |
| --- | --- | --- | --- | --- |
| `namespace` | string | No | — | limit the report to this namespace; omit for the whole wiki |

### `list_namespaces`

No parameters.

### `list_pages`

| Parameter | Type | Required | Accepted values | Description |
| --- | --- | --- | --- | --- |
| `namespace` | string | No | — | only list pages in this namespace |
| `offset` | integer | No | minimum: `0` | number of pages to skip; pass next_offset from the previous call |
| `limit` | integer | No | minimum: `1`; maximum: `500`; default: `100` | maximum pages to return |

### `read_attachment`

| Parameter | Type | Required | Accepted values | Description |
| --- | --- | --- | --- | --- |
| `slug` | string | Yes | — | page that owns the attachment, in namespace/page form, e.g. notes/my-page; no segment may start with _ or . |
| `filename` | string | Yes | — | attachment filename without a directory |
| `offset` | integer | No | minimum: `0` | first character to return |
| `limit` | integer | No | minimum: `1`; maximum: `100000`; default: `40000` | maximum characters to return |

### `read_namespace`

| Parameter | Type | Required | Accepted values | Description |
| --- | --- | --- | --- | --- |
| `name` | string | Yes | — | namespace name, e.g. notes; not a page slug, and it may not start with _ or . |

### `read_page`

| Parameter | Type | Required | Accepted values | Description |
| --- | --- | --- | --- | --- |
| `slug` | string | Yes | — | page identifier in namespace/page form, e.g. notes/my-page; no segment may start with _ or . |
| `section` | string | No | — | heading text; return only that heading and the text under it, up to the next heading of the same or a higher level |
| `offset` | integer | No | minimum: `0` | first character of the body to return |
| `limit` | integer | No | minimum: `1`; maximum: `100000`; default: `40000` | maximum body characters to return |

### `recent_changes`

| Parameter | Type | Required | Accepted values | Description |
| --- | --- | --- | --- | --- |
| `limit` | integer | No | minimum: `1`; maximum: `200`; default: `20` | maximum commits to return |

### `save_namespace`

| Parameter | Type | Required | Accepted values | Description |
| --- | --- | --- | --- | --- |
| `name` | string | Yes | — | namespace name, e.g. notes; not a page slug, and it may not start with _ or . |
| `basehash` | string | No | — | hash from read_namespace; required to update, omit to create |
| `public` | boolean | No | — | whether anonymous visitors can read the namespace |
| `title` | string | No | maximum length: `256` | human-readable namespace title |
| `description` | string | No | maximum length: `255` | brief namespace description |
| `image` | string | No | — | link preview image for pages without their own, as page/filename of a PNG or JPEG attachment in this namespace, e.g. index/hero.png |
| `skin` | string | No | `""`, `"bare"`, `"phosphor"`, `"newsprint"`, `"journal"`, `"soft"` | skin shown to visitors; empty for the default |
| `palette` | string | No | `""`, `"neutral"`, `"phosphor"`, `"dracula"`, `"everforest"`, `"flexoki"`, `"gruvbox"`, `"nord"`, `"rosé pine"`, `"solarized"`, `"tokyo night"` | colour palette shown to visitors; empty for the skin's own |
| `index` | string | No | — | one-segment page name used as the namespace index |
| `widgets` | array | No | items: string; `"pages"`, `"namespaces"`, `"pinned"`, `"tags"`, `"log"`, `"health"`, `"calendar"`, `"writing-stats"`, `"page-meta"`, `"backlinks"`, `"prev-entries"` | complete ordered widget list; empty for the default set |
| `tree` | array | No | items: string | complete ordered list of page or folder paths for the page tree |
| `new` | object | No | fields: `template`, `slug` | new-page template; set both fields empty to remove it |
| `export` | object | No | fields: `base_url`, `sitemap`, `robots_allow`, `links` | static export settings; an empty object removes them |

### `save_page`

| Parameter | Type | Required | Accepted values | Description |
| --- | --- | --- | --- | --- |
| `slug` | string | Yes | — | page identifier in namespace/page form, e.g. notes/my-page; no segment may start with _ or . |
| `basehash` | string | No | — | hash from read_page; required to update, omit to create |
| `body` | string | No | maximum length: `1048576` | complete Markdown body without frontmatter, at most 1 MiB as UTF-8; required to create, omit to keep the current body |
| `title` | string | No | maximum length: `256` | page title; defaults to the slug on create, omit to keep the current title |
| `tags` | array | No | maximum items: `32`; items: string; maximum length: `64` | complete tag list; replaces the current tags, omit to keep them |
| `pin` | boolean | No | — | show the page in the pinned sidebar widget; omit to keep the current value |

### `search`

| Parameter | Type | Required | Accepted values | Description |
| --- | --- | --- | --- | --- |
| `query` | string | Yes | minimum length: `1` | full-text query for page titles, bodies and tags |
| `namespace` | string | No | — | only search pages in this namespace |
| `offset` | integer | No | minimum: `0`; maximum: `1000` | number of best matches to skip; pass next_offset from the previous call |
| `limit` | integer | No | minimum: `1`; maximum: `50`; default: `20` | maximum hits to return |

### `search_attachments`

| Parameter | Type | Required | Accepted values | Description |
| --- | --- | --- | --- | --- |
| `query` | string | Yes | minimum length: `1` | keyword or semantic query for extracted attachment text |
| `namespace` | string | No | — | only search attachments of pages in this namespace |
| `limit` | integer | No | minimum: `1`; maximum: `50`; default: `20` | maximum hits to return |

### `upload_attachment`

| Parameter | Type | Required | Accepted values | Description |
| --- | --- | --- | --- | --- |
| `slug` | string | Yes | — | page that owns the attachment, in namespace/page form, e.g. notes/my-page; no segment may start with _ or . |
| `filename` | string | Yes | — | original filename without a directory |

<!-- /generated:mcp-parameters -->

## Common pitfalls

- **Repeated conflicts**: you saved with a stale `basehash`. Re-read and retry with the fresh hash.
- **`insufficient_scope`**: the grant lacks the scope. Reconnect and approve it if your HMD permissions allow, or issue a replacement PAT with the scope.
- **`search_attachments` missing**: document search is not enabled on the instance.

Next: [[MCP Integration]].
