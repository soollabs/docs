---
title: Security Architecture
tags: hmd, operations, security
---

HMD is a trusted-editor wiki. It protects the service boundary but does not sanitise raw HTML written by an authorised editor.

## Trust boundaries

- The TLS reverse proxy is trusted only when its source address matches `server.trusted_proxies`; only then does HMD use `X-Forwarded-Proto`.
- HMD trusts the configured OIDC provider for identity, the Git remote to retain pushed history, Tika to parse documents in a separate sandbox, and the model host for the embedding model.
- The filesystem holding HMD state and the Git worktree is trusted local storage.
- Public namespaces expose page views and attachments without login. Authenticated users reach only their scopes. Bearer PATs can have narrower scopes and namespace allowlists. Admins manage users, configuration and namespace settings.
- MCP is an authenticated API. Do not expose it to the internet without the same care as the browser service.

## Controls

- Local passwords are bcrypt hashes. PAT values are stored as SHA-256 digests.
- Sessions are HttpOnly, SameSite Lax cookies with a 30-day server-side limit. Cookie writes require exact Origin and CSRF-token checks.
- OIDC binds accounts to issuer and subject. Admission needs an allowlist or a verified email-domain rule.
- MCP OAuth is disabled by default. Tokens are stored as digests in private app state. Only access tokens authenticate the MCP resource. Access requests and refreshes recheck the live grant, client and user permissions. Users can disconnect consent grants. Replaying an authorisation code or refresh token revokes the token family.
- Repository reads and writes are confined below the Git worktree. Symlinks are excluded from pages, configuration, attachments and export.
- Request logs omit credentials, queries, bodies and client addresses. Do not add page bodies or tokens to application or proxy logs.
- HMD sends one Tika request at a time, cancels it after 60 seconds, skips embedded documents and accepts at most 8 MiB of extracted text.

## Data and recovery

- Git content is authoritative for pages, attachments and wiki configuration.
- `users.json`, `oauth.json`, local configuration and external secret files are sensitive authoritative app state. Keep `oauth.json` whenever it exists, even while OAuth is disabled.
- Sessions, search indexes, extracted search state and model downloads can be recreated.
- Back up content and app state, and restrict backup access.
- Restoring an older OAuth snapshot can bring back credentials revoked or rotated since. Before exposing a recovered service, disable the restored client registrations and require new registrations and fresh consent. See [[MCP OAuth]] and [[Storage And Recovery]].

## Known risks

| Risk | What to do |
| --- | --- |
| Anyone with write access can publish raw HTML. | Limit writers, especially on public namespaces. |
| Document search sends uploaded files to Tika, which parses untrusted content. | Run Tika privately, with resource limits. |
| Sign-in, Git hosting and model downloads depend on outside services. | Use HTTPS, watch for failures and keep local backups. |
| A static export has no access control. | Export only namespaces meant to be public. |

See [[Authentication And Access]], [[Reverse Proxies]], and [[Storage And Recovery]].
