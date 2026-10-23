---
title: Route Reference
tags: hmd, reference
---

HMD's routes by area, with method and authentication. Use it for reverse-proxy rules, health checks and API clients.

## Conventions

Content owns the root. Application routes live under `/_/`, the one top-level segment a namespace may never take. Unknown `/_/` paths never become content pages. OAuth discovery uses `/.well-known/` when OAuth is enabled.

- **None**: reachable without credentials (probes, login, static assets, one-use upload URLs).
- **Anonymous page**: a page view or attachment is served unauthenticated when the namespace is public, and is identical to a 404 when it is not. Every other request needs a login session or a Bearer personal access token (PAT).
- **Session or PAT**: a session cookie or `Authorization: Bearer` token. Scopes: `read` for GET/HEAD, `write` for POST/DELETE, `admin` for system settings and namespace management. Personal settings need only a signed-in user. Connected applications is browser-session only. API and MCP auth failures return HTTP 401 with a JSON body, never a login redirect. A PAT restricted to namespaces can only reach paths in those namespaces.

OAuth access tokens are valid for `/_/mcp` only. Refresh tokens are not bearer credentials. OAuth consent and connection-management routes need a browser session, not a PAT or OAuth token. Token and revocation endpoints use registered-client authentication.

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

## MCP OAuth

Registered only when OAuth is enabled. Browser POSTs need the live session, exact Origin and CSRF token. Approving or disconnecting a grant does not need the `write` or `admin` action. See [[MCP Integration]].

| Route | Auth | Purpose |
| --- | --- | --- |
| `GET/HEAD /.well-known/oauth-authorization-server` | None | Authorisation-server metadata. |
| `GET/HEAD /.well-known/oauth-protected-resource/_/mcp` | None | MCP protected-resource metadata. |
| `GET/HEAD /.well-known/oauth-protected-resource` | None | Root alias of the same resource document. |
| `GET /_/oauth/authorize` | Browser session or login continuation | Validate the request and show consent, or continue through login. Once the redirect URI is exactly validated, errors redirect back to the client with `error`, `error_description`, `state` and `iss`. Unvalidated client or callback values render an error page and never redirect. |
| `POST /_/oauth/authorize` | Browser session and CSRF | Approve or deny a pending request. |
| `POST /_/oauth/token` | Registered client | Exchange an authorisation code (S256 PKCE) or rotate a refresh token. |
| `POST /_/oauth/revoke` | Registered client | Revoke the client's own grant using an access or refresh token. |
| `POST /_/oauth/register` | None; DCR must be enabled | Register an MCP client with RFC 7591 JSON metadata. Grants no document access. |

Clients authenticate with their registered method: `none`, `client_secret_basic` or `client_secret_post`. Public clients still send their client ID.

## Settings, admin and namespaces

Personal settings (appearance, git author and access tokens) and their saves need only a signed-in user, and a token also needs the `preferences` scope; read-only mode still refuses the saves. Every other settings route and namespace management need the `admin` scope. Connected applications needs a browser session without administrative access. OAuth client administration needs an admin browser session. See [[Settings And Administration]].

| Route | Method | Purpose |
| --- | --- | --- |
| `/_/settings` | GET | Personal settings, opening on Appearance. |
| `/_/settings/{section}` | GET | Personal sections: `appearance`, `git-author`, `access-tokens`. System sections: `server`, `git`, `mcp`, `oidc`, `document-search`, `wiki`, `users`, `advanced` (environment overrides). The former `git-remote`, `behaviour` and `advanced-config` routes return 404. |
| `/_/settings/namespaces` | GET | Namespace list. |
| `/_/settings/namespaces/new` | GET | New namespace form. |
| `/_/settings/namespaces/{name}/edit` | GET | Namespace General page: name, description, index, tree and quick-create. |
| `/_/settings/namespaces/{name}/edit/published` | GET | Published visibility and appearance. |
| `/_/settings/namespaces/{name}/edit/static-site` | GET | Static-site settings and preview. |
| `/_/settings/namespaces/{name}/edit/widgets` | GET | Namespace widget composition. |
| `/_/settings/namespaces/{name}/export` | GET | Export the namespace as a static site. |
| `/_/settings/namespaces/{name}/preview` | GET | Create a protected static-site preview. |
| `/_/export-preview/{id}/{path...}` | GET/HEAD | Serve a snapshot to its creator with current `admin` access to the namespace. Previews expire after 15 minutes. |
| `/_/settings/connections` | GET | Connected applications for the signed-in user. |
| `/_/settings/connections/{id}/revoke` | POST | Disconnect one application. |
| `/_/settings/oauth-clients` | GET | MCP OAuth client administration. |
| `/_/settings/oauth-clients` | POST | Register a client; show its secret once when applicable. |
| `/_/settings/oauth-clients/{id}/disable` | POST | Disable a client and revoke its connections. |
| `/_/settings/oauth-clients/{id}/delete` | POST | Delete a disabled client. |
| `/_/settings/oauth-clients/delete-disabled` | POST | Delete all disabled clients. |
| `/_/api/settings/server` | POST | Save instance configuration. |
| `/_/api/settings/appearance` | POST | Save skin, palette and fonts. |
| `/_/api/settings/export` | POST | Bake current values into `config.yaml`. |
| `/_/api/settings/author` | POST | Save the personal Git author. |
| `/_/api/settings/tokens` | POST | Create a personal access token. |
| `/_/api/settings/tokens/revoke` | POST | Revoke a token. |
| `/_/api/namespaces` | POST | Save a namespace configuration. |
| `/_/api/namespaces/reset` | POST | Restore a namespace's default configuration. |
| `/_/api/namespaces/delete` | POST | Delete a namespace and every file beneath it. The UI asks for confirmation when files exist. The former `/delete-all` endpoint is removed. |
| `/_/api/settings/users` | POST | Create a user. |
| `/_/api/settings/users/scopes` | POST | Change a user's scopes. |
| `/_/api/settings/setup` | POST | Re-run the setup dialog. |
| `/_/api/settings/shutdown` | POST | Shut down HMD gracefully. |
| `/_/api/settings/attachments/migrate` | POST | Move attachments from the old top-level `attachments/` folder into their namespaces. |
| `/_/api/settings/attachments/delete` | POST | Delete the old-folder attachments of a namespace that no longer exists. |
| `/_/api/setup` | POST | Complete first-run setup (admin scope). |
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

Dot-prefixed drafts and templates live under `/_/hidden`. There is no hidden-page POST route.

| Route | Auth | Purpose |
| --- | --- | --- |
| `GET /_/hidden` | Read | Hidden page list. |
| `GET /_/hidden/{path...}` | Read | View or edit (`?do=edit`) a hidden page. |

## MCP

| Route | Auth | Purpose |
| --- | --- | --- |
| `POST /_/mcp` | Any authenticated | MCP JSON-RPC calls; each tool enforces its own scope and namespace rules. |

MCP is stateless, so there are no GET streams and no DELETE session teardown. `2026-07-28` requests need the matching version header and per-request protocol/client/capability metadata, and use `server/discover`. Legacy Streamable HTTP clients can negotiate `2025-03-26`, `2025-06-18` or `2025-11-25` through `initialize` without the modern header or metadata. See [[MCP Integration]] and [[MCP Tool Reference]] for the tool list and scope map.

## API

All API routes accept a Bearer PAT or a session cookie. Most return JSON; Markdown preview returns HTML, and attachment upload has a one-use capability alternative. See [[API Reference]] for response shapes and examples.

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

## Attachments and content

| Route | Auth | Purpose |
| --- | --- | --- |
| `GET /_/attachments/{path...}` | Anonymous page | Serve an attachment; public-or-404 by namespace. |
| `GET /{path...}` | Anonymous page | Page view, namespace index, or landing. `?do=` actions need a session or PAT. |

`?do=` actions include `edit`, `history`, `diff` and `rev` (view a past revision). Page changes go through the `POST /_/api/pages/*` endpoints, not content POST routes.

## Common pitfalls

- Reverse proxies must not rewrite or swallow `/_/` paths.
- Use `/_/live` or `/_/ready` for unauthenticated load-balancer probes.
- HMD returns 403 to a restricted PAT that cannot resolve a route to an allowed namespace.

Next: [[API Reference]].
