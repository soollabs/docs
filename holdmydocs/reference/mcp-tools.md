---
title: MCP Tool Reference
tags: hmd, reference, mcp
---

This page lists tools on the MCP endpoint (`POST /_/mcp`) and the scope each one requires. Check your instance's `tools/list` response for the available tools. Connection setup and the write flow are on [[MCP Integration]].

## Tools and scopes

The current application exposes fifteen tools. Fourteen are always present; `search_attachments` appears only when document search is enabled (`HMD_TIKA_URL` plus a model).

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
| `health` | read | Hygiene report: dangling wiki-links, orphans and stale pages. |
| `list_namespaces` | read | Namespaces with description, page count and visibility. |
| `read_namespace` | settings | One namespace's full settings and current hash. |
| `save_namespace` | settings | Create or update namespace settings (a Git commit). |
| `read_attachment` | read | Cached extracted text of one attachment. |
| `upload_attachment` | write | Create a one-use upload URL for a page-owned attachment. |
| `search_attachments` | read | Search extracted attachment text (document search only). |

Page tools take slugs in `namespace/page` form; namespace tools take the namespace name. `read_attachment` and `upload_attachment` apply the same namespace restriction through the attachment's owning page. `health` optionally takes a `namespace` to scope the report.

## Edit a page

`edit_page` applies one or more exact-text replacements to an existing page's Markdown body while preserving its title, tags and pin. It requires `slug`, `basehash`, a non-empty `edits` array, and optional `dryRun`.

```json
{
  "slug": "notes/example",
  "basehash": "<hash returned by read_page or the previous edit/save>",
  "edits": [{"oldText": "exact existing Markdown", "newText": "replacement Markdown"}],
  "dryRun": false
}
```

Edits run in order. At each step, `oldText` must occur exactly once in the current body; a missing or ambiguous match fails the whole request without a write. `newText` may be empty to delete matching text.

The final body is validated and written with the original `basehash` in one atomic commit. A stale hash fails without modifying the page, and a no-op makes no commit. The response contains `slug`, `hash`, `changed`, and a unified `diff`. With `dryRun: true`, HMD validates and returns those values without committing; `hash` remains current.

The tool limits a request to 128 replacements and the normal 1 MiB page-body limit. It accepts only valid UTF-8 text.

## How scopes map to tools

- **read** — `list_pages`, `read_page`, `search`, `backlinks`, `recent_changes`, `health`, `list_namespaces`, `read_attachment`, and `search_attachments` (when document search is enabled).
- **write** — `save_page`, `edit_page`, `delete_page`, `upload_attachment`.
- **settings** — `read_namespace`, `save_namespace`.

A tool call beyond the caller's scopes fails with a message like `forbidden: write scope required`. There is no namespace-deletion tool: a namespace is removed from the web UI, not by an agent.

## The basehash contract

Every read that returns a hash is an optimistic-lock handshake:

1. `read_page` (or `read_namespace`) first, and keep its `hash`.
2. Send that hash as `basehash` with the save or edit.
3. Each successful save or edit returns the hash for the next update.

A write with a stale `basehash` fails with a conflict instead of overwriting another writer's changes. On conflict, re-read, merge, and retry with the fresh hash. Omit `basehash` from `save_page` or `save_namespace` to create a page or namespace configuration — creating one that already exists also fails. `edit_page` always requires `basehash` and cannot create pages.

## Namespace restrictions

A token restricted to particular namespaces can only list, read, and write pages in those namespaces. `recent_changes` omits any commit that touches a file outside the caller's access — a commit is all-or-nothing, so a mixed commit disappears entirely. The other list tools (`list_pages`, `list_namespaces`, `search`, `backlinks`, `health`, `search_attachments`) filter results to what the caller can access.

Hidden pages, hidden templates, and `.wiki.yaml` are never visible to MCP tools. Attachments are reachable only through a page the caller can access.

## Common pitfalls

- **Writes keep failing with a conflict** — you saved with a stale `basehash`. Re-read the page or namespace and retry with the fresh hash.
- **`forbidden: write scope required`** — the token has read access only. Issue a token with the write scope for agent write workflows.
- **`search_attachments` is missing from the tool list** — document search is not enabled on the instance, so the tool is not registered.

Next: [[MCP Integration]].
