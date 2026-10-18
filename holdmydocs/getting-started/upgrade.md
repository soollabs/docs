---
title: Upgrade HMD
tags: hmd, getting-started, operations
---

Upgrade one release at a time unless the release notes say otherwise. Test reverse-proxy, OIDC or storage changes on a restored staging copy first. When building from source, use the Go version in the target release's `go.mod`.

## Upgrade

1. Read the release notes and pin the target image digest or binary checksum.
2. Back up `repo`, `app` and external secret files. Confirm the Git remote has the current local commit.
3. Stop HMD cleanly.
4. Update it:
   - Compose install from [[Install HMD]]: pull the pinned image or rebuild the pinned source revision, then run `docker compose -f compose.local.yaml up -d`. Use the same Compose file for every command. `pull` alone does not update a service configured with `build: .`.
   - Binary: replace it atomically while stopped.
5. Start HMD with the same data paths and service account. Do not change ownership of old root-owned volumes; restore into fresh volumes owned by UID/GID 65532.
6. Check the logs, `/_/ready`, local login, OIDC login, a page save, an attachment download, sync status and static export.

Compare your configuration with [[Configuration Reference]] first. HMD does not migrate configuration files or environment variables. Supply secrets through environment variables or secret files, not `config.yaml`.

## Roll back

- If the new version failed before writing data, stop it and redeploy the previous pinned artefact with the unchanged data directories.
- If it has written commits, keep the repository and investigate before rolling back.
- Never use `git reset --hard` on the live repository to roll back.

Then repeat the step 6 checks.

See [[Storage And Recovery]] and [[Troubleshooting]].
