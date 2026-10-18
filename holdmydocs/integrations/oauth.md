---
title: MCP OAuth
tags: hmd, integrations, oauth, mcp
---

With OAuth, an MCP client opens a browser window where the user signs in to HMD and approves what the client may do. No token is pasted into the client. OAuth is off by default; [[Personal Access Tokens]] keep working either way.

## Turn on OAuth

1. Make sure HMD is served over HTTPS and **Settings → Server → base URL** is the exact address clients use, for example `https://wiki.example.com`.
2. Open **Settings → MCP**, tick **enable MCP** and **enable OAuth for MCP clients**, and save.
3. Restart HMD.

For local testing over plain HTTP on `127.0.0.1`, also turn on **allow insecure loopback**. Never use it on a public address.

## Register a client

Most clients need to be registered before they can connect.

1. Open **Settings → MCP OAuth clients**.
2. Enter the client's name, its callback URLs (exactly as the client documents them) and which actions it may request.
3. Copy the client ID, and the secret if one is shown, into the client. The secret is shown once.

To replace a lost secret, register a new client, update the MCP client, then **Disable client** on the old one. Disabling is permanent and disconnects everyone using it. Disabled clients can then be deleted.

### Let clients register themselves

Some clients register automatically. To allow that, turn on **allow dynamic client registration** in **Settings → MCP** and restart. Anyone who can reach HMD can then register a client (up to 32), so review the list in **Settings → MCP OAuth clients** and delete ones you do not recognise. Registration alone gives no access: every user still signs in and approves.

## Connect and approve

When the client connects, HMD shows an approval page with the client name, its callback address and what it asks for. The user can approve some actions or namespaces and leave others out.

| Action | Allows |
| --- | --- |
| read | Searching and reading pages |
| write | Creating, editing and deleting pages and uploading files. Does not include read. |
| settings | Administrator access to every namespace, now and in future. Off unless **allow administrator delegation** is turned on. |

Some clients only ask for read. To let one edit, set its requested scope to `read write`, make sure its registration allows both, and reconnect.

## Disconnect

- Users see and disconnect their own clients in **Settings → Connected applications**. Access stops immediately.
- A connection lasts 30 days, then the user approves again.
- Turning OAuth off stops every OAuth connection. Turning it back on does not restore them.

## Back up and restore

OAuth state lives in `oauth.json` in the application directory. Back it up with the rest of that directory ([[Storage And Recovery]]), and keep it even if you turn OAuth off.

- Losing `oauth.json` disconnects every OAuth client.
- Restoring an old copy can bring back connections that were revoked since. After a restore, disable and re-register clients before reopening the wiki.
- If HMD logs `OAuth persistence is uncertain; restart required`, fix the disk problem and restart HMD. Do not delete `oauth.json`.

## Command line

With HMD stopped, you can also register and disable clients from the machine that holds the application directory:

```sh
hmd -oauth-client-add \
  -oauth-client-name "Example MCP client" \
  -oauth-client-redirect-uri "https://client.example/callback" \
  -oauth-client-auth-method none \
  -oauth-client-scopes read,write

hmd -oauth-client-disable -oauth-client-id "CLIENT_ID"
```

Repeat `-oauth-client-redirect-uri` for each callback. Use `none` for clients without a secret, or `client_secret_basic` for clients with one.

See [[MCP Integration]] and [[Authentication And Access]].
