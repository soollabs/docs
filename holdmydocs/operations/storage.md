---
title: Storage And Recovery
tags: hmd, operations
---

This page describes where HMD keeps data, what must be backed up, and the tested restore procedure.

## Storage classes

HMD has two storage classes:

```text
repo/                 Authoritative Git content: pages, attachments, wiki and namespace config
app/users.json        Authoritative accounts, password hashes, PAT digests, preferences
app/config.yaml       Local instance configuration
app/sessions.json     Disposable active sessions
app/search.bleve*     Rebuildable search index and manifest
app/models/           Rebuildable downloaded embedding model
```

Keep `app` on local disk. HMD updates account and session state with in-process locking and atomic rename writes, and the repository needs real Git filesystem semantics; the bundled Compose file documents the same requirement for the app directory. Both directories must be private and owned by the HMD service account. The repository can be backed by NFS only if its Git filesystem semantics are known until the remote has accepted it.

## Backup

1. Confirm the sync state is healthy and record `git -C repo rev-parse HEAD`.
2. Stop HMD or take filesystem-consistent snapshots of both directories.
3. Back up the full Git repository, including `.git`, and `app/users.json` and `app/config.yaml`. Include secret files referenced by configuration in a separate protected secret backup.
4. Treat backup access as administrative access. `users.json`, configuration, and secret files must not enter a public repository.

## Restore drill

1. Restore `repo` and `app` to new directories owned by the service account, both mode `0700`. Restore secret files with mode `0600`.
2. Start the same HMD version with `HMD_REPO_DIR` and `HMD_APP_DIR` pointing at those directories.
3. Check `/_/ready`, sign in with a known local account, open a recent page, and run `git -C repo fsck --full` and `git -C repo log -1`.
4. Check the sync state before allowing writes. Rebuildable index and model data may be absent; HMD recreates them.

This procedure was tested end to end on a demo instance: restoring both directories into fresh mode-0700 directories and starting the same version reproduced accounts, pages, and the exact Git history (`fsck --full` clean, HEAD matching the pre-restore snapshot). Test the same procedure periodically on an isolated host. Do not test a restore by overwriting the live data directories.
