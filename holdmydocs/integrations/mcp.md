---
title: MCP Integration
tags: hmd, integrations, mcp, oauth
---

Connect an AI assistant such as Claude Code to your wiki over MCP, so it can search, read and edit pages. It can only reach what its token or approval allows. The assistant signs in with a token you create (steps 2 and 3) or through the browser with OAuth (see Sign in with OAuth).

## 1. Turn on MCP

An administrator does this once.

1. Open **Settings → Server** and set **base URL** to the address people use for the wiki, for example `https://wiki.example.com` (no path).
2. Open **Settings → MCP**, tick **enable MCP** and save.
3. Restart HMD.

The MCP address is your base URL followed by `/_/mcp`, for example `https://wiki.example.com/_/mcp`.

## 2. Create a token for the assistant

Skip this step and the next if you use OAuth.

1. Open **Settings → Access tokens**.
2. Name the token after the assistant, for example `claude-code`.
3. Tick **read** to let it search and read, and **write** to let it edit. Tick namespaces to limit it to those; leave them all unticked for every namespace.
4. Click **Create token** and copy the value. It is shown once.

See [[Personal Access Tokens]] for expiry and revocation.

## 3. Connect your assistant

Claude Code:

```sh
claude mcp add --transport http hmd https://wiki.example.com/_/mcp \
  --header "Authorization: Bearer hmd_your_token"
```

Other clients that accept a JSON server list:

```json
{
  "mcpServers": {
    "hmd": {
      "type": "http",
      "url": "https://wiki.example.com/_/mcp",
      "headers": { "Authorization": "Bearer hmd_your_token" }
    }
  }
}
```

Ask the assistant to list your namespaces to check the connection.

## Sign in with OAuth

With OAuth, an MCP client opens a browser window where the user signs in to HMD and approves what the client may do. No token is pasted into the client. OAuth is off by default; [[Personal Access Tokens]] keep working either way.

### Turn on OAuth

1. Make sure MCP is on (step 1) and HMD is served over HTTPS at the base URL.
2. Open **Settings → MCP**, tick **enable OAuth for MCP clients** and save.
3. Restart HMD.

For local testing over plain HTTP on `127.0.0.1`, also turn on **allow insecure loopback**. Never use it on a public address.

### Register a client

Most clients need to be registered before they can connect.

1. Open **Settings → MCP OAuth clients**.
2. Enter the client's name, its callback URLs (exactly as the client documents them) and which actions it may request.
3. Copy the client ID, and the secret if one is shown, into the client. The secret is shown once.

To replace a lost secret, register a new client, update the MCP client, then **Disable client** on the old one. Disabling is permanent and disconnects everyone using it. Disabled clients can then be deleted.

#### Let clients register themselves

Some clients register automatically. To allow that, turn on **allow dynamic client registration** in **Settings → MCP** and restart. Anyone who can reach HMD can then register a client (up to 32), so review the list in **Settings → MCP OAuth clients** and delete ones you do not recognise. Registration alone gives no access: every user still signs in and approves.

### Connect and approve

When the client connects, HMD shows an approval page with the client name, its callback address and what it asks for. The user can approve some actions or namespaces and leave others out.

| Action | Allows |
| --- | --- |
| read | Searching and reading pages |
| write | Creating, editing and deleting pages and uploading files. Does not include read. |
| admin | Administrator access to every namespace, now and in future. Off unless **allow administrator delegation** is turned on. |

Some clients only ask for read. To let one edit, set its requested scope to `read write`, make sure its registration allows both, and reconnect.

### Disconnect

- Users see and disconnect their own clients in **Settings → Connected applications**. Access stops immediately.
- A connection lasts 30 days, then the user approves again.
- Turning OAuth off stops every OAuth connection. Turning it back on does not restore them.

### Back up and restore

OAuth state lives in `oauth.json` in the application directory. Back it up with the rest of that directory ([[Storage And Recovery]]), and keep it even if you turn OAuth off.

- Losing `oauth.json` disconnects every OAuth client.
- Restoring an old copy can bring back connections that were revoked since. After a restore, disable and re-register clients before reopening the wiki.
- If HMD logs `OAuth persistence is uncertain; restart required`, fix the disk problem and restart HMD. Do not delete `oauth.json`.

### Command line

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

## What the assistant can do

| Token access | The assistant can |
| --- | --- |
| read | List, read and search pages, follow backlinks, see recent changes, run the health report, read attachment text |
| write | Create, edit and delete pages, upload attachments |
| admin | Read and change namespace settings, in every namespace |

- Write does not include read. Tick both for an assistant that edits.
- Every change is a normal Git commit, so you can review and revert it in page history.
- Hidden pages and templates are never visible to the assistant.

The full tool list is in [[MCP Tool Reference]].

## Common problems

- **401 Unauthorized.** The token is wrong, expired or revoked, or MCP is off. Check the token in **Settings → Access tokens**.
- **The assistant can read but not edit.** The token has no **write** access. Create a new token with read and write.
- **Connection refused or wrong address.** The base URL must match the address the assistant uses, and HMD must be restarted after turning MCP on.

## Next steps

[[MCP Tool Reference]] for every tool, [[LLM Wiki]] for an assistant-maintained knowledge base, and [[Authentication And Access]] for accounts and permissions.
