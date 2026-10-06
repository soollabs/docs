---
title: Upgrade HMD
tags: hmd, getting-started, operations
---

Move a running instance to a newer HMD release without losing content, state, or the ability to roll back.

When building from source, use the Go version required by the target release's `go.mod`. Upgrade one release at a time unless the release notes say otherwise. Test reverse-proxy, OIDC, or storage changes in a restored staging copy first.

1. Read the release notes and pin the target image digest or binary checksum.
2. Back up `repo`, `app`, and external secret files. Confirm the Git remote has the current local commit.
3. Stop HMD cleanly. For Compose, pull the pinned image or rebuild the pinned source revision, then run `docker compose up -d`; for a binary, replace it atomically while stopped. `docker compose pull` alone does not update a service configured with `build: .`.
4. Start HMD with the same data paths and service account. Do not change old root-owned volume ownership; restore into fresh UID/GID 65532-owned volumes.
5. Check logs, `/_/ready`, local login, OIDC login, a page save, attachment download, sync status, and static export before declaring the upgrade done.

If the new version fails before writing data, stop it and redeploy the previous pinned artefact with the unchanged data directories. If it has written commits, preserve the repository and investigate before rolling back. Never use `git reset --hard` against the live repository as a rollback method.

After a rollback, run the same readiness, login, page, attachment, and sync checks.

## Common pitfalls

- Never change volume ownership in place. Old root-owned volumes must be restored into fresh UID/GID `65532`-owned volumes, not `chown`ed.
- Never use `git reset --hard` against the live repository as a rollback method; it discards commits.

See [[Storage And Recovery]] and [[Troubleshooting]].
