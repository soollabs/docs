---
title: API Reference
tags: hmd, reference, api
---

The `/_/api/*` endpoints let scripts, dashboards, and agents read and write the wiki, using the same scope and namespace restrictions as a login session. Most endpoints return JSON; Markdown preview returns HTML.

## Authentication

Use a personal access token (PAT) as a Bearer credential for scripts. The one-use attachment upload URL uses its own capability token:

```sh
curl -s -H "Authorization: Bearer hmd_your_token" \
  "https://wiki.example.com/_/api/health"
```

- A missing, malformed, or expired token returns **HTTP 401** with a JSON body, never a login redirect: `{"error":"unauthorized"}`.
- A token without the required scope returns **HTTP 403** with `{"error":"<scope>"}`, for example `{"error":"write"}`.
- A token restricted to particular namespaces can only reach results for those namespaces; the endpoints filter results rather than erroring.

Create tokens in **Settings** (see [[Personal Access Tokens]]). A logged-in session cookie also authenticates `/_/api/*`, but the `Authorization` header is the reliable choice for scripts and agents — it is explicit and does not depend on a browser session.

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
| `/_/api/namespaces` | POST | settings | Save a namespace configuration. |
| `/_/api/namespaces/reset` | POST | settings | Restore namespace defaults. |
| `/_/api/namespaces/delete` | POST | settings | Delete a namespace. |
| `/_/api/namespaces/delete-all` | POST | settings | Delete all namespaces. |
| `/_/api/settings/*` | POST | varies | Save settings, users and tokens (see [[Route Reference]]). |
| `/_/api/setup` | POST | settings | Complete first-run setup. |
| `/_/api/preview/{slug...}` | GET | read | Page title, snippet, tags and age. |
| `/_/api/preview` | POST | write | Render Markdown to HTML. |
| `/_/api/attachments/{slug...}` | POST | write | Upload an attachment. |
| `/_/api/attachment-uploads/{token}` | POST | none | One-use upload URL (MCP only). |

## Search

`GET /_/api/search?q=QUERY` searches page titles, bodies and tags. The query is the same syntax as `/_/search`, including `mark` highlighting in snippets.

```sh
curl -s -H "Authorization: Bearer hmd_your_token" \
  "https://wiki.example.com/_/api/search?q=docker"
```

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

Snippets are HTML-escaped text containing `<mark>` tags around matches, so render them with escaping enabled. Results are limited to pages the token can read.

## Attachment search

`GET /_/api/search/attachments?q=QUERY` searches the extracted text of attachments. The route is registered only when document search is enabled (`HMD_TIKA_URL` plus a model); on an instance without it the path returns 404. Each hit carries the owning page, filename, URL, an escaped excerpt, and a relevance score:

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

`GET /_/api/health` reports dangling wiki-links, orphan pages and pages unchanged for at least 180 days. An optional `?namespace=NAME` scopes the report to one namespace.

```sh
curl -s -H "Authorization: Bearer hmd_your_token" \
  "https://wiki.example.com/_/api/health"
```

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

`missing` lists wiki-link targets that do not exist, with the pages that link to them; `orphans` are pages nothing links to. `stale` entries include `slug` and `last_updated`. An empty report has all three arrays empty.

## Sync

`GET /_/api/sync` returns the current sync state:

```json
{
  "state": "ok",
  "detail": "",
  "at": "15:21",
  "last_success_unix": 1786801361
}
```

`state` is one of `ok`, `pending`, `failed`, or `no remote`. In bidirectional sync mode with a configured remote, the response also lists the pages changed by the fetch and the fetched commits.

`POST /_/api/sync/push-now` triggers a push immediately instead of waiting for the next poll:

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

`GET /_/api/preview/{slug...}` returns one page's title, a snippet of the first 40 words, tags, and a human-readable age:

```sh
curl -s -H "Authorization: Bearer hmd_your_token" \
  "https://wiki.example.com/_/api/preview/homelab/readme"
```

```json
{
  "title": "Home Lab",
  "snippet": "# Home Lab The home lab runs my services on three quiet machines …",
  "tags": ["homelab", "index"],
  "age": "2 hours ago"
}
```

A missing page returns 404 with a plain-text body.

## Markdown preview

`POST /_/api/preview` renders Markdown to HTML. Raw HTML written by trusted editors is not sanitised: do not embed this response in an untrusted origin. Send the Markdown as the request body, with `?slug=namespace/page` when the body contains wiki-links so they resolve inside the right namespace:

```sh
curl -s -X POST -H "Authorization: Bearer hmd_your_token" \
  -H "Content-Type: text/markdown" \
  --data-binary "See the [[Docker]] page." \
  "https://wiki.example.com/_/api/preview?slug=homelab"
```

```html
<p>See the <a class="wiki" href="/homelab/docker">…</a> page.</p>
```

## Upload an attachment

`POST /_/api/attachments/{slug...}` uploads one file as multipart form field `file` and commits it to the page's namespace:

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

`url` is the attachment's serve path, ready to embed as `[name](/…/report.pdf)` or `![alt](/…/report.pdf)`. `indexed` is true only when document search is enabled and the extraction succeeded. The response is 200 by default, 201 when the file was indexed, and 202 if the commit succeeded but the disposable index could not be rebuilt — the file is safe to use either way. A 201 means document search is enabled, not necessarily that extraction succeeded; check `indexed` for that.

## One-use upload URL

`POST /_/api/attachment-uploads/{token}` is the second half of the MCP `upload_attachment` tool: the tool returns a one-use `upload_url`, and this route receives the file. It needs no `Authorization` header — the token itself is the credential — and it can be used only once before expiring (10 minutes). Unknown, expired and already-used tokens return 404.

## Common pitfalls

- **401 `{"error":"unauthorized"}`** — the token is missing, malformed, or expired. Re-check the header and create a fresh token in Settings.
- **403 `{"error":"write"}`** — the token lacks the scope the route needs. Add the scope when creating the token.
- **`/_/api/search/attachments` 404** — document search is not enabled on the instance; the route is not registered at all.
- **Wiki-links render unstyled in previews** — pass `?slug=namespace/page` so they resolve in the page's namespace.
- Cookies also work for a logged-in browser session, but scripts and agents should send the `Authorization` header — it is explicit and does not depend on a browser session.

Next: [[MCP Tool Reference]].
