---
title: Git Sync
tags: hmd, operations, git
---

This page explains how HMD mirrors its content repository to a Git remote, what the two sync modes do, and what happens when a push or fetch fails.

Every save and delete creates a local Git commit. With a remote configured, HMD pushes asynchronously after the write, so saving never blocks on the network.

## Sync modes

- `push` (default) — local changes push to the remote; HMD does not pull.
- `bidirectional` — fetches and fast-forwards before saves and on the sync poll. Divergent histories fail rather than creating merge commits.

Set the mode in `config.yaml` (`git.sync_mode`) or at `/_/settings/git`, where the current sync state is shown:

![Git settings with remote and synchronisation controls](/_/attachments/holdmydocs/operations/git-sync/settings.png)

## Remotes

Use an HTTPS remote. Public repositories can be cloned and fetched without a token; private repositories and authenticated pushes need suitable credentials. SSH remotes are not supported. Supply `HMD_GIT_TOKEN` or a private file referenced by `git.token_file`. A token cannot be saved in `config.yaml` or entered in the UI; a legacy `git.token` file key is ignored. See [[Configuration]].

With no remote configured, the statusline shows "local only" and every save still commits locally.

## Read-only browsing

To browse the official documentation locally with HMD:

```sh
hmd_state="$(mktemp -d)"
HMD_SERVER_BIND=127.0.0.1:8080 \
HMD_APP_DIR="$hmd_state/app" \
HMD_SERVER_REPO_DIR="$hmd_state/repo" \
HMD_SERVER_READ_ONLY=true \
HMD_GIT_REMOTE_URL=https://github.com/soollabs/docs.git \
hmd
```

Open `http://127.0.0.1:8080/holdmydocs/`. HMD clones the public repository without a GitHub token or bootstrap account, skips setup and lets you browse its public namespace. Keep the state directory to reuse the clone; stop HMD before deleting it.

Read-only mode blocks content edits, uploads, setup, administrator operations and pushes, even for administrators. It fetches and fast-forwards remote updates in the background at `git.sync_poll_ms` intervals (10 seconds by default), regardless of `git.sync_mode`. Reload the page to see updated content. Fetch failures retain the last local snapshot; divergent histories are not merged, and uncommitted local changes are never discarded to apply an update. If reusing a checkout, its `origin` must match the configured URL; use a fresh `server.repo_dir` for a different remote.

For an existing local Git repository, set `HMD_SERVER_REPO_DIR` to its private checkout and omit `HMD_GIT_REMOTE_URL`. Without a remote, HMD does not fetch or push. A blank local or remote repository needs normal writable setup first; read-only mode does not initialise it.

Read-only mode still writes application state and updates the cloned snapshot and Git metadata, so both directories need private, writable local storage. Private Git repositories need credentials, and private HMD namespaces require an authorised HMD account.

## Push failures

A failed push does not undo the local commit. Inspect the sync state and server logs, correct the remote problem (credentials, network, host availability), then push from the server if needed. The sync state and its history are described in [[Monitoring And Maintenance]].

## Remote changes

In `bidirectional` mode, remote changes are pulled into the working tree on the sync poll. If a remote change reaches the page being edited, the save hits the optimistic-lock check and shows the normal conflict screen. See [[Pages]].
