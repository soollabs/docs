---
title: MCP Integration
tags: hmd, integrations, mcp
---

Connect an AI assistant such as Claude Code to your wiki over MCP, so it can search, read and edit pages. It can only reach what its token allows.

## 1. Turn on MCP

An administrator does this once.

1. Open **Settings → Server** and set **base URL** to the address people use for the wiki, for example `https://wiki.example.com` (no path).
2. Open **Settings → MCP**, tick **enable MCP** and save.
3. Restart HMD.

The MCP address is your base URL followed by `/_/mcp`, for example `https://wiki.example.com/_/mcp`.

## 2. Create a token for the assistant

1. Open **Settings → Access tokens**.
2. Name the token after the assistant, for example `claude-code`.
3. Tick **read** to let it search and read, and **write** to let it edit. Tick namespaces to limit it to those; leave them all unticked for every namespace.
4. Click **Create token** and copy the value. It is shown once.

See [[Personal Access Tokens]] for expiry and revocation. To sign in through the browser instead of pasting a token, an administrator can set up [[MCP OAuth]].

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

## What the assistant can do

| Token access | The assistant can |
| --- | --- |
| read | List, read and search pages, follow backlinks, see recent changes, run the health report, read attachment text |
| write | Create, edit and delete pages, upload attachments |
| settings | Read and change namespace settings, in every namespace |

- Write does not include read. Tick both for an assistant that edits.
- Every change is a normal Git commit, so you can review and revert it in page history.
- Hidden pages and templates are never visible to the assistant.

The full tool list is in [[MCP Tool Reference]].

## Common problems

- **401 Unauthorized.** The token is wrong, expired or revoked, or MCP is off. Check the token in **Settings → Access tokens**.
- **The assistant can read but not edit.** The token has no **write** access. Create a new token with read and write.
- **Connection refused or wrong address.** The base URL must match the address the assistant uses, and HMD must be restarted after turning MCP on.

## Next steps

[[MCP Tool Reference]] for every tool, and [[LLM Wiki]] for an assistant-maintained knowledge base.
