---
title: Configuration
tags: hmd, operations
---

This page explains where HMD keeps its settings, which ones you can change from the admin UI, which ones need a restart, and how to keep secrets out of the repository.

## Where settings live

Instance settings live in `config.yaml` inside `HMD_APP_DIR` by default. `HMD_CONFIG_FILE` chooses a different file. YAML is strict: an unknown key stops startup.

Every scalar YAML key has an environment equivalent formed as `HMD_` plus the upper-case key path, for example `git.remote_url` becomes `HMD_GIT_REMOTE_URL`. An environment value wins over the file and is read-only in the admin UI, where it carries a "set via HMD_X" badge. YAML list values such as `trusted_proxies` have no environment form.

`HMD_APP_DIR` and `HMD_CONFIG_FILE` are environment-only because they locate the configuration itself. Bootstrap credentials (`HMD_ADMIN_USER`, `HMD_ADMIN_PASSWORD`) are environment-only too, and are used only on the first start. See [[Configuration Reference]] for the full key table.

## The admin UI

Open `/_/admin` to configure the content repository, Git remote, upload limit, and sync mode. Saving the form writes `config.yaml` and applies the changes immediately; the UI marks the fields that need a restart:

- **server** — bind address and repository directory. Both require a restart; the app directory is shown read-only.
- **git remote** — remote URL, user, default author, token, and sync mode. Saving reconfigures the live repository and shows the current sync state.
- **behaviour** — maximum upload size, sync poll interval, and the read-only document extraction endpoint.
- **users** — bootstrap admin details and user management.

OIDC, MCP enablement, and the document-search model and index directories are not editable from the UI. Set them in `config.yaml` or via environment variables and restart.



## Restart-requiring settings

| Setting | Applies |
| --- | --- |
| `bind`, `repo_dir`, `HMD_APP_DIR` | Restart |
| Git remote, user, author, token | Immediately |
| `sync_mode`, `max_upload_bytes`, `sync_poll_ms` | Immediately |
| OIDC (all keys) | Restart |
| `mcp.enabled` | Restart |
| `HMD_TIKA_URL` | Restart |
| `document_search.model`, `model_dir`, `index_dir` | Restart |

## Document extraction (opt-in)

Document extraction is disabled until you set the environment-only `HMD_TIKA_URL` to a private Apache Tika Server and restart. HMD verifies the endpoint at startup, then stores its search index and downloaded embedding model under `HMD_APP_DIR` by default.

Extraction is serialised, times out after 60 seconds, skips embedded documents, and accepts at most 8 MiB of extracted text. These client-side limits do not constrain parser memory or CPU inside Tika, so Tika still needs its own private, resource-bounded sandbox — the bundled Compose file provides one under the `documents` profile. See [[Install HMD]].

## Secrets hygiene

Keep secrets out of committed files. `users.json`, `config.yaml`, and any secret files referenced by configuration are sensitive. Prefer a secret file (`git.token_file`, `oidc.client_secret_file`), a Docker secret, or a secret-injection environment variable over a literal token in `config.yaml`. Full keys and file rules: [[Configuration Reference]].
