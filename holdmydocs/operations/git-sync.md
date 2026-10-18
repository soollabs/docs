---
title: Git Sync
tags: hmd, operations, git
---

Every save and delete creates a local Git commit. With a remote configured, HMD pushes asynchronously after the write, so saving never waits on the network. With no remote, the statusline shows "local only" and saves still commit locally.

## Sync modes

| Mode | Behaviour |
| --- | --- |
| `push` (default) | Local changes push to the remote. HMD does not pull. |
| `bidirectional` | Fetches and fast-forwards before saves and on the sync poll. Divergent histories fail rather than creating merge commits. |

Set the mode in `config.yaml` (`git.sync_mode`) or at `/_/settings/git`, which also shows the current sync state:

![Git settings with remote and synchronisation controls](/_/attachments/holdmydocs/operations/git-sync/settings.png)

## Remotes

- Use an HTTPS remote. SSH remotes are not supported.
- Public repositories clone and fetch without a token. Private repositories and authenticated pushes need credentials.
- Supply the token as `HMD_GIT_TOKEN` or in a private file referenced by `git.token_file`. A token cannot be saved in `config.yaml` or entered in the UI, and a legacy `git.token` key is ignored.

See [[Configuration]].

## Read-only browsing

To browse the official documentation locally:

1. Start HMD:

   ```sh
   hmd_state="$(mktemp -d)"
   HMD_SERVER_BIND=127.0.0.1:8080 \
   HMD_APP_DIR="$hmd_state/app" \
   HMD_SERVER_REPO_DIR="$hmd_state/repo" \
   HMD_SERVER_READ_ONLY=true \
   HMD_GIT_REMOTE_URL=https://github.com/soollabs/docs.git \
   hmd
   ```

2. Open `http://127.0.0.1:8080/holdmydocs/`.

HMD clones the public repository without a GitHub token or bootstrap account and skips setup. Keep the state directory to reuse the clone, and stop HMD before deleting it.

- Read-only mode blocks content edits, uploads, setup, administrator operations and pushes, even for administrators.
- It fetches and fast-forwards in the background every `git.sync_poll_ms` (10 seconds by default), regardless of `git.sync_mode`. Reload the page to see updates.
- A failed fetch keeps the last local snapshot. Divergent histories are not merged, and uncommitted local changes are never discarded.
- A reused checkout's `origin` must match the configured URL. Use a fresh `server.repo_dir` for a different remote.
- For an existing local Git repository, set `HMD_SERVER_REPO_DIR` to its private checkout and omit `HMD_GIT_REMOTE_URL`. HMD then neither fetches nor pushes.
- A blank repository needs normal writable setup first. Read-only mode does not initialise it.
- Both the app directory and the repo directory need private, writable local storage.
- Private Git repositories need credentials, and private HMD namespaces need an authorised HMD account.

## Push failures

A failed push does not undo the local commit. Check the sync state and server logs, fix the remote problem (credentials, network, host availability), then push from the server if needed. See [[Monitoring And Maintenance]].

## Remote changes

In `bidirectional` mode, remote changes are pulled on the sync poll. If one reaches the page you are editing, your save shows the normal conflict screen. See [[Pages]].
