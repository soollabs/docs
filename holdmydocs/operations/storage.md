---
title: Storage And Recovery
tags: hmd, operations
---

Where HMD keeps data, what to back up, and how to restore it.

## Storage classes

```text
repo/                 Authoritative Git content: pages, attachments, wiki and namespace config
app/users.json        Authoritative accounts, password hashes, PAT digests, preferences
app/oauth.json        OAuth clients, grants, token digests, replay and revocation state (retain when present)
app/config.yaml       Local instance configuration
app/sessions.json     Disposable active sessions
app/search.bleve*     Rebuildable search index and manifest
app/models/           Rebuildable downloaded embedding model
```

- Keep `app` on local disk. The repository needs real Git filesystem semantics.
- Both directories must be private and owned by the HMD service account.
- Use NFS for the repository only after verifying it supports Git's locking and atomic file operations.
- Back up local commits even when a remote is configured. They are not mirrored until the remote accepts the push.

## Backup

1. Confirm the sync state is healthy and record `git -C repo rev-parse HEAD`.
2. Stop HMD or take filesystem-consistent snapshots of both directories.
3. Back up the full Git repository including `.git`, plus `app/users.json`, `app/config.yaml` and `app/oauth.json` whenever it exists, even if OAuth is disabled.
4. Back up secret files referenced by configuration separately, in protected storage.
5. Treat backup access as administrative access. Keep `users.json`, configuration, OAuth state and secret files out of public repositories.

## Restore

1. Restore `repo` and `app` to new directories owned by the service account, both mode `0700`. Restore secret files with mode `0600`.
2. Start the same HMD version with `HMD_SERVER_REPO_DIR` and `HMD_APP_DIR` pointing at those directories.
3. Check `/_/ready`, sign in with a known local account, open a recent page, and run `git -C repo fsck --full` and `git -C repo log -1`.
4. Check the sync state before allowing writes. HMD recreates missing index and model data.
5. If you restored OAuth state from an older snapshot, revoked or rotated credentials may be active again. Before exposing the instance, stop HMD and disable affected clients with `hmd -oauth-client-disable -oauth-client-id "CLIENT_ID"`. Provision replacement clients and require fresh user consent.

Test the restore periodically on an isolated host. Never test by overwriting the live data directories. On OAuth-enabled instances, also verify restored client registrations, grant expiry, refresh generations and revocations against the snapshot.

## OAuth state failures

OAuth state is not cache data. After an uncertain persistence failure replacing `oauth.json`, OAuth fails closed until HMD restarts. Fix the filesystem problem, keep the state file, and restart HMD. Do not delete `oauth.json` to clear the error. See [[MCP OAuth]].
