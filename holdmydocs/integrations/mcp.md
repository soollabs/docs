---
title: MCP Integration
tags: hmd, integrations, mcp
---

Connect an MCP client to read and write your wiki. Access is limited to the scope and namespaces of its credential.

## Prerequisites

- An HMD instance reachable from the agent's network, with MCP enabled.
- A personal access token (PAT) or an OAuth connection with the scopes you want to grant. OAuth setup is in [[MCP OAuth]].

## Enable the MCP endpoint

1. Set these and restart HMD. The endpoint is served at `POST /_/mcp`:

   ```sh
   HMD_MCP_ENABLED=true
   HMD_SERVER_BASE_URL=https://wiki.example.com
   ```

   `HMD_SERVER_BASE_URL` is required when MCP is on. It must be a bare origin (scheme and host, no path), because HMD builds upload URLs from it.

2. Choose a credential:

   - PAT: create a personal access token in **Settings** with the scopes the client needs. MCP uses the same token store as the API.
   - OAuth: follow [[MCP OAuth]].

3. Point the agent at the endpoint with a Bearer credential:

   ```http
   POST https://wiki.example.com/_/mcp
   Authorization: Bearer ACCESS_TOKEN
   ```

HMD supports stateless Streamable HTTP, protocol versions `2026-07-28`, `2025-11-25`, `2025-06-18` and `2025-03-26`. Use a compatible MCP SDK rather than building messages by hand.

- `2026-07-28` uses `server/discover` and per-request metadata (protocol version, client information, client capabilities). It requires the matching `MCP-Protocol-Version` header.
- The `2025` versions use `initialize`, then `notifications/initialized`, then tool requests. The first request can omit the version header. Later requests should send the negotiated version; without it HMD falls back to `2025-03-26`.
- No persistent sessions, no GET event streams, and no legacy HTTP+SSE transport.

## Authentication and access

Unauthenticated requests never redirect to the login page. With OAuth enabled they return HTTP 401 with the protected-resource metadata challenge. A missing, malformed or expired Bearer token returns `{"error":"unauthorized"}`. OAuth access tokens work only for `/_/mcp`, not as PATs.

Each request is limited to the credential's bounds intersected with the user's current permissions. OAuth also checks the live grant and client policy.

| Access | Tools |
| --- | --- |
| read | `list_pages`, `read_page`, `list_namespaces`, `search`, `backlinks`, `recent_changes`, `health`, `read_attachment`, and `search_attachments` when document search is enabled |
| write | `save_page`, `delete_page`, `upload_attachment`, `edit_page` (exact replacements and dry-run diffs) |
| settings | `read_namespace`, `save_namespace` |

- Write does not imply read. Request both when you need both.
- Settings implies read and write and bypasses namespace restrictions.
- A namespace-restricted token can only list, read or write pages in those namespaces. `recent_changes` omits any commit that touches a file outside the caller's access.
- OAuth tool errors name the missing scope or namespace.
- Some MCP applications request only `read` by default. To allow editing, set the application's OAuth scopes to `read write`, allow both actions in its HMD registration, and reconnect to grant consent.
- Tools see ordinary pages only. Hidden pages, draft pages, hidden templates and `.wiki.yaml` are not visible.

## Write with optimistic locking

1. Read the page and note its `hash`.
2. Pass it as `basehash` when you save. Each save returns the new hash.
3. On a conflict (stale hash), re-read the page, merge, and retry with the fresh hash.

## Attach a file

1. Call `upload_attachment` with the owning page slug and the original filename. It returns:

   - `upload_url`: a one-use multipart upload URL
   - `attachment_url`: the file's URL, under `/_/attachments/`
   - `expires_at`: 10 minutes after the call

2. POST the file to `upload_url` as multipart field `file`. Request a fresh URL if it expires:

   ```sh
   curl -s -X POST https://wiki.example.com/_/api/attachment-uploads/TOKEN \
     -F "file=@report.pdf"
   ```

3. Add `attachment_url` to the page with `save_page`, sending the page's hash as `basehash`. Use `[name](attachment_url)` for a link or `![alt](attachment_url)` for an image.

When document search is enabled, HMD keeps a hidden, Git-tracked text sidecar beside each uploaded source. `read_attachment` returns that text and `search_attachments` searches it. Plain Markdown and text sources get a sidecar even when document search is off.

## Common pitfalls

- **401 after creating a token.** `HMD_SERVER_BASE_URL` must match the origin the agent uses, and the token needs the scope the tools require.
- **Writes keep conflicting.** You saved with a stale `basehash`. Re-read and retry.

## Next steps

The tool list and scope table: [[MCP Tool Reference]]. The agent-side pattern for a durable knowledge base: [[LLM Wiki]].
