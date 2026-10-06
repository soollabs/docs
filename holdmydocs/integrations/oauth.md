---
title: MCP OAuth
tags: hmd, integrations, oauth, mcp
---

HMD provides OAuth authentication for MCP clients. OAuth is disabled by default. Personal access tokens work independently.

## Enable OAuth

Set the canonical public origin and enable MCP and OAuth:

```yaml
base_url: https://wiki.example.com
mcp:
  enabled: true
oauth:
  enabled: true
  allow_admin_delegation: false
```

Restart HMD after changing configuration. Production deployments require HTTPS. For local development only, `oauth.allow_insecure_loopback: true` allows an HTTP loopback origin; it does not allow a public HTTP issuer. `base_url` is the OAuth issuer, so configure it to the exact origin clients use. Spoofed `Host` and forwarded headers do not change it.

OAuth metadata is published at `/.well-known/oauth-authorization-server` and `/.well-known/oauth-protected-resource/_/mcp`. Clients should discover these endpoints. HMD supports the authorisation-code grant with S256 PKCE and the MCP resource indicator. Send the exact MCP resource URI (`<base_url>/_/mcp`) in the authorisation and code-exchange requests. A refresh request may omit the resource to inherit its grant, but a different resource is rejected. Client ID Metadata Documents (CIMD) are not supported.

## Register a client

### Admin interface

Sign in with an administrator account and open **Admin → Manage MCP OAuth clients** (`/_/admin/oauth`). Enter the MCP client's name, exact callback URLs, authentication method and allowed actions. Copy the generated client ID and secret into the MCP client's OAuth settings. Confidential secrets are shown once. The list includes callback URLs, allowed actions, authentication methods, registration source and disabled status; it never displays secret verifiers.

Use **Disable client and revoke all access** to permanently disable a registration and revoke its grants and tokens. To replace a secret, register a replacement client, disable the old registration and update the MCP client's credentials.

Disabled clients have a **Delete client** button. **Delete all disabled clients** removes every disabled registration and leaves active clients untouched. Deletion removes the client's associated grants, token families and token records, including its connection history. Active clients cannot be deleted; disable them first.

### Local administration

The CLI reads the configured app directory. Stop HMD before running a CLI command that opens its OAuth store. Redirect URIs must be exact; HTTPS is required except for loopback callbacks.

```sh
hmd \
  -oauth-client-add \
  -oauth-client-name "Example MCP client" \
  -oauth-client-redirect-uri "https://client.example/callback" \
  -oauth-client-auth-method none \
  -oauth-client-scopes read,write
```

Repeat `-oauth-client-redirect-uri` for each callback. Public clients use `none`. Every client must use S256 PKCE, including confidential clients. Confidential clients can use `client_secret_basic` or `client_secret_post`; the secret is printed once. Store it in the client's secret manager. HMD stores only a bcrypt digest of a confidential secret, never its plaintext value.

The command reads the normal HMD configuration and app directory. Run it on the machine that owns that app directory, and do not run it while the HMD server is using the OAuth store.

To replace a lost or compromised confidential-client secret, stop HMD, use `-oauth-client-add` to provision a replacement client and permanently disable the old registration, then update the MCP client with the new credentials before restarting HMD:

```sh
hmd -oauth-client-disable -oauth-client-id "hmd_c_..."
```

Disabling a client revokes its grants, access tokens and refresh tokens. The disable operation is permanent; users must approve a new connection to the replacement client.

## Dynamic client registration

To let MCP clients register themselves using RFC 7591, enable:

```yaml
oauth:
  enabled: true
  dynamic_registration: true
```

Restart HMD. Authorisation-server discovery then advertises `registration_endpoint` at `<base_url>/_/oauth/register`. With this option disabled, discovery omits that field and the endpoint returns 404.

Registration accepts a JSON document with `redirect_uris` and optional `client_name`, `token_endpoint_auth_method`, `scope`, `grant_types` and `response_types`. Defaults are `client_secret_basic`, `read`, the authorisation-code flow and the `code` response type. Authentication methods are `none`, `client_secret_basic` and `client_secret_post`. Callback URLs use the same exact-match validation as administrator registrations. Metadata URLs are not fetched. HMD does not implement RFC 7592 client self-management.

Public registration is limited to five attempts per minute across the instance, in addition to the OAuth per-address request limit. At most 32 dynamically registered clients are stored, within the overall 256-client limit; disabled registrations count until deleted. These limits reserve capacity for administrator registrations but do not prevent an attacker exhausting public registration capacity. Enable DCR only when that trade-off is acceptable. Review, disable and delete unwanted clients in the admin interface. DCR clients cannot request `settings`.

Registration does not grant access to documents. Every connection requires S256 PKCE, user authentication and consent. A dynamically supplied client name is not a verified application identity.

## User consent and scopes

When a client starts authorisation, the user signs in with the local password form or the configured OIDC provider. The user can deny the request or approve only some requested actions and namespaces. The consent page identifies the client, callback host, account and MCP resource.

- `read` permits MCP read operations.
- `write` permits page and attachment writes.
- `settings` grants administrative access. It is disabled by default; enabling `oauth.allow_admin_delegation` permits it for eligible users and registered clients. **Settings access is unrestricted across all current and future namespaces** and cannot be narrowed by namespace selection.

Granted scopes cannot exceed either the client's allowed scopes or the user's current HMD permissions. Those permissions are checked again when an OAuth token is used and when it is refreshed. `write` does not imply `read`; request `read write` for a client that needs both. `settings` implies both actions and bypasses namespace restrictions. A non-administrative grant may be limited to selected namespaces, or the user may explicitly approve all namespaces. See [[MCP Tool Reference]] for the tool-to-scope mapping.

Some MCP applications and services default to requesting only `read`. To enable edits, explicitly configure the application's OAuth scope setting to request `read write`, ensure its HMD registration allows both actions, and reconnect to approve the additional scope. Allowing `write` in HMD's client registration does not make the application request it: registration sets the maximum permissions, and consent cannot add an action absent from the application's request.

## Token lifecycle and revocation

HMD issues two-minute authorisation codes, 15-minute access tokens and refresh tokens bound to a 30-day grant family. Refresh tokens rotate when used; replaying an old refresh token revokes the surviving family. Refresh does not extend the grant-family expiry.

Clients must serialise refresh requests. Concurrent exchanges of the same refresh token are replay attempts: even if one succeeds, the duplicate can revoke its newly issued tokens. Refresh can narrow permissions but cannot restore scopes removed from a previous refresh.

If a token response is lost, do not retry a possibly consumed refresh token or assume an authorisation code remains usable. Start a new authorisation and consent flow. HMD does not retain plaintext successor tokens to replay a lost response.

Users can review and disconnect their own grants at `/_/connections`. Disconnect immediately revokes that grant's access tokens, refresh tokens and OAuth-derived upload capabilities. OAuth clients can use the RFC 7009 revocation endpoint at `/_/oauth/revoke`; revoking either token revokes the whole grant. Unknown tokens are handled without revealing whether they exist.

Disabling OAuth prevents OAuth credentials from being used but preserves stored replay and revocation state. Re-enabling OAuth does not restore grants that were already revoked. Changing the configured issuer/resource invalidates grants bound to the previous origin.

## Storage, backups and process model

Client registrations, consent grants, token digests and replay/revocation records live in the private `oauth.json` file under `HMD_APP_DIR`. Plaintext access tokens, refresh tokens, codes and confidential client secrets are not stored there. Treat the file and its backups as sensitive security state nonetheless.

Back up the complete app directory together with the Git repository and configuration, using a filesystem-consistent snapshot or a stopped instance. Include `oauth.json` whenever it exists, even while OAuth is disabled. Restore the OAuth state with the same protected app data; losing it invalidates existing OAuth credentials. Never copy a live `oauth.json` as an ordinary file-level backup while HMD is writing it.

Restoring an older snapshot can restore credentials revoked or rotated after the backup was taken. Before exposing a recovered instance, disable affected restored client registrations, provision replacements and require fresh consent. A restore does not preserve revocation decisions newer than its snapshot.

If replacing the state file succeeds but confirming directory durability fails, HMD reports `OAuth persistence is uncertain; restart required` and rejects OAuth state reads and writes. No successful token response is returned for that failed operation, but its state may already be on disk. Resolve the storage fault, retain `oauth.json`, and restart HMD to reopen the on-disk state. Do not delete the file or keep retrying token requests to clear the error. If an issuance response was lost, obtain new consent after recovery.

The OAuth store is locked to one running HMD process. Multiple replicas or concurrent instances sharing an app directory are not supported. Run one instance for this state store; use a coordinated migration and backup before moving it to another host.

See [[MCP Integration]], [[Authentication And Access]], and [[Storage And Recovery]].
