---
title: MCP Integration
tags: hmd, integrations, mcp, oauth
---

Connect an AI assistant such as Claude Code to your wiki over MCP, so it can search, read and edit pages.

An assistant connects in one of two ways. Pick the one that suits it:

| | Access token | OAuth |
| --- | --- | --- |
| How it signs in | You create a token in HMD and paste it into the assistant's settings. | The assistant opens a browser window, you sign in to HMD and approve it. |
| Administrator setup | Turn on MCP. | Turn on MCP and OAuth, and register the assistant. |
| Works with | Any MCP client that can send a header. | MCP clients that support OAuth sign-in. |

## Turn on MCP

An administrator does this once.

1. Open **Settings → Server** and set **base URL** to the address people use for the wiki, for example `https://wiki.example.com` (no path).
2. Open **Settings → MCP** and tick **enable MCP**.
3. For OAuth, also tick **enable OAuth for MCP clients**. OAuth needs HTTPS.
4. Save and restart HMD.

The MCP address is your base URL followed by `/_/mcp`, for example `https://wiki.example.com/_/mcp`.

## Connect with an access token

1. Open **Settings → Access tokens**.
2. Name the token after the assistant, for example `claude-code`.
3. Tick **read** to let it search and read, and **write** to let it edit. Tick namespaces to limit it to those; leave them all unticked for every namespace.
4. Click **Create token** and copy the value. It is shown once.
5. Add the server to your assistant with the token.

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

Ask the assistant to list your namespaces to check the connection. See [[Personal Access Tokens]] for expiry and revocation.

## Connect with OAuth

OAuth must be turned on and the assistant registered first (see Register OAuth clients below).

1. Add the server address to your assistant without a token.
2. When it connects, a browser window opens. Sign in to HMD.
3. The approval page shows the assistant and what it asks for. Approve the actions and namespaces you want it to have.

To disconnect, open **Settings → Connected applications**. Access stops immediately. Each connection lasts 30 days, then you approve again.

Some assistants ask only for read. To let one edit, set its requested scope to `read write`, make sure its registration allows both, and reconnect.

## Register OAuth clients

An administrator registers each assistant in **Settings → MCP OAuth clients**.

1. Enter the assistant's name, its callback URLs (exactly as its documentation gives them) and the actions it may request.
2. Copy the client ID, and the secret if one is shown, into the assistant. The secret is shown once.

To replace a lost secret, register the assistant again, update it with the new details, then click **Disable client** on the old registration. Disabling is permanent and disconnects everyone using it.

Some assistants can register themselves. To allow that, turn on **allow dynamic client registration** in **Settings → MCP** and restart. Anyone who can reach HMD can then register a client (up to 32), so delete any you do not recognise. A registered client still cannot read anything until a user signs in and approves it.

With HMD stopped, you can also register and disable clients from the command line:

```sh
hmd -oauth-client-add \
  -oauth-client-name "Example MCP client" \
  -oauth-client-redirect-uri "https://client.example/callback" \
  -oauth-client-auth-method none \
  -oauth-client-scopes read,write

hmd -oauth-client-disable -oauth-client-id "CLIENT_ID"
```

Repeat `-oauth-client-redirect-uri` for each callback. Use `none` for clients without a secret, or `client_secret_basic` for clients with one.

Turning OAuth off ends every OAuth connection, and turning it back on does not restore them. OAuth connections are kept in the application directory; see [[Storage And Recovery]] for backup and restore.

## What the assistant can do

Tokens and OAuth use the same access levels.

| Access | The assistant can |
| --- | --- |
| read | List, read and search pages, follow backlinks, see recent changes, run the health report, read attachment text |
| write | Create, edit and delete pages, upload attachments |
| admin | Read and change namespace settings, in every namespace |

- Write does not include read. Give both to an assistant that edits.
- OAuth offers admin only when **allow administrator delegation** is on.
- Every change is a normal Git commit, so you can review and revert it in page history.
- Hidden pages and templates are never visible to the assistant.

## Common problems

| Problem | Fix |
| --- | --- |
| `401 Unauthorized` | The token is wrong, expired or revoked, or MCP is off. Check it in **Settings → Access tokens**. |
| The assistant can read but not edit | It has no **write** access. Create a token with read and write, or reconnect over OAuth asking for `read write`. |
| Connection refused or wrong address | Make the base URL match the address the assistant uses, and restart HMD after turning MCP on. |
| OAuth will not start on a local test instance | Over plain HTTP on `127.0.0.1`, turn on **allow insecure loopback**. Never use it on a public address. |

## Next steps

[[MCP Tool Reference]] for every tool, and [[LLM Wiki]] for an assistant-maintained knowledge base.
