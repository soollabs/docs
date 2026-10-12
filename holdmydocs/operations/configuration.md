---
title: Configuration
tags: hmd, operations
---

HMD separates local instance settings, portable wiki settings and personal preferences.

## Where settings live

Instance settings live in `config.yaml` inside `HMD_APP_DIR` by default. `HMD_CONFIG_FILE` chooses a different file. YAML is strict: unknown keys stop startup. Keys are grouped under `server`, `git`, `mcp`, `oidc` and `document_search`.

Scalar environment variables normally use `HMD_` plus the upper-case dotted key path with underscores: `server.bind` becomes `HMD_SERVER_BIND`. Lists have no environment equivalent. Environment values override file values and make their UI controls read-only. Exceptions and environment-only settings are listed in [[Configuration Reference]].

`.wiki.yaml` holds the site name and landing destination; each namespace's `.namespace.yaml` holds its visibility, appearance, navigation and quick-create defaults. These files travel with the content repository. Personal preferences live against the account in `users.json`.

## Settings pages

Open `/_/settings/server` and use the System navigation:

- **Server** — bind address, repository directory, public origin, trusted proxies, read-only mode, upload limit, default skin and debug logging.
- **Git** — HTTPS remote, user, token file path, default author, branch, sync mode and poll interval.
- **MCP** — MCP enablement and OAuth enablement, dynamic registration, insecure-loopback development and administrator delegation.
- **OIDC single sign-on** — non-secret provider and admission configuration, including the client secret file path.
- **Document search** — Tika endpoint, model and storage directories.
- **Wiki** — site name, landing destination and re-run setup.
- **Users** — account and scope management.
- **Environment overrides** — effective overrides and configuration export; secrets are never exported.

Each setting has an info icon with its description, environment variable, restart requirement and storage location. Restart-required icons use the warning colour. Saving writes non-secret settings to the file; Git remote, sync mode, upload limit and poll interval apply immediately. The Restart column in [[Configuration Reference]] lists which changes need a restart.

![Server settings with info icons](/_/attachments/holdmydocs/operations/configuration/server.png)

## Read-only mode

`server.read_only` blocks editing, uploads, setup and all settings saves, including attempts to turn it off in the UI. To restore writes, turn it off in `config.yaml` or `HMD_SERVER_READ_ONLY` and restart HMD. Application state and remote snapshots still need writable private storage in read-only mode. See [[Git Sync]].

## Document extraction (opt-in)

Set `document_search.tika_url` to a private Apache Tika Server and restart. You can set it on the Document search page or override it with `HMD_DOCUMENT_SEARCH_TIKA_URL`. HMD verifies the endpoint at startup, then stores its search index and downloaded embedding model under `HMD_APP_DIR` by default.

Extraction is serialised, times out after 60 seconds, skips embedded documents and accepts at most 8 MiB of extracted text. These limits do not constrain parser memory or CPU inside Tika: run it in a separate, private, resource-bounded sandbox. The bundled Compose file provides a `documents` profile.

## Secrets hygiene

Git and OIDC secrets cannot be stored in `config.yaml` or edited in the UI. Supply `HMD_GIT_TOKEN` or a private file referenced by `git.token_file`; supply `HMD_OIDC_CLIENT_SECRET` or a private file referenced by `oidc.client_secret_file`. A legacy `git.token` file key is ignored; `oidc.client_secret` makes the file fail to load. Exporting configuration never writes secrets.

Keep account state, configuration, secret files and backups private. Secret file ownership, permissions and size rules are listed in [[Configuration Reference]]. Never paste a secret into a screenshot or commit it with the content repository.
