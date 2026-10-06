---
title: MCP Integration
tags: hmd, integrations, mcp
---

Connect a compatible MCP client to read and write your wiki over the Model Context Protocol, with the same scope and namespace restrictions as your tokens.

## Prerequisites

- An HMD instance reachable from the agent's network, with **MCP enabled**.
- A personal access token with the scopes you want to grant the agent.

## Enable the MCP endpoint

1. Set `HMD_MCP_ENABLED=true` and set `HMD_BASE_URL` to HMD's public origin, then restart HMD. The endpoint is served at `POST /_/mcp`:

   ```sh
   HMD_MCP_ENABLED=true
   HMD_BASE_URL=https://wiki.example.com
   ```

   `HMD_BASE_URL` is required whenever MCP is on. It must be a bare origin (scheme and host, no path), because HMD uses it to build the upload capability URLs it returns to the agent.

2. Create a personal access token in **Settings** with the scopes for the agent. MCP uses the same token store as the API.

3. Point the agent at the endpoint URL with the token as a Bearer credential:

   ```sh
   POST https://wiki.example.com/_/mcp
   Authorization: Bearer hmd_your_token
   MCP-Protocol-Version: 2026-07-28
   ```

   The client must support stateless Streamable HTTP requests with the `2026-07-28` protocol version and per-request client metadata. HMD does not support session headers, session query parameters or GET event streams. Check your client's protocol support before relying on it.

## How authentication works

The MCP endpoint never redirects to the login page the way a browser request does. A missing, malformed, or expired Bearer token returns **HTTP 401** with a JSON body like `{"error":"unauthorized"}`.

An authenticated token enforces exactly the scope and namespace restrictions from the token:

- **read** access provides `list_pages`, `read_page`, `list_namespaces`, `search`, `backlinks`, `recent_changes`, and `health`.
- **write** access adds `save_page`, `delete_page`, and `upload_attachment`.
- **write** access also adds `edit_page` for exact replacements and dry-run diffs.
- **settings** access provides `read_namespace` and `save_namespace`.
- `read_attachment` requires read access. When document search is enabled, `search_attachments` also requires read access.
- A token restricted to particular namespaces can only list, read, or write pages in those namespaces. `recent_changes` omits any commit that touches a file outside the caller's access.

HMD's MCP tools operate on ordinary pages only. Hidden pages and `.wiki.yaml` are outside the agent's reach.

## Write with optimistic locking

Each page carries a hash. Read a page first and pass its returned `hash` as `basehash` when you save; each successful save returns the new hash for the next update. If you save with a stale hash, HMD returns a conflict instead of silently overwriting another writer's changes. On conflict, re-read the page, merge, and retry with the fresh hash.

## Attach a file

1. Call `upload_attachment` with the owning page slug and the original filename. HMD returns three values:

   - `upload_url` — a one-use multipart upload URL
   - `attachment_url` — the URL of the uploaded file, under `/_/attachments/`
   - `expires_at` — the expiry time, 10 minutes later

2. POST the file to `upload_url` as multipart field `file`:

   ```sh
   curl -s -X POST https://wiki.example.com/_/api/attachment-uploads/TOKEN \
     -F "file=@report.pdf"
   ```

   The upload URL works once and expires after 10 minutes, so retry a fresh `upload_attachment` if you miss the window.

3. Add the returned `attachment_url` to the owning page with `save_page`. Use `[name](attachment_url)` for a link, or `![alt](attachment_url)` for an embedded image. Read the page first and send its hash as `basehash`.

When document search is enabled, HMD keeps a hidden, Git-tracked extracted text sidecar beside each uploaded source. `read_attachment` returns that cached text and `search_attachments` searches it. Plain Markdown and text sources get a sidecar automatically even when document search is off.

## Common pitfalls

- **The agent gets 401 after you create a token.** `HMD_BASE_URL` must match the origin the agent actually uses to reach you, and the token must include the scope the tools you call require.
- **Writes keep failing with a conflict.** You saved with a stale `basehash`. Re-read the page and retry; HMD never overwrites silently.
- **Hidden pages do not appear.** Draft pages, hidden templates, and `.wiki.yaml` are never visible to MCP tools.

## Next steps

The exact tool list and scope table: [[MCP Tool Reference]]. The agent-side pattern that combines these tools into a durable knowledge base: [[LLM Wiki]].
