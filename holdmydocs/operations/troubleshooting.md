---
title: Troubleshooting
tags: hmd, operations
---

This page covers the common failure modes an operator meets, what to check first, and how to fix each one.

Start with the process logs and `GET /_/ready`. Keep the request ID from a browser error and search the server log for it.

| Problem | Check | Fix |
| --- | --- | --- |
| HMD will not start | Read the named config error. | Correct the key or path. YAML rejects unknown keys. |
| `unsafe data directory` | Inspect owner and mode of app and repository paths. | Restore or recreate them as private directories owned by the service user. |
| Login redirects or CSRF 403 | Compare the public URL, `base_url`, Origin, and proxy TLS headers. | Set the canonical origin and a narrow `trusted_proxies` CIDR. |
| OIDC login fails | Check issuer reachability, callback URL, admission rules, and provider logs. | Correct provider or HMD configuration, then restart. |
| Pages save locally but do not reach Git | Check sync state and remote credentials. | Preserve local commits, repair remote access, and push from the host if needed. |
| Bidirectional sync fails | Inspect Git history for divergence. | Resolve it outside HMD, then fast-forward the checkout. |
| Search is unavailable | Check `/_/ready` and the search index path. | Remove only derived index files while stopped, then restart. |
| Document extraction fails | Check the private Tika URL, Tika logs, and the 60-second HMD timeout. | Restore or further constrain Tika; attachments remain stored when extraction fails. |
| PAT or MCP returns 401/403 | Check expiry, scopes, namespace allowlist, and `mcp.enabled`. | Create or adjust a least-privilege token and restart after enabling MCP. |

For recovery, use [[Storage And Recovery]]. For probe and log details, use [[Monitoring And Maintenance]]. For quick answers to common questions, see the [[FAQ]].
