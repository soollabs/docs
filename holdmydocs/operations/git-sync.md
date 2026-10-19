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

## Read-only mirror

Read-only mode serves a Git repository without allowing any changes, for example to browse the official documentation locally:

```sh
mkdir -p -m 700 hmd-docs
HMD_SERVER_BIND=127.0.0.1:8080 \
HMD_APP_DIR=hmd-docs/app \
HMD_SERVER_REPO_DIR=hmd-docs/repo \
HMD_SERVER_READ_ONLY=true \
HMD_GIT_REMOTE_URL=https://github.com/soollabs/docs.git \
./hmd
```

Then open <http://127.0.0.1:8080/holdmydocs/>.

- No account or token is needed for a public repository. Private repositories need a Git token, and private namespaces still need a sign-in.
- Nobody can save pages, upload or change settings, administrators included. Signed-in users with write access can try the editor, but nothing is saved.
- HMD fetches updates every 10 seconds. Reload the page to see them.
- Keep `hmd-docs` to reuse the download next time. Use a new folder for a different repository.

## Push failures

A failed push does not undo the local commit. Check the sync state and server logs, fix the remote problem (credentials, network, host availability), then push from the server if needed. See [[Monitoring And Maintenance]].

## Remote changes

In `bidirectional` mode, remote changes are pulled on the sync poll. If one reaches the page you are editing, your save shows the normal conflict screen. See [[Pages]].
