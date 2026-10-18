---
title: Install HMD
tags: hmd, getting-started
---

Start a private HMD instance on your own computer with local storage. If someone has already installed HMD for you, skip to [[Your First Wiki]].

## What you need

- Git.
- Docker Engine with the Compose plugin, or Go 1.27.2 or newer.
- OpenSSL to generate a password, and a password manager to store it.
- Two persistent directories or volumes: one for content, one for application state. Application state must be on local disk, not NFS.
- Free local port `8080` and a unique administrator password of at least 12 characters.

You do not need a remote Git repository, a database service, an AI account or Apache Tika.

## Option 1: Docker Compose

### Quick trial

1. Clone the source, generate a password and start HMD:

   ```sh
   git clone https://github.com/soollabs/holdmydocs.git hmd
   cd hmd
   export HMD_ADMIN_USER=admin
   export HMD_ADMIN_PASSWORD="$(openssl rand -base64 18)"
   docker compose up -d --build
   curl -f http://127.0.0.1:8080/_/ready
   ```

2. Save the password in your password manager. `printf '%s\n' "$HMD_ADMIN_PASSWORD"` displays it.
3. Open <http://127.0.0.1:8080>, sign in and continue with [[First-Run Setup]].

The included Compose file needs both variables on every `docker compose` command, including `down`. In a new terminal, export the same username and password first. Stop the trial with `docker compose down` (no `--volumes`) to keep your pages and account. Do not run this stack and the one below against the same volumes.

### Longer-running installation

1. Clone the source. For production, check out the release revision you intend to run.

   ```sh
   git clone https://github.com/soollabs/holdmydocs.git hmd
   cd hmd
   ```

2. In the `hmd` directory, create `compose.local.yaml`. It has no Git remote credentials; the repository's `docker-compose.yaml` covers remote sync and document extraction.

   ```yaml
   services:
     hmd:
       build: .
       ports:
         - "127.0.0.1:8080:8080"
       environment:
         GOMEMLIMIT: 384MiB
         HMD_ADMIN_USER: "${HMD_ADMIN_USER:-}"
         HMD_ADMIN_PASSWORD: "${HMD_ADMIN_PASSWORD:-}"
       volumes:
         - repo:/data/repo
         - app:/data/app
       user: "65532:65532"
       read_only: true
       cap_drop: [ALL]
       security_opt: [no-new-privileges:true]
       init: true
       restart: unless-stopped
       cpus: 1.0
       mem_limit: 512m
       pids_limit: 128
       tmpfs:
         - /tmp:size=64m,mode=1777,nosuid,nodev,noexec

   volumes:
     repo:
     app:
   ```

   The loopback binding makes the wiki reachable only from this computer. The named volumes keep content and accounts when the container is replaced.

3. Generate a password and start HMD:

   ```sh
   export HMD_ADMIN_USER=admin
   export HMD_ADMIN_PASSWORD="$(openssl rand -base64 18)"
   docker compose -f compose.local.yaml up -d --build
   ```

4. Save the password (`printf '%s\n' "$HMD_ADMIN_PASSWORD"` displays it), then check readiness:

   ```sh
   curl -f http://127.0.0.1:8080/_/ready
   ```

   If it is not ready, read the logs:

   ```sh
   docker compose -f compose.local.yaml logs --tail=100 hmd
   ```

5. Open <http://127.0.0.1:8080> and sign in as `admin`.

   ![Local password sign-in screen](/_/attachments/holdmydocs/getting-started/install/login.png)

6. Follow [[First-Run Setup]] to name your wiki and create its first namespace.
7. Remove the bootstrap credentials. The account is stored in the `app` volume, so the variables are no longer needed:

   ```sh
   unset HMD_ADMIN_USER HMD_ADMIN_PASSWORD
   docker compose -f compose.local.yaml up -d --force-recreate
   ```

   Sign in again to confirm. Keep the `app` volume: removing it deletes your accounts and local settings.

## Option 2: Bare binary

1. Build HMD and create the data directories:

   ```sh
   git clone https://github.com/soollabs/holdmydocs.git hmd
   cd hmd
   go build -o hmd ./cmd/hmd
   install -d -m 700 ./data/app ./data/repo
   ```

2. Generate and save a password, then run HMD in the foreground:

   ```sh
   export HMD_ADMIN_PASSWORD="$(openssl rand -base64 18)"
   printf '%s\n' "$HMD_ADMIN_PASSWORD"
   HMD_SERVER_BIND=127.0.0.1:8080 \
   HMD_SERVER_REPO_DIR=./data/repo \
   HMD_APP_DIR=./data/app \
   HMD_ADMIN_USER=admin \
   ./hmd
   ```

3. In another terminal, run `curl -f http://127.0.0.1:8080/_/ready`, then open <http://127.0.0.1:8080>, sign in and complete [[First-Run Setup]].
4. Stop HMD with **Ctrl+C** and run `unset HMD_ADMIN_PASSWORD`. Later starts omit the bootstrap credentials:

   ```sh
   HMD_SERVER_BIND=127.0.0.1:8080 \
   HMD_SERVER_REPO_DIR=./data/repo \
   HMD_APP_DIR=./data/app \
   ./hmd
   ```

Both data directories must be owned by the account running HMD, must not overlap and must stay at mode `0700`. For long-running use, run HMD under a dedicated service account and a process supervisor.

## Before exposing HMD to a network

These examples are local trials. Before sharing the wiki:

1. Put HTTPS in front of HMD and set its public URL and trusted proxies: [[Reverse Proxies]].
2. Review accounts, permissions and public namespaces: [[Authentication And Access]].
3. Back up both the content repository and application state, and test recovery: [[Storage And Recovery]].
4. Pin a release revision or image and plan upgrades: [[Upgrade HMD]].

Add an HTTPS Git remote later with [[Git Sync]]. PDF and Office attachment search is optional; see [[Attachments]] for the Apache Tika requirements.

## Common pitfalls

- **Port 8080 is in use.** Docker: change the first `8080` in the port mapping, for example `127.0.0.1:8081:8080`. Binary: set `HMD_SERVER_BIND` to `127.0.0.1:8081`. Use the new port in the browser and readiness check.
- **Unsafe data directory.** The service account must own both directories at mode `0700`. Do not loosen permissions. For old root-owned container volumes, see [[Storage And Recovery]].
- **First account not created.** Set both bootstrap variables with a unique password of at least 12 characters. HMD rejects weak or placeholder passwords; the startup logs give the reason.
- **Remote unavailable.** A local save can still be waiting for a background push. See [[Git Sync]].

## Stop or remove a local trial

- Docker: `docker compose -f compose.local.yaml down` stops the stack and keeps the volumes. Add `--volumes` only to delete all pages and accounts.
- Binary: stop the process. Delete `data/repo` and `data/app` only if you no longer need them or have a verified backup.

## Next steps

**Continue with [[First-Run Setup]], then [[Your First Wiki]].** If startup fails, use [[Troubleshooting]].
