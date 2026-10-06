---
title: Route Reference
tags: hmd, reference
---

This page maps HMD's routes, grouped by area, with the HTTP method and authentication requirement for each. Use it to write reverse-proxy rules, health checks, and API clients.

## Conventions

Content owns the root. Application routes are reserved under `/_/` — the one top-level segment a namespace may never take. Unknown `/_/` paths never become content pages.

Authentication works in three layers:

- **None** — reachable without credentials (probes, login, static assets, one-use upload URLs).
- **Anonymous page** — a plain page view or attachment is served unauthenticated when the namespace is public, and is byte-identical to a 404 when it is not. Every other request needs a login session or a Bearer personal access token (PAT).
- **Session or PAT** — a session cookie or `Authorization: Bearer` token. Scope requirements: `read` for GET/HEAD, `write` for POST/DELETE, and `settings` for administrator and namespace-management operations (not personal settings). On an API or MCP route an auth failure is HTTP 401 with a JSON body — never a login redirect. A PAT restricted to namespaces can only reach paths that resolve to those namespaces.

## Probes and root

| Route | Auth | Purpose |
| --- | --- | --- |
| `GET /_/live` | None | Process liveness. Always 200. |
| `GET /_/ready` | None | Repository and index readiness. 503 until both are ready. |
| `GET /` | None | Redirects to the configured landing (`.wiki.yaml`); access to the destination is checked separately. |

## Quick-create

| Route | Auth | Purpose |
| --- | --- | --- |
| `GET /_/new` | Write | New-page editor using the namespace's `new:` template. |
| `GET /_/static/...` | None | Static assets (CSS, JavaScript, fonts). |

## Authentication

| Route | Auth | Purpose |
| --- | --- | --- |
| `GET /_/login` | None | Login form. |
| `POST /_/login` | None | Local password login (unless `oidc.local_login` is off). |
| `POST /_/logout` | Write | Ends the session. |
| `GET /_/auth/oidc/login` | None | Starts the OIDC flow. |
| `GET /_/auth/oidc/callback` | None | OIDC redirect target. |
| `GET /_/auth/oidc/icon` | None | Provider icon (cached from the provider). |

## Settings, admin and namespaces

The personal settings page and its token and appearance actions require an account, not administrator access. Admin and namespace management require the `settings` scope. The UI is described on [[Settings And Administration]].

| Route | Method | Purpose |
| --- | --- | --- |
| `/_/settings` | GET | Personal settings (appearance, git author, tokens). |
| `/_/admin` | GET | Instance configuration and users. |
| `/_/namespaces` | GET | Namespace list. |
| `/_/namespaces/new` | GET | New namespace form. |
| `/_/namespaces/{name}/edit` | GET | Edit one namespace's `.namespace.yaml`. |
| `/_/settings/namespaces/{name}/export` | GET | Export the namespace as a static site. |
| `/_/api/settings/server` | POST | Save instance configuration. |
| `/_/api/settings/appearance` | POST | Save skin, palette and fonts. |
| `/_/api/settings/export` | POST | Bake current values into `config.yaml`. |
| `/_/api/settings/author` | POST | Save the personal Git author. |
| `/_/api/settings/tokens` | POST | Create a personal access token. |
| `/_/api/settings/tokens/revoke` | POST | Revoke a token. |
| `/_/api/namespaces` | POST | Save a namespace configuration. |
| `/_/api/namespaces/reset` | POST | Restore a namespace's default configuration. |
| `/_/api/namespaces/delete` | POST | Delete a namespace. |
| `/_/api/namespaces/delete-all` | POST | Delete every namespace. |
| `/_/api/settings/users` | POST | Create a user. |
| `/_/api/settings/users/scopes` | POST | Change a user's scopes. |
| `/_/api/settings/setup` | POST | Re-run the setup dialog. |
| `/_/api/setup` | POST | Complete first-run setup (settings scope). |
| `/_/api/settings/wiki` | POST | Save `.wiki.yaml` (site name and landing). |
| `/_/api/settings/help/reset` | POST | Restore the help guide. |

## Search and tags

| Route | Auth | Purpose |
| --- | --- | --- |
| `GET /_/search` | Read | Full-text search page. |
| `GET /_/search/attachments` | Read | Attachment search page; registered only when document search is enabled. |
| `GET /_/tags` | Read | Tag index. |
| `GET /_/tags/{tag}` | Read | Pages carrying one tag. |
| `GET /_/health-report` | Read | Wiki hygiene report (dangling links, orphans, stale pages). |

## Hidden pages

Hidden pages are dot-prefixed drafts and templates — app-internal content that is never addressable as a normal page, so it lives under `/_/hidden`.

| Route | Auth | Purpose |
| --- | --- | --- |
| `GET /_/hidden` | Read | Hidden page list. |
| `GET /_/hidden/{path...}` | Read | View or edit (`?do=edit`) a hidden page. |

There is no hidden-page POST route.

## MCP

| Route | Auth | Purpose |
| --- | --- | --- |
| `POST /_/mcp` | Any authenticated | MCP JSON-RPC calls; each tool enforces its own scope and namespace rules. |

MCP is stateless: it does not support GET streams or DELETE session teardown. Clients must send the required `MCP-Protocol-Version: 2026-07-28` header and protocol metadata. See [[MCP Integration]].

The tool list and scope map are on [[MCP Tool Reference]].

## API

All API routes accept a Bearer personal access token — a logged-in session cookie also works. Most return JSON; Markdown preview returns HTML and attachment upload has a one-use capability alternative. See [[API Reference]] for response shapes and worked examples.

| Route | Auth | Purpose |
| --- | --- | --- |
| `GET /_/api/search` | Read | Full-text search. |
| `GET /_/api/search/attachments` | Read | Attachment search; registered only when document search is enabled. |
| `GET /_/api/health` | Read | Wiki hygiene report. |
| `GET /_/api/sync` | Read | Sync status. |
| `POST /_/api/sync/push-now` | Write | Push to the remote immediately. |
| `POST /_/api/pages/{slug...}` | Write | Create or update a page. |
| `POST /_/api/pages/delete/{slug...}` | Write | Delete a page. |
| `POST /_/api/pages/rename/{slug...}` | Write | Rename a page. |
| `POST /_/api/pages/tags/{slug...}` | Write | Change page tags. |
| `POST /_/api/pages/revert/{slug...}` | Write | Restore an older revision. |
| `GET /_/api/preview/{slug...}` | Read | Page metadata and snippet. |
| `POST /_/api/preview` | Write | Render Markdown to HTML. |
| `POST /_/api/attachments/{slug...}` | Write | Upload an attachment to a page. |
| `POST /_/api/attachment-uploads/{token}` | None | One-use upload URL created by the MCP `upload_attachment` tool. |

## Attachments

| Route | Auth | Purpose |
| --- | --- | --- |
| `GET /_/attachments/{path...}` | Anonymous page | Serve an attachment; public-or-404 by namespace, like page views. |

## Content dispatcher

| Route | Auth | Purpose |
| --- | --- | --- |
| `GET /{path...}` | Anonymous page | Page view, namespace index, or landing. `?do=` actions need a session or PAT. |

GET actions include `edit`, `history`, `diff`, and `rev` (view a past revision). Page changes go through `POST /_/api/pages/*` JSON endpoints, not content POST routes.

## Common pitfalls

- Reverse proxies must not rewrite or swallow `/_/` paths — the app and its MCP/API clients depend on them verbatim.
- Use `/_/live` or `/_/ready` for unauthenticated load-balancer probes.
- A restricted PAT that cannot resolve a route to an allowed namespace gets 403 rather than 404, so the caller learns the restriction instead of guessing at a page.

Next: [[API Reference]].
