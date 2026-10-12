---
title: Install HMD
tags: hmd, getting-started
---

Start a private HMD instance on your own computer. This guide uses local storage so you can try the editor without setting up a Git host, a domain, or an external service.

Choose **Docker Compose** if you use containers, or **a bare binary** if you want to run the Go application directly. Both paths end at the same sign-in screen. If someone has already installed HMD for you, skip to [[Your First Wiki]].

## What you need

- Git to download the source.
- Docker Engine with the Compose plugin, or Go 1.27.2 or newer to build locally.
- OpenSSL to generate a password, and a password manager to record it.
- Two persistent directories or volumes: one for content, one for application state. Application state must be on local disk, not NFS.
- An unused local port `8080` and a unique administrator password of at least 12 characters.

You do **not** need a remote Git repository, a separate database service, an AI account, or Apache Tika. Those are not prerequisites for writing pages.

## Option 1: Docker Compose

### Quick trial

For a short local trial, use the repository's `docker-compose.yaml`. Clone the source and generate a password:

```sh
git clone https://github.com/soollabs/holdmydocs.git hmd
cd hmd
export HMD_ADMIN_USER=admin
export HMD_ADMIN_PASSWORD="$(openssl rand -base64 18)"
docker compose up -d --build
curl -f http://127.0.0.1:8080/_/ready
```

Record the generated password in your password manager. Run `printf '%s\n' "$HMD_ADMIN_PASSWORD"` to display it in this terminal, then open <http://127.0.0.1:8080>, sign in and continue with [[First-Run Setup]].

The included Compose file requires both environment variables on every `docker compose` command, including `down`, although HMD uses them only to create the first administrator. Keep this terminal open. In a new terminal, export the same username and saved password before running Compose.

Stop the trial with `docker compose down` without `--volumes` to keep your pages and account. For a longer-running installation, use the `compose.local.yaml` example below so you can remove the bootstrap credentials from the environment. Do not run both stacks against the same data volumes.

### Longer-running installation

### Download HMD

```sh
git clone https://github.com/soollabs/holdmydocs.git hmd
cd hmd
```

For a production deployment, check out the release revision you intend to run rather than following the moving default branch.

### Create a local configuration

In the cloned `hmd` directory, create a file named `compose.local.yaml` with this content. This local-only example deliberately leaves out Git remote credentials; the repository's `docker-compose.yaml` is a separate example for remote sync and optional document extraction.

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

The loopback binding makes the wiki accessible only from this computer. Named volumes keep your content and accounts when the container is replaced.

The container runs as an unprivileged user with a read-only container filesystem, no Linux capabilities and no privilege escalation. CPU, memory and process limits bound resource use; `tmpfs` provides temporary writable storage without executable files. HMD still saves pages and account state to the mounted volumes.

### Start HMD

Generate a unique password by running these commands from the cloned `hmd` directory:

```sh
export HMD_ADMIN_USER=admin
export HMD_ADMIN_PASSWORD="$(openssl rand -base64 18)"
docker compose -f compose.local.yaml up -d --build
```

Record the password in your password manager; `printf '%s\n' "$HMD_ADMIN_PASSWORD"` displays it in this terminal. The first build downloads dependencies and compiles HMD. When the container has started, check readiness:

```sh
curl -f http://127.0.0.1:8080/_/ready
```

A successful response means HMD can read its repository and its search index is open. If it is not ready yet, inspect startup logs:

```sh
docker compose -f compose.local.yaml logs --tail=100 hmd
```

### Sign in

Open <http://127.0.0.1:8080> and sign in as `admin` with the password you chose.

![Local password sign-in screen](/_/attachments/holdmydocs/getting-started/install/login.png)

After a successful sign-in, follow [[First-Run Setup]] to name your wiki and create its first namespace.

### Remove the bootstrap credentials

The environment variables create the first administrator; the account is persisted in the `app` volume. After confirming sign-in works, remove those variables and recreate the container so it no longer holds them:

```sh
unset HMD_ADMIN_USER HMD_ADMIN_PASSWORD
docker compose -f compose.local.yaml up -d --force-recreate
```

Sign in again to confirm the saved account still works. Keep the `app` volume: removing it removes your accounts and local settings.

## Option 2: Bare binary

Download and build the source:

```sh
git clone https://github.com/soollabs/holdmydocs.git hmd
cd hmd
go build -o hmd ./cmd/hmd
install -d -m 700 ./data/app ./data/repo
```

Generate a password and record it in your password manager, then run HMD in the foreground:

```sh
export HMD_ADMIN_PASSWORD="$(openssl rand -base64 18)"
printf '%s\n' "$HMD_ADMIN_PASSWORD"
HMD_SERVER_BIND=127.0.0.1:8080 \
HMD_SERVER_REPO_DIR=./data/repo \
HMD_APP_DIR=./data/app \
HMD_ADMIN_USER=admin \
./hmd
```

In another terminal, check `curl -f http://127.0.0.1:8080/_/ready`, then open <http://127.0.0.1:8080> and sign in. Complete [[First-Run Setup]].

Stop HMD with **Ctrl+C** and run `unset HMD_ADMIN_PASSWORD`. On subsequent starts, run it without the bootstrap credentials, from the same `hmd` directory:

```sh
HMD_SERVER_BIND=127.0.0.1:8080 \
HMD_SERVER_REPO_DIR=./data/repo \
HMD_APP_DIR=./data/app \
./hmd
```

Both data directories must be private, owned by the account running HMD, and must not overlap. Keep their permissions at `0700`. For a long-running installation, use a dedicated service account and a process supervisor rather than leaving a terminal open.

## Before exposing HMD to a network

The examples above are local trials, not an internet-facing deployment. Before sharing the live wiki:

1. Put HTTPS in front of HMD and configure its public URL and trusted proxies: [[Reverse Proxies]].
2. Review accounts, permissions, and public namespaces: [[Authentication And Access]].
3. Back up both the content repository and application state, and test recovery: [[Storage And Recovery]].
4. Pin a release revision or image and plan upgrades: [[Upgrade HMD]].

You can add an HTTPS Git remote later with [[Git Sync]]. Search inside PDF and Office attachments is also optional; see [[Attachments]] for the Apache Tika requirements. Neither is needed for normal Markdown search.

## Common pitfalls

- **Port 8080 is already in use.** For Docker, change the first `8080` in the port mapping, for example `127.0.0.1:8081:8080`. For a binary, change `HMD_SERVER_BIND` to `127.0.0.1:8081`. Use the new port in the browser and readiness check too.
- **Startup reports an unsafe data directory.** Check that the service account owns both directories and they have mode `0700`. Do not loosen permissions to make startup succeed. Old root-owned container volumes need a planned recovery; see [[Storage And Recovery]].
- **The first account is not created.** Supply both bootstrap variables and a unique password of at least 12 characters. HMD rejects weak or recognised placeholder passwords. Check the startup logs for the specific reason.
- **The remote is unavailable.** A successful local save can still be waiting for a background push. A failed push and a failed page save are different problems; see [[Git Sync]].

## Stop or remove a local trial

For Docker, `docker compose -f compose.local.yaml down` stops the stack and keeps its named volumes. Do not add `--volumes` unless you intend to delete all of this installation's pages and accounts.

For a binary, stop the process. Remove `data/repo` and `data/app` only when you are sure you no longer need their contents or have a verified backup.

## Next steps

**Continue with [[First-Run Setup]], then [[Your First Wiki]].** If startup fails, use [[Troubleshooting]].
