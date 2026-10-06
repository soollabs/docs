---
title: Security Architecture
tags: hmd, operations, security
---

This page describes HMD's trust boundaries, the controls that enforce them, and the residual risks an operator accepts.

HMD is a trusted-editor wiki. It protects the service boundary; it does not sanitise raw HTML written by an authorised editor.

## Trust boundaries

Internet browsers reach HMD through a TLS reverse proxy. The proxy is trusted only when its source address matches `trusted_proxies`; only then does HMD use `X-Forwarded-Proto`. HMD trusts the configured OIDC provider to verify identity, the configured Git remote to retain pushed history, Tika to parse documents in a separate sandbox, and the model host to provide the configured embedding model. The filesystem holding HMD state and the Git worktree is trusted local storage.

Public namespaces expose normal page views and their attachments without login. Authenticated users can access only their scopes. Bearer PATs can have narrower scopes and namespace allowlists. Administrative access can manage users, configuration, and namespace settings. MCP is an authenticated API surface and should not be internet-exposed without the same care as the browser service.

## Controls

- Local passwords are bcrypt hashes; PAT values are stored as SHA-256 digests.
- Sessions are HttpOnly, SameSite Lax cookies with a 30-day server-side limit. Cookie writes require exact Origin and CSRF-token checks.
- OIDC binds accounts to issuer and subject. Admission needs an allowlist or a verified email-domain rule.
- MCP OAuth is disabled by default. Access and refresh tokens are stored as digests in private app state. Only access tokens authenticate the MCP resource; refresh tokens are exchanged at the token endpoint, never used as bearer credentials. Access requests and refreshes recheck the live grant, client and user permissions. Consent grants are user-disconnectable; replay of an authorisation code or refresh token revokes the token family.
- Repository reads and writes are confined below the Git worktree. Unix builds use descriptor-relative no-follow opens; symlinks are excluded from pages, configuration, attachments, and export.
- Request logs omit credentials, queries, bodies, and client addresses. Do not add page bodies or tokens to application or proxy logs.
- HMD sends one Tika extraction request at a time, cancels it after 60 seconds, skips embedded documents, and accepts at most 8 MiB of extracted text.

## Data and recovery

Git content is authoritative for pages, attachments, and wiki configuration. `users.json`, `oauth.json`, local configuration, and external secret files are sensitive authoritative app state. Preserve `oauth.json` whenever it exists, even while OAuth is disabled. Sessions, search indexes, extracted search state, and model downloads can be recreated. Back up authoritative content and app state, and restrict backup access.

Restoring an older OAuth snapshot can restore credentials revoked or rotated after that snapshot. Disable affected restored client registrations before exposing the recovered service and require replacement registrations and fresh consent. See [[MCP OAuth]] and [[Storage And Recovery]].

## Residual risks

| Risk | Mitigation | Owner and review |
| --- | --- | --- |
| Trusted editors can publish unsafe raw HTML. | Limit writers; keep sensitive namespaces private. | Operator, review 2027-08-14 |
| Tika parsers process hostile documents. | Keep Tika private and separately sandboxed with parser-specific limits; HMD's request and output bounds do not sandbox parsers. | Operator, review 2027-08-14 |
| External OIDC, Git, and model services can fail or be compromised. | Pin configuration, use TLS, monitor failures, and maintain local backups. | Operator, review 2027-08-14 |
| Static export has no runtime access control. | Export only namespaces intended for publication. | Operator, review 2027-08-14 |

See [[Authentication And Access]], [[Reverse Proxies]], and [[Storage And Recovery]].
