---
title: Troubleshooting
tags: hmd, operations
---

Start with the process logs and `GET /_/ready`. Keep the request ID from a browser error and search the server log for it.

| Problem | Check | Fix |
| --- | --- | --- |
| HMD will not start | Read the named config error. | Correct the key or path. YAML rejects unknown keys. |
| `unsafe data directory` | Owner and mode of the app and repository paths. | Make them private directories owned by the service user. |
| Login redirects or CSRF 403 | Public URL, `server.base_url`, Origin and proxy TLS headers. | Set the canonical origin and narrow `server.trusted_proxies` CIDRs. |
| OIDC login fails | Issuer reachability, callback URL, admission rules and provider logs. | Correct the provider or HMD configuration, then restart. |
| Pages save locally but do not reach Git | Sync state and remote credentials. | Keep local commits, repair remote access, and push from the host if needed. |
| Bidirectional sync fails | Git history for divergence. | Resolve it outside HMD, then fast-forward the checkout. |
| Search is unavailable | `/_/ready` and the search index path. | Stop HMD, remove only the derived index files, then restart. |
| Document extraction fails | Private Tika URL, Tika logs and the 60-second HMD timeout. | Restore Tika or restrict it further. Attachments stay stored when extraction fails. |
| PAT or MCP returns 401/403 | Expiry, scopes, namespace allowlist and `mcp.enabled`. | Create or adjust a least-privilege token. Restart after enabling MCP. |

For recovery, see [[Storage And Recovery]]. For probes and logs, see [[Monitoring And Maintenance]]. For common questions, see the [[FAQ]].
