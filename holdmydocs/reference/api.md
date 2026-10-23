---
title: API Reference
tags: hmd, reference, api
---

The `/_/api/*` endpoints let scripts and agents read and write the wiki with the same scope and namespace restrictions as a login session. Most return JSON; Markdown preview returns HTML.

## Authentication

Send a personal access token (PAT) as a Bearer credential. Create tokens in **Settings** (see [[Personal Access Tokens]]). A session cookie also works, but scripts should use the header.

```sh
curl -s -H "Authorization: Bearer hmd_your_token" \
  "https://wiki.example.com/_/api/health"
```

- A missing, malformed or expired token returns **401** with `{"error":"unauthorized"}`, never a login redirect.
- A token without the required scope returns **403** with `{"error":"<scope>"}`, for example `{"error":"write"}`.
- A token restricted to namespaces only sees results from those namespaces; endpoints filter rather than error.

## Endpoints

| Endpoint | Method | Scope | Purpose |
| --- | --- | --- | --- |
| `/_/api/search` | GET | read | Full-text search. |
| `/_/api/search/attachments` | GET | read | Attachment search (document search enabled only). |
| `/_/api/health` | GET | read | Wiki hygiene report. |
| `/_/api/sync` | GET | read | Sync status. |
| `/_/api/sync/push-now` | POST | write | Push to the remote immediately. |
| `/_/api/pages/{slug...}` | POST | write | Create or save a page. |
| `/_/api/pages/delete/{slug...}` | POST | write | Delete a page. |
| `/_/api/pages/rename/{slug...}` | POST | write | Rename a page. |
| `/_/api/pages/tags/{slug...}` | POST | write | Change page tags. |
| `/_/api/pages/revert/{slug...}` | POST | write | Restore an earlier revision. |
| `/_/api/namespaces` | POST | admin | Save a namespace configuration. |
| `/_/api/namespaces/reset` | POST | admin | Restore namespace defaults. |
| `/_/api/namespaces/delete` | POST | admin | Delete a namespace and every file beneath it. |
| `/_/api/settings/*` | POST | varies | Save settings, users and tokens (see [[Route Reference]]). |
| `/_/api/setup` | POST | admin | Complete first-run setup. |
| `/_/api/preview/{slug...}` | GET | read | Page title, snippet, tags and age. |
| `/_/api/preview` | POST | write | Render Markdown to HTML. |
| `/_/api/attachments/{slug...}` | POST | write | Upload an attachment. |
| `/_/api/attachment-uploads/{token}` | POST | none | One-use upload URL (MCP only). |

## Search

`GET /_/api/search?q=QUERY` searches titles, bodies and tags, using the same syntax as `/_/search`. Results are limited to pages the token can read. Snippets are HTML-escaped text with `<mark>` around matches.

```json
[
  {
    "slug": "homelab/docker",
    "title": "Docker",
    "snippet": "… <mark>Docker</mark>\n\nAll containers run on `proxmox-1` …",
    "tags": ["homelab", "docker"]
  }
]
```

## Attachment search

`GET /_/api/search/attachments?q=QUERY` searches the extracted text of attachments. It exists only when document search is enabled (`HMD_DOCUMENT_SEARCH_TIKA_URL` plus a model); otherwise it returns 404.

```json
[
  {
    "owner_slug": "homelab/backups",
    "filename": "restic-check.pdf",
    "url": "/_/attachments/homelab/backups/restic-check.pdf",
    "excerpt": "… <mark>restic</mark> check output …",
    "score": 2.43
  }
]
```

## Health

`GET /_/api/health` reports dangling wiki-links, orphan pages and pages unchanged for at least 180 days. Add `?namespace=NAME` to scope it to one namespace.

```json
{
  "missing": [
    {
      "slug": "homelab/readme",
      "sources": ["homelab/readme"]
    }
  ],
  "orphans": ["homelab/servers"],
  "stale": []
}
```

- `missing`: link targets that do not exist, with the pages that link to them.
- `orphans`: pages nothing links to.
- `stale`: entries with `slug` and `last_updated`.

## Sync

`GET /_/api/sync` returns the sync state. `state` is `ok`, `pending`, `failed` or `no remote`. In bidirectional mode with a remote, the response also lists pages changed by the fetch and the fetched commits.

```json
{
  "state": "ok",
  "detail": "",
  "at": "15:21",
  "last_success_unix": 1786801361
}
```

`POST /_/api/sync/push-now` pushes immediately instead of waiting for the next poll:

```sh
curl -s -X POST -H "Authorization: Bearer hmd_your_token" \
  "https://wiki.example.com/_/api/sync/push-now"
```

```json
{
  "ok": true,
  "state": "ok",
  "detail": "",
  "last_success_unix": 1786801361
}
```

## Page preview

`GET /_/api/preview/{slug...}` returns the title, a snippet of the first 40 words, tags and a human-readable age. A missing page returns 404 with a plain-text body.

```json
{
  "title": "Home Lab",
  "snippet": "# Home Lab The home lab runs my services on three quiet machines …",
  "tags": ["homelab", "index"],
  "age": "2 hours ago"
}
```

## Markdown preview

`POST /_/api/preview` renders the request body to HTML. Pass `?slug=namespace/page` so wiki-links resolve in the right namespace. Raw HTML from trusted editors is not sanitised, so do not embed the response in an untrusted origin.

```sh
curl -s -X POST -H "Authorization: Bearer hmd_your_token" \
  -H "Content-Type: text/markdown" \
  --data-binary "See the [[Docker]] page." \
  "https://wiki.example.com/_/api/preview?slug=homelab"
```

## Upload an attachment

`POST /_/api/attachments/{slug...}` uploads one file as multipart field `file` and commits it to the page's namespace:

```sh
curl -s -X POST -H "Authorization: Bearer hmd_your_token" \
  -F "file=@report.pdf" \
  "https://wiki.example.com/_/api/attachments/homelab/backups"
```

```json
{
  "url": "/_/attachments/homelab/backups/report.pdf",
  "indexed": false
}
```

- `url` is the serve path, ready to embed as `[name](/…/report.pdf)` or `![alt](/…/report.pdf)`.
- `indexed` is true only when document search is enabled and extraction succeeded.
- Status is 200 by default, 201 when document search is enabled (check `indexed` for extraction), and 202 when the commit succeeded but the index could not be rebuilt. The file is safe to use in every case.

## One-use upload URL

`POST /_/api/attachment-uploads/{token}` receives the file for the MCP `upload_attachment` tool, which returns the one-use `upload_url`. It needs no `Authorization` header. The token expires after 10 minutes or first use; unknown, expired and used tokens return 404.

## Common pitfalls

- **401:** the token is missing, malformed or expired. Check the header and create a fresh token in Settings.
- **403:** the token lacks the scope the route needs. Add it when creating the token.
- **404 on `/_/api/search/attachments`:** document search is not enabled.
- **Unstyled wiki-links in previews:** pass `?slug=namespace/page`.

Next: [[MCP Tool Reference]].
