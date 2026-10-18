---
title: MCP Tool Reference
tags: hmd, reference, mcp
---

Tools on the MCP endpoint (`POST /_/mcp`) and the scope each requires. Your instance's `tools/list` response is authoritative. Setup is on [[MCP Integration]].

## Tools and scopes

Fifteen tools exist. `search_attachments` appears only when document search is enabled (`HMD_DOCUMENT_SEARCH_TIKA_URL` plus a model).

| Tool | Scope | What it does |
| --- | --- | --- |
| `list_pages` | read | Every accessible page with slug, title and tags. |
| `read_page` | read | One page: raw Markdown body, metadata, and its current hash. |
| `save_page` | write | Create or update a page (each changed save is a Git commit). |
| `edit_page` | write | Apply exact-text replacements to an existing page, or preview a diff. |
| `delete_page` | write | Delete a page (still recoverable from Git history). |
| `search` | read | Full-text search of titles, bodies and tags. |
| `backlinks` | read | Pages whose wiki-links target a given page. |
| `recent_changes` | read | Newest accessible commits, newest first. |
| `health` | read | Dangling wiki-links, orphans and stale pages. Optional `namespace` scopes the report. |
| `list_namespaces` | read | Namespaces with description, page count and visibility. |
| `read_namespace` | settings | One namespace's full settings and current hash. |
| `save_namespace` | settings | Create or update namespace settings (a Git commit). |
| `read_attachment` | read | Cached extracted text of one attachment. |
| `upload_attachment` | write | Create a one-use upload URL for a page-owned attachment. |
| `search_attachments` | read | Search extracted attachment text (document search only). |

Page tools take slugs as `namespace/page`; namespace tools take the namespace name. A call beyond the caller's scopes returns an MCP tool error naming the required scope. There is no namespace-deletion tool; delete namespaces in the web UI.

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
- The response contains `slug`, `hash`, `changed` and a unified `diff`.
- With `dryRun: true`, HMD validates and returns the same values without committing; `hash` stays current.
- Limits: 128 replacements per request, the 1 MiB page-body limit, valid UTF-8 only.

## The basehash contract

1. Call `read_page` (or `read_namespace`) and keep its `hash`.
2. Send it as `basehash` with the save or edit.
3. Use the new hash the write returns for the next update.

A stale `basehash` fails with a conflict instead of overwriting another writer. Re-read, merge and retry. Omit `basehash` on `save_page` or `save_namespace` to create; creating something that already exists fails. `edit_page` always needs `basehash` and cannot create pages.

## Namespace restrictions

A token restricted to certain namespaces can only list, read and write pages in them. List tools (`list_pages`, `list_namespaces`, `search`, `backlinks`, `health`, `search_attachments`) filter results to what the caller can access. `read_attachment` and `upload_attachment` apply the restriction through the attachment's page.

`recent_changes` drops any commit that touches a file outside the caller's access, so a mixed commit disappears entirely.

Hidden pages, hidden templates and `.wiki.yaml` are never visible to MCP tools.

## Common pitfalls

- **Repeated conflicts**: you saved with a stale `basehash`. Re-read and retry with the fresh hash.
- **`insufficient_scope`**: the grant lacks the scope. Reconnect and approve it if your HMD permissions allow, or issue a replacement PAT with the scope.
- **`search_attachments` missing**: document search is not enabled on the instance.

Next: [[MCP Integration]].
