---
title: Install HMD
tags: hmd, getting-started
---

Start a private HMD instance on your own computer with local storage. If someone has already installed HMD for you, skip to [[Your First Wiki]].

## What you need

- A Linux, macOS or Windows computer, or Docker.
- An administrator password of at least 12 characters, kept in a password manager.

Remove `HMD_ADMIN_USER` and `HMD_ADMIN_PASSWORD` after the first start; see [[Authentication And Access]].

You don't need a database, a Git hosting account or an AI service.

## Option 1: Release binary

Every release publishes a binary per platform and a `SHA256SUMS` file on the [releases page](https://github.com/soollabs/holdmydocs/releases).

1. Download the latest release for this machine and verify it (Linux and macOS):

   ```sh
   tag="$(curl -fsSLo /dev/null -w '%{url_effective}' https://github.com/soollabs/holdmydocs/releases/latest)"
   tag="${tag##*/}"
   os="$(uname -s | tr '[:upper:]' '[:lower:]')"
   case "$(uname -m)" in x86_64|amd64) arch=amd64 ;; aarch64|arm64) arch=arm64 ;; esac
   file="hmd-$tag-$os-$arch"
   curl -fsSLO "https://github.com/soollabs/holdmydocs/releases/download/$tag/$file"
   curl -fsSLO "https://github.com/soollabs/holdmydocs/releases/download/$tag/SHA256SUMS"
   sha256sum --ignore-missing -c SHA256SUMS   # macOS: shasum -a 256 --ignore-missing -c SHA256SUMS
   install -m 755 "$file" hmd
   ```

   On Windows, download `hmd-<tag>-windows-amd64.exe` and `SHA256SUMS` from the releases page, and compare the output of `Get-FileHash .\hmd-<tag>-windows-amd64.exe` with the matching line.

2. Create the data directories, generate and save a password, then run HMD in the foreground:

   ```sh
   install -d -m 700 ./data/app ./data/repo
   export HMD_ADMIN_PASSWORD="$(openssl rand -base64 18)"
   printf '%s\n' "$HMD_ADMIN_PASSWORD"
   HMD_SERVER_BIND=127.0.0.1:8080 \
   HMD_SERVER_REPO_DIR=./data/repo \
   HMD_APP_DIR=./data/app \
   HMD_ADMIN_USER=admin \
   ./hmd
   ```

3. In another terminal, run `curl -f http://127.0.0.1:8080/_/ready`, then open <http://127.0.0.1:8080> and sign in as `admin`.

   ![Local password sign-in screen](/_/attachments/holdmydocs/getting-started/install/login.png)

4. Follow [[First-Run Setup]] to name your wiki and create its first namespace.
5. Stop HMD with **Ctrl+C**. Later starts do not need the administrator variables:

   ```sh
   HMD_SERVER_BIND=127.0.0.1:8080 \
   HMD_SERVER_REPO_DIR=./data/repo \
   HMD_APP_DIR=./data/app \
   ./hmd
   ```

Keep both `data` folders: they hold your pages, accounts and settings. To keep HMD running after you log out and start it at boot, see **Run as a service** below.

## Option 2: Docker Compose

The image is `ghcr.io/soollabs/holdmydocs`, tagged with each release. Use a release tag: `latest` follows unreleased development.

1. Find the latest release tag:

   ```sh
   curl -fsSLo /dev/null -w '%{url_effective}\n' https://github.com/soollabs/holdmydocs/releases/latest
   ```

2. Create `compose.local.yaml` in an empty directory, replacing `<tag>` with that tag:

   ```yaml
   services:
     hmd:
       image: ghcr.io/soollabs/holdmydocs:<tag>
       ports:
         - "127.0.0.1:8080:8080"
       environment:
         HMD_ADMIN_USER: "${HMD_ADMIN_USER:-}"
         HMD_ADMIN_PASSWORD: "${HMD_ADMIN_PASSWORD:-}"
       volumes:
         - repo:/data/repo
         - app:/data/app
       restart: unless-stopped

   volumes:
     repo:
     app:
   ```

   `127.0.0.1` keeps the wiki reachable only from this computer. The two volumes keep your pages and accounts when the container is replaced. For a hardened setup with Git sync and document search, start from the `docker-compose.yaml` in the [source repository](https://github.com/soollabs/holdmydocs).

3. Generate a password and start HMD:

   ```sh
   export HMD_ADMIN_USER=admin
   export HMD_ADMIN_PASSWORD="$(openssl rand -base64 18)"
   docker compose -f compose.local.yaml up -d
   ```

4. Save the password (`printf '%s\n' "$HMD_ADMIN_PASSWORD"` displays it), then check readiness:

   ```sh
   curl -f http://127.0.0.1:8080/_/ready
   ```

   If it is not ready, read the logs:

   ```sh
   docker compose -f compose.local.yaml logs --tail=100 hmd
   ```

5. Open <http://127.0.0.1:8080>, sign in as `admin` and follow [[First-Run Setup]].
The administrator variables are only read on the very first start. Later `docker compose` commands work without them.

## Option 3: Build from source

You need Git and the Go version named in the source's `go.mod`.

```sh
git clone https://github.com/soollabs/holdmydocs.git hmd
cd hmd
git checkout "$(git describe --tags --abbrev=0)"
go build -o hmd ./cmd/hmd
```

Then continue from step 2 of Option 1 above.

## Run as a service

On Linux, systemd keeps HMD running in the background, starts it at boot and restarts it after **Shut down**.

1. Create a user and data folders for HMD, and install the binary:

   ```sh
   sudo useradd --system --home-dir /var/lib/hmd --create-home hmd
   sudo install -d -m 700 -o hmd -g hmd /var/lib/hmd/app /var/lib/hmd/repo
   sudo install -m 755 hmd /usr/local/bin/hmd
   ```

   To keep the pages and accounts from your trial, stop it and copy them across first: `sudo cp -a data/app data/repo /var/lib/hmd/ && sudo chown -R hmd:hmd /var/lib/hmd`.

2. Create `/etc/systemd/system/hmd.service`:

   ```ini
   [Unit]
   Description=Hold My Docs
   After=network-online.target

   [Service]
   User=hmd
   Environment=HMD_SERVER_BIND=127.0.0.1:8080
   Environment=HMD_SERVER_REPO_DIR=/var/lib/hmd/repo
   Environment=HMD_APP_DIR=/var/lib/hmd/app
   ExecStart=/usr/local/bin/hmd
   Restart=always

   [Install]
   WantedBy=multi-user.target
   ```

   On a fresh install with no trial data, also add `Environment=HMD_ADMIN_USER=admin` and `Environment=HMD_ADMIN_PASSWORD=...` for the first start, then remove them.

3. Start it and check it:

   ```sh
   sudo systemctl enable --now hmd
   systemctl status hmd
   ```

Docker installs already restart automatically through `restart: unless-stopped`.

## Before exposing HMD to a network

These examples are local trials. Before sharing the wiki:

1. Put HTTPS in front of HMD and set its public URL and trusted proxies: [[Reverse Proxies]].
2. Review accounts, permissions and public namespaces: [[Authentication And Access]].
3. Back up both the content repository and application state, and test recovery: [[Storage And Recovery]].
4. Plan upgrades: [[Upgrade HMD]].

Add an HTTPS Git remote later with [[Git Sync]]. PDF and Office attachment search is optional; see [[Attachments]] for the Apache Tika requirements.

## Common pitfalls

- **Port 8080 is in use.** Docker: change the first `8080` in the port mapping, for example `127.0.0.1:8081:8080`. Binary: set `HMD_SERVER_BIND` to `127.0.0.1:8081`. Use the new port in the browser and readiness check.
- **`sha256sum: command not found` on macOS.** Use `shasum -a 256 --ignore-missing -c SHA256SUMS`.
- **`unsafe data directory` at startup.** The data folders must belong to the user running HMD and be private: `chmod 700` them. Do not make them more open.
- **First account not created.** Set both bootstrap variables with a unique password of at least 12 characters. HMD rejects weak or placeholder passwords; the startup logs give the reason.
- **Remote unavailable.** A local save can still be waiting for a background push. See [[Git Sync]].

## Stop or remove a local trial

- Docker: `docker compose -f compose.local.yaml down` stops the stack and keeps the volumes. Add `--volumes` only to delete all pages and accounts.
- Binary: stop the process. Delete `data/repo` and `data/app` only if you no longer need them or have a verified backup.

## Next steps

**Continue with [[First-Run Setup]], then [[Your First Wiki]].** If startup fails, use [[Troubleshooting]].
