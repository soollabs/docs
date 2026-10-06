---
title: Authentication And Access
tags: hmd, operations, security
---

This page covers accounts, scopes, sessions, personal access tokens, MCP OAuth, login throttling, OIDC, and the request-level protections on browser writes.

## Accounts and scopes

The first local account is created from `HMD_ADMIN_USER` and `HMD_ADMIN_PASSWORD` when `users.json` does not exist. Bootstrap passwords must be 12–72 bytes, contain no control characters, and cannot be common placeholders or the user name. Remove the bootstrap variables after that first start.

Users have explicit `read`, `write`, and `settings` scopes. `settings` grants administrative access. Manage users and scopes at `/_/admin`; scope or password changes revoke that user's active sessions. Sessions are server-side, expire after 30 days, and each new login replaces the user's prior session. Log out to revoke the current session immediately.

Local login throttles repeated failures by source and user, and only four bcrypt checks run at once. A login failure intentionally gives no account-specific detail.

## Personal access tokens

Use personal access tokens (PATs) for scripts and MCP, never browser cookies. Tokens have a label, expiry, explicit scopes, and an optional namespace allowlist. Their value is shown once; HMD stores only a SHA-256 digest. Revoke a suspected token at `/_/settings` by its label. Changing a user's scopes also limits its tokens on the next request. See [[Personal Access Tokens]].


Per-user preferences such as skin, palette, and fonts are stored against the account in `users.json` and edited at `/_/settings`:


## MCP OAuth

OAuth is an opt-in alternative to PATs for MCP clients. Users sign in with the normal local form or configured OIDC provider, then approve the client's requested actions and namespace access. They can review and disconnect grants at `/_/connections`; this revokes the grant's access and refresh tokens.

OAuth access tokens are not PATs: they authenticate only `/_/mcp`, not browser pages or other API routes. Refresh tokens never authenticate MCP requests; clients send them to `/_/oauth/token` to obtain a new access/refresh pair. Refresh tokens rotate on use; reuse of an old refresh token revokes its token family. Authorisation codes are single use; replaying a consumed code revokes the credentials derived from it. Clients must serialise token requests. Either token can be submitted to the RFC 7009 revocation endpoint at `/_/oauth/revoke`. See [[MCP OAuth]] for setup, client provisioning, backup and recovery.

## OIDC

OIDC is disabled until `oidc.issuer` is configured. It requires a client ID, client secret and public HTTPS `base_url`. Use `allowed_subjects` or `allowed_email_domains` to admit identities in HMD, or explicitly set `allow_any_authenticated: true` to delegate admission to the identity provider. Register `<base_url>/_/auth/oidc/callback` with the provider. Use a secret file for the client secret.

HMD identifies a user by the verified issuer and subject, not by their display name or email address. An admitted user is provisioned on first login with the configured default scopes. Email-domain admission only accepts verified email claims. OIDC uses state and PKCE cookies; a provider outage prevents OIDC login but does not invalidate existing sessions or local login when it remains enabled.

When OIDC is configured, the login page shows the SSO button alongside the password form:


## Browser requests

Cookie-authenticated writes require an exact `Origin` match and a session-bound CSRF token. Bearer-token requests use their token instead. Authenticated and login responses are `no-store`. HMD sends CSP nonces for scripts, frame denial, no-sniff, no-referrer, COOP, and a restrictive permissions policy. Raw HTML in page bodies is trusted editor content, so only publish namespaces whose writers you trust: a public page serves its raw HTML verbatim.

See [[Reverse Proxies]] before serving HMD through TLS termination.
