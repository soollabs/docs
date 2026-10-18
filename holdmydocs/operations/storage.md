---
title: Storage And Recovery
tags: hmd, operations
---

Where HMD keeps data, what to back up, and how to restore it.

## What HMD stores

HMD keeps everything in two folders. Back up both.

| Folder | Holds |
| --- | --- |
| `repo` | Your pages, attachments, and wiki and namespace settings, as a Git repository |
| `app` | Accounts, passwords (hashed), access tokens, OAuth connections, server settings, and a search index HMD rebuilds if lost |

- Keep `app` on a local disk, not a network share.
- Both folders must belong to the user running HMD and be private (`chmod 700`).
- Saves reach a Git remote a moment later, so the local `repo` can be ahead of it.

## Backup

Stop HMD, copy both folders, start it again. A remote Git repository is not a backup on its own: it has no accounts or settings.

Service install ([[Install HMD]]):

```sh
sudo systemctl stop hmd
sudo tar -czf "hmd-backup-$(date +%F).tar.gz" -C /var/lib/hmd app repo
sudo systemctl start hmd
```

Docker Compose install, run from the folder with `compose.local.yaml`:

```sh
docker compose -f compose.local.yaml stop
docker run --rm -v "$(basename "$PWD")_app:/data/app:ro" -v "$(basename "$PWD")_repo:/data/repo:ro" \
  -v "$PWD:/backup" alpine tar -czf "/backup/hmd-backup-$(date +%F).tar.gz" -C /data app repo
docker compose -f compose.local.yaml start
```

If the volume names differ, find them with `docker volume ls`.

- Keep backups private: they contain password hashes, token records and settings.
- Back up any secret files you configured, such as a Git token file, separately.
- Snapshots of both folders taken at the same moment work too, without stopping HMD.

## Restore

1. Stop HMD.
2. Unpack the backup in place of the current folders. For a service install:

   ```sh
   sudo tar -xzf hmd-backup-2026-10-18.tar.gz -C /var/lib/hmd
   sudo chown -R hmd:hmd /var/lib/hmd
   ```

3. Start the same HMD version the backup came from, then sign in and open a recent page.
4. If you use OAuth, clients revoked after the backup may work again. Disable and re-register them in **Settings → MCP OAuth clients** before reopening the wiki.

Try a restore on another machine now and then, so you know it works. Never test by overwriting the live folders.

If HMD logs `OAuth persistence is uncertain; restart required`, fix the disk problem and restart HMD. Do not delete `oauth.json`.
