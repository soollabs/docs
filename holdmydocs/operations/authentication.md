---
title: Authentication And Access
tags: hmd, operations, security
---

Accounts, scopes, tokens, OAuth, OIDC and browser write protections.

## Accounts and scopes

1. On first start, with no `users.json`, HMD creates the first account from `HMD_ADMIN_USER` and `HMD_ADMIN_PASSWORD`.
2. Use a password of 12–72 bytes with no control characters. Common placeholders and the user name are rejected.
3. Remove both variables after that first start.

- Scopes are `read` (view pages), `write` (edit pages) and `settings` (administrator).

### Add a user

1. Open **Settings → Users**.
2. Enter a username and a password of at least 12 characters, and tick their scopes.
3. Click **Create user**, then give them the password.

You can change a user's scopes later in the same list; this signs them out. HMD cannot yet change a password, remove a user or take away all access: the least a user can have is `read`. For other sign-in options, use OIDC below.
- Sessions expire after 30 days. A new login replaces the user's previous session. Log out to revoke the current one immediately.
- Local login throttles repeated failures by source and user.

Skin, palette and font preferences are stored per account in `users.json` and edited at `/_/settings/appearance`:

![Personal appearance preferences](/_/attachments/holdmydocs/operations/authentication/preferences.png)

## Personal access tokens

Use personal access tokens (PATs) for scripts and MCP, never browser cookies. See [[Personal Access Tokens]].

- Each token has a label, an expiry, explicit scopes and an optional namespace allowlist.
- The value is shown once. HMD stores only a SHA-256 digest.
- Revoke a token by label at `/_/settings/access-tokens`.
- Changing a user's scopes also limits their tokens from the next request.

![Personal token management without exposing a token value](/_/attachments/holdmydocs/admin/personal-access-tokens/tokens.png)

## MCP OAuth

OAuth is an opt-in alternative to PATs for MCP clients. Setup, client provisioning, backup and recovery are in [[MCP OAuth]].

- Users sign in with the local form or OIDC, then approve the client's actions and namespace access.
- Review and disconnect grants at `/_/settings/connections`. Disconnecting revokes the grant's access and refresh tokens.
- OAuth access tokens authenticate only `/_/mcp`.
- Clients exchange refresh tokens at `/_/oauth/token` for a new access/refresh pair. Refresh tokens never authenticate MCP requests.
- Refresh tokens rotate on use. Reusing an old one revokes its token family.
- Authorisation codes are single use. Replaying one revokes the credentials derived from it.
- Clients must serialise token requests.
- Revoke either token type at `/_/oauth/revoke` (RFC 7009).

## OIDC

OIDC is disabled until `oidc.issuer` is set. It also needs a client ID, a client secret and a public HTTPS `server.base_url`.

1. Register `<server.base_url>/_/auth/oidc/callback` with the provider.
2. Supply the secret with `HMD_OIDC_CLIENT_SECRET` or a private file named in `oidc.client_secret_file`. It cannot be edited in the UI, and `oidc.client_secret` in `config.yaml` makes loading fail.
3. Choose who is admitted: `oidc.allowed_subjects`, `oidc.allowed_email_domains`, or `oidc.allow_any_authenticated: true` to leave admission to the provider.

- Users are identified by verified issuer and subject, not display name or email.
- Admitted users are provisioned on first login with the configured default scopes.
- Email-domain admission accepts only verified email claims.
- A provider outage blocks OIDC login only. Existing sessions and local login (if enabled) keep working.

![A fictional OIDC sign-in button below local login](/_/attachments/holdmydocs/operations/authentication/oidc-login.png)

## Who can write

Anyone with `write` can put raw HTML in a page, and a public namespace shows it to every visitor. Only give `write` on public namespaces to people you trust.

See [[Reverse Proxies]] before serving HMD through TLS termination.
