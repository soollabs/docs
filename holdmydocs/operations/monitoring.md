---
title: Monitoring And Maintenance
tags: hmd, operations
---

This page covers the log format, health endpoints, graceful shutdown, sync states, and what to alert on.

## Logs

HMD writes structured text logs to stderr. Request records have `request_id`, `method`, matched `route`, `status`, `bytes`, and `duration`. Queries, credentials, client addresses, and upload contents are not logged. Keep logs long enough to investigate a reported request ID: every browser error page carries one, and `grep <request_id>` finds the matching request record.

## Health endpoints

`GET /_/live` is unauthenticated and returns `200` when the process accepts requests. `GET /_/ready` is also unauthenticated and returns `200` only when the repository can be read and the search index is open; otherwise it returns `503`. Use the latter for deployment readiness:

```sh
curl -fsS https://wiki.example.com/_/live
curl -fsS https://wiki.example.com/_/ready
```

The Docker health check uses the same readiness check (the `-healthcheck` flag).

## Graceful shutdown

HMD handles `SIGINT` and `SIGTERM` by stopping new connections and allowing requests up to 30 seconds to finish. It then waits within the same deadline for asynchronous Git pushes started by completed saves before closing the search index.

## Sync states

The sync state is one of `ok`, `pending`, `failed`, or `no remote`. `no remote` means no remote is configured (the statusline shows "local only"); the other states appear once a remote is configured. A failed push, fetch, or divergent bidirectional pull leaves the local commit intact but needs operator action.

## Health report

`/_/health-report` is an authenticated wiki hygiene report, not a liveness check. It lists wiki-linked but missing pages, orphaned pages (no incoming links), and pages whose latest Git revision is at least 180 days old. Review its results before deleting pages.


## Alerting

Alert on readiness failures, repeated `sync failed` warnings, `panic serving request`, `graceful shutdown failed`, low disk space, and failed backups. HMD does not expose Prometheus metrics; collect these checks and logs in the monitoring system already used by the deployment.

## Failure guide

| Symptom | Action |
| --- | --- |
| Disk full | Stop writes, free space or restore capacity, then restart and verify `/_/ready`. |
| Git remote outage | Preserve the local repository, fix credentials or network access, then push from the host or wait for the next sync. |
| Divergent Git history | Resolve the divergence outside HMD and fast-forward the local checkout. Do not reset the live worktree. |
| Corrupt search index | Stop HMD, remove only the configured derived index and its `.manifest.json`, then start HMD to rebuild it. |
| Invalid config | Read the startup error, correct the named key, and restart. Unknown YAML keys fail deliberately. |
| OIDC outage | Use an existing local account if local login remains enabled; otherwise restore provider access. |
| Tika failure | Keep attachments, inspect Tika logs and network policy, then restart HMD after Tika passes `GET /tika`. A 60-second extraction timeout is reported as a skipped extraction. |

See [[Troubleshooting]] for install, proxy, access, and recovery checks.
