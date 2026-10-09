---
title: Git Sync
tags: hmd, operations, git
---

This page explains how HMD mirrors its content repository to a Git remote, what the two sync modes do, and what happens when a push or fetch fails.

Every save and delete creates a local Git commit. With a remote configured, HMD pushes asynchronously after the write, so saving never blocks on the network.

## Sync modes

- `push` (default) — local changes push to the remote; HMD does not pull.
- `bidirectional` — fetches and fast-forwards before saves and on the sync poll. Divergent histories fail rather than creating merge commits.

Set the mode in `config.yaml` (`sync_mode`) or at `/_/admin` under git remote, where the current sync state is shown:


## Remotes

Use an HTTPS remote. Public repositories can be cloned and fetched without a token; private repositories and authenticated pushes need suitable credentials. SSH remotes are not supported. Prefer a token file (`git.token_file`) or a secret-injection environment variable over a literal token in `config.yaml`. See [[Configuration]] for the secrets guidance.

With no remote configured, the statusline shows "local only" and every save still commits locally.

## Read-only browsing

Set `read_only: true` or `HMD_READ_ONLY=true` to browse without allowing edits or pushes. With a remote configured, HMD fetches and fast-forwards in the background at `sync_poll_ms` intervals, even when `sync_mode` is `push`. Without a remote, it only reads the existing local repository. Existing namespace visibility and authentication rules still apply. See [[First-Run Setup]] for the token-free official Docs example.

## Push failures

A failed push does not undo the local commit. Inspect the sync state and server logs, correct the remote problem (credentials, network, host availability), then push from the server if needed. The sync state and its history are described in [[Monitoring And Maintenance]].

## Remote changes

In `bidirectional` mode, remote changes are pulled into the working tree on the sync poll. If a remote change reaches the page being edited, the save hits the optimistic-lock check and shows the normal conflict screen. See [[Pages]].
