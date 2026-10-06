---
title: Personal Access Tokens
tags: hmd, administration, security
---

Personal access tokens (PATs) let scripts, agents, and MCP clients authenticate as you without your password or a browser session.

Create and revoke tokens from `/_/settings` under the **access tokens** tab.

## Create a token

1. Open `/_/settings` and open the **access tokens** tab.
2. Name the token after the client that will use it, for example `claude-code`.
3. Choose an expiry: 1 day, 7 days, 30 days (the default), 1 year, or never.
4. Select at least one scope: `read`, `write`, or `settings`.
5. Leave every namespace box unchecked for all namespaces, or check the namespaces you want the token limited to.
6. Click **Create token**.

The token value appears once, directly above the form. Copy it now: HMD stores only its SHA-256 digest and cannot show it again.



## What the scopes mean

- `read` — view pages and search.
- `write` — anything that writes to the store: saving, renaming, tagging, and uploading.
- `settings` — administrative access to `/_/settings`, `/_/admin`, and `/_/namespaces`. A token with `settings` is unrestricted: namespace restrictions do not apply, and the token list labels it `Administrator`.

A token's scopes can never exceed its owner's. HMD rejects a token for a scope the owner does not have, and filters effective scopes again on every request. If you reduce a user's scopes, its existing tokens are limited on the next request without being re-created.

A namespace restriction applies to every non-administrative request: other namespaces are treated as nonexistent, and restricted areas stay out of search, tags, and health reports.

## Use a token

Send the token as a Bearer credential to the API or the MCP endpoint. Token values start with `hmd_` followed by 64 hexadecimal characters:

```sh
curl -H "Authorization: Bearer hmd_..." https://wiki.example.com/_/api/health
```

## Revoke a token

Tokens are revoked by name from the same **access tokens** tab: click **revoke** next to the token. The name is the revocation key and must be unique per user, so HMD cannot revoke the wrong token. Revoke any token whose secret may have been exposed or whose client is retired; the change applies immediately.


## Common pitfalls

- Copy the value when it is displayed — it can never be shown again.
- HMD stores at most 64 tokens per user and names are unique. Reuse or revoke old tokens instead of duplicating names.
- A token with `settings` bypasses namespace restrictions. Issue it only to clients you trust completely.
- Tokens and browser sessions are separate. A token cannot log in to the web UI, and revoking it does not end your session.

See [[Settings And Administration]], [[Authentication And Access]], and [[MCP Integration]].
