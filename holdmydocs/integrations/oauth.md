---
title: MCP OAuth
tags: hmd, integrations, oauth, mcp
---

HMD can authenticate MCP clients with OAuth. It is off by default. Personal access tokens work independently.

## Enable OAuth

1. Set the public origin and enable MCP and OAuth:

   ```yaml
   server:
     base_url: https://wiki.example.com
   mcp:
     enabled: true
     oauth:
       enabled: true
       allow_admin_delegation: false
   ```

2. Restart HMD.

- `server.base_url` is the OAuth issuer. Set it to the exact origin clients use.
- Production requires HTTPS. For local development only, `mcp.oauth.allow_insecure_loopback: true` allows an HTTP loopback origin.
- Metadata is published at `/.well-known/oauth-authorization-server` and `/.well-known/oauth-protected-resource/_/mcp`.
- HMD supports the authorisation-code grant with S256 PKCE and the MCP resource indicator. Send the exact resource URI (`<base_url>/_/mcp`) in the authorisation and code-exchange requests.
- A refresh request may omit the resource to inherit its grant. A different resource is rejected.
- Client ID Metadata Documents (CIMD) are not supported.

## Register a client

### Admin interface

1. Sign in as an administrator and open **Settings → MCP OAuth clients** (`/_/settings/oauth-clients`).
2. Enter the client's name, exact callback URLs, authentication method and allowed actions.
3. Copy the generated client ID and secret into the MCP client. Confidential secrets are shown once.

- **Disable client** permanently disables a registration and revokes its grants and tokens. To replace a secret, register a new client, disable the old one and update the MCP client.
- **Delete client** appears on disabled clients. **Delete all disabled** removes every disabled registration. Deletion also removes the client's grants, token families, token records and connection history. Active clients cannot be deleted.

### Command line

Stop HMD first: the CLI opens the OAuth store in the configured app directory, so run it on the machine that owns that directory. Redirect URIs must be exact, and HTTPS is required except for loopback callbacks.

```sh
hmd \
  -oauth-client-add \
  -oauth-client-name "Example MCP client" \
  -oauth-client-redirect-uri "https://client.example/callback" \
  -oauth-client-auth-method none \
  -oauth-client-scopes read,write
```

- Repeat `-oauth-client-redirect-uri` for each callback.
- Public clients use `none`. Confidential clients use `client_secret_basic` or `client_secret_post`; the secret is printed once.
- Every client must use S256 PKCE.

To replace a lost or compromised secret, stop HMD, add a replacement client, disable the old one, then update the MCP client before restarting:

```sh
hmd -oauth-client-disable -oauth-client-id "hmd_c_..."
```

Disabling is permanent and revokes the client's grants, access tokens and refresh tokens. Users must approve a new connection to the replacement.

## Dynamic client registration

Enable RFC 7591 registration, then restart HMD:

```yaml
oauth:
  enabled: true
  dynamic_registration: true
```

- Discovery then advertises `registration_endpoint` at `<base_url>/_/oauth/register`. When disabled, discovery omits it and the endpoint returns 404.
- The request is a JSON document with `redirect_uris` and optional `client_name`, `token_endpoint_auth_method`, `scope`, `grant_types` and `response_types`.
- Defaults: `client_secret_basic`, `read`, authorisation-code flow, `code` response type. Authentication methods: `none`, `client_secret_basic`, `client_secret_post`.
- Callback URLs get the same exact-match validation as admin registrations. Metadata URLs are not fetched. RFC 7592 self-management is not implemented.
- Limits: five public registrations per minute across the instance, plus the OAuth per-address limit. At most 32 dynamic clients, within the 256-client total. Disabled registrations count until deleted.
- DCR clients cannot request `settings`.

Warning: the limits do not stop an attacker exhausting public registration capacity. Enable DCR only if you accept that, and review and delete unwanted clients in the admin interface.

Registration grants no document access. Every connection still needs S256 PKCE, user authentication and consent. A dynamically supplied client name is not a verified identity.

## Consent and scopes

The user signs in with the local password form or the configured OIDC provider. The consent page shows the client, callback host, account and MCP resource. The user can deny, or approve only some actions and namespaces.

| Scope | Permits |
| --- | --- |
| `read` | MCP read operations |
| `write` | Page and attachment writes. Does not imply `read`. |
| `settings` | Administrative access. Implies read and write. |

- Request `read write` for a client that needs both. See [[MCP Tool Reference]] for the tool-to-scope mapping.
- `settings` is disabled by default. `mcp.oauth.allow_admin_delegation` permits it for eligible users and registered clients. **Settings access covers all current and future namespaces** and cannot be narrowed.
- Granted scopes cannot exceed the client's allowed scopes or the user's current permissions. Permissions are rechecked on use and on refresh.
- Non-administrative grants can be limited to selected namespaces, or the user can approve all namespaces.

Some MCP applications request only `read` by default. To allow edits, set the application's OAuth scope to `read write`, make sure its HMD registration allows both, and reconnect to approve. Registration sets the maximum; consent cannot add an action the application did not request.

## Tokens and revocation

| Credential | Lifetime |
| --- | --- |
| Authorisation code | 2 minutes |
| Access token | 15 minutes |
| Refresh token | Bound to a 30-day grant family. Refresh does not extend it. |

- Refresh tokens rotate on use. Replaying an old refresh token revokes the surviving family. Replaying a used authorisation code revokes the credentials derived from it.
- Clients must serialise token requests. Concurrent exchanges of one refresh token count as replay and can revoke the new tokens.
- Refresh can narrow permissions but cannot restore scopes dropped by an earlier refresh.
- If a token response is lost, start a new authorisation and consent flow. Do not retry a possibly consumed refresh token or code.
- Users review and disconnect their own grants at `/_/settings/connections`. Disconnecting immediately revokes the grant's access tokens, refresh tokens and OAuth-derived upload capabilities.
- Clients can revoke via the RFC 7009 endpoint `/_/oauth/revoke`. Revoking either token revokes the whole grant.
- Disabling OAuth stops OAuth credentials working but keeps replay and revocation state. Re-enabling does not restore revoked grants.
- Changing the issuer or resource invalidates grants bound to the old origin.

## Storage and backups

- OAuth state (registrations, grants, token digests, replay and revocation records) is in the private `oauth.json` under `HMD_APP_DIR`. No plaintext tokens, codes or client secrets are stored, but treat the file and its backups as sensitive.
- Back up the whole app directory with the Git repository and configuration, using a filesystem-consistent snapshot or a stopped instance. Include `oauth.json` whenever it exists, even with OAuth disabled. Never copy it as a plain file while HMD is writing it.
- Losing `oauth.json` invalidates existing OAuth credentials.
- An older snapshot can restore credentials revoked or rotated since. Before exposing a recovered instance, disable the restored client registrations, provision replacements and require fresh consent.
- If HMD reports `OAuth persistence is uncertain; restart required`, it rejects OAuth state reads and writes. Fix the storage fault, keep `oauth.json`, and restart HMD. Do not delete the file or keep retrying token requests. If an issuance response was lost, get new consent after recovery.
- The OAuth store is locked to one running HMD process. Multiple instances sharing an app directory are not supported. Back up and migrate in a coordinated way when moving hosts.

See [[MCP Integration]], [[Authentication And Access]], and [[Storage And Recovery]].
