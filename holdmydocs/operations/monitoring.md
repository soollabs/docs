---
title: Monitoring And Maintenance
tags: hmd, operations
---

## Logs

HMD writes structured text logs to stderr. Request records have `request_id`, `method`, matched `route`, `status`, `bytes` and `duration`. Queries, credentials, client addresses and upload contents are not logged.

Every browser error page shows a request ID. Run `grep <request_id>` on the logs to find the matching record.

## Health endpoints

Both endpoints are unauthenticated.

| Endpoint | Returns |
| --- | --- |
| `GET /_/live` | `200` when the process accepts requests. |
| `GET /_/ready` | `200` when the repository can be read and the search index is open, otherwise `503`. Use this for deployment readiness. |

```sh
curl -fsS https://wiki.example.com/_/live
curl -fsS https://wiki.example.com/_/ready
```

While HMD starts, `/_/live` returns `200` and other requests get `503` with `Retry-After`. Browsers see a page that reloads itself once HMD is ready.

The Docker health check runs the same readiness check (the `-healthcheck` flag).

## Graceful shutdown

On `SIGINT` or `SIGTERM`, HMD stops accepting connections and gives requests up to 30 seconds to finish. Within the same deadline it waits for asynchronous Git pushes from completed saves, then closes the search index. **Shut down** in the top-bar menu (users with settings access) does the same.

## Sync states

| State | Meaning |
| --- | --- |
| `ok` | In sync with the remote. |
| `pending` | A sync is waiting or running. |
| `failed` | A push, fetch or divergent bidirectional pull failed. The local commit is intact but needs operator action. |
| `no remote` | No remote is configured. The statusline shows "local only". |

## Health report

`/_/health-report` is a wiki hygiene report for signed-in users. It lists:

- Pages that are wiki-linked but missing.
- Orphaned pages (no incoming links).
- Pages whose latest Git revision is at least 180 days old.

Review it before deleting pages.

![Health report with a missing page and an orphaned page](/_/attachments/holdmydocs/operations/monitoring/health.png)

## Alerting

Alert on:

- Readiness failures.
- Repeated `sync failed` warnings.
- `panic serving request` and `graceful shutdown failed`.
- Low disk space and failed backups.

HMD exposes no Prometheus metrics, so feed these checks and logs into your existing monitoring.

## Failure guide

| Symptom | Action |
| --- | --- |
| Disk full | Stop writes, free space or restore capacity, restart, then verify `/_/ready`. |
| Git remote outage | Keep the local repository, fix credentials or network access, then push from the host or wait for the next sync. |
| Divergent Git history | Resolve it outside HMD and fast-forward the local checkout. Do not reset the live worktree. |
| Corrupt search index | Stop HMD, remove only the configured derived index and its `.manifest.json`, then start HMD to rebuild it. |
| Invalid config | Read the startup error, fix the named key and restart. Unknown YAML keys fail deliberately. |
| OIDC outage | Use an existing local account if local login is still enabled, otherwise restore provider access. |
| Tika failure | Keep attachments, check Tika logs and network policy, then restart HMD once `GET /tika` passes. At startup HMD waits up to `server.tika_timeout` seconds for Tika before exiting. A 60-second extraction timeout is reported as a skipped extraction. |

See [[Troubleshooting]] for install, proxy, access and recovery checks.
