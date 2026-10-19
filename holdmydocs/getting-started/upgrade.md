---
title: Upgrade HMD
tags: hmd, getting-started, operations
---

Back up before every upgrade, and read the release notes for anything you need to change.

## Upgrade

1. Read the [release notes](https://github.com/soollabs/holdmydocs/releases) for the target release.
2. Stop HMD and back it up ([[Storage And Recovery]]).
3. Check the release notes for settings that changed, and update your configuration to match.
4. Update it the same way you installed it ([[Install HMD]]):
   - Release binary: download and verify the new release as in install step 1, then replace your `hmd` with it. For a service install: `sudo install -m 755 hmd /usr/local/bin/hmd`.
   - Docker Compose: change the tag in `image: ghcr.io/soollabs/holdmydocs:<tag>`, then run `docker compose -f compose.local.yaml pull` and `docker compose -f compose.local.yaml up -d`.
   - From source: `git checkout <tag>`, then rebuild with the Go version in that tag's `go.mod`.
5. Start HMD with the same data folders.
6. Sign in, open and save a page, and check the status bar shows sync is working.

After an upgrade administrators may see a **Help page changed** banner. It means the wiki's `.help.md` differs from the help text of the new version. Use **Reset to built-in** in the settings to take the new text, or dismiss the banner to keep your own.

## Roll back

- If the new version will not start, put the previous `hmd` binary or image tag back and start it with the same data folders.
- If it started and people saved pages, restore your backup instead, or keep the new version and fix the problem: going back loses those saves.
- Never run `git reset --hard` on the live repository.

See [[Storage And Recovery]] and [[Troubleshooting]].
